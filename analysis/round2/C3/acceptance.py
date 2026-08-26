"""C3 acceptance: existing conditions must be byte-identical after the patch.

Runs MockAgent over every pre-existing condition and writes a canonical JSON
dump with the fields that legitimately vary between runs removed: the wall-clock
timestamp, latency, and the two fields C3 itself adds.  Run once on the
pre-patch tree and once after, then diff.

MockAgent is deterministic (seeded from scenario id, seed and stage), and the
runner is a pure function of task, condition and seed, so any difference in this
dump is a real behavioural change.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from dual_audio.agents import MockAgent
from dual_audio.core.conditions import CONDITIONS
from dual_audio.interaction import ClosedLoopRunner

VOLATILE = {"timestamp", "latency_s", "oracle_state_text", "belief_elicited"}
PRE_EXISTING = [
    "full_audio",
    "gap_no_state_change",
    "state_change_short",
    "clue_removed",
    "transcript_only",
    "neutral_audio",
    "hidden_user_action",
    "prosody_high",
    "prosody_low",
]
# A spread of domains, buckets and both branches, kept small so this runs fast.
PICKS = [
    "flight_1to2_b0_s05",
    "flight_1to2_b1_s05",
    "router_5to8_b0_s05",
    "pharmacy_12to20_b1_s05",
    "bank_12to20_b0_s05",
    "tenancy_5to8_b1_s05",
]


def strip(obj):
    if isinstance(obj, dict):
        return {k: strip(v) for k, v in obj.items() if k not in VOLATILE}
    if isinstance(obj, list):
        return [strip(v) for v in obj]
    return obj


def main() -> None:
    label = sys.argv[1]
    scen_dir = ROOT / "data" / "scenarios_v05"
    runner = ClosedLoopRunner(audio_renderer=None)
    out = {}
    for sid in PICKS:
        task = json.loads((scen_dir / (sid + ".json")).read_text(encoding="utf-8"))
        for cond in PRE_EXISTING:
            for seed in (0, 1):
                traj = runner.execute(
                    agent=MockAgent(),
                    task=task,
                    condition=CONDITIONS[cond],
                    seed=seed,
                )
                out["%s|%s|%d" % (sid, cond, seed)] = strip(traj)
    path = Path(__file__).resolve().parent / (label + ".json")
    path.write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8"
    )
    print("wrote %d trajectories -> %s" % (len(out), path.name))


if __name__ == "__main__":
    main()
