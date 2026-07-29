# DUAL-AudioBench

DUAL-AudioBench is a **turn-based, audio-conditioned agent benchmark** for
long-horizon conversational state tracking. The evaluated model participates
in the interaction, chooses an action before a time gap, and must recover after
its action and an external event change the world.

This repository intentionally implements a narrow benchmark orchestrator
instead of a general customer-service platform. Every state variable,
transition, observation, option, and scoring decision is inspectable.

## Benchmark boundary

The benchmark is:

- closed-loop: the model's pre-gap action changes later state;
- alternating-turn: user and evaluated agent turns are processed separately;
- audio-conditioned: real-model runs hear individual/replayed WAV turns;
- tool-using: model choices execute symbolic Python actions;
- belief-explicit: the model reports calibrated hidden-state distributions at
  three checkpoints;
- dual-control: a matched condition lets the user execute a hidden tool action
  during the gap;
- deterministic at the environment layer: equal transition inputs produce
  equal outputs;
- trajectory-scored: both decisions and the resulting state are logged.

The benchmark is not:

- a completed-WAV next-action classifier;
- full duplex;
- speech-to-speech, because agent decisions are structured text rather than
  synthesized model speech;
- a claim about hour-scale long-audio understanding. The present benchmark
  should be described as long-horizon conversational state tracking.

## Closed-loop lifecycle

The main runner is
[`dual_audio/interaction/runner.py`](dual_audio/interaction/runner.py). One
trajectory follows this sequence:

```text
1. Initialize hidden state from the task.
2. Present one scripted user turn as text or audio.
3. Ask the evaluated model for the corresponding agent turn.
4. Repeat steps 2-3 for the pre-gap dialogue.
5. Present a randomized pre-gap action menu and collect belief checkpoint 1.
6. Execute the model-selected symbolic action against hidden state.
7. Add a deterministic user acknowledgement.
8. Optionally execute a hidden user tool action during the gap.
9. Advance time and apply the condition's external event.
10. Generate the resumed user observation from the resulting state.
11. Collect belief checkpoint 2 without allowing an action yet.
12. Collect belief checkpoint 3 with the randomized final action menu.
13. Execute and score the model-selected post-gap action.
14. Store the complete trajectory as one JSONL record.
```

In compact form:

```text
task.initial_state
  -> scripted user turn
  -> evaluated agent turn(s)
  -> evaluated pre-gap action
  -> execute_action(...)
  -> transition(state, action, elapsed_time, external_event, user_action)
  -> post_gap_observation(resulting_state)
  -> resumed state belief
  -> final state belief + evaluated post-gap action
  -> state-based evaluation
```

Scripted agent text in a task is a dialogue-intent constraint, not prerecorded
agent audio. It keeps the deterministic user script coherent while the tested
model still produces the actual intervening response.

## Quick start

Python 3.10 or newer is recommended. The fake agent validates orchestration
without model weights, API keys, TTS, or audio tools:

```bash
python scenarios/generate.py --variants 2
python run_eval.py --model fake --conditions all --passes 5
python score.py closed_loop results/fake_closed_loop.jsonl
python -m unittest discover -s tests -v
```

The default output is `results/<model>_closed_loop.jsonl`. Runs are
checkpointed after every trajectory and resume by `(scenario, condition,
seed)`.

### Gemini

Install the SDK and plotting dependency, set the API key, and run:

```powershell
pip install google-genai matplotlib
$env:GOOGLE_API_KEY = "..."
python run_eval.py --model gemini --conditions full_audio --passes 5
```

The compatibility filename `models/gemini_live.py` now uses Gemini's standard
multimodal content call. Half-duplex interaction is provided by the benchmark
runner, so a persistent realtime session is not required.

### Qwen

The local Qwen adapter requires PyTorch, Transformers, and
`qwen-omni-utils`. Hardware requirements depend on the selected checkpoint:

```bash
python run_eval.py --model qwen --conditions full_audio --passes 5
```

### Local audio dependencies

Real audio runs and audio pre-rendering require `espeak-ng` and `ffmpeg`.
The fake model skips TTS unless `--render-fake-audio` is supplied.

