# Amendments 7–14 and S-1 to S-6 — adjudication of the independent review

**Inputs.**
- Prompt `verification/amendments7-14_review_prompt.md` (49d9d0f8…) and package `verification/amendments7-14_review_package.md` (33128746…), committed at dcc6764 before sending.
- Sent 2026-11-08 by the author through Claude in Chrome, at JAE's request, as the only message of a fresh claude.ai incognito chat. No project was attached, and the four connectors (ClickUp, Google Docs, Google Drive, Claude in Chrome) were switched off for the chat with JAE's approval and switched back on afterwards. The text sent was fetched from the public commit and SHA-256-verified (1adb3415…) before sending.
- Reply saved verbatim: `verification/amendments7-14_review_transcript.md`, 37,498 characters, SHA-256 of the raw message text bd51f8c6…f36b43 (matched).
- Single round under the entry-3 rule; no third round.

**Decision rule (DECISIONS entry 34, fixed before sending):** "pipeline-invalid, or any of S-1 to S-6 a rescue → hold E2, and use §K's single re-set; method property → amend 14.3 to the pipeline reading (instrument check on B2/B4) and report D_div's flat lead response beside E2 as a limitation."

**Status: RATIFIED by JAE 2026-11-08, with changes (DECISIONS entry 35):**
1. §K's grading-day record still happens on 2026-11-20: "E2 unrun — suite gate not met (S-3 RESCUE)", in DECISIONS and RECORD, citing 15.16.
2. The AI2 route-3 cutoff stays 2026-11-13. The re-set moves when E2 runs, not which data it uses.
3. Amendment 15 states how F1 is discharged: the frozen joint-weakness null is declared unattainable (S-3 evidence), the pulse sweep is reported as a characterization, and the RESCUE is disclosed in Methods. The 2026-12-04 gate therefore has a defined pass condition.
4. 2026-12-04 is final (a miss → CLOSE). The E2 gate is scheduled to reach ALL PASS by 2026-12-01.

Also recorded (JAE): the S-3 pulse / false-SUPPORT construction was recommended by JAE's other session.

## Verdicts and the decision rule

| Finding | Review verdict | Proposed adjudication |
|---|---|---|
| S-1 | CORRECTION | Accept |
| S-2 | CORRECTION | Accept |
| **S-3** | **RESCUE** | **Accept (CONFIRMED).** Grader rows: all 25 pulse-sweep cells read SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000, so the replacement cannot fail by construction, and the frozen joint-weakness condition (F1) is not measured. |
| S-4 | CORRECTION | Accept |
| S-5 | no verdict | Accept the correction to its "Reading" (R4) |
| S-6 | METHOD PROPERTY | Accept |
| S-6 treatment | CORRECTION, conditional on 15.7 and 15.8 | Accept, with the conditions |

**Applying the rule:** S-3 is confirmed as a RESCUE, so **E2 is held and §K's single re-set is used.** The re-set follows R17 (15.16): the new day is 2026-12-04, and the reason recorded is "suite gate not met", never "data availability". The S-6 branch (method property) is applied as well, through 15.7 and 15.8.

## Findings R1–R27

