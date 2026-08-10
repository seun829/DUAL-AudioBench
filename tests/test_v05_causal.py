"""Construct-validity contracts for the schema-v0.5 main benchmark."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from dual_audio.core.conditions import CONDITIONS, condition_turns
from dual_audio.core.environment import correct_action, execute_action, transition
from dual_audio.interaction.runner import _menu, _style_menu
from dual_audio.users.scripted import ScriptedUserSimulator
from report_results import causal_clue_summary
from scenarios.generate_v05 import BRANCHES, build
from scenarios.templates import TEMPLATES


BUCKETS = ("1-2", "5-8", "12-20")


def terminal_state(task: dict) -> dict:
    """Execute the declared gold pre-gap path and external transition."""

    action = task["pre_gap"]["correct_action"]
    return transition(
        task["domain"],
        execute_action(task["domain"], task["initial_state"], action),
        action,
        task["transition"]["elapsed_minutes"],
        task["transition"]["external_event"],
        None,
    )


class V05CausalQualityTests(unittest.TestCase):
    def test_generated_pool_is_balanced_and_separate(self):
        files = sorted(Path("data/scenarios_v05").glob("*.json"))
        self.assertEqual(len(files), 84)
        tasks = [json.loads(path.read_text(encoding="utf-8")) for path in files]
        self.assertEqual({task["schema_version"] for task in tasks}, {"0.5"})
        self.assertTrue(all(task["scenario_id"].endswith("_s05") for task in tasks))
        self.assertEqual(
            {task["causal_design"]["branch"] for task in tasks}, set(BRANCHES)
        )
        for domain in {task["domain"] for task in tasks}:
            for bucket in BUCKETS:
                members = [
                    task
                    for task in tasks
                    if task["domain"] == domain and task["bucket"] == bucket
                ]
                self.assertEqual(len(members), 2)
                self.assertEqual(
                    {task["causal_design"]["branch"] for task in members},
                    set(BRANCHES),
                )

    def test_counterfactual_clue_changes_gold_state_and_action(self):
        user = ScriptedUserSimulator()
        for name in TEMPLATES:
            for bucket in BUCKETS:
                tasks = [build(name, bucket, index) for index in range(2)]
                states = [terminal_state(task) for task in tasks]
                variable = tasks[0]["causal_design"]["outcome_variable"]
                actions = [
                    correct_action(task["domain"], state)
                    for task, state in zip(tasks, states)
                ]
                with self.subTest(template=name, bucket=bucket):
                    self.assertNotEqual(states[0][variable], states[1][variable])
                    self.assertNotEqual(actions[0], actions[1])
                    for task, state, action in zip(tasks, states, actions):
                        self.assertEqual(
                            action, task["causal_design"]["expected_post_action"]
                        )
                        self.assertEqual(
                            state["causal_alignment"],
                            task["causal_design"]["branch"],
                        )
                        self.assertIn(
                            state[variable], task["belief_schema"][variable]
                        )
                    self.assertEqual(
                        user.post_gap(tasks[0], states[0], CONDITIONS["full_audio"]),
                        user.post_gap(tasks[1], states[1], CONDITIONS["full_audio"]),
                    )

    def test_removed_clue_makes_pair_publicly_indistinguishable(self):
        """No scenario ID, voice, text, or menu-order shortcut may reveal branch."""

        user = ScriptedUserSimulator()
        for name in TEMPLATES:
            for bucket in BUCKETS:
                left, right = [build(name, bucket, index) for index in range(2)]
                left_state, right_state = terminal_state(left), terminal_state(right)
                with self.subTest(template=name, bucket=bucket):
                    self.assertEqual(
                        condition_turns(left, CONDITIONS["clue_removed"]),
                        condition_turns(right, CONDITIONS["clue_removed"]),
                    )
                    self.assertEqual(left["audio_profile"], right["audio_profile"])
                    self.assertEqual(
                        user.post_gap(
                            left, left_state, CONDITIONS["clue_removed"]
                        ),
                        user.post_gap(
                            right, right_state, CONDITIONS["clue_removed"]
                        ),
                    )
                    for seed in (0, 1):
                        self.assertEqual(
                            _menu(left, "pre_gap", seed)[0],
                            _menu(right, "pre_gap", seed)[0],
                        )
                        self.assertEqual(
                            _menu(left, "post_gap", seed)[0],
                            _menu(right, "post_gap", seed)[0],
                        )
                        self.assertEqual(
                            _style_menu(left, seed)[0], _style_menu(right, seed)[0]
                        )

    def test_full_pair_differs_only_at_the_causal_clue_in_public_history(self):
        for name in TEMPLATES:
            for bucket in BUCKETS:
                left, right = [build(name, bucket, index) for index in range(2)]
                differences = [
                    (first, second)
                    for first, second in zip(left["turns"], right["turns"])
                    if first != second
                ]
                with self.subTest(template=name, bucket=bucket):
                    self.assertEqual(len(differences), 1)
                    self.assertEqual(differences[0][0]["kind"], "clue")
                    self.assertEqual(differences[0][1]["kind"], "clue")

    def test_belief_schema_directly_scores_the_causal_clue(self):
        for name in TEMPLATES:
            task = build(name, "5-8", 0)
            with self.subTest(template=name):
                self.assertEqual(
                    task["belief_schema"]["causal_alignment"], list(BRANCHES)
                )
                definitions = task["belief_definitions"]["causal_alignment"]
                self.assertEqual(set(definitions), set(BRANCHES))
                self.assertTrue(all(definitions.values()))

    def test_standard_event_hides_terminal_result_but_controls_remain_truthful(self):
        user = ScriptedUserSimulator()
        for name in TEMPLATES:
            task = build(name, "5-8", 0)
            state = terminal_state(task)
            causal = task["causal_post_gap_observation"]
            with self.subTest(template=name):
                self.assertEqual(
                    user.post_gap(task, state, CONDITIONS["full_audio"]),
                    causal["text"],
                )
                no_event_action = task["pre_gap"]["correct_action"]
                no_event_state = transition(
                    task["domain"],
                    execute_action(
                        task["domain"], task["initial_state"], no_event_action
                    ),
                    no_event_action,
                    task["transition"]["elapsed_minutes"],
                    None,
                    None,
                )
                self.assertNotEqual(
                    user.post_gap(
                        task,
                        no_event_state,
                        CONDITIONS["gap_no_state_change"],
                    ),
                    causal["text"],
                )

    def test_prosody_pairs_preserve_words_and_technical_gold(self):
        user = ScriptedUserSimulator()
        for name in TEMPLATES:
            for bucket in BUCKETS:
                for branch in range(2):
                    task = build(name, bucket, branch)
                    state = terminal_state(task)
                    with self.subTest(template=name, bucket=bucket, branch=branch):
                        self.assertEqual(
                            user.post_gap(
                                task, state, CONDITIONS["prosody_high"]
                            ),
                            user.post_gap(
                                task, state, CONDITIONS["prosody_low"]
                            ),
                        )
                        self.assertEqual(
                            correct_action(task["domain"], state),
                            task["causal_design"]["expected_post_action"],
                        )

    def test_causal_report_scores_complete_pairs_and_no_clue_ceiling(self):
        rows = []
        for condition in ("full_audio", "clue_removed"):
            for branch, gold in (
                ("misaligned", "repair"),
                ("aligned", "close"),
            ):
                selected = gold if condition == "full_audio" else "repair"
                rows.append(
                    {
                        "causal_pair_id": "example:1-2:s05",
                        "causal_branch": branch,
                        "condition": condition,
                        "seed": 0,
                        "post_gap_action": selected,
                        "post_gap_success": selected == gold,
                        "trajectory_success": selected == gold,
                    }
                )
        summary = causal_clue_summary(rows)
        self.assertIsNotNone(summary)
        self.assertEqual(
            summary["clue_removed_deterministic_post_accuracy_ceiling"], 0.5
        )
        self.assertEqual(
            summary["conditions"]["full_audio"][
                "complete_counterfactual_pairs"
            ],
            1,
        )
        self.assertEqual(
            summary["conditions"]["full_audio"][
                "both_branches_post_gap_correct"
            ],
            1.0,
        )
        self.assertEqual(
            summary["conditions"]["clue_removed"]["post_gap_accuracy"],
            0.5,
        )
        self.assertEqual(
            summary["conditions"]["clue_removed"][
                "selected_action_changes_across_branches"
            ],
            0.0,
        )


if __name__ == "__main__":
    unittest.main()
