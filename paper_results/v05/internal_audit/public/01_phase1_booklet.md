# DUAL-AudioBench v0.5 independent audit — phase 1 (annotator 1)

Scenario freeze: `e16319a791ab4600f88a33f7957e66eec18be262649caac03845c161119044b9`

Complete the phase-1 CSV before opening phase 2. Do not inspect task
JSON, code, private keys, or another auditor's responses. Select the
best next action using only the public dialogue. `Answerable` asks
whether exactly one option follows without outside domain knowledge.
The rule-match question is simple: choose `aligned` when the user's
clue satisfies the stated success rule, or `misaligned` when it
violates that rule. It does not ask whether you agree with the gold.
Ambiguity is 1 (unambiguous) through 5 (not answerable).

## Item ANNOTATOR_01-01

### Public dialogue

1. **User:** Hi, my washing machine has stopped draining properly.
2. **Agent:** I can look at that. Do you have the model number?
3. **User:** Yes, it starts with W-D-nine.
4. **Agent:** The standard cover route authorises purchases from the covered retail channel; another purchase channel falls outside its terms.
5. **User:** Understood; I checked how the item was purchased.
6. **Agent:** Have you cleaned the filter recently?
7. **User:** Yes, I cleared it yesterday.
8. **Agent:** Is there parking near the property?
9. **User:** Yes, right outside.
10. **Agent:** Is the number ending in one-seven-four still yours?
11. **User:** Yes, that is mine.
12. **Agent:** Would you like the outcome confirmed in writing?
13. **User:** Yes, in writing please.
14. **Agent:** Is the machine level on the floor?
15. **User:** Yes, it sits flat.
16. **Agent:** How long has it been doing this?
17. **User:** About four days now.
18. **Agent:** Is it plumbed into a standard waste pipe?
19. **User:** Yes, the usual arrangement.
20. **Agent:** Was the purchase made through the channel covered by this claim route?
21. **User:** We bought it as a standard retail item, which is the purchase channel covered by this route.
22. **Agent:** Would weekday or weekend suit for a visit?
23. **User:** Weekdays are easier.
24. **Agent:** Does it make any unusual noise?
25. **User:** There is a low humming sound.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the purchase channel falls outside the submitted cover route
- `aligned` — the purchase channel is covered by the submitted route

### Candidate next actions

- **A.** Talk the user through fixing it themselves first.
- **B.** Send an engineer before any assessment happens.
- **C.** Close the request and ask the user to call back.
- **D.** Open the cover claim and send it for assessment.
- **E.** Approve a whole replacement machine straight away.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-02

### Public dialogue

1. **User:** Hi, I am applying for a resident parking permit.
2. **Agent:** I can take you through that. Do you have the property reference?
3. **User:** Yes, it ends in three-one-seven.
4. **Agent:** The eligibility check issues the permit only when the proof names the applicant; proof naming another occupant is refused.
5. **User:** Understood; I compared the names on the documents.
6. **Agent:** Is the vehicle kept at the property overnight?
7. **User:** Yes, every night.
8. **Agent:** Do you need a visitor allowance as well?
9. **User:** No, just the one permit.
10. **Agent:** Is the number ending in two-four-eight still current?
11. **User:** Yes, that is current.
12. **Agent:** Would you like the permit posted or collected?
13. **User:** Posted is easier for me.
14. **Agent:** Have you held a permit in this zone before?
15. **User:** No, this is my first one.
16. **Agent:** Would you like a receipt by email?
17. **User:** Yes, email please.
18. **Agent:** Would you like an annual or monthly permit?
19. **User:** Annual would be better.
20. **Agent:** Does the supporting proof name the same person who is applying for the permit?
21. **User:** The tenancy proof is in my flatmate's name, while I am the person filing for the permit.
22. **Agent:** Do you know the registration plate?
23. **User:** Yes, I have it written down here.
24. **Agent:** How many vehicles need covering?
25. **User:** Just the one.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the supporting proof names someone other than the applicant
- `aligned` — the supporting proof names the permit applicant

### Candidate next actions

- **A.** Send the whole thing straight to the appeals team.
- **B.** Hand out a temporary permit before any check is run.
- **C.** Close the request and ask the caller to apply again later.
- **D.** Send the application into the automated eligibility check.
- **E.** Read the plate back once more before applying.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-03

### Public dialogue

1. **User:** Hi, I am trying to finish enrolling for the coming term.
2. **Agent:** I can help with that. Do you have your student reference?
3. **User:** Yes, it ends in six-two-two.
4. **Agent:** Enrolment is confirmed only when transferred study has the required assessment; unassessed study is held for review.
5. **User:** Understood; I checked the assessment status.
6. **Agent:** Have you arranged your tuition payment method?
7. **User:** Yes, that is all set up.
8. **Agent:** Is your term address the same as last year?
9. **User:** Yes, the same place.
10. **Agent:** Is the contact number ending in eight-one-nine right?
11. **User:** Yes, that is correct.
12. **Agent:** Have you chosen all of your modules yet?
13. **User:** Yes, I picked them last week.
14. **Agent:** Have the transferred credits already received the prior-study assessment required for enrolment?
15. **User:** My overseas transfer credits have already received the required assessment.
16. **Agent:** Are you studying full time or part time?
17. **User:** Full time this year.
18. **Agent:** Do you require any study support arrangements?
19. **User:** No, nothing like that.
20. **Agent:** Do you need a timetable sent to you?
21. **User:** Yes, that would be handy.
22. **Agent:** Would you like a locker on campus?
23. **User:** No, I do not need one.
24. **Agent:** Would you like reminders before the deadline?
25. **User:** Yes, reminders would help.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transferred study has not received its required assessment
- `aligned` — the transferred study has already received the required assessment

### Candidate next actions

- **A.** Set aside the entry requirements entirely for this student.
- **B.** Go back over the chosen modules before submitting.
- **C.** Put the enrolment through the automated registration run.
- **D.** Close the request and ask the student to try again.
- **E.** Push the whole thing back to a later term instead.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-04

### Public dialogue

1. **User:** Hi, I need to report some damage to my car from this morning.
2. **Agent:** I am sorry to hear that. Was anybody injured?
3. **User:** No, thankfully everyone is fine.
4. **Agent:** The assessment settles only when the registered keeper matches the policy name; a mismatch is held for proof.
5. **User:** Understood; I compared the keeper and policy names.
6. **Agent:** Where did the incident take place?
7. **User:** In a supermarket car park.
8. **Agent:** Was another driver involved?
9. **User:** Yes, but they left before I could speak to them.
10. **Agent:** Would you need a courtesy car meanwhile?
11. **User:** Yes, that would help a lot.
12. **Agent:** Would you like updates by message?
13. **User:** Yes, messages are fine.
14. **Agent:** Is the car still driveable?
15. **User:** Yes, it drives, but the wing is dented.
16. **Agent:** Have you reported it to the authorities?
17. **User:** Yes, I did that this morning.
18. **Agent:** Do you have a preferred repair garage?
19. **User:** No, whichever one you recommend.
20. **Agent:** Did anybody witness what happened?
21. **User:** One person nearby saw it.
22. **Agent:** Is the number ending in seven-six-five still yours?
23. **User:** Yes, that is right.
24. **Agent:** Does the registered keeper match the person named on the policy?
25. **User:** The vehicle registration and the insurance cover are both in my name.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the registered keeper and policyholder names differ
- `aligned` — the registered keeper matches the policyholder name

### Candidate next actions

- **A.** Chase the bystander for a statement before lodging anything.
- **B.** Write the car off before anything has been assessed.
- **C.** Approve the garage work before the report is lodged.
- **D.** Close the report and ask the caller to get in touch later.
- **E.** Lodge the report into the automated assessment run.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-05

### Public dialogue

1. **User:** Hi, there is a charge on my account that I did not make.
2. **Agent:** I can help with that. Do you see the amount and date?
3. **User:** Yes, it is forty-two dollars from last Tuesday.
4. **Agent:** The automated review accepts a dispute only when the charge's card identifier matches the current card record; otherwise it returns unmatched.
5. **User:** Understood; I checked which card identifier the charge used.
6. **Agent:** Was the disputed charge tied to the same card identifier that is currently on file?
7. **User:** My current card was reissued, and the disputed transaction carried that same reissued-card reference.
8. **Agent:** Is the mailing address on the profile still correct?
9. **User:** Yes, that address is right.
10. **Agent:** Would a paper copy of the outcome be helpful?
11. **User:** No, electronic is fine.
12. **Agent:** Do you use the mobile application to check balances?
13. **User:** Yes, almost every day.
14. **Agent:** Was the physical card in your possession that day?
15. **User:** Yes, it was in my wallet the whole time.
16. **Agent:** Have you shared the number with any recurring service?
17. **User:** Only my usual streaming subscription.
18. **Agent:** Is the contact number ending in six-one-eight still yours?
19. **User:** Yes, that number is current.
20. **Agent:** Were there other unfamiliar amounts on the same statement?
21. **User:** No, just that single one.
22. **Agent:** Did you travel outside your normal area recently?
23. **User:** No, I have been home all month.
24. **Agent:** Would you like alerts for every future transaction?
25. **User:** Yes, please turn those on.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the charge identifier differs from the current card record
- `aligned` — the charge identifier matches the current card record

### Candidate next actions

- **A.** Ask the merchant for paperwork before opening anything.
- **B.** Send out another physical card before reviewing the charge.
- **C.** Close the request and tell the user to watch the balance.
- **D.** File the disputed amount into the automated review queue.
- **E.** Freeze the whole account before the charge is examined.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-06

### Public dialogue

1. **User:** Hi, I am calling to refill my blood pressure prescription.
2. **Agent:** Can I get your date of birth to open the profile?
3. **User:** It is March twelfth, nineteen seventy-one.
4. **Agent:** The claim is approved only when the pharmacy billing profile matches the currently active plan; otherwise it is rejected.
5. **User:** Understood; I checked which plan the profile uses.
6. **Agent:** Would you like a text when the order is ready?
7. **User:** Yes, a text is fine.
8. **Agent:** Is Doctor Patel still the prescriber?
9. **User:** Yes, Doctor Patel is still my doctor.
10. **Agent:** Do you need any other prescriptions refilled?
11. **User:** No, just this one.
12. **Agent:** Is the phone number ending in four-two-two-one current?
13. **User:** Yes, that is still my number.
14. **Agent:** Are there any new allergies to record?
15. **User:** No new allergies.
16. **Agent:** Is the generic version acceptable?
17. **User:** Yes, generic is fine.
18. **Agent:** Is the pickup location on Main Street still convenient?
19. **User:** Yes, I am nearby.
20. **Agent:** Does the pharmacy billing profile match the plan that is active now?
21. **User:** The replacement plan is active, but the pharmacy profile still shows my previous plan.
22. **Agent:** Would you like pickup or delivery?
23. **User:** Pickup is fine.
24. **Agent:** Has the dosage changed recently?
25. **User:** No, it is the same ten milligram dose.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the pharmacy bills an outdated plan rather than the active plan
- `aligned` — the pharmacy billing profile matches the active plan

### Candidate next actions

- **A.** Wait without submitting anything yet.
- **B.** Close the request without sending the order.
- **C.** Bypass the normal transaction and offer another payment route.
- **D.** Pause and contact the prescriber for a new order.
- **E.** Submit the order to the automated claim process.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-07

### Public dialogue

1. **User:** Hi, there is a charge on my account that I did not make.
2. **Agent:** I can help with that. Do you see the amount and date?
3. **User:** Yes, it is forty-two dollars from last Tuesday.
4. **Agent:** The automated review accepts a dispute only when the charge's card identifier matches the current card record; otherwise it returns unmatched.
5. **User:** Understood; I checked which card identifier the charge used.
6. **Agent:** Is the mailing address on the profile still correct?
7. **User:** Yes, that address is right.
8. **Agent:** Did you travel outside your normal area recently?
9. **User:** No, I have been home all month.
10. **Agent:** Would a paper copy of the outcome be helpful?
11. **User:** No, electronic is fine.
12. **Agent:** Would you like alerts for every future transaction?
13. **User:** Yes, please turn those on.
14. **Agent:** Do you use the mobile application to check balances?
15. **User:** Yes, almost every day.
16. **Agent:** Were there other unfamiliar amounts on the same statement?
17. **User:** No, just that single one.
18. **Agent:** Was the disputed charge tied to the same card identifier that is currently on file?
19. **User:** My current card was reissued, and the disputed transaction carried that same reissued-card reference.
20. **Agent:** Have you shared the number with any recurring service?
21. **User:** Only my usual streaming subscription.
22. **Agent:** Was the physical card in your possession that day?
23. **User:** Yes, it was in my wallet the whole time.
24. **Agent:** Is the contact number ending in six-one-eight still yours?
25. **User:** Yes, that number is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the charge identifier differs from the current card record
- `aligned` — the charge identifier matches the current card record

### Candidate next actions

- **A.** File the disputed amount into the automated review queue.
- **B.** Ask the merchant for paperwork before opening anything.
- **C.** Freeze the whole account before the charge is examined.
- **D.** Close the request and tell the user to watch the balance.
- **E.** Send out another physical card before reviewing the charge.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-08

### Public dialogue

1. **User:** Hi, I am trying to move my number across to your network.
2. **Agent:** I can start that. Do you have the transfer code ready?
3. **User:** Yes, I received it by text yesterday.
4. **Agent:** The number transfer completes only when its ownership record matches the required direct account holder; an intermediary record is rejected.
5. **User:** Understood; I checked the ownership record.
6. **Agent:** Is the billing address on file still correct?
7. **User:** Yes, that has not changed.
8. **Agent:** Would you like data roaming switched on?
9. **User:** Yes, that would be useful.
10. **Agent:** Is the number currently active and in use?
11. **User:** Yes, I am using it right now.
12. **Agent:** Would you like a confirmation message when it completes?
13. **User:** Yes, please send one.
14. **Agent:** Would you like a paper bill as well?
15. **User:** No, online only is fine.
16. **Agent:** Do you need international calling enabled?
17. **User:** No, I do not need that.
18. **Agent:** Does the ownership record on the transfer match the required account holder?
19. **User:** The handset came through a reseller, and the transfer still carries the reseller's intermediary subscriber record.
20. **Agent:** Have you settled the balance with the old network?
21. **User:** Yes, that was cleared last week.
22. **Agent:** Is the alternative contact ending in four-zero-three current?
23. **User:** Yes, that one still works.
24. **Agent:** Do you want to keep the same monthly bundle?
25. **User:** Yes, the same one is fine.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transfer carries an intermediary ownership record instead of the required direct record
- `aligned` — the ownership record matches the required direct account holder

### Candidate next actions

- **A.** Close the request and ask the user to start again later.
- **B.** Read the transfer code back once more before sending anything.
- **C.** Give the user a brand new number instead of moving the old one.
- **D.** Send the transfer into the automated porting queue.
- **E.** Post out another SIM before the transfer is attempted.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-09

### Public dialogue

1. **User:** Hi, I cannot get into my work account this morning.
2. **Agent:** I can help. Does it reject you at the first screen?
3. **User:** Yes, it will not take me past that point.
4. **Agent:** Access is restored only when the reset targets the active authentication system; resetting an unused credential store leaves the account locked.
5. **User:** Understood; I checked which credential system was targeted.
6. **Agent:** Have you tried a different browser?
7. **User:** Yes, I tried two of them.
8. **Agent:** Would a written summary afterwards be useful?
9. **User:** Yes, please send one.
10. **Agent:** Are colleagues able to get in normally?
11. **User:** As far as I know, yes.
12. **Agent:** Do you have the authenticator application installed?
13. **User:** Yes, it is on my phone.
14. **Agent:** Are you connected through the office network?
15. **User:** No, I am at home today.
16. **Agent:** Does the same thing happen on your phone?
17. **User:** Yes, exactly the same.
18. **Agent:** Was the reset aimed at the credential system the company currently uses?
19. **User:** The company uses federated single sign-on, and the reset was aimed at that federated identity system.
20. **Agent:** Is the recovery contact ending in eight-three-seven current?
21. **User:** Yes, that is still current.
22. **Agent:** Did you change anything on your machine recently?
23. **User:** No, nothing that I noticed.
24. **Agent:** Is the address you enter the work one?
25. **User:** Yes, my work address.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the reset targets a credential store the company no longer uses
- `aligned` — the reset targets the company's active authentication system

### Candidate next actions

- **A.** Create an entirely new account for the user instead.
- **B.** Close the request and ask the user to retry tomorrow.
- **C.** Have the user wipe stored browser data before anything else.
- **D.** Hand out a temporary way around the login screen.
- **E.** Start the standard credential reset for the account.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-10

### Public dialogue

1. **User:** Hi, the heating in my flat has not worked for three days.
2. **Agent:** I am sorry about that. Can you confirm the flat number?
3. **User:** Yes, it is flat twelve on the third floor.
4. **Agent:** The visit can be completed only when the contractor's authority matches the current managing agent's requirements; expired authority blocks access.
5. **User:** Understood; I checked the contractor's access authority.
6. **Agent:** Is there a boiler cupboard inside the flat?
7. **User:** Yes, in the hallway.
8. **Agent:** Have you checked the thermostat setting?
9. **User:** Yes, it is turned right up.
10. **Agent:** Are neighbours reporting the same problem?
11. **User:** One of them mentioned it too.
12. **Agent:** Is it the whole flat or one room?
13. **User:** The whole flat is cold.
14. **Agent:** Is there a buzzer at the main entrance?
15. **User:** Yes, there is one.
16. **Agent:** Does the hot water still run?
17. **User:** Yes, the water is fine.
18. **Agent:** Is the number ending in nine-zero-six still right?
19. **User:** Yes, that is my number.
20. **Agent:** Would daytime access be possible?
21. **User:** Yes, I work from home.
22. **Agent:** Would you like a text before anyone arrives?
23. **User:** Yes, a text would help.
24. **Agent:** Does the contractor hold the access authority required by the current managing agent?
25. **User:** The contractor still has expired authority from the former managing agent, not the current credentials.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the contractor holds expired authority from the former agent
- `aligned` — the contractor holds current authority accepted by the managing agent

### Candidate next actions

- **A.** Close the request and ask the tenant to report it again.
- **B.** Move the tenant elsewhere before any visit is attempted.
- **C.** Raise the job and send it to the contractor rota.
- **D.** Approve a complete new heating system immediately.
- **E.** Post out portable heaters and leave it there.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-11

### Public dialogue

