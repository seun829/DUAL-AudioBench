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
python scenarios/generate_v05.py
python run_eval.py --model fake --conditions all --passes 5
python score.py closed_loop results/fake_v05_closed_loop.jsonl
python -m unittest discover -s tests -v
```

Generation and evaluation default to the main benchmark in
`data/scenarios_v05/`. The schema-v0.3 files in `data/scenarios/` and
schema-v0.4 files in `data/scenarios_v04/` remain frozen; do not pool
trajectories across schema versions. The default output is
`results/<model>_v05_closed_loop.jsonl`. Runs are
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

### OpenRouter

Any audio-capable model reachable through OpenRouter's OpenAI-compatible
endpoint can be evaluated without a provider-specific SDK:

```powershell
$env:OPENROUTER_API_KEY = "..."          # or a key= entry in .env
$env:OPENROUTER_MODEL = "google/gemini-2.5-flash"
python run_eval.py --model openrouter --conditions full_audio --passes 5
```

Token usage, upstream cost, and request latency are recorded on every
trajectory and also accumulated in `results/openrouter_usage.json`. Note that audio-native models such as
`openai/gpt-audio-mini` reject text-only requests and therefore cannot run
`transcript_only`; check both `ask` and `ask_text` before committing to a run.

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
allowed belief-state values, their short operational definitions, and the
instruction. `AgentResponse` contains a
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
| Banking | Files a disputed charge for automated review | A review cycle returns unmatched when the filed card differs from the charged card |
| Scheduling | Requests coverage approval for a booking | An authorization review declines a referral from an ineligible provider type |
| Logistics | Books a parcel onto a delivery run | A delivery window returns the parcel when the label address is stale |
| Energy | Submits a meter reading for validation | A validation cycle flags the reading when supply points are unregistered |
| Account access | Starts a credential reset | A propagation window leaves the account locked when authentication is federated |
| Repair | Opens a warranty claim for assessment | An assessment cycle rejects a purchase channel outside the covered terms |
| Housing | Dispatches a contractor visit | A visit window records refused access when entry permissions are stale |
| Mobile service | Sends a number transfer to the porting queue | A porting window rejects a mismatched ownership record |
| Education | Submits an enrolment for registration | A registration run holds enrolment when prior study is unassessed |
| Motor insurance | Lodges a damage report for assessment | An assessment run holds the claim when the keeper differs from the policyholder |
| Permits | Submits a permit application for eligibility checking | An eligibility check refuses proof naming another occupant |

All fourteen domains share one structural schema: a clue reveals a latent
property, the naive pre-gap action proceeds anyway, and the external event
resolves against the user. That is breadth of surface form, not of mechanism.

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

The scorer also performs a paired clue-ablation analysis with a
domain-clustered confidence interval and exact domain sign-flip test. The
control is considered established only when the interval excludes zero on a
capable model; a bare magnitude threshold is not treated as validation.

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

Schema v0.4 crosses three carrier-transcript variants with two eSpeak user
voices and assigns category-specific gold approaches for frustration,
urgency, and confusion. This provides the experimental pair, not evidence
that the TTS contrast is perceptually valid. Blinded human audibility
validation remains required.

Schema v0.5 preserves that paired prosody design and adds 42 balanced causal
clue pairs. In each pair, one early fact changes the terminal hidden state and
the correct post-gap action while later public wording and menus remain fixed.
# Schema v0.5 causal-clue design

Schema v0.5 is the main benchmark version. It repairs a construct-validity
failure found in v0.4 while leaving every v0.3 and v0.4 task and result frozen.

## Why v0.4 showed little clue dependence

In v0.4, removing the early clue changed only one public utterance. It did not
change the initialized hidden state, the deterministic transition, or the gold
post-gap action. The resumed user observation then named the terminal outcome
directly (for example, rejected or unmatched). A model could therefore ignore
the clue and recover the correct action from the last turn. The ablation was a
memory perturbation, but it was not a causal test of clue use.

The old automated checks established deterministic transitions, valid menus,
and non-leaking option text. They did not assert that changing the clue changed
the terminal hidden state and required action. Schema v0.5 adds that missing
invariant.

## Counterfactual construction

Each of 14 domains, three clue-distance buckets, and two causal branches makes
84 separately identified tasks. The branches form 42 matched pairs:

- `misaligned`: the early fact conflicts with the rule, producing a repairable
  terminal state and a domain-specific recovery action;
- `aligned`: the early fact satisfies the rule, producing successful completion
  and `close_case` as the correct action.

The dialogue states a short generic causal rule before asking for the clue. The
paired clue then changes one relevant fact. All filler turns, voices, option
sets, option ordering, and the post-gap words are held constant. The resumed
observation says the process ended but withholds its hidden result, forcing the
model to combine the early fact with the stated rule.

For example, the router pair states that intact saved configuration permits a
firmware update to finish, whereas corrupted configuration leaves it stuck.
One clue says the saved data was intact and the other says it was corrupted.
Both branches later hear that the maintenance cycle ended and its result display
is blank. The correct actions are consequently `close_case` and
`inspect_persistent_state`.

## Enforced invariants

The generator and tests require all of the following:

1. Both branches exist for every domain and distance bucket.
2. Their terminal hidden outcomes differ.
3. Their correct post-gap actions differ.
4. With the original clues, public histories differ at exactly one clue turn.
5. With the clue ablated, public user histories are identical.
6. Paired menu contents and randomized label order are identical.
7. The standard post-gap observation is identical and does not disclose which
   hidden branch occurred.
8. The no-state-change and hidden-user-action controls remain truthfully
   state-conditioned rather than using the ambiguous standard observation.
9. `causal_alignment` is explicitly included in the belief schema and scored.
10. The prosody pair preserves words, state, and technical gold action.

Balanced indistinguishable branches imply a 50% expected post-gap ceiling for
a clue-independent policy. Unlike the v0.4 ablation, an above-ceiling result can
now be interpreted as evidence of retaining and applying the clue. Statistical
inference must still use matched scenario/seed effects clustered by the 14
domains.

## Human-solvability judgment

The tasks are structurally human-solvable in principle: every causal rule is
given in the conversation; no outside domain knowledge is necessary; each clue
maps unambiguously to one of two outcomes; the correct action exists exactly
once in the menu; and the resumption explicitly asks the participant to use the
earlier detail. This is an expert structural audit, not a measured human
baseline. Before publication, a small blinded study should target roughly
85--95% post-gap action accuracy. Below 80% would suggest ambiguity or burden;
100% is unnecessary and may indicate an overly easy task.

## Validation completed

- 84 schema-v0.5 files generated in `data/scenarios_v05/`.
- 55 repository tests pass, including eight causal-pair/reporting regression
  tests.
- A 756-trajectory fake-agent run covers all 84 tasks and all nine conditions
  with zero runtime errors.
- The reporting pipeline produces readable Markdown, indented JSON, CSV,
  retention/modality/prosody curves, and causal-clue counterfactual metrics.

The fake model is an orchestration fixture that reads runner-private gold
labels. Its scores are not benchmark evidence.


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
python score.py closed_loop results/fake_v05_closed_loop.jsonl
```

