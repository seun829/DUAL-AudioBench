"""Export and score a blinded one-author audit of automatic failure tags.

Usage:
  python -m dual_audio.evaluation.failure_tag_audit export \
      data/scenarios_v05 \
      paper_results/v05/reports/priority_preliminary/trajectories.csv \
      paper_results/v05/internal_audit author_01

  python -m dual_audio.evaluation.failure_tag_audit report \
      paper_results/v05/internal_audit author_01
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from dual_audio.evaluation.audit_utils import (
    completed_gold_items,
    safe_slug,
    stable_rng,
)


RESPONSE_FIELDS = (
    "auditor",
    "audit_item_id",
    "labels_semicolon_separated",
    "evidence_or_reason",
    "confidence_1_to_5",
    "notes",
)

EXTRA_TAG_DEFINITIONS = {
    "OFF_MENU_RESPONSE": "No valid action from the displayed menu was recorded.",
}


def _bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def _summary_candidates(
    summary_path: Path, scenario_ids: set[str]
) -> list[dict[str, str]]:
    with summary_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row
        for row in rows
        if row.get("scenario_id") in scenario_ids
        and not _bool(row.get("trajectory_success"))
        and not row.get("error", "").strip()
    ]


def _tags(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(
        sorted(tag.strip() for tag in row.get("failure_tags", "").split(";") if tag.strip())
    )


def _select_trajectories(
    gold_items: list[dict], candidates: list[dict[str, str]], auditor: str
) -> list[dict[str, str]]:
    """Select one failed trajectory per gold scenario with balanced coverage."""

    models = sorted({row["model"] for row in candidates})
    conditions = sorted({row["condition"] for row in candidates})
    combinations = [
        (model, condition)
        for model in models
        for condition in conditions
        if any(
            row["model"] == model and row["condition"] == condition
            for row in candidates
        )
    ]
    stable_rng(auditor, "failure_tag_combinations").shuffle(combinations)
    global_tags = Counter(tag for row in candidates for tag in _tags(row))
    model_counts: Counter[str] = Counter()
    condition_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    selected = []

    for index, gold in enumerate(gold_items):
        scenario_candidates = [
            row for row in candidates if row["scenario_id"] == gold["scenario_id"]
        ]
        if not scenario_candidates:
            raise SystemExit(
                f"No failed trajectory found for gold scenario {gold['scenario_id']}."
            )
        desired = combinations[index % len(combinations)]
        preferred = [
            row
            for row in scenario_candidates
            if (row["model"], row["condition"]) == desired
        ]
        pool = preferred or scenario_candidates
        stable_rng(auditor, gold["scenario_id"], "failure_candidates").shuffle(pool)

        def score(row: dict[str, str]) -> tuple[float, ...]:
            row_tags = _tags(row)
            rarity = sum(1 / global_tags[tag] for tag in row_tags)
            return (
                model_counts[row["model"]],
                condition_counts[row["condition"]],
                sum(tag_counts[tag] for tag in row_tags),
                -rarity,
                -len(row_tags),
            )

        chosen = min(pool, key=score)
        selected.append(chosen)
        model_counts[chosen["model"]] += 1
        condition_counts[chosen["condition"]] += 1
        tag_counts.update(_tags(chosen))
    return selected


def _load_trajectory(
    summary: dict[str, str], cache: dict[Path, list[dict]]
) -> dict[str, Any]:
    path = Path(summary["source"])
    if not path.is_absolute():
        path = Path.cwd() / path
    if path not in cache:
        cache[path] = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    for row in cache[path]:
        if (
            row.get("model") == summary["model"]
            and row.get("scenario_id") == summary["scenario_id"]
            and row.get("condition") == summary["condition"]
            and str(row.get("seed")) == summary["seed"]
            and not row.get("error")
        ):
            return row
    raise SystemExit(
        "Could not locate summarized trajectory in source file: "
        f"{summary['scenario_id']}/{summary['model']}/{summary['condition']}/"
        f"seed={summary['seed']}"
    )


def _action_description(row: dict, stage: str, action: str | None) -> str:
    if not action:
        return "No valid menu action was recorded."
    for item in row[f"{stage}_menu"]:
        if item.get("label") == row.get(f"{stage}_action_label"):
            return item["description"]
    return action.replace("_", " ")


def _expected_description(task: dict, stage: str, expected: str | None) -> str:
    for item in task[f"{stage}_actions"]:
        if item["action"] == expected:
            return item["description"]
    task_action = str(expected or "").replace("_", " ")
    return task_action or "No expected action recorded."


def _dialogue_markdown(row: dict) -> list[str]:
    lines = []
    for index, turn in enumerate(row.get("turns", []), start=1):
        speaker = str(turn.get("role", "unknown")).capitalize()
        lines.append(f"{index}. **{speaker}:** {turn.get('text', '')}")
    return lines


def _belief_markdown(row: dict) -> list[str]:
    names = {
        "pre_gap": "Before the gap",
        "post_observation": "Immediately after resumption",
        "pre_final_action": "With the final action",
    }
    lines = [
        "| Checkpoint | State variable | Correct value | Model's top value | Confidence | Correct? |",
        "|---|---|---|---|---:|:---:|",
    ]
    for checkpoint, title in names.items():
        evaluation = (
            row.get("belief_checkpoints", {})
            .get(checkpoint, {})
            .get("evaluation", {})
        )
        variables = evaluation.get("variables", {})
        if not variables:
            lines.append(f"| {title} | --- | --- | missing report | --- | no |")
            continue
        for variable, result in variables.items():
            confidence = result.get("confidence")
            rendered_confidence = (
                f"{float(confidence):.2f}" if confidence is not None else "---"
            )
            lines.append(
                f"| {title} | `{variable}` | `{result.get('target')}` | "
                f"`{result.get('top_state')}` | {rendered_confidence} | "
                f"{'yes' if result.get('correct') else 'no'} |"
            )
    return lines


def export_packet(
    tasks_dir: str,
    trajectory_summary: str,
    audit_root: str,
    auditor: str,
) -> None:
    """Export a blinded 21-trajectory packet tied to the scenario gold set."""

    root = Path(audit_root)
    output = root / "failure_tags"
    public = output / "public"
    private = output / "private"
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    slug = safe_slug(auditor)
    gold_items = completed_gold_items(root, auditor)
    scenario_ids = {item["scenario_id"] for item in gold_items}
    tasks = {
        task["scenario_id"]: task
        for path in sorted(Path(tasks_dir).glob("*.json"))
        for task in [json.loads(path.read_text(encoding="utf-8"))]
    }
    missing = scenario_ids - set(tasks)
    if missing:
        raise SystemExit(f"Gold scenarios missing from task directory: {sorted(missing)}")

    definitions: dict[str, str] = dict(EXTRA_TAG_DEFINITIONS)
    for scenario_id in scenario_ids:
        for tag, description in tasks[scenario_id]["tag_definitions"].items():
            previous = definitions.get(tag)
            if previous is not None and previous != description:
                raise SystemExit(f"Conflicting definition for failure tag {tag}.")
            definitions[tag] = description
    definitions.pop("PROSODY_GROUNDING_FAILURE", None)

    candidates = _summary_candidates(Path(trajectory_summary), scenario_ids)
    selected = _select_trajectories(gold_items, candidates, auditor)
    cache: dict[Path, list[dict]] = {}
    trajectories = [_load_trajectory(row, cache) for row in selected]
    paired = list(zip(gold_items, selected, trajectories))
    stable_rng(auditor, "failure_tag_item_order").shuffle(paired)

    lines = [
        f"# DUAL-AudioBench internal failure-tag audit ({auditor})",
        "",
        "This packet contains one failed model trajectory for each scenario in",
        f"the prespecified {len(gold_items)}-scenario author gold set. Model names,",
        "conditions, and automatic tags are hidden. Judge only the recorded",
        "dialogue, actions, states, and belief summaries below.",
        "",
        "Select every supported tag. Tags are not mutually exclusive. Enter exact",
        "tag names separated by semicolons; enter `NONE` when no listed tag is",
        "supported. Do not infer an unobservable mental process beyond the trace.",
        "Confidence is 1 (guessing) through 5 (certain).",
        "",
        "## Tag definitions",
        "",
    ]
    for tag in sorted(definitions):
        lines.append(f"- `{tag}`: {definitions[tag]}")
    lines.append("")

    key: dict[str, Any] = {
        "auditor": auditor,
        "gold_set_size": len(gold_items),
        "selection": "one failed trajectory per completed author-gold scenario",
        "tag_definitions": definitions,
        "items": {},
    }
    response_rows = []
    for index, (gold, summary, row) in enumerate(paired, start=1):
        item_id = f"FAILURE-{index:02d}"
        lines.extend(
            [
                f"## Item {item_id}",
                "",
                "### Recorded dialogue",
                "",
                *_dialogue_markdown(row),
                "",
                "### Evaluated decisions",
                "",
                f"- First action selected: {_action_description(row, 'pre_gap', row.get('pre_gap_action'))}",
                f"- Expected first action: {_expected_description(tasks[gold['scenario_id']], 'pre_gap', row.get('expected_pre_gap_action'))}",
                f"- First action correct: {'yes' if row.get('pre_gap_success') else 'no'}",
                f"- Final action selected: {_action_description(row, 'post_gap', row.get('post_gap_action'))}",
                f"- Expected final action: {_expected_description(tasks[gold['scenario_id']], 'post_gap', row.get('expected_post_gap_action'))}",
                f"- Final action correct: {'yes' if row.get('post_gap_success') else 'no'}",
                "",
                "### Belief summary",
                "",
                *_belief_markdown(row),
                "",
                "Record all supported tags, a short evidence-based reason, and",
                "your confidence in the response CSV.",
                "",
                "---",
                "",
            ]
        )
        response_rows.append(
            {
                "auditor": auditor,
                "audit_item_id": item_id,
                "labels_semicolon_separated": "",
                "evidence_or_reason": "",
                "confidence_1_to_5": "",
                "notes": "",
            }
        )
        key["items"][item_id] = {
            **gold,
            "model": summary["model"],
            "condition": summary["condition"],
            "seed": int(summary["seed"]),
            "source": summary["source"],
            "automatic_tags": list(_tags(summary)),
        }

    booklet_path = public / f"{slug}_failure_tag_booklet.md"
    responses_path = public / f"{slug}_failure_tag_responses.csv"
    key_path = private / f"{slug}_failure_tag_key.json"
    booklet_path.write_text("\n".join(lines), encoding="utf-8")
    with responses_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESPONSE_FIELDS)
        writer.writeheader()
        writer.writerows(response_rows)
    key_path.write_text(
        json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Exported {len(response_rows)} blinded failure trajectories -> {public}")
    print(f"Private scoring key -> {key_path}")


def _parse_labels(raw: str, allowed: set[str]) -> set[str]:
    labels = {label.strip() for label in raw.split(";") if label.strip()}
    if labels == {"NONE"}:
        return set()
    unknown = labels - allowed
    if unknown:
        raise SystemExit(f"Unknown failure tags in response: {sorted(unknown)}")
    return labels


def report(audit_root: str, auditor: str) -> None:
    """Compare automatic tags with the completed one-author gold labels."""

    root = Path(audit_root) / "failure_tags"
    slug = safe_slug(auditor)
    key = json.loads(
        (root / "private" / f"{slug}_failure_tag_key.json").read_text(
            encoding="utf-8"
        )
    )
    responses_path = root / "public" / f"{slug}_failure_tag_responses.csv"
    with responses_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != len(key["items"]):
        raise SystemExit("Failure-tag response count does not match private key.")
    allowed = set(key["tag_definitions"])
    comparisons = []
    for row in rows:
        if not row.get("labels_semicolon_separated", "").strip() or not row.get(
            "evidence_or_reason", ""
        ).strip():
            raise SystemExit(
                f"Incomplete failure-tag response: {row.get('audit_item_id')}"
            )
        item = key["items"].get(row["audit_item_id"])
        if item is None:
            raise SystemExit(f"Unknown audit item: {row['audit_item_id']}")
        human = _parse_labels(row["labels_semicolon_separated"], allowed)
        automatic = set(item["automatic_tags"])
        comparisons.append((row["audit_item_id"], automatic, human))

    tp = sum(len(auto & human) for _, auto, human in comparisons)
    fp = sum(len(auto - human) for _, auto, human in comparisons)
    fn = sum(len(human - auto) for _, auto, human in comparisons)
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    exact = sum(auto == human for _, auto, human in comparisons) / len(comparisons)
    tags = sorted(set().union(*(auto | human for _, auto, human in comparisons)))
    per_tag = []
    for tag in tags:
        tag_tp = sum(tag in auto and tag in human for _, auto, human in comparisons)
        auto_n = sum(tag in auto for _, auto, _ in comparisons)
        human_n = sum(tag in human for _, _, human in comparisons)
        per_tag.append(
            {
                "tag": tag,
                "automatic_n": auto_n,
                "human_n": human_n,
                "true_positive_n": tag_tp,
                "precision": tag_tp / auto_n if auto_n else None,
                "recall": tag_tp / human_n if human_n else None,
            }
        )
    metrics = {
        "auditor": auditor,
        "n": len(comparisons),
        "exact_set_agreement": exact,
        "micro_precision": precision,
        "micro_recall": recall,
        "micro_f1": f1,
        "per_tag": per_tag,
    }
    lines = [
        "# Internal failure-tag audit report",
        "",
        f"- Auditor: {auditor}",
        f"- Gold-set trajectories: {len(comparisons)}",
        f"- Exact tag-set agreement: {exact:.1%}",
        f"- Automatic-tag precision: {precision:.1%}",
        f"- Automatic-tag recall: {recall:.1%}",
        f"- Micro F1: {f1:.3f}",
        "",
        "This is a one-author internal adjudication, not inter-annotator agreement.",
        "",
        "| Tag | Automatic | Author | Match | Precision | Recall |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in per_tag:
        p = "---" if item["precision"] is None else f"{item['precision']:.1%}"
        r = "---" if item["recall"] is None else f"{item['recall']:.1%}"
        lines.append(
            f"| `{item['tag']}` | {item['automatic_n']} | {item['human_n']} | "
            f"{item['true_positive_n']} | {p} | {r} |"
        )
    (root / "failure_tag_audit_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    (root / "failure_tag_audit_metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Readable report -> {root / 'failure_tag_audit_report.md'}")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "export" and len(sys.argv) == 6:
        export_packet(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif command == "report" and len(sys.argv) == 4:
        report(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
