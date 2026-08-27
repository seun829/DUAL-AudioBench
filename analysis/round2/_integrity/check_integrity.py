"""Guardrail G1/G2 integrity check.

Records a SHA-256 manifest of every file that must not change (the G1 protected
source files, the frozen scenario set, and the whole frozen-evidence tree under
paper_results/).  Run with ``baseline`` once before any work, then ``verify``
after each task.  Line endings are normalised to LF before hashing so a CRLF
checkout does not produce a spurious difference.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "baseline.json"

# G1: files whose contents determine realized states, gold actions, or audio.
G1_FILES = [
    "dual_audio/core/environment.py",
    "dual_audio/modalities/audio.py",
    "dual_audio/users/scripted.py",
]
# G1 + G2: whole trees that must not change.
FROZEN_TREES = ["data/scenarios_v05", "paper_results"]
# The E1 oracle-state run is a NEW directory that G2 explicitly permits under
# paper_results/v05/raw/<new_slug>/. Additions there are expected; nothing
# pre-existing may change.
NEW_RUN_PREFIXES = ("paper_results/v05/raw/oracle_state/",)

TEXT_SUFFIXES = {
    ".py", ".json", ".jsonl", ".md", ".csv", ".tex", ".txt", ".sty",
    ".ps1", ".bib", ".log", ".sh", ".yml", ".yaml", ".cfg", ".ini",
}


def digest(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def collect() -> dict[str, str]:
    manifest: dict[str, str] = {}
    for rel in G1_FILES:
        p = ROOT / rel
        manifest[rel] = digest(p) if p.exists() else "MISSING"
    for tree in FROZEN_TREES:
        base = ROOT / tree
        for p in sorted(base.rglob("*")):
            if p.is_file():
                rel = p.relative_to(ROOT).as_posix()
                if rel.startswith(NEW_RUN_PREFIXES):
                    continue
                manifest[rel] = digest(p)
    return manifest


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    current = collect()
    if mode == "baseline":
        OUT.write_text(json.dumps(current, indent=0, sort_keys=True), encoding="utf-8")
        print(f"baseline written: {len(current)} files -> {OUT}")
        return
    if not OUT.exists():
        raise SystemExit("no baseline.json; run with 'baseline' first")
    base = json.loads(OUT.read_text(encoding="utf-8"))
    changed = sorted(k for k in base.keys() & current.keys() if base[k] != current[k])
    removed = sorted(base.keys() - current.keys())
    added = sorted(current.keys() - base.keys())
    for label, rows in (("CHANGED", changed), ("REMOVED", removed), ("ADDED", added)):
        for r in rows:
            print(f"{label}: {r}")
    if changed or removed or added:
        raise SystemExit(
            f"INTEGRITY FAIL: {len(changed)} changed, {len(removed)} removed, {len(added)} added"
        )
    print(f"INTEGRITY OK: {len(current)} protected files unchanged")


if __name__ == "__main__":
    main()
