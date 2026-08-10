"""Create readable, comparative reports from one or more trajectory JSONL files.

Outputs:
  - report.md: human-readable overview, metrics, controls, and difficulty flags
  - metrics.json: indented machine-readable aggregate metrics
  - metrics.csv: one flat row per model and condition
  - trajectories.csv: compact per-trajectory audit table
  - <model>_retention.png: full-audio retention curve
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from dual_audio.core.conditions import CONTROL_CONDITIONS
from score import (
    modality_belief_curve,
    paired_checkpoint_effect,
    paired_cluster_effect,
    prosody_summary_plot,
    retention_curve,
    summarize,
    summarize_beliefs,
    summarize_prosody,
)


def _mean(values: Iterable[float | bool]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else math.nan


def _percent(value: float | None) -> str:
    return "N/A" if value is None or math.isnan(value) else f"{value:.1%}"


def _number(value: float | None, digits: int = 3) -> str:
    return "N/A" if value is None or math.isnan(value) else f"{value:.{digits}f}"


def _safe_json(value: Any) -> Any:
    """Convert Counters, tuples, and NaN values to portable JSON values."""

    if isinstance(value, dict):
        return {str(key): _safe_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_safe_json(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def load_files(paths: list[Path]) -> tuple[list[dict], dict[str, list[dict]]]:
    """Load all rows, retaining source-file membership for readable exports."""

    rows = []
    by_source = {}
    for path in paths:
        source_rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        by_source[str(path)] = source_rows
        for row in source_rows:
            copied = dict(row)
            copied["_source"] = str(path)
            rows.append(copied)
    return rows, by_source


def completed_trajectories(rows: list[dict]) -> list[dict]:
    """Deduplicate successful rows by model/scenario/condition/seed."""

    indexed = {}
    for row in rows:
        if row.get("error"):
            continue
        key = (
            row.get("model"),
            row.get("scenario_id"),
            row.get("condition"),
            row.get("seed"),
        )
        indexed[key] = row
    return list(indexed.values())


def usage_summary(rows: list[dict]) -> dict[str, Any]:
    """Aggregate trajectory-level API telemetry."""

    usage = [row.get("api_usage", {}) for row in rows]
    return {
        "trajectories": len(rows),
        "model_calls": sum(int(item.get("model_calls", 0) or 0) for item in usage),
        "metered_calls": sum(
            int(item.get("metered_calls", 0) or 0) for item in usage
        ),
        "prompt_tokens": sum(
            int(item.get("prompt_tokens", 0) or 0) for item in usage
        ),
        "completion_tokens": sum(
            int(item.get("completion_tokens", 0) or 0) for item in usage
        ),
        "total_tokens": sum(
            int(item.get("total_tokens", 0) or 0) for item in usage
        ),
        "cost": round(sum(float(item.get("cost", 0) or 0) for item in usage), 6),
        "request_latency_s": round(
            sum(float(item.get("request_latency_s", 0) or 0) for item in usage),
            3,
        ),
        "trajectory_latency_s": round(
            sum(float(row.get("latency_s", 0) or 0) for row in rows),
            3,
        ),
        "errors": sum(bool(row.get("error")) for row in rows),
    }


def paired_controls(rows: list[dict]) -> dict[str, Any]:
    """Compute the benchmark's matched control effects for one model."""
    return {
        "clue_ablation_post_gap": paired_cluster_effect(
            rows, "full_audio", "clue_removed", "post_gap_success"
        ),
        "clue_ablation_trajectory": paired_cluster_effect(
            rows, "full_audio", "clue_removed", "trajectory_success"
        ),
        "hidden_user_action_post_gap": paired_cluster_effect(
            rows, "hidden_user_action", "full_audio", "post_gap_success"
        ),
        "modality_pre_gap_action": paired_cluster_effect(
            rows, "transcript_only", "full_audio", "pre_gap_success"
        ),
        "modality_post_gap_action": paired_cluster_effect(
            rows, "transcript_only", "full_audio", "post_gap_success"
        ),
        "modality_post_observation_belief": paired_checkpoint_effect(
            rows, "transcript_only", "full_audio", "post_observation"
        ),
        "modality_trajectory": paired_cluster_effect(
            rows, "transcript_only", "full_audio", "trajectory_success"
        ),
        "state_change_post_gap": paired_cluster_effect(
            rows, "full_audio", "gap_no_state_change", "post_gap_success"
        ),
        "neutral_audio_post_gap": paired_cluster_effect(
            rows, "neutral_audio", "full_audio", "post_gap_success"
        ),
        "neutral_audio_post_observation_belief": paired_checkpoint_effect(
            rows, "neutral_audio", "full_audio", "post_observation"
        ),
        "prosody": summarize_prosody(rows),
    }


