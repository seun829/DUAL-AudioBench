# R9. No-change effect with travel excluded

## The mechanism difference, confirmed from the scenario data

Gold post-gap action under `gap_no_state_change`, derived on the gold pre-gap path: **travel -> close_case**, all other 13 domains -> continue_monitoring. Travel is the only domain where suppressing the event produces a *resolved* world rather than an unfinished one, because its event (`departure_delay`) has no in-flight guard while every other domain's event is gated on the process variable already being mid-run.

## Paired no-change minus ordinary audio

| Model | Scope | Metric | paired n | clusters | Effect (pp) | 95% CI | p |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | all 14 domains | belief after gap | 168 | 14 | 21.4 | [4.8, 36.3] | 0.0297 |
| Gemini 2.5 | all 14 domains | final action | 168 | 14 | 3.6 | [-13.7, 20.2] | 0.7412 |
| Gemini 2.5 | all 14 domains | first action | 168 | 14 | -1.8 | [-13.7, 8.3] | 0.8555 |
| Gemini 2.5 | 13 domains, travel excluded | belief after gap | 156 | 13 | 23.7 | [7.1, 39.1] | 0.0239 |
| Gemini 2.5 | 13 domains, travel excluded | final action | 156 | 13 | 5.8 | [-12.8, 22.4] | 0.5886 |
| Gemini 2.5 | 13 domains, travel excluded | first action | 156 | 13 | -1.9 | [-14.7, 9.6] | 0.8555 |
| Gemini 2.5 | travel only | belief after gap | 12 | 1 | -8.3 | [-8.3, -8.3] | 1.0000 |
| Gemini 2.5 | travel only | final action | 12 | 1 | -25.0 | [-25.0, -25.0] | 1.0000 |
| Gemini 2.5 | travel only | first action | 12 | 1 | 0.0 | [0.0, 0.0] | 1.0000 |
| Gemini 3 | all 14 domains | belief after gap | 168 | 14 | 27.4 | [17.3, 37.5] | 0.0010 |
| Gemini 3 | all 14 domains | final action | 168 | 14 | 1.2 | [-7.1, 9.5] | 0.8892 |
| Gemini 3 | all 14 domains | first action | 168 | 14 | -5.4 | [-11.3, 0.0] | 0.1562 |
| Gemini 3 | 13 domains, travel excluded | belief after gap | 156 | 13 | 29.5 | [19.2, 39.7] | 0.0010 |
| Gemini 3 | 13 domains, travel excluded | final action | 156 | 13 | 2.6 | [-5.8, 10.9] | 0.6621 |
| Gemini 3 | 13 domains, travel excluded | first action | 156 | 13 | -5.1 | [-11.5, 0.6] | 0.2109 |
| Gemini 3 | travel only | belief after gap | 12 | 1 | 0.0 | [0.0, 0.0] | 1.0000 |
| Gemini 3 | travel only | final action | 12 | 1 | -16.7 | [-16.7, -16.7] | 1.0000 |
| Gemini 3 | travel only | first action | 12 | 1 | -8.3 | [-8.3, -8.3] | 1.0000 |
| GPT Audio Mini | all 14 domains | belief after gap | 168 | 14 | 32.1 | [19.0, 44.6] | 0.0011 |
| GPT Audio Mini | all 14 domains | final action | 168 | 14 | -0.6 | [-14.9, 13.1] | 1.0000 |
| GPT Audio Mini | all 14 domains | first action | 168 | 14 | -4.2 | [-9.5, 1.2] | 0.2412 |
| GPT Audio Mini | 13 domains, travel excluded | belief after gap | 156 | 13 | 33.3 | [19.9, 46.2] | 0.0017 |
| GPT Audio Mini | 13 domains, travel excluded | final action | 156 | 13 | 3.2 | [-10.3, 15.4] | 0.7129 |
| GPT Audio Mini | 13 domains, travel excluded | first action | 156 | 13 | -5.1 | [-10.3, 0.6] | 0.1582 |
| GPT Audio Mini | travel only | belief after gap | 12 | 1 | 16.7 | [16.7, 16.7] | 1.0000 |
| GPT Audio Mini | travel only | final action | 12 | 1 | -50.0 | [-50.0, -50.0] | 1.0000 |
| GPT Audio Mini | travel only | first action | 12 | 1 | 8.3 | [8.3, 8.3] | 1.0000 |

## Reading

**The effect holds on 13 domains. This closes the hole.** The belief effect is +21.4/+27.4/+32.1 across all 14 domains and +23.7/+29.5/+33.3 with travel excluded -- a shift of at most 2.3 points. The final-action effect moves from +3.6/+1.2/-0.6 to +5.8/+2.6/+3.2.

The paper's reported no-change belief effect of +21.4 / +27.4 / +32.1 is therefore not an artefact of the travel domain, and the 13-domain version does not need to become primary. A one-line sensitivity footnote is enough: *excluding the six travel scenarios, whose gap event is a notification rather than a processing window, the belief effect is +23.7/+29.5/+33.3.*

The travel-only rows are reported for completeness but are 6 scenarios in a single domain cluster, so their intervals are uninformative by construction -- `paired_cluster_effect` has one cluster to bootstrap from. They should not be quoted as an effect.

Separately from the statistics, the wording problem in R1's Q1 sense remains and is worth one sentence in the paper: the sentence at `main.tex:286` ("the no-change observation truthfully states that processing remains unresolved") is accurate for 78 of 84 scenarios and false for the 6 travel ones, where the utterance says the flight is still on time and the gold action is to close the case.
