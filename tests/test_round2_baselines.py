"""C4. Regression tests for the round-2 corrections.

Three properties that were silently violated before this round:

  1. the paired-scenario invariant (V2): branches differ only at the clue and
     the state it determines, never in the public conversation or the menus;
  2. majority-class chance is computed and is not equal to uniform chance on
     full_audio (C1), so the two-month misreading cannot recur unnoticed;
  3. the oracle condition injects its state sentence at post_gap and nowhere
     else, and suppresses the belief-only checkpoint (C3).
"""

from __future__ import annotations

import copy
import json
import re
import unittest
from collections import defaultdict
from pathlib import Path

from dual_audio.agents import MockAgent
from dual_audio.agents.replay import _instruction
from dual_audio.core.conditions import CONDITIONS
from dual_audio.core.types import AgentResponse, Observation
from dual_audio.interaction import ClosedLoopRunner
from score import (
    fixed_position_action_chance,
    majority_class_action_chance,
    majority_class_belief_chance,
    summarize,
)

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "data" / "scenarios_v05"

# Fields that legitimately differ between the two branches of a causal pair:
# the clue itself, the branch label, the initial-state values the clue fixes,
# prose that describes the branch, and the hidden diagnostic failure tags.
ALLOWED_DIFF = [
    r"^clue$",
    r"^clue_answer$",
    r"^clue_ablation_text$",
    r"^scenario_id$",
    r"^causal_design\.(branch|expected_post_action|paired_scenario_id)$",
    r"^turns\.\d+\.text$",
    r"^initial_state\.[a-z_]+$",
    r"^belief_definitions\.causal_alignment\.(aligned|misaligned)$",
    r"^prosody_stimulus\.stimulus_id$",
    r"^questions\.\d+\.(question|gold_answer)$",
    r"^(pre|post)_gap_actions\.\d+\.failure_tags",
]
ALLOWED_RE = [re.compile(p) for p in ALLOWED_DIFF]


def _flatten(obj, prefix: str = "") -> dict:
    out = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            out.update(_flatten(value, f"{prefix}.{key}" if prefix else str(key)))
    elif isinstance(obj, list):
        out[f"{prefix}_count"] = len(obj)
        for index, value in enumerate(obj):
            out.update(_flatten(value, f"{prefix}.{index}"))
    else:
        out[prefix] = obj
    return out


def _load_tasks() -> dict:
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(SCENARIOS.glob("*.json"))
    }


class PairedScenarioInvariantTests(unittest.TestCase):
    """V2: the causal contrast must be the only difference between branches."""

    def test_branches_differ_only_at_the_clue(self):
        pairs = defaultdict(dict)
        for task in _load_tasks().values():
            design = task["causal_design"]
            pairs[design["pair_id"]][design["branch"]] = task
        self.assertEqual(len(pairs), 42)

        offenders = []
        for pair_id, branches in sorted(pairs.items()):
            self.assertEqual(set(branches), {"misaligned", "aligned"}, pair_id)
            left = _flatten(branches["misaligned"])
            right = _flatten(branches["aligned"])
            for key in sorted(set(left) | set(right)):
                if left.get(key, "<absent>") == right.get(key, "<absent>"):
                    continue
                if any(rx.match(key) for rx in ALLOWED_RE):
                    continue
                offenders.append((pair_id, key))
        self.assertEqual(offenders, [], f"unmatched pair fields: {offenders[:5]}")

    def test_public_menus_are_identical_across_branches(self):
        pairs = defaultdict(dict)
        for task in _load_tasks().values():
            design = task["causal_design"]
            pairs[design["pair_id"]][design["branch"]] = task
        for pair_id, branches in sorted(pairs.items()):
            left, right = branches["misaligned"], branches["aligned"]
            for stage in ("pre_gap_actions", "post_gap_actions"):
                self.assertEqual(
                    [(a["action"], a["description"]) for a in left[stage]],
                    [(a["action"], a["description"]) for a in right[stage]],
                    f"{pair_id} {stage} differs in content or order",
                )

    def test_only_clue_turns_differ_in_text(self):
        pairs = defaultdict(dict)
        for task in _load_tasks().values():
            design = task["causal_design"]
            pairs[design["pair_id"]][design["branch"]] = task
        for pair_id, branches in sorted(pairs.items()):
            left, right = branches["misaligned"], branches["aligned"]
            self.assertEqual(len(left["turns"]), len(right["turns"]), pair_id)
            for index, (a, b) in enumerate(zip(left["turns"], right["turns"])):
                self.assertEqual(a["speaker"], b["speaker"], f"{pair_id}@{index}")
                self.assertEqual(a.get("kind"), b.get("kind"), f"{pair_id}@{index}")
                if a["text"] != b["text"]:
                    self.assertIn(
                        a.get("kind"),
                        {"clue", "clue_prompt"},
                        f"{pair_id} turn {index} ({a.get('kind')}) differs in text",
                    )


