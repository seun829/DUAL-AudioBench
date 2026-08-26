"""R6. Per-variable belief accuracy and the joint confusion.

Belief accuracy in the paper is the all-variables conjunction.  This splits it
into the domain outcome variable and causal_alignment, taken from
belief_checkpoints.<cp>.evaluation.variables.<var>.correct, and reports the
2x2 joint confusion:

  both correct      the reported all_correct
  alignment only    knew which branch it was in, could not apply the rule
  outcome only      named the right outcome without resolving the branch
  neither           no state information recovered
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R6"
CHECKPOINTS = [
    ("pre-gap", "pre_gap"),
    ("after gap", "post_observation"),
    ("final", "pre_final_action"),
]


def main() -> None:
    tasks = C.load_tasks()
    rows = C.annotate(C.load_rows())

    for r in rows:
        var = C.outcome_variable(tasks[r["scenario_id"]])
        r["_outcome_var"] = var
        for _, cp in CHECKPOINTS:
            v = r["belief_checkpoints"][cp]["evaluation"]["variables"]
            r["out_ok_" + cp] = bool(v.get(var, {}).get("correct"))
            r["align_ok_" + cp] = bool(v.get("causal_alignment", {}).get("correct"))

    csv_rows = []
    cells: dict = {}
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        for label, cp in CHECKPOINTS:
            n = len(sub)
            conf = Counter(
                (r["out_ok_" + cp], r["align_ok_" + cp]) for r in sub
            )
            entry = {
                "n": n,
                "outcome": 100.0 * C.rate(sub, "out_ok_" + cp) / 100.0 * 100.0,
                "align": C.rate(sub, "align_ok_" + cp),
                "both": 100.0 * conf[(True, True)] / n,
                "align_only": 100.0 * conf[(False, True)] / n,
                "outcome_only": 100.0 * conf[(True, False)] / n,
                "neither": 100.0 * conf[(False, False)] / n,
            }
            entry["outcome"] = C.rate(sub, "out_ok_" + cp)
            # of the failures of the conjunction, which variable was missed
            fails = n - conf[(True, True)]
            entry["fail_align_missed"] = (
                100.0 * (conf[(True, False)] + conf[(False, False)]) / fails
                if fails else float("nan")
            )
            entry["fail_outcome_missed"] = (
                100.0 * (conf[(False, True)] + conf[(False, False)]) / fails
                if fails else float("nan")
            )
            cells[(model, cond, cp)] = entry
            csv_rows.append([
                C.MODEL_LABEL[model], C.COND_LABEL[cond], label, n,
                round(entry["outcome"], 1), round(entry["align"], 1),
                round(entry["both"], 1), round(entry["align_only"], 1),
                round(entry["outcome_only"], 1), round(entry["neither"], 1),
                round(entry["fail_align_missed"], 1),
                round(entry["fail_outcome_missed"], 1),
            ])

    C.write_csv(TASK, [
        "model", "condition", "checkpoint", "n",
        "outcome_variable_correct", "causal_alignment_correct",
        "both_correct", "alignment_only", "outcome_only", "neither",
        "of_failures_pct_missing_alignment", "of_failures_pct_missing_outcome",
    ], csv_rows)

    md = ["# R6. Per-variable belief accuracy", ""]
    md.append(
        "`outcome variable` is the domain state variable (`dispute_status`, "
        "`firmware_status`, `connection_status`, ...); `causal_alignment` is the "
        "two-valued branch variable. `both correct` is exactly the `all_correct` "
        "figure the paper reports as belief accuracy."
    )
    md.append("")
    md.append("## After the gap (the checkpoint the paper reports)")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Outcome var", "Alignment", "Both (= reported)",
             "Alignment only", "Outcome only", "Neither"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c],
                    "%.1f" % cells[(m, c, "post_observation")]["outcome"],
                    "%.1f" % cells[(m, c, "post_observation")]["align"],
                    "**%.1f**" % cells[(m, c, "post_observation")]["both"],
                    "%.1f" % cells[(m, c, "post_observation")]["align_only"],
                    "%.1f" % cells[(m, c, "post_observation")]["outcome_only"],
                    "%.1f" % cells[(m, c, "post_observation")]["neither"],
                ]
                for (m, c) in C.populated_cells(rows)
            ],
        )
    )
    md.append("")
    md.append("## Which variable is missed, as a share of conjunction failures")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "% of failures missing alignment",
             "% of failures missing outcome"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c],
                    "%.1f" % cells[(m, c, "post_observation")]["fail_align_missed"],
                    "%.1f" % cells[(m, c, "post_observation")]["fail_outcome_missed"],
                ]
                for (m, c) in C.populated_cells(rows)
            ],
        )
    )
    md.append("")
    md.append("## All three checkpoints")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Checkpoint", "n", "Outcome", "Alignment",
             "Both", "Align only", "Outcome only", "Neither",
             "fail: missed align", "fail: missed outcome"],
            csv_rows,
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    fa = {m: cells[(m, "full_audio", "post_observation")] for m in C.MODEL_ORDER}
    md.append(
        "Under ordinary audio, `causal_alignment` is recovered far more reliably "
        "than the outcome: %s against %s. The dominant failure is therefore "
        "**alignment right, outcome wrong** (%s of all trajectories), which means "
        "the models generally do resolve which branch they are in and then fail to "
        "apply the completion rule to it."
        % (
            "/".join("%.1f" % fa[m]["align"] for m in C.MODEL_ORDER),
            "/".join("%.1f" % fa[m]["outcome"] for m in C.MODEL_ORDER),
            "/".join("%.1f" % fa[m]["align_only"] for m in C.MODEL_ORDER),
        )
    )
    md.append("")
    md.append(
        "That is a more specific diagnosis than the paper currently offers, and it "
        "matters for the framing: the bottleneck under ordinary audio is not clue "
        "retrieval, it is rule application to a retrieved clue. The clue-removed "
        "condition confirms the split from the other side -- alignment accuracy "
        "falls to %s there, and with it the outcome."
        % "/".join(
            "%.1f" % cells[(m, "clue_removed", "post_observation")]["align"]
            for m in C.MODEL_ORDER
        )
    )
    md.append("")
    md.append(
        "`outcome only` -- naming the right outcome without resolving the branch -- "
        "is rare (%s), as it should be: on this design the outcome is not "
        "guessable independently of the branch."
        % "/".join("%.1f" % fa[m]["outcome_only"] for m in C.MODEL_ORDER)
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("%-16s %-22s %7s %7s %7s %7s %7s %7s" % (
        "model", "condition", "outcome", "align", "both", "alignOnly",
        "outOnly", "neither"))
    for (m, c) in C.populated_cells(rows):
        e = cells[(m, c, "post_observation")]
        print("%-16s %-22s %7.1f %7.1f %7.1f %7.1f %7.1f %7.1f" % (
            C.MODEL_LABEL[m], C.COND_LABEL[c], e["outcome"], e["align"],
            e["both"], e["align_only"], e["outcome_only"], e["neither"]))


if __name__ == "__main__":
    main()
