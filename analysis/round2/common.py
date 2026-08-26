"""Shared loaders and conventions for the round-2 reanalysis.

Statistical helpers are imported from ``score`` rather than reimplemented, so
every interval in analysis/round2 uses exactly the convention already used in
the paper: domain-clustered bootstrap, exact sign-flip test, seed 8128.
"""

from __future__ import annotations

import copy
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import score  # noqa: E402
from dual_audio.core.conditions import CONDITIONS  # noqa: E402
from dual_audio.core.environment import (  # noqa: E402
    correct_action,
    execute_action,
    transition,
)
from dual_audio.interaction.runner import _menu  # noqa: E402
from dual_audio.users.scripted import ScriptedUserSimulator  # noqa: E402

RAW = ROOT / "paper_results" / "v05" / "raw"
SCENARIOS = ROOT / "data" / "scenarios_v05"
OUTROOT = ROOT / "analysis" / "round2"

clustered_bootstrap_ci = score.clustered_bootstrap_ci
paired_cluster_effect = score.paired_cluster_effect

MODEL_ORDER = [
    "google/gemini-2.5-flash",
    "google/gemini-3-flash-preview",
    "openai/gpt-audio-mini",
]
MODEL_LABEL = {
    "google/gemini-2.5-flash": "Gemini 2.5",
    "google/gemini-3-flash-preview": "Gemini 3",
    "openai/gpt-audio-mini": "GPT Audio Mini",
}
# Order and labels as used in paper/main.tex Table 6.
COND_ORDER = [
    "full_audio",
    "gap_no_state_change",
    "state_change_short",
    "clue_removed",
    "transcript_only",
    "neutral_audio",
    "hidden_user_action",
    "prosody_high",
    "prosody_low",
]
COND_LABEL = {
    "full_audio": "Ordinary audio",
    "gap_no_state_change": "No state change",
    "state_change_short": "Short clue",
    "clue_removed": "Clue removed",
    "transcript_only": "Transcript",
    "neutral_audio": "Neutral audio",
    "hidden_user_action": "Explicit user update",
    "prosody_high": "High prosody",
    "prosody_low": "Low prosody",
}
BRANCH_ORDER = ["misaligned", "aligned"]


