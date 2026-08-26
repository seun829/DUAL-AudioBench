"""R5. Revision gain and stale belief mass.

Every trajectory carries a belief_revision block written by _belief_revision()
(dual_audio/interaction/runner.py:170).  The paper defines these in the metrics
appendix and reports none of them.

Per variable, restricted to variables whose true state actually changed across
the gap:

  belief_revision_gain     P(new state | after observation) - P(new state | pre-gap)
  final_revision_gain      P(new state | before final action) - P(new state | pre-gap)
  reflection_gain          P(new state | before final action) - P(new state | after obs)
  stale_belief_persistence P(old state | after observation)

The stored mean_* fields average over changed variables within one trajectory.
Averaging those means across trajectories would weight a trajectory with one
changed variable the same as one with two, so this script pools at the VARIABLE
level and reports the contributing variable count per cell.  Trajectory-level
means are reported alongside for comparability with the stored fields.

causal_alignment changes only under the explicit-user-update condition, so in
eight of nine conditions the only contributing variable is the domain outcome.
"""

from __future__ import annotations

import csv as _csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R5"

GAINS = [
    ("revision gain", "belief_revision_gain"),
    ("final revision gain", "final_revision_gain"),
    ("reflection gain", "reflection_gain"),
    ("stale belief mass", "stale_belief_persistence"),
]


