from __future__ import annotations

from dual_audio.core.conditions import Condition, condition_turns
from dual_audio.core.environment import post_gap_observation


PROSODY_TRANSCRIPT_FRAMES = (
    "{observation}",
    "I am following up now. {observation}",
    "{observation} Please tell me the appropriate next step.",
)


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

    def post_gap(
        self,
        task: dict,
        state: dict,
        condition: Condition | None = None,
    ) -> str:
        """Describe the actual post-transition state in deterministic language."""

        observation = post_gap_observation(task["domain"], state)
        user_action_observation = state.get("gap_user_action_observation")
        if user_action_observation:
            observation = f"{user_action_observation} {observation}"
        causal = task.get("causal_post_gap_observation")
        if (
            causal
            and (condition is None or condition.apply_external_event)
            and not (condition and condition.apply_user_action)
            and state.get(causal["state_variable"]) in causal["hidden_values"]
        ):
            # Standard v0.5 pairs intentionally hide which terminal branch
            # occurred.  The earlier causal clue is the only distinguishing
            # public evidence.  Controls with no event or a hidden user action
            # retain the fully state-derived observation above.
            observation = causal["text"]
        if condition and condition.name in {"prosody_high", "prosody_low"}:
            index = int(
                task.get("prosody_stimulus", {}).get("transcript_variant", 0)
            )
            frame = PROSODY_TRANSCRIPT_FRAMES[index % len(PROSODY_TRANSCRIPT_FRAMES)]
            return frame.format(observation=observation)
        return observation
