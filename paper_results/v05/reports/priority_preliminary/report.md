# DUAL-AudioBench evaluation report

- Raw attempt rows: 1349
- Unique completed trajectories: 1339
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 10
- Models: google/gemini-2.5-flash, google/gemini-3-flash-preview, openai/gpt-audio-mini

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## google/gemini-2.5-flash

- Coverage: 504/1512 trajectories (33.3%)
- Overall partial outcomes: 68.8% pre-gap, 31.9% post-gap, 29.8% both actions, 4.2% strict trajectory
- API calls: 7,591 (7,591 metered)
- Tokens: 9,923,795 (9,700,800 prompt + 222,995 completion)
- Reported API cost: $9.2956
- API request time: 1425.8 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 1.2% | 69.6% | 35.1% | 99.0% | 6.0% | 39.3% | $4.4706 |
| clue_removed | 168 | 1.2% | 59.5% | 25.0% | 98.6% | 10.1% | 29.8% | $4.3725 |
| transcript_only | 168 | 10.1% | 77.4% | 35.7% | 100.0% | 51.8% | 51.8% | $0.4524 |

### Belief probability metrics

| Condition | Brier | NLL | Normalized entropy | ECE | Revision gain | Stale mass |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0.787 | 6.745 | 0.225 | 0.362 | -0.009 | 0.021 |
| clue_removed | 1.006 | 8.036 | 0.309 | 0.457 | 0.147 | 0.022 |
| transcript_only | 0.472 | 4.174 | 0.218 | 0.171 | 0.282 | 0.018 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 168 | 14 | 10.1% | 3.6% to 17.3% | 0.0195 |
| Full audio - clue removed, full trajectory | 168 | 14 | 0.0% | -2.4% to 2.4% | 1.0000 |
| Hidden user action - full audio, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, pre-gap action | 168 | 14 | 7.7% | -2.4% to 17.9% | 0.2197 |
| Transcript - full audio, post-gap action | 168 | 14 | 0.6% | -7.7% to 8.9% | 1.0000 |
| Transcript - full audio, immediate belief | 168 | 14 | 12.5% | -0.6% to 25.0% | 0.1104 |
| Transcript - full audio, strict trajectory | 168 | 14 | 8.9% | 2.4% to 16.7% | 0.0312 |
| Full audio - no-state-change gap, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Neutral audio - full audio, immediate belief | 0 | 0 | N/A | N/A to N/A | N/A |

### Prosody selectivity

- Identical-transcript pairs: 0; unique stimuli: 0.
- High-affect style accuracy: N/A [N/A, N/A].
- Low-affect style accuracy: N/A [N/A, N/A].
- Both deliveries correct: N/A [N/A, N/A] (random pair chance N/A).
- Directional style contrast: N/A [N/A, N/A].
- Technical-action invariance: N/A [N/A, N/A].
- Post-observation top-belief invariance: N/A [N/A, N/A].
- Post-observation belief JSD: N/A [N/A, N/A].
- Pre-final belief JSD: N/A [N/A, N/A].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 35.1% | 1.2% | 11.9% | 0.0% | 64.3% |
| transcript_only | 84 | 35.7% | 10.1% | 8.3% | 1.2% | 60.7% |
| clue_removed | 84 | 25.0% | 1.2% | 1.2% | 0.0% | 53.6% |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 0.0% | 25.0% | 75.0% | 25.0% |
| domain: banking | 12 | 0.0% | 41.7% | 100.0% | 41.7% |
| domain: education | 12 | 0.0% | 25.0% | 66.7% | 25.0% |
| domain: energy | 12 | 8.3% | 58.3% | 91.7% | 58.3% |
| domain: housing | 12 | 0.0% | 58.3% | 91.7% | 58.3% |
| domain: logistics | 12 | 0.0% | 0.0% | 8.3% | 0.0% |
| domain: mobile_service | 12 | 0.0% | 16.7% | 58.3% | 25.0% |
| domain: motor_insurance | 12 | 8.3% | 58.3% | 100.0% | 58.3% |
| domain: permits | 12 | 0.0% | 25.0% | 75.0% | 25.0% |
| domain: pharmacy | 12 | 0.0% | 25.0% | 66.7% | 25.0% |
| domain: repair | 12 | 0.0% | 16.7% | 25.0% | 33.3% |
| domain: scheduling | 12 | 0.0% | 25.0% | 75.0% | 25.0% |
| domain: tech_support | 12 | 0.0% | 41.7% | 75.0% | 50.0% |
| domain: travel | 12 | 0.0% | 41.7% | 66.7% | 41.7% |
| bucket: 1-2 | 56 | 1.8% | 41.1% | 71.4% | 41.1% |
| bucket: 12-20 | 56 | 1.8% | 25.0% | 67.9% | 28.6% |
| bucket: 5-8 | 56 | 0.0% | 32.1% | 69.6% | 35.7% |