Primary metrics:

- repeated-trial trajectory pass@1;
- pre-gap action accuracy;
- post-gap action accuracy;
- scenario-level majority accuracy;
- variance across run seeds;
- equal-weight domain-clustered bootstrap 95% confidence intervals and exact
  domain sign-flip tests;
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

- pass@k, labeled with the number of observed run seeds;
- paired full-versus-clue-removed effect with uncertainty;
- paired high/low response-style accuracy and directional contrast;
- technical-action and top-belief invariance across prosody pairs;
- belief Jensen-Shannon divergence across prosody pairs;
- multilabel failure-tag distribution;
- retention curve by clue-distance bucket.

Chance is calculated from logged menu sizes:

- one five-choice action: `1/5 = 20%`;
- two independent five-choice actions: `1/25 = 4%`.
- one four-choice response approach: `1/4 = 25%`;
- a matched high/low response-approach pair: `1/16 = 6.25%`.

Schema-v0.3, v0.4, and v0.5 full success additionally require correct top-state
beliefs at three checkpoints. The scorer therefore reports a dynamic full
action-plus-belief chance baseline based on each task's belief-state space.
Prosodic conditions additionally include their response-style choice.

The retention plot includes clustered uncertainty bands. Separate figures show
the immediate audio/text belief gap and prosody selectivity. Generate a
readable Markdown report, indented JSON, and CSV files with:

```bash
python report_results.py results/openrouter_v05_closed_loop.jsonl --out-dir results/report_v05
```

## Failure tags and annotation

Incorrect choices may encode more than one failure. For example, repeating a
restart can be both a repeated action and evidence of clue loss. The schema
therefore stores `failure_tags` as a list rather than forcing one label.

The task templates contain proposed tags, but publishable labels require
independent annotation:

```bash
python -m dual_audio.evaluation.annotations export data/scenarios_v05 ann_a.csv A
python -m dual_audio.evaluation.annotations export data/scenarios_v05 ann_b.csv B
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

- The frozen v0.3 pilot contains 1,344 completed real-model trajectories over
  84 tasks, three models, and zero terminal API errors.
- The frozen v0.4 study contains 2,352 completed real-model trajectories over
  84 separately identified tasks, two models, and seven conditions.
- Schema v0.5 contains 84 tasks arranged as 42 balanced causal clue pairs. The
  end-to-end fake run completed all 756 task-condition pairs with zero runtime
  errors and generated every metric table and figure.
- Fifty-five focused tests cover transitions, schemas, prompts, parsing,
  domain-clustered inference, causal clue ablation, and matched prosody pairs.
- A structural expert audit found all 14 mechanisms human-solvable in
  principle; this is not a substitute for an empirical human baseline.

The fake agent remains an orchestration fixture. Independent trap annotation,
audible-prosody validation, and human accuracy are still empirical work.

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
models/            Gemini, Qwen, OpenRouter, and fake compatibility modules
data/scenarios/    generated schema-v0.3 benchmark tasks
data/scenarios_v04/ frozen schema-v0.4 validation tasks
data/scenarios_v05/ main schema-v0.5 causal-pair tasks
tests/             transitions, controls, runner, generator, metrics
analyze_pilot.py   saves paired deltas and belief/action matrices as files
run_eval.py        crash-resumable batch trajectory runner
score.py           metrics, control comparisons, tags, retention plot
paper_results/     cross-model results, scores, figures, and cost records
```

## Implementation summaries

The original passive-to-agentic conversion is documented in
[`docs/IMPLEMENTATION_SUMMARY.md`](docs/IMPLEMENTATION_SUMMARY.md).

The belief-tracking and hidden-user-action extension added afterward is
documented in
[`docs/IMPLEMENTATION_SUMMARY_V2.md`](docs/IMPLEMENTATION_SUMMARY_V2.md).

The versioned prompt, prosody, statistics, reporting, and paid-run changes are
documented in
[`docs/IMPLEMENTATION_SUMMARY_V04.md`](docs/IMPLEMENTATION_SUMMARY_V04.md).

