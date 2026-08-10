from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from dual_audio.core.conditions import CONDITIONS, condition_turns
from dual_audio.core.environment import execute_action, transition
from dual_audio.core.types import AgentResponse
from dual_audio.interaction.runner import ClosedLoopRunner
from scenarios.generate import BUCKETS, build


class OracleAgent:
    def __init__(self, wrong_pre_description: str | None = None):
        self.wrong_pre_description = wrong_pre_description

    def respond(self, observation, history):
        if observation.stage == "dialogue":
            return AgentResponse(message=observation.instruction)
        belief = {
            variable: {
                value: (
                    1.0
                    if value == str(observation.private["belief_targets"][variable])
                    else 0.0
                )
                for value in values
            }
            for variable, values in observation.belief_schema.items()
        }
        action = observation.private.get("expected_action_label")
        if not observation.action_menu:
            action = None
        elif observation.stage == "pre_gap" and self.wrong_pre_description:
            action = next(
                item["label"]
                for item in observation.action_menu
                if self.wrong_pre_description.lower()
                in item["description"].lower()
            )
        return AgentResponse(
            action=action,
            response_style=observation.private.get("expected_style_label"),
            state_belief=belief,
            needs_revalidation=False,
        )


class GeneratorTests(unittest.TestCase):
    def test_recorded_distance_is_calculated_from_turns(self):
        for domain in ("router", "pharmacy", "flight"):
            for bucket, (low, high) in BUCKETS.items():
                for variant in range(4):
                    task = build(domain, bucket, variant)
                    clue_index = next(
                        i
                        for i, turn in enumerate(task["turns"])
                        if turn["kind"] == "clue"
                    )
                    actual = len(task["turns"]) - clue_index - 1
                    self.assertEqual(actual, task["clue_turn_distance"])
                    self.assertGreaterEqual(actual, low)
                    self.assertLessEqual(actual, high)
                    for index, turn in enumerate(task["turns"]):
                        self.assertEqual(
                            turn["speaker"], "user" if index % 2 == 0 else "agent"
                        )

    def test_ablation_preserves_menu_and_turn_count(self):
        task = build("router", "12-20", 0)
        original = condition_turns(task, CONDITIONS["full_audio"])
        ablated = condition_turns(task, CONDITIONS["clue_removed"])
        self.assertEqual(len(original), len(ablated))
        self.assertEqual(task["post_gap_actions"], task["post_gap_actions"])
        clue = next(turn for turn in ablated if turn["kind"] == "clue_ablation")
        self.assertNotIn("outage", clue["text"].lower())