1. **User:** Hi, I am checking on my flight to Denver this afternoon.
2. **Agent:** I see the two-fifteen departure. Is that the flight you mean?
3. **User:** Yes. I want to make sure everything is on track.
4. **Agent:** A departure delay that is at least as long as the Denver connection window makes the onward flight impossible unless it is protected.
5. **User:** Understood; I have the connection time in front of me.
6. **Agent:** Do you have dietary or accessibility needs?
7. **User:** No, nothing like that.
8. **Agent:** Is the rewards number ending in nine-nine-three yours?
9. **User:** Yes, that is mine.
10. **Agent:** Do you need directions to the departure terminal?
11. **User:** No, I know where to go.
12. **Agent:** Are you checking any bags?
13. **User:** Just one checked bag.
14. **Agent:** Would you like gate-change notifications by text?
15. **User:** Yes, that would help.
16. **Agent:** Does anything else on the reservation look wrong?
17. **User:** No, everything else looks right.
18. **Agent:** How much connection time is scheduled in Denver?
19. **User:** There are only ninety minutes between the flights in Denver.
20. **Agent:** Do you already have a seat assignment?
21. **User:** Yes, fourteen C, an aisle.
22. **Agent:** The security wait is about twenty minutes. Are you leaving soon?
23. **User:** Yes, I am heading to the airport shortly.
24. **Agent:** Is the contact phone number on the booking current?
25. **User:** Yes, it is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the scheduled connection window is the short ninety-minute option
- `aligned` — the scheduled connection window is the long four-hour option

### Candidate next actions

- **A.** Replace the current departure even though it is still on time.
- **B.** Change the later segment immediately despite the current on-time status.
- **C.** Offer disruption compensation before a disruption occurs.
- **D.** Enable active monitoring for changes to the itinerary.
- **E.** Close the request without monitoring for changes.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-12

### Public dialogue

1. **User:** Hi, I am calling to refill my blood pressure prescription.
2. **Agent:** Can I get your date of birth to open the profile?
3. **User:** It is March twelfth, nineteen seventy-one.
4. **Agent:** The claim is approved only when the pharmacy billing profile matches the currently active plan; otherwise it is rejected.
5. **User:** Understood; I checked which plan the profile uses.
6. **Agent:** Is the generic version acceptable?
7. **User:** Yes, generic is fine.
8. **Agent:** Does the pharmacy billing profile match the plan that is active now?
9. **User:** The replacement plan is active, and the pharmacy profile already shows that same plan.
10. **Agent:** Do you need any other prescriptions refilled?
11. **User:** No, just this one.
12. **Agent:** Would you like a text when the order is ready?
13. **User:** Yes, a text is fine.
14. **Agent:** Has the dosage changed recently?
15. **User:** No, it is the same ten milligram dose.
16. **Agent:** Is Doctor Patel still the prescriber?
17. **User:** Yes, Doctor Patel is still my doctor.
18. **Agent:** Would you like pickup or delivery?
19. **User:** Pickup is fine.
20. **Agent:** Is the pickup location on Main Street still convenient?
21. **User:** Yes, I am nearby.
22. **Agent:** Is the phone number ending in four-two-two-one current?
23. **User:** Yes, that is still my number.
24. **Agent:** Are there any new allergies to record?
25. **User:** No new allergies.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the pharmacy bills an outdated plan rather than the active plan
- `aligned` — the pharmacy billing profile matches the active plan

### Candidate next actions

- **A.** Bypass the normal transaction and offer another payment route.
- **B.** Close the request without sending the order.
- **C.** Submit the order to the automated claim process.
- **D.** Pause and contact the prescriber for a new order.
- **E.** Wait without submitting anything yet.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-13

### Public dialogue

1. **User:** Hi, the heating in my flat has not worked for three days.
2. **Agent:** I am sorry about that. Can you confirm the flat number?
3. **User:** Yes, it is flat twelve on the third floor.
4. **Agent:** The visit can be completed only when the contractor's authority matches the current managing agent's requirements; expired authority blocks access.
5. **User:** Understood; I checked the contractor's access authority.
6. **Agent:** Does the contractor hold the access authority required by the current managing agent?
7. **User:** The contractor still has expired authority from the former managing agent, not the current credentials.
8. **Agent:** Is there a buzzer at the main entrance?
9. **User:** Yes, there is one.
10. **Agent:** Have you checked the thermostat setting?
11. **User:** Yes, it is turned right up.
12. **Agent:** Is there a boiler cupboard inside the flat?
13. **User:** Yes, in the hallway.
14. **Agent:** Would you like a text before anyone arrives?
15. **User:** Yes, a text would help.
16. **Agent:** Would daytime access be possible?
17. **User:** Yes, I work from home.
18. **Agent:** Is the number ending in nine-zero-six still right?
19. **User:** Yes, that is my number.
20. **Agent:** Is it the whole flat or one room?
21. **User:** The whole flat is cold.
22. **Agent:** Does the hot water still run?
23. **User:** Yes, the water is fine.
24. **Agent:** Are neighbours reporting the same problem?
25. **User:** One of them mentioned it too.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the contractor holds expired authority from the former agent
- `aligned` — the contractor holds current authority accepted by the managing agent

### Candidate next actions

- **A.** Approve a complete new heating system immediately.
- **B.** Raise the job and send it to the contractor rota.
- **C.** Move the tenant elsewhere before any visit is attempted.
- **D.** Post out portable heaters and leave it there.
- **E.** Close the request and ask the tenant to report it again.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-14

### Public dialogue

1. **User:** Hi, I am trying to move my number across to your network.
2. **Agent:** I can start that. Do you have the transfer code ready?
3. **User:** Yes, I received it by text yesterday.
4. **Agent:** The number transfer completes only when its ownership record matches the required direct account holder; an intermediary record is rejected.
5. **User:** Understood; I checked the ownership record.
6. **Agent:** Would you like a paper bill as well?
7. **User:** No, online only is fine.
8. **Agent:** Does the ownership record on the transfer match the required account holder?
9. **User:** The handset came through a reseller, and the transfer still carries the reseller's intermediary subscriber record.
10. **Agent:** Is the number currently active and in use?
11. **User:** Yes, I am using it right now.
12. **Agent:** Is the billing address on file still correct?
13. **User:** Yes, that has not changed.
14. **Agent:** Would you like data roaming switched on?
15. **User:** Yes, that would be useful.
16. **Agent:** Would you like a confirmation message when it completes?
17. **User:** Yes, please send one.
18. **Agent:** Do you need international calling enabled?
19. **User:** No, I do not need that.
20. **Agent:** Do you want to keep the same monthly bundle?
21. **User:** Yes, the same one is fine.
22. **Agent:** Have you settled the balance with the old network?
23. **User:** Yes, that was cleared last week.
24. **Agent:** Is the alternative contact ending in four-zero-three current?
25. **User:** Yes, that one still works.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transfer carries an intermediary ownership record instead of the required direct record
- `aligned` — the ownership record matches the required direct account holder

### Candidate next actions

- **A.** Close the request and ask the user to start again later.
- **B.** Post out another SIM before the transfer is attempted.
- **C.** Give the user a brand new number instead of moving the old one.
- **D.** Send the transfer into the automated porting queue.
- **E.** Read the transfer code back once more before sending anything.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-15

### Public dialogue

1. **User:** Hi, I am applying for a resident parking permit.
2. **Agent:** I can take you through that. Do you have the property reference?
3. **User:** Yes, it ends in three-one-seven.
4. **Agent:** The eligibility check issues the permit only when the proof names the applicant; proof naming another occupant is refused.
5. **User:** Understood; I compared the names on the documents.
6. **Agent:** How many vehicles need covering?
7. **User:** Just the one.
8. **Agent:** Do you know the registration plate?
9. **User:** Yes, I have it written down here.
10. **Agent:** Have you held a permit in this zone before?
11. **User:** No, this is my first one.
12. **Agent:** Is the vehicle kept at the property overnight?
13. **User:** Yes, every night.
14. **Agent:** Do you need a visitor allowance as well?
15. **User:** No, just the one permit.
16. **Agent:** Would you like a receipt by email?
17. **User:** Yes, email please.
18. **Agent:** Would you like an annual or monthly permit?
19. **User:** Annual would be better.
20. **Agent:** Is the number ending in two-four-eight still current?
21. **User:** Yes, that is current.
22. **Agent:** Would you like the permit posted or collected?
23. **User:** Posted is easier for me.
24. **Agent:** Does the supporting proof name the same person who is applying for the permit?
25. **User:** The tenancy proof is in my flatmate's name, while I am the person filing for the permit.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the supporting proof names someone other than the applicant
- `aligned` — the supporting proof names the permit applicant

### Candidate next actions

- **A.** Send the whole thing straight to the appeals team.
- **B.** Read the plate back once more before applying.
- **C.** Send the application into the automated eligibility check.
- **D.** Close the request and ask the caller to apply again later.
- **E.** Hand out a temporary permit before any check is run.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-16

### Public dialogue

1. **User:** Hi, my latest energy statement looks far too high.
2. **Agent:** I can look into that. Do you have the account reference?
3. **User:** Yes, it ends in four-eight-one.
4. **Agent:** Reading validation succeeds only when every meter at the property is registered on the account; an omitted meter is flagged.
5. **User:** Understood; I compared the meters with the account.
6. **Agent:** Would you like a breakdown by period?
7. **User:** Yes, that would be helpful.
8. **Agent:** Is the contact number ending in five-five-two right?
9. **User:** Yes, that is correct.
10. **Agent:** Have you added any large appliance lately?
11. **User:** No, nothing new like that.
12. **Agent:** Has your household size changed this quarter?
13. **User:** No, still the same two of us.
14. **Agent:** Has anyone been out to the property recently?
15. **User:** No, nobody has visited.
16. **Agent:** Is the heating electric or gas?
17. **User:** It is all electric here.
18. **Agent:** Is the statement paper or electronic?
19. **User:** Electronic, it arrives by email.
20. **Agent:** Does the account include every meter currently at the property?
21. **User:** The property has two meters, but the supplier profile lists only one of them.
22. **Agent:** Do you pay by fixed monthly amount?
23. **User:** Yes, a fixed amount each month.
24. **Agent:** Would you like the outcome by email as well?
25. **User:** Yes, email is fine.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — at least one property meter is missing from the account
- `aligned` — every property meter is registered on the account

### Candidate next actions

- **A.** Send the figure you gave me for automated validation.
- **B.** Close the request and ask the user to watch the next statement.
- **C.** Refund the difference before anything is validated.
- **D.** Send an engineer out before checking the figure.
- **E.** Read back through old tariff rates before submitting.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-17

### Public dialogue

1. **User:** Hi, I cannot get into my work account this morning.
2. **Agent:** I can help. Does it reject you at the first screen?
3. **User:** Yes, it will not take me past that point.
4. **Agent:** Access is restored only when the reset targets the active authentication system; resetting an unused credential store leaves the account locked.
5. **User:** Understood; I checked which credential system was targeted.
6. **Agent:** Have you tried a different browser?
7. **User:** Yes, I tried two of them.
8. **Agent:** Is the address you enter the work one?
9. **User:** Yes, my work address.
10. **Agent:** Is the recovery contact ending in eight-three-seven current?
11. **User:** Yes, that is still current.
12. **Agent:** Would a written summary afterwards be useful?
13. **User:** Yes, please send one.
14. **Agent:** Does the same thing happen on your phone?
15. **User:** Yes, exactly the same.
16. **Agent:** Are colleagues able to get in normally?
17. **User:** As far as I know, yes.
18. **Agent:** Are you connected through the office network?
19. **User:** No, I am at home today.
20. **Agent:** Did you change anything on your machine recently?
21. **User:** No, nothing that I noticed.
22. **Agent:** Do you have the authenticator application installed?
23. **User:** Yes, it is on my phone.
24. **Agent:** Was the reset aimed at the credential system the company currently uses?
25. **User:** The company uses federated single sign-on, but the reset was aimed at the old local password store.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the reset targets a credential store the company no longer uses
- `aligned` — the reset targets the company's active authentication system

### Candidate next actions

- **A.** Create an entirely new account for the user instead.
- **B.** Have the user wipe stored browser data before anything else.
- **C.** Close the request and ask the user to retry tomorrow.
- **D.** Hand out a temporary way around the login screen.
- **E.** Start the standard credential reset for the account.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-18

### Public dialogue

1. **User:** Hi, a parcel of mine says it could not be delivered.
2. **Agent:** I can check that. Do you have the tracking reference?
3. **User:** Yes, it begins with seven-seven-four.
4. **Agent:** The delivery run succeeds only when the parcel label matches the current account address; a mismatch sends it back.
5. **User:** Understood; I compared the label with the account.
6. **Agent:** Did the courier leave a card of any kind?
7. **User:** No, I did not find one.
8. **Agent:** Would a collection point be acceptable instead?
9. **User:** Yes, if it is nearby.
10. **Agent:** Is the parcel time-sensitive at all?
11. **User:** Somewhat, I need it this week.
12. **Agent:** Has this happened with earlier parcels?
13. **User:** Not that I can recall.
14. **Agent:** Does the address printed on the parcel match the current account address?
15. **User:** The parcel label and the account both show my current address.
16. **Agent:** Would you like notifications by message?
17. **User:** Yes, that would be useful.
18. **Agent:** Would a neighbour accept the parcel for you?
19. **User:** Yes, the one next door usually would.
20. **Agent:** Is the contact number ending in two-nine-five current?
21. **User:** Yes, that is the right number.
22. **Agent:** Was anybody at home during the attempt?
23. **User:** Yes, I was in all afternoon.
24. **Agent:** Is there a secure porch or side entrance?
25. **User:** There is a porch, yes.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the parcel label contains an outdated destination
- `aligned` — the parcel label matches the current destination

### Candidate next actions

- **A.** Book the parcel onto the next available delivery run.
- **B.** Send out replacement goods straight away.
- **C.** Open a loss claim before another attempt is made.
- **D.** Close the request and ask the user to track it themselves.
- **E.** Ring the depot before arranging anything else.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-19

### Public dialogue

1. **User:** Hi, a parcel of mine says it could not be delivered.
2. **Agent:** I can check that. Do you have the tracking reference?
3. **User:** Yes, it begins with seven-seven-four.
4. **Agent:** The delivery run succeeds only when the parcel label matches the current account address; a mismatch sends it back.
5. **User:** Understood; I compared the label with the account.
6. **Agent:** Would a collection point be acceptable instead?
7. **User:** Yes, if it is nearby.
8. **Agent:** Would you like notifications by message?
9. **User:** Yes, that would be useful.
10. **Agent:** Is there a secure porch or side entrance?
11. **User:** There is a porch, yes.
12. **Agent:** Did the courier leave a card of any kind?
13. **User:** No, I did not find one.
14. **Agent:** Has this happened with earlier parcels?
15. **User:** Not that I can recall.
16. **Agent:** Is the contact number ending in two-nine-five current?
17. **User:** Yes, that is the right number.
18. **Agent:** Would a neighbour accept the parcel for you?
19. **User:** Yes, the one next door usually would.
20. **Agent:** Is the parcel time-sensitive at all?
21. **User:** Somewhat, I need it this week.
22. **Agent:** Was anybody at home during the attempt?
23. **User:** Yes, I was in all afternoon.
24. **Agent:** Does the address printed on the parcel match the current account address?
25. **User:** The parcel label and the account both show my current address.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the parcel label contains an outdated destination
- `aligned` — the parcel label matches the current destination

### Candidate next actions

- **A.** Send out replacement goods straight away.
- **B.** Ring the depot before arranging anything else.
- **C.** Close the request and ask the user to track it themselves.
- **D.** Open a loss claim before another attempt is made.
- **E.** Book the parcel onto the next available delivery run.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-20

### Public dialogue

1. **User:** Hi, there is a charge on my account that I did not make.
2. **Agent:** I can help with that. Do you see the amount and date?
3. **User:** Yes, it is forty-two dollars from last Tuesday.
4. **Agent:** The automated review accepts a dispute only when the charge's card identifier matches the current card record; otherwise it returns unmatched.
5. **User:** Understood; I checked which card identifier the charge used.
6. **Agent:** Have you shared the number with any recurring service?
7. **User:** Only my usual streaming subscription.
8. **Agent:** Do you use the mobile application to check balances?
9. **User:** Yes, almost every day.
10. **Agent:** Would you like alerts for every future transaction?
11. **User:** Yes, please turn those on.
12. **Agent:** Would a paper copy of the outcome be helpful?
13. **User:** No, electronic is fine.
14. **Agent:** Did you travel outside your normal area recently?
15. **User:** No, I have been home all month.
16. **Agent:** Is the mailing address on the profile still correct?
17. **User:** Yes, that address is right.
18. **Agent:** Were there other unfamiliar amounts on the same statement?
19. **User:** No, just that single one.
20. **Agent:** Is the contact number ending in six-one-eight still yours?
21. **User:** Yes, that number is current.
22. **Agent:** Was the physical card in your possession that day?
23. **User:** Yes, it was in my wallet the whole time.
24. **Agent:** Was the disputed charge tied to the same card identifier that is currently on file?
25. **User:** My current card was reissued, but the disputed transaction carried the original card reference.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the charge identifier differs from the current card record
- `aligned` — the charge identifier matches the current card record

### Candidate next actions

- **A.** Ask the merchant for paperwork before opening anything.
- **B.** Freeze the whole account before the charge is examined.
- **C.** File the disputed amount into the automated review queue.
- **D.** Send out another physical card before reviewing the charge.
- **E.** Close the request and tell the user to watch the balance.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-21

### Public dialogue

1. **User:** Hi, I am trying to move my number across to your network.
2. **Agent:** I can start that. Do you have the transfer code ready?
3. **User:** Yes, I received it by text yesterday.
4. **Agent:** The number transfer completes only when its ownership record matches the required direct account holder; an intermediary record is rejected.
5. **User:** Understood; I checked the ownership record.
6. **Agent:** Would you like a confirmation message when it completes?
7. **User:** Yes, please send one.
8. **Agent:** Would you like a paper bill as well?
9. **User:** No, online only is fine.
10. **Agent:** Is the number currently active and in use?
11. **User:** Yes, I am using it right now.
12. **Agent:** Would you like data roaming switched on?
13. **User:** Yes, that would be useful.
14. **Agent:** Is the billing address on file still correct?
15. **User:** Yes, that has not changed.
16. **Agent:** Do you want to keep the same monthly bundle?
17. **User:** Yes, the same one is fine.
18. **Agent:** Do you need international calling enabled?
19. **User:** No, I do not need that.
20. **Agent:** Have you settled the balance with the old network?
21. **User:** Yes, that was cleared last week.
22. **Agent:** Is the alternative contact ending in four-zero-three current?
23. **User:** Yes, that one still works.
24. **Agent:** Does the ownership record on the transfer match the required account holder?
25. **User:** The handset came through a reseller, but the transfer was already updated to my direct subscriber record.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transfer carries an intermediary ownership record instead of the required direct record
- `aligned` — the ownership record matches the required direct account holder

