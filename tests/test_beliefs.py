from __future__ import annotations

import unittest

from dual_audio.core.beliefs import (
    evaluate_state_belief,
    normalize_state_belief,
)
from dual_audio.core.types import AgentResponse
from dual_audio.interaction.runner import _belief_checkpoint
from scenarios.generate import build


class BeliefTests(unittest.TestCase):
    def test_distribution_validation_and_scoring(self):
        schema = {"status": ("waiting", "done", "failed")}
        normalized = normalize_state_belief(
            {"status": {"waiting": 1, "done": 3, "failed": 0}},
            schema,
        )
        self.assertEqual(normalized["status"]["done"], 0.75)
        scored = evaluate_state_belief(
            normalized,
            schema,
            {"status": "done"},
        )
        self.assertTrue(scored["valid"])
        self.assertTrue(scored["all_correct"])
        self.assertAlmostEqual(
            scored["variables"]["status"]["target_probability"],
            0.75,
        )

        invalid = normalize_state_belief(
            {"status": {"waiting": -1, "done": 2}},
            schema,
        )
        self.assertEqual(invalid, {})

    def test_belief_action_failure_matrix(self):
        task = build("router", "1-2", 0)
        state = dict(task["initial_state"])

        correct_belief = AgentResponse(
            state_belief={
                "firmware_status": {
                    "not_started": 0.8,
                    "updating": 0.05,
                    "stuck": 0.05,
                    "completed": 0.05,
                    "interrupted": 0.05,
                }
            },
            needs_revalidation=False,
        )
        correct_belief_wrong_action = _belief_checkpoint(
            task,
            state,
            correct_belief,
            selected_action="close_case",
            expected_action="run_maintenance",
        )
        self.assertEqual(
            correct_belief_wrong_action["belief_action_outcome"],
            "ACTION_SELECTION_FAILURE",
        )

        wrong_belief = AgentResponse(
            state_belief={
                "firmware_status": {
                    "not_started": 0.1,
                    "updating": 0.1,
                    "stuck": 0.7,
                    "completed": 0.05,
                    "interrupted": 0.05,
                }
            },
            needs_revalidation=False,
        )
        wrong_belief_correct_action = _belief_checkpoint(
            task,
            state,
            wrong_belief,
            selected_action="run_maintenance",
            expected_action="run_maintenance",
        )
        self.assertEqual(
            wrong_belief_correct_action["belief_action_outcome"],
            "LUCKY_ACTION",
        )
        self.assertFalse(
            wrong_belief_correct_action["action_belief_consistent"]
        )

    def test_uncertain_revalidation_is_identified(self):
        task = build("pharmacy", "1-2", 0)
        state = dict(task["initial_state"])
        state["claim_status"] = "rejected"
        response = AgentResponse(
            state_belief={
                "claim_status": {
                    "not_submitted": 0.2,
                    "processing": 0.2,
                    "rejected": 0.4,
                    "approved": 0.2,
                }
            },
            needs_revalidation=True,
        )
        checkpoint = _belief_checkpoint(
            task,
            state,
            response,
            selected_action="review_account_configuration",
            expected_action="review_account_configuration",
        )
        self.assertTrue(checkpoint["low_confidence"])
        self.assertTrue(checkpoint["risk_calibration_consistent"])
        self.assertEqual(
            checkpoint["uncertainty_behavior"],
            "UNCERTAIN_RECHECKED",
        )


if __name__ == "__main__":
    unittest.main()