class ChanceBaselineTests(unittest.TestCase):
    """C1: majority-class chance must exist and must differ from uniform."""

    def _rows(self, gold_actions, domains=None, menu_size=5):
        domains = domains or ["d0"] * len(gold_actions)
        rows = []
        for index, (gold, domain) in enumerate(zip(gold_actions, domains)):
            rows.append({
                "scenario_id": f"s{index}",
                "domain": domain,
                "seed": 0,
                "condition": "full_audio",
                "trajectory_success": False,
                "pre_gap_success": False,
                "post_gap_success": gold == "close_case",
                "pre_gap_menu_size": menu_size,
                "post_gap_menu_size": menu_size,
                "response_style_menu_size": 1,
                "belief_checkpoint_chance": 0.125,
                "expected_post_gap_action": gold,
                "post_gap_action": gold,
                "post_gap_action_label": "A",
                "post_gap_menu": [
                    {"label": "A", "description": f"do {gold}"},
                    {"label": "B", "description": "do other"},
                ],
                "state_after_gap": {
                    "status": "x" if gold == "close_case" else "y",
                    "causal_alignment": (
                        "aligned" if gold == "close_case" else "misaligned"
                    ),
                },
                "belief_checkpoints": {
                    "pre_gap": {
                        "evaluation": {
                            "variables": {"status": {}, "causal_alignment": {}}
                        }
                    }
                },
            })
        return rows

    def test_majority_class_action_chance_is_reported(self):
        stats = summarize(self._rows(["close_case"] * 5 + ["repair"] * 5))
        self.assertIn("majority_class_action_chance", stats)
        self.assertIn("fixed_position_action_chance", stats)
        self.assertIn("majority_class_belief_chance", stats)

    def test_majority_class_exceeds_uniform_on_skewed_gold(self):
        # 50/50 close_case, one domain: a constant guess scores half, not 1/5.
        stats = summarize(self._rows(["close_case"] * 5 + ["repair"] * 5))
        self.assertAlmostEqual(stats["action_chance"], 0.2)
        self.assertAlmostEqual(stats["majority_class_action_chance"], 0.5)
        self.assertNotAlmostEqual(
            stats["majority_class_action_chance"], stats["action_chance"]
        )

    def test_majority_class_belief_exceeds_uniform_on_two_cell_gold(self):
        stats = summarize(self._rows(["close_case"] * 5 + ["repair"] * 5))
        self.assertAlmostEqual(stats["majority_class_belief_chance"], 0.5)
        self.assertGreater(
            stats["majority_class_belief_chance"],
            stats["belief_checkpoint_chance"]
            if "belief_checkpoint_chance" in stats
            else 0.125,
        )

    def test_majority_class_is_domain_conditional(self):
        # One gold per domain: a domain-aware constant policy scores 1.0.
        rows = self._rows(
            ["a", "a", "b", "b"], domains=["d0", "d0", "d1", "d1"]
        )
        self.assertAlmostEqual(majority_class_action_chance(rows), 1.0)

    def test_fixed_position_chance_reports_coverage(self):
        rows = self._rows(["close_case"] * 4)
        rate, coverage = fixed_position_action_chance(rows)
        self.assertAlmostEqual(coverage, 1.0)
        self.assertAlmostEqual(rate, 1.0)

    def test_belief_chance_handles_missing_checkpoints(self):
        rows = self._rows(["close_case"])
        rows[0]["belief_checkpoints"] = {}
        self.assertNotEqual(majority_class_belief_chance(rows), 0)


