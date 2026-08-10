"""Generate schema-v0.5 causally clue-dependent closed-loop tasks."""

from __future__ import annotations

import argparse
import copy
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dual_audio.core.belief_definitions import definitions_for
from scenarios.generate import BUCKETS, _mark, choice_leak_guard, leak_guard
from scenarios.templates import TAGS, TEMPLATES
from scenarios.v05_design import CAUSAL_DESIGNS, validate_design_registry


SCHEMA_VERSION = "0.5"
USER_VOICES = ("en-us+f3", "en-us+f4")
BRANCHES = ("misaligned", "aligned")


def _post_actions_for_branch(template: dict, expected: str) -> list[dict]:
    """Make exactly the state-derived branch action untagged."""

    actions = copy.deepcopy(template["post_gap_actions"])
    for item in actions:
        if item["action"] == expected:
            item["failure_tags"] = []
        elif not item.get("failure_tags"):
            item["failure_tags"] = ["EARLY_CLUE_LOSS"]
    if sum(not item["failure_tags"] for item in actions) != 1:
        raise ValueError(
            f"{template['domain']}: branch {expected} does not have one gold action"
        )
    return actions


def _question_rows(
    template: dict,
    design: dict,
    branch: dict,
    bucket: str,
    distance: int,
) -> list[dict]:
    """Version the clue and inferred-outcome QA targets with the branch."""

    rows = []
    for index, (question, answer, target) in enumerate(template["questions"]):
        if target == "clue":
            question = design["clue_prompt"]
            answer = branch["clue_answer"]
        elif target == "post_ff":
            answer = branch["post_answer"]
        rows.append(
            {
                "q_id": f"q{index + 1}",
                "question": question,
                "gold_answer": answer,
                "targets": target,
                "turn_distance": distance if target == "clue" else None,
                "bucket": (
                    bucket
                    if target == "clue"
                    else "post_ff"
                    if target == "post_ff"
                    else "filler"
                ),
            }
        )
    return rows


