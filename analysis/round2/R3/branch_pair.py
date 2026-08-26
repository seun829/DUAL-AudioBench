"""R3. Branch-pair accuracy for all models and all conditions.

A pair is scored correct only if the model got BOTH branches of the same causal
pair right within the same pass.  A constant policy scores exactly 0 on this
metric because the two branches have different gold answers, and uniform random
scores 1/25 = 4% for actions.  It is therefore the one action metric in the
benchmark that was never inflated by the answer skew.

Reported per model, per condition, per pass and pooled, with domain-clustered
95% intervals over the 14 domains.
"""

from __future__ import annotations

import csv as _csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R3"


def pair_rows(rows: list, model: str, cond: str, seed=None) -> list:
    """One synthetic row per (causal pair, seed) with both-branch outcomes."""

    by_key = defaultdict(dict)
    for r in rows:
        if r["model"] != model or r["condition"] != cond:
            continue
        if seed is not None and r["seed"] != seed:
            continue
        by_key[(r["causal_pair_id"], r["seed"])][r["causal_branch"]] = r
    out = []
    for (pid, s), branches in sorted(by_key.items()):
        if set(branches) != {"misaligned", "aligned"}:
            continue
        mis, ali = branches["misaligned"], branches["aligned"]
        out.append({
            "scenario_id": pid,
            "seed": s,
            "domain": mis["domain"],
            "both_action": mis["m_final_action"] and ali["m_final_action"],
            "both_belief": mis["m_belief_post"] and ali["m_belief_post"],
            "both_action_and_belief": (
                mis["m_final_action"] and ali["m_final_action"]
                and mis["m_belief_post"] and ali["m_belief_post"]
            ),
            "both_first_action": mis["m_first_action"] and ali["m_first_action"],
        })
    return out


FIELDS = [
    ("both final actions", "both_action"),
    ("both post-gap beliefs", "both_belief"),
    ("both actions and both beliefs", "both_action_and_belief"),
    ("both first actions", "both_first_action"),
]


