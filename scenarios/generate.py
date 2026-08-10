"""Generate schema-v0.4 closed-loop tasks with audited clue distances."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dual_audio.core.belief_definitions import definitions_for
from scenarios.templates import TAGS, TEMPLATES


BUCKETS = {"1-2": (1, 2), "5-8": (5, 8), "12-20": (12, 20)}
SCHEMA_VERSION = "0.4"
USER_VOICES = ("en-us+f3", "en-us+f4")


def leak_guard(turns: list[dict], clue_idx: int, clue_text: str) -> list[tuple]:
    """Return later turns that probably restate two or more clue keywords."""

    keywords = {
        word
        for word in re.findall(r"[a-z]+", clue_text.lower())
        if len(word) > 5
    }
    leaks = []
    for i, turn in enumerate(turns):
        if i <= clue_idx:
            continue
        hits = sorted(word for word in keywords if word in turn["text"].lower())
        if len(hits) >= 2:
            leaks.append((i, hits))
    return leaks


def choice_leak_guard(task: dict) -> None:
    """Reject tasks where only the untagged post-gap option echoes the clue."""

    clue_words = {
        word
        for word in re.findall(r"[a-z]+", task["clue"].lower())
        if len(word) > 5
    }
    descriptions = task["post_gap_actions"]
    overlap = {
        item["action"]: {
            word for word in clue_words if word in item["description"].lower()
        }
        for item in descriptions
    }
    correct = " ".join(
        item["description"]
        for item in descriptions
        if not item.get("failure_tags")
    )
    correct_hits = {
        word for word in clue_words if word in correct.lower()
    }
    wrong_hits = set().union(
        *(
            hits
            for action, hits in overlap.items()
            if action not in {
                item["action"]
                for item in descriptions
                if not item.get("failure_tags")
            }
        )
    )
    if correct_hits - wrong_hits:
        raise ValueError(
            "Only the untagged option repeats clue words: "
            f"{sorted(correct_hits - wrong_hits)}"
        )


def _mark(turns, kind):
    """Convert compact speaker/text tuples into typed turn dictionaries."""

    return [
        {"speaker": speaker, "text": text, "kind": kind}
        for speaker, text in turns
    ]


def build(template_name: str, bucket: str, variant_seed: int) -> dict:
    """Build and validate one deterministic schema-v0.4 scenario.

    Filler pairs are shuffled, a realizable even clue distance is selected,
    alternation and exact distance are asserted, and lexical leak guards run
    before the scenario is returned.
    """

    template = TEMPLATES[template_name]
    rng = random.Random(f"{template_name}-{bucket}-{variant_seed}")
    fillers = list(template["fillers"])
    pairs = [fillers[i : i + 2] for i in range(0, len(fillers), 2)]
    rng.shuffle(pairs)

    lo, hi = BUCKETS[bucket]
    # Distance is explicitly the number of conversational turns after the clue
    # and before the fast-forward. It includes the evaluated pre-gap action and
    # deterministic acknowledgement, so the minimum possible distance is two.
    possible = [
        value
        for value in range(max(2, lo), min(hi, len(fillers) + 2) + 1)
        if value % 2 == 0
    ]
    if not possible:
        raise ValueError(f"Bucket {bucket} has no realizable alternating-turn distance")
    target_distance = rng.choice(possible)
    after_needed = target_distance - 2
    after_pair_count = after_needed // 2
    after_pairs = pairs[:after_pair_count]
    before_pairs = pairs[after_pair_count:]
    before = [turn for pair in before_pairs for turn in pair]
    after = [turn for pair in after_pairs for turn in pair]

    turns = (
        _mark(template["setup"], "setup")
        + _mark(before, "filler")
        + [
            {
                "speaker": "agent",
                "text": template["clue_prompt"],
                "kind": "clue_prompt",
            },
            {"speaker": "user", "text": template["clue"], "kind": "clue"},
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

    for i, turn in enumerate(turns):
        expected = "user" if i % 2 == 0 else "agent"
        assert turn["speaker"] == expected, (
            f"{template_name}/{bucket}: expected {expected} at turn {i}, "
            f"got {turn['speaker']}"
        )

    clue_idx = next(i for i, turn in enumerate(turns) if turn["kind"] == "clue")
    actual_distance = len(turns) - clue_idx - 1
    assert actual_distance == target_distance, (
        f"{template_name}/{bucket}: recorded distance {target_distance}, "
        f"actual distance {actual_distance}"
    )
    leaks = leak_guard(turns, clue_idx, template["clue"])
    if leaks:
        raise ValueError(f"{template_name}/{bucket}: clue leak at turns {leaks}")

    scenario_id = (
        f"{template_name}_{bucket.replace('-', 'to')}_v{variant_seed}_s04"
    )
    belief_schema = template["belief_schema"]
    transcript_variant = tuple(BUCKETS).index(bucket)
    scenario = {
        "schema_version": SCHEMA_VERSION,
        "scenario_id": scenario_id,
        "domain": template["domain"],
        "bucket": bucket,
        "clue_turn_distance": actual_distance,
        "distance_definition": (
            "Number of agent/user turns after the clue and before fast-forward; "
            "includes the evaluated pre-gap action and user acknowledgement."
        ),
        "clue": template["clue"],
        "clue_answer": template["clue_answer"],
        "clue_ablation_text": template["clue_ablation_text"],
        "turns": turns,
        "initial_state": template["initial_state"],
        "pre_gap": {
            "agent_turn_index": len(turns) - 2,
            "correct_action": template["pre_gap_correct"],
        },
        "transition": template["transition"],
        "belief_schema": belief_schema,
        "belief_definitions": definitions_for(belief_schema),
        "revalidation_actions": template["revalidation_actions"],
        "belief_confidence_threshold": template["belief_confidence_threshold"],
        "pre_gap_actions": template["pre_gap_actions"],
        "post_gap_actions": template["post_gap_actions"],
        "prosody_pair": template["prosody_pair"],
        "prosody_stimulus": {
            "stimulus_id": f"{template_name}:{bucket}:voice{variant_seed % 2}",
            "transcript_variant": transcript_variant,
            "voice_variant": variant_seed % len(USER_VOICES),
        },
        "audio_profile": {
            "user_voice": USER_VOICES[variant_seed % len(USER_VOICES)],
            "agent_voice": "en-us+m3",
        },
        "response_styles": template["response_styles"],
        "questions": [
            {
                "q_id": f"q{i + 1}",
                "question": question,
                "gold_answer": answer,
                "targets": target,
                "turn_distance": actual_distance if target == "clue" else None,
                "bucket": (
                    bucket
                    if target == "clue"
                    else "post_ff"
                    if target == "post_ff"
                    else "filler"
                ),
            }
            for i, (question, answer, target) in enumerate(template["questions"])
        ],
        "tag_definitions": TAGS,
    }
    choice_leak_guard(scenario)
    return scenario


def main() -> None:
    """Generate every domain x distance bucket x requested variant."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--variants", type=int, default=2)
    parser.add_argument("--out", default="data/scenarios_v04")
    args = parser.parse_args()

    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    count = 0
    for template_name in TEMPLATES:
        for bucket in BUCKETS:
            for variant in range(args.variants):
                scenario = build(template_name, bucket, variant)
                path = output / f"{scenario['scenario_id']}.json"
                path.write_text(
                    json.dumps(scenario, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                count += 1
    print(f"Wrote {count} executable closed-loop tasks to {output}.")


if __name__ == "__main__":
    main()
