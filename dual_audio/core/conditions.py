from __future__ import annotations

import copy
from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    """A controlled intervention on task presentation or world evolution.

    Conditions are intentionally declarative. The user simulator and runner
    interpret these fields so paired conditions can share every non-target
    factor, especially menu contents and randomization.
    """

    name: str
    modality: str = "audio"
    apply_external_event: bool = True
    clue_mode: str = "original"
    prosody_variant: str = "native"
    score_style: bool = False


CONDITIONS = {
    "full_audio": Condition("full_audio"),
    "gap_no_state_change": Condition(
        "gap_no_state_change", apply_external_event=False
    ),
    "state_change_short": Condition(
        "state_change_short", clue_mode="move_to_end"
    ),
    "clue_removed": Condition("clue_removed", clue_mode="ablate"),
    "transcript_only": Condition("transcript_only", modality="transcript"),
    "neutral_audio": Condition("neutral_audio", prosody_variant="neutral"),
    "prosody_high": Condition(
        "prosody_high", prosody_variant="high", score_style=True
    ),
    "prosody_low": Condition(
        "prosody_low", prosody_variant="low", score_style=True
    ),
}

CONTROL_CONDITIONS = tuple(CONDITIONS)


def condition_turns(task: dict, condition: Condition) -> list[dict]:
    """Return a copied turn sequence after applying the condition's clue edit.

    ``ablate`` replaces clue content without changing turn count.
    ``move_to_end`` relocates the clue prompt/response pair directly before the
    pre-gap decision while preserving the rest of the conversation.
    """

    turns = copy.deepcopy(task["turns"])
    if condition.clue_mode == "ablate":
        for turn in turns:
            if turn.get("kind") == "clue":
                turn["text"] = task["clue_ablation_text"]
                turn["kind"] = "clue_ablation"
    elif condition.clue_mode == "move_to_end":
        clue_pair = [
            turn for turn in turns if turn.get("kind") in {"clue_prompt", "clue"}
        ]
        turns = [
            turn for turn in turns if turn.get("kind") not in {"clue_prompt", "clue"}
        ]
        # The stored index refers to the unmodified list. Recompute using the
        # explicit pre-gap marker after removing the original clue pair.
        insert_at = next(
            i for i, turn in enumerate(turns) if turn.get("kind") == "pre_gap_action"
        )
        turns[insert_at:insert_at] = clue_pair
    return turns


def prosody_for(task: dict, condition: Condition) -> tuple[str, str | None]:
    """Resolve post-gap delivery and, for contrastive pairs, the gold style."""

    pair = task["prosody_pair"]
    if condition.prosody_variant == "high":
        return pair["high"]["prosody"], pair["high"]["expected_style"]
    if condition.prosody_variant == "low":
        return pair["low"]["prosody"], pair["low"]["expected_style"]
    if condition.prosody_variant == "neutral":
        return "neutral", None
    return pair["native_prosody"], None