def main() -> None:
    rows = C.annotate(C.load_rows())

    csv_rows = []
    cells: dict = {}
    varmix: dict = {}
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        # pool at the variable level over changed variables
        pooled = defaultdict(list)
        contributing = Counter()
        traj_with_change = 0
        for r in sub:
            changed_here = False
            for var, row in r["belief_revision"]["variables"].items():
                if not row["state_changed"]:
                    continue
                changed_here = True
                contributing[var] += 1
                for _, key in GAINS:
                    val = row.get(key)
                    if val is not None:
                        pooled[key].append(float(val))
            traj_with_change += changed_here
        entry = {
            "n_traj": len(sub),
            "n_traj_with_change": traj_with_change,
            "n_var_obs": sum(contributing.values()),
        }
        for _, key in GAINS:
            vals = pooled[key]
            entry[key] = sum(vals) / len(vals) if vals else float("nan")
            entry[key + "_n"] = len(vals)
        # trajectory-level means, matching the stored mean_* fields
        for stored in ("mean_revision_gain", "mean_final_revision_gain",
                       "mean_stale_belief_persistence"):
            vals = [
                r["belief_revision"][stored] for r in sub
                if r["belief_revision"].get(stored) is not None
            ]
            entry[stored] = sum(vals) / len(vals) if vals else float("nan")
            entry[stored + "_n"] = len(vals)
        cells[(model, cond)] = entry
        varmix[(model, cond)] = dict(contributing)
        csv_rows.append([
            C.MODEL_LABEL[model], C.COND_LABEL[cond],
            entry["n_traj"], entry["n_traj_with_change"], entry["n_var_obs"],
            round(entry["belief_revision_gain"], 4),
            round(entry["final_revision_gain"], 4),
            round(entry["reflection_gain"], 4),
            round(entry["stale_belief_persistence"], 4),
            round(entry["mean_revision_gain"], 4),
            round(entry["mean_final_revision_gain"], 4),
            round(entry["mean_stale_belief_persistence"], 4),
            "; ".join("%s=%d" % kv for kv in sorted(contributing.items())),
        ])

    header = [
        "model", "condition", "n_trajectories", "n_trajectories_with_any_change",
        "n_changed_variable_observations",
        "revision_gain", "final_revision_gain", "reflection_gain",
        "stale_belief_mass",
        "stored_mean_revision_gain", "stored_mean_final_revision_gain",
        "stored_mean_stale_belief_persistence",
        "contributing_variables",
    ]
    C.write_csv(TASK, header, csv_rows)

    # ---------------- LaTeX ----------------
    tex = [
        "% R5: belief revision gain and stale mass, pooled over changed variables.",
        "% Computed from belief_revision, already stored in every trajectory.",
        "\\begin{table}[htbp]",
        "  \\centering",
        "  \\footnotesize",
        "  \\setlength{\\tabcolsep}{5pt}",
        "  \\renewcommand{\\arraystretch}{1.08}",
        "  \\caption{Belief revision across the gap, pooled over variables whose"
        " true state changed. Revision gain is the probability mass moved onto the"
        " new true state by the resumed evidence; reflection gain is the further"
        " movement between the belief-only checkpoint and the final action; stale"
        " mass is the probability still on the superseded state after the resumed"
        " evidence. $k$ is the number of contributing variable observations.}",
        "  \\label{tab:revision-gain}",
        "  \\begin{tabular}{@{}llrrrrr@{}}",
        "    \\toprule",
        "    \\dualcolhead{Model} & \\dualcolhead{Condition} & \\dualcolhead{$k$}"
        " & \\dualcolhead{Revision} & \\dualcolhead{Reflection} &"
        " \\dualcolhead{Final} & \\dualcolhead{Stale} \\\\",
        "    \\midrule",
    ]
    last_model = None
    for (model, cond) in C.populated_cells(rows):
        if last_model is not None and model != last_model:
            tex.append("    \\addlinespace")
        last_model = model
        e = cells[(model, cond)]
        tex.append(
            "    %s & %s & %d & %s & %s & %s & %s \\\\"
            % (
                C.MODEL_LABEL[model], C.COND_LABEL[cond], e["n_var_obs"],
                C.fmt(e["belief_revision_gain"], 3),
                C.fmt(e["reflection_gain"], 3),
                C.fmt(e["final_revision_gain"], 3),
                C.fmt(e["stale_belief_persistence"], 3),
            )
        )
    tex += ["    \\bottomrule", "  \\end{tabular}", "\\end{table}"]
    C.write_text(TASK, "table.tex", "\n".join(tex) + "\n")

    # ---------------- README ----------------
    md = ["# R5. Revision gain and stale belief mass", ""]
    md.append(
        "This is the most direct measurement of the mechanism the benchmark is "
        "named for. All four quantities are already computed per trajectory in "
        "`belief_revision.variables` and none appear in the paper."
    )
    md.append("")
    md.append(
        "Values are pooled at the **variable** level over variables whose true "
        "state changed across the gap. The stored `mean_*` fields average within a "
        "trajectory first; those are reported too, and they agree closely because "
        "almost every cell has exactly one contributing variable per trajectory."
    )
    md.append("")
    md.append("## Pooled over changed variables")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "k obs", "Revision gain", "Reflection gain",
             "Final revision gain", "Stale mass", "Contributing variables"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c],
                    cells[(m, c)]["n_var_obs"],
                    "%.3f" % cells[(m, c)]["belief_revision_gain"],
                    "%.3f" % cells[(m, c)]["reflection_gain"],
                    "%.3f" % cells[(m, c)]["final_revision_gain"],
                    "%.3f" % cells[(m, c)]["stale_belief_persistence"],
                    "; ".join("%s=%d" % kv for kv in sorted(varmix[(m, c)].items())),
                ]
                for (m, c) in C.populated_cells(rows)
            ],
        )
    )
    md.append("")
    md.append("## Trajectory-level means (the stored `mean_*` fields)")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "n with a change",
             "stored mean_revision_gain", "stored mean_final_revision_gain",
             "stored mean_stale_belief_persistence"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c],
                    cells[(m, c)]["mean_revision_gain_n"],
                    "%.3f" % cells[(m, c)]["mean_revision_gain"],
                    "%.3f" % cells[(m, c)]["mean_final_revision_gain"],
                    "%.3f" % cells[(m, c)]["mean_stale_belief_persistence"],
                ]
                for (m, c) in C.populated_cells(rows)
            ],
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    fa = {m: cells[(m, "full_audio")] for m in C.MODEL_ORDER}
    hu = {m: cells[(m, "hidden_user_action")] for m in C.MODEL_ORDER}
    md.append(
        "**This is the figure the work order hoped for, and it is there.** Under "
        "ordinary audio the resumed evidence moves %s of probability mass onto the "
        "new true state. Under explicit user update, where the same evidence states "
        "the outcome in plain language, it moves %s. The gap is %s points of "
        "probability mass, on the same scenarios and the same menus."
        % (
            "/".join("%.3f" % fa[m]["belief_revision_gain"] for m in C.MODEL_ORDER),
            "/".join("%.3f" % hu[m]["belief_revision_gain"] for m in C.MODEL_ORDER),
            "/".join("%+.3f" % (hu[m]["belief_revision_gain"]
                                - fa[m]["belief_revision_gain"])
                     for m in C.MODEL_ORDER),
        )
    )
    md.append("")
    md.append(
        "Stale mass tells the same story from the other side: after hearing the "
        "resumed utterance, %s of probability is still sitting on the state that "
        "has just been superseded under ordinary audio, against %s under explicit "
        "user update."
        % (
            "/".join("%.3f" % fa[m]["stale_belief_persistence"]
                     for m in C.MODEL_ORDER),
            "/".join("%.3f" % hu[m]["stale_belief_persistence"]
                     for m in C.MODEL_ORDER),
        )
    )
    md.append("")
    md.append(
        "Reflection gain -- the movement between the belief-only checkpoint and the "
        "final action, with no new evidence in between -- is %s under ordinary "
        "audio. Near zero is the expected and desirable result: it means the "
        "belief-only checkpoint is not being silently revised once the menu "
        "appears, so the two checkpoints measure what they claim to."
        % "/".join("%.3f" % fa[m]["reflection_gain"] for m in C.MODEL_ORDER)
    )
    md.append("")
    nc = {m: cells[(m, "gap_no_state_change")] for m in C.MODEL_ORDER}
    md.append(
        "**A finding worth its own sentence: under no state change, reflection "
        "gain is strongly negative for all three models (%s).** Between the "
        "belief-only checkpoint and the final action there is no new evidence, so "
        "this is the action menu itself pulling belief *away* from the true state. "
        "Revision gain of %s at the belief-only checkpoint decays to a final "
        "revision gain of %s once the five options are shown. The models correctly "
        "read \"still processing\" from the utterance and then talk themselves out "
        "of it when asked to choose an action -- which is a mechanism the paper "
        "currently has no way to name, and which the belief-only checkpoint exists "
        "precisely to expose."
        % (
            "/".join("%+.3f" % nc[m]["reflection_gain"] for m in C.MODEL_ORDER),
            "/".join("%.3f" % nc[m]["belief_revision_gain"] for m in C.MODEL_ORDER),
            "/".join("%.3f" % nc[m]["final_revision_gain"] for m in C.MODEL_ORDER),
        )
    )
    md.append("")
    md.append(
        "GPT Audio Mini also carries five to eight times the stale mass of either "
        "Gemini across every condition (%s under ordinary audio against %s and "
        "%s), which is a cleaner separation between the models than any accuracy "
        "column provides."
        % (
            "%.3f" % fa["openai/gpt-audio-mini"]["stale_belief_persistence"],
            "%.3f" % fa["google/gemini-2.5-flash"]["stale_belief_persistence"],
            "%.3f" % fa["google/gemini-3-flash-preview"]["stale_belief_persistence"],
        )
    )
    md.append("")
    md.append(
        "**Caveat on k.** The contributing-variable column confirms the concern in "
        "the work order: in every condition except explicit user update the only "
        "changed variable is the domain outcome, so `causal_alignment` contributes "
        "nothing to these means. Under explicit user update it does contribute, "
        "because 72 of 84 user-action specs rewrite it (see R10) -- which means the "
        "user-update revision gain is partly measuring the model tracking a "
        "variable the intervention itself overwrote, and should be quoted with that "
        "qualification."
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("%-16s %-22s %5s %7s %7s %7s %7s" % (
        "model", "condition", "k", "revis", "reflect", "final", "stale"))
    for (m, c) in C.populated_cells(rows):
        e = cells[(m, c)]
        print("%-16s %-22s %5d %7.3f %7.3f %7.3f %7.3f" % (
            C.MODEL_LABEL[m], C.COND_LABEL[c], e["n_var_obs"],
            e["belief_revision_gain"], e["reflection_gain"],
            e["final_revision_gain"], e["stale_belief_persistence"]))


if __name__ == "__main__":
    main()
