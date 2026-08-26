from __future__ import annotations

import unittest

from dual_audio.agents.replay import _belief_prompt, _decision_prompt
from dual_audio.core.types import Observation


class BeliefPromptTests(unittest.TestCase):
    def setUp(self):
        self.schema = {
            "connection_status": (
                "at_risk_if_delayed",
                "missed",
                "protected",
                "viable",
            )
        }

    def test_belief_prompt_defines_every_connection_state(self):
        prompt = _belief_prompt(
            Observation(
                text="The flight is delayed.",
                stage="post_gap_belief",
                belief_schema=self.schema,
            )
        )

        self.assertIn("State values and operational definitions", prompt)
        self.assertIn("at_risk_if_delayed:", prompt)
        self.assertIn("sufficiently long departure delay", prompt)
        self.assertIn("missed:", prompt)
        self.assertIn("at least the layover time", prompt)
        self.assertIn("protected:", prompt)
        self.assertIn("confirmed protection/rebooking", prompt)
        self.assertIn("viable:", prompt)
        self.assertIn("remains feasible", prompt)

    def test_decision_prompt_uses_the_same_definitions(self):
        prompt = _decision_prompt(
            Observation(
                text="",
                stage="post_gap",
                action_menu=(
                    {"label": "A", "description": "Continue monitoring."},
                ),
                belief_schema=self.schema,
            )
        )

        self.assertIn("State values and operational definitions", prompt)
        self.assertIn("at least the layover time", prompt)
        self.assertIn("confirmed protection/rebooking", prompt)

    def test_unknown_schema_values_still_appear_without_invented_meaning(self):
        prompt = _belief_prompt(
            Observation(
                text="",
                stage="post_gap_belief",
                belief_schema={"custom_status": ("waiting", "done")},
            )
        )

        self.assertIn("- custom_status:", prompt)
        self.assertIn("  - waiting", prompt)
        self.assertIn("  - done", prompt)


if __name__ == "__main__":
    unittest.main()
