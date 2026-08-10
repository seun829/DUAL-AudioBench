# Schema v0.4 implementation summary

Schema v0.4 is a versioned follow-up experiment. The original 84 files in
`data/scenarios/` remain schema v0.3 and were not regenerated. New tasks live
in `data/scenarios_v04/`, use distinct `_s04` IDs, and must not be pooled with
v0.3 absolute rates.

## Scenario and prompt fixes

- Added short public meanings for every belief value and included them in the
  belief-only and action prompts.
- Replaced false clue-ablation counterclaims with matched statements of
  uncertainty, preserving turn count without inserting opposite evidence.
- Added an explicit prosody stimulus ID, three carrier-transcript variants,
  two user voices, and four category-specific response approaches.
- Preserved identical words, hidden state, menus, and seed-dependent option
  order within each high/low prosody pair.
- Kept technical action and belief gold invariant across prosody; only the
  expected conversational response approach changes.

## Runtime and reproducibility fixes

- Added configurable eSpeak/FFmpeg paths and per-output audio/replay caches.
  Parallel shards no longer race on shared WAV files.
- Added crash-resumable task sharding and schema-mixing protection.
- Added an OpenRouter adapter with capped output, strict JSON Schema responses,
  retry handling, resolved-model logging, and per-trajectory tokens, cost, and
  request latency.
- Added hidden paid-run and status scripts whose manifests list conditions,
  expected rows, output files, process IDs, and actual accumulated cost.
- Preserved JSONL for streaming/resume while producing indented JSON,
  Markdown, and CSV sidecars for people.

## Statistical and reporting fixes

- Replaced sibling-scenario inference with equal-weight domain-clustered
  bootstrap confidence intervals and exact domain sign-flip tests.
- Labels repeated sampling as pass@k using the number of observed seeds; two
  runs are pass@2, never pass@5.
- Reports the audio/text effect separately for pre-gap action, post-gap
  action, immediate post-observation belief, and strict trajectory success.
- Adds prosody high/low accuracy, both-correct rate, directional style
  contrast, technical-action invariance, top-belief invariance, belief JSD,
  delivery-category slices, and clustered intervals.
- Adds confidence bands to retention curves plus separate modality-belief and
  prosody-selectivity figures.
- Saves readable Markdown, indented JSON, metric CSV, trajectory CSV, paired
  deltas, and belief/action matrices.

## Verification completed

- 84 v0.3 files remain schema 0.3; 84 separate v0.4 files are schema 0.4.
- The full 84 x 9-condition fake run completed 756/756 trajectories with zero
  runtime errors and generated every report/figure artifact.
- All 84 high/low pairs had identical resumed transcripts.
- Forty-seven focused tests pass.
- A paid Gemini 2.5 Flash audio gate completed 14/14 metered calls with no API
  errors: 20,594 tokens, $0.0203 reported cost, and 71.9 seconds end to end.
- The gate passed both technical actions but failed strict success because the
  belief top state was wrong, confirming independent action/belief scoring.
- A second prosody gate verified strict schemas and readable `W/X/Y/Z` style
  menus on both Gemini 2.5 Flash and Gemini 3 Flash, with 28/28 metered calls,
  valid belief reports, and no API errors.

## Experiment separation

The 1,344 existing schema-v0.3 trajectories remain usable as the pilot result.
Schema v0.4 changes task wording, belief instructions, prosody stimuli, and
inference clustering, so report it as a confirmatory follow-up. Within-version
paired effects are comparable; absolute rates across versions are descriptive
only.

Human validation and key rotation were intentionally not performed.
