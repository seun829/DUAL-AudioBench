# Independent failure-tag audit report

- Auditor: annotator_01
- Gold-set trajectories: 21
- Exact tag-set agreement: 33.3%
- Automatic-tag precision: 83.8%
- Automatic-tag recall: 55.4%
- Micro F1: 0.667

This is an independent single-annotator audit, not inter-annotator agreement.

| Tag | Automatic | Independent annotator | Match | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| `ACTION_SELECTION_FAILURE` | 1 | 6 | 1 | 100.0% | 16.7% |
| `EARLY_CLUE_LOSS` | 10 | 6 | 4 | 40.0% | 66.7% |
| `PREMATURE_CLOSE` | 1 | 1 | 1 | 100.0% | 100.0% |
| `PREMATURE_ESCALATION` | 1 | 5 | 1 | 100.0% | 20.0% |
| `REPEATED_ACTION` | 0 | 6 | 0 | --- | 0.0% |
| `STATE_BELIEF_ERROR` | 20 | 20 | 20 | 100.0% | 100.0% |
| `STATE_SYNC_FAILURE` | 1 | 5 | 1 | 100.0% | 20.0% |
| `TIME_INFERENCE_FAILURE` | 3 | 7 | 3 | 100.0% | 42.9% |