### Candidate next actions

- **A.** Post out another SIM before the transfer is attempted.
- **B.** Send the transfer into the automated porting queue.
- **C.** Read the transfer code back once more before sending anything.
- **D.** Close the request and ask the user to start again later.
- **E.** Give the user a brand new number instead of moving the old one.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-22

### Public dialogue

1. **User:** Hi, I am checking on my flight to Denver this afternoon.
2. **Agent:** I see the two-fifteen departure. Is that the flight you mean?
3. **User:** Yes. I want to make sure everything is on track.
4. **Agent:** A departure delay that is at least as long as the Denver connection window makes the onward flight impossible unless it is protected.
5. **User:** Understood; I have the connection time in front of me.
6. **Agent:** Is the rewards number ending in nine-nine-three yours?
7. **User:** Yes, that is mine.
8. **Agent:** Do you need directions to the departure terminal?
9. **User:** No, I know where to go.
10. **Agent:** Do you already have a seat assignment?
11. **User:** Yes, fourteen C, an aisle.
12. **Agent:** Are you checking any bags?
13. **User:** Just one checked bag.
14. **Agent:** The security wait is about twenty minutes. Are you leaving soon?
15. **User:** Yes, I am heading to the airport shortly.
16. **Agent:** Does anything else on the reservation look wrong?
17. **User:** No, everything else looks right.
18. **Agent:** Do you have dietary or accessibility needs?
19. **User:** No, nothing like that.
20. **Agent:** Is the contact phone number on the booking current?
21. **User:** Yes, it is current.
22. **Agent:** Would you like gate-change notifications by text?
23. **User:** Yes, that would help.
24. **Agent:** How much connection time is scheduled in Denver?
25. **User:** There are four hours between the flights in Denver.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the scheduled connection window is the short ninety-minute option
- `aligned` — the scheduled connection window is the long four-hour option

### Candidate next actions

- **A.** Offer disruption compensation before a disruption occurs.
- **B.** Change the later segment immediately despite the current on-time status.
- **C.** Close the request without monitoring for changes.
- **D.** Replace the current departure even though it is still on time.
- **E.** Enable active monitoring for changes to the itinerary.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-23

### Public dialogue

1. **User:** Hi, my washing machine has stopped draining properly.
2. **Agent:** I can look at that. Do you have the model number?
3. **User:** Yes, it starts with W-D-nine.
4. **Agent:** The standard cover route authorises purchases from the covered retail channel; another purchase channel falls outside its terms.
5. **User:** Understood; I checked how the item was purchased.
6. **Agent:** Is it plumbed into a standard waste pipe?
7. **User:** Yes, the usual arrangement.
8. **Agent:** Is the number ending in one-seven-four still yours?
9. **User:** Yes, that is mine.
10. **Agent:** Is the machine level on the floor?
11. **User:** Yes, it sits flat.
12. **Agent:** Was the purchase made through the channel covered by this claim route?
13. **User:** We bought it as a discounted display unit, while this cover route applies to standard retail purchases.
14. **Agent:** Would weekday or weekend suit for a visit?
15. **User:** Weekdays are easier.
16. **Agent:** Does it make any unusual noise?
17. **User:** There is a low humming sound.
18. **Agent:** How long has it been doing this?
19. **User:** About four days now.
20. **Agent:** Have you cleaned the filter recently?
21. **User:** Yes, I cleared it yesterday.
22. **Agent:** Would you like the outcome confirmed in writing?
23. **User:** Yes, in writing please.
24. **Agent:** Is there parking near the property?
25. **User:** Yes, right outside.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the purchase channel falls outside the submitted cover route
- `aligned` — the purchase channel is covered by the submitted route

### Candidate next actions

- **A.** Send an engineer before any assessment happens.
- **B.** Approve a whole replacement machine straight away.
- **C.** Open the cover claim and send it for assessment.
- **D.** Talk the user through fixing it themselves first.
- **E.** Close the request and ask the user to call back.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-24

### Public dialogue

1. **User:** Hi, my washing machine has stopped draining properly.
2. **Agent:** I can look at that. Do you have the model number?
3. **User:** Yes, it starts with W-D-nine.
4. **Agent:** The standard cover route authorises purchases from the covered retail channel; another purchase channel falls outside its terms.
5. **User:** Understood; I checked how the item was purchased.
6. **Agent:** Would weekday or weekend suit for a visit?
7. **User:** Weekdays are easier.
8. **Agent:** How long has it been doing this?
9. **User:** About four days now.
10. **Agent:** Is the number ending in one-seven-four still yours?
11. **User:** Yes, that is mine.
12. **Agent:** Have you cleaned the filter recently?
13. **User:** Yes, I cleared it yesterday.
14. **Agent:** Does it make any unusual noise?
15. **User:** There is a low humming sound.
16. **Agent:** Is the machine level on the floor?
17. **User:** Yes, it sits flat.
18. **Agent:** Is it plumbed into a standard waste pipe?
19. **User:** Yes, the usual arrangement.
20. **Agent:** Is there parking near the property?
21. **User:** Yes, right outside.
22. **Agent:** Would you like the outcome confirmed in writing?
23. **User:** Yes, in writing please.
24. **Agent:** Was the purchase made through the channel covered by this claim route?
25. **User:** We bought it as a discounted display unit, while this cover route applies to standard retail purchases.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the purchase channel falls outside the submitted cover route
- `aligned` — the purchase channel is covered by the submitted route

### Candidate next actions

- **A.** Open the cover claim and send it for assessment.
- **B.** Talk the user through fixing it themselves first.
- **C.** Close the request and ask the user to call back.
- **D.** Approve a whole replacement machine straight away.
- **E.** Send an engineer before any assessment happens.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-25

### Public dialogue

1. **User:** Hi, I cannot get into my work account this morning.
2. **Agent:** I can help. Does it reject you at the first screen?
3. **User:** Yes, it will not take me past that point.
4. **Agent:** Access is restored only when the reset targets the active authentication system; resetting an unused credential store leaves the account locked.
5. **User:** Understood; I checked which credential system was targeted.
6. **Agent:** Have you tried a different browser?
7. **User:** Yes, I tried two of them.
8. **Agent:** Is the address you enter the work one?
9. **User:** Yes, my work address.
10. **Agent:** Is the recovery contact ending in eight-three-seven current?
11. **User:** Yes, that is still current.
12. **Agent:** Would a written summary afterwards be useful?
13. **User:** Yes, please send one.
14. **Agent:** Does the same thing happen on your phone?
15. **User:** Yes, exactly the same.
16. **Agent:** Are colleagues able to get in normally?
17. **User:** As far as I know, yes.
18. **Agent:** Are you connected through the office network?
19. **User:** No, I am at home today.
20. **Agent:** Did you change anything on your machine recently?
21. **User:** No, nothing that I noticed.
22. **Agent:** Do you have the authenticator application installed?
23. **User:** Yes, it is on my phone.
24. **Agent:** Was the reset aimed at the credential system the company currently uses?
25. **User:** The company uses federated single sign-on, and the reset was aimed at that federated identity system.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the reset targets a credential store the company no longer uses
- `aligned` — the reset targets the company's active authentication system

### Candidate next actions

- **A.** Hand out a temporary way around the login screen.
- **B.** Close the request and ask the user to retry tomorrow.
- **C.** Have the user wipe stored browser data before anything else.
- **D.** Create an entirely new account for the user instead.
- **E.** Start the standard credential reset for the account.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-26

### Public dialogue

1. **User:** Hi, I am calling to refill my blood pressure prescription.
2. **Agent:** Can I get your date of birth to open the profile?
3. **User:** It is March twelfth, nineteen seventy-one.
4. **Agent:** The claim is approved only when the pharmacy billing profile matches the currently active plan; otherwise it is rejected.
5. **User:** Understood; I checked which plan the profile uses.
6. **Agent:** Is the generic version acceptable?
7. **User:** Yes, generic is fine.
8. **Agent:** Is Doctor Patel still the prescriber?
9. **User:** Yes, Doctor Patel is still my doctor.
10. **Agent:** Would you like pickup or delivery?
11. **User:** Pickup is fine.
12. **Agent:** Is the pickup location on Main Street still convenient?
13. **User:** Yes, I am nearby.
14. **Agent:** Are there any new allergies to record?
15. **User:** No new allergies.
16. **Agent:** Do you need any other prescriptions refilled?
17. **User:** No, just this one.
18. **Agent:** Has the dosage changed recently?
19. **User:** No, it is the same ten milligram dose.
20. **Agent:** Is the phone number ending in four-two-two-one current?
21. **User:** Yes, that is still my number.
22. **Agent:** Would you like a text when the order is ready?
23. **User:** Yes, a text is fine.
24. **Agent:** Does the pharmacy billing profile match the plan that is active now?
25. **User:** The replacement plan is active, and the pharmacy profile already shows that same plan.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the pharmacy bills an outdated plan rather than the active plan
- `aligned` — the pharmacy billing profile matches the active plan

### Candidate next actions

- **A.** Bypass the normal transaction and offer another payment route.
- **B.** Submit the order to the automated claim process.
- **C.** Close the request without sending the order.
- **D.** Wait without submitting anything yet.
- **E.** Pause and contact the prescriber for a new order.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-27

### Public dialogue

1. **User:** Hi, a parcel of mine says it could not be delivered.
2. **Agent:** I can check that. Do you have the tracking reference?
3. **User:** Yes, it begins with seven-seven-four.
4. **Agent:** The delivery run succeeds only when the parcel label matches the current account address; a mismatch sends it back.
5. **User:** Understood; I compared the label with the account.
6. **Agent:** Did the courier leave a card of any kind?
7. **User:** No, I did not find one.
8. **Agent:** Would a collection point be acceptable instead?
9. **User:** Yes, if it is nearby.
10. **Agent:** Is the parcel time-sensitive at all?
11. **User:** Somewhat, I need it this week.
12. **Agent:** Has this happened with earlier parcels?
13. **User:** Not that I can recall.
14. **Agent:** Does the address printed on the parcel match the current account address?
15. **User:** The parcel label still shows my previous address, while the account has my current address.
16. **Agent:** Would you like notifications by message?
17. **User:** Yes, that would be useful.
18. **Agent:** Would a neighbour accept the parcel for you?
19. **User:** Yes, the one next door usually would.
20. **Agent:** Is the contact number ending in two-nine-five current?
21. **User:** Yes, that is the right number.
22. **Agent:** Was anybody at home during the attempt?
23. **User:** Yes, I was in all afternoon.
24. **Agent:** Is there a secure porch or side entrance?
25. **User:** There is a porch, yes.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the parcel label contains an outdated destination
- `aligned` — the parcel label matches the current destination

### Candidate next actions

- **A.** Book the parcel onto the next available delivery run.
- **B.** Ring the depot before arranging anything else.
- **C.** Close the request and ask the user to track it themselves.
- **D.** Open a loss claim before another attempt is made.
- **E.** Send out replacement goods straight away.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-28

### Public dialogue

1. **User:** Hi, I am trying to book the specialist appointment I was referred for.
2. **Agent:** I can look at that. Do you have the referral date?
3. **User:** Yes, it was issued on the ninth.
4. **Agent:** Authorization is granted only when the referral comes from the required primary-care source; another source is declined.
5. **User:** Understood; I checked who issued the referral.
6. **Agent:** Is the address on the file still where you live?
7. **User:** Yes, nothing has moved.
8. **Agent:** Do mornings or afternoons suit you better?
9. **User:** Mornings are easier for me.
10. **Agent:** Would you travel to the second site if it were sooner?
11. **User:** Yes, I could manage that.
12. **Agent:** Do you have a preferred practitioner at the practice?
13. **User:** No, whoever is available is fine.
14. **Agent:** Is the phone number ending in three-four-zero correct?
15. **User:** Yes, that one is right.
16. **Agent:** Are you currently taking any regular medication?
17. **User:** Just a vitamin supplement.
18. **Agent:** Did the referral come from the source required for authorization?
19. **User:** The referral came from the walk-in centre, not my regular primary-care physician.
20. **Agent:** Have you seen this specialist before?
21. **User:** No, this would be the first visit.
22. **Agent:** Do you need step-free access at the building?
23. **User:** No, stairs are fine for me.
24. **Agent:** Would you like a reminder message beforehand?
25. **User:** Yes, a message would help.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the referral came from a source that does not qualify
- `aligned` — the referral came from the required qualifying source

### Candidate next actions

- **A.** Reserve the slot and settle the coverage question later.
- **B.** Close the request and ask the user to try again later.
- **C.** Move straight to a self-funded booking instead.
- **D.** Send the booking through for coverage approval.
- **E.** Ring the specialist office before requesting anything.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-29

### Public dialogue

1. **User:** Hi, I am calling to refill my blood pressure prescription.
2. **Agent:** Can I get your date of birth to open the profile?
3. **User:** It is March twelfth, nineteen seventy-one.
4. **Agent:** The claim is approved only when the pharmacy billing profile matches the currently active plan; otherwise it is rejected.
5. **User:** Understood; I checked which plan the profile uses.
6. **Agent:** Would you like a text when the order is ready?
7. **User:** Yes, a text is fine.
8. **Agent:** Is Doctor Patel still the prescriber?
9. **User:** Yes, Doctor Patel is still my doctor.
10. **Agent:** Do you need any other prescriptions refilled?
11. **User:** No, just this one.
12. **Agent:** Is the phone number ending in four-two-two-one current?
13. **User:** Yes, that is still my number.
14. **Agent:** Are there any new allergies to record?
15. **User:** No new allergies.
16. **Agent:** Is the generic version acceptable?
17. **User:** Yes, generic is fine.
18. **Agent:** Is the pickup location on Main Street still convenient?
19. **User:** Yes, I am nearby.
20. **Agent:** Does the pharmacy billing profile match the plan that is active now?
21. **User:** The replacement plan is active, and the pharmacy profile already shows that same plan.
22. **Agent:** Would you like pickup or delivery?
23. **User:** Pickup is fine.
24. **Agent:** Has the dosage changed recently?
25. **User:** No, it is the same ten milligram dose.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the pharmacy bills an outdated plan rather than the active plan
- `aligned` — the pharmacy billing profile matches the active plan

### Candidate next actions

- **A.** Bypass the normal transaction and offer another payment route.
- **B.** Close the request without sending the order.
- **C.** Wait without submitting anything yet.
- **D.** Submit the order to the automated claim process.
- **E.** Pause and contact the prescriber for a new order.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-30

### Public dialogue

1. **User:** Hi, I am trying to move my number across to your network.
2. **Agent:** I can start that. Do you have the transfer code ready?
3. **User:** Yes, I received it by text yesterday.
4. **Agent:** The number transfer completes only when its ownership record matches the required direct account holder; an intermediary record is rejected.
5. **User:** Understood; I checked the ownership record.
6. **Agent:** Would you like a paper bill as well?
7. **User:** No, online only is fine.
8. **Agent:** Does the ownership record on the transfer match the required account holder?
9. **User:** The handset came through a reseller, but the transfer was already updated to my direct subscriber record.
10. **Agent:** Is the number currently active and in use?
11. **User:** Yes, I am using it right now.
12. **Agent:** Is the billing address on file still correct?
13. **User:** Yes, that has not changed.
14. **Agent:** Would you like data roaming switched on?
15. **User:** Yes, that would be useful.
16. **Agent:** Would you like a confirmation message when it completes?
17. **User:** Yes, please send one.
18. **Agent:** Do you need international calling enabled?
19. **User:** No, I do not need that.
20. **Agent:** Do you want to keep the same monthly bundle?
21. **User:** Yes, the same one is fine.
22. **Agent:** Have you settled the balance with the old network?
23. **User:** Yes, that was cleared last week.
24. **Agent:** Is the alternative contact ending in four-zero-three current?
25. **User:** Yes, that one still works.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transfer carries an intermediary ownership record instead of the required direct record
- `aligned` — the ownership record matches the required direct account holder

### Candidate next actions

- **A.** Give the user a brand new number instead of moving the old one.
- **B.** Close the request and ask the user to start again later.
- **C.** Read the transfer code back once more before sending anything.
- **D.** Post out another SIM before the transfer is attempted.
- **E.** Send the transfer into the automated porting queue.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-31

### Public dialogue

1. **User:** Hi, I am trying to move my number across to your network.
2. **Agent:** I can start that. Do you have the transfer code ready?
3. **User:** Yes, I received it by text yesterday.
4. **Agent:** The number transfer completes only when its ownership record matches the required direct account holder; an intermediary record is rejected.
5. **User:** Understood; I checked the ownership record.
6. **Agent:** Would you like a confirmation message when it completes?
7. **User:** Yes, please send one.
8. **Agent:** Would you like a paper bill as well?
9. **User:** No, online only is fine.
10. **Agent:** Is the number currently active and in use?
11. **User:** Yes, I am using it right now.
12. **Agent:** Would you like data roaming switched on?
13. **User:** Yes, that would be useful.
14. **Agent:** Is the billing address on file still correct?
15. **User:** Yes, that has not changed.
16. **Agent:** Do you want to keep the same monthly bundle?
17. **User:** Yes, the same one is fine.
18. **Agent:** Do you need international calling enabled?
19. **User:** No, I do not need that.
20. **Agent:** Have you settled the balance with the old network?
21. **User:** Yes, that was cleared last week.
22. **Agent:** Is the alternative contact ending in four-zero-three current?
23. **User:** Yes, that one still works.
24. **Agent:** Does the ownership record on the transfer match the required account holder?
25. **User:** The handset came through a reseller, and the transfer still carries the reseller's intermediary subscriber record.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transfer carries an intermediary ownership record instead of the required direct record
- `aligned` — the ownership record matches the required direct account holder

### Candidate next actions

- **A.** Read the transfer code back once more before sending anything.
- **B.** Close the request and ask the user to start again later.
- **C.** Post out another SIM before the transfer is attempted.
- **D.** Give the user a brand new number instead of moving the old one.
- **E.** Send the transfer into the automated porting queue.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-32

### Public dialogue

