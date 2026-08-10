# Schema-v0.4 paid experiment plan

## Confirmatory matrix

| Run | Conditions | Seeds | Trajectories |
|---|---|---:|---:|
| Gemini 2.5 headline | full audio, transcript, clue removed, prosody high, prosody low | 2 | 840 |
| Gemini 3 headline | full audio, transcript, clue removed, prosody high, prosody low | 2 | 840 |
| Gemini 2.5 controls | no-state-change gap, neutral audio | 2 | 336 |
| Gemini 3 controls | no-state-change gap, neutral audio | 2 | 336 |
| **Total** | 7 conditions on 2 models | 2 | **2,352** |

The two controls reuse the matching `full_audio` rows from the headline run.
Inference pairs by scenario and seed, averages sibling variants inside domain,
then bootstraps/sign-flips the 14 independent domain effects.

## Measured execution properties

- Each long audio trajectory makes approximately 14 model calls.
- Initial paid gates completed with zero API errors on both models.
- Audio trajectories currently average about $0.021; transcript trajectories
  average roughly $0.002–$0.004.
- Projected matrix cost is approximately $43, recorded per trajectory rather
  than inferred from file duration.
- Twelve headline shards and six control shards run per model. Outputs and WAV
  caches are process-isolated and resumable.

Check progress with:

```powershell
scripts/paid_v04_status.ps1 -RunSlug `
  gemini25_headline,gemini3_headline,gemini25_controls,gemini3_controls
```

After every shard is complete, generate indented JSON, Markdown, CSV, paired
deltas, matrices, and curves with:

```powershell
scripts/finalize_paid_v04.ps1 -RunSlug `
  gemini25_headline,gemini3_headline,gemini25_controls,gemini3_controls
```

Raw JSONL remains one object per line because that format enables atomic
checkpointing and crash-safe resume. The finalizer always creates readable
indented JSON sidecars; no one-line JSONL is intended as the human-facing
report.
