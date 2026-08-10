# Schema v0.5 causal-clue design

Schema v0.5 is the main benchmark version. It repairs a construct-validity
failure found in v0.4 while leaving every v0.3 and v0.4 task and result frozen.

## Why v0.4 showed little clue dependence

In v0.4, removing the early clue changed only one public utterance. It did not
change the initialized hidden state, the deterministic transition, or the gold
post-gap action. The resumed user observation then named the terminal outcome
directly (for example, rejected or unmatched). A model could therefore ignore
the clue and recover the correct action from the last turn. The ablation was a
memory perturbation, but it was not a causal test of clue use.

The old automated checks established deterministic transitions, valid menus,
and non-leaking option text. They did not assert that changing the clue changed
the terminal hidden state and required action. Schema v0.5 adds that missing
invariant.

## Counterfactual construction

Each of 14 domains, three clue-distance buckets, and two causal branches makes
84 separately identified tasks. The branches form 42 matched pairs:

- `misaligned`: the early fact conflicts with the rule, producing a repairable
  terminal state and a domain-specific recovery action;
- `aligned`: the early fact satisfies the rule, producing successful completion
  and `close_case` as the correct action.

The dialogue states a short generic causal rule before asking for the clue. The
paired clue then changes one relevant fact. All filler turns, voices, option
sets, option ordering, and the post-gap words are held constant. The resumed
observation says the process ended but withholds its hidden result, forcing the
model to combine the early fact with the stated rule.

For example, the router pair states that intact saved configuration permits a
firmware update to finish, whereas corrupted configuration leaves it stuck.
One clue says the saved data was intact and the other says it was corrupted.
Both branches later hear that the maintenance cycle ended and its result display
is blank. The correct actions are consequently `close_case` and
`inspect_persistent_state`.

## Enforced invariants

The generator and tests require all of the following:

1. Both branches exist for every domain and distance bucket.
2. Their terminal hidden outcomes differ.
3. Their correct post-gap actions differ.
4. With the original clues, public histories differ at exactly one clue turn.
5. With the clue ablated, public user histories are identical.
6. Paired menu contents and randomized label order are identical.
7. The standard post-gap observation is identical and does not disclose which
   hidden branch occurred.
8. The no-state-change and hidden-user-action controls remain truthfully
   state-conditioned rather than using the ambiguous standard observation.
9. `causal_alignment` is explicitly included in the belief schema and scored.
10. The prosody pair preserves words, state, and technical gold action.

Balanced indistinguishable branches imply a 50% expected post-gap ceiling for
a clue-independent policy. Unlike the v0.4 ablation, an above-ceiling result can
now be interpreted as evidence of retaining and applying the clue. Statistical
inference must still use matched scenario/seed effects clustered by the 14
domains.

## Human-solvability judgment

The tasks are structurally human-solvable in principle: every causal rule is
given in the conversation; no outside domain knowledge is necessary; each clue
maps unambiguously to one of two outcomes; the correct action exists exactly
once in the menu; and the resumption explicitly asks the participant to use the
earlier detail. This is an expert structural audit, not a measured human
baseline. Before publication, a small blinded study should target roughly
85--95% post-gap action accuracy. Below 80% would suggest ambiguity or burden;
100% is unnecessary and may indicate an overly easy task.

## Validation completed

- 84 schema-v0.5 files generated in `data/scenarios_v05/`.
- 55 repository tests pass, including eight causal-pair/reporting regression
  tests.
- A 756-trajectory fake-agent run covers all 84 tasks and all nine conditions
  with zero runtime errors.
- The reporting pipeline produces readable Markdown, indented JSON, CSV,
  retention/modality/prosody curves, and causal-clue counterfactual metrics.

The fake model is an orchestration fixture that reads runner-private gold
labels. Its scores are not benchmark evidence.
