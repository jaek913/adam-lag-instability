# Independent check: DESIGN Amendments 7–14 and suite findings S-1 to S-6

Single round, final. I judged only the written package. Any statement about mechanism that the package does not show is marked as an inference.

---

## Pass 1: Permissibility

**Summary.** No amendment in 7–14 changes any of the four items the header protects (§K's thresholds, windows, spike definition or FA grid).
- Amendments 8, 10, 11, 12.1, 13 and 14.3 touch only suite construction and suite criteria.
- Amendments 7.1–7.3, 7.5, 9.1 and 9.2 change rules that apply to real data, but none of those four items.
- No gradient-norm value had been read. The only A1 facts available were the layout and the 57/61 event counts. Neither indicates which E2 outcome a construction choice would favour.

The exceptions are §K's own wider clause (R1) and an outcome-routing effect created by 14.3 together with the S-6 decision rule (R2).

**R1**
- **Pass:** 1. **Severity:** MINOR.
- **Location:** §K last sentence; 7.1–7.3, 7.5, 9.1, 9.2.
- **Evidence:** §K says "No re-tuning of windows, spike definition, baselines, construction pins, or FA grid after A1 is touched". The amendment, by contrast, says 7.1 "c(v) … evaluated on the path recomputed at that candidate"; 9.1 says "The words 'or after a reset' are struck."
- **Why it matters.** §K's own clause is broader than the header rule. Several amendments change real-data behaviour of a baseline (B4 after reset), of P-FA (the B4 candidate set, N_out) and of P-HOLD (undefined s(j−1)), all after A1 was touched (the loss was read before Amendment 7).
  - None of this is re-tuning. Each item fills a point the frozen text left unspecified, or restores the behaviour of a named tool's source, and was made blind to g.
  - However, no amendment states that it was checked against §K's wider clause. A reader of the null note will ask.
- **Proposed fix:** "15.1 §K re-tuning clause. Amendments 7.1–7.3, 7.5, 9.1 and 9.2 change real-data construction details after A1's loss was read and before any gradient-norm value entered any computation. Each specifies a point the frozen text left open (7.1–7.3, 7.5) or restores the pinned source behaviour of a tool-defined baseline (9.1, 9.2). None was chosen with any detector score, threshold or lead in hand. They are declared here as specifications under §K's 'no re-tuning' clause, not re-tunings. No further real-data construction change of any kind is permitted before E2's single run."

**R2**
- **Pass:** 1. **Severity:** MAJOR.
- **Location:** 14.3 no-vacuous clause; the S-6 decision rule; §K re-set.
- **Evidence:** 14.3: "the cell fails unless D_div and at least one baseline meet the ≥ 80 % detection condition". S-6: "pipeline-invalid or rescue → hold E2 and use §K's single re-set".
- **Why it matters.**
  - Amendment 14 (2026-11-07) was written after suite run v1 (2026-11-06). The author therefore already had S-5, which shows D_div's synthetic leads are weak and that E2 returns REFUTE in about 85–90 % of high-φ cells.
  - I accept the owner's statement that the clause was meant to prevent a vacuous pass. Its effect, however, is that **the method under test failing to perform** can fail a pipeline gate. Under the decision rule that holds E2, and §K's re-set path then ends in CLOSE.
  - That route replaces the pre-registered STOP-with-null-note with a CLOSE that carries no verdict on Claim A. It is the one outcome-relevant asymmetry in Amendments 7–14. The issue is the effect, not the intent.
- **Proposed fix:** "15.2 Gate scope. A suite gate may hold E2 only for a pipeline fault: disagreement with the reference implementation, a failed hand probe, or a criterion that the reference implementation also fails on a detector-agnostic quantity. A synthetic result showing that D_div responds weakly, or later than the baselines, is a property of the method under test. It is reported beside E2 and never holds E2."

---

## Pass 2: Can every rule still return each of its outcomes?

**Outcome by outcome:**
- **INSUFFICIENT EVENTS** can no longer occur on A1: 57 ≥ 5 eligible events at k = 4. That was settled legitimately by P-KLAD.
- **§K CLOSE** is now reachable only through an unrun E2 (R17).
- **SUPPORT, INCONCLUSIVE and REFUTE** are all reachable in principle. Their rates are very unequal and barely depend on whether a precursor exists. R3 and R4 give the details.

**R3**
- **Pass:** 2. **Severity:** MAJOR.
- **Location:** D.3 E2 outcome partition and §K, read against S-5 and Part 4.
- **Evidence:** a1s_null SUPPORT/INCONCLUSIVE/REFUTE is 0.000/0.130/0.870 at φ 0.9; a1s_effect is 0.000/0.155/0.845. Across all cells, null REFUTE is 0.79–0.99.
- **Why it matters.** On the A1 layout at φ ≥ 0.8, REFUTE occurs at about the same rate whether or not a 1,000-step precursor is planted. The likelihood ratio is roughly 0.9–1.0.
  - **Structural cause.** REFUTE is "C_min ≤ 0", which includes the point mass at C_min = 0. Under no signal, 46–58 % of replicates have every lead equal to 0 (S-2). C_min is also a minimum over four baselines, so a chance lead by *any* baseline drives it down, while D_div must beat all four.
  - **Rough size of the chance floor** (an estimate, not a measurement). At A1's headline n* ≈ 4 over roughly 36,000 out-of-window grid observations, each detector has about a 1.8 % chance per event of an alarm in the roughly 160 observations that produce an in-window lead. Each such chance lead is worth about 700 steps on average. That adds roughly 10–15 steps to every detector's mean lead, and C_min sees the largest of the four baseline floors.
  - **What a REFUTE on A1 would establish:** at headline FA, D_div's mean lead over 57 events did not exceed the best baseline's. Under the suite's constructions, D_div shows no detectable lead advantage.
  - **What it would not establish:** that no gradient-norm precursor exists, or that smoothing has no value. REFUTE is the modal outcome under the null and under linear-ramp precursors alike, and no cell measures how often REFUTE occurs in a world where D_div truly leads (R4).
  - **PROCEED.** Under the null, PROCEED (via INCONCLUSIVE) occurs at about 0.10–0.20. It is therefore not evidence for D_div either.
- **Proposed fix:** "15.3 Reading of E2. Beside any E2 label, the result states the suite's rates of that label under (i) the planted null and (ii) the planted effect, both on the A1-structure layout (13.3) at the φ_y cell selected under 15.5. A REFUTE is described as 'D_div's mean lead did not exceed the best baseline's at matched FA'. It is not described as evidence against the existence of precursors. The null note reports that REFUTE is the null's modal outcome (0.87–0.91 on the A1 layout)."

**R4**
- **Pass:** 2. **Severity:** MAJOR.
- **Location:** D.5 planted effect as amended by 8.1; S-5.
- **Evidence:** SUPPORT reaches ≥ 0.10 only at φ = 0.5. a1s_effect gives 0.255 at φ 0.5, then 0.015, 0.000, 0.000, 0.000. Every grid10_effect cell is ≤ 0.07.
- **Why it matters.**
  - **No cell shows that SUPPORT is reachable where Claim A's mechanism should work.** No suite cell plants a world in which D_div's population mean lead clearly exceeds every baseline's. In most effect cells, B2 or B4 leads D_div, so REFUTE is the *correct* answer there, and S-5's "little power to return SUPPORT" partly misreads its own table.
  - **Positive control lost.** 8.1 made the planted effect "reported, not required", so nothing in the suite certifies that SUPPORT can be reached.
  - **At A1's realised regime.** A1's regime is unknown, because no gradient-norm value has been read. If A1's grid-10 φ̂_y ≥ 0.8, the suite's best estimate of P(SUPPORT) under any planted world is about 0–2 %. SUPPORT is plausible only near φ̂_y ≈ 0.5, and even there at about 25 %.
- **Proposed fix:** "15.4 Positive control (reported, no criterion). Fixed and committed before any gradient-norm value is read, on fresh disjoint seeds, on the A1-structure layout across the φ_y grid at 57 events: a precursor for which smoothing is designed to win. This is a sustained mean shift of δ × stationary SD over the final 1,000 steps before t_e, with white measurement noise of SD σ_m added to y. δ and σ_m are chosen on calibration seeds as the smallest values at which D_div's population mean lead exceeds every baseline's by ≥ 100 steps. Reported: SUPPORT/INCONCLUSIVE/REFUTE rates. If no (δ, σ_m) on the grid {0.5, 1, 2} × {1, 2, 4} achieves this, that is reported as 'no construction found in which D_div leads', and it is cited beside E2."

---

## Pass 3: Places where two analysts could compute different numbers

**R5**
- **Pass:** 3. **Severity:** MAJOR.
- **Location:** D.5 regime span; 10.2 "Use in E2"; 11.1; 13.3.
- **Evidence:** D.5: "the run reports which cell the realised A1 data lands in. If A1's realised φ̂_y falls outside [0.5, 0.98] …".
- **Why it matters.**
  - **The estimator is undefined.** No text defines φ̂_y for A1. Open choices include: lag-1 ACF of y on the grid or by step; raw or detrended (y drifts, D.2 E1 scope); pooled across blocks or per block; whether pairs may cross gaps; whether dropped observations are carried forward.
  - **Several rules depend on it.** It selects the cell for 10.2's lookup, for 11.1/13.3's power figures and for R3's reporting. It also triggers a grid extension, made by amendment *after g is read*, "before any INCONCLUSIVE is interpreted".
  - **Two kinds of discretion.** The estimator and the "nearest cell" rule are each a choice made after seeing the data.
- **Proposed fix:** "15.5 φ̂_y on A1. φ̂_y = lag-1 sample autocorrelation of y on A1's kept grid series. It uses all pairs of consecutive grid observations within a detector-series block (no pair crosses a gap), includes carried-forward observations, takes no detrending, and pools the blocks. It is computed in E2's single run. Cell selection: the φ_y grid value nearest φ̂_y on the linear scale, with ties going to the larger value. If φ̂_y lies outside [0.5, 0.98], the nearest edge cell is used and the extension cells {0.3, 0.99} are pre-committed now and run in the same session as E2, with no further amendment."

**R6**
- **Pass:** 3. **Severity:** MAJOR.
- **Location:** 10.2 "Use in E2".
- **Evidence:** "The false-SUPPORT rate is read at the calibrated h nearest the realised rate, per detector."
- **Why it matters.**
  - **The rule does not yield one number.** There are five calibrated heights h_{φ,d}, each tuned to one detector's rate. A1 produces five realised rates. "Per detector" gives up to five false-SUPPORT rates, and the rule does not say which one the D.3 E2 report states, or what "nearest" means across detectors.
  - **Its content is empty anyway** (R15): every one of those 25 cells reads 0.000.
- **Proposed fix:** fold into R15's fix (withdraw the lookup).

**R7**
- **Pass:** 3. **Severity:** MAJOR.
- **Location:** 11.1, 13.3, 12.2.
- **Evidence:** 11.1: "Its outcome rates are the detection probability … that E2 reports beside an INCONCLUSIVE". 13.3: "planted effect, L = 1,000 steps, A = 2: reported."
- **Why it matters.**
  - **Two candidate cells.** Two cell families both claim to represent "57 events": per-step realised_count_effect (11.1) and the A1-structure a1s_effect (13.3).
  - **They disagree.** At φ 0.5, SUPPORT is 0.150 in one and 0.255 in the other. Choosing between them after seeing E2 is a judgment.
- **Proposed fix:** "15.6 Severity cells for A1. Every severity or power figure reported beside E2 is taken from the A1-structure cells (13.3, and 15.4 when run) at the cell selected under 15.5. The per-step 57-event cells (11.1) are reported in the supplement only."

**R8**
- **Pass:** 3. **Severity:** BLOCKER.
- **Location:** S-6 decision rule, "apply the bar to B2/B4 as the instrument check"; Part 4 dyn-range rows.
- **Evidence:** Grader rows such as "(25,75): VACUOUS … (eligible: ['B2'])". For grid-10 φ 0.95 and 0.98 at (75,125), the grader prints only "VACUOUS", with no separation result for B2 or B4.
- **Why it matters.**
  - **No criterion exists.** The method-property route needs an instrument-check criterion, and no amendment states one. Open questions: B2 alone or B2 and B4? Both pairs? Is a group in which B4 is below 80 % a pass?
  - **The evidence is incomplete.** The grader stops at the vacuity test, so the package does not show B2/B4 separation at (25,75) in any group, or at (75,125) for grid-10 φ ≥ 0.95. "B2 and B4 separate cleanly" is shown for only 8 of 20 pair × group cases.
  - **Any criterion now would be post hoc.** Writing one after seeing these numbers, and grading it on cells 260–289, would be choosing the construction after the result.
- **Proposed fix:** "15.7 Dynamic-range instrument check (replaces 14.3's 'No vacuous pass' clause; 14.3's construction is unchanged). Pass, per φ_y and grid, at each pair (25, 75) and (75, 125):
  - every baseline B1–B4 that detects ≥ 80 % of events at both L must have non-overlapping 10th–90th-percentile ranges of per-replicate mean lead between L and L + 50;
  - the cell fails unless at least one baseline qualifies at every pair.

  The grader prints the detection rate and range for every detector, D_div included, at every pair, whether or not the pair is vacuous. Graded on fresh evaluation seeds disjoint from cells 260–289 and from every earlier range. D_div's rows are reported under 15.8 and are not graded."

**R9**
- **Pass:** 3. **Severity:** MINOR.
- **Location:** 7.4, 8.2(14).
- **Evidence:** "The E2 resamples, the E1 permutation and the E5 shifts each use a fresh `default_rng(20261030)`."
- **Why it matters.**
  - **The suite's resample stream is unspecified.** The text does not say whether the E2 resamples inside a suite replicate draw from the replicate's child stream or from the fixed 20261030 stream. If it is the fixed stream, every replicate reuses the same resample indices, and the suite's SUPPORT/INCONCLUSIVE rates understate resampling variability.
  - **E1, E2 and E5 share one stream.** They draw identical uniform streams. That is harmless for validity, but the claim "no generator is shared" is true only nominally.
- **Proposed fix:** "15.9 RNG. Within a suite replicate, every draw, including the E2 resamples, comes from that replicate's child generator. On real data, the E2, E1 and E5 generators are default_rng(SeedSequence(20261030, spawn_key=(k,))) with k = 1, 2, 3 respectively."

**R10**
- **Pass:** 3. **Severity:** MINOR.
- **Location:** 13.1.
- **Evidence:** "Construction items 19a–19f accepted as written … The 40 cells already run under them stand, with no rerun."
- **Why it matters.**
  - **Not reviewable here.** The constructions live in a findings file, not in DESIGN.md, so this review cannot check them.
  - **Accepted after the fact.** They were adopted by amendment after 40 cells had already run under them.
- **Proposed fix:** "15.10. The text of items 19a–19f is appended verbatim to DESIGN.md. The record states the commit hashes of the 40 cells' runs and of suite_findings.md at acceptance, and states that no item was changed after any of those cells was graded."

---

## Pass 4: Changes beyond what each amendment declares

**R11**
- **Pass:** 4. **Severity:** MAJOR.
- **Location:** 11.1, against D.3 E2 INCONCLUSIVE.
- **Evidence:** The frozen text says "reported with the measured detection probability at the observed effect". 11.1 fixes this at a planted "L = 100, A = 2".
- **Why it matters.**
  - **The report form changes without saying so.** The frozen report ties detection probability to the *observed* effect. 11.1 substitutes one fixed planted effect.
  - **The substitute is a REFUTE world.** At φ ≥ 0.8 that effect has D_div's mean lead *below* B2's (for example 5.7 against 8.7 at φ 0.9). Its SUPPORT rate (about 0–0.01) says nothing about power at an observed C_min > 0, which is the only situation in which INCONCLUSIVE arises.
- **Proposed fix:** "15.11. Beside an INCONCLUSIVE, 'detection probability at the observed effect' is the SUPPORT rate of the pre-committed cell (15.4 or 13.3, at the cell selected under 15.5) whose mean C_min is nearest the observed C_min, if that difference is within ±25 % of the observed C_min. Otherwise the result states 'no suite cell measured detection probability at the observed effect'. 11.1's outcome rates are reported as power at that stated planted effect, not at the observed effect."

**R12**
- **Pass:** 4. **Severity:** MAJOR.
- **Location:** 12.2, against D.5's header.
- **Evidence:** 12.2 "scopes D.5's 'committed and ALL PASS before any hashed-data run'".
- **Why it matters.**
  - **It is a relaxation, not a scoping.** Under 12.2, E2 may run while the E5 alignment control, the E1 probe and the Leg B probes are unbuilt or failing.
  - **The frozen gate was arguably already breached.** A1's loss enumeration (entry 13) is a run of code on hashed data, done before any suite pass. The amendments never address this.
  - **A gate failure could come after E2 is recorded.** The E5 control says the flag "must not trip at planted L = 100". With D_div's weak detection at L = 100 (mean leads of about 4–6 at φ ≥ 0.9), that may fail after E2 has run. This is an inference.
- **Proposed fix:** "15.12. 12.2 relaxes the frozen D.5 gate; it is recorded as a relaxation, not a scoping. The record states:
  - (a) the A1 loss enumeration (entry 13) ran before any D.5 cell passed, and which spike-rule tests (test_a1_events.py; Amendment 3 cases) had passed at that commit;
  - (b) if a later gate fails after E2 is recorded, E2's label stands and the failure is reported beside it, unless the failure is a pipeline fault in code shared with E2, in which case E2 is re-run once with the corrected code and both results are reported."

**R13**
- **Pass:** 4. **Severity:** MINOR.
- **Location:** 7.6.
- **Evidence:** "Detected requires lead > 0 … Lead values are unchanged."
- **Why it matters.**
  - **Detection rates change.** Under the frozen text, an alarm at t_e itself was not a miss, so it counted as detected. 7.6 moves it to a separate "concurrent" count, which changes every detection rate.
  - **Those rates drive other rules.** They trigger D.3 E2's "≤ 50 %" clause, 10.2's lookup and 14.3's ≥ 80 % qualification. 7.6 declares only that leads are unchanged.
- **Proposed fix:** "15.13. The detection rate in D.3 E2's ≤ 50 % clause, in 10.2 and in 14.3 is detected / eligible as defined in 7.6. The rate including concurrent events is reported beside it."

**R14**
- **Pass:** 4. **Severity:** MINOR.
- **Location:** 9.1, 8.1.
- **Evidence:** 9.1 is titled "wording corrected to the cited source". It "corrects the Amendment 5.2 B4 'Warm-up' bullet".
- **Why it matters.**
  - **Real behaviour changes.** 9.1 changes B4's real-data behaviour after every reset, not only its wording.
  - **The reference's independence for this item is unrecorded.** The discrepancy was found by the reference (D-03), and the spec was then amended toward production and source. The record does not say who edited `reference/` to match, so its independence for this item is not established.
- **Proposed fix:** "15.14. 9.1 changes B4's real-data behaviour after a reset. For D-03 and D-04 the record states which implementation changed, who changed it, and that the reference author changed the reference from the amended DESIGN text alone."

---

## Pass 5: Internal consistency

**Items checked and found consistent:**
- **8.1 against the frozen D.5 pass criteria.** The replacement is declared: the oracle is withdrawn and the planted effect becomes reported. Its cost is R4.
- **7.4 against 8.2(14).** The supersession is explicit.
- **13.3's arithmetic.** The block sizes (1,420 / 10,820 / 34,390, total 46,630) and the 2,920-step eligible span are correct.

**R15**
- **Pass:** 5. **Severity:** MAJOR.
- **Location:** 10.2, against 10.3.
- **Evidence:** 10.3 rejects the step because a false-SUPPORT criterion on it "would pass trivially". Yet all 25 null_pulse_sweep cells read "SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000".
- **Why it matters.**
  - **The pulse is worse than the step it replaced.** When h is tuned for D_div, the raw readers saturate. When it is tuned for a raw reader, D_div sits at about 1–3 %. In both cases SUPPORT is structurally impossible.
  - **F1's requirement is not measured.** F1 asks for the false-support rate when *all* detectors are weak together. Nothing in the suite measures it, and 10.2's lookup would report a structural 0.000 as reassurance.
- **Proposed fix:** "15.15. The pulse-sweep cells (10.2) are relabelled 'characterization: detector response to a one-observation pulse', with no criterion. 10.2's 'Use in E2' is withdrawn. If every detector's detection rate on A1 is ≤ 50 %, the result states that the suite has no construction in which all five detectors sit jointly in 30–50 %, and reports instead the planted-null false-SUPPORT rate (13.3, at the cell selected under 15.5) and the step-precursor rates (10.3)."

**R16**
- **Pass:** 5. **Severity:** MAJOR.
- **Location:** 14.3, against A1.5 and 13.2.
- **Evidence:** 14.3 requires D_div ≥ 80 % at "L ∈ {25, 75, 125}" (per-step) and 250 steps (grid). A1.5 says "a precursor shorter than about one fast window (320 steps) favours the raw-reading baselines by construction."
- **Why it matters.**
  - **A self-contradiction.** L = 25 is below w_f = 32 (per-step), and 250 steps is below 320 steps (grid). Requiring D_div to detect ≥ 80 % there contradicts the design's own scope condition. 13.2 even certifies the opposite behaviour as a gate.
  - **Half of S-6 follows from this.** The (25,75) failure in all 10 groups is this inconsistency, not new information.
- **Proposed fix:** covered by R8's 15.7, which removes D_div from the gate. Add to 15.7: "D_div's (25, 75) rows are labelled 'inside the A1.5 scope condition'."

**R17**
- **Pass:** 5. **Severity:** MAJOR.
- **Location:** 12.2 target date; §K re-set; S-6 decision rule.
- **Evidence:** "The E2 gate is targeted to reach ALL PASS by 2026-11-18". §K: "If E2 is still unrun on the re-set day, §K returns CLOSE with a short null note on data availability".
- **Why it matters.**
  - **A mislabelled close.** §K's re-set was written for unavailable data. If a suite hold uses it, the final CLOSE note would cite "data availability", which would be false.
  - **The timing is tight.** Two days separate the target from the grading day (2026-11-20).
- **Proposed fix:** "15.16. If E2 is unrun on 2026-11-20 because its suite gate has not passed, the DECISIONS/RECORD entry states that reason. The re-set day is set once, by dated amendment, to 2026-12-04. If E2 is still unrun then, §K returns CLOSE with a null note titled 'suite gate not met'. The note reports S-1 to S-6, the failing cells and this review. It never cites data availability."

**R18**
- **Pass:** 5. **Severity:** MAJOR.
- **Location:** 10.1, against D.2 P-HOLD note (i).
- **Evidence:** Note (i) says the unequal-memory null "measures this, so it is bounded". S-2 finding 3 says "the cell measures the invariance that the N1 fix built in".
- **Why it matters.**
  - **The frozen Methods claim loses its support.** It says the second-order effect of *differently clustered onsets* is bounded by this cell. But S₁ and S₄₀ have nearly identical onset processes under P-HOLD, and criterion (c) passes by construction (0.965–1.000).
  - **Nothing now bounds the effect for the real detectors.**
- **Proposed fix:** "15.17. Reported from every planted-null cell, including 13.3 on the A1 layout: per detector, the share of events with at least one in-window alarm and the mean in-window chance lead. The largest between-detector difference is stated in the Methods as the measured size of note (i)'s second-order effect. It replaces the claim that the unequal-memory cell bounds it."

**R19**
- **Pass:** 5. **Severity:** MINOR.
- **Location:** 14.1, 14.2; §K grading.
- **Evidence:** "moves to the Phase 3 gate"; 14.2's self-test covers "one byte changed" only.
- **Why it matters.**
  - **Unverified verdict.** §K's verdict would be recorded before verify.py exists.
  - **Partial coverage.** 14.2 covers one of the fixture's three legs. The out-of-tolerance leg is partly covered by reference agreement; the unsigned CIC flag leg is not covered at all.
- **Proposed fix:** "15.18. The E2/§K entry is marked 'verification pending (Phase 3 broken fixture)' until verify.py passes the D.5 broken fixture. The label is not changed by verification unless verify.py finds a value outside tolerance, which is then reported as a correction."

**R20**
- **Pass:** 5. **Severity:** MINOR.
- **Location:** 8.2(14), 10.1, 12.1, 13.3, 14.3 (seed-disjointness claims).
- **Evidence:** "children of `numpy.random.SeedSequence(20261030).spawn(N)`"; "child indices 23,000–23,999, which no run has used".
- **Why it matters.**
  - **Asserted, not shown.** N is never stated. Indices up to 40,000,000+ are used, and no seed map appears in DESIGN, so disjointness cannot be checked.
  - **Ordering is unverifiable.** "Graded on fresh seeds" depends on cells.json having been committed before each exploratory run.
- **Proposed fix:** "15.19. Child i is defined as SeedSequence(20261030, spawn_key=(i,)). A committed seed map lists every index range with its cell, its purpose (calibration, exploratory or evaluation) and the commit hash at which it was first assigned. That hash must precede the first run using the range."

**R21**
- **Pass:** 5. **Severity:** MINOR.
- **Location:** 7, 8, 11 status lines.
- **Evidence:** "before any gradient-norm value is read for scoring", against the background's "No gradient-norm value has entered any computation".
- **Why it matters.** "For scoring" is a weaker claim. The record should carry the stronger one, if it is true.
- **Proposed fix:** "15.20. As of this amendment no gradient-norm value has entered any computation, for scoring or otherwise; the only operations on files containing them are SHA-256 byte hashes."

---

## Pass 6: Question (a), S-6

**R22**
- **Pass:** 6. **Severity:** MAJOR.
- **Location:** S-6; 14.3; dyn-range rows.

**Strongest case for PIPELINE-INVALID.**
1. **The Standard's own flag.** It marks "any … no-dynamic-range metric" as verdict-invalid. C_min contains D_div's mean lead as one term. If that term cannot resolve 50-observation differences in precursor length, C_min's sign is set by D_div's noise and the baselines' leads, not by D_div's warning ability.
2. **The author's own BLOCKER test.** Combined with S-5, the outcome barely moves with the data at φ ≥ 0.8: REFUTE is 0.87 under the null and 0.85 under the effect (a1s, φ 0.9). That is the test the author applied to S-1 and Amendment 6 ("the rule decides the outcome independently of the data").

**Strongest case for METHOD PROPERTY.**
1. **The measuring chain has range.** The same statistic, matching, hold and lead code, agreeing exactly with an independent reference, resolves 50-observation differences for B2 and B4 with clean separation.
2. **D_div's own response is weak but not flat.** Its median lead rises with L in every group. What is wide is its spread across replicates.
3. **Half the failure is predicted by the design.** The (25,75) failure is A1.5's scope condition (R16).
4. **The outcome does move where the design expects D_div to work.** At φ 0.5, null REFUTE is 0.85–0.87 against 0.43 under the a1s effect. Its near-invariance at high φ coincides with D_div being *beaten* in those constructions. A REFUTE is then the correct answer to E2's comparative question, not an unmeasured one.
5. **Holding E2 for this reason would make the gate block negatives** (R2).

**Candidate mechanism** (an inference, not verified from the package). D_div's score is a percentile over history since the last gap. A fixed θ near 1 therefore acts as a different effective bar at different distances from the block start: near the start, alarming needs a near-record value; late in the block, it only needs to be in the top fraction. Per-event detection then depends on the event's position, and per-replicate mean leads become a mixture of misses, late detections and chance leads (S-4's lead of about 120). The baselines' scales do not drift in this way.

**Verdict.**

`S-6: METHOD PROPERTY`

E2's comparative question is validly measured. Its interpretation must carry the limitation in R3 and in 15.8 below.

**Evidence that would change the verdict to PIPELINE-INVALID:**
- **(a)** In the R4 positive control, D_div's population mean lead beats every baseline by ≥ 100 steps, yet SUPPORT + INCONCLUSIVE is not materially above the null's rate of about 0.13. The statistic would then be unable to express a real advantage.
- **(b)** Fixing θ at its long-series population value collapses D_div's 10–90 spread but not the baselines'. The *matching step* (P-FA at n* ≈ 4–5), not the detector, would then be making one side of the contrast noisier. That is an asymmetric fault of the procedure.
- **(c)** Not verdict-changing: if regressing D_div's per-event lead on history length since the gap explains most of the spread, that confirms the mechanism above and should be reported.

**Proposed fix:** "15.8 D_div lead response (reported beside E2). E2's result states:
  - D_div's 10th–90th-percentile ranges at L ∈ {75, 125} (per-step and grid-10, every φ_y);
  - its detection rates at every L in 14.3;
  - that, unlike B2 and B4, D_div's lead does not resolve 50-observation differences in precursor length at A = 6;
  - that E2 therefore tests whether D_div's mean lead exceeds the best baseline's, not whether D_div tracks precursor length.

  Checks (b) and (c) of this review are run on synthetic cells before E2 and reported."

---

## Pass 7: Question (b), correction or rescue?

**R23 — S-1.**
- **Pass:** 7. **Severity:** MINOR.
- **Location:** 8.1; S-1.
- **Evidence:** "no correct pipeline can meet the criterion for B1, B2 and B3."
- **Assessment against the four questions:**
  - The original oracle was unattainable by any correct pipeline: a 10⁻³-noise oracle cannot be the noisy pipeline's target.
  - The replacement was fixed before the suite run.
  - Agreement is deterministic, so fresh seeds are not at issue.
  - It does weaken what the suite certifies: from "recovers the planted effect" to "computes the spec", with the planted effect demoted to power. R4 restores a positive control.
- **Verdict:** `S-1: CORRECTION`
- **Proposed fix:** R4 (15.4).

**R24 — S-2.**
- **Pass:** 7. **Severity:** MINOR.
- **Location:** 10.1; S-2.
- **Evidence:** "REFUTE is the correct outcome there."
- **Assessment against the four questions:**
  - "False-REFUTE ≤ 0.05" is unattainable by any correct pipeline: under a no-precursor null, C_min ≤ 0 is a true statement.
  - The criterion was chosen after an exploratory run that was declared as such.
  - It was graded on fresh seeds.
  - What it now certifies is a built-in invariance. The frozen note (i)'s bound needs R18.
- **Verdict:** `S-2: CORRECTION`
- **Proposed fix:** R18 (15.17).

**R25 — S-3.**
- **Pass:** 7. **Severity:** MAJOR.
- **Location:** 10.2; S-3.
- **Evidence:** All 25 pulse cells read "0.000/0.000/1.000".
- **Assessment against the four questions:**
  - The frozen F1 band was likely attainable by another construction (the step came close: four detectors in 0.35–0.55, B1 near 0.2). Its infeasibility was shown for the pulse only.
  - The replacement was fixed before grading and graded on fresh seeds.
  - However, it replaces a joint-weakness condition with one that cannot fail by construction, and adds a lookup that would report that structural zero as severity. It lowers the bar so that the gate passes.
- **Verdict:** `S-3: RESCUE`
- **Proposed fix:** R15 (15.15). Optionally, a reported mixed-shape cell that targets the joint band, with no criterion.

**R26 — S-4.**
- **Pass:** 7. **Severity:** MINOR.
- **Location:** 12.1; S-4.
- **Evidence:** "the binding criterion is changed after the frozen bar failed."
- **Assessment against the four questions:**
  - REFUTE ≥ 0.95 is unattainable by a correct pipeline under the frozen statistic, because of the chance-alarm floor. Even the alternative flip_long cells, with A calibrated, fall to 0.935–0.940 in three cells.
  - The change is disclosed.
  - It was graded on fresh seeds.
  - The REFUTE rate is reported as the kill rule's power. The cost: the binding criterion "SUPPORT ≤ 0.05" now largely duplicates the planted null, so the flip no longer certifies that the kill rule fires.
- **Verdict:** `S-4: CORRECTION`
- **Proposed fix:** "15.21. The decision-flip REFUTE rates (0.825–0.950 per-step; 0.875–0.935 on the A1 layout) are stated in the Methods as the kill rule's measured power against short precursors. The flip's binding criterion is recorded as a false-SUPPORT check, not as a demonstration that the rule returns REFUTE."

**S-5.** S-5 changes no criterion, so no verdict applies. Its "Reading" should be corrected to say that, in most effect cells, a baseline's mean lead exceeds D_div's, so REFUTE is the correct comparative answer there (R4).

**R27 — S-6 (the proposed treatment).**
- **Pass:** 7. **Severity:** MAJOR.
- **Location:** S-6 decision rule; 14.3.
- **Evidence:** "method property → apply the bar to B2/B4 as the instrument check".
- **Assessment against the four questions:**
  - A correct pipeline meets the clause only if D_div has the property. The clause therefore tests the hypothesis, not the instrument, and its (25,75) half contradicts A1.5 (R16).
  - The treatment was *not* fixed before the graded run, and *not* yet graded on fresh seeds.
  - It removes a certification of D_div's sensitivity, which is the thing E2 is meant to measure. A gate requiring the method under test to perform before it may be tested would systematically turn negatives into no-results (R2).
  - Dropping D_div from the gate is therefore a correction of the gate's scope, **on the condition** that R8's criterion (15.7) is committed before any further dynamic-range run and graded on fresh seeds, and that 15.8 is adopted. Without those conditions it is a rescue.
- **Verdict:** `S-6: CORRECTION` (conditional on 15.7 and 15.8)
- **Proposed fix:** 15.7 and 15.8.

**Net consequence for the owner's decision rule.** Under the verdicts above, the rule's "method property" branch applies. E2 may proceed once 15.7 is graded on fresh seeds and passes, and once 15.3, 15.5, 15.6, 15.8, 15.11 and 15.16 are committed, all before any gradient-norm value is read.

---

## Summary table

| ID | Pass | Severity | Location | Finding | Verdict |
|---|---|---|---|---|---|
| R1 | 1 | MINOR | §K; 7.1–7.3, 7.5, 9.1–9.2 | Real-data construction changes after A1 touched; permissible, but undeclared against §K's wider clause | — |
| R2 | 1 | MAJOR | 14.3; S-6 rule; §K re-set | D_div's synthetic weakness can route the project to CLOSE instead of STOP | — |
| R3 | 2 | MAJOR | D.3 E2; §K | REFUTE is modal under null and effect alike (likelihood ratio ≈ 1 at φ ≥ 0.8); what REFUTE establishes | — |
| R4 | 2 | MAJOR | D.5/8.1; S-5 | No positive control; SUPPORT reachable only near φ 0.5 | — |
| R5 | 3 | MAJOR | D.5 regime span; 10.2; 11.1; 13.3 | φ̂_y on A1 undefined; cell selection is a judgment | — |
| R6 | 3 | MAJOR | 10.2 | Lookup does not yield one number | — |
| R7 | 3 | MAJOR | 11.1 vs 13.3 | Two candidate cell families for A1's power figures | — |
| R8 | 3 | BLOCKER | S-6 rule; grader | Instrument-check criterion unwritten; B2/B4 evidence partly masked | — |
| R9 | 3 | MINOR | 7.4; 8.2(14) | Suite resample stream unspecified; E1/E2/E5 share one stream | — |
| R10 | 3 | MINOR | 13.1 | Constructions accepted by reference, after cells ran | — |
| R11 | 4 | MAJOR | 11.1 vs D.3 E2 | Fixed planted effect substituted for the "observed effect" | — |
| R12 | 4 | MAJOR | 12.2 vs D.5 | Gate relaxed but called a scoping; enumeration timing unaddressed | — |
| R13 | 4 | MINOR | 7.6 | Detection-rate change feeds triggers, undeclared | — |
| R14 | 4 | MINOR | 9.1; 8.1 | Real-data B4 change; reference independence for D-03 unrecorded | — |
| R15 | 5 | MAJOR | 10.2 vs 10.3 | Pulse null passes more trivially than the rejected step | — |
| R16 | 5 | MAJOR | 14.3 vs A1.5, 13.2 | D_div ≥ 80 % required inside the design's own scope condition | — |
| R17 | 5 | MAJOR | 12.2; §K re-set | A suite hold would close under a "data availability" label | — |
| R18 | 5 | MAJOR | 10.1 vs D.2 note (i) | The "bounded" claim no longer has a measurement behind it | — |
| R19 | 5 | MINOR | 14.1–14.2 | §K recorded before verify.py exists; fixture coverage partial | — |
| R20 | 5 | MINOR | 8.2(14) et al. | Seed disjointness asserted, not shown | — |
| R21 | 5 | MINOR | 7, 8, 11 status lines | "Read for scoring" is weaker than the background claim | — |
| R22 | 6 | MAJOR | S-6 | Dynamic-range failure is D_div's, not the pipeline's | **S-6: METHOD PROPERTY** |
| R23 | 7 | MINOR | S-1 / 8.1 | Unattainable oracle replaced before the run | **S-1: CORRECTION** |
| R24 | 7 | MINOR | S-2 / 10.1 | Unattainable bar; fresh seeds; bound restored by R18 | **S-2: CORRECTION** |
| R25 | 7 | MAJOR | S-3 / 10.2 | Replacement cannot fail by construction | **S-3: RESCUE** |
| R26 | 7 | MINOR | S-4 / 12.1 | Bar unattainable under the frozen statistic; power now reported | **S-4: CORRECTION** |
| — | 7 | — | S-5 | Severity record; no criterion changed | no verdict |
| R27 | 7 | MAJOR | S-6 treatment | Correct scope fix only if 15.7 is fixed first and graded on fresh seeds | **S-6: CORRECTION** (conditional on 15.7, 15.8) |