1. **User:** Hi, I am applying for a resident parking permit.
2. **Agent:** I can take you through that. Do you have the property reference?
3. **User:** Yes, it ends in three-one-seven.
4. **Agent:** The eligibility check issues the permit only when the proof names the applicant; proof naming another occupant is refused.
5. **User:** Understood; I compared the names on the documents.
6. **Agent:** Is the vehicle kept at the property overnight?
7. **User:** Yes, every night.
8. **Agent:** Do you need a visitor allowance as well?
9. **User:** No, just the one permit.
10. **Agent:** Is the number ending in two-four-eight still current?
11. **User:** Yes, that is current.
12. **Agent:** Would you like the permit posted or collected?
13. **User:** Posted is easier for me.
14. **Agent:** Have you held a permit in this zone before?
15. **User:** No, this is my first one.
16. **Agent:** Would you like a receipt by email?
17. **User:** Yes, email please.
18. **Agent:** Would you like an annual or monthly permit?
19. **User:** Annual would be better.
20. **Agent:** Does the supporting proof name the same person who is applying for the permit?
21. **User:** The tenancy proof and the permit filing are both in my name.
22. **Agent:** Do you know the registration plate?
23. **User:** Yes, I have it written down here.
24. **Agent:** How many vehicles need covering?
25. **User:** Just the one.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the supporting proof names someone other than the applicant
- `aligned` — the supporting proof names the permit applicant

### Candidate next actions

- **A.** Hand out a temporary permit before any check is run.
- **B.** Send the application into the automated eligibility check.
- **C.** Read the plate back once more before applying.
- **D.** Send the whole thing straight to the appeals team.
- **E.** Close the request and ask the caller to apply again later.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-33

### Public dialogue

1. **User:** Hi, my router keeps dropping the connection every few minutes.
2. **Agent:** Sorry to hear that. How long has this been happening?
3. **User:** About a week now. I work from home, so it is disruptive.
4. **Agent:** The maintenance cycle completes only when the saved configuration is intact; a corrupted configuration makes it stall.
5. **User:** Understood; I checked that detail earlier.
6. **Agent:** Does the unit itself ever lose power?
7. **User:** No, it never fully turns off.
8. **Agent:** Have any cables or ports been changed recently?
9. **User:** No, the cabling is exactly as it was before.
10. **Agent:** Do all devices drop at the same time?
11. **User:** Yes. Phones, TV, and laptop all lose it together.
12. **Agent:** Have you moved it away from possible wireless interference?
13. **User:** Yes, and that made no difference.
14. **Agent:** Have you tried restarting the router?
15. **User:** Yes, I restarted it once already. It came back up but still drops.
16. **Agent:** What do the lights do when the connection drops?
17. **User:** The internet light goes orange for a bit, then back to green.
18. **Agent:** Is the issue on wireless only, or wired too?
19. **User:** Both. Even my desktop on ethernet loses connection.
20. **Agent:** What did the saved-configuration check report before this began?
21. **User:** The saved-configuration check reported intact data after last week's outage.
22. **Agent:** Did your provider report a service interruption?
23. **User:** Their status page shows nothing in my area.
24. **Agent:** Can another nearby customer on the same service connect normally?
25. **User:** Yes, my neighbor uses the same provider and hers is fine.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the saved configuration is corrupted, so maintenance will stall
- `aligned` — the saved configuration is intact, so maintenance will complete

### Candidate next actions

- **A.** Escalate immediately to a hardware replacement.
- **B.** Begin the guided software maintenance procedure.
- **C.** Investigate the upstream service path before changing the device.
- **D.** Close the case and ask the user to monitor it independently.
- **E.** Run the basic power recovery procedure one more time.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-34

### Public dialogue

1. **User:** Hi, my router keeps dropping the connection every few minutes.
2. **Agent:** Sorry to hear that. How long has this been happening?
3. **User:** About a week now. I work from home, so it is disruptive.
4. **Agent:** The maintenance cycle completes only when the saved configuration is intact; a corrupted configuration makes it stall.
5. **User:** Understood; I checked that detail earlier.
6. **Agent:** What did the saved-configuration check report before this began?
7. **User:** The saved-configuration check reported corrupted data after last week's outage.
8. **Agent:** Have you tried restarting the router?
9. **User:** Yes, I restarted it once already. It came back up but still drops.
10. **Agent:** Does the unit itself ever lose power?
11. **User:** No, it never fully turns off.
12. **Agent:** Have any cables or ports been changed recently?
13. **User:** No, the cabling is exactly as it was before.
14. **Agent:** Did your provider report a service interruption?
15. **User:** Their status page shows nothing in my area.
16. **Agent:** Can another nearby customer on the same service connect normally?
17. **User:** Yes, my neighbor uses the same provider and hers is fine.
18. **Agent:** Is the issue on wireless only, or wired too?
19. **User:** Both. Even my desktop on ethernet loses connection.
20. **Agent:** Do all devices drop at the same time?
21. **User:** Yes. Phones, TV, and laptop all lose it together.
22. **Agent:** Have you moved it away from possible wireless interference?
23. **User:** Yes, and that made no difference.
24. **Agent:** What do the lights do when the connection drops?
25. **User:** The internet light goes orange for a bit, then back to green.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the saved configuration is corrupted, so maintenance will stall
- `aligned` — the saved configuration is intact, so maintenance will complete

### Candidate next actions

- **A.** Close the case and ask the user to monitor it independently.
- **B.** Escalate immediately to a hardware replacement.
- **C.** Begin the guided software maintenance procedure.
- **D.** Investigate the upstream service path before changing the device.
- **E.** Run the basic power recovery procedure one more time.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-35

### Public dialogue

1. **User:** Hi, I am checking on my flight to Denver this afternoon.
2. **Agent:** I see the two-fifteen departure. Is that the flight you mean?
3. **User:** Yes. I want to make sure everything is on track.
4. **Agent:** A departure delay that is at least as long as the Denver connection window makes the onward flight impossible unless it is protected.
5. **User:** Understood; I have the connection time in front of me.
6. **Agent:** Do you have dietary or accessibility needs?
7. **User:** No, nothing like that.
8. **Agent:** Is the rewards number ending in nine-nine-three yours?
9. **User:** Yes, that is mine.
10. **Agent:** Do you need directions to the departure terminal?
11. **User:** No, I know where to go.
12. **Agent:** Are you checking any bags?
13. **User:** Just one checked bag.
14. **Agent:** Would you like gate-change notifications by text?
15. **User:** Yes, that would help.
16. **Agent:** Does anything else on the reservation look wrong?
17. **User:** No, everything else looks right.
18. **Agent:** How much connection time is scheduled in Denver?
19. **User:** There are four hours between the flights in Denver.
20. **Agent:** Do you already have a seat assignment?
21. **User:** Yes, fourteen C, an aisle.
22. **Agent:** The security wait is about twenty minutes. Are you leaving soon?
23. **User:** Yes, I am heading to the airport shortly.
24. **Agent:** Is the contact phone number on the booking current?
25. **User:** Yes, it is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the scheduled connection window is the short ninety-minute option
- `aligned` — the scheduled connection window is the long four-hour option

### Candidate next actions

- **A.** Close the request without monitoring for changes.
- **B.** Replace the current departure even though it is still on time.
- **C.** Enable active monitoring for changes to the itinerary.
- **D.** Offer disruption compensation before a disruption occurs.
- **E.** Change the later segment immediately despite the current on-time status.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-36

### Public dialogue

1. **User:** Hi, I am trying to book the specialist appointment I was referred for.
2. **Agent:** I can look at that. Do you have the referral date?
3. **User:** Yes, it was issued on the ninth.
4. **Agent:** Authorization is granted only when the referral comes from the required primary-care source; another source is declined.
5. **User:** Understood; I checked who issued the referral.
6. **Agent:** Are you currently taking any regular medication?
7. **User:** Just a vitamin supplement.
8. **Agent:** Do you have a preferred practitioner at the practice?
9. **User:** No, whoever is available is fine.
10. **Agent:** Would you travel to the second site if it were sooner?
11. **User:** Yes, I could manage that.
12. **Agent:** Is the phone number ending in three-four-zero correct?
13. **User:** Yes, that one is right.
14. **Agent:** Do mornings or afternoons suit you better?
15. **User:** Mornings are easier for me.
16. **Agent:** Do you need step-free access at the building?
17. **User:** No, stairs are fine for me.
18. **Agent:** Would you like a reminder message beforehand?
19. **User:** Yes, a message would help.
20. **Agent:** Is the address on the file still where you live?
21. **User:** Yes, nothing has moved.
22. **Agent:** Have you seen this specialist before?
23. **User:** No, this would be the first visit.
24. **Agent:** Did the referral come from the source required for authorization?
25. **User:** The referral came from my regular primary-care physician, which is the required source.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the referral came from a source that does not qualify
- `aligned` — the referral came from the required qualifying source

### Candidate next actions

- **A.** Close the request and ask the user to try again later.
- **B.** Send the booking through for coverage approval.
- **C.** Move straight to a self-funded booking instead.
- **D.** Ring the specialist office before requesting anything.
- **E.** Reserve the slot and settle the coverage question later.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-37

### Public dialogue

1. **User:** Hi, the heating in my flat has not worked for three days.
2. **Agent:** I am sorry about that. Can you confirm the flat number?
3. **User:** Yes, it is flat twelve on the third floor.
4. **Agent:** The visit can be completed only when the contractor's authority matches the current managing agent's requirements; expired authority blocks access.
5. **User:** Understood; I checked the contractor's access authority.
6. **Agent:** Does the hot water still run?
7. **User:** Yes, the water is fine.
8. **Agent:** Have you checked the thermostat setting?
9. **User:** Yes, it is turned right up.
10. **Agent:** Would you like a text before anyone arrives?
11. **User:** Yes, a text would help.
12. **Agent:** Are neighbours reporting the same problem?
13. **User:** One of them mentioned it too.
14. **Agent:** Is it the whole flat or one room?
15. **User:** The whole flat is cold.
16. **Agent:** Is the number ending in nine-zero-six still right?
17. **User:** Yes, that is my number.
18. **Agent:** Is there a buzzer at the main entrance?
19. **User:** Yes, there is one.
20. **Agent:** Does the contractor hold the access authority required by the current managing agent?
21. **User:** The contractor still has expired authority from the former managing agent, not the current credentials.
22. **Agent:** Would daytime access be possible?
23. **User:** Yes, I work from home.
24. **Agent:** Is there a boiler cupboard inside the flat?
25. **User:** Yes, in the hallway.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the contractor holds expired authority from the former agent
- `aligned` — the contractor holds current authority accepted by the managing agent

### Candidate next actions

- **A.** Move the tenant elsewhere before any visit is attempted.
- **B.** Close the request and ask the tenant to report it again.
- **C.** Approve a complete new heating system immediately.
- **D.** Raise the job and send it to the contractor rota.
- **E.** Post out portable heaters and leave it there.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-38

### Public dialogue

1. **User:** Hi, there is a charge on my account that I did not make.
2. **Agent:** I can help with that. Do you see the amount and date?
3. **User:** Yes, it is forty-two dollars from last Tuesday.
4. **Agent:** The automated review accepts a dispute only when the charge's card identifier matches the current card record; otherwise it returns unmatched.
5. **User:** Understood; I checked which card identifier the charge used.
6. **Agent:** Is the mailing address on the profile still correct?
7. **User:** Yes, that address is right.
8. **Agent:** Did you travel outside your normal area recently?
9. **User:** No, I have been home all month.
10. **Agent:** Would a paper copy of the outcome be helpful?
11. **User:** No, electronic is fine.
12. **Agent:** Would you like alerts for every future transaction?
13. **User:** Yes, please turn those on.
14. **Agent:** Do you use the mobile application to check balances?
15. **User:** Yes, almost every day.
16. **Agent:** Were there other unfamiliar amounts on the same statement?
17. **User:** No, just that single one.
18. **Agent:** Was the disputed charge tied to the same card identifier that is currently on file?
19. **User:** My current card was reissued, but the disputed transaction carried the original card reference.
20. **Agent:** Have you shared the number with any recurring service?
21. **User:** Only my usual streaming subscription.
22. **Agent:** Was the physical card in your possession that day?
23. **User:** Yes, it was in my wallet the whole time.
24. **Agent:** Is the contact number ending in six-one-eight still yours?
25. **User:** Yes, that number is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the charge identifier differs from the current card record
- `aligned` — the charge identifier matches the current card record

### Candidate next actions

- **A.** Close the request and tell the user to watch the balance.
- **B.** Ask the merchant for paperwork before opening anything.
- **C.** Freeze the whole account before the charge is examined.
- **D.** Send out another physical card before reviewing the charge.
- **E.** File the disputed amount into the automated review queue.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-39

### Public dialogue

1. **User:** Hi, I am trying to book the specialist appointment I was referred for.
2. **Agent:** I can look at that. Do you have the referral date?
3. **User:** Yes, it was issued on the ninth.
4. **Agent:** Authorization is granted only when the referral comes from the required primary-care source; another source is declined.
5. **User:** Understood; I checked who issued the referral.
6. **Agent:** Is the address on the file still where you live?
7. **User:** Yes, nothing has moved.
8. **Agent:** Do mornings or afternoons suit you better?
9. **User:** Mornings are easier for me.
10. **Agent:** Would you travel to the second site if it were sooner?
11. **User:** Yes, I could manage that.
12. **Agent:** Do you have a preferred practitioner at the practice?
13. **User:** No, whoever is available is fine.
14. **Agent:** Is the phone number ending in three-four-zero correct?
15. **User:** Yes, that one is right.
16. **Agent:** Are you currently taking any regular medication?
17. **User:** Just a vitamin supplement.
18. **Agent:** Did the referral come from the source required for authorization?
19. **User:** The referral came from my regular primary-care physician, which is the required source.
20. **Agent:** Have you seen this specialist before?
21. **User:** No, this would be the first visit.
22. **Agent:** Do you need step-free access at the building?
23. **User:** No, stairs are fine for me.
24. **Agent:** Would you like a reminder message beforehand?
25. **User:** Yes, a message would help.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the referral came from a source that does not qualify
- `aligned` — the referral came from the required qualifying source

### Candidate next actions

- **A.** Ring the specialist office before requesting anything.
- **B.** Send the booking through for coverage approval.
- **C.** Reserve the slot and settle the coverage question later.
- **D.** Move straight to a self-funded booking instead.
- **E.** Close the request and ask the user to try again later.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-40

### Public dialogue

1. **User:** Hi, my latest energy statement looks far too high.
2. **Agent:** I can look into that. Do you have the account reference?
3. **User:** Yes, it ends in four-eight-one.
4. **Agent:** Reading validation succeeds only when every meter at the property is registered on the account; an omitted meter is flagged.
5. **User:** Understood; I compared the meters with the account.
6. **Agent:** Would you like a breakdown by period?
7. **User:** Yes, that would be helpful.
8. **Agent:** Is the contact number ending in five-five-two right?
9. **User:** Yes, that is correct.
10. **Agent:** Have you added any large appliance lately?
11. **User:** No, nothing new like that.
12. **Agent:** Has your household size changed this quarter?
13. **User:** No, still the same two of us.
14. **Agent:** Has anyone been out to the property recently?
15. **User:** No, nobody has visited.
16. **Agent:** Is the heating electric or gas?
17. **User:** It is all electric here.
18. **Agent:** Is the statement paper or electronic?
19. **User:** Electronic, it arrives by email.
20. **Agent:** Does the account include every meter currently at the property?
21. **User:** The property has two meters, and the supplier profile lists both of them.
22. **Agent:** Do you pay by fixed monthly amount?
23. **User:** Yes, a fixed amount each month.
24. **Agent:** Would you like the outcome by email as well?
25. **User:** Yes, email is fine.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — at least one property meter is missing from the account
- `aligned` — every property meter is registered on the account

### Candidate next actions

- **A.** Read back through old tariff rates before submitting.
- **B.** Send the figure you gave me for automated validation.
- **C.** Refund the difference before anything is validated.
- **D.** Send an engineer out before checking the figure.
- **E.** Close the request and ask the user to watch the next statement.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-41

### Public dialogue

1. **User:** Hi, I am trying to finish enrolling for the coming term.
2. **Agent:** I can help with that. Do you have your student reference?
3. **User:** Yes, it ends in six-two-two.
4. **Agent:** Enrolment is confirmed only when transferred study has the required assessment; unassessed study is held for review.
5. **User:** Understood; I checked the assessment status.
6. **Agent:** Have you arranged your tuition payment method?
7. **User:** Yes, that is all set up.
8. **Agent:** Is your term address the same as last year?
9. **User:** Yes, the same place.
10. **Agent:** Is the contact number ending in eight-one-nine right?
11. **User:** Yes, that is correct.
12. **Agent:** Have you chosen all of your modules yet?
13. **User:** Yes, I picked them last week.
14. **Agent:** Have the transferred credits already received the prior-study assessment required for enrolment?
15. **User:** My overseas transfer credits are still unassessed, although an assessment is required.
16. **Agent:** Are you studying full time or part time?
17. **User:** Full time this year.
18. **Agent:** Do you require any study support arrangements?
19. **User:** No, nothing like that.
20. **Agent:** Do you need a timetable sent to you?
21. **User:** Yes, that would be handy.
22. **Agent:** Would you like a locker on campus?
23. **User:** No, I do not need one.
24. **Agent:** Would you like reminders before the deadline?
25. **User:** Yes, reminders would help.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transferred study has not received its required assessment
- `aligned` — the transferred study has already received the required assessment

### Candidate next actions

- **A.** Put the enrolment through the automated registration run.
- **B.** Close the request and ask the student to try again.
- **C.** Push the whole thing back to a later term instead.
- **D.** Set aside the entry requirements entirely for this student.
- **E.** Go back over the chosen modules before submitting.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-42

### Public dialogue

1. **User:** Hi, I need to report some damage to my car from this morning.
2. **Agent:** I am sorry to hear that. Was anybody injured?
3. **User:** No, thankfully everyone is fine.
4. **Agent:** The assessment settles only when the registered keeper matches the policy name; a mismatch is held for proof.
5. **User:** Understood; I compared the keeper and policy names.
6. **Agent:** Is the car still driveable?
7. **User:** Yes, it drives, but the wing is dented.
8. **Agent:** Does the registered keeper match the person named on the policy?
9. **User:** The vehicle registration and the insurance cover are both in my name.
10. **Agent:** Did anybody witness what happened?
11. **User:** One person nearby saw it.
12. **Agent:** Would you like updates by message?
13. **User:** Yes, messages are fine.
14. **Agent:** Where did the incident take place?
15. **User:** In a supermarket car park.
16. **Agent:** Do you have a preferred repair garage?
17. **User:** No, whichever one you recommend.
18. **Agent:** Was another driver involved?
19. **User:** Yes, but they left before I could speak to them.
20. **Agent:** Is the number ending in seven-six-five still yours?
21. **User:** Yes, that is right.
22. **Agent:** Would you need a courtesy car meanwhile?
23. **User:** Yes, that would help a lot.
24. **Agent:** Have you reported it to the authorities?
25. **User:** Yes, I did that this morning.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the registered keeper and policyholder names differ
- `aligned` — the registered keeper matches the policyholder name

