# Amendment 1 — scoped independent check: adjudication

Dated 2026-10-30. Single round (DECISIONS entry 2 Addendum B; entry 6).

- **Prompt:** verification/amendment1_review_prompt.md (MD5 832fbc0407af8a4ed4e2476ebdd54920).
- **Package:** verification/amendment1_review_package.md (MD5 e152bb703c253fb9dd0f4cf5cbd91506). It contains draft v2 of the amendment, drafts/DESIGN_Amendment_1_DRAFT.md (MD5 ffd2b3008f80e40d5cf5302ee3860dd8), committed at ced1674.
- **Reviewer reply, verbatim:** verification/amendment1_review_transcript.md (MD5 619a6766b38e2bd9cbfb795f13026d89; 18,246 bytes; byte-identical to the reply JAE attached).
- **Reviewer:** a fresh claude.ai incognito chat with web search off; the prompt and package were the only message.

**Result:** 16 findings: 1 BLOCKER, 7 MAJOR, 8 MINOR.
- Adopted as proposed: 11.
- Adopted with an adaptation (the reason is given for each): G1, G2, G4, G6, G15.
- Rebutted: none.
- One further item was found by the author during adjudication: S1.

No finding needed an A1 metric value. Every blank the reviewer left ("___") is either an upper bound from metadata already read (step index only) or a quantity that the structural report computes from the step index and null masks before any metric value is read (Amendment 1, A1.12).

## Findings

