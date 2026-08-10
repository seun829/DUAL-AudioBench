from __future__ import annotations

import unittest

from score import (
    expected_calibration_error,
    paired_cluster_effect,
    summarize,
    summarize_prosody,
)


class ScoringTests(unittest.TestCase):
    def test_expected_calibration_error(self):
        perfectly_calibrated = [(1.0, True), (0.0, False)]
        self.assertAlmostEqual(
            expected_calibration_error(perfectly_calibrated),
            0.0,
        )
        overconfident = [(0.9, False), (0.9, False)]
        self.assertAlmostEqual(
            expected_calibration_error(overconfident),
            0.9,
        )

    def test_dynamic_chance_and_reliability_metrics(self):
        rows = []
        outcomes = {
            "scenario_a": [True, True, True, True, True],
            "scenario_b": [True, False, False, False, False],
        }
        for scenario_id, values in outcomes.items():
            for seed, success in enumerate(values):
                rows.append(
                    {
                        "scenario_id": scenario_id,
                        "seed": seed,
                        "trajectory_success": success,
                        "pre_gap_success": success,
                        "post_gap_success": success,
                        "pre_gap_menu_size": 5,
                        "post_gap_menu_size": 5,
                        "response_style_menu_size": 1,
                        "belief_checkpoint_chance": 1 / 4,
                    }
                )
        stats = summarize(rows)
        self.assertAlmostEqual(stats["pass1"], 0.6)
        self.assertAlmostEqual(stats["two_action_chance"], 1 / 25)
        self.assertAlmostEqual(stats["action_trajectory_chance"], 1 / 25)
        self.assertAlmostEqual(
            stats["trajectory_chance"],
            (1 / 25) * (1 / 4) ** 3,
        )
        self.assertAlmostEqual(stats["action_chance"], 1 / 5)
        self.assertAlmostEqual(stats["majority"], 0.5)
        self.assertAlmostEqual(stats["all_trials"], 0.5)
        self.assertEqual(stats["pass_at_5"], 1.0)

    def test_pass_at_k_uses_the_number_of_available_trials(self):
        rows = []
        for seed, success in enumerate((False, True)):
            rows.append(
                {
                    "scenario_id": "scenario_a",
                    "domain": "domain_a",
                    "seed": seed,
                    "trajectory_success": success,
                    "pre_gap_success": success,
                    "post_gap_success": success,
                    "pre_gap_menu_size": 5,
                    "post_gap_menu_size": 5,
                    "response_style_menu_size": 1,
                    "belief_checkpoint_chance": 1 / 4,
                }
            )
        stats = summarize(rows)
        self.assertEqual(stats["pass_k"], 2)
        self.assertEqual(stats["pass_at_k"], 1.0)
        self.assertIsNone(stats["pass_at_5"])

    def test_paired_effect_weights_domains_not_sibling_scenarios(self):
        rows = []
        for index in range(6):
            for condition, success in (("left", True), ("right", False)):
                rows.append(
                    {
                        "scenario_id": f"a_{index}",
                        "domain": "domain_a",
                        "seed": 0,
                        "condition": condition,
                        "metric": success,
                    }
                )
        for condition, success in (("left", False), ("right", True)):
            rows.append(
                {
                    "scenario_id": "b_0",
                    "domain": "domain_b",
                    "seed": 0,
                    "condition": condition,
                    "metric": success,
                }
            )
        effect = paired_cluster_effect(rows, "left", "right", "metric")
        self.assertEqual(effect["paired_n"], 7)
        self.assertEqual(effect["clusters"], 2)
        self.assertAlmostEqual(effect["delta"], 0.0)

    def test_prosody_pair_chance_uses_both_four_way_menus(self):
        rows = []
        for condition in ("prosody_high", "prosody_low"):
            rows.append(
                {
                    "scenario_id": "scenario_a",
                    "domain": "domain_a",
                    "seed": 0,
                    "condition": condition,
                    "post_gap_observation": "same words",
                    "post_gap_prosody": (
                        "urgent" if condition == "prosody_high" else "calm"
                    ),
                    "response_style": "chosen",
                    "expected_response_style": "chosen",
                    "response_style_success": True,
                    "response_style_menu_size": 4,
                    "post_gap_action": "same_action",
                    "prosody_stimulus_id": "stimulus_a",
                    "belief_checkpoints": {
                        checkpoint: {"state_belief": {"state": {"ok": 1.0}}}
                        for checkpoint in (
                            "post_observation",
                            "pre_final_action",
                        )
                    },
                }
            )
        stats = summarize_prosody(rows)
        self.assertAlmostEqual(stats["both_style_random_chance"], 1 / 16)


if __name__ == "__main__":
    unittest.main()