def build(template_name: str, bucket: str, branch_index: int) -> dict:
    """Build one branch of a matched causal counterfactual pair.

    Pair members use the same filler ordering, voices, public menus, causal
    rule, and resumed observation.  Only the early clue and its corresponding
    hidden alignment state differ.
    """

    validate_design_registry(set(TEMPLATES))
    if branch_index not in (0, 1):
        raise ValueError("v0.5 branch_index must be 0 (misaligned) or 1 (aligned)")
    template = TEMPLATES[template_name]
    design = CAUSAL_DESIGNS[template_name]
    branch = design["branches"][branch_index]
    if branch["id"] != BRANCHES[branch_index]:
        raise ValueError(f"{template_name}: branch order is not canonical")

    # Excluding branch_index is intentional: paired branches must have the
    # same filler transcript rather than variant-specific filler shuffles.
    rng = random.Random(f"{template_name}-{bucket}-v05-layout")
    fillers = list(template["fillers"])
    pairs = [fillers[index : index + 2] for index in range(0, len(fillers), 2)]
    rng.shuffle(pairs)

    lo, hi = BUCKETS[bucket]
    possible = [
        value
        for value in range(max(2, lo), min(hi, len(fillers) + 2) + 1)
        if value % 2 == 0
    ]
    if not possible:
        raise ValueError(f"Bucket {bucket} has no realizable alternating distance")
    target_distance = rng.choice(possible)
    after_pair_count = (target_distance - 2) // 2
    after_pairs = pairs[:after_pair_count]
    before_pairs = pairs[after_pair_count:]
    before = [turn for pair in before_pairs for turn in pair]
    after = [turn for pair in after_pairs for turn in pair]

    turns = (
        _mark(template["setup"], "setup")
        + _mark(design["rule_turns"], "causal_rule")
        + _mark(before, "filler")
        + [
            {
                "speaker": "agent",
                "text": design["clue_prompt"],
                "kind": "clue_prompt",
            },
            {"speaker": "user", "text": branch["clue"], "kind": "clue"},
        ]
        + _mark(after, "filler")
        + [
            {
                "speaker": "agent",
                "text": template["pre_ff"][0][1],
                "kind": "pre_gap_action",
            },
            {
                "speaker": "user",
                "text": template["pre_ff"][1][1],
                "kind": "pre_gap_acknowledgement",
            },
        ]
    )

    for index, turn in enumerate(turns):
        expected_speaker = "user" if index % 2 == 0 else "agent"
        if turn["speaker"] != expected_speaker:
            raise ValueError(
                f"{template_name}/{bucket}/{branch['id']}: expected "
                f"{expected_speaker} at turn {index}, got {turn['speaker']}"
            )

    clue_index = next(index for index, turn in enumerate(turns) if turn["kind"] == "clue")
    actual_distance = len(turns) - clue_index - 1
    if actual_distance != target_distance:
        raise ValueError(
            f"{template_name}/{bucket}: recorded distance {target_distance}, "
            f"actual {actual_distance}"
        )
    leaks = leak_guard(turns, clue_index, branch["clue"])
    if leaks:
        raise ValueError(f"{template_name}/{bucket}/{branch['id']}: clue leak {leaks}")

    pair_id = f"{template_name}:{bucket}:s05"
    scenario_id = (
        f"{template_name}_{bucket.replace('-', 'to')}_b{branch_index}_s05"
    )
    paired_index = 1 - branch_index
    paired_id = (
        f"{template_name}_{bucket.replace('-', 'to')}_b{paired_index}_s05"
    )

    initial_state = copy.deepcopy(template["initial_state"])
    initial_state.update(copy.deepcopy(branch["state_patch"]))
    initial_state["causal_alignment"] = branch["id"]
    initial_state["benchmark_schema"] = SCHEMA_VERSION

    belief_schema = copy.deepcopy(template["belief_schema"])
    belief_schema["causal_alignment"] = list(BRANCHES)
    belief_definitions = definitions_for(belief_schema)
    belief_definitions["causal_alignment"] = copy.deepcopy(
        design["causal_definitions"]
    )

    voice_variant = tuple(BUCKETS).index(bucket) % len(USER_VOICES)
    post_actions = _post_actions_for_branch(
        template, branch["expected_post_action"]
    )
    scenario = {
        "schema_version": SCHEMA_VERSION,
        "scenario_id": scenario_id,
        "domain": template["domain"],
        "bucket": bucket,
        "clue_turn_distance": actual_distance,
        "distance_definition": (
            "Number of agent/user turns after the causal clue and before fast-forward; "
            "includes the evaluated pre-gap action and user acknowledgement."
        ),
        "clue": branch["clue"],
        "clue_answer": branch["clue_answer"],
        "clue_ablation_text": template["clue_ablation_text"],
        "turns": turns,
        "initial_state": initial_state,
        "pre_gap": {
            "agent_turn_index": len(turns) - 2,
            "correct_action": template["pre_gap_correct"],
        },
        "transition": copy.deepcopy(template["transition"]),
        "belief_schema": belief_schema,
        "belief_definitions": belief_definitions,
        "revalidation_actions": copy.deepcopy(template["revalidation_actions"]),
        "belief_confidence_threshold": template["belief_confidence_threshold"],
        "pre_gap_actions": copy.deepcopy(template["pre_gap_actions"]),
        "post_gap_actions": post_actions,
        "causal_design": {
            "pair_id": pair_id,
            "paired_scenario_id": paired_id,
            "branch": branch["id"],
            "outcome_variable": design["outcome_variable"],
            "hidden_outcomes": copy.deepcopy(design["hidden_outcomes"]),
            "expected_post_action": branch["expected_post_action"],
            "intervention": "early_clue_only",
        },
        "causal_post_gap_observation": {
            "state_variable": design["outcome_variable"],
            "hidden_values": copy.deepcopy(design["hidden_outcomes"]),
            "text": design["ambiguous_observation"],
        },
        # Menu randomization uses the pair ID so counterfactual branches cannot
        # be distinguished by option order after clue removal.
        "menu_pairing_id": pair_id,
        "prosody_pair": copy.deepcopy(template["prosody_pair"]),
        "prosody_stimulus": {
            "stimulus_id": f"{pair_id}:{branch['id']}",
            "transcript_variant": tuple(BUCKETS).index(bucket),
            "voice_variant": voice_variant,
        },
        "audio_profile": {
            "user_voice": USER_VOICES[voice_variant],
            "agent_voice": "en-us+m3",
        },
        "response_styles": copy.deepcopy(template["response_styles"]),
        "questions": _question_rows(
            template, design, branch, bucket, actual_distance
        ),
        "tag_definitions": copy.deepcopy(TAGS),
    }
    choice_leak_guard(scenario)
    return scenario


def main() -> None:
    """Generate all 14 domains x 3 distances x 2 causal branches."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/scenarios_v05")
    args = parser.parse_args()

    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    count = 0
    for template_name in TEMPLATES:
        for bucket in BUCKETS:
            for branch_index in range(2):
                scenario = build(template_name, bucket, branch_index)
                path = output / f"{scenario['scenario_id']}.json"
                path.write_text(
                    json.dumps(scenario, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                count += 1
    print(f"Wrote {count} causal schema-v0.5 tasks to {output}.")


if __name__ == "__main__":
    main()