# --------------------------------------------------------------------------
# trajectory loading
# --------------------------------------------------------------------------
def load_rows(include_errors: bool = False) -> list[dict]:
    """Load every stored v0.5 trajectory, asserting one row per key.

    load_done() in run_eval.py deliberately excludes error rows so a later
    invocation retries them, which means an error row and its successful retry
    both sit in the same shard file.  Duplicates among *successful* rows would
    silently double-count, so those raise; duplicated error keys are expected
    and are returned only when include_errors is set.
    """

    rows: list[dict] = []
    for path in sorted(RAW.rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            row["_source_file"] = path.relative_to(ROOT).as_posix()
            rows.append(row)
    if include_errors:
        return rows
    good = [r for r in rows if not r.get("error")]
    seen: dict = {}
    dupes = []
    for row in good:
        key = (row.get("model"), row["scenario_id"], row["condition"], row["seed"])
        if key in seen:
            dupes.append((key, seen[key], row["_source_file"]))
        seen[key] = row["_source_file"]
    if dupes:
        raise SystemExit(
            "duplicate successful trajectory keys ({} total); first: {}".format(
                len(dupes), dupes[:3]
            )
        )
    return good


def annotate(rows: list[dict]) -> list[dict]:
    """Attach the flat 0/1 metric fields the tasks below group on."""

    for row in rows:
        cps = row["belief_checkpoints"]
        row["m_first_action"] = bool(row["pre_gap_success"])
        row["m_final_action"] = bool(row["post_gap_success"])
        row["m_belief_pre"] = bool(cps["pre_gap"]["evaluation"]["all_correct"])
        row["m_belief_post"] = bool(
            cps["post_observation"]["evaluation"]["all_correct"]
        )
        row["m_belief_final"] = bool(
            cps["pre_final_action"]["evaluation"]["all_correct"]
        )
        row["m_strict"] = bool(row["trajectory_success"])
        row["m_action_trajectory"] = bool(row["action_trajectory_success"])
    return rows


def by_model_condition(rows: list[dict]) -> dict:
    out = defaultdict(list)
    for row in rows:
        out[(row["model"], row["condition"])].append(row)
    return out


def rate(rows: list[dict], field: str) -> float:
    """Percent of rows where field is true; nan for an empty group."""

    if not rows:
        return float("nan")
    return 100.0 * sum(bool(r[field]) for r in rows) / len(rows)


def populated_cells(rows: list[dict]) -> list[tuple[str, str]]:
    """Model/condition cells that actually have data, in paper order."""

    have = {(r["model"], r["condition"]) for r in rows}
    return [
        (m, c) for m in MODEL_ORDER for c in COND_ORDER if (m, c) in have
    ]


# --------------------------------------------------------------------------
# scenario loading and gold-path derivation
# --------------------------------------------------------------------------
def load_tasks() -> dict:
    tasks = {}
    for path in sorted(SCENARIOS.glob("*.json")):
        task = json.loads(path.read_text(encoding="utf-8"))
        task["_filename"] = path.name
        tasks[task["scenario_id"]] = task
    return tasks


def gold_path_state(task: dict, condition_name: str) -> dict:
    """Realized post-gap state on the gold pre-gap action path.

    Mirrors ClosedLoopRunner.execute: execute the correct pre-gap action, then
    advance time with the condition's event / user-action selection.
    """

    condition = CONDITIONS[condition_name]
    state = execute_action(
        task["domain"],
        copy.deepcopy(task["initial_state"]),
        task["pre_gap"]["correct_action"],
    )
    return transition(
        domain=task["domain"],
        current_state=state,
        agent_action=task["pre_gap"]["correct_action"],
        elapsed_minutes=task["transition"]["elapsed_minutes"],
        external_event=(
            task["transition"]["external_event"]
            if condition.apply_external_event
            else None
        ),
        user_action=(
            task["transition"].get("user_action")
            if condition.apply_user_action
            else None
        ),
    )


def gold_post_action(task: dict, condition_name: str) -> str:
    return correct_action(task["domain"], gold_path_state(task, condition_name))


def gold_belief_values(task: dict, condition_name: str) -> dict:
    state = gold_path_state(task, condition_name)
    return {var: str(state[var]) for var in task["belief_schema"]}


def post_gap_text(task: dict, condition_name: str) -> str:
    return ScriptedUserSimulator().post_gap(
        task, gold_path_state(task, condition_name), CONDITIONS[condition_name]
    )


def outcome_variable(task: dict) -> str:
    """The domain outcome variable, i.e. the belief variable that is not
    causal_alignment."""

    for var in task["belief_schema"]:
        if var != "causal_alignment":
            return var
    raise KeyError(task["scenario_id"])


def label_to_action(task: dict, stage: str, seed: int) -> dict:
    """Recover the label -> internal action mapping by description join.

    Deliberately avoids relying on the shuffle: the description is the join
    key, so the result does not depend on CPython's RNG staying stable (R8).
    """

    by_desc = {a["description"]: a["action"] for a in task[stage + "_actions"]}
    menu, _ = _menu(task, stage, seed)
    return {item["label"]: by_desc[item["description"]] for item in menu}


def stored_label_to_action(task: dict, stage: str, stored_menu: list) -> dict:
    """Same mapping, taken from the menu exactly as logged in the trajectory."""

    by_desc = {a["description"]: a["action"] for a in task[stage + "_actions"]}
    return {item["label"]: by_desc[item["description"]] for item in stored_menu}


# --------------------------------------------------------------------------
# output helpers
# --------------------------------------------------------------------------
def outdir(task_id: str) -> Path:
    d = OUTROOT / task_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_csv(task_id: str, header: list, rows: list) -> Path:
    path = outdir(task_id) / "results.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    return path


def write_text(task_id: str, name: str, text: str) -> Path:
    path = outdir(task_id) / name
    path.write_text(text, encoding="utf-8")
    return path


def fmt(value, nd: int = 1, dash: str = "--") -> str:
    """Format a float for a table cell; nan becomes a LaTeX-safe dash."""

    if value is None:
        return dash
    try:
        if value != value:  # nan
            return dash
    except TypeError:
        return dash
    return "{:.{}f}".format(value, nd)


def md_table(header: list, rows: list) -> str:
    out = [
        "| " + " | ".join(str(h) for h in header) + " |",
        "|" + "|".join("---" for _ in header) + "|",
    ]
    for r in rows:
        out.append(
            "| " + " | ".join("" if c is None else str(c) for c in r) + " |"
        )
    return "\n".join(out)