### Candidate next actions

- **A.** Approve the garage work before the report is lodged.
- **B.** Lodge the report into the automated assessment run.
- **C.** Close the report and ask the caller to get in touch later.
- **D.** Chase the bystander for a statement before lodging anything.
- **E.** Write the car off before anything has been assessed.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-43

### Public dialogue

1. **User:** Hi, I am trying to book the specialist appointment I was referred for.
2. **Agent:** I can look at that. Do you have the referral date?
3. **User:** Yes, it was issued on the ninth.
4. **Agent:** Authorization is granted only when the referral comes from the required primary-care source; another source is declined.
5. **User:** Understood; I checked who issued the referral.
6. **Agent:** Did the referral come from the source required for authorization?
7. **User:** The referral came from my regular primary-care physician, which is the required source.
8. **Agent:** Is the address on the file still where you live?
9. **User:** Yes, nothing has moved.
10. **Agent:** Do you need step-free access at the building?
11. **User:** No, stairs are fine for me.
12. **Agent:** Do you have a preferred practitioner at the practice?
13. **User:** No, whoever is available is fine.
14. **Agent:** Do mornings or afternoons suit you better?
15. **User:** Mornings are easier for me.
16. **Agent:** Are you currently taking any regular medication?
17. **User:** Just a vitamin supplement.
18. **Agent:** Would you like a reminder message beforehand?
19. **User:** Yes, a message would help.
20. **Agent:** Is the phone number ending in three-four-zero correct?
21. **User:** Yes, that one is right.
22. **Agent:** Would you travel to the second site if it were sooner?
23. **User:** Yes, I could manage that.
24. **Agent:** Have you seen this specialist before?
25. **User:** No, this would be the first visit.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the referral came from a source that does not qualify
- `aligned` — the referral came from the required qualifying source

### Candidate next actions

- **A.** Ring the specialist office before requesting anything.
- **B.** Reserve the slot and settle the coverage question later.
- **C.** Move straight to a self-funded booking instead.
- **D.** Close the request and ask the user to try again later.
- **E.** Send the booking through for coverage approval.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-44

### Public dialogue

1. **User:** Hi, I am calling to refill my blood pressure prescription.
2. **Agent:** Can I get your date of birth to open the profile?
3. **User:** It is March twelfth, nineteen seventy-one.
4. **Agent:** The claim is approved only when the pharmacy billing profile matches the currently active plan; otherwise it is rejected.
5. **User:** Understood; I checked which plan the profile uses.
6. **Agent:** Is the generic version acceptable?
7. **User:** Yes, generic is fine.
8. **Agent:** Is Doctor Patel still the prescriber?
9. **User:** Yes, Doctor Patel is still my doctor.
10. **Agent:** Would you like pickup or delivery?
11. **User:** Pickup is fine.
12. **Agent:** Is the pickup location on Main Street still convenient?
13. **User:** Yes, I am nearby.
14. **Agent:** Are there any new allergies to record?
15. **User:** No new allergies.
16. **Agent:** Do you need any other prescriptions refilled?
17. **User:** No, just this one.
18. **Agent:** Has the dosage changed recently?
19. **User:** No, it is the same ten milligram dose.
20. **Agent:** Is the phone number ending in four-two-two-one current?
21. **User:** Yes, that is still my number.
22. **Agent:** Would you like a text when the order is ready?
23. **User:** Yes, a text is fine.
24. **Agent:** Does the pharmacy billing profile match the plan that is active now?
25. **User:** The replacement plan is active, but the pharmacy profile still shows my previous plan.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the pharmacy bills an outdated plan rather than the active plan
- `aligned` — the pharmacy billing profile matches the active plan

### Candidate next actions

- **A.** Pause and contact the prescriber for a new order.
- **B.** Submit the order to the automated claim process.
- **C.** Wait without submitting anything yet.
- **D.** Bypass the normal transaction and offer another payment route.
- **E.** Close the request without sending the order.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-45

### Public dialogue

1. **User:** Hi, I am checking on my flight to Denver this afternoon.
2. **Agent:** I see the two-fifteen departure. Is that the flight you mean?
3. **User:** Yes. I want to make sure everything is on track.
4. **Agent:** A departure delay that is at least as long as the Denver connection window makes the onward flight impossible unless it is protected.
5. **User:** Understood; I have the connection time in front of me.
6. **Agent:** Does anything else on the reservation look wrong?
7. **User:** No, everything else looks right.
8. **Agent:** How much connection time is scheduled in Denver?
9. **User:** There are four hours between the flights in Denver.
10. **Agent:** Would you like gate-change notifications by text?
11. **User:** Yes, that would help.
12. **Agent:** Do you need directions to the departure terminal?
13. **User:** No, I know where to go.
14. **Agent:** Are you checking any bags?
15. **User:** Just one checked bag.
16. **Agent:** Is the rewards number ending in nine-nine-three yours?
17. **User:** Yes, that is mine.
18. **Agent:** The security wait is about twenty minutes. Are you leaving soon?
19. **User:** Yes, I am heading to the airport shortly.
20. **Agent:** Do you already have a seat assignment?
21. **User:** Yes, fourteen C, an aisle.
22. **Agent:** Do you have dietary or accessibility needs?
23. **User:** No, nothing like that.
24. **Agent:** Is the contact phone number on the booking current?
25. **User:** Yes, it is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the scheduled connection window is the short ninety-minute option
- `aligned` — the scheduled connection window is the long four-hour option

### Candidate next actions

- **A.** Offer disruption compensation before a disruption occurs.
- **B.** Enable active monitoring for changes to the itinerary.
- **C.** Replace the current departure even though it is still on time.
- **D.** Change the later segment immediately despite the current on-time status.
- **E.** Close the request without monitoring for changes.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-46

### Public dialogue

1. **User:** Hi, I cannot get into my work account this morning.
2. **Agent:** I can help. Does it reject you at the first screen?
3. **User:** Yes, it will not take me past that point.
4. **Agent:** Access is restored only when the reset targets the active authentication system; resetting an unused credential store leaves the account locked.
5. **User:** Understood; I checked which credential system was targeted.
6. **Agent:** Have you tried a different browser?
7. **User:** Yes, I tried two of them.
8. **Agent:** Was the reset aimed at the credential system the company currently uses?
9. **User:** The company uses federated single sign-on, but the reset was aimed at the old local password store.
10. **Agent:** Would a written summary afterwards be useful?
11. **User:** Yes, please send one.
12. **Agent:** Is the address you enter the work one?
13. **User:** Yes, my work address.
14. **Agent:** Do you have the authenticator application installed?
15. **User:** Yes, it is on my phone.
16. **Agent:** Is the recovery contact ending in eight-three-seven current?
17. **User:** Yes, that is still current.
18. **Agent:** Does the same thing happen on your phone?
19. **User:** Yes, exactly the same.
20. **Agent:** Did you change anything on your machine recently?
21. **User:** No, nothing that I noticed.
22. **Agent:** Are colleagues able to get in normally?
23. **User:** As far as I know, yes.
24. **Agent:** Are you connected through the office network?
25. **User:** No, I am at home today.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the reset targets a credential store the company no longer uses
- `aligned` — the reset targets the company's active authentication system

### Candidate next actions

- **A.** Start the standard credential reset for the account.
- **B.** Close the request and ask the user to retry tomorrow.
- **C.** Have the user wipe stored browser data before anything else.
- **D.** Create an entirely new account for the user instead.
- **E.** Hand out a temporary way around the login screen.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-47

### Public dialogue

1. **User:** Hi, I cannot get into my work account this morning.
2. **Agent:** I can help. Does it reject you at the first screen?
3. **User:** Yes, it will not take me past that point.
4. **Agent:** Access is restored only when the reset targets the active authentication system; resetting an unused credential store leaves the account locked.
5. **User:** Understood; I checked which credential system was targeted.
6. **Agent:** Have you tried a different browser?
7. **User:** Yes, I tried two of them.
8. **Agent:** Would a written summary afterwards be useful?
9. **User:** Yes, please send one.
10. **Agent:** Are colleagues able to get in normally?
11. **User:** As far as I know, yes.
12. **Agent:** Do you have the authenticator application installed?
13. **User:** Yes, it is on my phone.
14. **Agent:** Are you connected through the office network?
15. **User:** No, I am at home today.
16. **Agent:** Does the same thing happen on your phone?
17. **User:** Yes, exactly the same.
18. **Agent:** Was the reset aimed at the credential system the company currently uses?
19. **User:** The company uses federated single sign-on, but the reset was aimed at the old local password store.
20. **Agent:** Is the recovery contact ending in eight-three-seven current?
21. **User:** Yes, that is still current.
22. **Agent:** Did you change anything on your machine recently?
23. **User:** No, nothing that I noticed.
24. **Agent:** Is the address you enter the work one?
25. **User:** Yes, my work address.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the reset targets a credential store the company no longer uses
- `aligned` — the reset targets the company's active authentication system

### Candidate next actions

- **A.** Close the request and ask the user to retry tomorrow.
- **B.** Hand out a temporary way around the login screen.
- **C.** Create an entirely new account for the user instead.
- **D.** Have the user wipe stored browser data before anything else.
- **E.** Start the standard credential reset for the account.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-48

### Public dialogue

1. **User:** Hi, I need to report some damage to my car from this morning.
2. **Agent:** I am sorry to hear that. Was anybody injured?
3. **User:** No, thankfully everyone is fine.
4. **Agent:** The assessment settles only when the registered keeper matches the policy name; a mismatch is held for proof.
5. **User:** Understood; I compared the keeper and policy names.
6. **Agent:** Where did the incident take place?
7. **User:** In a supermarket car park.
8. **Agent:** Was another driver involved?
9. **User:** Yes, but they left before I could speak to them.
10. **Agent:** Would you need a courtesy car meanwhile?
11. **User:** Yes, that would help a lot.
12. **Agent:** Would you like updates by message?
13. **User:** Yes, messages are fine.
14. **Agent:** Is the car still driveable?
15. **User:** Yes, it drives, but the wing is dented.
16. **Agent:** Have you reported it to the authorities?
17. **User:** Yes, I did that this morning.
18. **Agent:** Do you have a preferred repair garage?
19. **User:** No, whichever one you recommend.
20. **Agent:** Did anybody witness what happened?
21. **User:** One person nearby saw it.
22. **Agent:** Is the number ending in seven-six-five still yours?
23. **User:** Yes, that is right.
24. **Agent:** Does the registered keeper match the person named on the policy?
25. **User:** The vehicle is registered to my partner, while the insurance cover names me.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the registered keeper and policyholder names differ
- `aligned` — the registered keeper matches the policyholder name

### Candidate next actions

- **A.** Approve the garage work before the report is lodged.
- **B.** Write the car off before anything has been assessed.
- **C.** Lodge the report into the automated assessment run.
- **D.** Chase the bystander for a statement before lodging anything.
- **E.** Close the report and ask the caller to get in touch later.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-49

### Public dialogue

1. **User:** Hi, I am trying to finish enrolling for the coming term.
2. **Agent:** I can help with that. Do you have your student reference?
3. **User:** Yes, it ends in six-two-two.
4. **Agent:** Enrolment is confirmed only when transferred study has the required assessment; unassessed study is held for review.
5. **User:** Understood; I checked the assessment status.
6. **Agent:** Do you need a timetable sent to you?
7. **User:** Yes, that would be handy.
8. **Agent:** Would you like a locker on campus?
9. **User:** No, I do not need one.
10. **Agent:** Is the contact number ending in eight-one-nine right?
11. **User:** Yes, that is correct.
12. **Agent:** Would you like reminders before the deadline?
13. **User:** Yes, reminders would help.
14. **Agent:** Have you chosen all of your modules yet?
15. **User:** Yes, I picked them last week.
16. **Agent:** Do you require any study support arrangements?
17. **User:** No, nothing like that.
18. **Agent:** Have the transferred credits already received the prior-study assessment required for enrolment?
19. **User:** My overseas transfer credits are still unassessed, although an assessment is required.
20. **Agent:** Are you studying full time or part time?
21. **User:** Full time this year.
22. **Agent:** Have you arranged your tuition payment method?
23. **User:** Yes, that is all set up.
24. **Agent:** Is your term address the same as last year?
25. **User:** Yes, the same place.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transferred study has not received its required assessment
- `aligned` — the transferred study has already received the required assessment

### Candidate next actions

- **A.** Go back over the chosen modules before submitting.
- **B.** Close the request and ask the student to try again.
- **C.** Push the whole thing back to a later term instead.
- **D.** Put the enrolment through the automated registration run.
- **E.** Set aside the entry requirements entirely for this student.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-50

### Public dialogue

1. **User:** Hi, my washing machine has stopped draining properly.
2. **Agent:** I can look at that. Do you have the model number?
3. **User:** Yes, it starts with W-D-nine.
4. **Agent:** The standard cover route authorises purchases from the covered retail channel; another purchase channel falls outside its terms.
5. **User:** Understood; I checked how the item was purchased.
6. **Agent:** Is it plumbed into a standard waste pipe?
7. **User:** Yes, the usual arrangement.
8. **Agent:** Is the number ending in one-seven-four still yours?
9. **User:** Yes, that is mine.
10. **Agent:** Is the machine level on the floor?
11. **User:** Yes, it sits flat.
12. **Agent:** Was the purchase made through the channel covered by this claim route?
13. **User:** We bought it as a standard retail item, which is the purchase channel covered by this route.
14. **Agent:** Would weekday or weekend suit for a visit?
15. **User:** Weekdays are easier.
16. **Agent:** Does it make any unusual noise?
17. **User:** There is a low humming sound.
18. **Agent:** How long has it been doing this?
19. **User:** About four days now.
20. **Agent:** Have you cleaned the filter recently?
21. **User:** Yes, I cleared it yesterday.
22. **Agent:** Would you like the outcome confirmed in writing?
23. **User:** Yes, in writing please.
24. **Agent:** Is there parking near the property?
25. **User:** Yes, right outside.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the purchase channel falls outside the submitted cover route
- `aligned` — the purchase channel is covered by the submitted route

### Candidate next actions

- **A.** Send an engineer before any assessment happens.
- **B.** Close the request and ask the user to call back.
- **C.** Talk the user through fixing it themselves first.
- **D.** Open the cover claim and send it for assessment.
- **E.** Approve a whole replacement machine straight away.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-51

### Public dialogue

1. **User:** Hi, I am applying for a resident parking permit.
2. **Agent:** I can take you through that. Do you have the property reference?
3. **User:** Yes, it ends in three-one-seven.
4. **Agent:** The eligibility check issues the permit only when the proof names the applicant; proof naming another occupant is refused.
5. **User:** Understood; I compared the names on the documents.
6. **Agent:** Do you need a visitor allowance as well?
7. **User:** No, just the one permit.
8. **Agent:** Does the supporting proof name the same person who is applying for the permit?
9. **User:** The tenancy proof is in my flatmate's name, while I am the person filing for the permit.
10. **Agent:** Would you like an annual or monthly permit?
11. **User:** Annual would be better.
12. **Agent:** Is the vehicle kept at the property overnight?
13. **User:** Yes, every night.
14. **Agent:** Do you know the registration plate?
15. **User:** Yes, I have it written down here.
16. **Agent:** Would you like the permit posted or collected?
17. **User:** Posted is easier for me.
18. **Agent:** How many vehicles need covering?
19. **User:** Just the one.
20. **Agent:** Have you held a permit in this zone before?
21. **User:** No, this is my first one.
22. **Agent:** Would you like a receipt by email?
23. **User:** Yes, email please.
24. **Agent:** Is the number ending in two-four-eight still current?
25. **User:** Yes, that is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the supporting proof names someone other than the applicant
- `aligned` — the supporting proof names the permit applicant

### Candidate next actions

- **A.** Read the plate back once more before applying.
- **B.** Send the application into the automated eligibility check.
- **C.** Close the request and ask the caller to apply again later.
- **D.** Send the whole thing straight to the appeals team.
- **E.** Hand out a temporary permit before any check is run.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-52

### Public dialogue

1. **User:** Hi, my washing machine has stopped draining properly.
2. **Agent:** I can look at that. Do you have the model number?
3. **User:** Yes, it starts with W-D-nine.
4. **Agent:** The standard cover route authorises purchases from the covered retail channel; another purchase channel falls outside its terms.
5. **User:** Understood; I checked how the item was purchased.
6. **Agent:** Have you cleaned the filter recently?
7. **User:** Yes, I cleared it yesterday.
8. **Agent:** Is there parking near the property?
9. **User:** Yes, right outside.
10. **Agent:** Is the number ending in one-seven-four still yours?
11. **User:** Yes, that is mine.
12. **Agent:** Would you like the outcome confirmed in writing?
13. **User:** Yes, in writing please.
14. **Agent:** Is the machine level on the floor?
15. **User:** Yes, it sits flat.
16. **Agent:** How long has it been doing this?
17. **User:** About four days now.
18. **Agent:** Is it plumbed into a standard waste pipe?
19. **User:** Yes, the usual arrangement.
20. **Agent:** Was the purchase made through the channel covered by this claim route?
21. **User:** We bought it as a discounted display unit, while this cover route applies to standard retail purchases.
22. **Agent:** Would weekday or weekend suit for a visit?
23. **User:** Weekdays are easier.
24. **Agent:** Does it make any unusual noise?
25. **User:** There is a low humming sound.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the purchase channel falls outside the submitted cover route
- `aligned` — the purchase channel is covered by the submitted route

### Candidate next actions

- **A.** Approve a whole replacement machine straight away.
- **B.** Open the cover claim and send it for assessment.
- **C.** Close the request and ask the user to call back.
- **D.** Talk the user through fixing it themselves first.
- **E.** Send an engineer before any assessment happens.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-53

### Public dialogue

1. **User:** Hi, I am calling to refill my blood pressure prescription.
2. **Agent:** Can I get your date of birth to open the profile?
3. **User:** It is March twelfth, nineteen seventy-one.
4. **Agent:** The claim is approved only when the pharmacy billing profile matches the currently active plan; otherwise it is rejected.
5. **User:** Understood; I checked which plan the profile uses.
6. **Agent:** Is the generic version acceptable?
7. **User:** Yes, generic is fine.
8. **Agent:** Does the pharmacy billing profile match the plan that is active now?
9. **User:** The replacement plan is active, but the pharmacy profile still shows my previous plan.
10. **Agent:** Do you need any other prescriptions refilled?
11. **User:** No, just this one.
12. **Agent:** Would you like a text when the order is ready?
13. **User:** Yes, a text is fine.
14. **Agent:** Has the dosage changed recently?
15. **User:** No, it is the same ten milligram dose.
16. **Agent:** Is Doctor Patel still the prescriber?
17. **User:** Yes, Doctor Patel is still my doctor.
18. **Agent:** Would you like pickup or delivery?
19. **User:** Pickup is fine.
20. **Agent:** Is the pickup location on Main Street still convenient?
21. **User:** Yes, I am nearby.
22. **Agent:** Is the phone number ending in four-two-two-one current?
23. **User:** Yes, that is still my number.
24. **Agent:** Are there any new allergies to record?
25. **User:** No new allergies.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the pharmacy bills an outdated plan rather than the active plan
- `aligned` — the pharmacy billing profile matches the active plan