| ID | Sev. | Proposed | Action |
|---|---|---|---|
| R1 | MINOR | CONFIRMED | Adopt 15.1: declare 7.1–7.3, 7.5, 9.1 and 9.2 as specifications under §K's "no re-tuning" clause, and permit no further real-data construction change before E2. |
| R2 | MAJOR | CONFIRMED | Adopt 15.2: a suite gate may hold E2 only for a pipeline fault. D_div's weakness is reported, never a hold. |
| R3 | MAJOR | CONFIRMED | Adopt 15.3: state the null and effect rates of the E2 label beside it; REFUTE is described as "mean lead did not exceed the best baseline's". |
| R4 | MAJOR | CONFIRMED | Adopt 15.4: a reported positive control (sustained shift plus measurement noise, where smoothing should win), fixed before any g is read. |
| R5 | MAJOR | CONFIRMED | Adopt 15.5: define φ̂_y on A1 and the cell-selection rule now, and pre-commit the extension cells. |
| R6 | MAJOR | CONFIRMED | Folded into 15.15 (lookup withdrawn). |
| R7 | MAJOR | CONFIRMED | Adopt 15.6: every severity figure beside E2 comes from the A1-structure cells (13.3 / 15.4). |
| R8 | BLOCKER | CONFIRMED | Adopt 15.7: B1–B4 instrument check; at least one baseline must qualify at every pair; the grader prints every detector's row at every pair; graded on fresh seeds disjoint from cells 260–289. D_div's (25, 75) rows are labelled "inside the A1.5 scope condition" (R16). |
| R9 | MINOR | **Partly WITHDRAWN** | The suite's resample stream mirrors E2 on A1 exactly (a fresh `default_rng(20261030)` per run, stated in run_suite.py). The suite validates the procedure as it will run, and a per-replicate stream would validate a different procedure. CONFIRMED in part: E1, E2 and E5 get distinct streams, SeedSequence(20261030, spawn_key=(k,)) with k = 1, 2, 3. |
| R10 | MINOR | CONFIRMED | Adopt 15.10: append items 19a–19f verbatim to DESIGN, with the run commits. |
| R11 | MAJOR | CONFIRMED | Adopt 15.11: "detection probability at the observed effect" = the nearest pre-committed cell by mean C_min within ±25 %; otherwise state that none exists. |
| R12 | MAJOR | CONFIRMED | Adopt 15.12: record 12.2 as a relaxation. Entry 13: the A1 loss enumeration ran after `test_a1_events.py` passed 20/20 at 81481b6, and before any D.5 cell existed. |
| R13 | MINOR | CONFIRMED | Adopt 15.13. |
| R14 | MINOR | CONFIRMED | Adopt 15.14. The record (entries 19–20) shows that the reference's original author (a separate agent, given DESIGN.md only) changed the reference from the amended text alone; this is stated in the amendment. |
| R15 | MAJOR | CONFIRMED | Adopt 15.15: the pulse-sweep cells become a characterization; 10.2's "Use in E2" is withdrawn. |
| R16 | MAJOR | CONFIRMED | Covered by 15.7. |
| R17 | MAJOR | CONFIRMED | Adopt 15.16: re-set to 2026-12-04, labelled "suite gate not met". |
| R18 | MAJOR | CONFIRMED | Adopt 15.17: measure the between-detector chance-lead difference from the planted-null cells. |
| R19 | MINOR | CONFIRMED | Adopt 15.18: the §K entry is marked "verification pending (Phase 3 broken fixture)". |
| R20 | MINOR | CONFIRMED | Adopt 15.19: committed seed map with first-assignment commits. |
| R21 | MINOR | CONFIRMED | Adopt 15.20. True as stated: the only operations on files containing g have been byte hashes (the D.1 masks, the cell-equality checks and the PRV self-test's copy of run-025). |
| R22 | MAJOR | Accept the verdict | Adopt 15.8, and run checks (b) θ-fixed spread and (c) lead against history length on synthetic cells before E2. |
| R23–R24, R26 | MINOR | Accept | — |
| R25 | MAJOR | **CONFIRMED** | S-3 is a RESCUE (see above). |
| R27 | MAJOR | Accept | Conditions 15.7 and 15.8 as above. |

## Consequence (if ratified)

- **Amendment 15** adopts 15.1–15.20 as adjudicated above.
- **Built and run before E2 touches any g:**
  - the 15.7 instrument check (fresh seeds);
  - the 15.4 positive control;
  - the 15.17 measurement;
  - the 15.8 checks (b) and (c);
  - the seed map;
  - the 15.5 extension cells.
- **Grading day:** re-set once to 2026-12-04, reason "suite gate not met" (15.16).
- §K's thresholds, windows, spike definition and FA grid are untouched.
