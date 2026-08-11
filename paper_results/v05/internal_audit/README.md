# Schema-v0.5 internal author audit

Two independent, readable audit packets are ready in `public/`, one for
`author_01` and one for `author_02`. Each contains all 84 scenarios in a
different randomized order with independently randomized menu labels.
Counterfactual siblings are never adjacent.

All four current booklets are stamped with scenario manifest
`e16319a791ab4600f88a33f7957e66eec18be262649caac03845c161119044b9`,
matching `paper_results/v05/SCENARIO_FREEZE.md`. The response sheets were reset
when the scenarios changed; do not reuse answers from an earlier packet.

## Blinding protocol

For each author:

1. Receive only that author's files from `public/`.
2. Read `author_XX_phase1_booklet.md` and complete the corresponding phase-1
   response CSV.
3. Save and timestamp the completed phase-1 CSV before opening phase 2.
4. Read `author_XX_phase2_booklet.md` and complete the phase-2 response CSV.
5. Do not inspect task JSON, source code, `private/`, or the other author's
   packet/responses until both phases are complete.

Phase 1 asks for the best pre-gap action and causal-alignment label using only
the public dialogue. Phase 2 discloses the benchmark operation that must be
assumed executed, presents the public resumption, and asks for terminal state
and final action. This separation prevents the declared operation from leaking
the phase-1 gold answer.

`causal_alignment` simply means **whether the clue matches the stated success
rule**. Select `aligned` when the clue satisfies the rule and `misaligned` when
it violates the rule. It is not asking whether the auditor agrees with the
benchmark answer.

Use exact labels from the booklets. Enter `yes` or `no` for answerability and an
ambiguity score from 1 (unambiguous) through 5 (not answerable). Evidence and
notes should identify any unclear wording or competing action.

## Private material

The files in `private/` map anonymous items and randomized labels back to
scenario IDs, executable gold states, and actions. Never distribute or commit
them before auditing is complete. The directory is ignored by Git.

## Scoring completed packets

After both authors finish:

```powershell
python -m dual_audio.evaluation.scenario_audit report `
  paper_results/v05/internal_audit author_01 author_02
```

This produces:

- `internal_audit_report.md`: readable gold accuracy and cross-author agreement;
- `internal_audit_metrics.json`: indented structured metrics;
- `adjudication.csv`: only items requiring author discussion.

Resolve every row in `adjudication.csv` before freezing the paid run. Report
this exercise as an **internal author audit**, not an independent human baseline.

## Regenerating or adding authors

```powershell
python -m dual_audio.evaluation.scenario_audit export `
  data/scenarios_v05 paper_results/v05/internal_audit `
  author_01 author_02 author_03
```

Regeneration is deterministic for a given auditor ID and unchanged scenario
files.
