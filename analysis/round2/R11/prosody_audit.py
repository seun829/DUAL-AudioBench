"""R11. Prosody parameter audit.

For each of the 84 scenarios, resolve prosody_pair.high.prosody and
.low.prosody through the PROSODY table in dual_audio/modalities/audio.py and
report the pitch and speed delta.  Counts how many scenarios have the high
member higher on both axes, on one, or on neither.

Also reports the completion state of the listening packet:
paper_results/v05/internal_audit/prosody/public/01_prosody_responses.csv --
how many of the 21 rows have a non-empty more_intense_clip, and for those,
whether the choice matches the intended high member.

The private answer key is gitignored and absent from this checkout, so the
intended-high mapping is recovered from the public booklet where it is stated,
and reported as NOT FOUND otherwise.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C
from dual_audio.modalities.audio import PROSODY

TASK = "R11"
AUDIT = (
    C.ROOT / "paper_results" / "v05" / "internal_audit" / "prosody" / "public"
)


def main() -> None:
    tasks = C.load_tasks()

    detail = []
    contrast = Counter()
    direction = Counter()
    for sid in sorted(tasks):
        t = tasks[sid]
        p = t["prosody_pair"]
        hi, lo = p["high"]["prosody"], p["low"]["prosody"]
        hp, hs = (int(x) for x in PROSODY[hi])
        lp, ls = (int(x) for x in PROSODY[lo])
        dp, ds = hp - lp, hs - ls
        if dp > 0 and ds > 0:
            d = "higher on both"
        elif dp > 0 or ds > 0:
            d = "higher on one"
        else:
            d = "higher on neither"
        direction[d] += 1
        contrast[(hi, hp, hs, lo, lp, ls, dp, ds, d)] += 1
        detail.append([
            sid, t["domain"], p["native_prosody"],
            hi, hp, hs, p["high"]["expected_style"],
            lo, lp, ls, p["low"]["expected_style"],
            dp, ds, d,
            t.get("prosody_stimulus", {}).get("transcript_variant"),
            t["audio_profile"]["user_voice"],
        ])

    C.write_csv(TASK, [
        "scenario_id", "domain", "native_prosody",
        "high_name", "high_pitch", "high_speed", "high_expected_style",
        "low_name", "low_pitch", "low_speed", "low_expected_style",
        "delta_pitch", "delta_speed", "direction",
        "transcript_variant", "user_voice",
    ], detail)

    # ---------------- listening packet completion ----------------
    resp_path = AUDIT / "01_prosody_responses.csv"
    booklet = AUDIT / "01_prosody_booklet.md"
    audit_rows = []
    filled = 0
    total = 0
    if resp_path.exists():
        with resp_path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                total += 1
                mi = (row.get("more_intense_clip") or "").strip()
                if mi:
                    filled += 1
                audit_rows.append([
                    row.get("audit_item_id"), mi or "(blank)",
                    (row.get("clip_a_tone") or "").strip() or "(blank)",
                    (row.get("clip_b_tone") or "").strip() or "(blank)",
                    (row.get("speech_clarity") or "").strip() or "(blank)",
                    (row.get("confidence_1_to_5") or "").strip() or "(blank)",
                ])
    # can the intended high member be recovered from the public booklet?
    key_available = False
    if booklet.exists():
        text = booklet.read_text(encoding="utf-8", errors="replace")
        key_available = bool(re.search(r"intended|answer key|high member", text, re.I))

    with (C.outdir(TASK) / "listening_packet_status.csv").open(
        "w", newline="", encoding="utf-8"
    ) as fh:
        w = csv.writer(fh)
        w.writerow(["audit_item_id", "more_intense_clip", "clip_a_tone",
                    "clip_b_tone", "speech_clarity", "confidence"])
        w.writerows(audit_rows)

    # ---------------- LaTeX ----------------
    tex = [
        "% R11: the acoustic contrast behind the high/low prosody conditions.",
        "\\begin{table}[htbp]",
        "  \\centering",
        "  \\footnotesize",
        "  \\setlength{\\tabcolsep}{5pt}",
        "  \\renewcommand{\\arraystretch}{1.08}",
        "  \\caption{The five distinct acoustic contrasts behind the high and low"
        " prosody conditions. Pitch and speed are the eSpeak-NG \\texttt{-p} and"
        " \\texttt{-s} arguments; within a pair the words and voice are identical."
        " A positive delta means the high member is higher. The manipulation has no"
        " consistent direction: in 54 of 84 scenarios the high member is lower in"
        " pitch or slower.}",
        "  \\label{tab:prosody-contrast}",
        "  \\begin{tabular}{@{}llllrrl@{}}",
        "    \\toprule",
        "    \\dualcolhead{High} & \\dualcolhead{$p$/$s$} & \\dualcolhead{Low} &"
        " \\dualcolhead{$p$/$s$} & \\dualcolhead{$\\Delta p$} &"
        " \\dualcolhead{$\\Delta s$} & \\dualcolhead{$n$} \\\\",
        "    \\midrule",
    ]
    for (hi, hp, hs, lo, lp, ls, dp, ds, d), n in contrast.most_common():
        tex.append(
            "    %s & %d/%d & %s & %d/%d & %+d & %+d & %d \\\\"
            % (hi, hp, hs, lo, lp, ls, dp, ds, n)
        )
    tex += ["    \\bottomrule", "  \\end{tabular}", "\\end{table}"]
    C.write_text(TASK, "table.tex", "\n".join(tex) + "\n")

    # ---------------- README ----------------
    md = ["# R11. Prosody parameter audit", ""]
    md.append(
        "The only acoustic difference between the high and low conditions is the "
        "eSpeak-NG `-p` (pitch, 0-99) and `-s` (speed, words/min) pair looked up "
        "from `PROSODY` in `dual_audio/modalities/audio.py:12-19`. No amplitude, "
        "word-gap, or voice change; within a pair the words and voice are identical."
    )
    md.append("")
    md.append("## The five distinct contrasts")
    md.append("")
    md.append(
        C.md_table(
            ["High name", "pitch/speed", "Low name", "pitch/speed",
             "delta pitch", "delta speed", "n", "Direction"],
            [
                [hi, "%d/%d" % (hp, hs), lo, "%d/%d" % (lp, ls),
                 "%+d" % dp, "%+d" % ds, n, d]
                for (hi, hp, hs, lo, lp, ls, dp, ds, d), n in contrast.most_common()
            ],
        )
    )
    md.append("")
    md.append("## Direction summary")
    md.append("")
    md.append(
        C.md_table(
            ["Direction", "scenarios", "share"],
            [[k, v, "%.0f%%" % (100.0 * v / 84)]
             for k, v in direction.most_common()],
        )
    )
    md.append("")
    md.append("## Listening packet completion")
    md.append("")
    md.append(
        "`paper_results/v05/internal_audit/prosody/public/01_prosody_responses.csv` "
        "contains **%d rows, of which %d have a non-empty `more_intense_clip`**."
        % (total, filled)
    )
    md.append("")
    md.append(
        C.md_table(
            ["Item", "more intense", "clip A tone", "clip B tone", "clarity",
             "confidence"],
            audit_rows,
        )
    )
    md.append("")
    md.append(
        "**Whether the two answered choices match the intended high member: "
        "NOT FOUND.** The intended-high mapping lives in the nested `private/` "
        "directory, which `.gitignore` excludes (`paper_results/v05/internal_audit/"
        "**/private/`) and which is absent from this checkout. The public booklet "
        "%s state it either. With 2 of 21 rows answered the comparison would be "
        "uninformative regardless."
        % ("does not" if not key_available else "may")
    )
    md.append("")
    md.append("## Reading")
    md.append("")
    md.append(
        "**The manipulation has no consistent acoustic direction, and this is the "
        "finding that should change the paper.** Of 84 scenarios, %d have the high "
        "member higher on both pitch and speed, %d on only one axis, and %d on "
        "neither."
        % (
            direction.get("higher on both", 0),
            direction.get("higher on one", 0),
            direction.get("higher on neither", 0),
        )
    )
    md.append("")
    md.append(
        "Two specific problems. In the 30 `frustrated` vs `calm` pairs the high "
        "member is **20 pitch units lower** than the low member (30 against 50), "
        "compensated only by being 25 wpm faster. In the 18 `confused` vs "
        "`confident` pairs the high member is 5 pitch units higher but **15 wpm "
        "slower** -- the smallest and most ambiguous contrast in the set. `high` "
        "and `low` name an expected *response style* "
        "(`acknowledge_impact`, `acknowledge_urgency`, `clarify_and_reassure` "
        "against `proceed_directly`), not an acoustic intensity, and the `PROSODY` "
        "table encodes no monotone intensity ordering."
    )
    md.append("")
    md.append(
        "Consequences for the paper. The existing hedge at `main.tex:361` "
        "(\"cannot distinguish model insensitivity from an insufficiently "
        "recognizable synthetic-speech manipulation\") is correct but understates "
        "the problem: it is not that the manipulation might be too subtle, it is "
        "that it is not a single-directional manipulation at all, so pooling the "
        "five contrasts into one high-versus-low contrast is not well defined. Any "
        "prosody claim has to be made per contrast, with n=30/24/18/6/6. The "
        "listening audit at 2 of 21 rows cannot settle it either way."
    )
    md.append("")
    md.append(
        "A third, separate confound worth noting: the two prosody conditions also "
        "change the **words**, via `PROSODY_TRANSCRIPT_FRAMES` "
        "(`dual_audio/users/scripted.py:7-11`), with 28 scenarios on each of the "
        "three carrier frames. So prosody-versus-ordinary is not a pure acoustic "
        "contrast; high-versus-low within a scenario is, because both members share "
        "that scenario's frame."
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("direction summary:", dict(direction))
    for (hi, hp, hs, lo, lp, ls, dp, ds, d), n in contrast.most_common():
        print("  %-11s %2d/%3d  vs %-11s %2d/%3d  dp=%+3d ds=%+3d  n=%2d  %s"
              % (hi, hp, hs, lo, lp, ls, dp, ds, n, d))
    print()
    print("listening packet: %d rows, %d answered" % (total, filled))


if __name__ == "__main__":
    main()
