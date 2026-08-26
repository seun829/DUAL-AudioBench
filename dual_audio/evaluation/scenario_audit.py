"""Export and score blinded internal scenario-audit packets.

Usage:
  python -m dual_audio.evaluation.scenario_audit export \
      data/scenarios_v05 paper_results/v05/internal_audit author_01 author_02

  python -m dual_audio.evaluation.scenario_audit report \
      paper_results/v05/internal_audit author_01 author_02

Auditors complete phase 1 before receiving/opening phase 2. Private keys must
not be distributed with the public booklets and blank response sheets.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

from dual_audio.core.conditions import CONDITIONS
from dual_audio.core.environment import correct_action, execute_action, transition
from dual_audio.users.scripted import ScriptedUserSimulator


PRE_FIELDS = (
    "auditor",
    "audit_item_id",
    "pre_action_label",
    "causal_alignment",
    "answerable_yes_no",
    "ambiguity_1_to_5",
    "evidence_turn_or_reason",
    "notes",
)
POST_FIELDS = (
    "auditor",
    "audit_item_id",
    "terminal_state",
    "post_action_label",
    "answerable_yes_no",
    "ambiguity_1_to_5",
    "evidence_turn_or_reason",
    "notes",
)


def _rng(*parts: object) -> random.Random:
    digest = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return random.Random(digest)


def _safe_slug(value: str) -> str:
    slug = "".join(character if character.isalnum() else "_" for character in value)
    return slug.strip("_").lower() or "auditor"


def _scenario_manifest_sha256(paths: list[Path]) -> str:
    """Match the paid launcher's filename-plus-file-hash freeze digest."""

    records = [
        f"{path.name}:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        for path in sorted(paths, key=lambda path: path.name)
    ]
    return hashlib.sha256("\n".join(records).encode("utf-8")).hexdigest()


def _task_order(tasks: list[dict], auditor: str) -> list[dict]:
    """Randomize tasks without placing counterfactual siblings together."""

    for attempt in range(100):
        ordered = list(tasks)
        _rng(auditor, "task_order", attempt).shuffle(ordered)
        pair_ids = [task["causal_design"]["pair_id"] for task in ordered]
        if all(left != right for left, right in zip(pair_ids, pair_ids[1:])):
            return ordered
    raise RuntimeError("Could not separate causal siblings in audit order.")


def _menu(task: dict, stage: str, auditor: str) -> tuple[list[dict], dict[str, str]]:
    actions = [dict(item) for item in task[f"{stage}_actions"]]
    _rng(auditor, task["scenario_id"], stage, "audit_menu").shuffle(actions)
    public = []
    mapping = {}
    for index, item in enumerate(actions):
        label = chr(ord("A") + index)
        public.append({"label": label, "description": item["description"]})
        mapping[label] = item["action"]
    return public, mapping


def _gold_path(task: dict) -> tuple[dict, str]:
    action = task["pre_gap"]["correct_action"]
    state = execute_action(task["domain"], task["initial_state"], action)
    state = transition(
        task["domain"],
        state,
        action,
        task["transition"]["elapsed_minutes"],
        task["transition"]["external_event"],
        None,
    )
    observation = ScriptedUserSimulator().post_gap(
        task, state, CONDITIONS["full_audio"]
    )
    return state, observation


def _dialogue(task: dict) -> list[dict]:
    marker = task["pre_gap"]["agent_turn_index"]
    return task["turns"][:marker]


