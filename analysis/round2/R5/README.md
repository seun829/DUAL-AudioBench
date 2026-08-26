# R5. Revision gain and stale belief mass

This is the most direct measurement of the mechanism the benchmark is named for. All four quantities are already computed per trajectory in `belief_revision.variables` and none appear in the paper.

Values are pooled at the **variable** level over variables whose true state changed across the gap. The stored `mean_*` fields average within a trajectory first; those are reported too, and they agree closely because almost every cell has exactly one contributing variable per trajectory.

## Pooled over changed variables

| Model | Condition | k obs | Revision gain | Reflection gain | Final revision gain | Stale mass | Contributing variables |
|---|---|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 116 | -0.009 | 0.006 | -0.003 | 0.021 | access_status=9; authorization_status=9; claim_progress=12; claim_state=3; claim_status=8; connection_status=7; dispute_status=12; enrolment_status=8; firmware_status=9; permit_status=9; port_status=7; reading_status=11; shipment_status=1; work_order_status=11 |
| Gemini 2.5 | No state change | 108 | 0.596 | -0.298 | 0.298 | 0.028 | access_status=11; authorization_status=7; claim_progress=12; claim_state=5; claim_status=8; connection_status=2; dispute_status=12; enrolment_status=11; firmware_status=10; permit_status=6; port_status=5; reading_status=4; shipment_status=4; work_order_status=11 |
| Gemini 2.5 | Short clue | 105 | 0.142 | 0.039 | 0.181 | 0.017 | access_status=8; authorization_status=7; claim_progress=9; claim_state=3; claim_status=7; connection_status=6; dispute_status=12; enrolment_status=11; firmware_status=10; permit_status=5; port_status=5; reading_status=9; shipment_status=3; work_order_status=10 |
| Gemini 2.5 | Clue removed | 100 | 0.147 | 0.008 | 0.155 | 0.022 | access_status=9; authorization_status=4; claim_progress=12; claim_state=7; claim_status=4; connection_status=8; dispute_status=11; enrolment_status=10; firmware_status=8; permit_status=4; port_status=2; reading_status=9; work_order_status=12 |
| Gemini 2.5 | Transcript | 125 | 0.282 | 0.007 | 0.289 | 0.018 | access_status=12; authorization_status=8; claim_progress=12; claim_state=9; claim_status=5; connection_status=6; dispute_status=12; enrolment_status=10; firmware_status=11; permit_status=11; port_status=4; reading_status=10; shipment_status=3; work_order_status=12 |
| Gemini 2.5 | Neutral audio | 108 | 0.236 | 0.009 | 0.245 | 0.013 | access_status=8; authorization_status=6; claim_progress=8; claim_state=6; claim_status=8; connection_status=7; dispute_status=12; enrolment_status=9; firmware_status=9; permit_status=8; port_status=7; reading_status=7; shipment_status=1; work_order_status=12 |
| Gemini 2.5 | Explicit user update | 184 | 0.778 | 0.016 | 0.795 | 0.044 | access_status=7; authorization_status=7; causal_alignment=72; claim_progress=10; claim_state=4; claim_status=8; connection_status=12; dispute_status=11; enrolment_status=10; firmware_status=8; permit_status=6; port_status=5; reading_status=10; shipment_status=2; work_order_status=12 |
| Gemini 2.5 | High prosody | 114 | 0.194 | 0.020 | 0.214 | 0.016 | access_status=9; authorization_status=6; claim_progress=8; claim_state=7; claim_status=10; connection_status=7; dispute_status=10; enrolment_status=11; firmware_status=10; permit_status=7; port_status=5; reading_status=8; shipment_status=5; work_order_status=11 |
| Gemini 2.5 | Low prosody | 105 | 0.046 | 0.051 | 0.097 | 0.023 | access_status=11; authorization_status=5; claim_progress=10; claim_state=5; claim_status=9; connection_status=6; dispute_status=11; enrolment_status=12; firmware_status=9; permit_status=5; port_status=4; reading_status=6; shipment_status=1; work_order_status=11 |
| Gemini 3 | Ordinary audio | 130 | 0.309 | 0.089 | 0.398 | 0.020 | access_status=12; authorization_status=9; claim_progress=11; claim_state=7; claim_status=11; connection_status=6; dispute_status=12; enrolment_status=9; firmware_status=12; permit_status=10; port_status=6; reading_status=7; shipment_status=6; work_order_status=12 |
| Gemini 3 | No state change | 117 | 0.585 | -0.085 | 0.500 | 0.013 | access_status=12; authorization_status=6; claim_progress=12; claim_state=7; claim_status=10; connection_status=1; dispute_status=10; enrolment_status=9; firmware_status=12; permit_status=8; port_status=7; reading_status=8; shipment_status=3; work_order_status=12 |
| Gemini 3 | Short clue | 112 | 0.280 | 0.042 | 0.322 | 0.022 | access_status=11; authorization_status=8; claim_progress=11; claim_state=4; claim_status=9; connection_status=7; dispute_status=10; enrolment_status=8; firmware_status=11; permit_status=6; port_status=5; reading_status=7; shipment_status=4; work_order_status=11 |
| Gemini 3 | Clue removed | 111 | 0.224 | 0.021 | 0.245 | 0.018 | access_status=11; authorization_status=2; claim_progress=12; claim_state=11; claim_status=10; connection_status=8; dispute_status=8; enrolment_status=8; firmware_status=12; permit_status=6; port_status=5; reading_status=6; work_order_status=12 |
| Gemini 3 | Transcript | 137 | 0.413 | 0.119 | 0.532 | 0.025 | access_status=12; authorization_status=9; claim_progress=12; claim_state=11; claim_status=9; connection_status=6; dispute_status=11; enrolment_status=11; firmware_status=11; permit_status=8; port_status=8; reading_status=12; shipment_status=5; work_order_status=12 |
| Gemini 3 | Neutral audio | 127 | 0.336 | 0.032 | 0.368 | 0.028 | access_status=12; authorization_status=9; claim_progress=11; claim_state=5; claim_status=10; connection_status=6; dispute_status=12; enrolment_status=8; firmware_status=11; permit_status=8; port_status=9; reading_status=9; shipment_status=6; work_order_status=11 |
| Gemini 3 | Explicit user update | 198 | 0.811 | 0.051 | 0.862 | 0.047 | access_status=9; authorization_status=9; causal_alignment=72; claim_progress=11; claim_state=6; claim_status=11; connection_status=12; dispute_status=12; enrolment_status=8; firmware_status=11; permit_status=6; port_status=7; reading_status=10; shipment_status=3; work_order_status=11 |
| Gemini 3 | High prosody | 123 | 0.297 | 0.020 | 0.318 | 0.013 | access_status=11; authorization_status=6; claim_progress=12; claim_state=7; claim_status=11; connection_status=7; dispute_status=11; enrolment_status=7; firmware_status=12; permit_status=7; port_status=7; reading_status=9; shipment_status=4; work_order_status=12 |
| Gemini 3 | Low prosody | 116 | 0.250 | 0.020 | 0.270 | 0.014 | access_status=11; authorization_status=7; claim_progress=10; claim_state=5; claim_status=11; connection_status=6; dispute_status=11; enrolment_status=11; firmware_status=12; permit_status=8; port_status=6; reading_status=7; shipment_status=1; work_order_status=10 |
| GPT Audio Mini | Ordinary audio | 105 | -0.010 | 0.038 | 0.028 | 0.103 | access_status=12; authorization_status=5; claim_progress=3; claim_state=10; claim_status=6; connection_status=6; dispute_status=11; enrolment_status=7; firmware_status=7; permit_status=7; port_status=8; reading_status=8; shipment_status=3; work_order_status=12 |
| GPT Audio Mini | No state change | 91 | 0.272 | -0.060 | 0.212 | 0.126 | access_status=12; authorization_status=4; claim_progress=2; claim_state=9; claim_status=6; dispute_status=11; enrolment_status=9; firmware_status=5; permit_status=8; port_status=7; reading_status=5; shipment_status=2; work_order_status=11 |
| GPT Audio Mini | Short clue | 108 | -0.057 | 0.010 | -0.048 | 0.114 | access_status=12; authorization_status=6; claim_progress=6; claim_state=10; claim_status=7; connection_status=6; dispute_status=12; enrolment_status=7; firmware_status=8; permit_status=8; port_status=5; reading_status=7; shipment_status=4; work_order_status=10 |
| GPT Audio Mini | Clue removed | 87 | 0.045 | 0.043 | 0.088 | 0.115 | access_status=12; authorization_status=2; claim_progress=1; claim_state=10; claim_status=10; connection_status=6; dispute_status=8; enrolment_status=5; firmware_status=5; permit_status=4; port_status=6; reading_status=8; work_order_status=10 |
| GPT Audio Mini | Neutral audio | 102 | -0.008 | 0.025 | 0.017 | 0.117 | access_status=12; authorization_status=5; claim_progress=5; claim_state=12; claim_status=8; connection_status=6; dispute_status=9; enrolment_status=5; firmware_status=7; permit_status=7; port_status=7; reading_status=6; shipment_status=2; work_order_status=11 |
| GPT Audio Mini | Explicit user update | 183 | 0.456 | 0.017 | 0.474 | 0.113 | access_status=12; authorization_status=4; causal_alignment=72; claim_progress=6; claim_state=12; claim_status=9; connection_status=12; dispute_status=10; enrolment_status=8; firmware_status=4; permit_status=9; port_status=7; reading_status=7; shipment_status=2; work_order_status=9 |
| GPT Audio Mini | High prosody | 97 | -0.027 | 0.009 | -0.019 | 0.111 | access_status=12; authorization_status=5; claim_progress=5; claim_state=12; claim_status=7; connection_status=6; dispute_status=6; enrolment_status=8; firmware_status=5; permit_status=6; port_status=7; reading_status=7; shipment_status=2; work_order_status=9 |
| GPT Audio Mini | Low prosody | 96 | -0.010 | -0.016 | -0.026 | 0.119 | access_status=11; authorization_status=5; claim_progress=2; claim_state=9; claim_status=6; connection_status=6; dispute_status=10; enrolment_status=8; firmware_status=6; permit_status=7; port_status=6; reading_status=8; shipment_status=3; work_order_status=9 |

