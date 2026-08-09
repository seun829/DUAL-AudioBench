"""Regression tests for structured-reply parsing in the replay adapter.

A hosted model frequently wraps the requested JSON object in a Markdown fence.
In the 2026-07-30 Gemini pilot, 81 of 162 decision replies (50%) parsed only
after fence handling was added, and every one of them carried a genuinely valid
belief distribution. Without it those distributions are discarded and the
belief metrics -- the pilot's headline result -- become meaningless.

The contract these tests lock in:

* well-formed JSON parses whether it is bare, fenced, or fenced with a language
  tag and surrounding prose;
* genuinely malformed JSON is reported invalid, and specifically is **not**
  back-filled with an invented uniform distribution.
"""

from __future__ import annotations

import unittest

from dual_audio.agents.replay import _extract_label, _parse_json
from dual_audio.core.beliefs import normalize_state_belief


SCHEMA = {"claim_status": ("not_submitted", "processing", "rejected", "approved")}
BELIEF = {
    "claim_status": {
        "not_submitted": 0.9,
        "processing": 0.05,
        "rejected": 0.025,
        "approved": 0.025,
    }
}
EXPECTED = {"state_belief": BELIEF, "needs_revalidation": False, "choice": "D"}

BARE = (
    '{"state_belief": {"claim_status": {"not_submitted": 0.9, "processing": 0.05,'
    ' "rejected": 0.025, "approved": 0.025}}, "needs_revalidation": false,'
    ' "choice": "D"}'
)
FENCED = f"```\n{BARE}\n```"
FENCED_TAGGED_WITH_PROSE = (
    "Here is my assessment of the hidden state.\n\n"
    f"```json\n{BARE}\n```\n\n"
    "Let me know if you would like me to re-verify the claim."
)
# Verbatim failure shape observed in the pilot: a stray quote closes the object
# early, so no balanced JSON object exists anywhere in the reply.
MALFORMED = (
    '```json\n{\n  "state_belief": {\n    "claim_status": {\n'
    '      "not_submitted": 1,\n      "processing": 0,\n'
    '      "rejected": 0,\n      "approved": 0\n    }\n  ",\n'
    '  "needs_revalidation": false,\n  "choice": "E"\n}\n```'
)


class ResponseParsingTests(unittest.TestCase):
    def test_bare_json_parses(self):
        self.assertEqual(_parse_json(BARE), EXPECTED)

    def test_fenced_json_parses(self):
        self.assertEqual(_parse_json(FENCED), EXPECTED)

    def test_fenced_with_language_tag_and_trailing_text_parses(self):
        self.assertEqual(_parse_json(FENCED_TAGGED_WITH_PROSE), EXPECTED)

    def test_every_well_formed_shape_yields_the_same_valid_belief(self):
        """Presentation must not change the scored distribution."""

        for name, raw in (
            ("bare", BARE),
            ("fenced", FENCED),
            ("fenced+prose", FENCED_TAGGED_WITH_PROSE),
        ):
            with self.subTest(shape=name):
                belief = normalize_state_belief(
                    _parse_json(raw).get("state_belief"), SCHEMA
                )
                self.assertEqual(
                    belief["claim_status"]["not_submitted"], 0.9, name
                )
                self.assertEqual(
                    _extract_label(raw, _parse_json(raw), "choice", set("ABCDE")),
                    "D",
                )

    def test_malformed_json_is_flagged_invalid_not_back_filled(self):
        """Malformed input must fail loudly rather than gain invented mass.

        The bug class guarded here is a fabricated belief: if a parse failure
        were back-filled with a uniform distribution, the row would look like a
        confident, valid report while carrying no model evidence at all.
        """

        parsed = _parse_json(MALFORMED)
        self.assertEqual(parsed, {})

        belief = normalize_state_belief(parsed.get("state_belief"), SCHEMA)
        self.assertEqual(belief, {}, "malformed reply must yield no distribution")

        uniform = 1 / len(SCHEMA["claim_status"])
        self.assertNotEqual(
            belief,
            {"claim_status": {value: uniform for value in SCHEMA["claim_status"]}},
            "parse failure must not be back-filled with a uniform distribution",
        )

    def test_partial_and_out_of_schema_beliefs_stay_invalid(self):
        """Fence recovery must not weaken schema validation."""

        # Parses as JSON, but the values are not the declared state values.
        off_schema = '```json\n{"state_belief": {"claim_status": {"paid": 1.0}}}\n```'
        self.assertEqual(
            normalize_state_belief(
                _parse_json(off_schema).get("state_belief"), SCHEMA
            ),
            {},
        )

        # Parses, in schema, but carries zero total mass.
        zero_mass = (
            '```json\n{"state_belief": {"claim_status": {"not_submitted": 0,'
            ' "processing": 0, "rejected": 0, "approved": 0}}}\n```'
        )
        self.assertEqual(
            normalize_state_belief(
                _parse_json(zero_mass).get("state_belief"), SCHEMA
            ),
            {},
        )

    def test_action_label_fallback_is_documented_behaviour(self):
        """Record that a label is still read from prose when JSON fails.

        ``_extract_label`` falls back to a word-boundary search of the raw
        reply, so a malformed reply can still yield an action. On the pilot's
        six malformed replies this recovered the stated choice correctly every
        time, and the accompanying belief was still flagged invalid -- so the
        row stays auditable. This test exists so the behaviour cannot change
        unnoticed, since it is the one path where a parse failure does not
        surface in the trajectory.
        """

        self.assertEqual(
            _extract_label(MALFORMED, {}, "choice", set("ABCDE")), "E"
        )
        # A reply with no permitted label must yield None rather than a guess.
        self.assertIsNone(
            _extract_label("I cannot determine the state.", {}, "choice", set("ABCDE"))
        )


if __name__ == "__main__":
    unittest.main()
