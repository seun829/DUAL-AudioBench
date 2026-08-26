"""Scientific-quality contracts for the versioned schema-v0.4 benchmark."""

from __future__ import annotations

import unittest

from dual_audio.core.conditions import CONDITIONS, condition_turns, prosody_for
from dual_audio.core.environment import (
    correct_action,
    execute_action,
    transition,
)
from dual_audio.users.scripted import ScriptedUserSimulator
from scenarios.generate import build
from scenarios.templates import HIGH_STYLE_BY_PROSODY, TEMPLATES


class V04QualityTests(unittest.TestCase):
    def test_new_schema_has_distinct_ids_and_complete_belief_definitions(self):
        for name, template in TEMPLATES.items():
            task = build(name, "5-8", 0)
            with self.subTest(domain=template["domain"]):
                self.assertEqual(task["schema_version"], "0.4")
                self.assertTrue(task["scenario_id"].endswith("_s04"))
                self.assertEqual(
                    set(task["belief_definitions"]),
                    set(task["belief_schema"]),
                )
                for variable, values in task["belief_schema"].items():
                    self.assertEqual(
                        set(task["belief_definitions"][variable]), set(values)
                    )
                    self.assertTrue(
                        all(task["belief_definitions"][variable].values())
                    )

    def test_clue_ablation_withholds_information_without_asserting_the_opposite(self):
        uncertainty_markers = ("not sure", "do not have", "cannot confirm")
        for name in TEMPLATES:
            task = build(name, "5-8", 0)
            ablation = task["clue_ablation_text"].lower()
            with self.subTest(domain=task["domain"]):
                self.assertTrue(any(marker in ablation for marker in uncertainty_markers))
                full = condition_turns(task, CONDITIONS["full_audio"])
                removed = condition_turns(task, CONDITIONS["clue_removed"])
                self.assertEqual(len(full), len(removed))
                differences = [
                    (left, right)
                    for left, right in zip(full, removed)
                    if left != right
                ]
                self.assertEqual(len(differences), 1)

    def test_gold_path_is_human_decidable_from_declared_options(self):
        for name in TEMPLATES:
            task = build(name, "5-8", 0)
            with self.subTest(domain=task["domain"]):
                self.assertEqual(
                    sum(not item["failure_tags"] for item in task["pre_gap_actions"]),
                    1,
                )
                self.assertEqual(
                    next(
                        item["action"]
                        for item in task["pre_gap_actions"]
                        if not item["failure_tags"]
                    ),
                    task["pre_gap"]["correct_action"],
                )
                action = task["pre_gap"]["correct_action"]
                state = transition(
                    task["domain"],
                    execute_action(task["domain"], task["initial_state"], action),
                    action,
                    task["transition"]["elapsed_minutes"],
                    task["transition"]["external_event"],
                    None,
                )
                gold = correct_action(task["domain"], state)
                self.assertEqual(
                    next(
                        item["action"]
                        for item in task["post_gap_actions"]
                        if not item["failure_tags"]
                    ),
                    gold,
                )

    def test_prosody_has_three_transcripts_two_voices_and_matched_pairs(self):
        user = ScriptedUserSimulator()
        for name in TEMPLATES:
            tasks = [
                build(name, bucket, variant)
                for bucket in ("1-2", "5-8", "12-20")
                for variant in (0, 1)
            ]
            voices = {task["audio_profile"]["user_voice"] for task in tasks}
            transcript_variants = {
                task["prosody_stimulus"]["transcript_variant"] for task in tasks
            }
            self.assertEqual(len(voices), 2)
            self.assertEqual(len(transcript_variants), 3)
            for task in tasks:
                action = task["pre_gap"]["correct_action"]
                state = transition(
                    task["domain"],
                    execute_action(task["domain"], task["initial_state"], action),
                    action,
                    task["transition"]["elapsed_minutes"],
                    task["transition"]["external_event"],
                    None,
                )
                high_text = user.post_gap(task, state, CONDITIONS["prosody_high"])
                low_text = user.post_gap(task, state, CONDITIONS["prosody_low"])
                self.assertEqual(high_text, low_text)

    def test_prosody_gold_is_category_specific_with_four_style_options(self):
        for name in TEMPLATES:
            task = build(name, "5-8", 0)
            high_prosody, high_style = prosody_for(
                task, CONDITIONS["prosody_high"]
            )
            _, low_style = prosody_for(task, CONDITIONS["prosody_low"])
            with self.subTest(domain=task["domain"]):
                self.assertEqual(high_style, HIGH_STYLE_BY_PROSODY[high_prosody])
                self.assertEqual(low_style, "proceed_directly")
                self.assertEqual(len(task["response_styles"]), 4)


if __name__ == "__main__":
    unittest.main()