def difficulty_flags(
    rows: list[dict],
    controls: dict[str, Any],
) -> list[str]:
    """Flag likely ceiling effects or weak causal controls."""

    full = [row for row in rows if row["condition"] == "full_audio"]
    flags = []
    if full:
        action_rate = _mean(row["action_trajectory_success"] for row in full)
        trajectory_rate = _mean(row["trajectory_success"] for row in full)
        if action_rate >= 0.8:
            if len(full) < 6:
                flags.append(
                    f"Preliminary only: the full-audio subset scored "
                    f"{_percent(action_rate)} on both actions, but n={len(full)} "
                    "is too small to establish a ceiling."
                )
            else:
                flags.append(
                    f"The full-audio subset scored {_percent(action_rate)} on "
                    f"both actions across n={len(full)}; the action task may be "
                    "near a ceiling."
                )
        if trajectory_rate >= 0.7:
            flags.append(
                f"Full trajectory success is {_percent(trajectory_rate)}; "
                "increase state branching, distractors, or horizon length."
            )
        invalid = _mean(
            not row.get("belief_reporting_success", False) for row in full
        )
        if action_rate >= 0.8 and trajectory_rate < 0.5 and invalid >= 0.5:
            flags.append(
                "Actions are easy while structured belief reporting dominates "
                "failures; difficulty is formatting-heavy rather than behavioral."
            )
    clue = controls["clue_ablation_post_gap"]
    if clue["paired_n"] and clue["ci"][0] <= 0 <= clue["ci"][1]:
        flags.append(
            "The domain-clustered clue-ablation interval crosses zero; construct "
            "validity is not established for this model."
        )
    if not flags:
        flags.append(
            "No obvious ceiling or ineffective-clue warning fired."
        )
    return flags


def slice_metrics(rows: list[dict], field: str) -> dict[str, dict[str, Any]]:
    """Summarize full-audio performance across one scenario field."""

    groups = defaultdict(list)
    for row in rows:
        if row["condition"] == "full_audio":
            groups[str(row[field])].append(row)
    return {
        name: {
            "n": len(group),
            "trajectory_success": _mean(
                row["trajectory_success"] for row in group
            ),
            "action_trajectory_success": _mean(
                row["action_trajectory_success"] for row in group
            ),
            "pre_gap_success": _mean(row["pre_gap_success"] for row in group),
            "post_gap_success": _mean(row["post_gap_success"] for row in group),
        }
        for name, group in sorted(groups.items())
    }


def causal_clue_summary(rows: list[dict]) -> dict[str, Any] | None:
    """Summarize v0.5 counterfactual branch discrimination.

    Each pair/seed contains an aligned and a misaligned hidden world.  Their
    gold post-gap actions differ, while clue-removed public inputs are matched.
    """

    causal_rows = [row for row in rows if row.get("causal_pair_id")]
    if not causal_rows:
        return None
    output: dict[str, Any] = {
        "clue_removed_deterministic_post_accuracy_ceiling": 0.5,
        "conditions": {},
    }
    for condition in ("full_audio", "transcript_only", "clue_removed"):
        selected = [row for row in causal_rows if row["condition"] == condition]
        if not selected:
            continue
        by_branch = defaultdict(list)
        paired = defaultdict(dict)
        for row in selected:
            branch = row.get("causal_branch")
            by_branch[branch].append(row)
            paired[(row["causal_pair_id"], row["seed"])][branch] = row
        complete = [
            branches
            for branches in paired.values()
            if set(branches) == {"aligned", "misaligned"}
        ]
        output["conditions"][condition] = {
            "trajectories": len(selected),
            "complete_counterfactual_pairs": len(complete),
            "post_gap_accuracy": _mean(
                row["post_gap_success"] for row in selected
            ),
            "strict_trajectory_accuracy": _mean(
                row["trajectory_success"] for row in selected
            ),
            "both_branches_post_gap_correct": _mean(
                all(row["post_gap_success"] for row in branches.values())
                for branches in complete
            ),
            "both_branches_strict_correct": _mean(
                all(row["trajectory_success"] for row in branches.values())
                for branches in complete
            ),
            "selected_action_changes_across_branches": _mean(
                branches["aligned"].get("post_gap_action")
                != branches["misaligned"].get("post_gap_action")
                for branches in complete
            ),
            "by_branch": {
                branch: {
                    "n": len(group),
                    "post_gap_accuracy": _mean(
                        row["post_gap_success"] for row in group
                    ),
                    "strict_trajectory_accuracy": _mean(
                        row["trajectory_success"] for row in group
                    ),
                }
                for branch, group in sorted(by_branch.items())
            },
        }
    return output


