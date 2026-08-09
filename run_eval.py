"""Run the alternating-turn, closed-loop DUAL-AudioBench evaluation.

Each JSONL row is a complete trajectory:

    scripted user audio -> evaluated agent dialogue turns
    -> evaluated pre-gap action -> tool execution -> deterministic time update
    -> state-conditioned user audio -> evaluated post-gap action -> scoring

The old one-completed-WAV action classifier is intentionally not exposed as a
benchmark mode. ``transcript_only`` is available as an explicit control.
"""

from __future__ import annotations

import argparse
import importlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from dual_audio.agents import MockAgent, ReplayModelAgent
from dual_audio.core.conditions import CONDITIONS, CONTROL_CONDITIONS
from dual_audio.interaction import ClosedLoopRunner
from dual_audio.modalities.audio import TurnAudioRenderer


def get_agent(name: str):
    """Construct the normalized agent selected by the CLI."""

    if name == "fake":
        return MockAgent()
    modules = {
        "gemini": "models.gemini_live",
        "qwen": "models.qwen_omni",
        "openrouter": "models.openrouter",
    }
    if name not in modules:
        raise ValueError(name)
    return ReplayModelAgent(importlib.import_module(modules[name]))


def parse_conditions(value: str) -> list[str]:
    """Expand ``all`` or validate a comma-separated condition list."""

    names = list(CONTROL_CONDITIONS) if value == "all" else value.split(",")
    unknown = [name for name in names if name not in CONDITIONS]
    if unknown:
        raise ValueError(
            f"Unknown conditions {unknown}; choose from {list(CONDITIONS)} or all"
        )
    return names


def load_done(path: Path) -> set[tuple[str, str, int]]:
    """Return successful trajectory keys already checkpointed in ``path``.

    Error rows are deliberately excluded so a later invocation retries them.
    """

    done = set()
    if not path.exists():
        return done
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("schema_version") != "0.3":
            raise ValueError(
                f"{path} contains pre-v0.3 trajectories; choose a new output "
                "path before running the belief-tracking benchmark."
            )
        if not row.get("error"):
            done.add((row["scenario_id"], row["condition"], row["seed"]))
    return done


def main() -> None:
    """Run the crash-resumable task x condition x seed evaluation batch."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        choices=["fake", "gemini", "qwen", "openrouter"],
        required=True,
    )
    parser.add_argument("--scenarios", default="data/scenarios")
    parser.add_argument(
        "--conditions",
        default="full_audio",
        help="comma-separated condition names, or 'all'",
    )
    parser.add_argument("--passes", type=int, default=5)
    parser.add_argument("--out", default=None)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--rate-limit-seconds", type=float, default=1.0)
    parser.add_argument(
        "--render-fake-audio",
        action="store_true",
        help="exercise local TTS even though MockAgent does not need it",
    )
    args = parser.parse_args()

    condition_names = parse_conditions(args.conditions)
    tasks = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(Path(args.scenarios).glob("*.json"))
    ]
    for task in tasks:
        if task.get("schema_version") != "0.3":
            raise SystemExit(
                f"{task.get('scenario_id')} is not schema 0.3; regenerate tasks "
                "with `python scenarios/generate.py`."
            )

    output = Path(args.out or f"results/{args.model}_closed_loop.jsonl")
    output.parent.mkdir(parents=True, exist_ok=True)
    done = load_done(output)
    agent = get_agent(args.model)
    needs_audio = args.model != "fake" or args.render_fake_audio
    renderer = TurnAudioRenderer() if needs_audio else None
    runner = ClosedLoopRunner(audio_renderer=renderer)
    print(
        f"[{args.model}/closed_loop] {len(done)} trajectories logged; "
        f"conditions={condition_names}"
    )

    with output.open("a", encoding="utf-8") as log:
        for task in tasks:
            for condition_name in condition_names:
                condition = CONDITIONS[condition_name]
                for seed in range(args.passes):
                    key = (task["scenario_id"], condition_name, seed)
                    if key in done:
                        continue
                    started = time.time()
                    trajectory = None
                    error = None
                    for attempt in range(args.retries + 1):
                        try:
                            trajectory = runner.execute(
                                agent=agent,
                                task=task,
                                condition=condition,
                                seed=seed,
                            )
                            break
                        except Exception as exc:  # preserve a checkpoint on failures
                            error = repr(exc)
                            if attempt < args.retries:
                                time.sleep(min(2**attempt, 8))
                    failed = trajectory is None
                    if trajectory is None:
                        trajectory = {
                            "schema_version": "0.3",
                            "scenario_id": task["scenario_id"],
                            "domain": task["domain"],
                            "bucket": task["bucket"],
                            "condition": condition_name,
                            "seed": seed,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "trajectory_success": False,
                            "error": error,
                        }
                    trajectory["model"] = args.model
                    trajectory["latency_s"] = round(time.time() - started, 3)
                    trajectory["error"] = error if failed else None
                    log.write(json.dumps(trajectory, ensure_ascii=False) + "\n")
                    log.flush()
                    status = (
                        "ERR"
                        if trajectory.get("error")
                        else "pass"
                        if trajectory["trajectory_success"]
                        else "fail"
                    )
                    print(
                        f"{status:<4} {task['scenario_id']}/{condition_name}/seed={seed}"
                    )
                    if args.model != "fake" and args.rate_limit_seconds:
                        time.sleep(args.rate_limit_seconds)
    print(f"Done -> {output}")


if __name__ == "__main__":
    main()