class OracleConditionTests(unittest.TestCase):
    """C3: the oracle sentence appears at post_gap and nowhere else."""

    def setUp(self):
        self.task = json.loads(
            (SCENARIOS / "flight_1to2_b0_s05.json").read_text(encoding="utf-8")
        )

    def _run(self, condition_name):
        seen = []

        class Spy:
            def __init__(self):
                self.inner = MockAgent()

            def respond(self, observation, history):
                seen.append(
                    (observation.stage, observation.oracle_state_text,
                     _instruction(observation))
                )
                return self.inner.respond(observation, history)

        trajectory = ClosedLoopRunner().execute(
            agent=Spy(),
            task=self.task,
            condition=CONDITIONS[condition_name],
            seed=0,
        )
        return trajectory, seen

    def test_oracle_text_only_at_post_gap(self):
        _, seen = self._run("oracle_state")
        for stage, oracle, _ in seen:
            if stage == "post_gap":
                self.assertTrue(oracle, "post_gap must carry the oracle sentence")
            else:
                self.assertEqual(oracle, "", f"{stage} must not carry it")

    def test_oracle_names_the_realized_state(self):
        trajectory, seen = self._run("oracle_state")
        prompt = next(p for stage, _, p in seen if stage == "post_gap")
        for variable in self.task["belief_schema"]:
            self.assertIn(
                str(trajectory["state_after_gap"][variable]),
                prompt,
                f"{variable} must be stated in the oracle prompt",
            )

    def test_oracle_suppresses_the_belief_checkpoint(self):
        trajectory, seen = self._run("oracle_state")
        self.assertNotIn("post_gap_belief", [stage for stage, _, _ in seen])
        self.assertFalse(trajectory["belief_elicited"])
        self.assertNotIn(
            "post_gap_belief",
            [call["stage"] for call in trajectory["model_calls"]],
        )

    def test_oracle_prompt_drops_the_belief_request(self):
        _, seen = self._run("oracle_state")
        prompt = next(p for stage, _, p in seen if stage == "post_gap")
        self.assertNotIn("state_belief", prompt)
        self.assertNotIn("needs_revalidation", prompt)
        self.assertIn('{"choice": "A"}', prompt)

    def test_existing_conditions_keep_the_belief_checkpoint(self):
        for condition_name in ("full_audio", "gap_no_state_change",
                               "prosody_high"):
            trajectory, seen = self._run(condition_name)
            self.assertIn(
                "post_gap_belief",
                [stage for stage, _, _ in seen],
                condition_name,
            )
            self.assertTrue(trajectory["belief_elicited"], condition_name)
            self.assertIsNone(trajectory["oracle_state_text"], condition_name)
            prompt = next(p for stage, _, p in seen if stage == "post_gap")
            self.assertIn("state_belief", prompt)

    def test_oracle_scores_the_same_action_as_full_audio(self):
        # The oracle condition must not change the world, only the prompt.
        oracle, _ = self._run("oracle_state")
        full, _ = self._run("full_audio")
        self.assertEqual(
            oracle["expected_post_gap_action"], full["expected_post_gap_action"]
        )
        self.assertEqual(oracle["state_after_gap"], full["state_after_gap"])
        self.assertEqual(oracle["post_gap_menu"], full["post_gap_menu"])


class ObservationDefaultTests(unittest.TestCase):
    """The new Observation field must default to empty for every caller."""

    def test_oracle_state_text_defaults_to_empty(self):
        self.assertEqual(Observation(text="x", stage="post_gap").oracle_state_text, "")

    def test_condition_flags_default_to_previous_behaviour(self):
        for name, condition in CONDITIONS.items():
            if name == "oracle_state":
                continue
            self.assertTrue(condition.elicit_belief, name)
            self.assertFalse(condition.oracle_state, name)


if __name__ == "__main__":
    unittest.main()
