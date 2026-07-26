"""Create and score a blinded human audibility check for prosodic pairs.

Usage:
  python -m dual_audio.evaluation.prosody_validation export \
      data/turn_audio/manifest.jsonl listener_a.csv listener_a
  python -m dual_audio.evaluation.prosody_validation report listener_a.csv listener_b.csv
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from pathlib import Path


def export_sheet(manifest_path: str, output: str, listener: str) -> None:
    """Create a listener-specific randomized sheet and private answer key."""

    clips = [
        json.loads(line)
        for line in Path(manifest_path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    clips = [
        clip
        for clip in clips
        if clip["condition"] in {"prosody_high", "prosody_low"}
        and clip["kind"] == "post_gap_observation"
    ]
    random.Random(hashlib.sha256(listener.encode()).hexdigest()).shuffle(clips)
    fieldnames = [
        "listener",
        "clip_id",
        "audio_path",
        "perceived_delivery_high_or_low",
        "confidence_1_to_5",
    ]
    with Path(output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, clip in enumerate(clips):
            writer.writerow(
                {
                    "listener": listener,
                    "clip_id": f"clip_{index:04d}",
                    "audio_path": clip["audio_path"],
                    "perceived_delivery_high_or_low": "",
                    "confidence_1_to_5": "",
                }
            )
    key_path = Path(output).with_suffix(".key.json")
    key_path.write_text(
        json.dumps(
            {
                f"clip_{index:04d}": clip["condition"].removeprefix("prosody_")
                for index, clip in enumerate(clips)
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {len(clips)} blinded clips -> {output}")
    print(f"Private scoring key -> {key_path}")


def report(paths: list[str]) -> None:
    """Score intended-delivery identification and cross-listener agreement."""

    if len(paths) < 2:
        raise SystemExit("At least two human listeners are required.")
    judgments = {}
    accuracies = []
    for path in paths:
        key = json.loads(Path(path).with_suffix(".key.json").read_text(encoding="utf-8"))
        with Path(path).open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if any(not row["perceived_delivery_high_or_low"].strip() for row in rows):
            raise SystemExit(f"{path} contains unrated clips.")
        listener = rows[0]["listener"]
        judgments[listener] = {
            row["audio_path"]: row["perceived_delivery_high_or_low"].strip().lower()
            for row in rows
        }
        accuracies.append(
            (
                listener,
                sum(
                    row["perceived_delivery_high_or_low"].strip().lower()
                    == key[row["clip_id"]]
                    for row in rows
                )
                / len(rows),
            )
        )
    for listener, accuracy in accuracies:
        print(f"{listener}: intended-prosody identification={accuracy:.1%}")
    names = list(judgments)
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            shared = judgments[left].keys() & judgments[right].keys()
            agreement = sum(
                judgments[left][clip] == judgments[right][clip] for clip in shared
            ) / len(shared)
            print(f"{left} vs {right}: raw agreement={agreement:.1%}")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "export" and len(sys.argv) == 5:
        export_sheet(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "report" and len(sys.argv) >= 4:
        report(sys.argv[2:])
    else:
        print(__doc__)
