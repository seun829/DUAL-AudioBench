"""Capture score.py's full text output and every summarize() field, so the C1
patch can be proved additive (acceptance: previously reported fields must be
reproduced bit-identically).
"""
import io, json, sys, contextlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import score

LOG = ROOT / "paper_results" / "v05" / "raw" / "gemini3_priority" / "gemini3_priority_shard00-of-12.jsonl"
out = Path(__file__).resolve().parent
rows = score.load(LOG)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    score.condition_table(rows)
    score.belief_report(rows)
    score.paired_control_report(rows)
    score.failure_report(rows)
(out / (sys.argv[1] + "_text.txt")).write_text(buf.getvalue(), encoding="utf-8")
fields = {}
from collections import defaultdict
groups = defaultdict(list)
for r in rows:
    groups[r["condition"]].append(r)
for cond, g in sorted(groups.items()):
    fields[cond] = score.summarize(g)
(out / (sys.argv[1] + "_fields.json")).write_text(
    json.dumps(fields, indent=1, sort_keys=True, default=str), encoding="utf-8")
print("wrote", sys.argv[1], "| conditions:", sorted(groups), "| rows:", len(rows))
