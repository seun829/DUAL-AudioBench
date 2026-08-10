# DUAL-AudioBench evaluation report

- Raw attempt rows: 14
- Unique completed trajectories: 14
- Duplicate successful rows ignored in metrics: 0
- API/runtime error attempts: 0
- Models: google/gemini-2.5-flash, mistralai/voxtral-small-24b-2507

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## google/gemini-2.5-flash

- Coverage: 7/162 trajectories (4.3%)
- Overall partial outcomes: 100.0% pre-gap, 71.4% post-gap, 71.4% both actions, 0.0% strict trajectory
- API calls: 98 (98 metered)
- Tokens: 125,323 (122,740 prompt + 2,583 completion)
- Reported API cost: $0.1187
- API request time: 4.8 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 1 | 0.0% | 100.0% | 100.0% | 66.7% | 0.0% | 0.0% | $0.0204 |
| gap_no_state_change | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | $0.0196 |
| state_change_short | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | $0.0182 |
| clue_removed | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 0.0% | 0.0% | $0.0185 |
| transcript_only | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | $0.0020 |
| hidden_user_action | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 0.0% | 0.0% | $0.0198 |
| prosody_high | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | $0.0202 |

### Matched controls

| Control | Paired n | Effect |
|---|---:|---:|
| Full audio - clue removed, post-gap | 1 | 0.0% |
| Full audio - clue removed, full trajectory | 1 | 0.0% |
| Hidden user action - full audio, post-gap | 1 | -100.0% |
| Prosody high+low both correct | 0 | N/A |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: travel | 1 | 0.0% | 100.0% | 100.0% | 100.0% |
| bucket: 12-20 | 1 | 0.0% | 100.0% | 100.0% | 100.0% |

### Failure tags

- `STATE_BELIEF_ERROR`: 6 (75.0% of tags)
- `BELIEF_REPORT_INVALID`: 1 (12.5% of tags)
- `PREMATURE_CLOSE`: 1 (12.5% of tags)

### Difficulty assessment

- Preliminary only: the full-audio subset scored 100.0% on both actions, but n=1 is too small to establish a ceiling.
- Actions are easy while structured belief reporting dominates failures; difficulty is formatting-heavy rather than behavioral.
- Clue removal changes post-gap accuracy by less than five points; the benchmark may not require the intended early clue.

## mistralai/voxtral-small-24b-2507

- Coverage: 7/162 trajectories (4.3%)
- Overall partial outcomes: 100.0% pre-gap, 71.4% post-gap, 71.4% both actions, 0.0% strict trajectory
- API calls: 98 (98 metered)
- Tokens: 17,576 (15,061 prompt + 2,515 completion)
- Reported API cost: $0.4009
- API request time: 5.2 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| full_audio | 2 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | $0.1324 |
| gap_no_state_change | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | $0.0674 |
| state_change_short | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | $0.0654 |
| clue_removed | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 0.0% | 0.0% | $0.0669 |
| transcript_only | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | $0.0004 |
| hidden_user_action | 1 | 0.0% | 100.0% | 0.0% | 100.0% | 100.0% | 0.0% | $0.0684 |

### Matched controls

| Control | Paired n | Effect |
|---|---:|---:|
| Full audio - clue removed, post-gap | 1 | 0.0% |
| Full audio - clue removed, full trajectory | 1 | 0.0% |
| Hidden user action - full audio, post-gap | 1 | -100.0% |
| Prosody high+low both correct | 0 | N/A |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|
| domain: travel | 2 | 0.0% | 100.0% | 100.0% | 100.0% |
| bucket: 12-20 | 2 | 0.0% | 100.0% | 100.0% | 100.0% |

### Failure tags

- `STATE_BELIEF_ERROR`: 6 (100.0% of tags)

### Difficulty assessment

- Preliminary only: the full-audio subset scored 100.0% on both actions, but n=2 is too small to establish a ceiling.
- Clue removal changes post-gap accuracy by less than five points; the benchmark may not require the intended early clue.

## Interpretation cautions

- This is one seed, so it is an initial pass rather than a stable estimate of stochastic model reliability.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
