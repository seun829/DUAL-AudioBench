# Implementation summary v2

This document covers the second benchmark extension: explicit probabilistic
hidden-state belief tracking and temporally separated hidden user actions. It
builds on the passive-to-agentic conversion documented in
`IMPLEMENTATION_SUMMARY.md`.

## Goals

The v2 extension distinguishes failures that action accuracy alone collapses:

| Belief | Action | Interpretation |
|---|---|---|
| Correct | Correct | Full success |
| Correct | Wrong | Action-selection failure |
| Wrong | Correct | Lucky action |
| Wrong | Wrong | State-synchronization failure |
| Uncertain | Non-verification action | Poor risk calibration |
| Uncertain | Revalidation action | Appropriate verification |

It also adds a dual-control condition in which the user takes an unobserved
tool action while the evaluated agent is unavailable.

## 1. Extended the agent response contract

Files:

- `dual_audio/core/types.py`
- `dual_audio/agents/replay.py`
- `dual_audio/agents/mock.py`

`Observation` now declares the state variables and allowed values the agent
must reason over. `AgentResponse` now carries:

```json
{
  "state_belief": {
    "firmware_status": {
      "not_started": 0.05,
      "updating": 0.05,
      "stuck": 0.80,
      "completed": 0.05,
      "interrupted": 0.05
    }
  },
  "needs_revalidation": false,
  "choice": "A"
}
```

The real-model adapter prompts for JSON-only probability distributions,
validates public labels, and normalizes valid state distributions. The mock
agent generates deterministic correct, incorrect, and uncertain beliefs for
pipeline testing.

## 2. Added three belief checkpoints

File:

- `dual_audio/interaction/runner.py`

Every trajectory now records:

1. `pre_gap`: belief reported with the pre-gap action;
2. `post_observation`: belief-only update immediately after the resumed user
   utterance;
3. `pre_final_action`: belief repeated with the final action.

The belief-only checkpoint cannot select an action. The resumed user audio is
added to history once, then replayed from history for the final decision. This
prevents the final model call from hearing a duplicated resumed utterance.

Missing or malformed belief distributions make belief reporting invalid. Full
trajectory success requires:

- correct pre-gap action;
- correct post-gap action;
- any required prosodic response style;
- valid belief reports at all checkpoints;
- correct top-state belief at all checkpoints.

The action-only trajectory result remains available separately as
`action_trajectory_success`.

## 3. Added belief validation and scoring

File:

- `dual_audio/core/beliefs.py`

For every task-declared variable, the evaluator:

- rejects unknown states and negative or non-finite probabilities;
- normalizes positive distributions;
- identifies the maximum-probability state;
- records probability assigned to ground truth;
- scores top-state correctness;
- computes multiclass Brier score;
- computes negative log likelihood;
- computes normalized entropy.

No uniform fallback is invented for missing reports. Such a fallback would
hide format failures and distort calibration.

## 4. Added belief-revision metrics

Files:

- `dual_audio/interaction/runner.py`
- `score.py`

Trajectory-level belief revision records:

- probability of the eventual post-gap state before the gap;
- probability of that state after resumed evidence;
- probability of that state immediately before the final action;
- evidence-driven revision gain;
- final revision gain;
- reflection-only gain between post-observation and pre-final checkpoints;
- probability mass remaining on the stale pre-gap state when state changed.

Aggregate reports include checkpoint accuracy, mean revision gain, and stale
belief persistence by experimental condition.

## 5. Added calibration metrics

File:

- `score.py`

The scorer now aggregates:

- mean Brier score;
- expected calibration error over top-state confidence;
- belief-report validity;
- `needs_revalidation` consistency with the configured confidence threshold.

Each task declares `belief_confidence_threshold`, currently `0.60`.

## 6. Added belief-action consistency

File:

- `dual_audio/interaction/runner.py`

For action checkpoints, the evaluator constructs a hypothetical state using
the model's maximum-probability state assignment. It then asks the executable
state policy which action that belief implies.

This produces:

- `implied_action_from_top_belief`;
- `action_belief_consistent`;
- `belief_action_outcome`;
- `uncertainty_behavior`.

The four belief/action outcome classes are reported directly. Low-confidence
choices are split into `UNCERTAIN_ACTED` and `UNCERTAIN_RECHECKED` using
task-declared `revalidation_actions`.

## 7. Added executable hidden user tools

Files:

- `dual_audio/core/environment.py`
- `scenarios/templates.py`
- `dual_audio/core/conditions.py`

`transition` now takes an optional fifth causal input:

```python
transition(
    current_state,
    agent_action,
    elapsed_minutes,
    external_event,
    user_action,
)
```

The user action has a task-defined timestamp that must fall within the elapsed
gap. It is applied before the external transition rule.

Implemented user tools:

- router: `power_cycle_during_maintenance`;
- pharmacy: `contact_plan_provider`;
- travel: `self_protect_onward_segment`.

These modify the same hidden world used by agent tools and external events.

## 8. Added the hidden-user-action condition

File:

- `dual_audio/core/conditions.py`

The main `full_audio` condition leaves the task's user action inactive. The
matched `hidden_user_action` condition activates it while preserving:

- pre-gap dialogue;
- model action menus and randomized order;
- elapsed time;
- external event;
- audio modality.

The resumed observation deterministically reports what the user did and the
resulting observable state. The correct final action is recomputed from that
state. For example, the travel user can protect the onward segment before the
departure delay, changing the connection from `missed` to `protected` and
changing the correct agent response.

## 9. Updated task and trajectory schemas

Files:

- `scenarios/generate.py`
- `data/scenarios/*.json`
- `run_eval.py`

The schema version is now `0.3`.

Task additions:

- `belief_schema`;
- `belief_confidence_threshold`;
- `revalidation_actions`;
- `transition.user_action`.

Trajectory additions:

- all three belief checkpoints;
- belief revision metrics;
- action-belief consistency;
- belief/action outcome classes;
- uncertainty behavior;
- belief-report and state-belief success;
- hidden user action;
- state snapshot immediately after the hidden user tool;
- belief-state-space chance fields.

The runner refuses to append v0.3 results to a pre-v0.3 JSONL file.

## 10. Updated chance baselines

File:

- `score.py`

The scorer distinguishes:

- one-action random chance (`1/5`);
- two-action random chance (`1/25`);
- full action-plus-belief chance, using the product of the task's belief-state
  space across three checkpoints;
- optional response-style chance for prosodic conditions.

This preserves interpretable action floors while reflecting the stricter
full-success definition.

## 11. Added tests

Files:

- `tests/test_beliefs.py`
- `tests/test_closed_loop.py`
- `tests/test_scoring.py`

New tests cover:

- distribution validation and normalization;
- top-state scoring;
- belief/action outcome interpretations;
- uncertain revalidation behavior;
- three checkpoint collection;
- positive belief revision after a state change;
- deterministic hidden user actions;
- hidden user actions changing state, observation, and answer;
- expected calibration error;
- belief-aware random chance.

## Validation status

At the time of this summary:

- 18 schema-v0.3 tasks generate successfully;
- all task menus still contain five choices;
- 16 focused unit tests pass;
- an 810-trajectory fake-agent run completes all nine conditions and five
  seeds;
- aggregate scoring prints belief accuracy, revision, stale persistence,
  Brier score, ECE, action-belief consistency, risk consistency, and the
  belief/action outcome matrix.

As before, the fake agent is only an orchestration fixture. Real-model
calibration results, human task solvability, independent failure annotation,
and perceptual prosody validation remain empirical work.