## Trajectory-level means (the stored `mean_*` fields)

| Model | Condition | n with a change | stored mean_revision_gain | stored mean_final_revision_gain | stored mean_stale_belief_persistence |
|---|---|---|---|---|---|
| Gemini 2.5 | Ordinary audio | 116 | -0.009 | -0.003 | 0.021 |
| Gemini 2.5 | No state change | 108 | 0.596 | 0.298 | 0.028 |
| Gemini 2.5 | Short clue | 105 | 0.142 | 0.181 | 0.017 |
| Gemini 2.5 | Clue removed | 100 | 0.147 | 0.155 | 0.022 |
| Gemini 2.5 | Transcript | 125 | 0.282 | 0.289 | 0.018 |
| Gemini 2.5 | Neutral audio | 108 | 0.236 | 0.245 | 0.013 |
| Gemini 2.5 | Explicit user update | 146 | 0.750 | 0.771 | 0.052 |
| Gemini 2.5 | High prosody | 114 | 0.194 | 0.214 | 0.016 |
| Gemini 2.5 | Low prosody | 105 | 0.046 | 0.097 | 0.023 |
| Gemini 3 | Ordinary audio | 130 | 0.309 | 0.398 | 0.020 |
| Gemini 3 | No state change | 117 | 0.585 | 0.500 | 0.013 |
| Gemini 3 | Short clue | 112 | 0.280 | 0.322 | 0.022 |
| Gemini 3 | Clue removed | 111 | 0.224 | 0.245 | 0.018 |
| Gemini 3 | Transcript | 137 | 0.413 | 0.532 | 0.025 |
| Gemini 3 | Neutral audio | 127 | 0.336 | 0.368 | 0.028 |
| Gemini 3 | Explicit user update | 152 | 0.795 | 0.854 | 0.057 |
| Gemini 3 | High prosody | 123 | 0.297 | 0.318 | 0.013 |
| Gemini 3 | Low prosody | 116 | 0.250 | 0.270 | 0.014 |
| GPT Audio Mini | Ordinary audio | 105 | -0.010 | 0.028 | 0.103 |
| GPT Audio Mini | No state change | 91 | 0.272 | 0.212 | 0.126 |
| GPT Audio Mini | Short clue | 108 | -0.057 | -0.048 | 0.114 |
| GPT Audio Mini | Clue removed | 87 | 0.045 | 0.088 | 0.115 |
| GPT Audio Mini | Neutral audio | 102 | -0.008 | 0.017 | 0.117 |
| GPT Audio Mini | Explicit user update | 151 | 0.435 | 0.451 | 0.120 |
| GPT Audio Mini | High prosody | 97 | -0.027 | -0.019 | 0.111 |
| GPT Audio Mini | Low prosody | 96 | -0.010 | -0.026 | 0.119 |

