# Closed-loop implementation summary

This document summarizes the code changes made while converting
DUAL-AudioBench from a passive completed-audio action classifier into a
closed-loop, alternating-turn benchmark.

## Starting point

The original pipeline:

- synthesized one WAV containing scripted user turns, scripted agent turns,
  the fast-forward marker, and the resumed user turn;
- made one model call after the entire recording;
- stored the post-gap state directly as scenario metadata;
- exposed canonical action names in a sorted menu;
- used single-label failure traps;
- generated one prosodic delivery per scenario;
- lacked matched causal controls;
- trusted a sampled clue-distance field;
- plotted a `1/6` chance floor despite five-option menus;
- emphasized pass@5 over repeated-run reliability.

That system tested next-action classification from recorded context. The
evaluated model did not cause the state transition.

## 1. Added a normalized agent interface

Files:

- `dual_audio/core/types.py`
- `dual_audio/agents/base.py`
- `dual_audio/agents/replay.py`
- `dual_audio/agents/mock.py`

`Observation` and `AgentResponse` now define the data exchanged at each turn.
All real model modules are wrapped behind:

```python
agent.respond(observation, history) -> AgentResponse
```

The replay adapter builds accumulated alternating-turn audio from actual model
responses. It also supports the transcript-only control and parses randomized
public option labels from structured JSON.

## 2. Added executable tools and transitions

File:

- `dual_audio/core/environment.py`

The benchmark now has separate functions for:

- executing the selected symbolic action;
- advancing time and applying an external event;
- deriving the correct action from current state;
- generating a user observation from current state.

Transitions deep-copy their inputs. Scenario JSON stores transition inputs,
not a precomputed post-gap answer.

## 3. Added the closed-loop runner

File:

- `dual_audio/interaction/runner.py`

The runner now:

1. initializes task state;
2. alternates scripted user turns with evaluated model responses;
3. collects the model's pre-gap action;
4. executes that action;
5. advances time through the deterministic transition;
6. produces a state-conditioned resumed observation;
7. collects and scores the post-gap action;
8. writes the whole trajectory.

If the pre-gap action is wrong, the later state, observation, and state-based
answer can change.

## 4. Replaced static scenario updates with schema-v0.2 tasks

Files:

- `scenarios/templates.py`
- `scenarios/generate.py`
- `data/scenarios/*.json`

Templates now define:

- initial state;
- symbolic actions and public descriptions;
- transition inputs;
- clue-ablation utterances;
- response-style options;
- contrastive prosody metadata.

The generated scenarios do not contain `state_update`.

## 5. Corrected clue-distance generation

The generator now calculates distance from the completed turn sequence:

```python
actual_distance = len(turns) - clue_index - 1
assert actual_distance == target_distance
```

The distance definition includes the evaluated pre-gap action and user
acknowledgement. This makes 2 the minimum feasible distance and resolves the
incompatibility between alternating turns and a claimed distance of 1.

## 6. Added matched controls

File:

- `dual_audio/core/conditions.py`

Implemented controls:

- full audio;
- gap without external state change;
- state change with a short clue distance;
- early-clue ablation;
- transcript only;
- neutral audio;
- high- and low-prosody identical-transcript pairs.

Paired runs reuse the same menu and option order.

## 7. Reduced action-choice leakage

Canonical action names are no longer shown to the model. Each run:

- shuffles descriptions deterministically;
- assigns public labels `A` through `E`;
- holds the mapping fixed across paired controls;
- checks whether only the correct description repeats clue content.

The scorer compares full and clue-removed performance and warns when the
difference is too small.

## 8. Added genuine prosodic pairs

Files:

- `dual_audio/core/conditions.py`
- `dual_audio/modalities/audio.py`
- `audio/tts.py`
- `dual_audio/evaluation/prosody_validation.py`

Prosodic conditions keep the resumed transcript and technical decision
identical while changing audible delivery and the expected secondary response
approach. A blinded listener-sheet workflow was added so audibility can be
validated rather than assumed.

## 9. Redesigned failure tags

Files:

- `scenarios/templates.py`
- `dual_audio/evaluation/annotations.py`

Actions now store zero or more failure tags. This permits cases such as a
restart being both a repeated action and a clue-loss failure. Independent
annotation sheets and pairwise agreement reporting were added.

## 10. Corrected scoring

File:

- `score.py`

The scorer now reports:

- trajectory pass@1;
- pre-gap and post-gap action accuracy;
- scenario-level majority accuracy;
- variance across seeds;
- clustered bootstrap confidence intervals;
- success on every repeated trial;
- supplemental pass@5;
- paired control effects;
- multilabel failure counts.

Chance is calculated from logged menu sizes. With five choices, one action has
a 20% chance floor; two required actions have a 4% trajectory floor.

## 11. Changed audio orchestration

Files:

- `dual_audio/modalities/audio.py`
- `audio/tts.py`

The benchmark renders individual turns and replay WAVs instead of a single
completed conversation recording. The audio CLI also produces a manifest for
human validation.

## 12. Standardized model use

Files:

- `models/gemini_live.py`
- `models/qwen_omni.py`
- `models/fake.py`

Gemini and Qwen expose audio and transcript inference functions consumed by
the shared replay adapter. The fake model is now an explicitly oracle-backed,
deterministic test fixture.

## 13. Replaced the passive evaluator

File:

- `run_eval.py`

The public evaluation CLI now runs complete closed-loop trajectories. It
supports:

- condition selection;
- repeated deterministic seeds;
- retry handling;
- per-trajectory JSONL checkpointing;
- resume support;
- rate limiting.

The old completed-WAV action mode is not exposed as the main benchmark.

## 14. Added focused tests

Files:

- `tests/test_closed_loop.py`
- `tests/test_scoring.py`

Tests cover:

- exact clue-distance calculation;
- alternating speaker order;
- clue-ablation turn matching;
- transition determinism;
- action-dependent state changes;
- no-state-change behavior;
- closed-loop pre-gap action control;
- dynamic state-based post-gap answers;
- paired menu ordering;
- identical-transcript prosodic pairs;
- dynamic 1/5 and 1/25 chance calculations.

## Validation performed

The implementation was validated with:

- 10 passing unit tests;
- 18 regenerated tasks;
- five-choice menus at both decision stages;
- no hard-coded `state_update` in generated tasks;
- a 720-trajectory fake-agent run spanning all controls.

Audio rendering could not be executed in the development environment because
`espeak-ng` was unavailable. The code path is documented and compile-checked,
but perceptual validation remains a required external experiment.
