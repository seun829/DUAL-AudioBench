# DUAL-AudioBench evaluation report

- Raw attempt rows: 9
- Unique completed trajectories: 9
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 0
- Models: fake

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## fake

- Coverage: 9/9 trajectories (100.0%)
- Overall partial outcomes: 88.9% pre-gap, 11.1% post-gap, 11.1% both actions, 11.1% strict trajectory
- API calls: 0 (0 metered)
- Tokens: 0 (0 prompt + 0 completion)
- Reported API cost: $0.0000
- API request time: 0.0 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0000 |
| gap_no_state_change | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0000 |
| state_change_short | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | $0.0000 |
| clue_removed | 1 | 0.0% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | $0.0000 |
| transcript_only | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0000 |
| neutral_audio | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0000 |
| hidden_user_action | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0000 |
| prosody_high | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0000 |
| prosody_low | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0000 |

### Belief probability metrics

| Condition | Brier | NLL | Normalized entropy | ECE | Revision gain | Stale mass |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0.785 | 1.202 | 0.695 | 0.562 | -0.063 | 0.100 |
| gap_no_state_change | 0.785 | 1.202 | 0.695 | 0.562 | -0.063 | 0.100 |
| state_change_short | 0.137 | 0.340 | 0.720 | 0.275 | 0.597 | 0.073 |
| clue_removed | 1.010 | 1.476 | 0.670 | 0.667 | N/A | N/A |
| transcript_only | 0.785 | 1.202 | 0.695 | 0.562 | -0.063 | 0.100 |
| neutral_audio | 0.785 | 1.202 | 0.695 | 0.562 | -0.063 | 0.100 |
| hidden_user_action | 0.785 | 1.202 | 0.695 | 0.562 | -0.067 | 0.475 |
| prosody_high | 0.785 | 1.202 | 0.695 | 0.562 | -0.063 | 0.100 |
| prosody_low | 0.785 | 1.202 | 0.695 | 0.562 | -0.063 | 0.100 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Full audio - clue removed, full trajectory | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Hidden user action - full audio, post-gap | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, pre-gap action | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, post-gap action | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, immediate belief | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, strict trajectory | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Full audio - no-state-change gap, post-gap | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Neutral audio - full audio, immediate belief | 1 | 1 | 0.0% | 0.0% to 0.0% | 1.0000 |

### Prosody selectivity

- Identical-transcript pairs: 1; unique stimuli: 1.
- High-affect style accuracy: 100.0% [100.0%, 100.0%].
- Low-affect style accuracy: 100.0% [100.0%, 100.0%].
- Both deliveries correct: 100.0% [100.0%, 100.0%] (random pair chance 6.2%).
- Directional style contrast: 100.0% [100.0%, 100.0%].
- Technical-action invariance: 100.0% [100.0%, 100.0%].
- Post-observation top-belief invariance: 100.0% [100.0%, 100.0%].
- Post-observation belief JSD: 0.000 [0.000, 0.000].
- Pre-final belief JSD: 0.000 [0.000, 0.000].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0 | 0.0% | 0.0% | N/A | N/A | N/A |
| transcript_only | 0 | 0.0% | 0.0% | N/A | N/A | N/A |
| clue_removed | 0 | 0.0% | 0.0% | N/A | N/A | N/A |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: banking | 1 | 0.0% | 0.0% | 100.0% | 0.0% |
| bucket: 12-20 | 1 | 0.0% | 0.0% | 100.0% | 0.0% |

### Failure tags

- `STATE_BELIEF_ERROR`: 8 (100.0% of failed trajectories)
- `PREMATURE_CLOSE`: 7 (87.5% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 1 (12.5% of failed trajectories)

### Difficulty assessment

- The domain-clustered clue-ablation interval crosses zero; construct validity is not established for this model.

## Interpretation cautions

- Results contain 1 observed run seed(s); pass@k is labeled with the number actually available.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
