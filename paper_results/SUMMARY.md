# DUAL-AudioBench — cross-model results

**Benchmark:** 84 schema-v0.3 scenarios across 14 domains (expanded from 18 / 3 domains).
**Runs:** 1344 real-model trajectories, **0 errors** after one retried upstream 429.
**Statistics:** scenario-clustered bootstrap, 20k resamples over the 84 scenarios. Clustering
matters — 168 trials per condition are 84 scenarios × 2 seeds, not 168 independent draws, and an
unclustered test inflates significance by roughly two orders of magnitude on this data.

| Model | Lab | Conditions | Trajectories |
|---|---|---|---|
| `google/gemini-2.5-flash` | Google | full_audio, transcript_only, clue_removed | 504 |
| `google/gemini-3-flash-preview` | Google | full_audio, transcript_only, clue_removed | 504 |
| `openai/gpt-audio-mini` | OpenAI | full_audio, clue_removed only¹ | 336 |

¹ `gpt-audio-mini` is audio-native and **refuses text-only requests**, so it cannot run
`transcript_only`. Both of its conditions are audio, so it still contributes a cross-lab test of the
clue ablation.

---

## 1. Benchmark validity: the clue ablation replicates

| Model | pass@1 | Ablation (full − clue_removed, post-gap) | 95% CI | p |
|---|---|---|---|---|
| `gpt-audio-mini` | 7.7% | −4.8% | [−13.7, +4.8] | 0.340 ns |
| `gemini-2.5-flash` | 23.8% | **+11.9%** | [+2.4, +21.4] | **0.019 \*** |
| `gemini-3-flash` | 51.8% | **+20.2%** | [+11.3, +29.8] | **<0.001 \*\*\*** |

The tasks measurably depend on the clue, in both models capable of the task, and **the dependence
grows with capability**. `gpt-audio-mini` shows nothing because it is near the floor (pass@1 7.7%,
belief 15.5%) — a model that never extracts the clue cannot lose anything when it is removed. Read
the ablation as a validity check that requires a minimally capable subject, not as evidence against
the benchmark.

**This supersedes the earlier 18-scenario result** (+12.2%, p=0.169, ns), which was a power failure:
the effect size barely moved (12.2% → 11.9% on the same model) while the CI tightened enough to
exclude zero. Estimated power for this effect went from 31% at 18 scenarios to 86% at 84.

## 2. Main finding: audio degrades belief tracking, not action selection

Modality effect (`transcript_only` − `full_audio`), decomposed:

| Component | gemini-2.5-flash | gemini-3-flash |
|---|---|---|
| pre-gap action | −4.8% (0.306 ns) | −4.8% (0.110 ns) |
| post-gap action | **+31.0% (<0.001 \*\*\*)** | +2.4% (0.571 ns) |
| **belief, 3 checkpoints** | **+17.3% (0.001 \*\*)** | **+14.3% (<0.001 \*\*\*)** |
| composite pass@1 | +19.0% (<0.001 \*\*\*) | +10.7% (0.018 \*) |

Three claims, each supported by two independent models:

1. **Audio never hurts before the gap.** Null in both models. This rules out a perception or
   TTS-quality explanation — if the model could not parse synthetic speech, pre-gap accuracy would
   fall too. It does not.
2. **The post-gap *action* penalty is a capability limitation.** Large in gemini-2.5-flash (+31.0%),
   entirely gone in gemini-3-flash (+2.4%, ns).
3. **The *belief* penalty persists.** +17.3% → +14.3%, barely attenuated, still highly significant in
   the stronger model even though its action penalty has vanished.

**Belief tracking is the durable audio deficit.** A newer model closes the action gap while leaving
the belief gap essentially intact — which is only visible because the benchmark scores beliefs
separately from actions.

Note the mechanism changed even as the effect held: stale-belief mass was 9.7% vs 2.5% (audio vs
text) in gemini-2.5-flash but 0.3% vs 0.1% in gemini-3-flash. The newer model no longer clings to
stale states; its belief reports are simply less accurate under audio. Do not describe the deficit as
"stale belief" — that was specific to the weaker model.

## 3. Headline rates

| Model | Condition | pass@1 | pre-gap | post-gap | belief |
|---|---|---|---|---|---|
| gemini-2.5-flash | full_audio | 23.8% | 78.0% | 45.8% | 37.5% |
| | transcript_only | 42.9% | 73.2% | 76.8% | 54.8% |
| | clue_removed | 19.0% | 76.2% | 33.9% | 41.1% |
| gemini-3-flash | full_audio | 51.8% | 94.6% | 75.6% | 67.9% |
| | transcript_only | 62.5% | 89.9% | 78.0% | 82.1% |
| | clue_removed | 42.9% | 94.0% | 55.4% | 73.2% |
| gpt-audio-mini | full_audio | 7.7% | 65.5% | 49.4% | 15.5% |
| | clue_removed | 5.4% | 67.3% | 54.2% | 13.7% |

Chance floors: single action 20.0%, two independent actions 4.0%, full action+belief 0.060%.

## 4. Limitations to state in the paper