### Failure tags

- `STATE_BELIEF_ERROR`: 461 (95.4% of failed trajectories)
- `EARLY_CLUE_LOSS`: 208 (43.1% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 87 (18.0% of failed trajectories)
- `PREMATURE_CLOSE`: 44 (9.1% of failed trajectories)
- `STATE_SYNC_FAILURE`: 34 (7.0% of failed trajectories)
- `PREMATURE_ESCALATION`: 20 (4.1% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 16 (3.3% of failed trajectories)
- `BELIEF_REPORT_INVALID`: 12 (2.5% of failed trajectories)
- `REPEATED_ACTION`: 3 (0.6% of failed trajectories)

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired.

## google/gemini-3-flash-preview

- Coverage: 499/1512 trajectories (33.0%)
- Overall partial outcomes: 77.4% pre-gap, 44.3% post-gap, 42.9% both actions, 13.4% strict trajectory
- API calls: 7,522 (7,522 metered)
- Tokens: 10,029,916 (9,761,136 prompt + 268,780 completion)
- Reported API cost: $9.8109
- API request time: 1934.8 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 14.9% | 80.4% | 47.0% | 99.8% | 54.2% | 51.2% | $4.5797 |
| clue_removed | 163 | 3.7% | 66.9% | 27.0% | 100.0% | 25.2% | 32.5% | $4.4359 |
| transcript_only | 168 | 21.4% | 84.5% | 58.3% | 100.0% | 57.1% | 64.3% | $0.7953 |

### Belief probability metrics

| Condition | Brier | NLL | Normalized entropy | ECE | Revision gain | Stale mass |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0.459 | 4.833 | 0.142 | 0.200 | 0.309 | 0.020 |
| clue_removed | 0.893 | 8.785 | 0.263 | 0.392 | 0.227 | 0.018 |
| transcript_only | 0.320 | 2.811 | 0.123 | 0.142 | 0.413 | 0.025 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 163 | 14 | 19.8% | 8.3% to 30.5% | 0.0059 |
| Full audio - clue removed, full trajectory | 163 | 14 | 11.4% | 4.8% to 17.9% | 0.0078 |
| Hidden user action - full audio, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, pre-gap action | 168 | 14 | 4.2% | -4.2% to 13.7% | 0.4688 |
| Transcript - full audio, post-gap action | 168 | 14 | 11.3% | -0.6% to 23.8% | 0.1274 |
| Transcript - full audio, immediate belief | 168 | 14 | 13.1% | 5.4% to 20.8% | 0.0127 |
| Transcript - full audio, strict trajectory | 168 | 14 | 6.5% | -1.2% to 14.9% | 0.1885 |
| Full audio - no-state-change gap, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Neutral audio - full audio, immediate belief | 0 | 0 | N/A | N/A to N/A | N/A |

### Prosody selectivity

- Identical-transcript pairs: 0; unique stimuli: 0.
- High-affect style accuracy: N/A [N/A, N/A].
- Low-affect style accuracy: N/A [N/A, N/A].
- Both deliveries correct: N/A [N/A, N/A] (random pair chance N/A).
- Directional style contrast: N/A [N/A, N/A].
- Technical-action invariance: N/A [N/A, N/A].
- Post-observation top-belief invariance: N/A [N/A, N/A].
- Post-observation belief JSD: N/A [N/A, N/A].
- Pre-final belief JSD: N/A [N/A, N/A].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 47.0% | 14.9% | 16.7% | 3.6% | 75.0% |
| transcript_only | 84 | 58.3% | 21.4% | 32.1% | 6.0% | 59.5% |
| clue_removed | 80 | 27.0% | 3.7% | 3.8% | 1.2% | 41.2% |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 8.3% | 50.0% | 100.0% | 50.0% |
| domain: banking | 12 | 25.0% | 66.7% | 100.0% | 66.7% |
| domain: education | 12 | 25.0% | 58.3% | 75.0% | 58.3% |
| domain: energy | 12 | 8.3% | 33.3% | 58.3% | 33.3% |
| domain: housing | 12 | 41.7% | 58.3% | 100.0% | 58.3% |
| domain: logistics | 12 | 16.7% | 25.0% | 50.0% | 33.3% |
| domain: mobile_service | 12 | 0.0% | 25.0% | 50.0% | 25.0% |
| domain: motor_insurance | 12 | 25.0% | 33.3% | 91.7% | 41.7% |
| domain: permits | 12 | 33.3% | 75.0% | 83.3% | 75.0% |
| domain: pharmacy | 12 | 16.7% | 66.7% | 91.7% | 66.7% |
| domain: repair | 12 | 8.3% | 33.3% | 58.3% | 33.3% |
| domain: scheduling | 12 | 0.0% | 25.0% | 75.0% | 33.3% |
| domain: tech_support | 12 | 0.0% | 41.7% | 100.0% | 41.7% |
| domain: travel | 12 | 0.0% | 41.7% | 91.7% | 41.7% |
| bucket: 1-2 | 56 | 10.7% | 41.1% | 75.0% | 42.9% |
| bucket: 12-20 | 56 | 19.6% | 48.2% | 82.1% | 48.2% |
| bucket: 5-8 | 56 | 14.3% | 46.4% | 83.9% | 50.0% |

### Failure tags

- `STATE_BELIEF_ERROR`: 378 (87.5% of failed trajectories)
- `EARLY_CLUE_LOSS`: 169 (39.1% of failed trajectories)
- `PREMATURE_CLOSE`: 43 (10.0% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 42 (9.7% of failed trajectories)
- `STATE_SYNC_FAILURE`: 33 (7.6% of failed trajectories)
- `PREMATURE_ESCALATION`: 23 (5.3% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 6 (1.4% of failed trajectories)
- `BELIEF_REPORT_INVALID`: 1 (0.2% of failed trajectories)
- `REPEATED_ACTION`: 1 (0.2% of failed trajectories)

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired.

## openai/gpt-audio-mini

- Coverage: 336/1512 trajectories (22.2%)
- Overall partial outcomes: 60.4% pre-gap, 24.4% post-gap, 20.2% both actions, 0.3% strict trajectory
- API calls: 5,107 (5,107 metered)
- Tokens: 4,912,308 (4,688,129 prompt + 224,179 completion)
- Reported API cost: $3.3509
- API request time: 1183.9 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 168 | 0.0% | 65.5% | 22.0% | 99.4% | 17.9% | 31.0% | $1.6853 |
| clue_removed | 168 | 0.6% | 55.4% | 26.8% | 99.8% | 15.5% | 17.3% | $1.6656 |

### Belief probability metrics

| Condition | Brier | NLL | Normalized entropy | ECE | Revision gain | Stale mass |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 0.559 | 1.326 | 0.803 | 0.078 | -0.010 | 0.103 |
| clue_removed | 0.678 | 1.228 | 0.888 | 0.148 | 0.045 | 0.115 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 168 | 14 | -4.8% | -14.3% to 5.4% | 0.4336 |
| Full audio - clue removed, full trajectory | 168 | 14 | -0.6% | -1.8% to 0.0% | 1.0000 |
| Hidden user action - full audio, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, pre-gap action | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, post-gap action | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, immediate belief | 0 | 0 | N/A | N/A to N/A | N/A |
| Transcript - full audio, strict trajectory | 0 | 0 | N/A | N/A to N/A | N/A |
| Full audio - no-state-change gap, post-gap | 0 | 0 | N/A | N/A to N/A | N/A |
| Neutral audio - full audio, immediate belief | 0 | 0 | N/A | N/A to N/A | N/A |

### Prosody selectivity

- Identical-transcript pairs: 0; unique stimuli: 0.
- High-affect style accuracy: N/A [N/A, N/A].
- Low-affect style accuracy: N/A [N/A, N/A].
- Both deliveries correct: N/A [N/A, N/A] (random pair chance N/A).
- Directional style contrast: N/A [N/A, N/A].
- Technical-action invariance: N/A [N/A, N/A].
- Post-observation top-belief invariance: N/A [N/A, N/A].
- Post-observation belief JSD: N/A [N/A, N/A].
- Pre-final belief JSD: N/A [N/A, N/A].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 22.0% | 0.0% | 1.2% | 0.0% | 36.9% |
| clue_removed | 84 | 26.8% | 0.6% | 0.0% | 0.0% | 31.0% |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 12 | 0.0% | 0.0% | 100.0% | 0.0% |
| domain: banking | 12 | 0.0% | 50.0% | 91.7% | 50.0% |
| domain: education | 12 | 0.0% | 8.3% | 58.3% | 8.3% |
| domain: energy | 12 | 0.0% | 16.7% | 66.7% | 16.7% |
| domain: housing | 12 | 0.0% | 50.0% | 100.0% | 50.0% |
| domain: logistics | 12 | 0.0% | 8.3% | 25.0% | 8.3% |
| domain: mobile_service | 12 | 0.0% | 16.7% | 66.7% | 16.7% |
| domain: motor_insurance | 12 | 0.0% | 0.0% | 25.0% | 8.3% |
| domain: permits | 12 | 0.0% | 8.3% | 58.3% | 16.7% |
| domain: pharmacy | 12 | 0.0% | 0.0% | 50.0% | 8.3% |
| domain: repair | 12 | 0.0% | 25.0% | 83.3% | 33.3% |
| domain: scheduling | 12 | 0.0% | 0.0% | 41.7% | 8.3% |
| domain: tech_support | 12 | 0.0% | 25.0% | 58.3% | 33.3% |
| domain: travel | 12 | 0.0% | 50.0% | 91.7% | 50.0% |
| bucket: 1-2 | 56 | 0.0% | 14.3% | 64.3% | 17.9% |
| bucket: 12-20 | 56 | 0.0% | 19.6% | 69.6% | 23.2% |
| bucket: 5-8 | 56 | 0.0% | 21.4% | 62.5% | 25.0% |

### Failure tags

- `STATE_BELIEF_ERROR`: 328 (97.9% of failed trajectories)
- `EARLY_CLUE_LOSS`: 203 (60.6% of failed trajectories)
- `STATE_SYNC_FAILURE`: 36 (10.7% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 18 (5.4% of failed trajectories)
- `PREMATURE_ESCALATION`: 10 (3.0% of failed trajectories)
- `REPEATED_ACTION`: 9 (2.7% of failed trajectories)
- `BELIEF_REPORT_INVALID`: 4 (1.2% of failed trajectories)
- `PREMATURE_CLOSE`: 4 (1.2% of failed trajectories)

### Difficulty assessment

- The domain-clustered clue-ablation interval crosses zero; construct validity is not established for this model.

## Interpretation cautions

- Results contain 2 observed run seed(s); pass@k is labeled with the number actually available.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
