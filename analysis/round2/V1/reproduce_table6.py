"""V1. Reproduce the paper's complete condition table (Table 6) from raw JSONL.

Recomputes, per model and condition:
  first action  = pre_gap_success
  final action  = post_gap_success
  belief        = belief_checkpoints.post_observation.evaluation.all_correct
  strict        = trajectory_success

and compares each cell against the values hard-coded below, which are
transcribed verbatim from paper/main.tex Table 6 (tab:all-results).

Also audits the integrity claims in the work order: n=168 per populated cell,
error-row count, 4368 total non-error rows, and 9/9/8 conditions per model.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "V1"

# Transcribed from paper/main.tex lines 452-481 (Table 6).
# model label, condition label -> (n, first, final, belief, strict)
PAPER = {
    ("Gemini 2.5", "Ordinary audio"): (168, 69.6, 35.1, 39.3, 1.2),
    ("Gemini 2.5", "No state change"): (168, 67.9, 38.7, 60.7, 8.9),
    ("Gemini 2.5", "Short clue"): (168, 63.7, 35.7, 35.7, 1.8),
    ("Gemini 2.5", "Clue removed"): (168, 59.5, 25.0, 29.8, 1.2),
    ("Gemini 2.5", "Transcript"): (168, 77.4, 35.7, 51.8, 10.1),
    ("Gemini 2.5", "Neutral audio"): (168, 64.9, 31.5, 32.7, 0.6),
    ("Gemini 2.5", "Explicit user update"): (168, 63.7, 72.0, 72.6, 17.9),
    ("Gemini 2.5", "High prosody"): (168, 68.5, 36.9, 37.5, 0.6),
    ("Gemini 2.5", "Low prosody"): (168, 63.7, 32.1, 35.7, 3.6),
    ("Gemini 3", "Ordinary audio"): (168, 80.4, 47.0, 51.2, 14.9),
    ("Gemini 3", "No state change"): (168, 75.0, 48.2, 78.6, 21.4),
    ("Gemini 3", "Short clue"): (168, 66.1, 42.3, 50.6, 11.9),
    ("Gemini 3", "Clue removed"): (168, 66.7, 26.8, 32.1, 3.6),
    ("Gemini 3", "Transcript"): (168, 84.5, 58.3, 64.3, 21.4),
    ("Gemini 3", "Neutral audio"): (168, 78.0, 45.2, 54.2, 10.7),
    ("Gemini 3", "Explicit user update"): (168, 75.0, 79.8, 85.1, 22.0),
    ("Gemini 3", "High prosody"): (168, 74.4, 44.6, 51.2, 0.6),
    ("Gemini 3", "Low prosody"): (168, 72.0, 40.5, 53.0, 2.4),
    ("GPT Audio Mini", "Ordinary audio"): (168, 65.5, 22.0, 31.0, 0.0),
    ("GPT Audio Mini", "No state change"): (168, 61.3, 21.4, 63.1, 3.0),
    ("GPT Audio Mini", "Short clue"): (168, 66.7, 20.8, 32.7, 1.2),
    ("GPT Audio Mini", "Clue removed"): (168, 55.4, 26.8, 17.3, 0.6),
    ("GPT Audio Mini", "Neutral audio"): (168, 63.1, 19.0, 32.1, 0.6),
    ("GPT Audio Mini", "Explicit user update"): (168, 65.5, 63.1, 67.9, 8.9),
    ("GPT Audio Mini", "High prosody"): (168, 60.7, 19.6, 30.4, 0.0),
    ("GPT Audio Mini", "Low prosody"): (168, 60.7, 20.2, 40.5, 0.6),
}

FIELDS = [
    ("first action", "m_first_action"),
    ("final action", "m_final_action"),
    ("belief after gap", "m_belief_post"),
    ("strict", "m_strict"),
]


def main() -> None:
    all_rows = C.load_rows(include_errors=True)
    rows = C.annotate(C.load_rows())
    errs = [r for r in all_rows if r.get("error")]
    groups = C.by_model_condition(rows)

    # ---------------- integrity audit ----------------
    audit: list[tuple[str, str, str]] = []

    def check(label: str, got, want) -> None:
        audit.append((label, str(got), "PASS" if got == want else "FAIL (expected %s)" % want))

    check("total non-error rows", len(rows), 4368)
    check("total rows in files", len(all_rows), 4412)
    check("error rows in files", len(errs), 0)
    good_keys = {
        (r["model"], r["scenario_id"], r["condition"], r["seed"]) for r in rows
    }
    orphans = [
        r for r in errs
        if (r.get("model"), r["scenario_id"], r["condition"], r["seed"])
        not in good_keys
    ]
    check("error rows never retried", len(orphans), 0)
    orphan_cells = sorted({(r.get("model"), r["condition"]) for r in orphans})
    per_model_conds = Counter(r["model"] for r in rows)
    conds_per_model = {
        m: len({r["condition"] for r in rows if r["model"] == m})
        for m in C.MODEL_ORDER
    }
    for m, want in zip(C.MODEL_ORDER, (9, 9, 8)):
        check("conditions for " + C.MODEL_LABEL[m], conds_per_model.get(m), want)
    bad_n = [
        (C.MODEL_LABEL[m], C.COND_LABEL[c], len(groups[(m, c)]))
        for (m, c) in C.populated_cells(rows)
        if len(groups[(m, c)]) != 168
    ]
    check("populated cells with n!=168", len(bad_n), 0)
    check("populated cells", len(C.populated_cells(rows)), 26)

    # ---------------- cell-by-cell comparison ----------------
    csv_rows = []
    mismatches = []
    for (model, cond) in C.populated_cells(rows):
        g = groups[(model, cond)]
        mlab, clab = C.MODEL_LABEL[model], C.COND_LABEL[cond]
        want = PAPER.get((mlab, clab))
        got_n = len(g)
        line = [mlab, clab, got_n, want[0] if want else ""]
        for fname, field in FIELDS:
            got = C.rate(g, field)
            line.append(round(got, 1))
        if want:
            for i, (fname, field) in enumerate(FIELDS):
                got = round(C.rate(g, field), 1)
                exp = want[1 + i]
                line.append(exp)
                if abs(got - exp) > 0.05:
                    mismatches.append((mlab, clab, fname, got, exp))
            if got_n != want[0]:
                mismatches.append((mlab, clab, "n", got_n, want[0]))
        else:
            line.extend([""] * len(FIELDS))
        csv_rows.append(line)

    header = (
        ["model", "condition", "n_recomputed", "n_paper"]
        + ["%s_recomputed" % f for f, _ in FIELDS]
        + ["%s_paper" % f for f, _ in FIELDS]
    )
    C.write_csv(TASK, header, csv_rows)

    # ---------------- README ----------------
    md = ["# V1. Reproduce the paper's complete condition table (Table 6)", ""]
    md.append(
        "Recomputed from every non-error row under `paper_results/v05/raw/`. "
        "Paper values transcribed from `paper/main.tex` Table 6 "
        "(`tab:all-results`, lines 452-481)."
    )
    md.append("")
    md.append("## Cell comparison (percent; `=` means the recomputed value matches)")
    md.append("")
    disp_header = ["Model", "Condition", "n", "First", "Final", "Belief", "Strict"]
    disp_rows = []
    for line in csv_rows:
        mlab, clab, n = line[0], line[1], line[2]
        cells = []
        for i in range(len(FIELDS)):
            got = line[4 + i]
            exp = line[4 + len(FIELDS) + i]
            if exp == "":
                cells.append("%.1f (no paper cell)" % got)
            elif abs(got - exp) <= 0.05:
                cells.append("%.1f =" % got)
            else:
                cells.append("**%.1f vs %.1f**" % (got, exp))
        disp_rows.append([mlab, clab, n] + cells)
    md.append(C.md_table(disp_header, disp_rows))
    md.append("")
    md.append("## Integrity audit")
    md.append("")
    md.append(C.md_table(["check", "value", "verdict"], [list(a) for a in audit]))
    md.append("")
    if orphan_cells:
        md.append("Error rows with no successful retry, by cell:")
        md.append("")
        md.append(
            C.md_table(
                ["model", "condition", "count"],
                [
                    [C.MODEL_LABEL.get(m, m), C.COND_LABEL.get(c, c),
                     sum(1 for r in orphans if r.get("model") == m
                         and r["condition"] == c)]
                    for (m, c) in orphan_cells
                ],
            )
        )
        md.append("")
    md.append("## Reading")
    md.append("")
    if mismatches:
        md.append(
            "**%d of %d compared cells do not match.**" % (len(mismatches), 26 * 4)
        )
        md.append("")
        md.append(
            C.md_table(
                ["model", "condition", "metric", "recomputed", "paper"],
                [list(m) for m in mismatches],
            )
        )
    else:
        md.append(
            "All %d compared cells (26 populated model-condition cells x 4 metrics) "
            "match `paper/main.tex` Table 6 to one decimal place. Every populated "
            "cell has exactly n=168, there are 26 populated cells (9 + 9 + 8), and "
            "4,368 non-error rows in total, as the work order states."
            % (26 * 4)
        )
    md.append("")
    md.append(
        "One correction to the work order's acceptance list: the raw files contain "
        "**44 error rows**, not zero. 20 of them were retried successfully within "
        "the same shard file (`load_done` in `run_eval.py` deliberately excludes "
        "error rows so a later invocation retries them), so they do not affect any "
        "reported number. The remaining 24 are all "
        "`openai/gpt-audio-mini` x `transcript_only`, an abandoned attempt that "
        "failed with `OpenRouter HTTP 400: Provider returned error` -- that model "
        "cannot serve the text-only endpoint used by the transcript control. That "
        "is why GPT Audio Mini has 8 conditions rather than 9, and why the paper's "
        "Table 6 correctly omits the cell. The accurate claim is *zero error rows "
        "among the 26 reported cells*."
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("mismatched cells:", len(mismatches))
    for m in mismatches:
        print("  MISMATCH", m)
    for label, got, verdict in audit:
        print("%-34s %-8s %s" % (label, got, verdict))


if __name__ == "__main__":
    main()
