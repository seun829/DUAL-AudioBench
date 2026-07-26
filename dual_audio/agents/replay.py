from __future__ import annotations

import json
import re
from pathlib import Path
from types import ModuleType

from dual_audio.core.types import AgentResponse, Observation
from dual_audio.modalities.audio import combine_wavs


def _dialogue_prompt(observation: Observation) -> str:
    """Build the constrained natural-response instruction for filler turns."""

    return (
        "Respond naturally and concisely to the latest user audio. "
        f"Follow this dialogue intent: {observation.instruction}"
    )


def _decision_prompt(observation: Observation) -> str:
    """Build a JSON-only prompt from public descriptions and randomized labels."""

    options = "\n".join(
        f"{item['label']}. {item['description']}" for item in observation.action_menu
    )
    style = ""
    schema = '{"choice": "A"}'
    if observation.style_menu:
        style_options = "\n".join(
            f"{item['label']}. {item['description']}" for item in observation.style_menu
        )
        style = f"\n\nResponse approach:\n{style_options}"
        schema = '{"choice": "A", "response_style": "X"}'
    return (
        "Choose the single best next action from the equally plausible options below. "
        "Use the conversation and current observation; option order is randomized.\n\n"
        f"{options}{style}\n\nReturn JSON only in this form: {schema}"
    )


def _transcript_prompt(observation: Observation, history: list[dict]) -> str:
    """Serialize visible conversation history for the transcript control."""

    lines = []
    for turn in history:
        speaker = "User" if turn["role"] == "user" else "Agent"
        lines.append(f"{speaker}: {turn.get('text', '')}")
    lines.append(f"User: {observation.text}")
    instruction = (
        _dialogue_prompt(observation)
        if observation.stage == "dialogue"
        else _decision_prompt(observation)
    )
    return "\n".join(lines) + "\n\n" + instruction


def _extract_label(raw: str, key: str, labels: set[str]) -> str | None:
    """Parse a permitted public label from JSON, with a strict text fallback."""

    try:
        parsed = json.loads(raw)
        value = str(parsed.get(key, "")).strip()
        if value in labels:
            return value
    except (json.JSONDecodeError, TypeError):
        pass
    for label in sorted(labels, key=len, reverse=True):
        if re.search(rf"\b{re.escape(label)}\b", raw):
            return label
    return None


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

        instruction = (
            _dialogue_prompt(observation)
            if observation.stage == "dialogue"
            else _decision_prompt(observation)
        )
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

        action_labels = {item["label"] for item in observation.action_menu}
        style_labels = {item["label"] for item in observation.style_menu}
        return AgentResponse(
            action=_extract_label(raw, "choice", action_labels),
            response_style=(
                _extract_label(raw, "response_style", style_labels)
                if style_labels
                else None
            ),
            raw=raw,
        )