def build_metrics(rows: list[dict]) -> dict[str, Any]:
    """Build complete nested metrics grouped by model and condition."""

    successful_attempts = [row for row in rows if not row.get("error")]
    valid = completed_trajectories(rows)
    scenario_count = len({row.get("scenario_id") for row in valid})
    observed_seeds = {row.get("seed") for row in valid}
    models = defaultdict(list)
    for row in valid:
        models[row["model"]].append(row)
    output = {
        "inputs": sorted({row["_source"] for row in rows}),
        "attempt_rows": len(rows),
        "unique_completed_trajectories": len(valid),
        "duplicate_success_rows": len(successful_attempts) - len(valid),
        "error_attempt_rows": sum(bool(row.get("error")) for row in rows),
        "observed_scenarios": scenario_count,
        "observed_seeds": len(observed_seeds),
        "models": {},
    }
    for model, model_rows in sorted(models.items()):
        condition_groups = defaultdict(list)
        for row in model_rows:
            condition_groups[row["condition"]].append(row)
        conditions = {}
        for condition in CONTROL_CONDITIONS:
            group = condition_groups.get(condition)
            if not group:
                continue
            primary = summarize(group)
            beliefs = summarize_beliefs(group)
            conditions[condition] = {
                "primary": primary,
                "action_trajectory_success": _mean(
                    row["action_trajectory_success"] for row in group
                ),
                "beliefs": beliefs,
                "usage": usage_summary(group),
                "failure_tags": dict(
                    Counter(
                        tag
                        for row in group
                        if not row["trajectory_success"]
                        for tag in row.get("failure_tags", [])
                    )
                ),
            }
        controls = paired_controls(model_rows)
        failures = Counter(
            tag
            for row in model_rows
            if not row["trajectory_success"]
            for tag in row.get("failure_tags", [])
        )
        model_scenarios = len({row["scenario_id"] for row in model_rows})
        model_seeds = len({row["seed"] for row in model_rows})
        expected_per_model = (
            model_scenarios * len(condition_groups) * max(model_seeds, 1)
        )
        output["models"][model] = {
            "usage": usage_summary(model_rows),
            "coverage": {
                "completed": len(model_rows),
                "expected": expected_per_model,
                "fraction": len(model_rows) / expected_per_model,
            },
            "overall": {
                "n": len(model_rows),
                "failed_trajectories": sum(
                    not row["trajectory_success"] for row in model_rows
                ),
                "trajectory_success": _mean(
                    row["trajectory_success"] for row in model_rows
                ),
                "action_trajectory_success": _mean(
                    row["action_trajectory_success"] for row in model_rows
                ),
                "pre_gap_success": _mean(
                    row["pre_gap_success"] for row in model_rows
                ),
                "post_gap_success": _mean(
                    row["post_gap_success"] for row in model_rows
                ),
                "belief_reporting_success": _mean(
                    row["belief_reporting_success"] for row in model_rows
                ),
                "state_belief_success": _mean(
                    row["state_belief_success"] for row in model_rows
                ),
            },
            "conditions": conditions,
            "controls": controls,
            "full_audio_by_domain": slice_metrics(model_rows, "domain"),
            "full_audio_by_bucket": slice_metrics(model_rows, "bucket"),
            "causal_clue": causal_clue_summary(model_rows),
            "failure_tags": dict(failures),
            "difficulty_flags": difficulty_flags(model_rows, controls),
        }
    return _safe_json(output)


