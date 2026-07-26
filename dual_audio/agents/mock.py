from __future__ import annotations

import hashlib
import random

from dual_audio.core.types import AgentResponse, Observation


P_CORRECT = {
    "1-2": 0.92,
    "5-8": 0.72,
    "12-20": 0.45,
}


def _rng(*parts: object) -> random.Random:
    """Create a process-independent RNG from stable benchmark identifiers."""

    digest = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return random.Random(digest)


class MockAgent:
    """Deterministic dry-run agent.

    It deliberately uses runner-private oracle labels. This makes it useful for
    exercising the benchmark mechanics, but it is not a scientific baseline.
    """

    def respond(self, observation: Observation, history: list[dict]) -> AgentResponse:
        """Return deterministic oracle-biased choices for pipeline validation."""

        if observation.stage == "dialogue":
            return AgentResponse(message=observation.instruction or "Please continue.")

        private = observation.private
        rng = _rng(
            private.get("scenario_id"),
            private.get("seed"),
            observation.stage,
        )
        expected = private["expected_action_label"]
        probability = P_CORRECT.get(private.get("bucket"), 0.7)
        if private.get("condition") == "clue_removed":
            probability = max(0.2, probability - 0.35)

        labels = [item["label"] for item in observation.action_menu]
        action = expected if rng.random() < probability else rng.choice(
            [label for label in labels if label != expected]
        )

        style = None
        if observation.style_menu:
            expected_style = private["expected_style_label"]
            style_labels = [item["label"] for item in observation.style_menu]
            style = expected_style if rng.random() < 0.85 else rng.choice(
                [label for label in style_labels if label != expected_style]
            )
        return AgentResponse(action=action, response_style=style)