| # | Sev. | Verdict | Adjudication | Lands in |
|---|---|---|---|---|
| G1 | MAJOR | ADOPT, adapted | **Guard adopted:** if n* = 0 at headline FA on A1, E2 is unrun for data availability, never REFUTE. FA grid points with n* < 2 are reported as "not matchable" and enter no contrast. **Adaptation:** the reviewer's blank "A1 has N = ___" cannot be filled from a row count; the only A1 file read is the incomplete route-1 copy of run-025 (D-02). What metadata does give is an upper bound: the last step is 543,360, so N ≤ 54,337 grid observations, and before exclusions n* ≤ 3, 5, 11 and 27 at FA 0.5, 1, 2 and 5. That bound is stated now. The realised N is set by the A1.12 structural report. N_out and n* depend on the loss events and are reported with E2. Stated consequence: headline matching on A1 is coarse (n* ≈ 5). | A1.2, A1.12 |
| G2 | MAJOR | ADOPT, adapted | Cost declared: the per-gap eligibility warm-up is 11,280 steps (1,000 + 128 grid observations) against 1,128 frozen. Counts of events made ineligible by minimum history are reported separately from dedup merges and from rewind ineligibility. **Adaptation:** the number of stretches longer than 11,280 steps needs the full segment list. It goes in the A1.12 structural report, not in a blank now. | A1.4, A1.12 |
| G3 | BLOCKER | ADOPT | t_e^g = 10·⌊t_e/10⌋. The scan window is 129 grid observations [t_e^g − 1,280, t_e^g]. Lead = t_e^g − t_j*. An alarm first at t_e^g gives lead 0; a miss gives 0; censored gives 1,280. t_e in steps stays the event time for dedup, the k ladder and reporting. The draft's "the w_s grid observations" (128) is corrected to 129, matching the frozen closed interval [t_e − 128, t_e]. | A1.4 |
| G4 | MAJOR | ADOPT, adapted | **Detector side as proposed:** only a gap containing a grid step resets detector state and the minimum history. **Adaptation 1:** D.1's completeness check already fails any segment with a missing step inside it, so a missing non-grid step can only lie in a gap between segments (a gap of 1–9 non-grid steps). The amendment says so. **Adaptation 2 (loss side):** the loss side keeps the frozen D.2 rule (the spike baseline restarts at every gap), not the reviewer's "treat L as non-finite". The loss side is per step as frozen, and the reviewer's version would change it. | A1.1 |
| G5 | MAJOR | ADOPT | A rewind event's history is counted from the last gap on the series P-SEG assigns it. A segment boundary that is not a gap resets nothing. This matches D.1 P-SEG: the earlier segment's series "shares history with the kept trajectory up to the checkpoint step". The draft's "that segment's first observation" was wrong. | A1.4 |
| G6 | MINOR | ADOPT, adapted | Dropped means null, non-positive or non-finite g on a grid step. A dropped first post-gap observation starts the series and the count at the first non-dropped one. **Adaptation:** the longest dropped run on A1 needs the full null mask, so it goes in the A1.12 report. Route 1's run-025 copy is incomplete (D-02) and is not used for it. | A1.1, A1.12 |
| G7 | MINOR | ADOPT | round(·) is round-half-up, implemented as ⌊x + 0.5⌋. Python's built-in round rounds half to even, so it is not used. This applies to every run as a clarification (A1.11). | A1.2, A1.11 |
| G8 | MINOR | ADOPT | In A1.6 the gradient norm is subsampled to step mod 10 = 0; the loss is kept per step. | A1.6 |
| G9 | MINOR | ADOPT | The scan window is 129 grid observations for every detector and every E4 pair. The draft's rationale "scan window equals w_s" is replaced: the frozen window is fixed and does not track w_s. | A1.2 (E4), A1.4 |
| G10 | MAJOR | ADOPT | A1.10 gives verbatim replacements for A1 in D.3 E2 and §K. It also covers D.0a, D.2 (the scan-window and eligibility sentences) and D.7's frozen line, which carry the same step constants. | A1.10 |
| G11 | MAJOR | ADOPT | The scope condition is a Methods/THESIS statement. It does not qualify E2 or §K: a REFUTE on A1 STOPs the project whatever the precursor lengths turn out to be. | A1.5, THESIS A4(c) |
| G12 | MINOR | ADOPT | Declared: the rung is resolved on A1 under the 2,000-step dedup and transported to per-step runs at 200. A2–A6 also report their eligible-event count at the other rung. | A1.3 |
| G13 | MINOR | ADOPT | On A1, B3's α and warm-up per grid observation are a construction choice under P-B3, labelled so in the Methods. | A1.2 |
| G14 | MINOR | ADOPT | E1's approximate-stationarity scope on A1 is restated over 2,560-step horizons. The drift in y over that horizon is reported beside ρ (computed after the push, with E1). | A1.5 |
| G15 | MAJOR | ADOPT, adapted | The suite cell plants all ten residues of t_e mod 10, a small-N_out probe (4,000 and 12,000 grid observations; the n* = 0 guard must fire at 4,000), and series ≥ 33,840 steps with ≥ 2 gaps. D.5's pass criteria are restated verbatim. **Adaptation:** the reviewer's probe "remove a single non-grid step" is split in two, because D.1 rejects a segment with a missing step: (i) a missing non-grid step inside a segment must make that segment fail D.1 completeness; (ii) a gap of 1–9 non-grid steps between segments must leave detector state and eligibility unchanged and restart the loss baseline. | A1.7 |
| G16 | MINOR | ADOPT | "All events" in the FA exclusion means every event at the rung that resolved on A1 (P-KLAD). This applies to every run as a clarification (A1.11). | A1.4, A1.11 |

## Found during adjudication (author)

- **S1 (MAJOR, D.1).** D.1's completeness check says "if A1 cannot be assembled to full per-step resolution … A1 is recorded as unavailable". Read literally, A1's native 10-step gradient norm fails that sentence. The amendment changed operators but did not restate the data check. Fix: for A1, the completeness check applies to the step index unchanged (every step present, loss every step). `optim/total_grad_norm` must be present by name and is required on grid steps only. Lands in A1.1 and A1.10.

## Review closure

Single round, as fixed in DECISIONS entry 2 Addendum B. No second round. Every finding is adopted, so no rebuttal is left for a reviewer to answer.

The adaptations to G1, G2, G4, G6 and G15 are narrower than or equal to the reviewer's proposals, for these reasons:
- G1, G2, G6: the blanks move to a pre-metric structural report.
- G4: the loss side stays as frozen.
- G15: the probe is made consistent with D.1.

None of these loosens a rule. REVIEW CLOSED 2026-10-30.
