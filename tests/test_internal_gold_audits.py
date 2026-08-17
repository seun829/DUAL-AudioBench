from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from dual_audio.evaluation.audit_utils import completed_gold_items
from dual_audio.evaluation.failure_tag_audit import (
    RESPONSE_FIELDS as FAILURE_FIELDS,
    _select_trajectories,
    report as failure_report,
)
from dual_audio.evaluation.gold_prosody_audit import (
    RESPONSE_FIELDS as PROSODY_FIELDS,
    report as prosody_report,
)


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class InternalGoldAuditTests(unittest.TestCase):
    def test_completed_gold_items_uses_two_phase_intersection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "private").mkdir()
            key = {
                "scenario_manifest_sha256": "freeze",
                "items": {
                    "A-01": {
                        "scenario_id": "scenario_1",
                        "causal_pair_id": "pair_1",
                        "causal_branch": "aligned",
                    },
                    "A-02": {
                        "scenario_id": "scenario_2",
                        "causal_pair_id": "pair_2",
                        "causal_branch": "misaligned",
                    },
                    "A-03": {
                        "scenario_id": "scenario_3",
                        "causal_pair_id": "pair_3",
                        "causal_branch": "aligned",
                    },
                },
            }
            (root / "private" / "author_01_key.json").write_text(
                json.dumps(key), encoding="utf-8"
            )
            pre_fields = (
                "audit_item_id",
                "pre_action_label",
                "causal_alignment",
                "answerable_yes_no",
            )
            post_fields = (
                "audit_item_id",
                "terminal_state",
                "post_action_label",
                "answerable_yes_no",
            )
            _write_csv(
                root / "public" / "author_01_phase1_responses.csv",
                pre_fields,
                [
                    {"audit_item_id": item, "pre_action_label": "A", "causal_alignment": "aligned", "answerable_yes_no": "yes"}
                    for item in ("A-01", "A-02", "A-03")
                ],
            )
            _write_csv(
                root / "public" / "author_01_phase2_responses.csv",
                post_fields,
                [
                    {"audit_item_id": item, "terminal_state": "done", "post_action_label": "B", "answerable_yes_no": "yes"}
                    for item in ("A-01", "A-02")
                ]
                + [
                    {"audit_item_id": "A-03", "terminal_state": "", "post_action_label": "", "answerable_yes_no": ""}
                ],
            )
            items = completed_gold_items(root, "author_01")
            self.assertEqual(
                [item["scenario_id"] for item in items],
                ["scenario_1", "scenario_2"],
            )

    def test_failure_selection_uses_every_gold_scenario_once(self):
        gold = [
            {"scenario_id": f"scenario_{index}"} for index in range(1, 5)
        ]
        candidates = []
        for item in gold:
            for model in ("model_a", "model_b"):
                candidates.append(
                    {
                        "scenario_id": item["scenario_id"],
                        "model": model,
                        "condition": "full_audio",
                        "failure_tags": "STATE_BELIEF_ERROR",
                    }
                )
        selected = _select_trajectories(gold, candidates, "author_01")
        self.assertEqual(len(selected), 4)
        self.assertEqual(
            {row["scenario_id"] for row in selected},
            {item["scenario_id"] for item in gold},
        )

    def test_one_author_failure_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "failure_tags"
            (root / "private").mkdir(parents=True)
            key = {
                "tag_definitions": {
                    "STATE_BELIEF_ERROR": "wrong state",
                    "EARLY_CLUE_LOSS": "lost clue",
                },
                "items": {
                    "FAILURE-01": {"automatic_tags": ["STATE_BELIEF_ERROR"]},
                    "FAILURE-02": {"automatic_tags": ["EARLY_CLUE_LOSS"]},
                },
            }
            (root / "private" / "author_01_failure_tag_key.json").write_text(
                json.dumps(key), encoding="utf-8"
            )
            _write_csv(
                root / "public" / "author_01_failure_tag_responses.csv",
                FAILURE_FIELDS,
                [
                    {
                        "auditor": "author_01",
                        "audit_item_id": "FAILURE-01",
                        "labels_semicolon_separated": "STATE_BELIEF_ERROR",
                        "evidence_or_reason": "top state is wrong",
                        "confidence_1_to_5": "5",
                        "notes": "",
                    },
                    {
                        "auditor": "author_01",
                        "audit_item_id": "FAILURE-02",
                        "labels_semicolon_separated": "NONE",
                        "evidence_or_reason": "not supported",
                        "confidence_1_to_5": "4",
                        "notes": "",
                    },
                ],
            )
            failure_report(str(Path(directory)), "author_01")
            metrics = json.loads(
                (root / "failure_tag_audit_metrics.json").read_text(encoding="utf-8")
            )
            self.assertEqual(metrics["n"], 2)
            self.assertEqual(metrics["micro_precision"], 0.5)

    def test_one_author_prosody_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "prosody"
            (root / "private").mkdir(parents=True)
            key = {
                "items": {
                    "PROSODY-01": {
                        "more_intense_clip": "A",
                        "variants": {
                            "A": {
                                "delivery": "high",
                                "prosody": "urgent",
                                "expected_style": "acknowledge_urgency",
                            },
                            "B": {
                                "delivery": "low",
                                "prosody": "calm",
                                "expected_style": "proceed_directly",
                            },
                        },
                    }
                }
            }
            (root / "private" / "author_01_prosody_key.json").write_text(
                json.dumps(key), encoding="utf-8"
            )
            row = {field: "" for field in PROSODY_FIELDS}
            row.update(
                {
                    "auditor": "author_01",
                    "audit_item_id": "PROSODY-01",
                    "more_intense_clip": "A",
                    "clip_a_tone": "urgent",
                    "clip_b_tone": "calm",
                    "speech_clarity": "both_clear",
                    "confidence_1_to_5": "5",
                }
            )
            _write_csv(
                root / "public" / "author_01_prosody_responses.csv",
                PROSODY_FIELDS,
                [row],
            )
            prosody_report(str(Path(directory)), "author_01")
            metrics = json.loads(
                (root / "prosody_audit_metrics.json").read_text(encoding="utf-8")
            )
            self.assertEqual(metrics["n_pairs"], 1)
            self.assertEqual(metrics["relative_intensity_accuracy"], 1.0)
            self.assertEqual(metrics["category_identification"], 1.0)
            self.assertEqual(metrics["both_clips_clear"], 1.0)


if __name__ == "__main__":
    unittest.main()