def write_pretty_sources(by_source: dict[str, list[dict]]) -> list[Path]:
    """Ensure every compact checkpoint file has an indented JSON sidecar."""

    outputs = []
    for source, rows in by_source.items():
        path = Path(source)
        target = (
            path.with_suffix(".json")
            if path.suffix.lower() == ".jsonl"
            else path.with_name(path.stem + "_pretty.json")
        )
        target.write_text(
            json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        outputs.append(target)
    return outputs


def write_metrics_csv(metrics: dict[str, Any], path: Path) -> None:
    """Write one flat, spreadsheet-friendly row per model and condition."""

    fields = [
        "model",
        "condition",
        "n",
        "trajectory_pass1",
        "pass_k",
        "pass_at_k",
        "domain_ci_low",
        "domain_ci_high",
        "action_trajectory_success",
        "pre_gap_success",
        "post_gap_success",
        "belief_validity",
        "belief_pre_accuracy",
        "belief_post_observation_accuracy",
        "belief_pre_final_accuracy",
        "revision_gain",
        "stale_belief_persistence",
        "brier",
        "ece",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "cost",
        "model_calls",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for model, model_data in metrics["models"].items():
            overall = model_data["overall"]
            writer.writerow(
                {
                    "model": model,
                    "condition": "__overall_partial__",
                    "n": overall["n"],
                    "trajectory_pass1": overall["trajectory_success"],
                    "action_trajectory_success": overall[
                        "action_trajectory_success"
                    ],
                    "pre_gap_success": overall["pre_gap_success"],
                    "post_gap_success": overall["post_gap_success"],
                    "belief_validity": overall["belief_reporting_success"],
                    "prompt_tokens": model_data["usage"]["prompt_tokens"],
                    "completion_tokens": model_data["usage"]["completion_tokens"],
                    "total_tokens": model_data["usage"]["total_tokens"],
                    "cost": model_data["usage"]["cost"],
                    "model_calls": model_data["usage"]["model_calls"],
                }
            )
            for condition, data in model_data["conditions"].items():
                primary = data["primary"]
                beliefs = data["beliefs"]
                usage = data["usage"]
                writer.writerow(
                    {
                        "model": model,
                        "condition": condition,
                        "n": primary["n"],
                        "trajectory_pass1": primary["pass1"],
                        "pass_k": primary["pass_k"],
                        "pass_at_k": primary["pass_at_k"],
                        "domain_ci_low": primary["ci"][0],
                        "domain_ci_high": primary["ci"][1],
                        "action_trajectory_success": data[
                            "action_trajectory_success"
                        ],
                        "pre_gap_success": primary["pre"],
                        "post_gap_success": primary["post"],
                        "belief_validity": _mean(
                            value
                            for value in beliefs["checkpoint_validity"].values()
                            if value is not None
                        ),
                        "belief_pre_accuracy": beliefs["checkpoint_accuracy"][
                            "pre_gap"
                        ],
                        "belief_post_observation_accuracy": beliefs[
                            "checkpoint_accuracy"
                        ]["post_observation"],
                        "belief_pre_final_accuracy": beliefs[
                            "checkpoint_accuracy"
                        ]["pre_final_action"],
                        "revision_gain": beliefs["revision_gain"],
                        "stale_belief_persistence": beliefs[
                            "stale_belief_persistence"
                        ],
                        "brier": beliefs["mean_brier"],
                        "ece": beliefs["ece"],
                        "prompt_tokens": usage["prompt_tokens"],
                        "completion_tokens": usage["completion_tokens"],
                        "total_tokens": usage["total_tokens"],
                        "cost": usage["cost"],
                        "model_calls": usage["model_calls"],
                    }
                )


def write_trajectories_csv(rows: list[dict], path: Path) -> None:
    """Write compact per-trajectory outcomes without deeply nested JSON."""

    fields = [
        "source",
        "model",
        "scenario_id",
        "domain",
        "bucket",
        "causal_pair_id",
        "causal_branch",
        "condition",
        "seed",
        "trajectory_success",
        "action_trajectory_success",
        "pre_gap_success",
        "post_gap_success",
        "belief_reporting_success",
        "state_belief_success",
        "response_style_success",
        "failure_tags",
        "model_calls",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "cost",
        "latency_s",
        "error",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            usage = row.get("api_usage", {})
            writer.writerow(
                {
                    "source": row["_source"],
                    "model": row.get("model"),
                    "scenario_id": row.get("scenario_id"),
                    "domain": row.get("domain"),
                    "bucket": row.get("bucket"),
                    "causal_pair_id": row.get("causal_pair_id"),
                    "causal_branch": row.get("causal_branch"),
                    "condition": row.get("condition"),
                    "seed": row.get("seed"),
                    "trajectory_success": row.get("trajectory_success"),
                    "action_trajectory_success": row.get(
                        "action_trajectory_success"
                    ),
                    "pre_gap_success": row.get("pre_gap_success"),
                    "post_gap_success": row.get("post_gap_success"),
                    "belief_reporting_success": row.get(
                        "belief_reporting_success"
                    ),
                    "state_belief_success": row.get("state_belief_success"),
                    "response_style_success": row.get("response_style_success"),
                    "failure_tags": ";".join(row.get("failure_tags", [])),
                    "model_calls": usage.get("model_calls"),
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                    "cost": usage.get("cost"),
                    "latency_s": row.get("latency_s"),
                    "error": row.get("error"),
                }
            )


def markdown_report(metrics: dict[str, Any]) -> str:
    """Render the aggregate metrics as readable Markdown tables."""

    lines = [
        "# DUAL-AudioBench evaluation report",
        "",
        f"- Raw attempt rows: {metrics['attempt_rows']}",
        f"- Unique completed trajectories: "
        f"{metrics['unique_completed_trajectories']}",
        f"- Duplicate successful rows ignored in metrics: "
        f"{metrics['duplicate_success_rows']}",
        f"- API/runtime error attempts: {metrics['error_attempt_rows']}",
        f"- Models: {', '.join(metrics['models'])}",
        "",
        "A trajectory passes only when both actions, any scored response style, "
        "all belief reports, and all hidden-state top predictions pass.",
    ]
    for model, data in metrics["models"].items():
        usage = data["usage"]
        coverage = data["coverage"]
        overall = data["overall"]
        lines.extend(
            [
                "",
                f"## {model}",
                "",
                f"- Coverage: {coverage['completed']}/{coverage['expected']} "
                f"trajectories ({coverage['fraction']:.1%})",
                f"- Overall partial outcomes: "
                f"{_percent(overall['pre_gap_success'])} pre-gap, "
                f"{_percent(overall['post_gap_success'])} post-gap, "
                f"{_percent(overall['action_trajectory_success'])} both actions, "
                f"{_percent(overall['trajectory_success'])} strict trajectory",
                f"- API calls: {usage['model_calls']:,} "
                f"({usage['metered_calls']:,} metered)",
                f"- Tokens: {usage['total_tokens']:,} "
                f"({usage['prompt_tokens']:,} prompt + "
                f"{usage['completion_tokens']:,} completion)",
                f"- Reported API cost: ${usage['cost']:.4f}",
                f"- API request time: {usage['request_latency_s'] / 60:.1f} minutes",
                "",
                "### Condition metrics",
                "",
                "| Condition | n | Full pass | Pre | Post | Belief valid | "
                "Belief pre | Belief post | Cost |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for condition in CONTROL_CONDITIONS:
            condition_data = data["conditions"].get(condition)
            if not condition_data:
                continue
            primary = condition_data["primary"]
            beliefs = condition_data["beliefs"]
            validity_values = [
                value
                for value in beliefs["checkpoint_validity"].values()
                if value is not None
            ]
            validity = _mean(validity_values)
            lines.append(
                f"| {condition} | {primary['n']} | {_percent(primary['pass1'])} | "
                f"{_percent(primary['pre'])} | {_percent(primary['post'])} | "
                f"{_percent(validity)} | "
                f"{_percent(beliefs['checkpoint_accuracy']['pre_gap'])} | "
                f"{_percent(beliefs['checkpoint_accuracy']['post_observation'])} | "
                f"${condition_data['usage']['cost']:.4f} |"
            )
        controls = data["controls"]
        lines.extend(
            [
                "",
                "### Matched controls",
                "",
                "| Control | Paired n | Domains | Effect | 95% CI | p |",
                "|---|---:|---:|---:|---:|---:|",
                "| Full audio - clue removed, post-gap | "
                f"{controls['clue_ablation_post_gap']['paired_n']} | "
                f"{controls['clue_ablation_post_gap']['clusters']} | "
                f"{_percent(controls['clue_ablation_post_gap']['delta'])} | "
                f"{_percent(controls['clue_ablation_post_gap']['ci'][0])} to "
                f"{_percent(controls['clue_ablation_post_gap']['ci'][1])} | "
                f"{_number(controls['clue_ablation_post_gap']['p_value'], 4)} |",
                "| Full audio - clue removed, full trajectory | "
                f"{controls['clue_ablation_trajectory']['paired_n']} | "
                f"{controls['clue_ablation_trajectory']['clusters']} | "
                f"{_percent(controls['clue_ablation_trajectory']['delta'])} | "
                f"{_percent(controls['clue_ablation_trajectory']['ci'][0])} to "
                f"{_percent(controls['clue_ablation_trajectory']['ci'][1])} | "
                f"{_number(controls['clue_ablation_trajectory']['p_value'], 4)} |",
                "| Hidden user action - full audio, post-gap | "
                f"{controls['hidden_user_action_post_gap']['paired_n']} | "
                f"{controls['hidden_user_action_post_gap']['clusters']} | "
                f"{_percent(controls['hidden_user_action_post_gap']['delta'])} | "
                f"{_percent(controls['hidden_user_action_post_gap']['ci'][0])} to "
                f"{_percent(controls['hidden_user_action_post_gap']['ci'][1])} | "
                f"{_number(controls['hidden_user_action_post_gap']['p_value'], 4)} |",
                "| Transcript - full audio, pre-gap action | "
                f"{controls['modality_pre_gap_action']['paired_n']} | "
                f"{controls['modality_pre_gap_action']['clusters']} | "
                f"{_percent(controls['modality_pre_gap_action']['delta'])} | "
                f"{_percent(controls['modality_pre_gap_action']['ci'][0])} to "
                f"{_percent(controls['modality_pre_gap_action']['ci'][1])} | "
                f"{_number(controls['modality_pre_gap_action']['p_value'], 4)} |",
                "| Transcript - full audio, post-gap action | "
                f"{controls['modality_post_gap_action']['paired_n']} | "
                f"{controls['modality_post_gap_action']['clusters']} | "
                f"{_percent(controls['modality_post_gap_action']['delta'])} | "
                f"{_percent(controls['modality_post_gap_action']['ci'][0])} to "
                f"{_percent(controls['modality_post_gap_action']['ci'][1])} | "
                f"{_number(controls['modality_post_gap_action']['p_value'], 4)} |",
                "| Transcript - full audio, immediate belief | "
                f"{controls['modality_post_observation_belief']['paired_n']} | "
                f"{controls['modality_post_observation_belief']['clusters']} | "
                f"{_percent(controls['modality_post_observation_belief']['delta'])} | "
                f"{_percent(controls['modality_post_observation_belief']['ci'][0])} to "
                f"{_percent(controls['modality_post_observation_belief']['ci'][1])} | "
                f"{_number(controls['modality_post_observation_belief']['p_value'], 4)} |",
                "| Transcript - full audio, strict trajectory | "
                f"{controls['modality_trajectory']['paired_n']} | "
                f"{controls['modality_trajectory']['clusters']} | "
                f"{_percent(controls['modality_trajectory']['delta'])} | "
                f"{_percent(controls['modality_trajectory']['ci'][0])} to "
                f"{_percent(controls['modality_trajectory']['ci'][1])} | "
                f"{_number(controls['modality_trajectory']['p_value'], 4)} |",
                "| Full audio - no-state-change gap, post-gap | "
                f"{controls['state_change_post_gap']['paired_n']} | "
                f"{controls['state_change_post_gap']['clusters']} | "
                f"{_percent(controls['state_change_post_gap']['delta'])} | "
                f"{_percent(controls['state_change_post_gap']['ci'][0])} to "
                f"{_percent(controls['state_change_post_gap']['ci'][1])} | "
                f"{_number(controls['state_change_post_gap']['p_value'], 4)} |",
                "| Neutral audio - full audio, immediate belief | "
                f"{controls['neutral_audio_post_observation_belief']['paired_n']} | "
                f"{controls['neutral_audio_post_observation_belief']['clusters']} | "
                f"{_percent(controls['neutral_audio_post_observation_belief']['delta'])} | "
                f"{_percent(controls['neutral_audio_post_observation_belief']['ci'][0])} to "
                f"{_percent(controls['neutral_audio_post_observation_belief']['ci'][1])} | "
                f"{_number(controls['neutral_audio_post_observation_belief']['p_value'], 4)} |",
                "",
                "### Prosody selectivity",
                "",
                f"- Identical-transcript pairs: {controls['prosody'].get('paired_n', 0)}; "
                f"unique stimuli: {controls['prosody'].get('unique_stimuli', 0)}.",
                f"- High-affect style accuracy: "
                f"{_percent(controls['prosody'].get('high_style', {}).get('mean'))} "
                f"[{_percent(controls['prosody'].get('high_style', {}).get('ci', [None, None])[0])}, "
                f"{_percent(controls['prosody'].get('high_style', {}).get('ci', [None, None])[1])}].",
                f"- Low-affect style accuracy: "
                f"{_percent(controls['prosody'].get('low_style', {}).get('mean'))} "
                f"[{_percent(controls['prosody'].get('low_style', {}).get('ci', [None, None])[0])}, "
                f"{_percent(controls['prosody'].get('low_style', {}).get('ci', [None, None])[1])}].",
                f"- Both deliveries correct: "
                f"{_percent(controls['prosody'].get('both_style_correct', {}).get('mean'))} "
                f"[{_percent(controls['prosody'].get('both_style_correct', {}).get('ci', [None, None])[0])}, "
                f"{_percent(controls['prosody'].get('both_style_correct', {}).get('ci', [None, None])[1])}] "
                f"(random pair chance "
                f"{_percent(controls['prosody'].get('both_style_random_chance'))}).",
                f"- Directional style contrast: "
                f"{_percent(controls['prosody'].get('style_contrast', {}).get('mean'))} "
                f"[{_percent(controls['prosody'].get('style_contrast', {}).get('ci', [None, None])[0])}, "
                f"{_percent(controls['prosody'].get('style_contrast', {}).get('ci', [None, None])[1])}].",
                f"- Technical-action invariance: "
                f"{_percent(controls['prosody'].get('technical_action_invariance', {}).get('mean'))} "
                f"[{_percent(controls['prosody'].get('technical_action_invariance', {}).get('ci', [None, None])[0])}, "
                f"{_percent(controls['prosody'].get('technical_action_invariance', {}).get('ci', [None, None])[1])}].",
                f"- Post-observation top-belief invariance: "
                f"{_percent(controls['prosody'].get('post_observation_top_belief_invariance', {}).get('mean'))} "
                f"[{_percent(controls['prosody'].get('post_observation_top_belief_invariance', {}).get('ci', [None, None])[0])}, "
                f"{_percent(controls['prosody'].get('post_observation_top_belief_invariance', {}).get('ci', [None, None])[1])}].",
                f"- Post-observation belief JSD: "
                f"{_number(controls['prosody'].get('post_observation_belief_jsd', {}).get('mean'))} "
                f"[{_number(controls['prosody'].get('post_observation_belief_jsd', {}).get('ci', [None, None])[0])}, "
                f"{_number(controls['prosody'].get('post_observation_belief_jsd', {}).get('ci', [None, None])[1])}].",
                f"- Pre-final belief JSD: "
                f"{_number(controls['prosody'].get('pre_final_belief_jsd', {}).get('mean'))} "
                f"[{_number(controls['prosody'].get('pre_final_belief_jsd', {}).get('ci', [None, None])[0])}, "
                f"{_number(controls['prosody'].get('pre_final_belief_jsd', {}).get('ci', [None, None])[1])}].",
            ]
        )
        causal = data.get("causal_clue")
        if causal:
            lines.extend(
                [
                    "",
                    "### Causal clue counterfactuals",
                    "",
                    "Each pair changes only the early clue and corresponding hidden "
                    "branch. Gold post-gap actions differ. After clue removal, a "
                    "deterministic policy cannot exceed 50% post-gap accuracy across "
                    "balanced indistinguishable branches.",
                    "",
                    "| Condition | Pairs | Post | Strict | Both post-correct | "
                    "Both strict | Action changes |",
                    "|---|---:|---:|---:|---:|---:|---:|",
                ]
            )
            for condition, values in causal["conditions"].items():
                lines.append(
                    f"| {condition} | {values['complete_counterfactual_pairs']} | "
                    f"{_percent(values['post_gap_accuracy'])} | "
                    f"{_percent(values['strict_trajectory_accuracy'])} | "
                    f"{_percent(values['both_branches_post_gap_correct'])} | "
                    f"{_percent(values['both_branches_strict_correct'])} | "
                    f"{_percent(values['selected_action_changes_across_branches'])} |"
                )
        lines.extend(
            [
                "",
                "### Full-audio slices",
                "",
                "| Slice | n | Full pass | Two-action pass | Pre | Post |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for kind, slices in (
            ("domain", data["full_audio_by_domain"]),
            ("bucket", data["full_audio_by_bucket"]),
        ):
            for name, values in slices.items():
                lines.append(
                    f"| {kind}: {name} | {values['n']} | "
                    f"{_percent(values['trajectory_success'])} | "
                    f"{_percent(values['action_trajectory_success'])} | "
                    f"{_percent(values['pre_gap_success'])} | "
                    f"{_percent(values['post_gap_success'])} |"
                )
        lines.extend(["", "### Failure tags", ""])
        failures = data["failure_tags"]
        if failures:
            total_failures = overall["failed_trajectories"]
            for tag, count in sorted(
                failures.items(), key=lambda item: (-item[1], item[0])
            ):
                lines.append(
                    f"- `{tag}`: {count} "
                    f"({count / total_failures:.1%} of failed trajectories)"
                )
        else:
            lines.append("- None.")
        lines.extend(["", "### Difficulty assessment", ""])
        lines.extend(f"- {flag}" for flag in data["difficulty_flags"])
    lines.extend(
        [
            "",
            "## Interpretation cautions",
            "",
            f"- Results contain {metrics['observed_seeds']} observed run seed(s); "
            "pass@k is labeled with the number actually available.",
            "- `transcript_only` is a control; audio conditions replay synthesized "
            "alternating turns.",
            "- Human annotation and audible-prosody validation remain separate "
            "validation steps and are not replaced by model scores.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows, by_source = load_files(args.inputs)
    readable = write_pretty_sources(by_source)
    metrics = build_metrics(rows)

    metrics_path = args.out_dir / "metrics.json"
    metrics_path.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_metrics_csv(metrics, args.out_dir / "metrics.csv")
    write_trajectories_csv(rows, args.out_dir / "trajectories.csv")
    report_path = args.out_dir / "report.md"
    report_path.write_text(markdown_report(metrics), encoding="utf-8")

    valid = completed_trajectories(rows)
    for model in metrics["models"]:
        model_rows = [row for row in valid if row["model"] == model]
        retention_curve(
            model_rows,
            args.out_dir / f"{_slug(model)}_retention.png",
        )
        modality_belief_curve(
            model_rows,
            args.out_dir / f"{_slug(model)}_modality_belief.png",
        )
        prosody_summary_plot(
            model_rows,
            args.out_dir / f"{_slug(model)}_prosody.png",
        )

    print(f"Readable trajectories: {', '.join(map(str, readable))}")
    print(f"Markdown report -> {report_path}")
    print(f"Metrics JSON/CSV -> {metrics_path}, {args.out_dir / 'metrics.csv'}")
    print(f"Trajectory CSV -> {args.out_dir / 'trajectories.csv'}")


if __name__ == "__main__":
    main()
