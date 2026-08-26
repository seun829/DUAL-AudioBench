# C3. The `oracle_state` condition

## Change

Additive only, four files, `dual_audio/core/environment.py` untouched.

| File | Change |
|---|---|
| `dual_audio/core/conditions.py` | `Condition` gains `elicit_belief: bool = True` and `oracle_state: bool = False`; one new `CONDITIONS` entry |
| `dual_audio/core/types.py` | `Observation` gains `oracle_state_text: str = ""` |
| `dual_audio/interaction/runner.py` | checkpoint-1 call gated on `condition.elicit_belief`; oracle sentence built from the realized state via `definitions_for`; two new logged fields (`oracle_state_text`, `belief_elicited`) |
| `dual_audio/agents/replay.py` | `_decision_prompt` prepends the oracle sentence and drops the belief request |

The prompt change removes `state_belief` and `needs_revalidation` from the JSON
example as well as from the instruction text, because
`models/openrouter.py:193` derives the enforced `response_format` from that
example. Verified: the derived schema for an oracle prompt is
`{"choice": <enum A-E>}` with `additionalProperties: false`.

## Acceptance: existing conditions are byte-identical

`acceptance.py` runs MockAgent over 108 trajectories (6 scenarios x 9
pre-existing conditions x 2 seeds) and dumps every trajectory with only the
wall-clock timestamp, latency, and the two fields C3 adds removed. MockAgent is
seeded from scenario id, seed and stage, and the runner is a pure function of
task, condition and seed, so any difference would be a real behavioural change.

```
before sha256: 39891860e2c6f749003c0820a3e43be92559e652782801b438545ff64b05d1e1
after  sha256: 39891860e2c6f749003c0820a3e43be92559e652782801b438545ff64b05d1e1
BYTE-IDENTICAL: True
```

## Scoring note

Score `post_gap_success` only. `belief_reporting_success` is false by
construction under this condition because no belief is elicited, which forces
`trajectory_success` false; the strict composite is meaningless here.
