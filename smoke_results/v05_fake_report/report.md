# DUAL-AudioBench evaluation report

- Raw attempt rows: 756
- Unique completed trajectories: 756
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 0
- Models: fake

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## fake

- Coverage: 756/756 trajectories (100.0%)
- Overall partial outcomes: 72.8% pre-gap, 70.4% post-gap, 55.0% both actions, 13.0% strict trajectory
- API calls: 0 (0 metered)
- Tokens: 0 (0 prompt + 0 completion)
- Reported API cost: $0.0000
- API request time: 0.0 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 84 | 11.9% | 73.8% | 72.6% | 100.0% | 47.6% | 42.9% | $0.0000 |
| gap_no_state_change | 84 | 11.9% | 73.8% | 72.6% | 100.0% | 47.6% | 42.9% | $0.0000 |
| state_change_short | 84 | 35.7% | 95.2% | 90.5% | 100.0% | 79.8% | 67.9% | $0.0000 |
| clue_removed | 84 | 0.0% | 42.9% | 34.5% | 100.0% | 22.6% | 17.9% | $0.0000 |
| transcript_only | 84 | 11.9% | 73.8% | 72.6% | 100.0% | 47.6% | 42.9% | $0.0000 |
| neutral_audio | 84 | 11.9% | 73.8% | 72.6% | 100.0% | 47.6% | 42.9% | $0.0000 |
| hidden_user_action | 84 | 11.9% | 73.8% | 72.6% | 100.0% | 47.6% | 42.9% | $0.0000 |
| prosody_high | 84 | 10.7% | 73.8% | 72.6% | 100.0% | 47.6% | 42.9% | $0.0000 |
| prosody_low | 84 | 10.7% | 73.8% | 72.6% | 100.0% | 47.6% | 42.9% | $0.0000 |

### Matched controls

| Control | Paired n | Domains | Effect | 95% CI | p |
|---|---:|---:|---:|---:|---:|
| Full audio - clue removed, post-gap | 84 | 14 | 38.1% | 26.2% to 50.0% | 0.0005 |
| Full audio - clue removed, full trajectory | 84 | 14 | 11.9% | 6.0% to 19.0% | 0.0078 |
| Hidden user action - full audio, post-gap | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, pre-gap action | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, post-gap action | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, immediate belief | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Transcript - full audio, strict trajectory | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Full audio - no-state-change gap, post-gap | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |
| Neutral audio - full audio, immediate belief | 84 | 14 | 0.0% | 0.0% to 0.0% | 1.0000 |

### Prosody selectivity

- Identical-transcript pairs: 84; unique stimuli: 84.
- High-affect style accuracy: 82.1% [73.8%, 89.3%].
- Low-affect style accuracy: 82.1% [73.8%, 89.3%].
- Both deliveries correct: 82.1% [73.8%, 89.3%] (random pair chance 6.2%).
- Directional style contrast: 73.8% [63.1%, 84.5%].
- Technical-action invariance: 100.0% [100.0%, 100.0%].
- Post-observation top-belief invariance: 100.0% [100.0%, 100.0%].
- Post-observation belief JSD: 0.000 [0.000, 0.000].
- Pre-final belief JSD: 0.000 [0.000, 0.000].

### Causal clue counterfactuals

Each pair changes only the early clue and corresponding hidden branch. Gold post-gap actions differ. After clue removal, a deterministic policy cannot exceed 50% post-gap accuracy across balanced indistinguishable branches.

| Condition | Pairs | Post | Strict | Both post-correct | Both strict | Action changes |
|---|---:|---:|---:|---:|---:|---:|
| full_audio | 42 | 72.6% | 11.9% | 57.1% | 2.4% | 88.1% |
| transcript_only | 42 | 72.6% | 11.9% | 57.1% | 2.4% | 88.1% |
| clue_removed | 42 | 34.5% | 0.0% | 14.3% | 0.0% | 76.2% |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: account_access | 6 | 16.7% | 66.7% | 66.7% | 66.7% |
| domain: banking | 6 | 0.0% | 33.3% | 50.0% | 50.0% |
| domain: education | 6 | 0.0% | 33.3% | 50.0% | 83.3% |
| domain: energy | 6 | 16.7% | 50.0% | 100.0% | 50.0% |
| domain: housing | 6 | 0.0% | 50.0% | 66.7% | 66.7% |
| domain: logistics | 6 | 16.7% | 66.7% | 83.3% | 66.7% |
| domain: mobile_service | 6 | 16.7% | 50.0% | 50.0% | 66.7% |
| domain: motor_insurance | 6 | 50.0% | 50.0% | 66.7% | 83.3% |
| domain: permits | 6 | 0.0% | 50.0% | 83.3% | 50.0% |
| domain: pharmacy | 6 | 16.7% | 83.3% | 83.3% | 100.0% |
| domain: repair | 6 | 0.0% | 66.7% | 83.3% | 83.3% |
| domain: scheduling | 6 | 16.7% | 66.7% | 66.7% | 83.3% |
| domain: tech_support | 6 | 0.0% | 100.0% | 100.0% | 100.0% |
| domain: travel | 6 | 16.7% | 66.7% | 83.3% | 66.7% |
| bucket: 1-2 | 28 | 28.6% | 85.7% | 92.9% | 92.9% |
| bucket: 12-20 | 28 | 0.0% | 21.4% | 42.9% | 46.4% |
| bucket: 5-8 | 28 | 7.1% | 71.4% | 85.7% | 78.6% |

### Failure tags

- `STATE_BELIEF_ERROR`: 635 (96.5% of failed trajectories)
- `EARLY_CLUE_LOSS`: 101 (15.3% of failed trajectories)
- `PREMATURE_ESCALATION`: 101 (15.3% of failed trajectories)
- `PREMATURE_CLOSE`: 97 (14.7% of failed trajectories)
- `TIME_INFERENCE_FAILURE`: 42 (6.4% of failed trajectories)
- `PROSODY_GROUNDING_FAILURE`: 30 (4.6% of failed trajectories)
- `STATE_SYNC_FAILURE`: 26 (4.0% of failed trajectories)
- `ACTION_SELECTION_FAILURE`: 12 (1.8% of failed trajectories)
- `REPEATED_ACTION`: 3 (0.5% of failed trajectories)

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired.

## Interpretation cautions

- Results contain 1 observed run seed(s); pass@k is labeled with the number actually available.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