### Candidate next actions

- **A.** Bypass the normal transaction and offer another payment route.
- **B.** Submit the order to the automated claim process.
- **C.** Pause and contact the prescriber for a new order.
- **D.** Close the request without sending the order.
- **E.** Wait without submitting anything yet.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-54

### Public dialogue

1. **User:** Hi, the heating in my flat has not worked for three days.
2. **Agent:** I am sorry about that. Can you confirm the flat number?
3. **User:** Yes, it is flat twelve on the third floor.
4. **Agent:** The visit can be completed only when the contractor's authority matches the current managing agent's requirements; expired authority blocks access.
5. **User:** Understood; I checked the contractor's access authority.
6. **Agent:** Is there a boiler cupboard inside the flat?
7. **User:** Yes, in the hallway.
8. **Agent:** Have you checked the thermostat setting?
9. **User:** Yes, it is turned right up.
10. **Agent:** Are neighbours reporting the same problem?
11. **User:** One of them mentioned it too.
12. **Agent:** Is it the whole flat or one room?
13. **User:** The whole flat is cold.
14. **Agent:** Is there a buzzer at the main entrance?
15. **User:** Yes, there is one.
16. **Agent:** Does the hot water still run?
17. **User:** Yes, the water is fine.
18. **Agent:** Is the number ending in nine-zero-six still right?
19. **User:** Yes, that is my number.
20. **Agent:** Would daytime access be possible?
21. **User:** Yes, I work from home.
22. **Agent:** Would you like a text before anyone arrives?
23. **User:** Yes, a text would help.
24. **Agent:** Does the contractor hold the access authority required by the current managing agent?
25. **User:** The contractor has the current authority required by the present managing agent.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the contractor holds expired authority from the former agent
- `aligned` — the contractor holds current authority accepted by the managing agent

### Candidate next actions

- **A.** Approve a complete new heating system immediately.
- **B.** Raise the job and send it to the contractor rota.
- **C.** Close the request and ask the tenant to report it again.
- **D.** Move the tenant elsewhere before any visit is attempted.
- **E.** Post out portable heaters and leave it there.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-55

### Public dialogue

1. **User:** Hi, my router keeps dropping the connection every few minutes.
2. **Agent:** Sorry to hear that. How long has this been happening?
3. **User:** About a week now. I work from home, so it is disruptive.
4. **Agent:** The maintenance cycle completes only when the saved configuration is intact; a corrupted configuration makes it stall.
5. **User:** Understood; I checked that detail earlier.
6. **Agent:** Did your provider report a service interruption?
7. **User:** Their status page shows nothing in my area.
8. **Agent:** Have you tried restarting the router?
9. **User:** Yes, I restarted it once already. It came back up but still drops.
10. **Agent:** Have any cables or ports been changed recently?
11. **User:** No, the cabling is exactly as it was before.
12. **Agent:** Does the unit itself ever lose power?
13. **User:** No, it never fully turns off.
14. **Agent:** What do the lights do when the connection drops?
15. **User:** The internet light goes orange for a bit, then back to green.
16. **Agent:** Is the issue on wireless only, or wired too?
17. **User:** Both. Even my desktop on ethernet loses connection.
18. **Agent:** Do all devices drop at the same time?
19. **User:** Yes. Phones, TV, and laptop all lose it together.
20. **Agent:** Can another nearby customer on the same service connect normally?
21. **User:** Yes, my neighbor uses the same provider and hers is fine.
22. **Agent:** Have you moved it away from possible wireless interference?
23. **User:** Yes, and that made no difference.
24. **Agent:** What did the saved-configuration check report before this began?
25. **User:** The saved-configuration check reported corrupted data after last week's outage.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the saved configuration is corrupted, so maintenance will stall
- `aligned` — the saved configuration is intact, so maintenance will complete

### Candidate next actions

- **A.** Escalate immediately to a hardware replacement.
- **B.** Close the case and ask the user to monitor it independently.
- **C.** Run the basic power recovery procedure one more time.
- **D.** Begin the guided software maintenance procedure.
- **E.** Investigate the upstream service path before changing the device.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-56

### Public dialogue

1. **User:** Hi, there is a charge on my account that I did not make.
2. **Agent:** I can help with that. Do you see the amount and date?
3. **User:** Yes, it is forty-two dollars from last Tuesday.
4. **Agent:** The automated review accepts a dispute only when the charge's card identifier matches the current card record; otherwise it returns unmatched.
5. **User:** Understood; I checked which card identifier the charge used.
6. **Agent:** Have you shared the number with any recurring service?
7. **User:** Only my usual streaming subscription.
8. **Agent:** Do you use the mobile application to check balances?
9. **User:** Yes, almost every day.
10. **Agent:** Would you like alerts for every future transaction?
11. **User:** Yes, please turn those on.
12. **Agent:** Would a paper copy of the outcome be helpful?
13. **User:** No, electronic is fine.
14. **Agent:** Did you travel outside your normal area recently?
15. **User:** No, I have been home all month.
16. **Agent:** Is the mailing address on the profile still correct?
17. **User:** Yes, that address is right.
18. **Agent:** Were there other unfamiliar amounts on the same statement?
19. **User:** No, just that single one.
20. **Agent:** Is the contact number ending in six-one-eight still yours?
21. **User:** Yes, that number is current.
22. **Agent:** Was the physical card in your possession that day?
23. **User:** Yes, it was in my wallet the whole time.
24. **Agent:** Was the disputed charge tied to the same card identifier that is currently on file?
25. **User:** My current card was reissued, and the disputed transaction carried that same reissued-card reference.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the charge identifier differs from the current card record
- `aligned` — the charge identifier matches the current card record

### Candidate next actions

- **A.** Freeze the whole account before the charge is examined.
- **B.** Ask the merchant for paperwork before opening anything.
- **C.** Send out another physical card before reviewing the charge.
- **D.** Close the request and tell the user to watch the balance.
- **E.** File the disputed amount into the automated review queue.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-57

### Public dialogue

1. **User:** Hi, a parcel of mine says it could not be delivered.
2. **Agent:** I can check that. Do you have the tracking reference?
3. **User:** Yes, it begins with seven-seven-four.
4. **Agent:** The delivery run succeeds only when the parcel label matches the current account address; a mismatch sends it back.
5. **User:** Understood; I compared the label with the account.
6. **Agent:** Would a collection point be acceptable instead?
7. **User:** Yes, if it is nearby.
8. **Agent:** Would you like notifications by message?
9. **User:** Yes, that would be useful.
10. **Agent:** Is there a secure porch or side entrance?
11. **User:** There is a porch, yes.
12. **Agent:** Did the courier leave a card of any kind?
13. **User:** No, I did not find one.
14. **Agent:** Has this happened with earlier parcels?
15. **User:** Not that I can recall.
16. **Agent:** Is the contact number ending in two-nine-five current?
17. **User:** Yes, that is the right number.
18. **Agent:** Would a neighbour accept the parcel for you?
19. **User:** Yes, the one next door usually would.
20. **Agent:** Is the parcel time-sensitive at all?
21. **User:** Somewhat, I need it this week.
22. **Agent:** Was anybody at home during the attempt?
23. **User:** Yes, I was in all afternoon.
24. **Agent:** Does the address printed on the parcel match the current account address?
25. **User:** The parcel label still shows my previous address, while the account has my current address.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the parcel label contains an outdated destination
- `aligned` — the parcel label matches the current destination

### Candidate next actions

- **A.** Close the request and ask the user to track it themselves.
- **B.** Ring the depot before arranging anything else.
- **C.** Send out replacement goods straight away.
- **D.** Open a loss claim before another attempt is made.
- **E.** Book the parcel onto the next available delivery run.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-58

### Public dialogue

1. **User:** Hi, I am trying to finish enrolling for the coming term.
2. **Agent:** I can help with that. Do you have your student reference?
3. **User:** Yes, it ends in six-two-two.
4. **Agent:** Enrolment is confirmed only when transferred study has the required assessment; unassessed study is held for review.
5. **User:** Understood; I checked the assessment status.
6. **Agent:** Do you need a timetable sent to you?
7. **User:** Yes, that would be handy.
8. **Agent:** Would you like a locker on campus?
9. **User:** No, I do not need one.
10. **Agent:** Is the contact number ending in eight-one-nine right?
11. **User:** Yes, that is correct.
12. **Agent:** Would you like reminders before the deadline?
13. **User:** Yes, reminders would help.
14. **Agent:** Have you chosen all of your modules yet?
15. **User:** Yes, I picked them last week.
16. **Agent:** Do you require any study support arrangements?
17. **User:** No, nothing like that.
18. **Agent:** Have the transferred credits already received the prior-study assessment required for enrolment?
19. **User:** My overseas transfer credits have already received the required assessment.
20. **Agent:** Are you studying full time or part time?
21. **User:** Full time this year.
22. **Agent:** Have you arranged your tuition payment method?
23. **User:** Yes, that is all set up.
24. **Agent:** Is your term address the same as last year?
25. **User:** Yes, the same place.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transferred study has not received its required assessment
- `aligned` — the transferred study has already received the required assessment

### Candidate next actions

- **A.** Put the enrolment through the automated registration run.
- **B.** Push the whole thing back to a later term instead.
- **C.** Go back over the chosen modules before submitting.
- **D.** Close the request and ask the student to try again.
- **E.** Set aside the entry requirements entirely for this student.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-59

### Public dialogue

1. **User:** Hi, a parcel of mine says it could not be delivered.
2. **Agent:** I can check that. Do you have the tracking reference?
3. **User:** Yes, it begins with seven-seven-four.
4. **Agent:** The delivery run succeeds only when the parcel label matches the current account address; a mismatch sends it back.
5. **User:** Understood; I compared the label with the account.
6. **Agent:** Has this happened with earlier parcels?
7. **User:** Not that I can recall.
8. **Agent:** Is the contact number ending in two-nine-five current?
9. **User:** Yes, that is the right number.
10. **Agent:** Would you like notifications by message?
11. **User:** Yes, that would be useful.
12. **Agent:** Was anybody at home during the attempt?
13. **User:** Yes, I was in all afternoon.
14. **Agent:** Would a neighbour accept the parcel for you?
15. **User:** Yes, the one next door usually would.
16. **Agent:** Is there a secure porch or side entrance?
17. **User:** There is a porch, yes.
18. **Agent:** Does the address printed on the parcel match the current account address?
19. **User:** The parcel label and the account both show my current address.
20. **Agent:** Is the parcel time-sensitive at all?
21. **User:** Somewhat, I need it this week.
22. **Agent:** Did the courier leave a card of any kind?
23. **User:** No, I did not find one.
24. **Agent:** Would a collection point be acceptable instead?
25. **User:** Yes, if it is nearby.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the parcel label contains an outdated destination
- `aligned` — the parcel label matches the current destination

### Candidate next actions

- **A.** Close the request and ask the user to track it themselves.
- **B.** Send out replacement goods straight away.
- **C.** Ring the depot before arranging anything else.
- **D.** Book the parcel onto the next available delivery run.
- **E.** Open a loss claim before another attempt is made.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-60

### Public dialogue

1. **User:** Hi, I need to report some damage to my car from this morning.
2. **Agent:** I am sorry to hear that. Was anybody injured?
3. **User:** No, thankfully everyone is fine.
4. **Agent:** The assessment settles only when the registered keeper matches the policy name; a mismatch is held for proof.
5. **User:** Understood; I compared the keeper and policy names.
6. **Agent:** Is the car still driveable?
7. **User:** Yes, it drives, but the wing is dented.
8. **Agent:** Does the registered keeper match the person named on the policy?
9. **User:** The vehicle is registered to my partner, while the insurance cover names me.
10. **Agent:** Did anybody witness what happened?
11. **User:** One person nearby saw it.
12. **Agent:** Would you like updates by message?
13. **User:** Yes, messages are fine.
14. **Agent:** Where did the incident take place?
15. **User:** In a supermarket car park.
16. **Agent:** Do you have a preferred repair garage?
17. **User:** No, whichever one you recommend.
18. **Agent:** Was another driver involved?
19. **User:** Yes, but they left before I could speak to them.
20. **Agent:** Is the number ending in seven-six-five still yours?
21. **User:** Yes, that is right.
22. **Agent:** Would you need a courtesy car meanwhile?
23. **User:** Yes, that would help a lot.
24. **Agent:** Have you reported it to the authorities?
25. **User:** Yes, I did that this morning.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the registered keeper and policyholder names differ
- `aligned` — the registered keeper matches the policyholder name

### Candidate next actions

- **A.** Approve the garage work before the report is lodged.
- **B.** Close the report and ask the caller to get in touch later.
- **C.** Write the car off before anything has been assessed.
- **D.** Chase the bystander for a statement before lodging anything.
- **E.** Lodge the report into the automated assessment run.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-61

### Public dialogue

1. **User:** Hi, I am trying to finish enrolling for the coming term.
2. **Agent:** I can help with that. Do you have your student reference?
3. **User:** Yes, it ends in six-two-two.
4. **Agent:** Enrolment is confirmed only when transferred study has the required assessment; unassessed study is held for review.
5. **User:** Understood; I checked the assessment status.
6. **Agent:** Have you chosen all of your modules yet?
7. **User:** Yes, I picked them last week.
8. **Agent:** Have you arranged your tuition payment method?
9. **User:** Yes, that is all set up.
10. **Agent:** Are you studying full time or part time?
11. **User:** Full time this year.
12. **Agent:** Is your term address the same as last year?
13. **User:** Yes, the same place.
14. **Agent:** Do you need a timetable sent to you?
15. **User:** Yes, that would be handy.
16. **Agent:** Is the contact number ending in eight-one-nine right?
17. **User:** Yes, that is correct.
18. **Agent:** Would you like a locker on campus?
19. **User:** No, I do not need one.
20. **Agent:** Do you require any study support arrangements?
21. **User:** No, nothing like that.
22. **Agent:** Would you like reminders before the deadline?
23. **User:** Yes, reminders would help.
24. **Agent:** Have the transferred credits already received the prior-study assessment required for enrolment?
25. **User:** My overseas transfer credits are still unassessed, although an assessment is required.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transferred study has not received its required assessment
- `aligned` — the transferred study has already received the required assessment

### Candidate next actions

- **A.** Put the enrolment through the automated registration run.
- **B.** Close the request and ask the student to try again.
- **C.** Go back over the chosen modules before submitting.
- **D.** Push the whole thing back to a later term instead.
- **E.** Set aside the entry requirements entirely for this student.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-62

### Public dialogue

1. **User:** Hi, I am trying to book the specialist appointment I was referred for.
2. **Agent:** I can look at that. Do you have the referral date?
3. **User:** Yes, it was issued on the ninth.
4. **Agent:** Authorization is granted only when the referral comes from the required primary-care source; another source is declined.
5. **User:** Understood; I checked who issued the referral.
6. **Agent:** Did the referral come from the source required for authorization?
7. **User:** The referral came from the walk-in centre, not my regular primary-care physician.
8. **Agent:** Is the address on the file still where you live?
9. **User:** Yes, nothing has moved.
10. **Agent:** Do you need step-free access at the building?
11. **User:** No, stairs are fine for me.
12. **Agent:** Do you have a preferred practitioner at the practice?
13. **User:** No, whoever is available is fine.
14. **Agent:** Do mornings or afternoons suit you better?
15. **User:** Mornings are easier for me.
16. **Agent:** Are you currently taking any regular medication?
17. **User:** Just a vitamin supplement.
18. **Agent:** Would you like a reminder message beforehand?
19. **User:** Yes, a message would help.
20. **Agent:** Is the phone number ending in three-four-zero correct?
21. **User:** Yes, that one is right.
22. **Agent:** Would you travel to the second site if it were sooner?
23. **User:** Yes, I could manage that.
24. **Agent:** Have you seen this specialist before?
25. **User:** No, this would be the first visit.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the referral came from a source that does not qualify
- `aligned` — the referral came from the required qualifying source

### Candidate next actions

- **A.** Move straight to a self-funded booking instead.
- **B.** Reserve the slot and settle the coverage question later.
- **C.** Ring the specialist office before requesting anything.
- **D.** Send the booking through for coverage approval.
- **E.** Close the request and ask the user to try again later.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-63

### Public dialogue

1. **User:** Hi, I need to report some damage to my car from this morning.
2. **Agent:** I am sorry to hear that. Was anybody injured?
3. **User:** No, thankfully everyone is fine.
4. **Agent:** The assessment settles only when the registered keeper matches the policy name; a mismatch is held for proof.
5. **User:** Understood; I compared the keeper and policy names.
6. **Agent:** Where did the incident take place?
7. **User:** In a supermarket car park.
8. **Agent:** Would you like updates by message?
9. **User:** Yes, messages are fine.
10. **Agent:** Is the number ending in seven-six-five still yours?
11. **User:** Yes, that is right.
12. **Agent:** Do you have a preferred repair garage?
13. **User:** No, whichever one you recommend.
14. **Agent:** Have you reported it to the authorities?
15. **User:** Yes, I did that this morning.
16. **Agent:** Did anybody witness what happened?
17. **User:** One person nearby saw it.
18. **Agent:** Does the registered keeper match the person named on the policy?
19. **User:** The vehicle is registered to my partner, while the insurance cover names me.
20. **Agent:** Was another driver involved?
21. **User:** Yes, but they left before I could speak to them.
22. **Agent:** Would you need a courtesy car meanwhile?
23. **User:** Yes, that would help a lot.
24. **Agent:** Is the car still driveable?
25. **User:** Yes, it drives, but the wing is dented.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the registered keeper and policyholder names differ
- `aligned` — the registered keeper matches the policyholder name

### Candidate next actions

- **A.** Close the report and ask the caller to get in touch later.
- **B.** Lodge the report into the automated assessment run.
- **C.** Chase the bystander for a statement before lodging anything.
- **D.** Write the car off before anything has been assessed.
- **E.** Approve the garage work before the report is lodged.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-64

