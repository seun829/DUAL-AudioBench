"""R1. Is the belief metric inflated the same way the action metric was?

Belief accuracy requires the top choice to be correct for EVERY variable in
belief_schema.  score.py reports chance as 1 / belief_state_space_size = 12.5%
for the usual 4x2 schema.  That is the uniform-random rate, not the rate a
constant guesser achieves.

Two constant-policy baselines are computed, both entirely data-derived:

  domain-conditional majority class
      For each domain, the single best (outcome_value, alignment_value) pair;
      averaged over rows.  This is the score of a policy that knows only which
      domain it is in -- which every model does, since the domain is stated in
      the conversation -- and otherwise always names the same state.  This is
      the primary corrected baseline.

  role-abstracted global constant policy
      A single policy expressed in roles rather than literal values, e.g.
      "always name the misaligned-branch terminal outcome and misaligned".
      Role labels are derived from the data, not assigned by hand: for each
      domain, the misaligned terminal is whatever the gold outcome value is on
      the b0 branch under full_audio, the aligned terminal is the b1 value, and
      the in-progress value is the gold value under gap_no_state_change.

Both are computed against the REALIZED belief targets stored in each
trajectory (state_after_gap restricted to belief_schema), so they are the exact
baselines for the reported accuracies, not an idealisation.  The gold pre-gap
path distribution over the 84 scenarios is reported alongside.
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R1"


def role_map(tasks: dict) -> dict:
    """domain -> {value: role}, derived from the gold path, not hand-assigned."""

    roles: dict = defaultdict(dict)
    for task in tasks.values():
        dom = task["domain"]
        var = C.outcome_variable(task)
        branch = task["causal_design"]["branch"]
        terminal = C.gold_belief_values(task, "full_audio")[var]
        inprog = C.gold_belief_values(task, "gap_no_state_change")[var]
        roles[dom][terminal] = (
            "misaligned_terminal" if branch == "misaligned" else "aligned_terminal"
        )
        roles[dom].setdefault(inprog, "in_progress")
    # any remaining declared value is the not-started role
    for task in tasks.values():
        dom = task["domain"]
        var = C.outcome_variable(task)
        for value in task["belief_schema"][var]:
            roles[dom].setdefault(value, "not_started")
    return roles


def main() -> None:
    tasks = C.load_tasks()
    rows = C.annotate(C.load_rows())
    roles = role_map(tasks)
    groups = C.by_model_condition(rows)

    # ---------------------------------------------------------------
    # 1 + 4: gold-path joint distribution and variable correlation
    # ---------------------------------------------------------------
    gold_joint: dict = {}
    gold_majority: dict = {}
    corr_rows = []
    for cond in C.COND_ORDER:
        joint = Counter()
        by_align = defaultdict(Counter)
        for task in tasks.values():
            var = C.outcome_variable(task)
            vals = C.gold_belief_values(task, cond)
            role = roles[task["domain"]][vals[var]]
            joint[(role, vals["causal_alignment"])] += 1
            by_align[vals["causal_alignment"]][role] += 1
        gold_joint[cond] = joint
        gold_majority[cond] = 100.0 * joint.most_common(1)[0][1] / sum(joint.values())
        # predictability of the outcome role from alignment alone
        correct = sum(c.most_common(1)[0][1] for c in by_align.values())
        total = sum(sum(c.values()) for c in by_align.values())
        corr_rows.append([
            C.COND_LABEL[cond],
            total,
            len(joint),
            round(100.0 * correct / total, 1),
            "; ".join(
                "%s->%s (%d/%d)"
                % (a, c.most_common(1)[0][0], c.most_common(1)[0][1], sum(c.values()))
                for a, c in sorted(by_align.items())
            ),
        ])

    # ---------------------------------------------------------------
    # 2 + 3: realized-target baselines per model x condition
    # ---------------------------------------------------------------
    def targets(row: dict) -> tuple[str, str, str]:
        task = tasks[row["scenario_id"]]
        var = C.outcome_variable(task)
        state = row["state_after_gap"]
        outcome = str(state[var])
        align = str(state["causal_alignment"])
        return outcome, align, roles[task["domain"]][outcome]

    baseline_rows = []
    for (model, cond) in C.populated_cells(rows):
        g = groups[(model, cond)]
        n = len(g)
        # domain-conditional majority class, joint
        per_dom_joint = defaultdict(Counter)
        per_dom_out = defaultdict(Counter)
        per_dom_align = defaultdict(Counter)
        role_joint = Counter()
        role_out = Counter()
        align_only = Counter()
        for row in g:
            dom = row["domain"]
            outcome, align, role = targets(row)
            per_dom_joint[dom][(outcome, align)] += 1
            per_dom_out[dom][outcome] += 1
            per_dom_align[dom][align] += 1
            role_joint[(role, align)] += 1
            role_out[role] += 1
            align_only[align] += 1
        maj_joint = 100.0 * sum(
            c.most_common(1)[0][1] for c in per_dom_joint.values()
        ) / n
        maj_out = 100.0 * sum(
            c.most_common(1)[0][1] for c in per_dom_out.values()
        ) / n
        maj_align = 100.0 * sum(
            c.most_common(1)[0][1] for c in per_dom_align.values()
        ) / n
        role_joint_rate = 100.0 * role_joint.most_common(1)[0][1] / n
        role_out_rate = 100.0 * role_out.most_common(1)[0][1] / n
        align_rate = 100.0 * align_only.most_common(1)[0][1] / n
        # exactly what score.py reports: mean of 1 / belief_state_space_size
        uniform = 100.0 * sum(
            1.0 / row["belief_state_space_size"] for row in g
        ) / n
        observed = C.rate(g, "m_belief_post")
        lo, hi = C.clustered_bootstrap_ci(g, "m_belief_post")
        baseline_rows.append({
            "model": model,
            "condition": cond,
            "n": n,
            "observed": observed,
            "ci_low": 100.0 * lo,
            "ci_high": 100.0 * hi,
            "uniform": uniform,
            "maj_joint": maj_joint,
            "maj_outcome": maj_out,
            "maj_align": maj_align,
            "role_joint": role_joint_rate,
            "role_outcome": role_out_rate,
            "role_align": align_rate,
            "best_joint_guess": role_joint.most_common(1)[0][0],
        })

    # ---------------------------------------------------------------
    # write CSV
    # ---------------------------------------------------------------
    header = [
        "model", "condition", "n",
        "belief_observed", "ci_low", "ci_high",
        "uniform_chance_reported_by_score_py",
        "majority_class_joint_domain_conditional",
        "majority_class_outcome_only", "majority_class_alignment_only",
        "role_abstracted_global_constant_joint",
        "role_abstracted_outcome_only", "role_abstracted_alignment_only",
        "clears_majority_baseline",
        "margin_over_majority",
        "best_single_role_guess",
    ]
    csv_rows = []
    for b in baseline_rows:
        clears = "YES" if b["ci_low"] > b["maj_joint"] else (
            "no" if b["ci_high"] < b["maj_joint"] else "inconclusive"
        )
        csv_rows.append([
            C.MODEL_LABEL[b["model"]], C.COND_LABEL[b["condition"]], b["n"],
            round(b["observed"], 1), round(b["ci_low"], 1), round(b["ci_high"], 1),
            round(b["uniform"], 1),
            round(b["maj_joint"], 1), round(b["maj_outcome"], 1),
            round(b["maj_align"], 1),
            round(b["role_joint"], 1), round(b["role_outcome"], 1),
            round(b["role_align"], 1),
            clears, round(b["observed"] - b["maj_joint"], 1),
            "%s + %s" % b["best_joint_guess"],
        ])
    C.write_csv(TASK, header, csv_rows)

    # ---------------------------------------------------------------
    # LaTeX
    # ---------------------------------------------------------------
    tex = [
        "% R1: belief accuracy against a corrected constant-policy baseline.",
        "% Paste into paper/main.tex. Columns use the \\dualcolhead macro already defined there.",
        "\\begin{table}[htbp]",
        "  \\centering",
        "  \\footnotesize",
        "  \\setlength{\\tabcolsep}{5pt}",
        "  \\renewcommand{\\arraystretch}{1.08}",
        "  \\caption{Post-gap belief accuracy against a corrected baseline. Uniform"
        " chance is $1/|\\mathcal{S}|$ as reported by the scoring code. Majority"
        " class is the best constant state assignment available to a policy that"
        " knows only the domain. Clears is whether the domain-clustered 95\\%"
        " interval lies strictly above the majority-class rate.}",
        "  \\label{tab:belief-baseline}",
        "  \\begin{tabular}{@{}llrrrrl@{}}",
        "    \\toprule",
        "    \\dualcolhead{Model} & \\dualcolhead{Condition} & \\dualcolhead{Belief}"
        " & \\dualcolhead{95\\% CI} & \\dualcolhead{Uniform} &"
        " \\dualcolhead{Majority} & \\dualcolhead{Clears} \\\\",
        "    \\midrule",
    ]
    last_model = None
    for b in baseline_rows:
        if last_model is not None and b["model"] != last_model:
            tex.append("    \\addlinespace")
        last_model = b["model"]
        clears = "YES" if b["ci_low"] > b["maj_joint"] else (
            "no" if b["ci_high"] < b["maj_joint"] else "inconclusive"
        )
        tex.append(
            "    %s & %s & %s & [%s, %s] & %s & %s & %s \\\\"
            % (
                C.MODEL_LABEL[b["model"]], C.COND_LABEL[b["condition"]],
                C.fmt(b["observed"]), C.fmt(b["ci_low"]), C.fmt(b["ci_high"]),
                C.fmt(b["uniform"]), C.fmt(b["maj_joint"]),
                {"YES": "yes", "no": "\\textbf{no}",
                 "inconclusive": "unclear"}[clears],
            )
        )
    tex += ["    \\bottomrule", "  \\end{tabular}", "\\end{table}"]
    C.write_text(TASK, "table.tex", "\n".join(tex) + "\n")

    # ---------------------------------------------------------------
    # README
    # ---------------------------------------------------------------
    fa = {b["condition"]: b for b in baseline_rows
          if b["model"] == "google/gemini-3-flash-preview"}
    maj_fa = fa["full_audio"]["maj_joint"]
    maj_nc = fa["gap_no_state_change"]["maj_joint"]

    md = ["# R1. Is the belief metric inflated the same way the action metric was?", ""]
    md.append("## Answer")
    md.append("")
    ordinary = [b for b in baseline_rows if b["condition"] == "full_audio"]
    nochange = [b for b in baseline_rows if b["condition"] == "gap_no_state_change"]

    def verdict(b: dict) -> str:
        if b["ci_low"] > b["maj_joint"]:
            return "YES"
        if b["ci_high"] < b["maj_joint"]:
            return "no"
        return "inconclusive"

    md.append(
        "**Yes. The suspicion in the work order is correct, and the consequence is "
        "worse than for the action metric: under ordinary audio, not one of the "
        "three models has a post-gap belief accuracy distinguishable from a "
        "constant guess.**"
    )
    md.append("")
    md.append(
        "The two belief variables are perfectly correlated by construction in the "
        "seven ordinary conditions. `causal_alignment` predicts the outcome role "
        "in **%s%% of the 84 scenarios**, and the gold joint state takes only "
        "**%d distinct values**: `misaligned_terminal + misaligned` on 42 "
        "scenarios and `aligned_terminal + aligned` on the other 42. On the gold "
        "pre-gap path a single constant guess is therefore jointly correct on "
        "**exactly half the set (%.1f%%)**. Measured against the realized targets "
        "actually stored in the trajectories it lands at %.1f-%.1f%% across "
        "models, and a policy that also knows the domain reaches **%.1f%%**. "
        "`score.py` reports chance for the same cell as **%.1f%%**."
        % (
            corr_rows[0][3], corr_rows[0][2],
            gold_majority["full_audio"],
            min(b["role_joint"] for b in ordinary),
            max(b["role_joint"] for b in ordinary),
            maj_fa, ordinary[0]["uniform"],
        )
    )
    md.append("")
    clears_ord = [b for b in ordinary if verdict(b) == "YES"]
    fails_ord = [b for b in ordinary if verdict(b) == "no"]
    unclear_ord = [b for b in ordinary if verdict(b) == "inconclusive"]
    md.append(
        "**Ordinary audio: %d of 3 models clear the corrected baseline.** "
        "%s%s%s"
        % (
            len(clears_ord),
            ("Below baseline: " + ", ".join(
                "%s (%.1f vs %.1f, CI upper %.1f)"
                % (C.MODEL_LABEL[b["model"]], b["observed"], b["maj_joint"],
                   b["ci_high"])
                for b in fails_ord) + ". ") if fails_ord else "",
            ("Interval spans the baseline: " + ", ".join(
                "%s (%.1f vs %.1f)"
                % (C.MODEL_LABEL[b["model"]], b["observed"], b["maj_joint"])
                for b in unclear_ord) + ". ") if unclear_ord else "",
            ("Clears: " + ", ".join(
                C.MODEL_LABEL[b["model"]] for b in clears_ord) + ".")
            if clears_ord else "",
        )
    )
    md.append("")
    md.append(
        "**No state change: %d of 3 models clear it** (%s), even though its "
        "baseline is comparable at %.1f%%. This is the asymmetry the paper needs. "
        "The headline belief effect of no-change over ordinary audio is not a "
        "case of both conditions sitting above chance with one higher; it is a "
        "case of only the no-change condition being above chance at all."
        % (
            sum(1 for b in nochange if verdict(b) == "YES"),
            ", ".join(
                "%s %.1f vs %.1f" % (C.MODEL_LABEL[b["model"]], b["observed"],
                                     b["maj_joint"])
                for b in nochange if verdict(b) == "YES"
            ),
            maj_nc,
        )
    )
    md.append("")
    md.append("## Reported belief accuracy against the corrected baseline")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Belief", "95% CI", "Uniform (score.py)",
             "Majority class", "Margin", "Clears?"],
            [
                [
                    C.MODEL_LABEL[b["model"]], C.COND_LABEL[b["condition"]],
                    "%.1f" % b["observed"],
                    "[%.1f, %.1f]" % (b["ci_low"], b["ci_high"]),
                    "%.1f" % b["uniform"], "%.1f" % b["maj_joint"],
                    "%+.1f" % (b["observed"] - b["maj_joint"]),
                    "**YES**" if b["ci_low"] > b["maj_joint"] else
                    ("**no**" if b["ci_high"] < b["maj_joint"] else "inconclusive"),
                ]
                for b in baseline_rows
            ],
        )
    )
    md.append("")
    md.append("## 1. Joint distribution of true post-gap belief values (gold path, n=84)")
    md.append("")
    md.append(
        "Outcome values are shown as data-derived roles so the 14 domains are "
        "comparable: `misaligned_terminal` is whatever the gold outcome value is "
        "on the b0 branch under ordinary audio, `aligned_terminal` the b1 value, "
        "`in_progress` the value under no-state-change."
    )
    md.append("")
    all_keys = sorted({k for j in gold_joint.values() for k in j})
    md.append(
        C.md_table(
            ["Condition"] + ["%s + %s" % k for k in all_keys]
            + ["majority class %"],
            [
                [C.COND_LABEL[c]] + [gold_joint[c].get(k, 0) for k in all_keys]
                + ["%.1f" % gold_majority[c]]
                for c in C.COND_ORDER
            ],
        )
    )
    md.append("")
    md.append("## 2 + 3. Constant-policy baselines (realized targets)")
    md.append("")
    md.append(
        C.md_table(
            ["Model", "Condition", "Majority joint (domain-conditional)",
             "Majority outcome only", "Majority alignment only",
             "Global constant joint", "Best single guess"],
            [
                [
                    C.MODEL_LABEL[b["model"]], C.COND_LABEL[b["condition"]],
                    "%.1f" % b["maj_joint"], "%.1f" % b["maj_outcome"],
                    "%.1f" % b["maj_align"], "%.1f" % b["role_joint"],
                    "%s + %s" % b["best_joint_guess"],
                ]
                for b in baseline_rows
            ],
        )
    )
    md.append("")
    md.append("## 4. Correlation between the two belief variables (gold path)")
    md.append("")
    md.append(
        C.md_table(
            ["Condition", "n", "distinct joint cells",
             "outcome predictable from alignment alone (%)",
             "best outcome per alignment value"],
            corr_rows,
        )
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    md.append(
        "The belief metric and the action metric are inflated by the *same* "
        "structural fact, reached by different routes. The action metric collapses "
        "because `close_case` is gold on both branches for half the set. The "
        "belief metric collapses because the gold joint state takes only two "
        "values across the whole 84, one per branch, in equal numbers. Either way "
        "a constant answer scores about half, and either way the code reports a "
        "uniform figure (%.1f%% for belief, 20%% for action) that is roughly four "
        "times too generous." % ordinary[0]["uniform"]
    )
    md.append("")
    md.append(
        "Two caveats worth carrying into the paper. First, the baselines here are "
        "computed against the *realized* belief targets stored in each trajectory, "
        "which is why the domain-conditional majority sits at %.1f%% rather than "
        "exactly 50%%: when a model picks the wrong pre-gap action the realized "
        "state differs, spreading the targets slightly. Second, the "
        "domain-conditional baseline is the fair one to quote, because every model "
        "is told the domain in the conversation; the role-abstracted figure is the "
        "weaker claim." % (maj_fa,)
    )
    md.append("")
    md.append(
        "`clue_removed` is the one cell where a model is reliably and "
        "substantially *below* a constant guess (GPT Audio Mini 17.3 against "
        "41.7). Ablating the clue does not push models toward the majority state; "
        "it pushes them somewhere worse than guessing."
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("%-16s %-22s %6s %14s %9s %9s %s" % (
        "model", "condition", "belief", "95% CI", "uniform", "majority", "clears"))
    for b in baseline_rows:
        clears = "YES" if b["ci_low"] > b["maj_joint"] else (
            "no" if b["ci_high"] < b["maj_joint"] else "inconclusive")
        print("%-16s %-22s %6.1f [%5.1f,%5.1f] %9.1f %9.1f %s" % (
            C.MODEL_LABEL[b["model"]], C.COND_LABEL[b["condition"]],
            b["observed"], b["ci_low"], b["ci_high"], b["uniform"],
            b["maj_joint"], clears))
    print()
    print("gold-path alignment->outcome predictability:")
    for r in corr_rows:
        print("  %-22s %5.1f%%  cells=%d" % (r[0], r[3], r[2]))


if __name__ == "__main__":
    main()
