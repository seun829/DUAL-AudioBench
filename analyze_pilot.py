"""Extract and save the pilot's comparison artifacts as files.

``score.py`` prints a human report. This command reuses its metric functions and
persists the specific comparisons a pilot write-up needs:

* the belief/action outcome matrix, overall and per condition;
* paired effects for every registered control with a full-audio counterpart;
* per-condition headline rates with chance floors.

Deltas are paired by ``(scenario_id, seed)`` so each comparison uses matched
trajectories rather than differing condition subsets.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from score import (
    load,
    paired_checkpoint_effect,
    paired_cluster_effect,
    summarize,
    summarize_beliefs,
    summarize_prosody,
)


OUTCOMES = (
    "FULL_SUCCESS",
    "ACTION_SELECTION_FAILURE",
    "LUCKY_ACTION",
    "STATE_SYNCHRONIZATION_FAILURE",
)

# Fields compared between two conditions on matched trajectories.
PAIRED_FIELDS = (
    "trajectory_success",
    "pre_gap_success",
    "post_gap_success",
    "state_belief_success",
)


def _rate(rows: list[dict], field: str) -> float | None:
    """Return the mean of a boolean field, or None when it is never present."""

    values = [bool(row.get(field)) for row in rows if row.get(field) is not None]
    return sum(values) / len(values) if values else None


def paired_delta(rows: list[dict], left: str, right: str) -> dict:
    """Compare two conditions on trajectories matched by scenario and seed."""

    def index(condition: str) -> dict:
        return {
            (row["scenario_id"], row["seed"]): row
            for row in rows
            if row["condition"] == condition and not row.get("error")
        }

    left_rows, right_rows = index(left), index(right)
    keys = sorted(left_rows.keys() & right_rows.keys())
    result = {"left": left, "right": right, "paired_n": len(keys), "fields": {}}
    for field in PAIRED_FIELDS:
        pairs = [
            (bool(left_rows[k].get(field)), bool(right_rows[k].get(field)))
            for k in keys
            if left_rows[k].get(field) is not None
            and right_rows[k].get(field) is not None
        ]
        if not pairs:
            continue
        left_rate = sum(a for a, _ in pairs) / len(pairs)
        right_rate = sum(b for _, b in pairs) / len(pairs)
        result["fields"][field] = {
            "n": len(pairs),
            f"{left}_rate": round(left_rate, 4),
            f"{right}_rate": round(right_rate, 4),
            "delta": round(left_rate - right_rate, 4),
            # discordant pairs: where exactly one condition succeeded
            "left_only": sum(1 for a, b in pairs if a and not b),
            "right_only": sum(1 for a, b in pairs if b and not a),
        }
        inference = paired_cluster_effect(rows, left, right, field)
        result["fields"][field].update(
            {
                "domain_clusters": inference["clusters"],
                "domain_clustered_ci": [
                    round(inference["ci"][0], 4),
                    round(inference["ci"][1], 4),
                ],
                "exact_sign_flip_p": round(inference["p_value"], 6),
            }
        )
    checkpoint = paired_checkpoint_effect(
        rows, left, right, "post_observation"
    )
    result["post_observation_belief_effect"] = {
        "delta": round(checkpoint["delta"], 4),
        "domain_clusters": checkpoint["clusters"],
        "domain_clustered_ci": [
            round(checkpoint["ci"][0], 4),
            round(checkpoint["ci"][1], 4),
        ],
        "exact_sign_flip_p": round(checkpoint["p_value"], 6),
    }
    # belief-dynamics comparison, the quantity the modality control targets
    result["belief"] = {
        cond: {
            key: round(value, 4)
            for key, value in summarize_beliefs(
                [r for r in (left_rows if cond == left else right_rows).values()]
            ).items()
            if isinstance(value, (int, float))
        }
        for cond in (left, right)
    }
    return result


def main() -> None:
    """Write the pilot comparison artifacts beside the trajectory log."""

    parser = argparse.ArgumentParser()
    parser.add_argument("results")
    parser.add_argument("--prefix", default=None)
    args = parser.parse_args()

    path = Path(args.results)
    rows = load(path)
    ok = [row for row in rows if not row.get("error")]
    prefix = Path(args.prefix or str(path.with_suffix("")))
    conditions = sorted({row["condition"] for row in ok})

    # ---- belief/action outcome matrix -------------------------------------
    matrix_path = prefix.with_name(prefix.name + "_belief_action_matrix.csv")
    with matrix_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["condition", "decisions", *OUTCOMES, *(f"{o}_pct" for o in OUTCOMES)])
        for condition in ["ALL", *conditions]:
            group = ok if condition == "ALL" else [r for r in ok if r["condition"] == condition]
            counts = summarize_beliefs(group)["outcome_matrix"]
            total = sum(counts.values()) or 1
            writer.writerow(
                [condition, total]
                + [counts.get(o, 0) for o in OUTCOMES]
                + [round(counts.get(o, 0) / total, 4) for o in OUTCOMES]
            )
    print(f"belief/action matrix     -> {matrix_path}")

    # ---- per-condition headline rates ------------------------------------
    summary_path = prefix.with_name(prefix.name + "_condition_summary.csv")
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["condition", "n", "pass1", "pre_gap", "post_gap", "state_belief",
             "action_chance", "two_action_chance", "trajectory_chance",
             "belief_revision_gain", "stale_belief_persistence", "mean_brier", "ece"]
        )
        for condition in conditions:
            group = [r for r in ok if r["condition"] == condition]
            stats, beliefs = summarize(group), summarize_beliefs(group)
            writer.writerow([
                condition, len(group),
                round(stats["pass1"], 4), round(stats["pre"], 4), round(stats["post"], 4),
                round(_rate(group, "state_belief_success") or 0.0, 4),
                round(stats["action_chance"], 4), round(stats["two_action_chance"], 4),
                round(stats["trajectory_chance"], 6),
                round(beliefs["revision_gain"], 4),
                round(beliefs["stale_belief_persistence"], 4),
                round(beliefs["mean_brier"], 4), round(beliefs["ece"], 4),
            ])
    print(f"condition summary        -> {summary_path}")

    # ---- paired comparisons ----------------------------------------------
    comparisons = {}
    if {"full_audio", "clue_removed"} <= set(conditions):
        comparisons["full_vs_clue_removed"] = paired_delta(ok, "full_audio", "clue_removed")
    if {"transcript_only", "full_audio"} <= set(conditions):
        comparisons["transcript_vs_full_audio"] = paired_delta(ok, "transcript_only", "full_audio")
    if {"gap_no_state_change", "full_audio"} <= set(conditions):
        comparisons["no_state_change_vs_full_audio"] = paired_delta(
            ok, "gap_no_state_change", "full_audio"
        )
    if {"state_change_short", "full_audio"} <= set(conditions):
        comparisons["short_distance_vs_full_audio"] = paired_delta(
            ok, "state_change_short", "full_audio"
        )
    if {"hidden_user_action", "full_audio"} <= set(conditions):
        comparisons["explicit_user_update_vs_full_audio"] = paired_delta(
            ok, "hidden_user_action", "full_audio"
        )
    if {"neutral_audio", "full_audio"} <= set(conditions):
        comparisons["neutral_audio_vs_full_audio"] = paired_delta(
            ok, "neutral_audio", "full_audio"
        )
    if {"prosody_high", "prosody_low"} <= set(conditions):
        comparisons["prosody_high_vs_low"] = summarize_prosody(ok)

    deltas_path = prefix.with_name(prefix.name + "_paired_deltas.json")
    deltas_path.write_text(json.dumps(comparisons, indent=2) + "\n", encoding="utf-8")
    print(f"paired deltas            -> {deltas_path}")

    for name, comparison in comparisons.items():
        if "left" not in comparison:
            print(
                f"\n{name}  (paired n={comparison.get('paired_n', 0)}, "
                f"unique stimuli={comparison.get('unique_stimuli', 0)})"
            )
            continue
        print(f"\n{name}  (paired n={comparison['paired_n']})")
        for field, values in comparison["fields"].items():
            left_key = f"{comparison['left']}_rate"
            right_key = f"{comparison['right']}_rate"
            print(
                f"  {field:<22} {comparison['left']}={values[left_key]:.1%}  "
                f"{comparison['right']}={values[right_key]:.1%}  "
                f"delta={values['delta']:+.1%}  "
                f"(only-left={values['left_only']}, only-right={values['right_only']})"
            )


if __name__ == "__main__":
    main()