## Core interfaces

### Agent contract

All evaluated models are normalized to the same interface:

```python
class Agent(Protocol):
    def respond(
        self,
        observation: Observation,
        history: list[dict],
    ) -> AgentResponse:
        ...
```

`Observation` contains the current text/audio turn, stage, public menu,
allowed belief-state values, and instruction. `AgentResponse` contains a
natural-language message, public action labels, probabilistic `state_belief`,
and `needs_revalidation`. See
[`dual_audio/core/types.py`](dual_audio/core/types.py).

Production prompts never contain canonical action names, gold actions, hidden
state, or private test metadata. The dry-run `MockAgent` is explicitly
oracle-backed and is only a pipeline fixture, not a scientific baseline.

### Audio replay adapter

Existing model-specific `ask(audio, prompt)` functions are wrapped by
`ReplayModelAgent`. On each call it:

1. collects prior user and evaluated-agent WAV turns;
2. appends the current user WAV;
3. concatenates them into a cached replay WAV;
4. asks the model for the current turn;
5. parses public action labels from structured JSON.

The model therefore hears its own earlier generated responses, not scripted
agent recordings. Transcript controls use each model module's `ask_text`
function instead.

### State and transition contract

Symbolic tools and transitions live in
[`dual_audio/core/environment.py`](dual_audio/core/environment.py).

```python
state_after_tool = execute_action(
    domain=task["domain"],
    current_state=current_state,
    action=selected_action,
)

state_after_gap = transition(
    domain=task["domain"],
    current_state=state_after_tool,
    agent_action=selected_action,
    elapsed_minutes=task["transition"]["elapsed_minutes"],
    external_event=event,
    user_action=gap_user_action,
)
```

Both functions deep-copy their input. They do not mutate task definitions or
reuse a post-gap state stored in scenario metadata. The post-gap answer key is
computed by `correct_action(domain, state_after_gap)`.

Consequently, a wrong pre-gap action can change:

- `state_before_gap`;
- the result of the time transition;
- the resumed user observation;
- the correct post-gap action.

## Task schema

Tasks are generated JSON documents with schema version `0.3`. Important fields
are:

```json
{
  "schema_version": "0.3",
  "scenario_id": "router_12to20_v0",
  "domain": "tech_support",
  "bucket": "12-20",
  "clue_turn_distance": 16,
  "turns": [
    {"speaker": "user", "text": "...", "kind": "setup"},
    {"speaker": "agent", "text": "...", "kind": "setup"}
  ],
  "initial_state": {"firmware_status": "not_started"},
  "pre_gap": {"correct_action": "run_maintenance"},
  "transition": {
    "elapsed_minutes": 30,
    "external_event": {"type": "maintenance_window_elapsed"},
    "user_action": {
      "action": "power_cycle_during_maintenance",
      "at_minute": 10
    }
  },
  "belief_schema": {
    "firmware_status": [
      "not_started", "updating", "stuck", "completed", "interrupted"
    ]
  },
  "revalidation_actions": ["inspect_persistent_state"],
  "belief_confidence_threshold": 0.6,
  "pre_gap_actions": [],
  "post_gap_actions": [],
  "prosody_pair": {},
  "response_styles": []
}
```

Action entries separate private semantics from public wording:

```json
{
  "action": "repeat_power_cycle",
  "description": "Repeat the basic power recovery procedure.",
  "failure_tags": ["REPEATED_ACTION", "EARLY_CLUE_LOSS"]
}
```

Only the description and a randomized label such as `C` are shown to the
model. Canonical names are used internally for tool execution and evaluation.

## Deterministic environment

The transition engine uses five explicit inputs:

```python
next_state = transition(
    current_state,
    agent_action,
    elapsed_minutes,
    external_event,
    user_action,
)
```

Current domain mechanics include:

| Domain | Pre-gap tool effect | Time/external transition |
|---|---|---|
| Router support | Starts maintenance or records another selected action | A sufficiently long maintenance window can stall a corrupted device at 47% |
| Pharmacy | Submits or changes the handling of a claim | A processor cycle approves or rejects from the active/billed-plan state |
| Travel | Enables monitoring or changes itinerary handling | A departure-delay event updates connection feasibility |

