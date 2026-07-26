"""Render individual user turns and prosodic-pair assets.

The closed-loop runner renders state-conditioned turns lazily. This command
pre-renders the gold-path assets and writes a manifest for inspection or human
prosody validation; it never creates a completed conversation WAV.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dual_audio.core.conditions import CONDITIONS, condition_turns, prosody_for
from dual_audio.core.environment import execute_action, post_gap_observation, transition
from dual_audio.modalities.audio import TurnAudioRenderer


def render_task(task: dict, condition_name: str, renderer: TurnAudioRenderer) -> list[dict]:
    """Render gold-path user turns for one task/condition manifest slice.

    Runtime evaluation still renders the observation resulting from the
    model-selected action. This helper uses the gold path only to prepare
    stable assets for inspection and human validation.
    """

    condition = CONDITIONS[condition_name]
    if condition.modality == "transcript":
        return []
    rows = []
    turns = condition_turns(task, condition)
    marker = next(
        i for i, turn in enumerate(turns) if turn["kind"] == "pre_gap_action"
    )
    presented = [
        turn for turn in turns[:marker] if turn["speaker"] == "user"
    ] + [turns[marker + 1]]
    for index, turn in enumerate(presented):
        path = renderer.render(turn["text"], "user", "neutral")
        rows.append(
            {
                "scenario_id": task["scenario_id"],
                "condition": condition_name,
                "turn_index": index,
                "kind": turn["kind"],
                "text": turn["text"],
                "prosody": "neutral",
                "audio_path": str(path),
            }
        )

    state = execute_action(
        task["domain"],
        task["initial_state"],
        task["pre_gap"]["correct_action"],
    )
    state = transition(
        task["domain"],
        state,
        task["pre_gap"]["correct_action"],
        task["transition"]["elapsed_minutes"],
        (
            task["transition"]["external_event"]
            if condition.apply_external_event
            else None
        ),
    )
    text = post_gap_observation(task["domain"], state)
    prosody, expected_style = prosody_for(task, condition)
    path = renderer.render(text, "user", prosody)
    rows.append(
        {
            "scenario_id": task["scenario_id"],
            "condition": condition_name,
            "turn_index": len(presented),
            "kind": "post_gap_observation",
            "text": text,
            "prosody": prosody,
            "expected_response_style": expected_style,
            "transcript_pair_id": (
                f"{task['scenario_id']}:post_gap"
                if condition_name in {"prosody_high", "prosody_low"}
                else None
            ),
            "audio_path": str(path),
        }
    )
    return rows


def main() -> None:
    """Pre-render selected audio conditions and write their JSONL manifest."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", default="data/scenarios")
    parser.add_argument("--out", default="data/turn_audio")
    parser.add_argument(
        "--conditions",
        default="full_audio,neutral_audio,prosody_high,prosody_low",
    )
    parser.add_argument("--only", default=None)
    args = parser.parse_args()

    condition_names = args.conditions.split(",")
    unknown = [name for name in condition_names if name not in CONDITIONS]
    if unknown:
        raise SystemExit(f"Unknown conditions: {unknown}")
    renderer = TurnAudioRenderer(args.out)
    rows = []
    for path in sorted(Path(args.scenarios).glob("*.json")):
        task = json.loads(path.read_text(encoding="utf-8"))
        if args.only and task["scenario_id"] != args.only:
            continue
        for condition_name in condition_names:
            rows.extend(render_task(task, condition_name, renderer))
    manifest = Path(args.out) / "manifest.jsonl"
    manifest.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Rendered {len(rows)} individual user turns -> {manifest}")


if __name__ == "__main__":
    main()
