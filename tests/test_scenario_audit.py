from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from dual_audio.evaluation.scenario_audit import export_packet, report


def _complete_with_private_gold(root: Path, auditor: str) -> None:
    key = json.loads(
        (root / "private" / f"{auditor}_key.json").read_text(encoding="utf-8")
    )
    paths = {
        "phase1": root / "public" / f"{auditor}_phase1_responses.csv",
        "phase2": root / "public" / f"{auditor}_phase2_responses.csv",
    }
    for phase, path in paths.items():
        with path.open(encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fields = list(reader.fieldnames or [])
            rows = list(reader)
        for row in rows:
            gold = key["items"][row["audit_item_id"]]
            if phase == "phase1":
                row["pre_action_label"] = gold["gold_pre_action_label"]
                row["causal_alignment"] = gold["gold_causal_alignment"]
            else:
                row["terminal_state"] = gold["gold_terminal_state"]
                row["post_action_label"] = gold["gold_post_action_label"]
            row["answerable_yes_no"] = "yes"
            row["ambiguity_1_to_5"] = "1"
            row["evidence_turn_or_reason"] = "causal rule and clue"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)


class ScenarioAuditTests(unittest.TestCase):
    def test_export_is_blinded_balanced_and_two_phase(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            export_packet("data/scenarios_v05", str(root), "auditor_a")
            export_packet("data/scenarios_v05", str(root), "auditor_b")
            key_a = json.loads(
                (root / "private" / "auditor_a_key.json").read_text(
                    encoding="utf-8"
                )
            )
            key_b = json.loads(
                (root / "private" / "auditor_b_key.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(len(key_a["items"]), 84)
            self.assertEqual(len(key_b["items"]), 84)
            pairs = [item["causal_pair_id"] for item in key_a["items"].values()]
            self.assertTrue(all(left != right for left, right in zip(pairs, pairs[1:])))
            self.assertNotEqual(
                [item["scenario_id"] for item in key_a["items"].values()],
                [item["scenario_id"] for item in key_b["items"].values()],
            )
            phase1 = (
                root / "public" / "auditor_a_phase1_booklet.md"
            ).read_text(encoding="utf-8")
            phase2 = (
                root / "public" / "auditor_a_phase2_booklet.md"
            ).read_text(encoding="utf-8")
            self.assertNotIn("Operation assumed executed", phase1)
            self.assertIn("Operation assumed executed", phase2)
            self.assertNotIn("scenario_id", phase1)
            self.assertNotIn("gold_", phase1)
            with (root / "public" / "auditor_a_phase1_responses.csv").open(
                encoding="utf-8"
            ) as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 84)

    def test_completed_gold_packets_score_and_agree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for auditor in ("auditor_a", "auditor_b"):
                export_packet("data/scenarios_v05", str(root), auditor)
                _complete_with_private_gold(root, auditor)
            report(str(root), ["auditor_a", "auditor_b"])
            text = (root / "internal_audit_report.md").read_text(encoding="utf-8")
            self.assertIn("Pre-gap action accuracy: 100.0%", text)
            self.assertIn("Post-gap action accuracy: 100.0%", text)
            self.assertIn("auditor_a vs auditor_b, terminal_state: 100.0%", text)
            with (root / "adjudication.csv").open(encoding="utf-8") as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 0)


if __name__ == "__main__":
    unittest.main()