Unit tests verify that identical inputs return equal states and that changing
the pre-gap action changes the result where expected.

### Hidden user actions during the gap

The `hidden_user_action` condition activates the task's
`transition.user_action` input. The action occurs while the agent is absent and
before the external transition threshold:

```text
agent tool action
  -> hidden user tool action at a task-defined minute
  -> elapsed-time/external transition
  -> state-conditioned user report
  -> agent belief resynchronization
```

Current hidden user tools are:

| Domain | Hidden user action | Shared-world effect |
|---|---|---|
| Router support | Power-cycles during maintenance | Interrupts an active maintenance process |
| Pharmacy | Calls the plan provider | Records independent confirmation that the active plan is valid |
| Travel | Rebooks the onward segment independently | Protects the connection before the delay event |

The action is not exposed before the gap. The resumed utterance reports what
the user did and the observable outcome. The final answer is recomputed from
the resulting shared state, so the user action can change the correct action.

## Experimental controls

Use a comma-separated subset with `--conditions`, or use
`--conditions all`.

| Condition | Changed factor | Capability isolated |
|---|---|---|
| `full_audio` | None | Main closed-loop benchmark |
| `gap_no_state_change` | Suppresses the external event but preserves elapsed time | Whether the gap itself causes stale-state behavior |
| `state_change_short` | Moves the same clue pair immediately before the pre-gap decision | State inference without long-distance memory pressure |
| `clue_removed` | Replaces only the clue response with a matched ablation utterance | Whether the model actually uses the clue |
| `transcript_only` | Presents text instead of audio | Text reasoning baseline |
| `neutral_audio` | Neutralizes resumed-turn prosody | Audio-processing baseline |
| `hidden_user_action` | Executes a task-defined user tool during the gap and reports it afterward | Temporally separated dual control and belief resynchronization |
| `prosody_high` | High-affect delivery of the resumed transcript | Prosody-sensitive secondary response choice |
| `prosody_low` | Low-affect delivery of the identical resumed transcript | Contrastive pair for `prosody_high` |

Paired-control invariants:

- action descriptions are identical across paired conditions;
- option order is identical for the same scenario/stage/seed;
- randomization does not include condition name in its seed;
- clue ablation preserves turn count;
- prosody pairs preserve the exact resumed transcript;
- the short-distance condition preserves total conversation length and moves
  the clue rather than deleting context.

## Action leakage controls

Each stage has five natural-language choices. Before presentation:

1. canonical action names are hidden;
2. choices are deterministically shuffled by scenario, stage, and seed;
3. public labels `A` through `E` are assigned after shuffling;
4. the same permutation is reused for paired conditions;
5. generation rejects a correct option if it alone repeats a clue content word.

The scorer also performs a paired clue-ablation analysis. If full and
clue-removed performance differ by less than five percentage points, it prints
a warning that the task may not be measuring clue use.

## Distance definition and validation

`clue_turn_distance` is calculated from the completed turn sequence. It is the
number of agent/user turns after the clue and before fast-forward, including:

- the evaluated pre-gap action; and
- the deterministic user acknowledgement.

Those two turns make 2 the minimum realizable distance. The `1-2` bucket
therefore currently contains distance 2. The generator calculates and asserts:

```python
actual_distance = len(turns) - clue_index - 1
assert actual_distance == recorded_distance
```

Each trajectory also logs `effective_clue_turn_distance`, because
`state_change_short` moves the clue at presentation time.

## Prosodic contrast design

`prosody_high` and `prosody_low` use:

- identical words;
- identical hidden state;
- identical technical action menus;
- different rendered pitch/rate controls;
- different expected secondary response approaches.

For example, a frustrated delivery expects a brief acknowledgement of impact,
while a calm delivery expects a direct neutral transition to the operational
step. The technical action remains state-dependent and unchanged.

This implementation provides the experimental pair, not evidence that the TTS
contrast is perceptually valid. Human audibility validation remains required.