### Public dialogue

1. **User:** Hi, my router keeps dropping the connection every few minutes.
2. **Agent:** Sorry to hear that. How long has this been happening?
3. **User:** About a week now. I work from home, so it is disruptive.
4. **Agent:** The maintenance cycle completes only when the saved configuration is intact; a corrupted configuration makes it stall.
5. **User:** Understood; I checked that detail earlier.
6. **Agent:** Does the unit itself ever lose power?
7. **User:** No, it never fully turns off.
8. **Agent:** Have any cables or ports been changed recently?
9. **User:** No, the cabling is exactly as it was before.
10. **Agent:** Do all devices drop at the same time?
11. **User:** Yes. Phones, TV, and laptop all lose it together.
12. **Agent:** Have you moved it away from possible wireless interference?
13. **User:** Yes, and that made no difference.
14. **Agent:** Have you tried restarting the router?
15. **User:** Yes, I restarted it once already. It came back up but still drops.
16. **Agent:** What do the lights do when the connection drops?
17. **User:** The internet light goes orange for a bit, then back to green.
18. **Agent:** Is the issue on wireless only, or wired too?
19. **User:** Both. Even my desktop on ethernet loses connection.
20. **Agent:** What did the saved-configuration check report before this began?
21. **User:** The saved-configuration check reported corrupted data after last week's outage.
22. **Agent:** Did your provider report a service interruption?
23. **User:** Their status page shows nothing in my area.
24. **Agent:** Can another nearby customer on the same service connect normally?
25. **User:** Yes, my neighbor uses the same provider and hers is fine.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the saved configuration is corrupted, so maintenance will stall
- `aligned` — the saved configuration is intact, so maintenance will complete

### Candidate next actions

- **A.** Investigate the upstream service path before changing the device.
- **B.** Close the case and ask the user to monitor it independently.
- **C.** Escalate immediately to a hardware replacement.
- **D.** Begin the guided software maintenance procedure.
- **E.** Run the basic power recovery procedure one more time.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-65

### Public dialogue

1. **User:** Hi, my latest energy statement looks far too high.
2. **Agent:** I can look into that. Do you have the account reference?
3. **User:** Yes, it ends in four-eight-one.
4. **Agent:** Reading validation succeeds only when every meter at the property is registered on the account; an omitted meter is flagged.
5. **User:** Understood; I compared the meters with the account.
6. **Agent:** Has your household size changed this quarter?
7. **User:** No, still the same two of us.
8. **Agent:** Do you pay by fixed monthly amount?
9. **User:** Yes, a fixed amount each month.
10. **Agent:** Is the statement paper or electronic?
11. **User:** Electronic, it arrives by email.
12. **Agent:** Would you like the outcome by email as well?
13. **User:** Yes, email is fine.
14. **Agent:** Have you added any large appliance lately?
15. **User:** No, nothing new like that.
16. **Agent:** Has anyone been out to the property recently?
17. **User:** No, nobody has visited.
18. **Agent:** Would you like a breakdown by period?
19. **User:** Yes, that would be helpful.
20. **Agent:** Is the heating electric or gas?
21. **User:** It is all electric here.
22. **Agent:** Is the contact number ending in five-five-two right?
23. **User:** Yes, that is correct.
24. **Agent:** Does the account include every meter currently at the property?
25. **User:** The property has two meters, but the supplier profile lists only one of them.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — at least one property meter is missing from the account
- `aligned` — every property meter is registered on the account

### Candidate next actions

- **A.** Close the request and ask the user to watch the next statement.
- **B.** Send the figure you gave me for automated validation.
- **C.** Read back through old tariff rates before submitting.
- **D.** Refund the difference before anything is validated.
- **E.** Send an engineer out before checking the figure.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-66

### Public dialogue

1. **User:** Hi, I cannot get into my work account this morning.
2. **Agent:** I can help. Does it reject you at the first screen?
3. **User:** Yes, it will not take me past that point.
4. **Agent:** Access is restored only when the reset targets the active authentication system; resetting an unused credential store leaves the account locked.
5. **User:** Understood; I checked which credential system was targeted.
6. **Agent:** Have you tried a different browser?
7. **User:** Yes, I tried two of them.
8. **Agent:** Was the reset aimed at the credential system the company currently uses?
9. **User:** The company uses federated single sign-on, and the reset was aimed at that federated identity system.
10. **Agent:** Would a written summary afterwards be useful?
11. **User:** Yes, please send one.
12. **Agent:** Is the address you enter the work one?
13. **User:** Yes, my work address.
14. **Agent:** Do you have the authenticator application installed?
15. **User:** Yes, it is on my phone.
16. **Agent:** Is the recovery contact ending in eight-three-seven current?
17. **User:** Yes, that is still current.
18. **Agent:** Does the same thing happen on your phone?
19. **User:** Yes, exactly the same.
20. **Agent:** Did you change anything on your machine recently?
21. **User:** No, nothing that I noticed.
22. **Agent:** Are colleagues able to get in normally?
23. **User:** As far as I know, yes.
24. **Agent:** Are you connected through the office network?
25. **User:** No, I am at home today.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the reset targets a credential store the company no longer uses
- `aligned` — the reset targets the company's active authentication system

### Candidate next actions

- **A.** Close the request and ask the user to retry tomorrow.
- **B.** Have the user wipe stored browser data before anything else.
- **C.** Create an entirely new account for the user instead.
- **D.** Hand out a temporary way around the login screen.
- **E.** Start the standard credential reset for the account.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-67

### Public dialogue

1. **User:** Hi, my washing machine has stopped draining properly.
2. **Agent:** I can look at that. Do you have the model number?
3. **User:** Yes, it starts with W-D-nine.
4. **Agent:** The standard cover route authorises purchases from the covered retail channel; another purchase channel falls outside its terms.
5. **User:** Understood; I checked how the item was purchased.
6. **Agent:** Would weekday or weekend suit for a visit?
7. **User:** Weekdays are easier.
8. **Agent:** How long has it been doing this?
9. **User:** About four days now.
10. **Agent:** Is the number ending in one-seven-four still yours?
11. **User:** Yes, that is mine.
12. **Agent:** Have you cleaned the filter recently?
13. **User:** Yes, I cleared it yesterday.
14. **Agent:** Does it make any unusual noise?
15. **User:** There is a low humming sound.
16. **Agent:** Is the machine level on the floor?
17. **User:** Yes, it sits flat.
18. **Agent:** Is it plumbed into a standard waste pipe?
19. **User:** Yes, the usual arrangement.
20. **Agent:** Is there parking near the property?
21. **User:** Yes, right outside.
22. **Agent:** Would you like the outcome confirmed in writing?
23. **User:** Yes, in writing please.
24. **Agent:** Was the purchase made through the channel covered by this claim route?
25. **User:** We bought it as a standard retail item, which is the purchase channel covered by this route.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the purchase channel falls outside the submitted cover route
- `aligned` — the purchase channel is covered by the submitted route

### Candidate next actions

- **A.** Close the request and ask the user to call back.
- **B.** Open the cover claim and send it for assessment.
- **C.** Approve a whole replacement machine straight away.
- **D.** Talk the user through fixing it themselves first.
- **E.** Send an engineer before any assessment happens.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-68

### Public dialogue

1. **User:** Hi, I am trying to move my number across to your network.
2. **Agent:** I can start that. Do you have the transfer code ready?
3. **User:** Yes, I received it by text yesterday.
4. **Agent:** The number transfer completes only when its ownership record matches the required direct account holder; an intermediary record is rejected.
5. **User:** Understood; I checked the ownership record.
6. **Agent:** Is the billing address on file still correct?
7. **User:** Yes, that has not changed.
8. **Agent:** Would you like data roaming switched on?
9. **User:** Yes, that would be useful.
10. **Agent:** Is the number currently active and in use?
11. **User:** Yes, I am using it right now.
12. **Agent:** Would you like a confirmation message when it completes?
13. **User:** Yes, please send one.
14. **Agent:** Would you like a paper bill as well?
15. **User:** No, online only is fine.
16. **Agent:** Do you need international calling enabled?
17. **User:** No, I do not need that.
18. **Agent:** Does the ownership record on the transfer match the required account holder?
19. **User:** The handset came through a reseller, but the transfer was already updated to my direct subscriber record.
20. **Agent:** Have you settled the balance with the old network?
21. **User:** Yes, that was cleared last week.
22. **Agent:** Is the alternative contact ending in four-zero-three current?
23. **User:** Yes, that one still works.
24. **Agent:** Do you want to keep the same monthly bundle?
25. **User:** Yes, the same one is fine.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transfer carries an intermediary ownership record instead of the required direct record
- `aligned` — the ownership record matches the required direct account holder

### Candidate next actions

- **A.** Close the request and ask the user to start again later.
- **B.** Post out another SIM before the transfer is attempted.
- **C.** Send the transfer into the automated porting queue.
- **D.** Read the transfer code back once more before sending anything.
- **E.** Give the user a brand new number instead of moving the old one.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-69

### Public dialogue

1. **User:** Hi, the heating in my flat has not worked for three days.
2. **Agent:** I am sorry about that. Can you confirm the flat number?
3. **User:** Yes, it is flat twelve on the third floor.
4. **Agent:** The visit can be completed only when the contractor's authority matches the current managing agent's requirements; expired authority blocks access.
5. **User:** Understood; I checked the contractor's access authority.
6. **Agent:** Does the hot water still run?
7. **User:** Yes, the water is fine.
8. **Agent:** Have you checked the thermostat setting?
9. **User:** Yes, it is turned right up.
10. **Agent:** Would you like a text before anyone arrives?
11. **User:** Yes, a text would help.
12. **Agent:** Are neighbours reporting the same problem?
13. **User:** One of them mentioned it too.
14. **Agent:** Is it the whole flat or one room?
15. **User:** The whole flat is cold.
16. **Agent:** Is the number ending in nine-zero-six still right?
17. **User:** Yes, that is my number.
18. **Agent:** Is there a buzzer at the main entrance?
19. **User:** Yes, there is one.
20. **Agent:** Does the contractor hold the access authority required by the current managing agent?
21. **User:** The contractor has the current authority required by the present managing agent.
22. **Agent:** Would daytime access be possible?
23. **User:** Yes, I work from home.
24. **Agent:** Is there a boiler cupboard inside the flat?
25. **User:** Yes, in the hallway.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the contractor holds expired authority from the former agent
- `aligned` — the contractor holds current authority accepted by the managing agent

### Candidate next actions

- **A.** Approve a complete new heating system immediately.
- **B.** Post out portable heaters and leave it there.
- **C.** Move the tenant elsewhere before any visit is attempted.
- **D.** Raise the job and send it to the contractor rota.
- **E.** Close the request and ask the tenant to report it again.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-70

### Public dialogue

1. **User:** Hi, I am trying to finish enrolling for the coming term.
2. **Agent:** I can help with that. Do you have your student reference?
3. **User:** Yes, it ends in six-two-two.
4. **Agent:** Enrolment is confirmed only when transferred study has the required assessment; unassessed study is held for review.
5. **User:** Understood; I checked the assessment status.
6. **Agent:** Have you chosen all of your modules yet?
7. **User:** Yes, I picked them last week.
8. **Agent:** Have you arranged your tuition payment method?
9. **User:** Yes, that is all set up.
10. **Agent:** Are you studying full time or part time?
11. **User:** Full time this year.
12. **Agent:** Is your term address the same as last year?
13. **User:** Yes, the same place.
14. **Agent:** Do you need a timetable sent to you?
15. **User:** Yes, that would be handy.
16. **Agent:** Is the contact number ending in eight-one-nine right?
17. **User:** Yes, that is correct.
18. **Agent:** Would you like a locker on campus?
19. **User:** No, I do not need one.
20. **Agent:** Do you require any study support arrangements?
21. **User:** No, nothing like that.
22. **Agent:** Would you like reminders before the deadline?
23. **User:** Yes, reminders would help.
24. **Agent:** Have the transferred credits already received the prior-study assessment required for enrolment?
25. **User:** My overseas transfer credits have already received the required assessment.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the transferred study has not received its required assessment
- `aligned` — the transferred study has already received the required assessment

### Candidate next actions

- **A.** Put the enrolment through the automated registration run.
- **B.** Set aside the entry requirements entirely for this student.
- **C.** Go back over the chosen modules before submitting.
- **D.** Close the request and ask the student to try again.
- **E.** Push the whole thing back to a later term instead.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-71

### Public dialogue

1. **User:** Hi, there is a charge on my account that I did not make.
2. **Agent:** I can help with that. Do you see the amount and date?
3. **User:** Yes, it is forty-two dollars from last Tuesday.
4. **Agent:** The automated review accepts a dispute only when the charge's card identifier matches the current card record; otherwise it returns unmatched.
5. **User:** Understood; I checked which card identifier the charge used.
6. **Agent:** Was the disputed charge tied to the same card identifier that is currently on file?
7. **User:** My current card was reissued, but the disputed transaction carried the original card reference.
8. **Agent:** Is the mailing address on the profile still correct?
9. **User:** Yes, that address is right.
10. **Agent:** Would a paper copy of the outcome be helpful?
11. **User:** No, electronic is fine.
12. **Agent:** Do you use the mobile application to check balances?
13. **User:** Yes, almost every day.
14. **Agent:** Was the physical card in your possession that day?
15. **User:** Yes, it was in my wallet the whole time.
16. **Agent:** Have you shared the number with any recurring service?
17. **User:** Only my usual streaming subscription.
18. **Agent:** Is the contact number ending in six-one-eight still yours?
19. **User:** Yes, that number is current.
20. **Agent:** Were there other unfamiliar amounts on the same statement?
21. **User:** No, just that single one.
22. **Agent:** Did you travel outside your normal area recently?
23. **User:** No, I have been home all month.
24. **Agent:** Would you like alerts for every future transaction?
25. **User:** Yes, please turn those on.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the charge identifier differs from the current card record
- `aligned` — the charge identifier matches the current card record

### Candidate next actions

- **A.** Freeze the whole account before the charge is examined.
- **B.** Close the request and tell the user to watch the balance.
- **C.** File the disputed amount into the automated review queue.
- **D.** Send out another physical card before reviewing the charge.
- **E.** Ask the merchant for paperwork before opening anything.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-72

### Public dialogue

1. **User:** Hi, my router keeps dropping the connection every few minutes.
2. **Agent:** Sorry to hear that. How long has this been happening?
3. **User:** About a week now. I work from home, so it is disruptive.
4. **Agent:** The maintenance cycle completes only when the saved configuration is intact; a corrupted configuration makes it stall.
5. **User:** Understood; I checked that detail earlier.
6. **Agent:** Did your provider report a service interruption?
7. **User:** Their status page shows nothing in my area.
8. **Agent:** Have you tried restarting the router?
9. **User:** Yes, I restarted it once already. It came back up but still drops.
10. **Agent:** Have any cables or ports been changed recently?
11. **User:** No, the cabling is exactly as it was before.
12. **Agent:** Does the unit itself ever lose power?
13. **User:** No, it never fully turns off.
14. **Agent:** What do the lights do when the connection drops?
15. **User:** The internet light goes orange for a bit, then back to green.
16. **Agent:** Is the issue on wireless only, or wired too?
17. **User:** Both. Even my desktop on ethernet loses connection.
18. **Agent:** Do all devices drop at the same time?
19. **User:** Yes. Phones, TV, and laptop all lose it together.
20. **Agent:** Can another nearby customer on the same service connect normally?
21. **User:** Yes, my neighbor uses the same provider and hers is fine.
22. **Agent:** Have you moved it away from possible wireless interference?
23. **User:** Yes, and that made no difference.
24. **Agent:** What did the saved-configuration check report before this began?
25. **User:** The saved-configuration check reported intact data after last week's outage.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the saved configuration is corrupted, so maintenance will stall
- `aligned` — the saved configuration is intact, so maintenance will complete

### Candidate next actions

- **A.** Investigate the upstream service path before changing the device.
- **B.** Run the basic power recovery procedure one more time.
- **C.** Escalate immediately to a hardware replacement.
- **D.** Begin the guided software maintenance procedure.
- **E.** Close the case and ask the user to monitor it independently.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-73

### Public dialogue

1. **User:** Hi, I am applying for a resident parking permit.
2. **Agent:** I can take you through that. Do you have the property reference?
3. **User:** Yes, it ends in three-one-seven.
4. **Agent:** The eligibility check issues the permit only when the proof names the applicant; proof naming another occupant is refused.
5. **User:** Understood; I compared the names on the documents.
6. **Agent:** How many vehicles need covering?
7. **User:** Just the one.
8. **Agent:** Do you know the registration plate?
9. **User:** Yes, I have it written down here.
10. **Agent:** Have you held a permit in this zone before?
11. **User:** No, this is my first one.
12. **Agent:** Is the vehicle kept at the property overnight?
13. **User:** Yes, every night.
14. **Agent:** Do you need a visitor allowance as well?
15. **User:** No, just the one permit.
16. **Agent:** Would you like a receipt by email?
17. **User:** Yes, email please.
18. **Agent:** Would you like an annual or monthly permit?
19. **User:** Annual would be better.
20. **Agent:** Is the number ending in two-four-eight still current?
21. **User:** Yes, that is current.
22. **Agent:** Would you like the permit posted or collected?
23. **User:** Posted is easier for me.
24. **Agent:** Does the supporting proof name the same person who is applying for the permit?
25. **User:** The tenancy proof and the permit filing are both in my name.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the supporting proof names someone other than the applicant
- `aligned` — the supporting proof names the permit applicant

### Candidate next actions

- **A.** Close the request and ask the caller to apply again later.
- **B.** Send the whole thing straight to the appeals team.
- **C.** Hand out a temporary permit before any check is run.
- **D.** Read the plate back once more before applying.
- **E.** Send the application into the automated eligibility check.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-74

### Public dialogue

1. **User:** Hi, I am checking on my flight to Denver this afternoon.
2. **Agent:** I see the two-fifteen departure. Is that the flight you mean?
3. **User:** Yes. I want to make sure everything is on track.
4. **Agent:** A departure delay that is at least as long as the Denver connection window makes the onward flight impossible unless it is protected.
5. **User:** Understood; I have the connection time in front of me.
6. **Agent:** Is the rewards number ending in nine-nine-three yours?
7. **User:** Yes, that is mine.
8. **Agent:** Do you need directions to the departure terminal?
9. **User:** No, I know where to go.
10. **Agent:** Do you already have a seat assignment?
11. **User:** Yes, fourteen C, an aisle.
12. **Agent:** Are you checking any bags?
13. **User:** Just one checked bag.
14. **Agent:** The security wait is about twenty minutes. Are you leaving soon?
15. **User:** Yes, I am heading to the airport shortly.
16. **Agent:** Does anything else on the reservation look wrong?
17. **User:** No, everything else looks right.
18. **Agent:** Do you have dietary or accessibility needs?
19. **User:** No, nothing like that.
20. **Agent:** Is the contact phone number on the booking current?
21. **User:** Yes, it is current.
22. **Agent:** Would you like gate-change notifications by text?
23. **User:** Yes, that would help.
24. **Agent:** How much connection time is scheduled in Denver?
25. **User:** There are only ninety minutes between the flights in Denver.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the scheduled connection window is the short ninety-minute option
- `aligned` — the scheduled connection window is the long four-hour option

