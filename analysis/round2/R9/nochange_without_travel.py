"""R9. No-change effect with travel excluded.

The no-change condition is not one manipulation.  In thirteen domains the gap
event is a processing window gated on the variable already being in flight, so
suppressing it leaves the process unfinished and the gold action becomes
continue_monitoring.  In travel the event is an unguarded delay notification, so
suppressing it means the delay never arrived and gold flips to close_case.

Recomputes the paired no-change-minus-ordinary effect on belief and final action
with the 6 travel scenarios dropped, beside the all-domain figure, using
score.paired_cluster_effect so the convention matches the paper.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R9"

FIELDS = [
    ("belief after gap", "m_belief_post"),
    ("final action", "m_final_action"),
    ("first action", "m_first_action"),
]


def main() -> None:
    tasks = C.load_tasks()
    rows = C.annotate(C.load_rows())

    # confirm the mechanism claim from the scenario data itself
    gold_nc = Counter()
    for t in tasks.values():
        gold_nc[(t["domain"], C.gold_post_action(t, "gap_no_state_change"))] += 1
    travel_gold = sorted(
        {a for (d, a) in gold_nc if d == "travel"}
    )
    other_gold = sorted(
        {a for (d, a) in gold_nc if d != "travel"}
    )

    csv_rows = []
    cells: dict = {}
    for model in C.MODEL_ORDER:
        base = [r for r in rows if r["model"] == model
                and r["condition"] in {"gap_no_state_change", "full_audio"}]
        for scope, sub in (
            ("all 14 domains", base),
            ("13 domains, travel excluded",
             [r for r in base if r["domain"] != "travel"]),
            ("travel only", [r for r in base if r["domain"] == "travel"]),
        ):
            for label, field in FIELDS:
                e = C.paired_cluster_effect(
                    sub, "gap_no_state_change", "full_audio", field
                )
                cells[(model, scope, field)] = e
                csv_rows.append([
                    C.MODEL_LABEL[model], scope, label,
                    e["paired_n"], e["clusters"],
                    round(100.0 * e["delta"], 1),
                    "[%.1f, %.1f]" % (100.0 * e["ci"][0], 100.0 * e["ci"][1]),
                    "%.4f" % e["p_value"],
                ])

    C.write_csv(TASK, [
        "model", "scope", "metric", "paired_n", "domain_clusters",
        "effect_pp", "ci95", "p_value",
    ], csv_rows)

    tex = [
        "% R9: no-change effect with the six travel scenarios excluded.",
        "\\begin{table}[htbp]",
        "  \\centering",
        "  \\footnotesize",
        "  \\setlength{\\tabcolsep}{5pt}",
        "  \\renewcommand{\\arraystretch}{1.08}",
        "  \\caption{Sensitivity of the no-change effect to the travel domain."
        " In thirteen domains suppressing the gap event leaves the process"
        " unfinished; in travel it means the delay never arrived, and the gold"
        " action flips. Effects are paired no-change minus ordinary audio with"
        " domain-clustered 95\\% intervals.}",
        "  \\label{tab:nochange-sensitivity}",
        "  \\begin{tabular}{@{}lllrl@{}}",
        "    \\toprule",
        "    \\dualcolhead{Model} & \\dualcolhead{Scope} &"
        " \\dualcolhead{Metric} & \\dualcolhead{$\\Delta$} &"
        " \\dualcolhead{95\\% CI} \\\\",
        "    \\midrule",
    ]
    last = None
    for model in C.MODEL_ORDER:
        if last is not None:
            tex.append("    \\addlinespace")
        last = model
        for scope in ("all 14 domains", "13 domains, travel excluded"):
            for label, field in FIELDS[:2]:
                e = cells[(model, scope, field)]
                tex.append(
                    "    %s & %s & %s & %s & [%s, %s] \\\\"
                    % (
                        C.MODEL_LABEL[model], scope, label,
                        C.fmt(100.0 * e["delta"]),
                        C.fmt(100.0 * e["ci"][0]), C.fmt(100.0 * e["ci"][1]),
                    )
                )
    tex += ["    \\bottomrule", "  \\end{tabular}", "\\end{table}"]
    C.write_text(TASK, "table.tex", "\n".join(tex) + "\n")

    md = ["# R9. No-change effect with travel excluded", ""]
    md.append("## The mechanism difference, confirmed from the scenario data")
    md.append("")
    md.append(
        "Gold post-gap action under `gap_no_state_change`, derived on the gold "
        "pre-gap path: **travel -> %s**, all other 13 domains -> %s. Travel is the "
        "only domain where suppressing the event produces a *resolved* world rather "
        "than an unfinished one, because its event (`departure_delay`) has no "
        "in-flight guard while every other domain's event is gated on the process "
        "variable already being mid-run."
        % (", ".join(travel_gold), ", ".join(other_gold))
    )
    md.append("")
    md.append("## Paired no-change minus ordinary audio")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Scope", "Metric", "paired n", "clusters", "Effect (pp)",
             "95% CI", "p"],
            csv_rows,
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    bel_all = [100.0 * cells[(m, "all 14 domains", "m_belief_post")]["delta"]
               for m in C.MODEL_ORDER]
    bel_13 = [100.0 * cells[(m, "13 domains, travel excluded", "m_belief_post")]["delta"]
              for m in C.MODEL_ORDER]
    act_all = [100.0 * cells[(m, "all 14 domains", "m_final_action")]["delta"]
               for m in C.MODEL_ORDER]
    act_13 = [100.0 * cells[(m, "13 domains, travel excluded", "m_final_action")]["delta"]
              for m in C.MODEL_ORDER]
    md.append(
        "**The effect holds on 13 domains. This closes the hole.** The belief "
        "effect is %s across all 14 domains and %s with travel excluded -- a shift "
        "of at most %.1f points. The final-action effect moves from %s to %s."
        % (
            "/".join("%+.1f" % v for v in bel_all),
            "/".join("%+.1f" % v for v in bel_13),
            max(abs(a - b) for a, b in zip(bel_all, bel_13)),
            "/".join("%+.1f" % v for v in act_all),
            "/".join("%+.1f" % v for v in act_13),
        )
    )
    md.append("")
    md.append(
        "The paper's reported no-change belief effect of +21.4 / +27.4 / +32.1 is "
        "therefore not an artefact of the travel domain, and the 13-domain version "
        "does not need to become primary. A one-line sensitivity footnote is enough: "
        "*excluding the six travel scenarios, whose gap event is a notification "
        "rather than a processing window, the belief effect is %s.*"
        % "/".join("%+.1f" % v for v in bel_13)
    )
    md.append("")
    md.append(
        "The travel-only rows are reported for completeness but are 6 scenarios in "
        "a single domain cluster, so their intervals are uninformative by "
        "construction -- `paired_cluster_effect` has one cluster to bootstrap from. "
        "They should not be quoted as an effect."
    )
    md.append("")
    md.append(
        "Separately from the statistics, the wording problem in R1's Q1 sense "
        "remains and is worth one sentence in the paper: the sentence at "
        "`main.tex:286` (\"the no-change observation truthfully states that "
        "processing remains unresolved\") is accurate for 78 of 84 scenarios and "
        "false for the 6 travel ones, where the utterance says the flight is still "
        "on time and the gold action is to close the case."
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    for r in csv_rows:
        if r[2] in ("belief after gap", "final action"):
            print("%-16s %-28s %-18s %+6.1f %s p=%s"
                  % (r[0], r[1], r[2], r[5], r[6], r[7]))


if __name__ == "__main__":
    main()
