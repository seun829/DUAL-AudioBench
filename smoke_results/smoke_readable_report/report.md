# DUAL-AudioBench initial two-model report

- Result rows: 1
- Successfully evaluated: 1
- API/runtime errors: 0
- Models: google/gemini-2.5-flash

A trajectory passes only when both actions, any scored response style, all belief reports, and all hidden-state top predictions pass.

## google/gemini-2.5-flash

- API calls: 0 (0 metered)
- Tokens: 0 (0 prompt + 0 completion)
- Reported API cost: $0.0000
- API request time: 0.0 minutes

### Condition metrics

| Condition | n | Full pass | Pre | Post | Belief valid | Belief pre | Belief post | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| transcript_only | 1 | 0.0% | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | $0.0000 |

### Matched controls

| Control | Paired n | Effect |
|---|---:|---:|
| Full audio − clue removed, post-gap | 0 | — |
| Full audio − clue removed, full trajectory | 0 | — |
| Hidden user action − full audio, post-gap | 0 | — |
| Prosody high+low both correct | 0 | — |

### Full-audio slices

| Slice | n | Full pass | Two-action pass | Pre | Post |
|---|---:|---:|---:|---:|---:|

### Failure tags

- `BELIEF_REPORT_INVALID`: 1 (50.0% of tags)
- `STATE_BELIEF_ERROR`: 1 (50.0% of tags)

### Difficulty assessment

- No obvious ceiling or ineffective-clue warning fired in this one-seed run.

## Interpretation cautions

- This is one seed, so it is an initial pass rather than a stable estimate of stochastic model reliability.
- `transcript_only` is a control; audio conditions replay synthesized alternating turns.
- Human annotation and audible-prosody validation remain separate validation steps and are not replaced by model scores.
