"""R7. Is the first action inflated too?

Gives the gold pre_gap.correct_action distribution over the 84 scenarios, its
majority-class rate (domain-conditional and global), and the best fixed-position
rate, so the reported 65.5-80.4% first-action accuracies can be read against the
right baseline.
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R7"


def main() -> None:
    tasks = C.load_tasks()
    rows = C.annotate(C.load_rows())

    # ---- gold distribution over the 84 scenarios ----
    gold = Counter(t["pre_gap"]["correct_action"] for t in tasks.values())
    per_dom = defaultdict(Counter)
    for t in tasks.values():
        per_dom[t["domain"]][t["pre_gap"]["correct_action"]] += 1
    n = len(tasks)
    global_major = 100.0 * gold.most_common(1)[0][1] / n
    dom_major = 100.0 * sum(
        c.most_common(1)[0][1] for c in per_dom.values()
    ) / n

    # ---- fixed-position rates, from the stored menus ----
    labels = sorted({i["label"] for r in rows for i in r["pre_gap_menu"]})
    fixed: dict = {}
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        per_label = {}
        for lab in labels:
            hit = 0
            for r in sub:
                task = tasks[r["scenario_id"]]
                mapping = C.stored_label_to_action(task, "pre_gap", r["pre_gap_menu"])
                if mapping.get(lab) == r["expected_pre_gap_action"]:
                    hit += 1
            per_label[lab] = 100.0 * hit / len(sub)
        fixed[(model, cond)] = per_label

    csv_rows = []
    for (model, cond) in C.populated_cells(rows):
        sub = [r for r in rows if r["model"] == model and r["condition"] == cond]
        obs = C.rate(sub, "m_first_action")
        lo, hi = C.clustered_bootstrap_ci(sub, "m_first_action")
        # realized gold distribution for this cell
        rc = Counter(r["expected_pre_gap_action"] for r in sub)
        rd = defaultdict(Counter)
        for r in sub:
            rd[r["domain"]][r["expected_pre_gap_action"]] += 1
        best_fixed = max(fixed[(model, cond)].values())
        best_lab = max(fixed[(model, cond)], key=lambda k: fixed[(model, cond)][k])
        csv_rows.append([
            C.MODEL_LABEL[model], C.COND_LABEL[cond], len(sub),
            round(obs, 1), "[%.1f, %.1f]" % (100.0 * lo, 100.0 * hi),
            round(100.0 * sum(1.0 / r["pre_gap_menu_size"] for r in sub) / len(sub), 1),
            round(100.0 * rc.most_common(1)[0][1] / len(sub), 1),
            rc.most_common(1)[0][0],
            round(100.0 * sum(c.most_common(1)[0][1] for c in rd.values()) / len(sub), 1),
            round(best_fixed, 1), best_lab,
            "YES" if 100.0 * lo > 100.0 * rc.most_common(1)[0][1] / len(sub)
            else "no",
        ])

    C.write_csv(TASK, [
        "model", "condition", "n", "first_action_observed", "ci95",
        "uniform_chance", "global_majority_class", "global_majority_action",
        "domain_conditional_majority_class", "best_fixed_position",
        "best_fixed_position_label", "clears_domain_majority",
    ], csv_rows)

    md = ["# R7. Is the first action inflated too?", ""]
    md.append("## Gold `pre_gap.correct_action` distribution over the 84 scenarios")
    md.append("")
    md.append(
        C.md_table(
            ["Gold first action", "n", "share"],
            [[a, c, "%.1f%%" % (100.0 * c / n)] for a, c in gold.most_common()],
        )
    )
    md.append("")
    md.append(
        "Global majority class: **%.1f%%** (`%s`). Domain-conditional majority "
        "class: **%.1f%%**. Uniform chance: 20.0%%."
        % (global_major, gold.most_common(1)[0][0], dom_major)
    )
    md.append("")
    md.append("## Reported first-action accuracy against those baselines")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "First action", "95% CI", "Uniform",
             "Global majority", "Domain majority", "Best fixed position",
             "Clears domain majority?"],
            [[r[0], r[1], r[3], r[4], r[5], r[6], r[8], "%s (%s)" % (r[9], r[10]),
              "**%s**" % r[11] if r[11] == "no" else r[11]] for r in csv_rows],
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    md.append(
        "**The first action is not inflated the way the final action is, but it is "
        "not a state-tracking measurement either.** Two facts, pulling in opposite "
        "directions:"
    )
    md.append("")
    md.append(
        "1. The gold pre-gap action is maximally spread across the benchmark: %d "
        "distinct actions over 84 scenarios, 6 each, so the **global** majority "
        "class is only %.1f%%. Best fixed-position is %.1f%%, close to the 20%% "
        "uniform rate, confirming the pre-gap shuffle works. Against either of "
        "those baselines the reported 55.4-84.5%% is a real result."
        % (len(gold), global_major, max(fixed[k][l] for k in fixed for l in fixed[k]))
    )
    md.append("")
    md.append(
        "2. The **domain-conditional** majority class is **%.1f%%**, and that is "
        "not a rounding artefact: within each of the 14 domains, all 6 scenarios "
        "share the same gold opening move. A policy that recognises the domain and "
        "recalls one action per domain scores a perfect 100 without listening to "
        "the conversation at all. So the domain-conditional column is degenerate "
        "here and no model can \"clear\" it -- the useful reading is the reverse: "
        "models score 55-85%% on a task that is answerable from the domain name "
        "alone."
        % dom_major
    )
    md.append("")
    md.append(
        "**What this means for the paper.** The sentence that first-action accuracy "
        "shows the benchmark is not uniformly hard **survives**, and needs the "
        "global-majority footnote (%.1f%%, not 20%%). But any sentence implying the "
        "first action demonstrates competence at *state tracking* should be cut: "
        "the pre-gap checkpoint precedes the gap, has a single correct answer per "
        "domain, and is best described as a domain-appropriate-action check that "
        "establishes the models can operate the menu at all. That is exactly the "
        "role the paper's own \"act correctly before the gap and fail afterward\" "
        "framing needs it to play, so this is a clarification rather than a "
        "correction."
        % global_major
    )
    md.append("")
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("gold pre-gap action distribution over 84 scenarios:")
    for a, c in gold.most_common():
        print("   %-34s %3d  %5.1f%%" % (a, c, 100.0 * c / n))
    print("global majority %.1f%%   domain-conditional majority %.1f%%"
          % (global_major, dom_major))
    print()
    for r in csv_rows:
        print("%-16s %-22s obs=%5.1f dom_major=%5.1f fixed=%5.1f clears=%s"
              % (r[0], r[1], r[3], r[8], r[9], r[11]))


if __name__ == "__main__":
    main()
