# Schema-v0.5 main experiment plan

## Main matrix

The definitive v0.5 run uses all nine registered conditions. Five conditions
carry the headline comparisons; four provide mechanism and validity controls.

| Role | Condition | Main question |
|---|---|---|
| Reference | `full_audio` | Can the audio-replay-conditioned agent complete the trajectory? |
| Modality | `transcript_only` | Does written history outperform replayed audio history? |
| Construct validity | `clue_removed` | Does performance depend on the causal clue? |
| Prosody | `prosody_high` | Is high-affect delivery grounded while technical behavior stays fixed? |
| Prosody | `prosody_low` | Is low-affect delivery grounded while technical behavior stays fixed? |
| Acoustic control | `neutral_audio` | Is an audio effect attributable to the intended delivery rather than any audio? |
| Transition control | `gap_no_state_change` | Does failure specifically follow a changing hidden state? |
| Retention control | `state_change_short` | Does moving the same clue near the decision remove distance-related loss? |
| Agency control | `hidden_user_action` | Can the agent recover when a reported user intervention during the gap changes a scored state or action? |

The earlier five-condition proposal was a budget-efficient minimum containing
the three headline contrasts: modality, causal ablation, and paired prosody. It
was not selected because the other conditions were invalid. For the main v0.5
paper, omitting all four mechanism controls would save money but weaken causal
interpretation, so the default launcher now runs all nine.

| Run | Tasks | Conditions | Seeds | Trajectories |
|---|---:|---:|---:|---:|
| Model 1 | 84 | 9 | 2 | 1,512 |
| Model 2 | 84 | 9 | 2 | 1,512 |
| **Total** | | | | **3,024** |

Two seeds are enough for the main matrix because the inferential unit is the 14
domain clusters, not the number of stochastic repeats. If resources permit,
adding model families is more valuable than adding seeds. A third model adds
1,512 trajectories.

The planned two-model panel is `google/gemini-2.5-flash` plus
`openai/gpt-audio-mini`. This supplies two model providers/families while
retaining both audio and transcript inputs and structured output support. The
local Qwen2.5-Omni adapter is not part of the main matrix on this machine:
there is no CUDA GPU and the required `qwen-omni-utils` package is absent.

Measured v0.4 cost was $43.47 for 2,352 trajectories. Replacing the second
Gemini model with the cheaper cross-family GPT Audio Mini should reduce the
v0.5 estimate, but the added causal-rule turn, belief variable, and two extra
audio conditions increase context. Reserve **$45--$55**, then replace this
estimate with the two-model compatibility gate's measured cost projection
before launching. Do not launch unless the key's live remaining limit covers
the projected run plus a 20% retry margin.

## Freeze and launch

Before paid execution:

1. Commit or tag the generated v0.5 task files and record their manifest hash.
2. Freeze the primary metrics and matched comparisons below.
3. Run one paid trajectory per model as a compatibility gate.
4. Launch the resumable all-nine-condition matrix.
5. Do not edit tasks, transitions, prompts, or scoring after observing v0.5
   model outcomes; any repair becomes v0.5.1 or v0.6 and is reported separately.

Example launches:

```powershell
scripts/run_paid_v05.ps1 `
  -ModelId "google/gemini-2.5-flash" `
  -RunSlug "gemini25_main"

scripts/run_paid_v05.ps1 `
  -ModelId "openai/gpt-audio-mini" `
  -RunSlug "gpt_audio_mini_main"
```

Check and finalize:

```powershell
scripts/paid_v05_status.ps1 -RunSlug gemini25_main,gpt_audio_mini_main
scripts/finalize_paid_v05.ps1 -RunSlug gemini25_main,gpt_audio_mini_main
```

The launch manifest expects 1,512 unique completed trajectories per model.
JSONL remains one record per line for atomic checkpointing and resume; the
finalizer creates human-readable indented JSON, Markdown, CSV, matrices, and
curves.

## Frozen inference and reporting

The single confirmatory construct-validity endpoint is the paired
`full_audio - clue_removed` post-gap action effect on Gemini 2.5 Flash, with
domain-clustered confidence intervals and the exact domain sign-flip test. The
same endpoint on GPT Audio Mini is a cross-family replication. A claim of
generalization requires the effect to have the same direction on both models;
it is not rescued by pooling their trajectories.

The transcript/audio belief contrast, retention effects, transition controls,
and prosody metrics are pre-specified secondary analyses. Raw p-values are
reported with effect sizes and clustered intervals, but no secondary result is
called confirmatory without an explicit multiplicity correction. Prosody is
exploratory until the audio pairs pass listener validation.

Report for every model:

- strict trajectory success, two-action success, pre-gap action, and post-gap
  action by condition;
- all-belief accuracy, belief validity, Brier score, NLL, ECE, belief revision,
  stale mass, and the belief/action matrix;
- full-audio minus clue-removed paired post-gap and strict effects with
  domain-clustered confidence intervals and sign-flip p-values;
- transcript-minus-full-audio paired action and belief effects;
- full-audio versus no-state-change and short-distance controls;
- high/low prosody paired style accuracy, directional contrast, technical
  invariance, and belief-distribution invariance;
- retention curves by distance and failure-tag distributions;
- causal pair accuracy, both-branch correctness, branch balance, and the 50%
  clue-independent ceiling.

Strict trajectory success is the conjunction of both actions and all three
belief reports. It is reported as a diagnostic composite, not substituted for
its action and belief components. The post-gap action is elicited after a
belief-only checkpoint and is therefore described as *belief-elicited action
accuracy*, not unprompted agent behavior. ECE pools dependent checkpoint and
variable observations and is descriptive rather than an inferential endpoint.

## Scope limitations frozen before outcomes

- `full_audio` is stateless accumulated-audio replay conditioning, not a
  continuous or full-duplex session.
- Transcript and audio conditions differ in representation, so the modality
  contrast is not attributed solely to acoustic perception.
- Synthetic eSpeak prosody is not treated as validated human affect until the
  listener study is complete.
- The independent audit documents scenario review but is not a population-level
  human-solvability baseline.
- Trial seeds jointly vary option order and stochastic sampling; seed variance
  is labeled accordingly.

No v0.3 or v0.4 trajectory is pooled into a v0.5 estimate.
