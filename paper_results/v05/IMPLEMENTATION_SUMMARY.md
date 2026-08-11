# Schema-v0.5 implementation summary

## Scenario and methodology repairs

- Kept 84 tasks: 14 domains × 3 clue distances × 2 balanced causal branches.
- Made both branches share the same pre-gap outcome; the flight task no longer
  asks the model to know an unrevealed future delay.
- Reworded the aligned `close_case` option as a successful-outcome hypothesis
  instead of incorrectly closing merely because time passed.
- Made the hidden-user-action control change a scored state or action in every
  domain. The ordinary transition engine still derives the terminal result.
- Kept clue-removed pair inputs, voices, menus, and post-gap wording matched;
  its balanced deterministic ceiling remains 50%.

## Evaluation and reproducibility

- Added aggregate NLL and normalized entropy to JSON, CSV, and Markdown output.
- Added registered-condition coverage so a partial v0.5 grid cannot appear
  complete merely because its observed rows are internally complete.
- Added provider-count telemetry and omitted the unsupported reasoning field for
  non-Gemini models.
- Selected Gemini 2.5 Flash plus GPT Audio Mini for a cross-provider main panel;
  local Qwen2.5-Omni cannot run on this CPU-only machine.
- Frozen one confirmatory clue-dependence endpoint; modality, controls, and
  unvalidated synthetic prosody are secondary/exploratory.
- Added launch and finalization checks for the exact frozen scenario hash.

## Verification

- Scenario freeze: `e16319a791ab4600f88a33f7957e66eec18be262649caac03845c161119044b9`.
- 62 unit tests pass.
- All 84 tasks, 42 causal pairs, 9 conditions, and 4,536 off-gold transition
  paths pass the executable audit.
- The full local matrix completed 756/756 trajectories with zero execution
  errors; the audio gate produced valid 16 kHz mono WAVs.
- Readable reports produce indented JSON, Markdown, CSV, failure metrics, and
  retention/modality/prosody plots.

## Remaining release gates

- No paid v0.5 trajectory has run.
- The OpenRouter key is not configured locally, so balance and model
  compatibility cannot yet be checked.
- Both regenerated internal-author response packets are blank. They are stamped
  with the frozen scenario hash and must not reuse pre-revision answers.
- Prosody remains exploratory until listener validation; the author audit is not
  an independent human baseline.
