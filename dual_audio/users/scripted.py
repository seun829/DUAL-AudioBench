from __future__ import annotations

from dual_audio.core.conditions import Condition, condition_turns
from dual_audio.core.environment import post_gap_observation


class ScriptedUserSimulator:
    """Deterministic task- and state-conditioned user simulator."""

    def pre_gap_turns(self, task: dict, condition: Condition) -> list[dict]:
        """Return turns before the model-controlled pre-gap action marker."""

        turns = condition_turns(task, condition)
        marker = next(
            i for i, turn in enumerate(turns) if turn["kind"] == "pre_gap_action"
        )
        return turns[:marker]

    def acknowledgement(self, task: dict, condition: Condition) -> dict:
        """Return the deterministic user turn immediately after that action."""

        turns = condition_turns(task, condition)
        marker = next(
            i for i, turn in enumerate(turns) if turn["kind"] == "pre_gap_action"
        )
        return turns[marker + 1]

    def post_gap(self, task: dict, state: dict) -> str:
        """Describe the actual post-transition state in deterministic language."""

        return post_gap_observation(task["domain"], state)
