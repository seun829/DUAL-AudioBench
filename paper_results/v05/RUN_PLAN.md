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
| Agency control | `hidden_user_action` | Can the agent recover when an unobserved user tool action changes state? |

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

Measured v0.4 cost was $43.47 for 2,352 trajectories: about $0.021 per audio
trajectory and $0.002--$0.004 per transcript trajectory. At those rates, the
full v0.5 two-model matrix is about $58. The added causal-rule turn and belief
variable will increase context slightly, so budget approximately $63--$70. The
five-condition minimum would be roughly $30 before that overhead.

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
  -ModelId "google/gemini-3-flash-preview" `
  -RunSlug "gemini3_main"
```

Check and finalize:

```powershell
scripts/paid_v05_status.ps1 -RunSlug gemini25_main,gemini3_main
scripts/finalize_paid_v05.ps1 -RunSlug gemini25_main,gemini3_main
```

The launch manifest expects 1,512 unique completed trajectories per model.
JSONL remains one record per line for atomic checkpointing and resume; the
finalizer creates human-readable indented JSON, Markdown, CSV, matrices, and
curves.

## Frozen primary reporting

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

No v0.3 or v0.4 trajectory is pooled into a v0.5 estimate.