def _write_response_sheet(
    path: Path,
    auditor: str,
    item_ids: list[str],
    fields: tuple[str, ...],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item_id in item_ids:
            row = {field: "" for field in fields}
            row["auditor"] = auditor
            row["audit_item_id"] = item_id
            writer.writerow(row)


def _definitions_markdown(definitions: dict[str, str]) -> list[str]:
    return [
        f"- `{value}` — {description}"
        for value, description in definitions.items()
    ]


def _dialogue_markdown(turns: list[dict]) -> list[str]:
    rows = []
    for index, turn in enumerate(turns, start=1):
        speaker = turn["speaker"].capitalize()
        rows.append(f"{index}. **{speaker}:** {turn['text']}")
    return rows


def _menu_markdown(menu: list[dict]) -> list[str]:
    return [f"- **{item['label']}.** {item['description']}" for item in menu]


def export_packet(tasks_dir: str, output_dir: str, auditor: str) -> None:
    """Create two-phase blinded booklets, response sheets, and a private key."""

    task_paths = sorted(Path(tasks_dir).glob("*.json"))
    tasks = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in task_paths
    ]
    if not tasks:
        raise SystemExit(f"No task JSON files found in {tasks_dir}.")
    if {str(task.get("schema_version")) for task in tasks} != {"0.5"}:
        raise SystemExit("Internal causal audit requires schema-v0.5 tasks.")

    root = Path(output_dir)
    public = root / "public"
    private = root / "private"
    public.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    slug = _safe_slug(auditor)
    scenario_hash = _scenario_manifest_sha256(task_paths)
    ordered = _task_order(tasks, auditor)
    width = len(str(len(ordered)))

    phase1 = [
        f"# DUAL-AudioBench v0.5 internal audit — phase 1 ({auditor})",
        "",
        f"Scenario freeze: `{scenario_hash}`",
        "",
        "Complete the phase-1 CSV before opening phase 2. Do not inspect task",
        "JSON, code, private keys, or another auditor's responses. Select the",
        "best next action using only the public dialogue. `Answerable` asks",
        "whether exactly one option follows without outside domain knowledge.",
        "The rule-match question is simple: choose `aligned` when the user's",
        "clue satisfies the stated success rule, or `misaligned` when it",
        "violates that rule. It does not ask whether you agree with the gold.",
        "Ambiguity is 1 (unambiguous) through 5 (not answerable).",
        "",
    ]
    phase2 = [
        f"# DUAL-AudioBench v0.5 internal audit — phase 2 ({auditor})",
        "",
        f"Scenario freeze: `{scenario_hash}`",
        "",
        "Open this only after saving the completed phase-1 CSV. The benchmark's",
        "declared pre-gap operation is now shown so every auditor evaluates the",
        "same gold-path transition. Infer the terminal state and best final",
        "action from the earlier causal rule, clue, elapsed time, and resumed",
        "observation. Ambiguity is 1 (unambiguous) through 5 (not answerable).",
        "",
    ]
    key: dict[str, Any] = {
        "schema_version": "0.5",
        "scenario_manifest_sha256": scenario_hash,
        "auditor": auditor,
        "instructions": "PRIVATE: do not distribute before both phases are complete.",
        "items": {},
    }
    item_ids = []

    for index, task in enumerate(ordered, start=1):
        item_id = f"{slug.upper()}-{index:0{width}d}"
        item_ids.append(item_id)
        pre_menu, pre_mapping = _menu(task, "pre_gap", auditor)
        post_menu, post_mapping = _menu(task, "post_gap", auditor)
        gold_state, post_observation = _gold_path(task)
        outcome_variable = task["causal_design"]["outcome_variable"]
        pre_gold = task["pre_gap"]["correct_action"]
        post_gold = correct_action(task["domain"], gold_state)
        pre_gold_label = next(
            label for label, action in pre_mapping.items() if action == pre_gold
        )
        post_gold_label = next(
            label for label, action in post_mapping.items() if action == post_gold
        )
        pre_gold_description = next(
            item["description"]
            for item in task["pre_gap_actions"]
            if item["action"] == pre_gold
        )

        phase1.extend(
            [
                f"## Item {item_id}",
                "",
                "### Public dialogue",
                "",
                *_dialogue_markdown(_dialogue(task)),
                "",
                "### Does the clue match the success rule? (`causal_alignment`)",
                "",
                *_definitions_markdown(
                    task["belief_definitions"]["causal_alignment"]
                ),
                "",
                "### Candidate next actions",
                "",
                *_menu_markdown(pre_menu),
                "",
                "Record the action label, rule-match label, answerability,",
                "ambiguity, and supporting dialogue turn in the phase-1 CSV.",
                "",
                "---",
                "",
            ]
        )
        phase2.extend(
            [
                f"## Item {item_id}",
                "",
                "### Earlier public dialogue",
                "",
                *_dialogue_markdown(_dialogue(task)),
                "",
                "### Operation assumed executed",
                "",
                f"> {pre_gold_description}",
                "",
                f"After **{task['transition']['elapsed_minutes']} minutes**, the user resumes:",
                "",
                f"> {post_observation}",
                "",
                f"### Terminal-state labels for `{outcome_variable}`",
                "",
                *_definitions_markdown(
                    task["belief_definitions"][outcome_variable]
                ),
                "",
                "### Candidate final actions",
                "",
                *_menu_markdown(post_menu),
                "",
                "Record the terminal-state label, final-action label,",
                "answerability, ambiguity, and evidence in the phase-2 CSV.",
                "",
                "---",
                "",
            ]
        )
        key["items"][item_id] = {
            "scenario_id": task["scenario_id"],
            "causal_pair_id": task["causal_design"]["pair_id"],
            "causal_branch": task["causal_design"]["branch"],
            "pre_action_mapping": pre_mapping,
            "gold_pre_action": pre_gold,
            "gold_pre_action_label": pre_gold_label,
            "gold_causal_alignment": task["causal_design"]["branch"],
            "outcome_variable": outcome_variable,
            "gold_terminal_state": gold_state[outcome_variable],
            "post_action_mapping": post_mapping,
            "gold_post_action": post_gold,
            "gold_post_action_label": post_gold_label,
        }

    (public / f"{slug}_phase1_booklet.md").write_text(
        "\n".join(phase1), encoding="utf-8"
    )
    (public / f"{slug}_phase2_booklet.md").write_text(
        "\n".join(phase2), encoding="utf-8"
    )
    _write_response_sheet(
        public / f"{slug}_phase1_responses.csv", auditor, item_ids, PRE_FIELDS
    )
    _write_response_sheet(
        public / f"{slug}_phase2_responses.csv", auditor, item_ids, POST_FIELDS
    )
    (private / f"{slug}_key.json").write_text(
        json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Exported {len(tasks)} blinded items for {auditor} -> {public}")
    print(f"Private scoring key -> {private / f'{slug}_key.json'}")


def _read_responses(path: Path, fields: tuple[str, ...]) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    missing_columns = set(fields) - set(rows[0] if rows else {})
    if missing_columns:
        raise SystemExit(f"{path} lacks columns: {sorted(missing_columns)}")
    required_answers = [field for field in fields if field not in {"notes"}]
    for row in rows:
        if any(not row[field].strip() for field in required_answers):
            raise SystemExit(
                f"Incomplete response in {path}: {row.get('audit_item_id')}"
            )
    return {row["audit_item_id"]: row for row in rows}


def _score_auditor(root: Path, auditor: str) -> tuple[dict[str, Any], dict[str, dict]]:
    slug = _safe_slug(auditor)
    key = json.loads((root / "private" / f"{slug}_key.json").read_text(encoding="utf-8"))
    pre = _read_responses(
        root / "public" / f"{slug}_phase1_responses.csv", PRE_FIELDS
    )
    post = _read_responses(
        root / "public" / f"{slug}_phase2_responses.csv", POST_FIELDS
    )
    if set(pre) != set(key["items"]) or set(post) != set(key["items"]):
        raise SystemExit(f"{auditor} response IDs do not match its private key.")

    canonical = {}
    mismatch_rows = []
    for item_id, gold in key["items"].items():
        pre_row, post_row = pre[item_id], post[item_id]
        pre_action = gold["pre_action_mapping"].get(
            pre_row["pre_action_label"].strip().upper(), "INVALID"
        )
        post_action = gold["post_action_mapping"].get(
            post_row["post_action_label"].strip().upper(), "INVALID"
        )
        observed = {
            "pre_action": pre_action,
            "causal_alignment": pre_row["causal_alignment"].strip().lower(),
            "terminal_state": post_row["terminal_state"].strip().lower(),
            "post_action": post_action,
            "pre_answerable": pre_row["answerable_yes_no"].strip().lower(),
            "post_answerable": post_row["answerable_yes_no"].strip().lower(),
            "pre_ambiguity": pre_row["ambiguity_1_to_5"].strip(),
            "post_ambiguity": post_row["ambiguity_1_to_5"].strip(),
        }
        expected = {
            "pre_action": gold["gold_pre_action"],
            "causal_alignment": gold["gold_causal_alignment"],
            "terminal_state": gold["gold_terminal_state"],
            "post_action": gold["gold_post_action"],
        }
        canonical[gold["scenario_id"]] = observed
        disagreements = [
            field for field, value in expected.items() if observed[field] != value
        ]
        if disagreements or observed["pre_answerable"] != "yes" or observed["post_answerable"] != "yes":
            mismatch_rows.append(
                {
                    "scenario_id": gold["scenario_id"],
                    "audit_item_id": item_id,
                    "disputed_fields": ";".join(disagreements),
                    "pre_answerable": observed["pre_answerable"],
                    "post_answerable": observed["post_answerable"],
                    "pre_notes": pre_row["notes"],
                    "post_notes": post_row["notes"],
                }
            )
    n = len(key["items"])
    metrics = {
        "auditor": auditor,
        "scenario_manifest_sha256": key.get("scenario_manifest_sha256"),
        "n": n,
        "pre_action_accuracy": sum(
            row["pre_action"] == key["items"][item_id]["gold_pre_action"]
            for item_id, row in ((item, canonical[gold["scenario_id"]]) for item, gold in key["items"].items())
        ) / n,
        "causal_alignment_accuracy": sum(
            row["causal_alignment"] == key["items"][item_id]["gold_causal_alignment"]
            for item_id, row in ((item, canonical[gold["scenario_id"]]) for item, gold in key["items"].items())
        ) / n,
        "terminal_state_accuracy": sum(
            row["terminal_state"] == key["items"][item_id]["gold_terminal_state"]
            for item_id, row in ((item, canonical[gold["scenario_id"]]) for item, gold in key["items"].items())
        ) / n,
        "post_action_accuracy": sum(
            row["post_action"] == key["items"][item_id]["gold_post_action"]
            for item_id, row in ((item, canonical[gold["scenario_id"]]) for item, gold in key["items"].items())
        ) / n,
        "pre_answerable_rate": sum(row["pre_answerable"] == "yes" for row in canonical.values()) / n,
        "post_answerable_rate": sum(row["post_answerable"] == "yes" for row in canonical.values()) / n,
        "mismatches": mismatch_rows,
    }
    return metrics, canonical


def report(output_dir: str, auditors: list[str]) -> None:
    """Score completed packets and report cross-author exact agreement."""

    if len(auditors) < 2:
        raise SystemExit("At least two auditors are required for agreement reporting.")
    root = Path(output_dir)
    scored = [_score_auditor(root, auditor) for auditor in auditors]
    metrics = [item[0] for item in scored]
    hashes = {metric.get("scenario_manifest_sha256") for metric in metrics}
    if len(hashes) != 1 or None in hashes:
        raise SystemExit("Auditor packets do not share one recorded scenario freeze.")
    canonical = {metric["auditor"]: rows for metric, rows in scored}
    lines = ["# Schema-v0.5 internal author-audit report", ""]
    for metric in metrics:
        lines.extend(
            [
                f"## {metric['auditor']}",
                "",
                f"- Items: {metric['n']}",
                f"- Pre-gap action accuracy: {metric['pre_action_accuracy']:.1%}",
                f"- Causal-alignment accuracy: {metric['causal_alignment_accuracy']:.1%}",
                f"- Terminal-state accuracy: {metric['terminal_state_accuracy']:.1%}",
                f"- Post-gap action accuracy: {metric['post_action_accuracy']:.1%}",
                f"- Pre-gap answerable: {metric['pre_answerable_rate']:.1%}",
                f"- Post-gap answerable: {metric['post_answerable_rate']:.1%}",
                f"- Items requiring adjudication: {len(metric['mismatches'])}",
                "",
            ]
        )
    lines.extend(["## Cross-author agreement", ""])
    fields = ("pre_action", "causal_alignment", "terminal_state", "post_action")
    for left, right in combinations(auditors, 2):
        shared = set(canonical[left]) & set(canonical[right])
        for field in fields:
            agreement = sum(
                canonical[left][item][field] == canonical[right][item][field]
                for item in shared
            ) / len(shared)
            lines.append(f"- {left} vs {right}, {field}: {agreement:.1%}")
    (root / "internal_audit_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    (root / "internal_audit_metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    adjudication_fields = (
        "auditor",
        "scenario_id",
        "audit_item_id",
        "disputed_fields",
        "pre_answerable",
        "post_answerable",
        "pre_notes",
        "post_notes",
        "adjudicated_resolution",
    )
    with (root / "adjudication.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=adjudication_fields)
        writer.writeheader()
        for metric in metrics:
            for row in metric["mismatches"]:
                writer.writerow(
                    {
                        "auditor": metric["auditor"],
                        **row,
                        "adjudicated_resolution": "",
                    }
                )
    print(f"Readable report -> {root / 'internal_audit_report.md'}")
    print(f"Adjudication sheet -> {root / 'adjudication.csv'}")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "export" and len(sys.argv) >= 6:
        tasks_dir, output_dir = sys.argv[2:4]
        for auditor in sys.argv[4:]:
            export_packet(tasks_dir, output_dir, auditor)
    elif command == "report" and len(sys.argv) >= 5:
        report(sys.argv[2], sys.argv[3:])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
