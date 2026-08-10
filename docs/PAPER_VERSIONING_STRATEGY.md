# Presenting v0.3, v0.4, and v0.5

Benchmark iteration is normal. What would be abnormal is pooling incompatible
versions, choosing the best-looking version after seeing scores, or presenting
earlier exploratory tests as independent confirmation. DUAL-AudioBench should
name v0.5 as the released benchmark and describe v0.3/v0.4 as development and
validation studies.

## Roles of the versions

| Version | Paper role | Appropriate claims | Do not do |
|---|---|---|---|
| v0.3 | Exploratory pilot | Motivated the action--belief dissociation and audio-replay hypothesis; established that the pipeline could expose diagnostic failures | Pool its rows with later versions or call it confirmatory |
| v0.4 | Validation and negative control study | Added stronger controls and prosody; showed that the original clue ablation did not establish causal clue use; supplies transparent evidence for redesign | Hide the null ablation, treat it as a v0.5 replication, or use it for headline benchmark rankings |
| v0.5 | Frozen main benchmark | All primary model comparisons, tables, curves, confidence intervals, and abstract/conclusion claims | Change tasks or scoring after seeing main results without issuing a new version |

The strongest narrative is not “three test sets.” It is a documented design
sequence:

```text
v0.3 exploratory signal
  -> v0.4 mechanism controls expose a noncausal clue shortcut
  -> v0.5 matched causal counterfactuals remove that shortcut
  -> frozen confirmatory evaluation
```

That sequence is a methodological contribution: the benchmark demonstrates
its own validation failure and repairs it with testable invariants.

## Main-paper result layout

Use v0.5 exclusively for the headline result section:

1. **Dataset/validity table:** 14 domains, 84 tasks, distance and branch
   balance, menu sizes, causal-pair invariants, and measured human accuracy when
   available.
2. **Main model table:** per-model results for all nine conditions, emphasizing
   strict trajectory, post-gap action, all-belief accuracy, calibration, and
   cost.
3. **Matched-effect table:** clue, modality, state-change, distance, and hidden
   user-action effects with clustered intervals and p-values.
4. **Retention figure:** post-gap action and belief performance across the three
   clue-distance buckets.
5. **Prosody figure/table:** paired style selectivity and technical/belief
   invariance. Prosody can be a centerpiece only after human audibility labels
   verify that the intended high/low contrasts are perceptible.
6. **Diagnostic figure/table:** belief/action matrix, stale-belief mass, revision
   gain, and failure tags.

Add a short “benchmark development and construct validation” subsection or an
appendix table for v0.3/v0.4. Report sample sizes, models, conditions, and effect
directions, including the v0.4 clue-ablation null. Earlier modality findings can
be labeled exploratory robustness evidence if their direction agrees with
v0.5; they are not additional v0.5 samples and not independent replications
because they share domains and benchmark machinery.

If v0.5 does not reproduce an earlier effect, report the discrepancy and base
the final claim on v0.5. The redesign intentionally changes the estimand from
remembering a helpful clue to applying a clue that causally determines hidden
state, so an effect-size shift is expected and scientifically informative.

## Suggested wording

Methods:

> We developed the benchmark iteratively. An exploratory pilot (v0.3) motivated
> the target failure mode. A controlled revision (v0.4) revealed that clue
> ablation did not alter task ground truth, preventing a causal interpretation.
> Before the main evaluation, we froze v0.5, which introduces balanced matched
> branches where a single early fact changes both the terminal hidden state and
> required recovery action. Unless explicitly labeled as development evidence,
> all reported benchmark results use v0.5.

Results:

> Results from v0.3 and v0.4 are reported separately as exploratory benchmark
> development studies and are never pooled with v0.5 estimates.

This framing is transparent, conventional for benchmark construction, and much
more defensible than pretending the benchmark was fully specified before the
pilot evidence existed.