## Trajectory schema

One JSONL row represents one complete evaluation attempt. It includes:

- model, scenario, condition, and seed;
- initial state;
- selected and expected pre-gap action;
- pre-gap state-belief distribution and revalidation flag;
- public pre-gap menu and menu size;
- state immediately after tool execution;
- hidden user action and state immediately after that user tool;
- elapsed time and applied external event;
- post-transition hidden state;
- generated resumed observation and prosody;
- state belief immediately after hearing the resumed observation;
- state belief repeated immediately before the final action;
- selected and expected post-gap action;
- optional selected and expected response style;
- final state;
- all alternating user/agent turns;
- raw model outputs;
- component successes, trajectory success, and multilabel failure tags;
- belief revision, stale-belief persistence, calibration, risk, and
  action-belief consistency fields.

This makes failures auditable without reconstructing state from a final answer.

## Scoring

Run:

```bash
python score.py closed_loop results/fake_closed_loop.jsonl
```

Primary metrics:

- repeated-trial trajectory pass@1;
- pre-gap action accuracy;
- post-gap action accuracy;
- scenario-level majority accuracy;
- variance across run seeds;
- scenario-clustered bootstrap 95% confidence intervals;
- fraction of scenarios that succeed on every repeated trial.

Belief-state metrics:

- state-belief top-state accuracy at all three checkpoints;
- belief-report validity;
- Brier score and negative log likelihood per checkpoint;
- expected calibration error over top-state confidence;
- probability gain assigned to the new state after resumed evidence;
- probability mass that persists on the stale pre-gap state;
- reflection-only gain between the resumed and pre-final checkpoints;
- action-belief consistency;
- `needs_revalidation` consistency with the model's own confidence;
- uncertain-act versus uncertain-recheck rates.

The scorer also reports the belief/action matrix:

| Belief | Action | Reported interpretation |
|---|---|---|
| Correct | Correct | Full success |
| Correct | Wrong | Action-selection failure |
| Wrong | Correct | Lucky action |
| Wrong | Wrong | State-synchronization failure |

Supplemental metrics and diagnostics:

- pass@5;
- paired full-versus-clue-removed accuracy delta;
- paired prosodic contrast success;
- multilabel failure-tag distribution;
- retention curve by clue-distance bucket.

Chance is calculated from logged menu sizes:

- one five-choice action: `1/5 = 20%`;
- two independent five-choice actions: `1/25 = 4%`.

Schema-v0.3 full success additionally requires correct top-state beliefs at
three checkpoints. The scorer therefore reports a dynamic full
action-plus-belief chance baseline based on each task's belief-state space.
Prosodic conditions additionally include their response-style choice.

The retention plot shows the post-gap action, two-action, and full
action-plus-belief floors. It does not use the previous incorrect `1/6`
constant.

## Failure tags and annotation

Incorrect choices may encode more than one failure. For example, repeating a
restart can be both a repeated action and evidence of clue loss. The schema
therefore stores `failure_tags` as a list rather than forcing one label.

The task templates contain proposed tags, but publishable labels require
independent annotation:

```bash
python -m dual_audio.evaluation.annotations export data/scenarios ann_a.csv A
python -m dual_audio.evaluation.annotations export data/scenarios ann_b.csv B
python -m dual_audio.evaluation.annotations report ann_a.csv ann_b.csv
```

The report requires at least two completed annotation files and prints exact
multilabel agreement and mean Jaccard agreement.

## Audio generation and human validation

The runner lazily renders and caches one WAV per turn. To pre-render gold-path
user turns and prosodic pairs:

```bash
python audio/tts.py
```

This writes `data/turn_audio/manifest.jsonl`, including transcript-pair IDs and
expected response styles.

The default `espeak-ng` pitch/rate changes are pipeline fixtures, not validated
human-quality emotional speech. Create blinded listener sheets with:

```bash
python -m dual_audio.evaluation.prosody_validation export \
  data/turn_audio/manifest.jsonl listener_a.csv listener_a
python -m dual_audio.evaluation.prosody_validation export \
  data/turn_audio/manifest.jsonl listener_b.csv listener_b
python -m dual_audio.evaluation.prosody_validation report \
  listener_a.csv listener_b.csv
```

