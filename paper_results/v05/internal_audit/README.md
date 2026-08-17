# Internal author audits

All three audits use the same prespecified 21-scenario gold set: the completed
25% subset in the author-1 scenario booklet. The subset contains one member of
21 different causal pairs, spans 13 domains and all three clue distances, and
includes 10 aligned and 11 misaligned scenarios.

These are internal construction and manipulation checks performed by one
author. They are not an independent human-performance baseline and do not
provide inter-rater agreement.

## 1. Scenario construction audit

The completed files are in `public/`:

- `author_01_phase1_booklet.md` and `author_01_phase1_responses.csv`
- `author_01_phase2_booklet.md` and `author_01_phase2_responses.csv`

Only the 21 prespecified rows are intended to be completed. The remaining rows
belong to the unaudited 75% and should stay blank. The completed subset recovered
the causal branch and delayed terminal state in all 21 items.

## 2. Failure-tag audit

Open:

- `failure_tags/public/author_01_failure_tag_booklet.md`
- `failure_tags/public/author_01_failure_tag_responses.csv`

The packet contains one failed trajectory for every gold-set scenario. Model
identity, evaluation condition, and automatic tags are hidden. For each item,
enter every tag supported by the visible trace, separated with semicolons, or
enter `NONE`. Also provide a short reason and confidence from 1 to 5.

After all 21 rows are complete, score the packet with:

```powershell
python -m dual_audio.evaluation.failure_tag_audit report `
  paper_results/v05/internal_audit author_01
```

The report gives exact-set agreement and per-tag precision/recall between the
automatic diagnostics and the author's judgments.

## 3. Prosody manipulation check

Open:

- `prosody/public/author_01_prosody_booklet.md`
- `prosody/public/author_01_prosody_responses.csv`

The packet contains 21 randomized high/low pairs (42 clips), one pair for every
gold-set scenario. Within a pair, the words and voice are identical. Listen in
a quiet setting with the same device and volume throughout. Do not inspect the
private key while rating.

Each row asks only which clip sounds stronger, the tone of clips A and B,
whether the speech is clear, and confidence from 1 to 5.

After all 21 rows are complete, score the packet with:

```powershell
python -m dual_audio.evaluation.gold_prosody_audit report `
  paper_results/v05/internal_audit author_01
```

The report gives relative-intensity accuracy, intended-tone accuracy, speech
clarity, and mean confidence.

## Private material

The nested `private/` directories contain scenario mappings, model and
condition identities, automatic failure tags, and intended prosody labels.
They are ignored by Git and must remain unopened until the corresponding audit
is complete. Only the `public/` materials should be shared with the auditor.

Report completed results as an **internal author audit** or **one-author
manipulation check**, not as independent human accuracy or inter-rater
validation.