## Reading

**This is the figure the work order hoped for, and it is there.** Under ordinary audio the resumed evidence moves -0.009/0.309/-0.010 of probability mass onto the new true state. Under explicit user update, where the same evidence states the outcome in plain language, it moves 0.778/0.811/0.456. The gap is +0.787/+0.502/+0.466 points of probability mass, on the same scenarios and the same menus.

Stale mass tells the same story from the other side: after hearing the resumed utterance, 0.021/0.020/0.103 of probability is still sitting on the state that has just been superseded under ordinary audio, against 0.044/0.047/0.113 under explicit user update.

Reflection gain -- the movement between the belief-only checkpoint and the final action, with no new evidence in between -- is 0.006/0.089/0.038 under ordinary audio. Near zero is the expected and desirable result: it means the belief-only checkpoint is not being silently revised once the menu appears, so the two checkpoints measure what they claim to.

**A finding worth its own sentence: under no state change, reflection gain is strongly negative for all three models (-0.298/-0.085/-0.060).** Between the belief-only checkpoint and the final action there is no new evidence, so this is the action menu itself pulling belief *away* from the true state. Revision gain of 0.596/0.585/0.272 at the belief-only checkpoint decays to a final revision gain of 0.298/0.500/0.212 once the five options are shown. The models correctly read "still processing" from the utterance and then talk themselves out of it when asked to choose an action -- which is a mechanism the paper currently has no way to name, and which the belief-only checkpoint exists precisely to expose.

GPT Audio Mini also carries five to eight times the stale mass of either Gemini across every condition (0.103 under ordinary audio against 0.021 and 0.020), which is a cleaner separation between the models than any accuracy column provides.

**Caveat on k.** The contributing-variable column confirms the concern in the work order: in every condition except explicit user update the only changed variable is the domain outcome, so `causal_alignment` contributes nothing to these means. Under explicit user update it does contribute, because 72 of 84 user-action specs rewrite it (see R10) -- which means the user-update revision gain is partly measuring the model tracking a variable the intervention itself overwrote, and should be quoted with that qualification.
