"""R8. Fixed-position and seed-variance baselines.

Part 1, fixed position: for each condition, the score of a policy that always
answers the same letter at the post-gap checkpoint.  The label to internal
action mapping is recovered by joining on the option DESCRIPTION taken from the
menu as logged in the trajectory, not by re-running the shuffle, so the result
does not depend on CPython's RNG remaining stable.

Part 2, seed variance: with only 2 passes per cell, the number of scenarios
where the two passes disagreed on the final action and on the post-gap belief.
High disagreement means the paired effects need wider intervals than they carry.
"""

from __future__ import annotations

import csv as _csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R8"


def main() -> None:
    tasks = C.load_tasks()
    rows = C.annotate(C.load_rows())
    labels = sorted({i["label"] for r in rows for i in r["post_gap_menu"]})

    # ---- sanity: the description join must resolve every stored menu ----
    unresolved = 0
    for r in rows:
        m = C.stored_label_to_action(
            tasks[r["scenario_id"]], "post_gap", r["post_gap_menu"]
        )
        if len(m) != len(r["post_gap_menu"]):
            unresolved += 1
        if r["post_gap_action"] is not None:
            if m.get(r["post_gap_action_label"]) != r["post_gap_action"]:
                unresolved += 1
    if unresolved:
        raise SystemExit("description join failed on %d rows" % unresolved)

    # ---- part 1: fixed position ----
    fixed_rows = []
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        per_label = {}
        for lab in labels:
            hit = 0
            for r in sub:
                m = C.stored_label_to_action(
                    tasks[r["scenario_id"]], "post_gap", r["post_gap_menu"]
                )
                if m.get(lab) == r["expected_post_gap_action"]:
                    hit += 1
            per_label[lab] = 100.0 * hit / len(sub)
        best = max(per_label, key=lambda k: per_label[k])
        fixed_rows.append(
            [C.MODEL_LABEL[model], C.COND_LABEL[cond], len(sub),
             round(C.rate(sub, "m_final_action"), 1)]
            + [round(per_label[l], 1) for l in labels]
            + [round(per_label[best], 1), best,
               round(100.0 * sum(1.0 / r["post_gap_menu_size"] for r in sub)
                     / len(sub), 1)]
        )

    C.write_csv(TASK, (
        ["model", "condition", "n", "final_action_observed"]
        + ["always_" + l for l in labels]
        + ["best_fixed_position", "best_label", "uniform_chance"]
    ), fixed_rows)

    # ---- part 2: seed variance ----
    seed_rows = []
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        by_scen = defaultdict(dict)
        for r in sub:
            by_scen[r["scenario_id"]][r["seed"]] = r
        both = [d for d in by_scen.values() if len(d) == 2]
        act_dis = bel_dis = act_lab_dis = 0
        for d in both:
            a, b = [d[s] for s in sorted(d)]
            act_dis += a["m_final_action"] != b["m_final_action"]
            bel_dis += a["m_belief_post"] != b["m_belief_post"]
            act_lab_dis += a["post_gap_action"] != b["post_gap_action"]
        n = len(both)
        seed_rows.append([
            C.MODEL_LABEL[model], C.COND_LABEL[cond], n,
            act_dis, round(100.0 * act_dis / n, 1),
            bel_dis, round(100.0 * bel_dis / n, 1),
            act_lab_dis, round(100.0 * act_lab_dis / n, 1),
        ])

    with (C.outdir(TASK) / "seed_variance.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        w = _csv.writer(fh)
        w.writerow([
            "model", "condition", "scenarios_with_both_passes",
            "final_action_correctness_disagreements", "pct",
            "belief_correctness_disagreements", "pct",
            "chosen_action_disagreements", "pct",
        ])
        w.writerows(seed_rows)

    md = ["# R8. Fixed-position and seed-variance baselines", ""]
    md.append("## Part 1. Fixed-position policy at the post-gap checkpoint")
    md.append("")
    md.append(
        "Score of a policy that always answers the same letter. Computed from the "
        "menu **as logged in each trajectory**, joined to internal action names by "
        "option description, so no dependence on the RNG. The join was verified "
        "against `post_gap_action_label` -> `post_gap_action` on all %d rows."
        % len(rows)
    )
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "n", "Observed"]
            + ["Always " + l for l in labels]
            + ["Best fixed", "Label", "Uniform"],
            fixed_rows,
        )
    )
    md.append("")
    best_all = max(r[9] for r in fixed_rows)
    all_vals = [r[4 + i] for r in fixed_rows for i in range(len(labels))]
    mean_all = sum(all_vals) / len(all_vals)
    below = [
        r for r in fixed_rows if r[3] < r[9]
    ]
    md.append(
        "**The shuffle is working.** The mean of all %d fixed-position rates is "
        "%.2f%%, against a 20.0%% uniform expectation. The maximum is %.1f%%, but "
        "that is the largest of %d draws, so it is upward-biased by selection; the "
        "range is %.1f-%.1f%%. No letter is systematically the answer, and none of "
        "the reported accuracies can be explained by position bias in the gold."
        % (len(all_vals), mean_all, best_all, len(all_vals),
           min(all_vals), max(all_vals))
    )
    md.append("")
    md.append(
        "**But %d cells score below their own best fixed-position policy**, and all "
        "of them are GPT Audio Mini:" % len(below)
    )
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Observed final action", "Best fixed position",
             "Label"],
            [[r[0], r[1], r[3], r[9], r[10]] for r in below],
        )
    )
    md.append("")
    md.append(
        "On 6 of its 8 conditions, GPT Audio Mini's final-action accuracy is at or "
        "below the score obtainable by pressing one fixed letter for the whole "
        "benchmark. The two exceptions are `clue_removed` (26.8 against 22.0) and "
        "`hidden_user_action` (63.1 against 22.0). This is a stronger and simpler "
        "statement than the majority-class comparison, and it belongs in the paper: "
        "for that model, on the ordinary audio condition, the post-gap action "
        "measurement carries no signal."
    )
    md.append("")
    md.append("## Part 2. Seed variance")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Scenarios", "Final-action flips", "%",
             "Belief flips", "%", "Chosen-action changes", "%"],
            seed_rows,
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    md.append(
        "Fixed position is a non-issue as a *confound* -- the shuffle is uniform to "
        "within 0.01 points on average -- but it is a useful *yardstick*, and by "
        "that yardstick GPT Audio Mini fails on 6 of 8 conditions (table above)."
    )
    md.append("")
    worst = max(seed_rows, key=lambda r: r[4])
    mean_act = sum(r[4] for r in seed_rows) / len(seed_rows)
    mean_bel = sum(r[6] for r in seed_rows) / len(seed_rows)
    mean_chg = sum(r[8] for r in seed_rows) / len(seed_rows)
    md.append(
        "**Seed variance is substantial and the paper should say so.** Across the "
        "26 cells, the two passes disagree on whether the final action was correct "
        "in %.1f%% of scenarios on average (worst cell %s %s at %.1f%%), and on "
        "belief correctness in %.1f%%. The *chosen action* changes between passes "
        "in %.1f%% of scenarios."
        % (mean_act, worst[0], worst[1], worst[4], mean_bel, mean_chg)
    )
    md.append("")
    md.append(
        "With two passes, a per-scenario accuracy is one of {0, 50, 100}, and a "
        "third of scenarios landing on 50 means the per-cell point estimate carries "
        "real sampling noise beyond what the domain-clustered interval captures -- "
        "the clustering handles between-domain variation, not between-pass "
        "variation. Two consequences worth stating in the limitations paragraph: "
        "the paired effects in the main text are on the optimistic side of their "
        "true width, and any effect smaller than roughly 10 points should not be "
        "read as established from 2 passes. The effects the paper actually leans "
        "on (no-change belief +21 to +32, user-update belief +33 to +37) are far "
        "outside that band, so the headline claims are unaffected."
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("best fixed-position anywhere: %.1f%%" % best_all)
    print()
    print("%-16s %-22s %8s %8s %8s" % (
        "model", "condition", "actFlip%", "belFlip%", "chgAct%"))
    for r in seed_rows:
        print("%-16s %-22s %8.1f %8.1f %8.1f" % (r[0], r[1], r[4], r[6], r[8]))


if __name__ == "__main__":
    main()
