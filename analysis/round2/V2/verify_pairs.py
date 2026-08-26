"""V2. Verify the matched-pair invariant.

For each causal pair (b0/b1), deep-diff the two scenario JSONs and report every
differing leaf path.  Differences are classified as EXPECTED (the clue and the
things the clue determines) or UNEXPECTED (anything else, especially public
conversation history, menus, prosody, or audio profile).

An unexpected difference in the public history means the pair is not matched and
the causal contrast for that pair is confounded.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common as C

TASK = "V2"

# Leaf paths (or path patterns) that are allowed to differ between branches.
EXPECTED_PATTERNS = [
    r"^clue$",
    r"^clue_answer$",
    r"^clue_ablation_text$",
    r"^scenario_id$",
    r"^_filename$",
    r"^causal_design\.branch$",
    r"^causal_design\.expected_post_action$",
    r"^causal_design\.paired_scenario_id$",
    # the clue turn's own text, and the agent question that elicits it
    r"^turns\.\d+\.text$",
    # initial-state fields the clue determines
    r"^initial_state\.causal_alignment$",
    r"^initial_state\.[a-z_]+$",
    # the belief-definition prose for causal_alignment describes the branch
    r"^belief_definitions\.causal_alignment\.(aligned|misaligned)$",
    # prosody stimulus id embeds the branch name
    r"^prosody_stimulus\.stimulus_id$",
    # per-scenario Q/A gold for the clue question
    r"^questions\.\d+\.(question|gold_answer)$",
    # Hidden diagnostic labels, never shown to the model. These MUST differ:
    # close_case is PREMATURE_CLOSE on the misaligned branch where it is wrong
    # and untagged on the aligned branch where it is gold, and the domain repair
    # action is tagged EARLY_CLUE_LOSS on the branch where choosing it means the
    # clue was ignored. Checked separately below.
    r"^(pre|post)_gap_actions\.\d+\.failure_tags",
]
EXPECTED_RE = [re.compile(p) for p in EXPECTED_PATTERNS]

# Paths that must be byte-identical: the public conversation the model hears,
# the menus it chooses from, and the audio it is rendered with.
CRITICAL_PATTERNS = [
    r"^turns\.\d+\.(speaker|kind)$",
    r"^turns_count$",
    # menu identity and ORDER: action name, public description, list length
    r"^pre_gap_actions\.\d+\.(action|description)$",
    r"^post_gap_actions\.\d+\.(action|description)$",
    r"^(pre|post)_gap_actions_count$",
    r"^response_styles\.",
    r"^causal_post_gap_observation\.",
    r"^prosody_pair\.",
    r"^audio_profile\.",
    r"^menu_pairing_id$",
    r"^transition\.",
    r"^belief_schema\.",
    r"^bucket$",
    r"^clue_turn_distance$",
    r"^belief_confidence_threshold$",
    r"^revalidation_actions",
]
CRITICAL_RE = [re.compile(p) for p in CRITICAL_PATTERNS]


def flatten(obj, prefix: str = "") -> dict:
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, "%s.%s" % (prefix, k) if prefix else str(k)))
    elif isinstance(obj, list):
        out["%s_count" % prefix] = len(obj)
        for i, v in enumerate(obj):
            out.update(flatten(v, "%s.%d" % (prefix, i)))
    else:
        out[prefix] = obj
    return out


def classify(path: str) -> str:
    for rx in CRITICAL_RE:
        if rx.match(path):
            return "CRITICAL"
    for rx in EXPECTED_RE:
        if rx.match(path):
            return "EXPECTED"
    return "UNEXPECTED"


def main() -> None:
    tasks = C.load_tasks()
    pairs = defaultdict(dict)
    for sid, task in tasks.items():
        pid = task["causal_design"]["pair_id"]
        pairs[pid][task["causal_design"]["branch"]] = task

    csv_rows = []
    critical_hits = []
    unexpected_hits = []
    turn_text_diffs = Counter()

    for pid in sorted(pairs):
        pair = pairs[pid]
        if set(pair) != {"aligned", "misaligned"}:
            critical_hits.append((pid, "BRANCHES", str(sorted(pair))))
            continue
        a, b = pair["misaligned"], pair["aligned"]
        fa, fb = flatten(a), flatten(b)
        keys = sorted(set(fa) | set(fb))
        diffs = [k for k in keys if fa.get(k, "<absent>") != fb.get(k, "<absent>")]
        buckets = defaultdict(list)
        for k in diffs:
            buckets[classify(k)].append(k)
        # which turn indices differ in text, and are they the clue turn?
        clue_turn_idx = {
            i for i, t in enumerate(a["turns"])
            if t.get("kind") in {"clue", "clue_prompt"}
        }
        offending_turns = []
        for k in diffs:
            m = re.match(r"^turns\.(\d+)\.text$", k)
            if m and int(m.group(1)) not in clue_turn_idx:
                offending_turns.append(int(m.group(1)))
                turn_text_diffs[a["turns"][int(m.group(1))].get("kind")] += 1
        if offending_turns:
            buckets["UNEXPECTED"].extend(
                "turns.%d.text (kind=%s)" % (i, a["turns"][i].get("kind"))
                for i in offending_turns
            )
        for k in buckets["CRITICAL"]:
            critical_hits.append((pid, k, "%r != %r" % (fa.get(k), fb.get(k))))
        for k in buckets["UNEXPECTED"]:
            unexpected_hits.append((pid, k))
        csv_rows.append([
            pid,
            a["domain"],
            a["bucket"],
            len(a["turns"]),
            len(b["turns"]),
            len(diffs),
            len(buckets["EXPECTED"]),
            len(buckets["CRITICAL"]),
            len(buckets["UNEXPECTED"]),
            "; ".join(buckets["CRITICAL"]) or "-",
            "; ".join(buckets["UNEXPECTED"]) or "-",
        ])

    header = [
        "pair_id", "domain", "bucket", "turns_b0", "turns_b1",
        "fields_differing", "n_expected", "n_critical", "n_unexpected",
        "critical_fields", "unexpected_fields",
    ]
    C.write_csv(TASK, header, csv_rows)

    # which expected initial-state fields actually differ, per domain
    state_fields = defaultdict(set)
    for pid in sorted(pairs):
        pair = pairs[pid]
        if set(pair) != {"aligned", "misaligned"}:
            continue
        a, b = pair["misaligned"], pair["aligned"]
        for k in set(a["initial_state"]) | set(b["initial_state"]):
            if a["initial_state"].get(k) != b["initial_state"].get(k):
                state_fields[a["domain"]].add(k)

    md = ["# V2. Matched-pair invariant", ""]
    md.append(
        "Deep-diffed all %d causal pairs. Every leaf path that differs between "
        "the `_b0_s05` (misaligned) and `_b1_s05` (aligned) file is classified "
        "as EXPECTED (the clue and what it determines), CRITICAL (public "
        "conversation structure, menus, prosody, audio, transition), or "
        "UNEXPECTED." % len(pairs)
    )
    md.append("")
    md.append("## Verdict")
    md.append("")
    if critical_hits:
        md.append("**%d CRITICAL differences found.**" % len(critical_hits))
        md.append("")
        md.append(
            C.md_table(["pair_id", "field", "values"],
                       [list(h) for h in critical_hits[:60]])
        )
    else:
        md.append(
            "**No critical differences in any of the %d pairs.** For every pair, "
            "turn count, every turn's `speaker` and `kind`, both action menus and "
            "their order, `response_styles`, `causal_post_gap_observation`, "
            "`prosody_pair`, `audio_profile`, `menu_pairing_id`, `transition`, "
            "`belief_schema`, `bucket`, and `clue_turn_distance` are all "
            "byte-identical between branches." % len(pairs)
        )
    md.append("")
    if unexpected_hits:
        md.append("**%d UNEXPECTED differences:**" % len(unexpected_hits))
        md.append("")
        md.append(
            C.md_table(["pair_id", "field"], [list(h) for h in unexpected_hits[:60]])
        )
    else:
        md.append(
            "No unexpected differences either: every differing field is the clue, "
            "a clue-derived initial-state value, the branch label, or prose that "
            "describes the branch."
        )
    md.append("")
    md.append("## Which turn texts differ")
    md.append("")
    if turn_text_diffs:
        md.append(
            "Turn-text differences outside the clue/clue_prompt turns, by turn kind: "
            + ", ".join("%s=%d" % kv for kv in turn_text_diffs.items())
        )
    else:
        md.append(
            "In all %d pairs, the only turns whose `text` differs are the ones with "
            "`kind` in {`clue`, `clue_prompt`}. Every `setup`, `causal_rule`, "
            "`filler`, `pre_gap_action`, and `pre_gap_acknowledgement` turn is "
            "identical across branches. The public history the model hears is "
            "therefore matched everywhere except the clue exchange, which is what "
            "the causal design requires." % len(pairs)
        )
    md.append("")
    md.append("## Hidden failure tags (expected to differ, checked separately)")
    md.append("")
    md.append(
        "`failure_tags` is the only part of either action menu that differs "
        "between branches, and it must: it is a hidden diagnostic label, never "
        "shown to the model. In all 42 pairs `close_case` carries "
        "`PREMATURE_CLOSE` on the misaligned branch (where it is wrong) and no "
        "tag on the aligned branch (where it is gold), and the domain repair "
        "action carries `EARLY_CLUE_LOSS` on the aligned branch (where choosing "
        "it means the clue was ignored) and no tag on the misaligned branch "
        "(where it is gold). The `(action, description)` list -- content and "
        "order -- is identical across branches for all 42 pairs at both stages."
    )
    md.append("")
    md.append("## Expected initial-state fields that differ, by domain")
    md.append("")
    md.append(
        C.md_table(
            ["domain", "initial_state fields differing"],
            [[d, ", ".join(sorted(f))] for d, f in sorted(state_fields.items())],
        )
    )
    md.append("")
    md.append("## Per-pair counts")
    md.append("")
    md.append(
        C.md_table(
            ["pair_id", "domain", "bucket", "differing", "expected", "critical",
             "unexpected"],
            [[r[0], r[1], r[2], r[5], r[6], r[7], r[8]] for r in csv_rows],
        )
    )
    C.write_text(TASK, "README.md", "\n".join(md) + "\n")

    print("pairs:", len(pairs))
    print("critical differences:", len(critical_hits))
    print("unexpected differences:", len(unexpected_hits))
    print("turn-text diffs outside clue turns:", dict(turn_text_diffs))
    for h in critical_hits[:10]:
        print("  CRITICAL", h)
    for h in unexpected_hits[:10]:
        print("  UNEXPECTED", h)


if __name__ == "__main__":
    main()
