"""Export and score an independent prosody audit on the scenario audit set.

Usage:
  python -m dual_audio.evaluation.gold_prosody_audit export \
      data/scenarios_v05 paper_results/v05/internal_audit annotator_01

  python -m dual_audio.evaluation.gold_prosody_audit report \
      paper_results/v05/internal_audit annotator_01
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sys
import wave
from collections import Counter
from pathlib import Path
from typing import Any

from dual_audio.core.conditions import CONDITIONS, prosody_for
from dual_audio.core.environment import execute_action, transition
from dual_audio.evaluation.audit_utils import (
    completed_gold_items,
    safe_slug,
    stable_rng,
)
from dual_audio.modalities.audio import TurnAudioRenderer
from dual_audio.users.scripted import ScriptedUserSimulator


RESPONSE_FIELDS = (
    "auditor",
    "audit_item_id",
    "more_intense_clip",
    "clip_a_tone",
    "clip_b_tone",
    "speech_clarity",
    "confidence_1_to_5",
    "notes",
)

TONE_OPTIONS = {"frustrated", "confused", "urgent", "confident", "calm", "unclear"}
INTENSITY_OPTIONS = {"A", "B", "SAME", "UNCLEAR"}
CLARITY_OPTIONS = {"both_clear", "only_a_clear", "only_b_clear", "neither_clear"}


def _gold_observation(task: dict, condition_name: str) -> tuple[str, str, str]:
    condition = CONDITIONS[condition_name]
    action = task["pre_gap"]["correct_action"]
    state = execute_action(task["domain"], task["initial_state"], action)
    state = transition(
        task["domain"],
        state,
        action,
        task["transition"]["elapsed_minutes"],
        task["transition"]["external_event"],
        None,
    )
    text = ScriptedUserSimulator().post_gap(task, state, condition)
    prosody, style = prosody_for(task, condition)
    if style is None:
        raise ValueError(f"{condition_name} must declare an expected style.")
    return text, prosody, style


def _duration_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / handle.getframerate()


def _render_or_reuse(
    renderer: TurnAudioRenderer,
    text: str,
    prosody: str,
    voice: str | None,
) -> Path:
    """Reuse an identical runtime stimulus before invoking local TTS."""

    resolved_voice = voice or "en-us+f3"
    filename = (
        hashlib.sha256(
            f"user|{resolved_voice}|{prosody}|{text}".encode("utf-8")
        ).hexdigest()[:24]
        + ".wav"
    )
    runtime_root = Path.cwd() / "data" / "runtime_audio"
    existing = sorted(runtime_root.glob(f"*/turns/{filename}"))
    if existing:
        return existing[0]
    return renderer.render(text, "user", prosody, voice=voice)


def export_packet(tasks_dir: str, audit_root: str, auditor: str) -> None:
    """Render two blinded post-gap clips per gold-set scenario."""

    root = Path(audit_root)
    output = root / "prosody"
    public = output / "public"
    private = output / "private"
    clips_dir = public / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    slug = safe_slug(auditor)
    gold_items = completed_gold_items(root, auditor)
    tasks = {
        task["scenario_id"]: task
        for path in sorted(Path(tasks_dir).glob("*.json"))
        for task in [json.loads(path.read_text(encoding="utf-8"))]
    }
    missing = {item["scenario_id"] for item in gold_items} - set(tasks)
    if missing:
        raise SystemExit(f"Gold scenarios missing from task directory: {sorted(missing)}")

    source_audio = output / "source_audio"
    renderer = TurnAudioRenderer(source_audio)
    items = list(gold_items)
    stable_rng(auditor, "prosody_item_order").shuffle(items)
    lines = [
        f"# DUAL-AudioBench independent prosody audit ({auditor})",
        "",
        "This packet contains one matched audio pair for each scenario in the",
        f"prespecified {len(items)}-scenario independent-audit set. The words and voice",
        "are identical within a pair; only pitch and speaking rate differ.",
        "Listen without opening the private key or scenario files.",
        "",
        "For each pair, answer four short questions in the response CSV:",
        "",
        "1. Which clip sounds more emotionally intense or urgent? Enter `A`, `B`, `same`, or `unclear`.",
        "2. What tone does each clip convey? Use `frustrated`, `confused`, `urgent`, `confident`, `calm`, or `unclear`.",
        "3. Is the speech clear? Use `both_clear`, `only_a_clear`, `only_b_clear`, or `neither_clear`.",
        "4. Rate confidence from 1 (guessing) to 5 (very sure).",
        "",
    ]
    key: dict[str, Any] = {
        "auditor": auditor,
        "gold_set_size": len(items),
        "selection": "both prosody variants for every completed independent-audit scenario",
        "items": {},
    }
    response_rows = []
    for index, gold in enumerate(items, start=1):
        item_id = f"PROSODY-{index:02d}"
        task = tasks[gold["scenario_id"]]
        rendered = {}
        for condition_name in ("prosody_high", "prosody_low"):
            text, prosody, style = _gold_observation(task, condition_name)
            source_path = _render_or_reuse(
                renderer,
                text,
                prosody,
                task.get("audio_profile", {}).get("user_voice"),
            )
            rendered[condition_name] = {
                "source_path": source_path,
                "text": text,
                "prosody": prosody,
                "expected_style": style,
            }
        if rendered["prosody_high"]["text"] != rendered["prosody_low"]["text"]:
            raise SystemExit(f"Prosody pair transcript mismatch: {gold['scenario_id']}")

        variants = ["prosody_high", "prosody_low"]
        stable_rng(auditor, gold["scenario_id"], "prosody_ab").shuffle(variants)
        public_variants = {}
        for letter, condition_name in zip(("A", "B"), variants):
            destination = clips_dir / f"{item_id}_{letter}.wav"
            shutil.copyfile(rendered[condition_name]["source_path"], destination)
            public_variants[letter] = {
                "condition": condition_name,
                "delivery": condition_name.removeprefix("prosody_"),
                "prosody": rendered[condition_name]["prosody"],
                "expected_style": rendered[condition_name]["expected_style"],
                "audio_path": str(destination.relative_to(public)),
                "duration_seconds": _duration_seconds(destination),
            }
        high_letter = next(
            letter
            for letter, item in public_variants.items()
            if item["delivery"] == "high"
        )
        lines.extend(
            [
                f"## Item {item_id}",
                "",
                f"- Clip A: [open audio]({public_variants['A']['audio_path'].replace(chr(92), '/')})",
                f"- Clip B: [open audio]({public_variants['B']['audio_path'].replace(chr(92), '/')})",
                "",
                "Record the stronger clip, both tones, speech clarity, and confidence.",
                "",
                "---",
                "",
            ]
        )
        response_rows.append(
            {
                field: auditor if field == "auditor" else item_id if field == "audit_item_id" else ""
                for field in RESPONSE_FIELDS
            }
        )
        key["items"][item_id] = {
            **gold,
            "transcript": rendered["prosody_high"]["text"],
            "variants": public_variants,
            "more_intense_clip": high_letter,
        }

    booklet_path = public / f"{slug}_prosody_booklet.md"
    responses_path = public / f"{slug}_prosody_responses.csv"
    key_path = private / f"{slug}_prosody_key.json"
    booklet_path.write_text("\n".join(lines), encoding="utf-8")
    with responses_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESPONSE_FIELDS)
        writer.writeheader()
        writer.writerows(response_rows)
    key_path.write_text(
        json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Exported {len(response_rows)} blinded prosody pairs -> {public}")
    print(f"Private scoring key -> {key_path}")


def _rating(row: dict[str, str], field: str) -> float:
    try:
        value = float(row[field])
    except (KeyError, ValueError) as exc:
        raise SystemExit(f"Invalid rating in {field}: {row.get(field)!r}") from exc
    if not 1 <= value <= 5:
        raise SystemExit(f"Rating outside 1--5 in {field}: {value}")
    return value


def report(audit_root: str, auditor: str) -> None:
    """Score the compact intensity, tone, and intelligibility judgments."""

    root = Path(audit_root) / "prosody"
    slug = safe_slug(auditor)
    key = json.loads(
        (root / "private" / f"{slug}_prosody_key.json").read_text(
            encoding="utf-8"
        )
    )
    reported_auditor = str(key.get("auditor", auditor))
    responses_path = root / "public" / f"{slug}_prosody_responses.csv"
    with responses_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = [field for field in RESPONSE_FIELDS if field != "notes"]
    if any(not row.get(field, "").strip() for row in rows for field in required):
        raise SystemExit("Prosody response sheet contains unrated fields.")
    if len(rows) != len(key["items"]):
        raise SystemExit("Prosody response count does not match private key.")

    category_total = 0
    category_correct = 0
    both_category = 0
    intensity_correct = 0
    intelligible_pairs = 0
    at_least_one_intelligible = 0
    confidence: list[float] = []
    category_confusion: Counter[tuple[str, str]] = Counter()
    for row in rows:
        item = key["items"].get(row["audit_item_id"])
        if item is None:
            raise SystemExit(f"Unknown prosody audit item: {row['audit_item_id']}")
        intensity = row["more_intense_clip"].strip().upper()
        if intensity not in INTENSITY_OPTIONS:
            raise SystemExit(f"Invalid more_intense_clip value: {intensity!r}")
        clarity = row["speech_clarity"].strip().lower()
        if clarity not in CLARITY_OPTIONS:
            raise SystemExit(f"Invalid speech_clarity value: {clarity!r}")
        item_category = 0
        for letter in ("A", "B"):
            variant = item["variants"][letter]
            category = row[f"clip_{letter.lower()}_tone"].strip().lower()
            if category not in TONE_OPTIONS:
                raise SystemExit(f"Invalid tone for clip {letter}: {category!r}")
            item_category += category == variant["prosody"]
            category_total += 1
            category_confusion[(variant["prosody"], category)] += 1
        category_correct += item_category
        both_category += item_category == 2
        intensity_correct += intensity == item["more_intense_clip"]
        intelligible_pairs += clarity == "both_clear"
        at_least_one_intelligible += clarity != "neither_clear"
        confidence.append(_rating(row, "confidence_1_to_5"))

    n = len(rows)
    metrics = {
        "auditor": reported_auditor,
        "n_pairs": n,
        "n_clips": 2 * n,
        "category_identification": category_correct / category_total,
        "both_categories_correct": both_category / n,
        "relative_intensity_accuracy": intensity_correct / n,
        "both_clips_clear": intelligible_pairs / n,
        "at_least_one_clip_clear": at_least_one_intelligible / n,
        "mean_confidence": sum(confidence) / len(confidence),
        "category_confusion": [
            {"intended": intended, "perceived": perceived, "n": count}
            for (intended, perceived), count in sorted(category_confusion.items())
        ],
    }
    lines = [
        "# Independent prosody audit report",
        "",
        f"- Auditor: {reported_auditor}",
        f"- Gold-set pairs: {n} ({2*n} clips)",
        f"- Relative-intensity accuracy: {metrics['relative_intensity_accuracy']:.1%}",
        f"- Intended-tone accuracy: {metrics['category_identification']:.1%}",
        f"- Both clips' tones correct: {metrics['both_categories_correct']:.1%}",
        f"- Both clips clear: {metrics['both_clips_clear']:.1%}",
        f"- Mean confidence: {metrics['mean_confidence']:.2f}/5",
        "",
        "This is an independent single-listener check, not inter-listener agreement.",
    ]
    (root / "prosody_audit_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    (root / "prosody_audit_metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Readable report -> {root / 'prosody_audit_report.md'}")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "export" and len(sys.argv) == 5:
        export_packet(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "report" and len(sys.argv) == 4:
        report(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
