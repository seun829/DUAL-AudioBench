"""R10. Count the causal_alignment rewrites in the gap user actions.

72 of 84 user-action specs are declarative with an effects list.  If those
effects target causal_alignment, the explicit-user-update condition overwrites
the very variable the clue exists to determine, so that condition stops being a
test of clue use.

Counts, by domain, how many of the 84 transition.user_action specs include an
effect targeting causal_alignment, and cross-checks against the realized
post-gap state actually stored in the trajectories.
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "R10"


def main() -> None:
    tasks = C.load_tasks()
    rows = C.annotate(C.load_rows())

    per_dom = defaultdict(lambda: {"n": 0, "declarative": 0, "rewrites": 0,
                                   "targets": Counter(), "actions": set()})
    detail = []
    for sid in sorted(tasks):
        t = tasks[sid]
        ua = t["transition"].get("user_action") or {}
        effects = ua.get("effects")
        d = per_dom[t["domain"]]
        d["n"] += 1
        d["actions"].add(ua.get("action"))
        targets = [e.get("target") for e in (effects or [])]
        rewrites = "causal_alignment" in targets
        if effects:
            d["declarative"] += 1
            for tg in targets:
                d["targets"][tg] += 1
        if rewrites:
            d["rewrites"] += 1
        detail.append([
            sid, t["domain"], t["causal_design"]["branch"],
            ua.get("action"),
            "declarative" if effects else "domain-coded",
            "YES" if rewrites else "no",
            "; ".join(
                "%s<-%s" % (e.get("target"),
                            e.get("value", "copy:" + str(e.get("copy_from"))))
                for e in (effects or [])
            ) or "-",
        ])

    C.write_csv(TASK, [
        "scenario_id", "domain", "branch", "user_action", "spec_style",
        "rewrites_causal_alignment", "effects",
    ], detail)

    total_rewrites = sum(d["rewrites"] for d in per_dom.values())
    total_decl = sum(d["declarative"] for d in per_dom.values())

    # cross-check against realized state under hidden_user_action
    flip = Counter()
    for r in rows:
        if r["condition"] != "hidden_user_action":
            continue
        init = r["initial_state"].get("causal_alignment")
        after = r["state_after_gap"].get("causal_alignment")
        flip[(r["domain"], init != after)] += 1
    flipped_domains = sorted({d for (d, f) in flip if f})

    dom_rows = [
        [
            dom, d["n"], d["declarative"], d["rewrites"],
            "%.0f%%" % (100.0 * d["rewrites"] / d["n"]),
            "; ".join(sorted(a for a in d["actions"] if a)),
            "; ".join("%s=%d" % kv for kv in sorted(d["targets"].items())),
        ]
        for dom, d in sorted(per_dom.items())
    ]

    md = ["# R10. `causal_alignment` rewrites in the gap user actions", ""]
    md.append("## Answer")
    md.append("")
    md.append(
        "**%d of 84** user-action specs include an effect targeting "
        "`causal_alignment` (%d of the %d declarative specs; the %d domain-coded "
        "specs have no effects list and rewrite nothing declaratively). "
        "That is **%.0f%% of the benchmark**."
        % (total_rewrites, total_rewrites, total_decl, 84 - total_decl,
           100.0 * total_rewrites / 84)
    )
    md.append("")
    md.append("## By domain")
    md.append("")
    md.append(
        C.md_table(
            ["Domain", "n", "declarative specs", "rewrites alignment", "share",
             "user action(s)", "effect targets"],
            dom_rows,
        )
    )
    md.append("")
    md.append("## Cross-check against the realized state")
    md.append("")
    md.append(
        "Independently of the spec text, comparing `initial_state.causal_alignment` "
        "with `state_after_gap.causal_alignment` in the %d stored "
        "`hidden_user_action` trajectories: alignment actually changed in the "
        "domains %s."
        % (sum(flip.values()), ", ".join(flipped_domains) or "(none)")
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    if total_rewrites >= 42:
        md.append(
            "**The paper has to qualify the explicit-user-update condition "
            "substantially.** In %d of 84 scenarios the hidden user action "
            "overwrites `causal_alignment` -- the variable that the early clue "
            "exists to determine and that the model is scored on reporting. In "
            "those scenarios the condition is not testing whether the model "
            "retained and applied the clue; it is testing whether the model can "
            "read a plainly-stated outcome that has made the clue irrelevant."
            % total_rewrites
        )
    else:
        md.append(
            "**The qualification needed is limited.** Only %d of 84 scenarios "
            "rewrite `causal_alignment`, so for the remaining %d the explicit-user-"
            "update condition still requires the model to hold the clue."
            % (total_rewrites, 84 - total_rewrites)
        )
    md.append("")
    md.append(
        "This interacts with R5. The user-update revision gain of 0.78 / 0.81 / "
        "0.46 is the largest effect in the benchmark, and `causal_alignment` is a "
        "contributing changed variable *only* in this condition (R5's k column "
        "jumps from ~110 to ~190). Part of that gain is therefore the model "
        "tracking a variable the intervention itself set, announced in the same "
        "utterance. The effect is still real -- the domain outcome variable also "
        "moves -- but the headline number should either be quoted for the outcome "
        "variable alone or carry an explicit note."
    )
    md.append("")
    md.append(
        "Suggested wording for the limitations paragraph: *in %d of 84 scenarios "
        "the hidden user action also sets the causal-alignment variable, so the "
        "explicit-user-update condition measures response to plainly stated "
        "evidence rather than retention of the earlier clue.*" % total_rewrites
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("rewrites causal_alignment: %d / 84  (declarative specs: %d)"
          % (total_rewrites, total_decl))
    for r in dom_rows:
        print("  %-16s n=%d decl=%d rewrites=%d  targets: %s"
              % (r[0], r[1], r[2], r[3], r[6]))
    print()
    print("realized alignment change under hidden_user_action, domains:",
          flipped_domains)


if __name__ == "__main__":
    main()