- **The ablation is a pooled result.** Significant across all 84 scenarios, but neither the original
  3 domains (+22.2%, p=0.120) nor the new 11 (+9.1%, p=0.086) reaches significance alone. Do not
  claim per-domain robustness.
- **The modality claim rests on two models from one lab.** No non-Google audio model tested could run
  both modalities: OpenAI refuses text-only, Meta `muse-spark` and NVIDIA `nemotron-omni` failed
  outright, and Mistral `voxtral` worked but echoed the prompt's example distribution verbatim
  (degenerate beliefs) at 2.9× the cost.
- **All 14 domains share one structural schema** — a latent property invalidates the naive action.
  This is breadth of surface form, not of mechanism.
- **Prosody is unvalidated.** `espeak-ng` pitch/rate contrast is a pipeline fixture; `prosody_high/low`
  were not run and no claim about emotional speech is supported.
- **No human solvability baseline.** Still open, still the obvious reviewer question.
- **Difficulty shifted with the expanded pool.** gemini-2.5-flash full_audio pass@1 was 5.6% on the
  original 18 scenarios and 23.8% on 84 — the new domains are easier. Paired deltas are unaffected
  (all within-scenario), but absolute rates are not comparable across scenario pools.
- **Malformed JSON.** `transcript_only` replies occasionally break structurally: the model appends
  unsolicited commentary at the `state_belief` closing brace. Fix with
  `response_format: {type: "json_schema"}`; deferred here to preserve comparability.

## 5. Methods and reproduction notes

**Structured-output parsing is a silent correctness hazard.** In the earlier 18-scenario run,
**81 of 162 (50%)** decision replies parsed *only* after `_parse_json` was hardened to strip Markdown
fences, and every one of them carried a valid belief distribution. Unhardened, belief validity reads
~46% instead of 96% and every belief metric is void. Fence rate is strongly condition-dependent —
87% of `transcript_only` replies versus ~35-39% of audio replies — so a smoke test on one condition
will not surface it. The failure is loud rather than silent (`normalize_state_belief` omits rather
than inventing a uniform distribution, so bad rows surface as `BELIEF_REPORT_INVALID`), but the
consequence is a wrong headline result. Locked in by `tests/test_response_parsing.py`.

**Residual malformed JSON is a model behaviour, not a parser bug.** On `transcript_only` only, the
model sometimes appends unsolicited commentary exactly at the `state_belief` closing brace and
mangles it (`reasoning": "…`, a vestigial `",`, or injected prose). ~4% of decision replies, spread
evenly across domains, concentrated at the `pre_gap` stage. These are left unparsed rather than
repaired — repairing would invent data. Fix properly with `response_format: {type: "json_schema"}`.

**Model compatibility must be checked on every condition before committing a run.** `gpt-audio-mini`
passed an audio smoke test and then failed 100% of `transcript_only` calls; that cost a wasted run.
Probe both `ask()` and `ask_text()`, and time a multi-call sequence — single-call probes measure
token price but miss per-call latency and overhead, which is how `xiaomi/mimo-v2.5` was mis-estimated
at $3.42 / ~5h when it was really ~$14 / ~75h.

**Scenario pool construction.** 84 scenarios = 14 domain templates × 3 clue-distance buckets × 2
variants. Note that `--variants` does **not** create independent tasks: variants share an identical
clue, action menu, initial state, transition, and belief schema, differing only in filler order — so
raising `--variants` inflates apparent cluster count without adding power. Independent designs come
from new domains, which is why the expansion added 11 domains rather than more variants. The truly
independent unit is arguably the domain (14), not the scenario (84), so quoted power is mildly
optimistic.

Generation is guarded: `leak_guard` rejects any post-clue turn repeating ≥2 clue keywords, and
`choice_leak_guard` rejects a correct option that uniquely echoes clue vocabulary (it caught two real
leaks during authoring). Validation covers all 280 combinations of domain × pre-gap action × hidden
user action × external event, asserting determinism, schema membership, that every reachable state
has a resumed observation, and that every state-derived correct action appears in its own menu.
`tests/test_domains.py` is generic over `TEMPLATES`, so a newly added domain is covered
automatically. 28 tests pass.

## 6. Cost

| Run | Cost |
|---|---|
| gemini-2.5-flash, 504 traj | $6.09 |
| gemini-3-flash, 504 traj (+retry) | $7.75 |
| gpt-audio-mini audio-only, 336 traj | $2.93 |
| aborted probes (gpt-audio-mini text, MiMo) | $0.77 |
| earlier 18-scenario p5 run | $3.00 |
| **Total** | **$20.53** |

## Contents

```
trajectories/   raw JSONL, one row per trajectory, all three models + earlier p5
scores/         score.py reports, belief/action matrices, condition summaries, paired deltas
figures/        retention curves
usage/          measured per-run token counts and cost
benchmark/      templates.py, environment.py, and the 84 generated scenarios
```

Reproduce (per model, via `OPENROUTER_MODEL`):

```
python run_eval.py --model openrouter \
  --conditions full_audio,transcript_only,clue_removed \
  --passes 2 --out results/<name>.jsonl
```
