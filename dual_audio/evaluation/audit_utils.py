"""Shared helpers for blinded internal audit packets."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from pathlib import Path


def safe_slug(value: str) -> str:
    """Return a stable filesystem-safe identifier."""

    slug = "".join(character if character.isalnum() else "_" for character in value)
    return slug.strip("_").lower() or "auditor"


def stable_rng(*parts: object) -> random.Random:
    """Return a deterministic random generator for an audit operation."""

    digest = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return random.Random(digest)


def completed_gold_items(audit_root: str | Path, auditor: str) -> list[dict]:
    """Load the scenarios completed in both phases of one scenario audit.

    The completed intersection is the prespecified author gold set. Item order
    follows the private key so later audit packets are deterministic.
    """

    root = Path(audit_root)
    slug = safe_slug(auditor)
    key_path = root / "private" / f"{slug}_key.json"
    phase1_path = root / "public" / f"{slug}_phase1_responses.csv"
    phase2_path = root / "public" / f"{slug}_phase2_responses.csv"
    key = json.loads(key_path.read_text(encoding="utf-8"))

    def completed_ids(path: Path, required: tuple[str, ...]) -> set[str]:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return {
            row["audit_item_id"]
            for row in rows
            if row.get("audit_item_id")
            and all(row.get(field, "").strip() for field in required)
        }

    phase1 = completed_ids(
        phase1_path,
        ("pre_action_label", "causal_alignment", "answerable_yes_no"),
    )
    phase2 = completed_ids(
        phase2_path,
        ("terminal_state", "post_action_label", "answerable_yes_no"),
    )
    completed = phase1 & phase2
    if not completed:
        raise SystemExit(f"No completed two-phase gold items found for {auditor}.")

    items = []
    for item_id, item in key["items"].items():
        if item_id in completed:
            items.append(
                {
                    "source_audit_item_id": item_id,
                    "scenario_id": item["scenario_id"],
                    "causal_pair_id": item["causal_pair_id"],
                    "causal_branch": item["causal_branch"],
                    "scenario_manifest_sha256": key.get(
                        "scenario_manifest_sha256"
                    ),
                }
            )
    return items
