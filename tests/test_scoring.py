from __future__ import annotations

import unittest

from score import expected_calibration_error, summarize


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


if __name__ == "__main__":
    unittest.main()
