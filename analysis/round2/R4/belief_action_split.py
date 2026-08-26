"""R4. The four-way belief/action split.

_belief_checkpoint() already writes belief_action_outcome into every trajectory
as one of FULL_SUCCESS, ACTION_SELECTION_FAILURE, LUCKY_ACTION, or
STATE_SYNCHRONIZATION_FAILURE.  The paper describes the split in prose and
reports no numbers from it.

The outcome is only populated where an expected action exists, which is the
pre_gap and pre_final_action checkpoints; the post_observation checkpoint is
belief-only and has no action to compare.

LUCKY_ACTION is the share of trajectories where the action was right on top of a
wrong belief, so it directly quantifies how much reported action accuracy is
unearned.  It is broken out by causal branch, as in R2.
"""

from __future__ import annotations

import csv as _csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R4"

OUTCOMES = [
    "FULL_SUCCESS",
    "ACTION_SELECTION_FAILURE",
    "LUCKY_ACTION",
    "STATE_SYNCHRONIZATION_FAILURE",
]
CHECKPOINTS = [("pre-gap", "pre_gap"), ("final", "pre_final_action")]


def main() -> None:
    rows = C.annotate(C.load_rows())

    # flat helper fields
    for r in rows:
        for label, cp in CHECKPOINTS:
            c = r["belief_checkpoints"][cp]
            r["out_" + cp] = c.get("belief_action_outcome")
            r["abc_" + cp] = c.get("action_belief_consistent")
            r["rcc_" + cp] = c.get("risk_calibration_consistent")
        r["lucky_final"] = r["out_pre_final_action"] == "LUCKY_ACTION"

    csv_rows = []
    cells: dict = {}
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        for label, cp in CHECKPOINTS:
            counts = Counter(r["out_" + cp] for r in sub)
            n = len(sub)
            missing = counts.get(None, 0)
            # consistency rates are over rows where the flag is a real bool
            abc = [r for r in sub if isinstance(r["abc_" + cp], bool)]
            rcc = [r for r in sub if isinstance(r["rcc_" + cp], bool)]
            entry = {
                "n": n,
                "missing": missing,
                "abc": 100.0 * sum(r["abc_" + cp] for r in abc) / len(abc)
                if abc else float("nan"),
                "abc_n": len(abc),
                "rcc": 100.0 * sum(r["rcc_" + cp] for r in rcc) / len(rcc)
                if rcc else float("nan"),
                "rcc_n": len(rcc),
            }
            for o in OUTCOMES:
                entry[o] = 100.0 * counts.get(o, 0) / n
            cells[(model, cond, cp)] = entry
            csv_rows.append(
                [C.MODEL_LABEL[model], C.COND_LABEL[cond], label, n]
                + [round(entry[o], 1) for o in OUTCOMES]
                + [missing, round(entry["abc"], 1), entry["abc_n"],
                   round(entry["rcc"], 1), entry["rcc_n"]]
            )

    header = (
        ["model", "condition", "checkpoint", "n"]
        + [o.lower() for o in OUTCOMES]
        + ["outcome_missing", "action_belief_consistent",
           "action_belief_consistent_n", "risk_calibration_consistent",
           "risk_calibration_consistent_n"]
    )
    C.write_csv(TASK, header, csv_rows)

    # ---------------- LUCKY_ACTION by branch ----------------
    lucky_rows = []
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        line = [C.MODEL_LABEL[model], C.COND_LABEL[cond]]
        for branch in ["misaligned", "aligned", None]:
            b = sub if branch is None else [
                r for r in sub if r["causal_branch"] == branch
            ]
            correct = [r for r in b if r["m_final_action"]]
            lucky = sum(r["lucky_final"] for r in b)
            line += [
                round(100.0 * lucky / len(b), 1),
                round(100.0 * lucky / len(correct), 1) if correct else "",
            ]
        lucky_rows.append(line)
    with (C.outdir(TASK) / "lucky_action_by_branch.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        w = _csv.writer(fh)
        w.writerow([
            "model", "condition",
            "lucky_pct_of_misaligned_rows", "lucky_share_of_correct_misaligned",
            "lucky_pct_of_aligned_rows", "lucky_share_of_correct_aligned",
            "lucky_pct_of_all_rows", "lucky_share_of_all_correct",
        ])
        w.writerows(lucky_rows)

    # ---------------- LaTeX ----------------
    tex = [
        "% R4: the four-way belief/action split at the final checkpoint.",
        "% Computed from belief_action_outcome, already stored in every trajectory.",
        "\\begin{table}[htbp]",
        "  \\centering",
        "  \\footnotesize",
        "  \\setlength{\\tabcolsep}{4pt}",
        "  \\renewcommand{\\arraystretch}{1.08}",
        "  \\caption{Joint belief/action outcomes at the final checkpoint"
        " (percent of 168 trajectories). Lucky action is a correct action on top"
        " of an incorrect state belief, so it measures how much reported action"
        " accuracy is unearned. Consistent is the rate at which the selected"
        " action matches the action implied by the model's own top belief.}",
        "  \\label{tab:belief-action-split}",
        "  \\begin{tabular}{@{}llrrrrr@{}}",
        "    \\toprule",
        "    \\dualcolhead{Model} & \\dualcolhead{Condition} &"
        " \\dualcolhead{Full} & \\dualcolhead{Action fail} &"
        " \\dualcolhead{Lucky} & \\dualcolhead{State fail} &"
        " \\dualcolhead{Consistent} \\\\",
        "    \\midrule",
    ]
    last_model = None
    for (model, cond) in C.populated_cells(rows):
        if last_model is not None and model != last_model:
            tex.append("    \\addlinespace")
        last_model = model
        e = cells[(model, cond, "pre_final_action")]
        tex.append(
            "    %s & %s & %s & %s & %s & %s & %s \\\\"
            % (
                C.MODEL_LABEL[model], C.COND_LABEL[cond],
                C.fmt(e["FULL_SUCCESS"]),
                C.fmt(e["ACTION_SELECTION_FAILURE"]),
                C.fmt(e["LUCKY_ACTION"]),
                C.fmt(e["STATE_SYNCHRONIZATION_FAILURE"]),
                C.fmt(e["abc"]),
            )
        )
    tex += ["    \\bottomrule", "  \\end{tabular}", "\\end{table}"]
    C.write_text(TASK, "table.tex", "\n".join(tex) + "\n")

    # ---------------- README ----------------
    md = ["# R4. The four-way belief/action split", ""]
    md.append(
        "All four categories come straight out of `belief_action_outcome`, which "
        "`_belief_checkpoint()` (`dual_audio/interaction/runner.py:170`) already "
        "writes into every trajectory. Nothing here is newly defined."
    )
    md.append("")
    md.append(
        "- `FULL_SUCCESS` -- belief correct on every variable and action correct\n"
        "- `ACTION_SELECTION_FAILURE` -- belief correct, action wrong\n"
        "- `LUCKY_ACTION` -- belief wrong, action right\n"
        "- `STATE_SYNCHRONIZATION_FAILURE` -- both wrong"
    )
    md.append("")
    md.append("## Final checkpoint")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Full success", "Action fail", "Lucky",
             "State fail", "Action/belief consistent", "Risk calib. consistent"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c],
                    "%.1f" % cells[(m, c, "pre_final_action")]["FULL_SUCCESS"],
                    "%.1f" % cells[(m, c, "pre_final_action")]["ACTION_SELECTION_FAILURE"],
                    "**%.1f**" % cells[(m, c, "pre_final_action")]["LUCKY_ACTION"],
                    "%.1f" % cells[(m, c, "pre_final_action")]["STATE_SYNCHRONIZATION_FAILURE"],
                    "%.1f" % cells[(m, c, "pre_final_action")]["abc"],
                    "%.1f" % cells[(m, c, "pre_final_action")]["rcc"],
                ]
                for (m, c) in C.populated_cells(rows)
            ],
        )
    )
    md.append("")
    md.append("## Pre-gap checkpoint")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Full success", "Action fail", "Lucky",
             "State fail", "Action/belief consistent", "Risk calib. consistent"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c],
                    "%.1f" % cells[(m, c, "pre_gap")]["FULL_SUCCESS"],
                    "%.1f" % cells[(m, c, "pre_gap")]["ACTION_SELECTION_FAILURE"],
                    "%.1f" % cells[(m, c, "pre_gap")]["LUCKY_ACTION"],
                    "%.1f" % cells[(m, c, "pre_gap")]["STATE_SYNCHRONIZATION_FAILURE"],
                    "%.1f" % cells[(m, c, "pre_gap")]["abc"],
                    "%.1f" % cells[(m, c, "pre_gap")]["rcc"],
                ]
                for (m, c) in C.populated_cells(rows)
            ],
        )
    )
    md.append("")
    md.append("## Lucky action by causal branch (final checkpoint)")
    md.append("")
    md.append(
        "`share of correct` is the fraction of the model's *correct* final actions "
        "that rested on a wrong belief. That is the unearned fraction of the "
        "reported action accuracy."
    )
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Misaligned: % rows", "Misaligned: share of correct",
             "Aligned: % rows", "Aligned: share of correct",
             "All: % rows", "All: share of correct"],
            lucky_rows,
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    fa = {m: cells[(m, "full_audio", "pre_final_action")] for m in C.MODEL_ORDER}
    lucky_fa = {r[0]: r for r in lucky_rows if r[1] == "Ordinary audio"}
    md.append(
        "Under ordinary audio the final-checkpoint split is dominated by joint "
        "failure: `STATE_SYNCHRONIZATION_FAILURE` accounts for %s of all "
        "trajectories, against `FULL_SUCCESS` at %s."
        % (
            "/".join("%.1f" % fa[m]["STATE_SYNCHRONIZATION_FAILURE"]
                     for m in C.MODEL_ORDER),
            "/".join("%.1f" % fa[m]["FULL_SUCCESS"] for m in C.MODEL_ORDER),
        )
    )
    md.append("")
    md.append(
        "**Lucky actions are a small share of the total but a large share of the "
        "successes.** Under ordinary audio, %s of every correct final action rests "
        "on an incorrect state belief (Gemini 2.5 / Gemini 3 / GPT Audio Mini). "
        "That is the quantity to quote when the paper says action accuracy "
        "overstates state competence."
        % "/".join(
            str(lucky_fa[C.MODEL_LABEL[m]][7]) + "%" for m in C.MODEL_ORDER
        )
    )
    md.append("")
    md.append(
        "Action/belief consistency -- whether the chosen action matches the action "
        "implied by the model's own top belief -- is %s under ordinary audio. The "
        "gap between that and 100 is the model contradicting its own stated belief, "
        "which is a different failure from getting the belief wrong."
        % "/".join("%.1f" % fa[m]["abc"] for m in C.MODEL_ORDER)
    )
    md.append("")
    md.append(
        "Risk calibration consistency -- whether `needs_revalidation` matches "
        "whether mean confidence actually fell below the scenario threshold -- is "
        "%s. This is the weakest of the derived diagnostics and worth reporting "
        "only as a calibration footnote."
        % "/".join("%.1f" % fa[m]["rcc"] for m in C.MODEL_ORDER)
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("%-16s %-22s %6s %6s %6s %6s %7s" % (
        "model", "condition", "FULL", "ACTF", "LUCKY", "STATEF", "consist"))
    for (m, c) in C.populated_cells(rows):
        e = cells[(m, c, "pre_final_action")]
        print("%-16s %-22s %6.1f %6.1f %6.1f %6.1f %7.1f" % (
            C.MODEL_LABEL[m], C.COND_LABEL[c], e["FULL_SUCCESS"],
            e["ACTION_SELECTION_FAILURE"], e["LUCKY_ACTION"],
            e["STATE_SYNCHRONIZATION_FAILURE"], e["abc"]))
    print()
    print("lucky share of correct actions (all rows):")
    for r in lucky_rows:
        print("  %-16s %-22s %s%%" % (r[0], r[1], r[7]))


if __name__ == "__main__":
    main()