class TransitionTests(unittest.TestCase):
    def test_router_transition_is_deterministic_and_action_dependent(self):
        task = build("router", "5-8", 0)
        started = execute_action(
            task["domain"], task["initial_state"], "run_maintenance"
        )
        args = (
            task["domain"],
            started,
            "run_maintenance",
            task["transition"]["elapsed_minutes"],
            task["transition"]["external_event"],
        )
        first = transition(*args)
        second = transition(*args)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(first["firmware_status"], "stuck")
        self.assertEqual(first["firmware_progress"], 47)

        no_action = transition(
            task["domain"],
            copy.deepcopy(task["initial_state"]),
            "invalid_action",
            task["transition"]["elapsed_minutes"],
            task["transition"]["external_event"],
        )
        self.assertEqual(no_action["firmware_status"], "not_started")

    def test_no_event_does_not_apply_world_change(self):
        task = build("pharmacy", "1-2", 0)
        state = execute_action(task["domain"], task["initial_state"], "submit_claim")
        updated = transition(
            task["domain"],
            state,
            "submit_claim",
            task["transition"]["elapsed_minutes"],
            None,
        )
        self.assertEqual(updated["claim_status"], "processing")
        self.assertEqual(updated["elapsed_minutes"], 20)

    def test_external_event_updates_other_domains(self):
        pharmacy = build("pharmacy", "1-2", 0)
        state = execute_action(
            pharmacy["domain"], pharmacy["initial_state"], "submit_claim"
        )
        updated = transition(
            pharmacy["domain"],
            state,
            "submit_claim",
            20,
            pharmacy["transition"]["external_event"],
        )
        self.assertEqual(updated["claim_status"], "rejected")

        flight = build("flight", "1-2", 0)
        state = execute_action(
            flight["domain"],
            flight["initial_state"],
            "enable_itinerary_monitoring",
        )
        updated = transition(
            flight["domain"],
            state,
            "enable_itinerary_monitoring",
            45,
            flight["transition"]["external_event"],
        )
        self.assertEqual(updated["departure_delay_minutes"], 120)
        self.assertEqual(updated["connection_status"], "missed")

    def test_hidden_user_action_is_a_deterministic_transition_input(self):
        task = build("router", "1-2", 0)
        state = execute_action(
            task["domain"], task["initial_state"], "run_maintenance"
        )
        args = (
            task["domain"],
            state,
            "run_maintenance",
            30,
            task["transition"]["external_event"],
            task["transition"]["user_action"],
        )
        first = transition(*args)
        second = transition(*args)
        self.assertEqual(first, second)
        self.assertEqual(first["firmware_status"], "interrupted")
        self.assertIn(
            "power_cycle_during_maintenance",
            first["user_action_history"],
        )


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.runner = ClosedLoopRunner(audio_renderer=None)

    def test_agent_controls_pre_gap_action_and_transition(self):
        task = build("router", "5-8", 0)
        result = self.runner.execute(
            OracleAgent(), task, CONDITIONS["full_audio"], seed=3
        )
        self.assertTrue(result["pre_gap_success"])
        self.assertEqual(result["state_before_gap"]["firmware_status"], "updating")
        self.assertEqual(result["state_after_gap"]["firmware_status"], "stuck")
        self.assertTrue(result["post_gap_success"])
        self.assertTrue(result["trajectory_success"])
        self.assertGreater(len(result["model_calls"]), 2)
        self.assertEqual(set(result["belief_checkpoints"]), {
            "pre_gap",
            "post_observation",
            "pre_final_action",
        })
        self.assertTrue(result["state_belief_success"])
        self.assertGreater(result["belief_revision"]["mean_revision_gain"], 0)

    def test_wrong_pre_gap_action_changes_resumed_world(self):
        task = build("router", "5-8", 0)
        result = self.runner.execute(
            OracleAgent("power recovery"),
            task,
            CONDITIONS["full_audio"],
            seed=3,
        )
        self.assertFalse(result["pre_gap_success"])
        self.assertEqual(result["state_after_gap"]["firmware_status"], "not_started")
        self.assertIn("never started", result["post_gap_observation"])
        self.assertEqual(result["expected_post_gap_action"], "run_maintenance")

    def test_controls_share_menu_order(self):
        task = build("flight", "12-20", 0)
        full = self.runner.execute(
            OracleAgent(), task, CONDITIONS["full_audio"], seed=4
        )
        ablated = self.runner.execute(
            OracleAgent(), task, CONDITIONS["clue_removed"], seed=4
        )
        self.assertEqual(full["post_gap_menu"], ablated["post_gap_menu"])
        self.assertEqual(
            full["clue_turn_distance"], ablated["effective_clue_turn_distance"]
        )

    def test_short_distance_and_prosodic_pair(self):
        task = build("pharmacy", "12-20", 0)
        short = self.runner.execute(
            OracleAgent(), task, CONDITIONS["state_change_short"], seed=1
        )
        self.assertEqual(short["effective_clue_turn_distance"], 2)

        high = self.runner.execute(
            OracleAgent(), task, CONDITIONS["prosody_high"], seed=1
        )
        low = self.runner.execute(
            OracleAgent(), task, CONDITIONS["prosody_low"], seed=1
        )
        self.assertEqual(
            high["post_gap_observation"], low["post_gap_observation"]
        )
        self.assertNotEqual(high["post_gap_prosody"], low["post_gap_prosody"])
        self.assertNotEqual(
            high["expected_response_style"], low["expected_response_style"]
        )
        self.assertTrue(high["response_style_success"])
        self.assertTrue(low["response_style_success"])
        self.assertEqual(
            [item["label"] for item in high["response_style_menu"]],
            list("WXYZ"),
        )

    def test_hidden_user_action_changes_shared_world_and_answer(self):
        task = build("flight", "5-8", 0)
        full = self.runner.execute(
            OracleAgent(), task, CONDITIONS["full_audio"], seed=2
        )
        dual = self.runner.execute(
            OracleAgent(), task, CONDITIONS["hidden_user_action"], seed=2
        )
        self.assertEqual(full["state_after_gap"]["connection_status"], "missed")
        self.assertEqual(
            dual["state_after_gap"]["connection_status"], "protected"
        )
        self.assertEqual(
            dual["gap_user_action"]["action"],
            "self_protect_onward_segment",
        )
        self.assertEqual(
            dual["state_after_user_action"]["connection_status"],
            "protected",
        )
        self.assertIn("I changed my later flight", dual["post_gap_observation"])
        self.assertEqual(
            dual["expected_post_gap_action"],
            "enable_itinerary_monitoring",
        )
        self.assertNotEqual(
            full["expected_post_gap_action"],
            dual["expected_post_gap_action"],
        )


if __name__ == "__main__":
    unittest.main()
