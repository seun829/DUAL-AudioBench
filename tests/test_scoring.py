from __future__ import annotations

import unittest

from score import summarize


class ScoringTests(unittest.TestCase):
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
                    }
                )
        stats = summarize(rows)
        self.assertAlmostEqual(stats["pass1"], 0.6)
        self.assertAlmostEqual(stats["trajectory_chance"], 1 / 25)
        self.assertAlmostEqual(stats["action_chance"], 1 / 5)
        self.assertAlmostEqual(stats["majority"], 0.5)
        self.assertAlmostEqual(stats["all_trials"], 0.5)
        self.assertEqual(stats["pass_at_5"], 1.0)


if __name__ == "__main__":
    unittest.main()
