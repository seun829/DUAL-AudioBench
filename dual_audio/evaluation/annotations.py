"""Export and validate independent multilabel trap annotations.

Usage:
  python -m dual_audio.evaluation.annotations export data/scenarios ann_a.csv A
  python -m dual_audio.evaluation.annotations export data/scenarios ann_b.csv B
  python -m dual_audio.evaluation.annotations report ann_a.csv ann_b.csv
"""

from __future__ import annotations

import csv
import itertools
import json
import sys
from pathlib import Path


def export_sheet(tasks_dir: str, output: str, annotator: str) -> None:
    """Write one blank, independently completable multilabel trap sheet."""

    rows = []
    for path in sorted(Path(tasks_dir).glob("*.json")):
        task = json.loads(path.read_text(encoding="utf-8"))
        for stage in ("pre_gap", "post_gap"):
            for item in task[f"{stage}_actions"]:
                if not item.get("failure_tags"):
                    continue
                rows.append(
                    {
                        "annotator": annotator,
                        "scenario_id": task["scenario_id"],
                        "stage": stage,
                        "action": item["action"],
                        "description": item["description"],
                        "labels_semicolon_separated": "",
                        "ambiguous": "",
                        "notes": "",
                    }
                )
    with Path(output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} blinded trap rows -> {output}")


def _read(path: str) -> tuple[str, dict[tuple[str, str, str], set[str]]]:
    """Load one completed annotation sheet and enforce one annotator ID."""

    labels = {}
    annotators = set()
    with Path(path).open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            annotators.add(row["annotator"].strip())
            raw = row["labels_semicolon_separated"].strip()
            if not raw:
                raise SystemExit(
                    f"Unlabeled row in {path}: {row['scenario_id']}/{row['action']}"
                )
            key = (row["scenario_id"], row["stage"], row["action"])
            labels[key] = {label.strip() for label in raw.split(";") if label.strip()}
    if len(annotators) != 1:
        raise SystemExit(f"{path} must contain exactly one annotator id")
    return annotators.pop(), labels


def report(paths: list[str]) -> None:
    """Report pairwise exact-set and Jaccard agreement on shared traps."""

    if len(paths) < 2:
        raise SystemExit("At least two independent annotation files are required.")
    annotations = [_read(path) for path in paths]
    shared = set.intersection(*(set(labels) for _, labels in annotations))
    if not shared:
        raise SystemExit("Annotation files have no shared items.")
    print(f"Annotators: {', '.join(name for name, _ in annotations)}")
    print(f"Shared traps: {len(shared)}")
    for (name_a, labels_a), (name_b, labels_b) in itertools.combinations(
        annotations, 2
    ):
        exact = sum(labels_a[key] == labels_b[key] for key in shared) / len(shared)
        jaccard = sum(
            len(labels_a[key] & labels_b[key])
            / len(labels_a[key] | labels_b[key])
            for key in shared
        ) / len(shared)
        print(
            f"{name_a} vs {name_b}: exact={exact:.1%}, "
            f"mean multilabel Jaccard={jaccard:.3f}"
        )


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "export" and len(sys.argv) == 5:
        export_sheet(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "report" and len(sys.argv) >= 4:
        report(sys.argv[2:])
    else:
        print(__doc__)