The report checks intended-prosody identification and listener agreement.

## Reproducibility safeguards

- Scenario generation uses stable per-domain/bucket/variant seeds.
- Action order uses stable scenario/stage/run seeds.
- Condition is excluded from menu-order seeds to preserve paired comparisons.
- Environment functions copy state rather than mutating input objects.
- Task JSON contains transition inputs, not precomputed post-gap state.
- Hidden user actions include a validated timestamp within the elapsed gap.
- Belief distributions are validated, normalized, and scored only against
  task-declared state values.
- JSONL is flushed after every trajectory.
- Successful trajectories are skipped on restart; failed rows are retried.
- The fake model is deterministic for a scenario/stage/seed.
- Tests cover distance, alternation, transition determinism, action dependence,
  controls, prosodic pairs, hidden user tools, belief revision, calibration,
  action-belief consistency, and chance calculations.

## Extending the benchmark

### Add a scenario variant

Edit [`scenarios/templates.py`](scenarios/templates.py), then regenerate:

```bash
python scenarios/generate.py --variants 2
```

Keep agent/user turns alternating. Do not add a hard-coded post-gap state.

### Add a domain

1. Add the task template and symbolic action descriptions.
2. Add domain branches to `execute_action`, `execute_user_action`,
   `transition`, `correct_action`, and `post_gap_observation`.
3. Add deterministic and action-dependence tests.
4. Ensure every state-reachable correct action exists in the post-gap menu.
5. Run clue-leak and distance generation checks.

### Add a model

For models with existing inference functions, expose:

```python
def ask(audio_path: str, instruction: str) -> str: ...
def ask_text(prompt: str) -> str: ...
```

Then add the module mapping in `run_eval.get_agent`. For a native stateful
adapter, implement `Agent.respond` directly.

### Add a condition

1. Add a `Condition` in `dual_audio/core/conditions.py`.
2. Implement only the intended presentation/event transformation.
3. Keep paired randomization stable.
4. Add a test demonstrating what changes and what remains identical.
5. Update the condition table in this README.

## Validation status

During the closed-loop implementation:

- 18 schema-v0.3 tasks were regenerated;
- all pre-gap and post-gap menus were verified to contain five choices;
- generated tasks were verified not to contain hard-coded `state_update`
  objects;
- 16 focused unit tests passed;
- an 810-trajectory schema-v0.3 fake-agent run completed across all nine
  conditions and five seeds;
- the fake run demonstrated dynamic chance floors, clue-ablation reporting,
  prosodic-pair scoring, hidden user actions, explicit belief revision,
  calibration, action-belief coupling, and multilabel failure reporting.

The fake agent is an orchestration test only. Human task solvability,
independent trap annotation, audible-prosody validation, and real-model
evaluation remain empirical work.

## Repository layout

```text
dual_audio/
  agents/          Agent protocol, fake agent, replay/response parser
  core/            observations, conditions, tools, policies, transitions
  evaluation/      human tag and prosody validation utilities
  interaction/     closed-loop alternating-turn runner
  modalities/      turn rendering and replay WAV assembly
  users/           deterministic state-conditioned user simulator
audio/             gold-path individual-turn rendering CLI
scenarios/         domain templates, leak guards, audited generator
models/            Gemini, Qwen, and fake compatibility modules
data/scenarios/    generated schema-v0.3 benchmark tasks
tests/             transitions, controls, runner, generator, metrics
run_eval.py        crash-resumable batch trajectory runner
score.py           metrics, control comparisons, tags, retention plot
```

## Implementation summaries

The original passive-to-agentic conversion is documented in
[`docs/IMPLEMENTATION_SUMMARY.md`](docs/IMPLEMENTATION_SUMMARY.md).

The belief-tracking and hidden-user-action extension added afterward is
documented in
[`docs/IMPLEMENTATION_SUMMARY_V2.md`](docs/IMPLEMENTATION_SUMMARY_V2.md).
