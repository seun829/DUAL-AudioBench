from __future__ import annotations

import json
import re
from pathlib import Path
from types import ModuleType

from dual_audio.core.beliefs import normalize_state_belief
from dual_audio.core.types import AgentResponse, Observation
from dual_audio.modalities.audio import combine_wavs


def _dialogue_prompt(observation: Observation) -> str:
    """Build the constrained natural-response instruction for filler turns."""

    return (
        "Respond naturally and concisely to the latest user audio. "
        f"Follow this dialogue intent: {observation.instruction}"
    )


def _decision_prompt(observation: Observation) -> str:
    """Build a JSON-only action, belief, and revalidation prompt."""

    options = "\n".join(
        f"{item['label']}. {item['description']}" for item in observation.action_menu
    )
    style = ""
    example = {
        "state_belief": {
            variable: {
                value: round(1 / len(values), 3) for value in values
            }
            for variable, values in observation.belief_schema.items()
        },
        "needs_revalidation": False,
        "choice": "A",
    }
    if observation.style_menu:
        style_options = "\n".join(
            f"{item['label']}. {item['description']}" for item in observation.style_menu
        )
        style = f"\n\nResponse approach:\n{style_options}"
        example["response_style"] = "X"
    belief_values = "\n".join(
        f"- {variable}: {', '.join(values)}"
        for variable, values in observation.belief_schema.items()
    )
    prior_belief = ""
    if observation.prior_state_belief:
        prior_belief = (
            "\n\nYour belief-only report immediately after the resumed "
            f"evidence was: {json.dumps(observation.prior_state_belief)}. "
            "Reconsider it if needed before returning the final action."
        )
    return (
        "Choose the single best next action from the equally plausible options below. "
        "Also report a probability distribution over every allowed hidden-state "
        "value and whether more verification is needed. Probabilities for each "
        "variable must be non-negative and sum to 1. Use only the listed state "
        "values and public option labels.\n\n"
        f"State variables:\n{belief_values}{prior_belief}\n\n"
        f"Actions:\n{options}{style}\n\n"
        f"Return JSON only in this shape: {json.dumps(example)}"
    )


def _belief_prompt(observation: Observation) -> str:
    """Build the belief-only checkpoint immediately after resumed evidence."""

    example = {
        "state_belief": {
            variable: {
                value: round(1 / len(values), 3) for value in values
            }
            for variable, values in observation.belief_schema.items()
        },
        "needs_revalidation": False,
    }
    values = "\n".join(
        f"- {variable}: {', '.join(allowed)}"
        for variable, allowed in observation.belief_schema.items()
    )
    return (
        "Update your hidden-state belief after the latest user evidence. "
        "Do not choose an action yet. Give a probability distribution for every "
        "variable; each distribution must sum to 1. Indicate whether you need "
        f"more verification.\n\nState variables:\n{values}\n\n"
        f"Return JSON only in this shape: {json.dumps(example)}"
    )


def _instruction(observation: Observation) -> str:
    """Select the prompt family for the current interaction checkpoint."""

    if observation.stage == "dialogue":
        return _dialogue_prompt(observation)
    if observation.stage == "post_gap_belief":
        return _belief_prompt(observation)
    return _decision_prompt(observation)


def _transcript_prompt(observation: Observation, history: list[dict]) -> str:
    """Serialize visible conversation history for the transcript control."""

    lines = []
    for turn in history:
        speaker = "User" if turn["role"] == "user" else "Agent"
        lines.append(f"{speaker}: {turn.get('text', '')}")
    if observation.text:
        lines.append(f"User: {observation.text}")
    return "\n".join(lines) + "\n\n" + _instruction(observation)


def _parse_json(raw: str) -> dict:
    """Parse a top-level JSON object or return an empty object."""

    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except (json.JSONDecodeError, TypeError):
        return {}


def _extract_label(
    raw: str,
    parsed: dict,
    key: str,
    labels: set[str],
) -> str | None:
    """Parse a permitted public label from JSON, with a strict text fallback."""

    value = str(parsed.get(key, "")).strip()
    if value in labels:
        return value
    for label in sorted(labels, key=len, reverse=True):
        if re.search(rf"\b{re.escape(label)}\b", raw):
            return label
    return None


def _extract_bool(parsed: dict, key: str) -> bool | None:
    """Return a literal JSON boolean without coercing strings or numbers."""

    value = parsed.get(key)
    return value if isinstance(value, bool) else None


class ReplayModelAgent:
    """Adapter for the repository's existing ``ask`` model modules.

    For audio conditions it replays the accumulated alternating-turn audio on
    every call. Earlier agent outputs therefore come from the evaluated model,
    not from the scenario recording. Transcript conditions use ``ask_text``.
    """

    def __init__(self, module: ModuleType, cache_dir: str | Path = "data/replay_audio"):
        self.module = module
        self.cache_dir = Path(cache_dir)

    def respond(self, observation: Observation, history: list[dict]) -> AgentResponse:
        """Replay audio or serialize text, invoke the model, and normalize output."""

        instruction = _instruction(observation)
        if observation.modality == "transcript":
            if not hasattr(self.module, "ask_text"):
                raise RuntimeError(
                    f"{self.module.__name__} does not implement ask_text(), "
                    "which is required for transcript_only."
                )
            raw = self.module.ask_text(_transcript_prompt(observation, history))
        else:
            paths = [
                Path(turn["audio_path"])
                for turn in history
                if turn.get("audio_path")
            ]
            if observation.audio_path:
                paths.append(observation.audio_path)
            if not paths:
                raise RuntimeError("Audio condition produced no turn audio.")
            replay = combine_wavs(paths, self.cache_dir)
            raw = self.module.ask(str(replay), instruction)

        if observation.stage == "dialogue":
            return AgentResponse(message=raw.strip(), raw=raw)

        parsed = _parse_json(raw)
        action_labels = {item["label"] for item in observation.action_menu}
        style_labels = {item["label"] for item in observation.style_menu}
        return AgentResponse(
            action=(
                _extract_label(raw, parsed, "choice", action_labels)
                if action_labels
                else None
            ),
            response_style=(
                _extract_label(
                    raw, parsed, "response_style", style_labels
                )
                if style_labels
                else None
            ),
            state_belief=normalize_state_belief(
                parsed.get("state_belief"),
                observation.belief_schema,
            ),
            needs_revalidation=_extract_bool(parsed, "needs_revalidation"),
            raw=raw,
        )
