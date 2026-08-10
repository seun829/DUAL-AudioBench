from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from run_eval import load_done


class ResumeTests(unittest.TestCase):
    def test_only_successful_same_schema_rows_are_reused(self):
        rows = [
            {
                "schema_version": "0.4",
                "scenario_id": "task_a_s04",
                "condition": "full_audio",
                "seed": 0,
                "error": None,
            },
            {
                "schema_version": "0.4",
                "scenario_id": "task_b_s04",
                "condition": "full_audio",
                "seed": 0,
                "error": "temporary failure",
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "resume.jsonl"
            path.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )
            self.assertEqual(
                load_done(path, "0.4"),
                {("task_a_s04", "full_audio", 0)},
            )

    def test_schema_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": "0.3",
                        "scenario_id": "old",
                        "condition": "full_audio",
                        "seed": 0,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "schema 0.3"):
                load_done(path, "0.4")


if __name__ == "__main__":
    unittest.main()
