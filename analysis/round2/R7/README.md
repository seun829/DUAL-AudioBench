# R7. Is the first action inflated too?

## Gold `pre_gap.correct_action` distribution over the 84 scenarios

| Gold first action | n | share |
|---|---|---|
| file_dispute | 6 | 7.1% |
| request_authorization | 6 | 7.1% |
| submit_enrolment | 6 | 7.1% |
| schedule_redelivery | 6 | 7.1% |
| enable_itinerary_monitoring | 6 | 7.1% |
| lodge_claim | 6 | 7.1% |
| submit_permit_application | 6 | 7.1% |
| submit_claim | 6 | 7.1% |
| run_maintenance | 6 | 7.1% |
| initiate_credential_reset | 6 | 7.1% |
| submit_port_request | 6 | 7.1% |
| dispatch_maintenance_visit | 6 | 7.1% |
| submit_reading | 6 | 7.1% |
| open_cover_claim | 6 | 7.1% |

Global majority class: **7.1%** (`file_dispute`). Domain-conditional majority class: **100.0%**. Uniform chance: 20.0%.

## Reported first-action accuracy against those baselines

| Model | Condition | First action | 95% CI | Uniform | Global majority | Domain majority | Best fixed position | Clears domain majority? |
|---|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 69.6 | [56.0, 81.5] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | No state change | 67.9 | [55.4, 80.4] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | Short clue | 63.7 | [51.8, 75.0] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | Clue removed | 59.5 | [43.5, 75.0] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | Transcript | 77.4 | [63.1, 89.3] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | Neutral audio | 64.9 | [53.0, 75.6] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | Explicit user update | 63.7 | [51.8, 75.0] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | High prosody | 68.5 | [60.1, 77.4] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 2.5 | Low prosody | 63.7 | [49.4, 77.4] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | Ordinary audio | 80.4 | [70.2, 89.9] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | No state change | 75.0 | [63.1, 85.7] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | Short clue | 66.1 | [54.8, 77.4] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | Clue removed | 66.7 | [50.0, 82.1] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | Transcript | 84.5 | [75.0, 92.3] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | Neutral audio | 78.0 | [69.0, 86.3] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | Explicit user update | 75.0 | [63.1, 85.7] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | High prosody | 74.4 | [63.1, 85.1] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| Gemini 3 | Low prosody | 72.0 | [58.3, 83.9] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | Ordinary audio | 65.5 | [52.4, 78.0] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | No state change | 61.3 | [46.4, 75.6] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | Short clue | 66.7 | [56.5, 77.4] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | Clue removed | 55.4 | [38.7, 71.4] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | Neutral audio | 63.1 | [50.6, 75.6] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | Explicit user update | 65.5 | [52.4, 78.0] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | High prosody | 60.7 | [48.8, 73.2] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |
| GPT Audio Mini | Low prosody | 60.7 | [48.8, 72.6] | 20.0 | 7.1 | 100.0 | 26.2 (B) | YES |

## Reading

**The first action is not inflated the way the final action is, but it is not a state-tracking measurement either.** Two facts, pulling in opposite directions:

1. The gold pre-gap action is maximally spread across the benchmark: 14 distinct actions over 84 scenarios, 6 each, so the **global** majority class is only 7.1%. Best fixed-position is 26.2%, close to the 20% uniform rate, confirming the pre-gap shuffle works. Against either of those baselines the reported 55.4-84.5% is a real result.

2. The **domain-conditional** majority class is **100.0%**, and that is not a rounding artefact: within each of the 14 domains, all 6 scenarios share the same gold opening move. A policy that recognises the domain and recalls one action per domain scores a perfect 100 without listening to the conversation at all. So the domain-conditional column is degenerate here and no model can "clear" it -- the useful reading is the reverse: models score 55-85% on a task that is answerable from the domain name alone.

**What this means for the paper.** The sentence that first-action accuracy shows the benchmark is not uniformly hard **survives**, and needs the global-majority footnote (7.1%, not 20%). But any sentence implying the first action demonstrates competence at *state tracking* should be cut: the pre-gap checkpoint precedes the gap, has a single correct answer per domain, and is best described as a domain-appropriate-action check that establishes the models can operate the menu at all. That is exactly the role the paper's own "act correctly before the gap and fail afterward" framing needs it to play, so this is a clarification rather than a correction.