### Candidate next actions

- **A.** Replace the current departure even though it is still on time.
- **B.** Change the later segment immediately despite the current on-time status.
- **C.** Enable active monitoring for changes to the itinerary.
- **D.** Close the request without monitoring for changes.
- **E.** Offer disruption compensation before a disruption occurs.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-75

### Public dialogue

1. **User:** Hi, my latest energy statement looks far too high.
2. **Agent:** I can look into that. Do you have the account reference?
3. **User:** Yes, it ends in four-eight-one.
4. **Agent:** Reading validation succeeds only when every meter at the property is registered on the account; an omitted meter is flagged.
5. **User:** Understood; I compared the meters with the account.
6. **Agent:** Is the statement paper or electronic?
7. **User:** Electronic, it arrives by email.
8. **Agent:** Is the contact number ending in five-five-two right?
9. **User:** Yes, that is correct.
10. **Agent:** Does the account include every meter currently at the property?
11. **User:** The property has two meters, and the supplier profile lists both of them.
12. **Agent:** Is the heating electric or gas?
13. **User:** It is all electric here.
14. **Agent:** Has your household size changed this quarter?
15. **User:** No, still the same two of us.
16. **Agent:** Have you added any large appliance lately?
17. **User:** No, nothing new like that.
18. **Agent:** Do you pay by fixed monthly amount?
19. **User:** Yes, a fixed amount each month.
20. **Agent:** Has anyone been out to the property recently?
21. **User:** No, nobody has visited.
22. **Agent:** Would you like the outcome by email as well?
23. **User:** Yes, email is fine.
24. **Agent:** Would you like a breakdown by period?
25. **User:** Yes, that would be helpful.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — at least one property meter is missing from the account
- `aligned` — every property meter is registered on the account

### Candidate next actions

- **A.** Refund the difference before anything is validated.
- **B.** Send an engineer out before checking the figure.
- **C.** Send the figure you gave me for automated validation.
- **D.** Read back through old tariff rates before submitting.
- **E.** Close the request and ask the user to watch the next statement.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-76

### Public dialogue

1. **User:** Hi, a parcel of mine says it could not be delivered.
2. **Agent:** I can check that. Do you have the tracking reference?
3. **User:** Yes, it begins with seven-seven-four.
4. **Agent:** The delivery run succeeds only when the parcel label matches the current account address; a mismatch sends it back.
5. **User:** Understood; I compared the label with the account.
6. **Agent:** Has this happened with earlier parcels?
7. **User:** Not that I can recall.
8. **Agent:** Is the contact number ending in two-nine-five current?
9. **User:** Yes, that is the right number.
10. **Agent:** Would you like notifications by message?
11. **User:** Yes, that would be useful.
12. **Agent:** Was anybody at home during the attempt?
13. **User:** Yes, I was in all afternoon.
14. **Agent:** Would a neighbour accept the parcel for you?
15. **User:** Yes, the one next door usually would.
16. **Agent:** Is there a secure porch or side entrance?
17. **User:** There is a porch, yes.
18. **Agent:** Does the address printed on the parcel match the current account address?
19. **User:** The parcel label still shows my previous address, while the account has my current address.
20. **Agent:** Is the parcel time-sensitive at all?
21. **User:** Somewhat, I need it this week.
22. **Agent:** Did the courier leave a card of any kind?
23. **User:** No, I did not find one.
24. **Agent:** Would a collection point be acceptable instead?
25. **User:** Yes, if it is nearby.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the parcel label contains an outdated destination
- `aligned` — the parcel label matches the current destination

### Candidate next actions

- **A.** Open a loss claim before another attempt is made.
- **B.** Book the parcel onto the next available delivery run.
- **C.** Ring the depot before arranging anything else.
- **D.** Close the request and ask the user to track it themselves.
- **E.** Send out replacement goods straight away.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-77

### Public dialogue

1. **User:** Hi, I am trying to book the specialist appointment I was referred for.
2. **Agent:** I can look at that. Do you have the referral date?
3. **User:** Yes, it was issued on the ninth.
4. **Agent:** Authorization is granted only when the referral comes from the required primary-care source; another source is declined.
5. **User:** Understood; I checked who issued the referral.
6. **Agent:** Are you currently taking any regular medication?
7. **User:** Just a vitamin supplement.
8. **Agent:** Do you have a preferred practitioner at the practice?
9. **User:** No, whoever is available is fine.
10. **Agent:** Would you travel to the second site if it were sooner?
11. **User:** Yes, I could manage that.
12. **Agent:** Is the phone number ending in three-four-zero correct?
13. **User:** Yes, that one is right.
14. **Agent:** Do mornings or afternoons suit you better?
15. **User:** Mornings are easier for me.
16. **Agent:** Do you need step-free access at the building?
17. **User:** No, stairs are fine for me.
18. **Agent:** Would you like a reminder message beforehand?
19. **User:** Yes, a message would help.
20. **Agent:** Is the address on the file still where you live?
21. **User:** Yes, nothing has moved.
22. **Agent:** Have you seen this specialist before?
23. **User:** No, this would be the first visit.
24. **Agent:** Did the referral come from the source required for authorization?
25. **User:** The referral came from the walk-in centre, not my regular primary-care physician.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the referral came from a source that does not qualify
- `aligned` — the referral came from the required qualifying source

### Candidate next actions

- **A.** Send the booking through for coverage approval.
- **B.** Move straight to a self-funded booking instead.
- **C.** Ring the specialist office before requesting anything.
- **D.** Close the request and ask the user to try again later.
- **E.** Reserve the slot and settle the coverage question later.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-78

### Public dialogue

1. **User:** Hi, my latest energy statement looks far too high.
2. **Agent:** I can look into that. Do you have the account reference?
3. **User:** Yes, it ends in four-eight-one.
4. **Agent:** Reading validation succeeds only when every meter at the property is registered on the account; an omitted meter is flagged.
5. **User:** Understood; I compared the meters with the account.
6. **Agent:** Is the statement paper or electronic?
7. **User:** Electronic, it arrives by email.
8. **Agent:** Is the contact number ending in five-five-two right?
9. **User:** Yes, that is correct.
10. **Agent:** Does the account include every meter currently at the property?
11. **User:** The property has two meters, but the supplier profile lists only one of them.
12. **Agent:** Is the heating electric or gas?
13. **User:** It is all electric here.
14. **Agent:** Has your household size changed this quarter?
15. **User:** No, still the same two of us.
16. **Agent:** Have you added any large appliance lately?
17. **User:** No, nothing new like that.
18. **Agent:** Do you pay by fixed monthly amount?
19. **User:** Yes, a fixed amount each month.
20. **Agent:** Has anyone been out to the property recently?
21. **User:** No, nobody has visited.
22. **Agent:** Would you like the outcome by email as well?
23. **User:** Yes, email is fine.
24. **Agent:** Would you like a breakdown by period?
25. **User:** Yes, that would be helpful.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — at least one property meter is missing from the account
- `aligned` — every property meter is registered on the account

### Candidate next actions

- **A.** Send the figure you gave me for automated validation.
- **B.** Read back through old tariff rates before submitting.
- **C.** Send an engineer out before checking the figure.
- **D.** Close the request and ask the user to watch the next statement.
- **E.** Refund the difference before anything is validated.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-79

### Public dialogue

1. **User:** Hi, I am applying for a resident parking permit.
2. **Agent:** I can take you through that. Do you have the property reference?
3. **User:** Yes, it ends in three-one-seven.
4. **Agent:** The eligibility check issues the permit only when the proof names the applicant; proof naming another occupant is refused.
5. **User:** Understood; I compared the names on the documents.
6. **Agent:** Do you need a visitor allowance as well?
7. **User:** No, just the one permit.
8. **Agent:** Does the supporting proof name the same person who is applying for the permit?
9. **User:** The tenancy proof and the permit filing are both in my name.
10. **Agent:** Would you like an annual or monthly permit?
11. **User:** Annual would be better.
12. **Agent:** Is the vehicle kept at the property overnight?
13. **User:** Yes, every night.
14. **Agent:** Do you know the registration plate?
15. **User:** Yes, I have it written down here.
16. **Agent:** Would you like the permit posted or collected?
17. **User:** Posted is easier for me.
18. **Agent:** How many vehicles need covering?
19. **User:** Just the one.
20. **Agent:** Have you held a permit in this zone before?
21. **User:** No, this is my first one.
22. **Agent:** Would you like a receipt by email?
23. **User:** Yes, email please.
24. **Agent:** Is the number ending in two-four-eight still current?
25. **User:** Yes, that is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the supporting proof names someone other than the applicant
- `aligned` — the supporting proof names the permit applicant

### Candidate next actions

- **A.** Hand out a temporary permit before any check is run.
- **B.** Read the plate back once more before applying.
- **C.** Send the whole thing straight to the appeals team.
- **D.** Send the application into the automated eligibility check.
- **E.** Close the request and ask the caller to apply again later.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-80

### Public dialogue

1. **User:** Hi, my latest energy statement looks far too high.
2. **Agent:** I can look into that. Do you have the account reference?
3. **User:** Yes, it ends in four-eight-one.
4. **Agent:** Reading validation succeeds only when every meter at the property is registered on the account; an omitted meter is flagged.
5. **User:** Understood; I compared the meters with the account.
6. **Agent:** Has your household size changed this quarter?
7. **User:** No, still the same two of us.
8. **Agent:** Do you pay by fixed monthly amount?
9. **User:** Yes, a fixed amount each month.
10. **Agent:** Is the statement paper or electronic?
11. **User:** Electronic, it arrives by email.
12. **Agent:** Would you like the outcome by email as well?
13. **User:** Yes, email is fine.
14. **Agent:** Have you added any large appliance lately?
15. **User:** No, nothing new like that.
16. **Agent:** Has anyone been out to the property recently?
17. **User:** No, nobody has visited.
18. **Agent:** Would you like a breakdown by period?
19. **User:** Yes, that would be helpful.
20. **Agent:** Is the heating electric or gas?
21. **User:** It is all electric here.
22. **Agent:** Is the contact number ending in five-five-two right?
23. **User:** Yes, that is correct.
24. **Agent:** Does the account include every meter currently at the property?
25. **User:** The property has two meters, and the supplier profile lists both of them.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — at least one property meter is missing from the account
- `aligned` — every property meter is registered on the account

### Candidate next actions

- **A.** Read back through old tariff rates before submitting.
- **B.** Send the figure you gave me for automated validation.
- **C.** Close the request and ask the user to watch the next statement.
- **D.** Send an engineer out before checking the figure.
- **E.** Refund the difference before anything is validated.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-81

### Public dialogue

1. **User:** Hi, I need to report some damage to my car from this morning.
2. **Agent:** I am sorry to hear that. Was anybody injured?
3. **User:** No, thankfully everyone is fine.
4. **Agent:** The assessment settles only when the registered keeper matches the policy name; a mismatch is held for proof.
5. **User:** Understood; I compared the keeper and policy names.
6. **Agent:** Where did the incident take place?
7. **User:** In a supermarket car park.
8. **Agent:** Would you like updates by message?
9. **User:** Yes, messages are fine.
10. **Agent:** Is the number ending in seven-six-five still yours?
11. **User:** Yes, that is right.
12. **Agent:** Do you have a preferred repair garage?
13. **User:** No, whichever one you recommend.
14. **Agent:** Have you reported it to the authorities?
15. **User:** Yes, I did that this morning.
16. **Agent:** Did anybody witness what happened?
17. **User:** One person nearby saw it.
18. **Agent:** Does the registered keeper match the person named on the policy?
19. **User:** The vehicle registration and the insurance cover are both in my name.
20. **Agent:** Was another driver involved?
21. **User:** Yes, but they left before I could speak to them.
22. **Agent:** Would you need a courtesy car meanwhile?
23. **User:** Yes, that would help a lot.
24. **Agent:** Is the car still driveable?
25. **User:** Yes, it drives, but the wing is dented.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the registered keeper and policyholder names differ
- `aligned` — the registered keeper matches the policyholder name

### Candidate next actions

- **A.** Close the report and ask the caller to get in touch later.
- **B.** Approve the garage work before the report is lodged.
- **C.** Write the car off before anything has been assessed.
- **D.** Lodge the report into the automated assessment run.
- **E.** Chase the bystander for a statement before lodging anything.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-82

### Public dialogue

1. **User:** Hi, the heating in my flat has not worked for three days.
2. **Agent:** I am sorry about that. Can you confirm the flat number?
3. **User:** Yes, it is flat twelve on the third floor.
4. **Agent:** The visit can be completed only when the contractor's authority matches the current managing agent's requirements; expired authority blocks access.
5. **User:** Understood; I checked the contractor's access authority.
6. **Agent:** Does the contractor hold the access authority required by the current managing agent?
7. **User:** The contractor has the current authority required by the present managing agent.
8. **Agent:** Is there a buzzer at the main entrance?
9. **User:** Yes, there is one.
10. **Agent:** Have you checked the thermostat setting?
11. **User:** Yes, it is turned right up.
12. **Agent:** Is there a boiler cupboard inside the flat?
13. **User:** Yes, in the hallway.
14. **Agent:** Would you like a text before anyone arrives?
15. **User:** Yes, a text would help.
16. **Agent:** Would daytime access be possible?
17. **User:** Yes, I work from home.
18. **Agent:** Is the number ending in nine-zero-six still right?
19. **User:** Yes, that is my number.
20. **Agent:** Is it the whole flat or one room?
21. **User:** The whole flat is cold.
22. **Agent:** Does the hot water still run?
23. **User:** Yes, the water is fine.
24. **Agent:** Are neighbours reporting the same problem?
25. **User:** One of them mentioned it too.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the contractor holds expired authority from the former agent
- `aligned` — the contractor holds current authority accepted by the managing agent

### Candidate next actions

- **A.** Post out portable heaters and leave it there.
- **B.** Approve a complete new heating system immediately.
- **C.** Move the tenant elsewhere before any visit is attempted.
- **D.** Close the request and ask the tenant to report it again.
- **E.** Raise the job and send it to the contractor rota.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-83

### Public dialogue

1. **User:** Hi, my router keeps dropping the connection every few minutes.
2. **Agent:** Sorry to hear that. How long has this been happening?
3. **User:** About a week now. I work from home, so it is disruptive.
4. **Agent:** The maintenance cycle completes only when the saved configuration is intact; a corrupted configuration makes it stall.
5. **User:** Understood; I checked that detail earlier.
6. **Agent:** What did the saved-configuration check report before this began?
7. **User:** The saved-configuration check reported intact data after last week's outage.
8. **Agent:** Have you tried restarting the router?
9. **User:** Yes, I restarted it once already. It came back up but still drops.
10. **Agent:** Does the unit itself ever lose power?
11. **User:** No, it never fully turns off.
12. **Agent:** Have any cables or ports been changed recently?
13. **User:** No, the cabling is exactly as it was before.
14. **Agent:** Did your provider report a service interruption?
15. **User:** Their status page shows nothing in my area.
16. **Agent:** Can another nearby customer on the same service connect normally?
17. **User:** Yes, my neighbor uses the same provider and hers is fine.
18. **Agent:** Is the issue on wireless only, or wired too?
19. **User:** Both. Even my desktop on ethernet loses connection.
20. **Agent:** Do all devices drop at the same time?
21. **User:** Yes. Phones, TV, and laptop all lose it together.
22. **Agent:** Have you moved it away from possible wireless interference?
23. **User:** Yes, and that made no difference.
24. **Agent:** What do the lights do when the connection drops?
25. **User:** The internet light goes orange for a bit, then back to green.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the saved configuration is corrupted, so maintenance will stall
- `aligned` — the saved configuration is intact, so maintenance will complete

### Candidate next actions

- **A.** Begin the guided software maintenance procedure.
- **B.** Close the case and ask the user to monitor it independently.
- **C.** Run the basic power recovery procedure one more time.
- **D.** Escalate immediately to a hardware replacement.
- **E.** Investigate the upstream service path before changing the device.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---

## Item ANNOTATOR_01-84

### Public dialogue

1. **User:** Hi, I am checking on my flight to Denver this afternoon.
2. **Agent:** I see the two-fifteen departure. Is that the flight you mean?
3. **User:** Yes. I want to make sure everything is on track.
4. **Agent:** A departure delay that is at least as long as the Denver connection window makes the onward flight impossible unless it is protected.
5. **User:** Understood; I have the connection time in front of me.
6. **Agent:** Does anything else on the reservation look wrong?
7. **User:** No, everything else looks right.
8. **Agent:** How much connection time is scheduled in Denver?
9. **User:** There are only ninety minutes between the flights in Denver.
10. **Agent:** Would you like gate-change notifications by text?
11. **User:** Yes, that would help.
12. **Agent:** Do you need directions to the departure terminal?
13. **User:** No, I know where to go.
14. **Agent:** Are you checking any bags?
15. **User:** Just one checked bag.
16. **Agent:** Is the rewards number ending in nine-nine-three yours?
17. **User:** Yes, that is mine.
18. **Agent:** The security wait is about twenty minutes. Are you leaving soon?
19. **User:** Yes, I am heading to the airport shortly.
20. **Agent:** Do you already have a seat assignment?
21. **User:** Yes, fourteen C, an aisle.
22. **Agent:** Do you have dietary or accessibility needs?
23. **User:** No, nothing like that.
24. **Agent:** Is the contact phone number on the booking current?
25. **User:** Yes, it is current.

### Does the clue match the success rule? (`causal_alignment`)

- `misaligned` — the scheduled connection window is the short ninety-minute option
- `aligned` — the scheduled connection window is the long four-hour option

### Candidate next actions

- **A.** Enable active monitoring for changes to the itinerary.
- **B.** Close the request without monitoring for changes.
- **C.** Replace the current departure even though it is still on time.
- **D.** Offer disruption compensation before a disruption occurs.
- **E.** Change the later segment immediately despite the current on-time status.

Record the action label, rule-match label, answerability,
ambiguity, and supporting dialogue turn in the phase-1 CSV.

---
