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
        probability = P_CORRECT.get(private.get("bucket"), 0.7)
        if private.get("condition") == "clue_removed":
            probability = max(0.2, probability - 0.35)

        state_belief: dict[str, dict[str, float]] = {}
        confidences = []
        for variable, allowed_values in observation.belief_schema.items():
            values = list(allowed_values)
            target = str(private["belief_targets"][variable])
            uncertain = rng.random() < 0.12
            belief_correct = rng.random() < probability
            if uncertain:
                target_probability = 0.45
                remainder = (1.0 - target_probability) / (len(values) - 1)
                distribution = {
                    value: target_probability if value == target else remainder
                    for value in values
                }
            elif belief_correct:
                target_probability = 0.78
                remainder = (1.0 - target_probability) / (len(values) - 1)
                distribution = {
                    value: target_probability if value == target else remainder
                    for value in values
                }
            else:
                wrong = rng.choice([value for value in values if value != target])
                distribution = {
                    value: (
                        0.68
                        if value == wrong
                        else 0.12
                        if value == target
                        else 0.20 / (len(values) - 2)
                    )
                    for value in values
                }
            state_belief[variable] = distribution
            confidences.append(max(distribution.values()))

        action = None
        if observation.action_menu:
            expected = private["expected_action_label"]
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
        return AgentResponse(
            action=action,
            response_style=style,
            state_belief=state_belief,
            needs_revalidation=(
                sum(confidences) / len(confidences) < 0.60
                if confidences
                else None
            ),
        )