def main() -> None:
    rows = C.annotate(C.load_rows())
    seeds = sorted({r["seed"] for r in rows})

    csv_rows = []
    cells: dict = {}
    for (model, cond) in C.populated_cells(rows):
        for scope in [("pooled", None)] + [("seed=%d" % s, s) for s in seeds]:
            label, seed = scope
            pr = pair_rows(rows, model, cond, seed)
            entry = {"n_pairs": len(pr)}
            line = [C.MODEL_LABEL[model], C.COND_LABEL[cond], label, len(pr)]
            for fname, field in FIELDS:
                obs = C.rate(pr, field)
                lo, hi = C.clustered_bootstrap_ci(pr, field)
                entry[field] = (obs, 100.0 * lo, 100.0 * hi)
                line += [round(obs, 1), "[%.1f, %.1f]" % (100.0 * lo, 100.0 * hi)]
            cells[(model, cond, label)] = entry
            csv_rows.append(line)

    header = ["model", "condition", "scope", "n_pairs"]
    for fname, _ in FIELDS:
        header += [fname, fname + " 95% CI"]
    C.write_csv(TASK, header, csv_rows)

    # ---------------- LaTeX ----------------
    tex = [
        "% R3: branch-pair accuracy. A constant policy scores 0 here and uniform",
        "% random scores 4 percent for actions, so this metric was never inflated.",
        "\\begin{table}[htbp]",
        "  \\centering",
        "  \\footnotesize",
        "  \\setlength{\\tabcolsep}{5pt}",
        "  \\renewcommand{\\arraystretch}{1.08}",
        "  \\caption{Branch-pair accuracy (percent of 42 causal pairs, pooled over"
        " both passes). A pair counts only if both branches are correct in the same"
        " pass, so a constant policy scores 0 and uniform random scores 4.0 for"
        " actions. Intervals are domain-clustered over the 14 domains.}",
        "  \\label{tab:branch-pair}",
        "  \\begin{tabular}{@{}llrrrr@{}}",
        "    \\toprule",
        "    \\dualcolhead{Model} & \\dualcolhead{Condition} &"
        " \\dualcolhead{$n$} & \\dualcolhead{Both actions} &"
        " \\dualcolhead{Both beliefs} & \\dualcolhead{Both, both} \\\\",
        "    \\midrule",
    ]
    last_model = None
    for (model, cond) in C.populated_cells(rows):
        if last_model is not None and model != last_model:
            tex.append("    \\addlinespace")
        last_model = model
        e = cells[(model, cond, "pooled")]
        tex.append(
            "    %s & %s & %d & %s & %s & %s \\\\"
            % (
                C.MODEL_LABEL[model], C.COND_LABEL[cond], e["n_pairs"],
                C.fmt(e["both_action"][0]), C.fmt(e["both_belief"][0]),
                C.fmt(e["both_action_and_belief"][0]),
            )
        )
    tex += ["    \\bottomrule", "  \\end{tabular}", "\\end{table}"]
    C.write_text(TASK, "table.tex", "\n".join(tex) + "\n")

    # ---------------- README ----------------
    md = ["# R3. Branch-pair accuracy, all models, all conditions", ""]
    md.append(
        "A pair scores 1 only if the model chose correctly on **both** branches "
        "within the **same pass**. A constant policy scores exactly 0 because the "
        "two branches have different gold answers; uniform random scores "
        "1/25 = 4.0% for actions. This metric was therefore never affected by the "
        "answer skew, which is why it is the natural headline."
    )
    md.append("")
    md.append("## Pooled over both passes (n=84 pair-passes per cell)")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "n", "Both actions", "95% CI", "Both beliefs",
             "95% CI", "Both + both"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c],
                    cells[(m, c, "pooled")]["n_pairs"],
                    "%.1f" % cells[(m, c, "pooled")]["both_action"][0],
                    "[%.1f, %.1f]" % cells[(m, c, "pooled")]["both_action"][1:],
                    "%.1f" % cells[(m, c, "pooled")]["both_belief"][0],
                    "[%.1f, %.1f]" % cells[(m, c, "pooled")]["both_belief"][1:],
                    "%.1f" % cells[(m, c, "pooled")]["both_action_and_belief"][0],
                ]
                for (m, c) in C.populated_cells(rows)
            ],
        )
    )
    md.append("")
    md.append("## Per pass")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Pass", "n", "Both actions", "Both beliefs",
             "Both + both"],
            [
                [
                    C.MODEL_LABEL[m], C.COND_LABEL[c], "seed=%d" % s,
                    cells[(m, c, "seed=%d" % s)]["n_pairs"],
                    "%.1f" % cells[(m, c, "seed=%d" % s)]["both_action"][0],
                    "%.1f" % cells[(m, c, "seed=%d" % s)]["both_belief"][0],
                    "%.1f" % cells[(m, c, "seed=%d" % s)]["both_action_and_belief"][0],
                ]
                for (m, c) in C.populated_cells(rows) for s in seeds
            ],
        )
    )
    md.append("")
    md.append("## Comparison with the paper")
    md.append("")
    md.append(
        "The paper reports pair accuracy only for the two Gemini models on "
        "clue-present and clue-removed: Gemini 2.5 11.9 / 1.2 and Gemini 3 "
        "16.7 / 3.6. Recomputed here:"
    )
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Both actions (recomputed)", "Paper", "Match?"],
            [
                [C.MODEL_LABEL[m], C.COND_LABEL[c],
                 "%.1f" % cells[(m, c, "pooled")]["both_action"][0],
                 "%.1f" % paper,
                 "yes" if abs(cells[(m, c, "pooled")]["both_action"][0] - paper) <= 0.05
                 else "**no**"]
                for m, c, paper in [
                    ("google/gemini-2.5-flash", "full_audio", 11.9),
                    ("google/gemini-2.5-flash", "clue_removed", 1.2),
                    ("google/gemini-3-flash-preview", "full_audio", 16.7),
                    ("google/gemini-3-flash-preview", "clue_removed", 3.6),
                ]
            ],
        )
    )
    md.append("")
    md.append("**GPT Audio Mini, missing from the paper entirely:**")
    md.append("")
    md.append(
        C.md_table(
            ["Condition", "Both actions", "95% CI", "Both beliefs", "Both + both"],
            [
                [
                    C.COND_LABEL[c],
                    "%.1f" % cells[("openai/gpt-audio-mini", c, "pooled")]["both_action"][0],
                    "[%.1f, %.1f]" % cells[("openai/gpt-audio-mini", c, "pooled")]["both_action"][1:],
                    "%.1f" % cells[("openai/gpt-audio-mini", c, "pooled")]["both_belief"][0],
                    "%.1f" % cells[("openai/gpt-audio-mini", c, "pooled")]["both_action_and_belief"][0],
                ]
                for (m, c) in C.populated_cells(rows) if m == "openai/gpt-audio-mini"
            ],
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    fa = {m: cells[(m, "full_audio", "pooled")] for m in C.MODEL_ORDER}
    md.append(
        "Under ordinary audio, both-action pair accuracy is %s against a 4.0%% "
        "uniform baseline and a 0.0%% constant-policy baseline. All three are "
        "above uniform, but the absolute numbers are low: the best model gets "
        "both branches of the same pair right in fewer than one case in five."
        % ", ".join("%s %.1f" % (C.MODEL_LABEL[m], fa[m]["both_action"][0])
                    for m in C.MODEL_ORDER)
    )
    md.append("")
    md.append(
        "Both-belief pair accuracy is much lower still (%s), and the conjunction "
        "of all four correct answers is %s. This is the cleanest statement of the "
        "benchmark's difficulty available anywhere in the data, and unlike the "
        "pooled single-branch numbers it needs no baseline caveat."
        % (
            ", ".join("%.1f" % fa[m]["both_belief"][0] for m in C.MODEL_ORDER),
            ", ".join("%.1f" % fa[m]["both_action_and_belief"][0]
                      for m in C.MODEL_ORDER),
        )
    )
    md.append("")
    md.append(
        "Note that both-belief pair accuracy is the metric R1's baseline problem "
        "does *not* touch: a constant belief guess scores 0 here for the same "
        "reason a constant action does. Where R1 found that no model's single-"
        "branch belief accuracy is distinguishable from a constant guess, the pair "
        "version shows the models are nonetheless doing something better than "
        "constant -- just not much better."
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("%-16s %-22s %6s %6s %6s" % ("model", "condition", "act", "bel", "both"))
    for (m, c) in C.populated_cells(rows):
        e = cells[(m, c, "pooled")]
        print("%-16s %-22s %6.1f %6.1f %6.1f" % (
            C.MODEL_LABEL[m], C.COND_LABEL[c], e["both_action"][0],
            e["both_belief"][0], e["both_action_and_belief"][0]))


if __name__ == "__main__":
    main()
