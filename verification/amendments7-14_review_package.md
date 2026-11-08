# PACKAGE — independent check of DESIGN Amendments 7–14 and suite findings S-1 to S-6

Frozen text verbatim from DESIGN.md at tag prereg-v1 (MD5 a9d051ac65fde38d5001a433b5d11506). Amendments verbatim from DESIGN.md (MD5 939ed539e232214d5ec0531048df504c). Findings verbatim from verification/suite_findings.md (S-1..S-6 sections only) and the suite verdict from verification/suite_verdict.md.

=== PART 1: Amendments 7–14 (under review) ===

## Amendment 7 (2026-10-31) — Construction items found while building the D.5 suite

**Status.** Appended below Amendment 6 under the append-only rule. Rationale: DECISIONS.md entry 18 (JAE decision 2026-10-31). Made and pushed before the D.5 suite is frozen or run for the record, and before any gradient-norm value is read for scoring. No detector threshold has been computed for any run. The working record of the eight items is `verification/construction_items_pending.md`.

**7.1 B4 candidate thresholds (P-FA, Amendment 6).** B4's score path depends on θ through its reset at each onset. The candidate set is the distinct out-of-window scored values of B4's **reset-free** path (θ = none). c(v) for each candidate is evaluated on the path **recomputed** at that candidate, with resets.

**7.2 N_out.** One common denominator for all detectors: grid observations with j ≥ 1,000 that lie outside every scan window. An observation where a detector's score is undefined (for example B1 with sd = 0) stays in N_out and is a non-alarm.

**7.3 Fresh crossing after an undefined score (P-HOLD).** An undefined s(j−1) counts as below θ. This is the same convention the frozen text uses for the first scored observation of a series and of each post-gap restart.

**7.4 P-RNG streams.** Each procedure creates its own generator; no generator is shared across procedures.
- The E2 resamples, the E1 permutation and the E5 shifts each use a fresh `default_rng(20261030)`.
- Each D.5 suite cell × replicate uses `default_rng([20261030, c, r])`, where c is the cell's index in the committed suite cell table and r the replicate index (0-based).
- Results therefore do not depend on the order in which procedures run.

**7.5 Percentile method.** The 5th percentile of the resampled C_min (D.3 E2) uses numpy's default linear interpolation (`numpy.percentile`, `method="linear"`).

**7.6 Detected and concurrent (D.3 E2 reporting).**
- **Detected** requires lead > 0: the detector is first in alarm inside the scan window strictly before t_e^g. A left-censored event (lead = 1,280) counts as detected.
- **Concurrent:** an event whose first in-window alarm is at t_e^g itself (lead 0). It is reported separately, per detector, as a "concurrent" count. It is neither detected nor a miss.
- **Miss:** no in-window alarm.
- The detection rate = detected / eligible events. Miss count and concurrent count are reported beside it.
- **Lead values are unchanged.** A concurrent event has lead 0, as does a miss (P-MISS), so the mean lead, every C_b, C_min and the E2 label are unaffected.

**7.7 Planted precursor (D.5 "Planted effect").**
- **Shape.** A linear rise in y from 0 to A over the L observations ending at the event (L ∈ {64, 100, 150, 200}; the A1-grid cell uses {640, 1,000, 1,500, 2,000} steps), added to the AR(1) base. After the event the series returns to the base.
- **Amplitude.** A ∈ {1, 2, 3} × the stationary SD of y. Every A is reported, and the pass criteria are applied at each A.
- **Gradient norm.** The synthetic g = exp(y), since y = ln g by definition.

**7.8 Suite events.**
- In the detector cells, events are planted directly at known steps.
- The spike rule is validated separately (`scripts/tests/test_a1_events.py`; the Amendment 3 suite cases).
- **End-to-end cell (JAE).** A generated loss series carries spikes, the spike rule finds the events, and the full pipeline runs on them. It is run in two cases:
  - **planted effect:** the precursor ramp in y ends at each loss spike;
  - **planted null:** no precursor.
  Each case must meet the D.5 pass criteria.

**Unchanged.** Windows, ratio, H, the FA rule and grid, P-FA top-scan matching and the coverage stop (Amendment 6), lead and censoring definitions, the spike rule, every outcome partition, and §K's thresholds, windows, spike definition and FA grid.

## Amendment 8 (2026-10-31) — D.5 oracle replaced by an independent reference implementation (suite finding S-1); suite construction items 9–14

**Status.** Appended below Amendment 7 under the append-only rule. Rationale: DECISIONS.md entry 19 (JAE decision 2026-10-31). Evidence: `verification/suite_findings.md` S-1, `scripts/tests/probe_oracle_criterion.py` and its outputs (synthetic data only). Made before the D.5 suite is frozen or run for the record, and before any gradient-norm or loss value is read for scoring.

**Defect (S-1).**
- D.5's oracle (F10; fix rounds N2, N4; restated in A1.7) applies the θ matched on the noisy series to the same planted series with the noise scaled by 10⁻³. It requires |recovered mean lead − oracle mean lead| ≤ 8 steps for every detector.
- For the detectors that normalise by a noise estimate (B1, B3), the 10⁻³ scaling makes the ramp about 1,000 noise-SDs tall, so the oracle lead is the ramp onset (L − 1). For B2, the noisy-series θ lies above the noise-free ramp, so the oracle lead is 0.
- The recovered leads are bounded by the noise, so the criterion cannot be met by any correct pipeline. D.5 could never be ALL PASS, and no hashed-data run could happen.
- **This was a design-stage error.** The design review adopted it without testing it on the normalised detectors. The suite found it before any real data.

**8.1 Replacement oracle (replaces the D.5 "Oracle" sentence and pass criteria, and the A1.7 lead tolerance).**
- **Reference implementation.** The oracle is an independent re-implementation of the whole chain on per-observation loops: block preparation (carry-forward, j counting), scores D_div and B1–B4, P-FA top-scan matching with hold and the coverage figure, leads (detected, concurrent, censored), C_b and C_min.
  - It is written from DESIGN.md (D.0–D.7 and Amendments 1–8) only, by a separate agent that is given only DESIGN.md and has no access to `analysis/` or `scripts/`.
  - It lives in `reference/`. How it was written is recorded in DECISIONS.md.
- **Pass, per suite cell.** On the same noisy series, both implementations must give:
  - θ and the realised onset count, equal to 1e-6 relative;
  - identical onset steps and identical leads (with the detected, concurrent and censored flags) for every detector;
  - C_min equal to 1e-6;
  - the same C_min sign in **100 %** of replicates.
- **Hand probes.** Both implementations must also reproduce exactly every hand-computed deterministic probe: onset, θ, lead and C_min (including the Amendment 5.3, 6.3 and 7.6 probes).
- **Kept unchanged:**
  - the planted null (false-support ≤ 0.05);
  - the unequal-memory null (false-REFUTE and false-SUPPORT each ≤ 0.05);
  - the decision flip (REFUTE);
  - dynamic range, the k ladder, regime span, alignment control, assembly probes, Leg B probes and the broken fixture.
- **Planted-effect cells (including the A1.7 ten-step grid cell).** These report, per cell, the recovered mean and median lead with the detection, concurrent and miss counts for every detector, plus the rule's outcome rates (SUPPORT, INCONCLUSIVE, REFUTE). This is power. It is reported, not required.
- The 10⁻³ noise series and its finite-score assertion are withdrawn.

**8.2 Suite construction (items 9–14; JAE).**
- **(9) Series.**
  - Each per-step cell series has 50,000 observations.
  - Events are placed at uniform random positions, with consecutive t_e at least scan + L_max + 1 = 329 observations apart and the first t_e ≥ 1,000 + scan + L_max.
  - The A1.7 ten-step grid cell keeps its own geometry (A1.7).
- **(10) Event in y.**
  - **Primary:** the event is a label at t_e. The ramp, if any, ends at t_e, and y then returns to the AR(1) base.
  - **Added surge cell:** the same series with y += 3·(50 − i)/50 at t_e + i, for i = 0 … 49. This is a +3 SD surge decaying linearly to 0 over 50 observations. Post-event out-of-window onsets then enter FA matching, as in real logs.
  - The surge cell runs for the planted null and the planted effect (L = 100, A = 2), across the φ_y grid at 20 events.
- **(11) Innovations.**
  - **Primary:** Gaussian AR(1) with mean 0 and unit stationary SD; g = exp(y).
  - **Added:** a Student-t cell (df = 3, scaled to unit innovation SD) for the planted null and the decision flip, across the φ_y grid at 20 events.
- **(12) Cell crossing.** 200 replicates per cell.
  - Planted effect: φ_y (5) × L (4) × A (3) at 20 events.
  - Regime span: φ_y (5) × events {5, 10, 20, 40} at L = 100, A = 2.
  - Planted null and decision flip: φ_y (5) at 20 events.
- **(13) Null with every detector's detection rate at 30–50 % (F1).**
  - Each event gets a one-observation pulse of height h at a uniform random offset in [1, scan] before it, with no ramp.
  - h is set per φ_y by a calibration run so that every detector's detection rate at headline FA lies in 30–50 %.
  - Calibration uses seeds disjoint from every evaluation seed. The calibration script and its output are committed before the suite verdict run.
- **(14) Seeds and execution.** This **supersedes Amendment 7.4's suite clause.** The E2, E1 and E5 clauses of 7.4 are unchanged.
  - The per-replicate seeds are children of `numpy.random.SeedSequence(20261030).spawn(N)`.
  - Each cell × replicate has a fixed child index, given in the committed cell table. Calibration uses an index range disjoint from every evaluation range.
  - Results are independent of worker scheduling. One cell is run both single-process and multi-process, and the results must be identical.
  - The suite is run with multiprocessing on the Windows host.

**Unchanged.** Every rule applied to real data: detectors, windows, ratio, H, the FA rule and grid, P-FA top-scan matching, the coverage stop, leads and censoring, the spike rule, every outcome partition, and §K's thresholds, windows, spike definition and FA grid.

## Amendment 9 (2026-10-31) — Amendment 5.2 wording corrected to the cited source (D-03, D-04); suite items 15–16

**Status.** Appended below Amendment 8 under the append-only rule. Rationale: DECISIONS.md entry 20 (JAE decision 2026-10-31); Discrepancy Register D-03 and D-04. Both wording defects were found by the independent reference implementation (Amendment 8.1). No real value has been read for scoring.

**9.1 B4 warm-up (D-03; corrects the Amendment 5.2 B4 "Warm-up" bullet).**
- **Corrected text.** "The first 30 observations of a series (or after a gap) are appended to the history, with no score." The words "or after a reset" are struck.
- **Source.** trainscope 0651b25 `ChangePointDetector.update` (vendored: `scripts/tests/third_party/trainscope_0651b25/changepoint.py`, lines 79–82 warm-up and lines 106–113 fire).
  - The warm-up applies only while the history holds fewer than 30 values.
  - A fire zeroes the accumulators only and keeps the history.
- This matches Amendment 5.2's own clause "A reset does not clear the median/MAD history". After a P-B4 reset, scoring continues at the next observation with S⁺ = 0.

**9.2 B3 update weight (D-04; clarifies the Amendment 5.2 B3 "Update" bullet).** The weight written there as 0.03 is ZClip 1.0.0's coded expression (1 − α) with α = 0.97, evaluated in float64 (vendored `zclip.py` lines 79–80). The coded expression governs.

**9.3 Suite items 15–16 (D.5; JAE).**
- **(15) Decision flip.** Ramp length L = 8 observations, A = 3 (× stationary SD), 20 events, across the φ_y grid; also the Student-t cell (Amendment 8.2(11)). Pass: REFUTE in ≥ 95 % of replicates.
- **(16) Unequal-memory null.**
  - The two synthetic baselines are S₁(j) = y(j) and S₄₀(j) = max(y(j−39) … y(j)), so one exceedance keeps S₄₀ above θ for 40 observations.
  - In this cell the baseline set is {S₁, S₄₀}. Both are matched with D_div at the same FA by P-FA (Amendment 6.1), and C_min is taken over these two.
  - The pass criterion is pending the item-17 measurement (finding S-2, if any).

**Unchanged.** Everything else in Amendments 5–8 and the frozen text.

## Amendment 10 (2026-11-06) — Unequal-memory null criterion (S-2) and the 30–50 % detection null (S-3)

**Status.** Appended below Amendment 9 under the append-only rule. Rationale: DECISIONS.md entry 23 (JAE decisions 2026-11-06). Evidence: `verification/suite_findings.md` S-2 and S-3. Synthetic data only; no real value has been read for scoring.

**10.1 Unequal-memory null (replaces the D.5 "Planted null with unequal alarm memory" pass criterion; construction per Amendment 9.3(16)).**
- **Why the frozen criterion fails (S-2).** False-REFUTE was measured at 0.735–0.800 in every φ_y cell. With no precursor, C_min (the minimum of two near-zero contrasts) is ≤ 0 in most replicates. REFUTE is the correct outcome there, so "false-REFUTE ≤ 0.05" cannot be met.
- **Pass, per φ_y cell (200 replicates):**
  - (a) false-SUPPORT ≤ 0.05;
  - (b) |median C_b| ≤ 1 observation for b ∈ {S₁, S₄₀};
  - (c) |C_S1 − C_S40| ≤ 1 observation in ≥ 95 % of replicates.
- **Reported, not required:** the false-REFUTE rate, P(C_b > 0 | C_b ≠ 0), and the share of replicates with C_b = 0.
- **What it tests.** Under P-HOLD the alarm state is the hold after a fresh crossing, so a baseline's raw alarm memory should not reach the alarm state or the contrast. The cell checks that invariance.
- **Seeds.** The criterion was chosen after the S-2 measurement (child indices 20,000,000–20,004,199), so that run is recorded as exploratory. The criterion is graded on the evaluation seeds of the unequal-memory cells in `scripts/suite/cells.json` (cells 115–119, child indices 23,000–23,999), which no run has used.

**10.2 Detection-rate null (replaces the D.5 F1 clause "including cells where every detector's detection rate at headline FA is between 30 % and 50 %" and Amendment 8.2(13)).**
- **Why the frozen construction fails (S-3).** It is unattainable because the detectors respond differently to the same planted shape.
  - With a one-observation pulse at φ_y = 0.9, B1–B3 reach 30–50 % near h = 3 and saturate by h = 6.
  - B4 reaches 0.49 at h = 40.
  - D_div is at 0.27 at h = 40 and 0.77 at h = 80.
  - No single h puts all five detectors in the band.
- **Construction.** A one-observation pulse of height h at a uniform offset in [1, scan] before each event, with no ramp (unchanged from 8.2(13)).
- **Calibration sweep (calibration seeds only).** Per φ_y, h is swept on that φ_y's calibration range in `cells.json` so that **each detector separately** reaches 30–50 % detection at some h. That gives up to five values h_{φ,d}, one per detector.
  - The sweep starts from the grid {1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100, 120}. Where no grid point puts detector d in the band, midpoints are bisected on the calibration seeds until one does.
  - h_{φ,d} is the calibrated h whose calibration detection rate for d is closest to 0.40.
  - The calibration script and its output are committed before the suite verdict run.
- **Pass (evaluation seeds, disjoint from calibration).** At every calibrated h_{φ,d}, 200 replicates: false-SUPPORT ≤ 0.05.
- **Reported:** detection rate for every detector at every calibrated h (the detector × h table), with the outcome rates.
- **Use in E2.** This sweep is the lookup E2 uses when A1's realised detection rates are ≤ 50 %. The false-SUPPORT rate is read at the calibrated h nearest the realised rate, per detector.

**10.3 Step precursor (characterization only; not a null).**
- A step of height h from a uniform offset in [1, scan] before each event through t_e is a precursor. It rewards the fastest-responding detector and biases the rule toward REFUTE, so a false-SUPPORT criterion on it would pass trivially.
- It is kept as a reported characterization, labelled "step precursor, not a null": detection rate and mean lead by detector × h, h ∈ {1.5, 2, 2.5}, 200 replicates per φ_y. It has no pass criterion.

**Unchanged.** Every rule applied to real data, and every other D.5 criterion as amended through Amendment 9.

## Amendment 11 (2026-11-06) — Suite cells at A1's realised event count (57)

**Status.** Appended below Amendment 10 under the append-only rule. Rationale: DECISIONS.md entry 25 (JAE decision 2026-11-06).

**Gap.**
- D.5 requires the planted null to hold "at the realised event count". The Phase 2 checklist's experiment-validation gate asks for the planted effect, planted null and planted decision flip "at the REAL event count".
- A1's realised count is 57 eligible events at k = 4 (DECISIONS entry 13). It was enumerated from the loss series alone, before any detector score was computed or any gradient-norm value read for scoring, in the P-KLAD order.
- Amendment 8.2(12) put the nulls and the decision flip at 20 events, and the regime span stops at 40, so no cell tested the realised count.

**11.1 Added cells (57 events, across the φ_y grid, 200 replicates each, on new SeedSequence child ranges disjoint from every earlier range).**
- **Planted null at 57:** no precursor. Pass: false-SUPPORT ≤ 0.05.
- **Decision flip at 57:** L = 8, A = 3 (Amendment 9.3(15)). Pass: REFUTE in ≥ 95 % of replicates.
- **Planted effect at 57:** L = 100, A = 2 (the regime-span setting). Reported, not required. Its outcome rates are the detection probability at this effect and this event count that E2 reports beside an INCONCLUSIVE.

**Unchanged.** Every other cell and criterion, and every rule applied to real data.

## Amendment 12 (2026-11-06) — Decision-flip criterion (S-4) and per-experiment suite gates

**Status.** Appended below Amendment 11 under the append-only rule. Rationale: DECISIONS.md entry 27 (JAE decisions 2026-11-06). Evidence: `verification/suite_findings.md` S-4, `verification/suite_verdict.md` (suite run v1), `scripts/outputs/s4_flip_phi0.9.txt`.

**12.1 Decision flip (replaces D.5 "Planted decision flip: … the rule must return REFUTE" as amended by 9.3(15)).**
- **Stated plainly:** the binding criterion is changed after the frozen bar failed. Suite run v1 graded every decision-flip cell FAIL: REFUTE 0.81–0.93 against ≥ 0.95 (20 and 57 events; Gaussian and t3).
- **Why the bar failed.** It assumed a zero chance-alarm floor under the mean-lead statistic.
  - Under the frozen statistic, any in-window alarm is a lead and a miss counts 0.
  - A single chance D_div alarm early in an event's 129-observation window has a lead of about 120.
  - That outweighs the baselines' genuine leads on an 8-observation ramp (at most L − 1 = 7), which makes C_min > 0 and the label INCONCLUSIVE.
- **The construction is not changed:** L = 8, A = 3, at 20 events (Gaussian and t3) and at 57 events, across the φ_y grid.
- **Binding criterion:** SUPPORT ≤ 0.05, graded on fresh evaluation seeds disjoint from every earlier range. The v1 flip cells are kept as the record of the failed bar.
- **Reported:** the REFUTE rate, as the kill rule's measured power against short-precursor worlds (v1: 0.81–0.93). It is stated in the Methods and beside the E2 result, with the mechanism above.
- **Added reported cells (no criterion):** L ∈ {16, 24} at 20 events across the φ_y grid. A is calibrated on calibration seeds as the smallest value in {3, 4, 5, 6, 8, 10, 12} at which the best raw-reading baseline (B1, B2 or B3) detects ≥ 90 % of events.

**12.2 Per-experiment suite gates (scopes D.5's "committed and ALL PASS before any hashed-data run").**
- **Purpose preserved:** no experiment touches real data with unvalidated code. The gate applies per experiment, before that experiment's first hashed-data run.
- **E2, E3, E4 gate.** Every statistical cell already built (Amendments 7–12) plus:
  - dynamic range (lead separation at planted L differences of 50 steps, planted ties, planted cluster with censoring and chained dedup);
  - the ten-step grid cell (A1.7);
  - the end-to-end loss-series cell, planted effect and planted null (Amendment 7.8);
  - the assembly probes (D.5);
  - the broken fixture (verify.py).
- **E1 gate.** E1's exact-identity hand probe (Amendment 4.1 suite addition).
- **E5 gate.** The alignment control (D.5 "Alignment control (E5)").
- **Leg B gate.** The Leg B probes (D.5 "Leg B"), before Leg B's first hashed-data run.
- **Order and target.** The ten-step grid and assembly probes are built first, since A1 is both. The E2 gate is targeted to reach ALL PASS by 2026-11-18.

**Unchanged.** Every rule applied to real data, and every other D.5 criterion as amended through Amendment 11.

## Amendment 13 (2026-11-07) — Ten-step grid and end-to-end construction (items 19a–19f); short-ramp bar; A1-structure cells

**Status.** Appended below Amendment 12 under the append-only rule. Rationale: DECISIONS.md entry 29 (JAE decisions 2026-11-07). Synthetic data only; the A1 layout is read from the committed structural report (step index only).

**13.1 Construction items 19a–19f accepted as written** (`verification/suite_findings.md`; `analysis/synth_e2e.py` ea5b385c5cf8053ccbfccf3fb3bef405). The 40 cells already run under them stand, with no rerun (DECISIONS entry 28).

**13.2 Short-ramp cell (A1.7 "must show the A1.5 scope condition").**
- A1.7's "must show" is a gate. Binding criterion, in the Amendment 12.1 form fixed before this cell was measured: SUPPORT ≤ 0.05, graded on fresh disjoint seeds.
- Reported: the REFUTE rate (measured 0.935–0.990 on the first seeds, which are kept as the record).
- This is a pipeline criterion only. It does not qualify §K (G11 unchanged), and the A1.5 scope statement stays in the Methods.

**13.3 A1-structure cells (E2 gate).**
- **Layout.** Synthetic series on A1's kept-series block/gap layout, from `scripts/outputs/a1_structural_report.json` `kept_blocks` (step index only): steps 1–14,200, 52,301–160,500 and 160,601–504,500, observed on step mod 10 = 0, giving 46,630 grid observations. This exercises the short first block (1,420 grid observations, mostly consumed by the 1,000-observation minimum history) and the 160,501–160,600 gap.
- **Events.** 61 planted loss spikes, mirroring A1's realised enumeration (entry 13): 57 eligible and 4 ineligible on minimum history (2 in block 1, 1 in block 2, 1 in block 3).
  - The eligible events are split 1 / 13 / 43 across the blocks, roughly in proportion to each block's eligible span, with one placed in block 1's 2,920-step eligible span.
  - Residues of t_e mod 10 cycle 0–9. Spacing is ≥ L_max + scan + grid steps.
  - Loss construction, spike rule (k = 4, dedup 2,000) and gradient-norm construction are as in 13.1 (19c, 19d).
- **Cells (across the φ_y grid, 200 replicates each, fresh disjoint seeds):**
  - planted null: false-SUPPORT ≤ 0.05;
  - decision flip, L = 80 steps (8 grid observations), A = 3: SUPPORT ≤ 0.05, REFUTE reported (12.1);
  - planted effect, L = 1,000 steps, A = 2: reported.
- **Eligibility check, every replicate.** The A1 eligibility rule (`scripts/a1_events.py` `eligibility`) must reproduce the designed eligibility of every planted event: 4 ineligible, split 2 / 1 / 1 by block, and 57 eligible. Ineligible events are reported per block against the rule's prediction. The spike rule must recover exactly the 61 planted events.
- Reference agreement (8.1) applies to these cells.

**Unchanged.** Every rule applied to real data, and every other D.5 criterion as amended through Amendment 12.

## Amendment 14 (2026-11-07) — Broken fixture moved to Phase 3; PRV hash self-test; graded dynamic-range cells

**Status.** Appended below Amendment 13 under the append-only rule. Rationale: DECISIONS.md entry 32 (JAE decisions 2026-11-07).

**14.1 Broken fixture (corrects Amendment 12.2's placement).**
- The D.5 broken fixture ("verify.py must fail on a corrupted hash, an out-of-tolerance value, and an unsigned CIC flag") moves to the **Phase 3 gate**. Per the Standard, verify.py is built at Phase 3 against claims.lock and the 7 CIC classes, and none of these exists before then.
- Amendment 12.2's listing of the broken fixture under the E2 gate is withdrawn.

**14.2 PRV hash self-test (E2 gate).**
- Data integrity before E2 is already required by D.6 item 7: SHA-256 re-verification at read time, in PRV.
- The check is `scripts/prv_hash_check.py`. It re-hashes every store file listed in SOURCES.md against its recorded SHA-256 and halts (exit 1) on any mismatch or missing file.
- **Negative self-test.** Run once, in scratch (never the data store), on a copy of one A1 file. The intact copy must pass and a deliberately corrupted copy (one byte changed) must halt. Recorded as a PRV self-test, part of the E2 gate.

**14.3 Dynamic range (replaces the D.5 clause "lead distributions separate at planted L differences of 50 steps").**
- **Reason.** A lead cannot exceed the scan window (128 steps per-step; 1,280 steps on grid 10). At the frozen L = 150 and 200 steps, every detector that catches the ramp saturates at the window, so separation there cannot be measured.
- **Cells.** Linear ramps at A = 6 (× stationary SD), across the φ_y grid, 200 replicates each.
  - **Per-step:** L ∈ {25, 75, 125} observations, 20 events, scan 128.
  - **Grid 10:** L ∈ {25, 75, 125} grid observations (250, 750, 1,250 steps), on the 13.1 construction (19a–19d), with leads in steps.
- **Pass, per φ_y and grid, over the pairs (25, 75) and (75, 125).** For each detector that detects ≥ 80 % of events at both L of a pair, the 10th–90th-percentile ranges of the per-replicate mean lead must not overlap between L and L + 50.
  - **No vacuous pass:** the cell fails unless D_div and at least one baseline meet the ≥ 80 % detection condition at both L of every pair.
- **Seeds.** A measurement run on calibration seeds (reported, exploratory) precedes the graded run on fresh disjoint evaluation seeds.
- Reference agreement (8.1) applies to these cells. The cluster and ties parts of the dynamic-range clause stand as committed (DECISIONS entry 31).

**Unchanged.** Every rule applied to real data, and every other D.5 criterion as amended through Amendment 13.

=== PART 2: The frozen text they modify (prereg-v1) ===

# DESIGN — Measurement-Lag Instability in Adaptive Optimizers

Dated 2026-10-30. **Status: FROZEN at the `prereg-v1` commit (2026-10-30); before it, a pre-freeze integrated specification (JAE decision 2026-10-30, Option 2).** Built from planning doc v0.5 Part 3 (planning/adam-lag-instability_planning.md, MD5 b055fc5963206e5334d8bf35c1cbca07, committed at b64c451) with Phase 0 carry-forwards 1–10 folded in; every change from v0.5 is listed in §D.9. Before the `prereg-v1` commit this file may be revised in place. **From the `prereg-v1` commit onward it is append-only: every change is a dated amendment appended below §D.9, never an edit**, with its rationale in DECISIONS.md. No amendment to §K's thresholds, windows, spike definition, or false-alarm grid is permitted after A1 is touched.

Companion files: THESIS.md (claims, falsifiers, Date station), PRIOR_ART.md (novelty gate; §4 scope of Claim A; §5 edge-of-stability distinction), DECISIONS.md (entries 1–3 with addenda).


## D.0 Governing facts and scope

- **No data has been touched.** All A1–A6 staging happens after the public `prereg-v1` commit (DECISIONS entry 1). Everything below is fixed before any hashed input exists.
- **Realised β₂ of every Leg A run is 0.95** (OLMo-0424 and OLMo 2 7B/13B configs: AdamW betas [0.9, 0.95]; second-moment window W = 1/(1−β₂) = 20 steps; global clipping max_grad_norm = 1.0). Consequences: (i) Leg A tests Claim A's early warning *independent of β₂* — the detector reads the gradient norm, not the optimizer state; (ii) Claim B's mechanism is tested only on Leg B's β₂ grid (D.4), which includes 0.95; (iii) the window pair (32, 128) is longer than the optimizer's own 20-step second-moment memory, which is stated in the Methods and probed by E4.
- **Scope of Claim A** (PRIOR_ART §4): the deployed current-versus-EMA tests (ZClip, SPAM, trainscope z-score) are fast–slow divergences with a one-step fast window. This paper's contribution is the smoothed fast window (w_f = 32, r = w_s/w_f = 4, inside the Divergence Theorem's Theorem 14 band r* in [3, 7]) motivated by the Adaptation Rate Theorem (no lead bound is claimed; THESIS A3(b)). E2 tests whether smoothing beats the raw-reading tests at matched false-alarm rate; if it does not, that is a reportable finding against Claim A.
- **Scope of Claim B** (THESIS Amendment A1): a Hessian-free, closed-form, observable-only predictor of the established second-moment lag mechanism — not a new mechanism. **Pre-freeze finding (2026-10-30, D.4.1):** The Measurement Trap's exponential-kernel boundary (Appendix A.4, EQ-5/EQ-6 — not §3.5, which the planning doc mis-cited) does not map cleanly onto Adam's second-moment loop in observable-only terms, so the D.4 fallback is applied now: Leg B carries no Claim B verdict; E6 and E7 are characterizations. THESIS.md records this as Amendment A2(d).

## D.0a Specification budget (anti-fishing disclosure, half 1)

- **Leg A:** 1 primary detector specification (D_div); 4 baselines (B1 rolling z-score, B2 fixed threshold, B3 ZClip EMA z-score, B4 CUSUM); 1 window pair (32, 128); 1 spike definition (with the pre-registered two-rung k ladder P-KLAD); 1 scan window; 1 headline false-alarm rate (1 alarm onset per 10,000 out-of-window steps, alarm held H = 32 steps) on a 4-point FA grid. Sensitivity (reported, no verdict): 2 alternate window pairs; baseline construction-pin sweeps listed in D.7; 1 alternate segment de-duplication rule; rewind events excluded (P-SEG); 2 censored-event variants (censored lead 0; censored events excluded for every detector) (P-CENS).
- **Leg B:** 1 model configuration; 1 (β₂ × LR) grid of 6 × 4 = 24 runs; 1 seed per cell + 1 replicate seed on 4 pre-specified central cells (28 runs). No verdict-bearing specification (D.4.1 fallback).
- No other specifications are planned. Any addition is a dated amendment. The number actually tried is disclosed at Phase 4 (half 2).

## D.2 Operators (Leg A)

All operators are causal (use data at or before step t only). Steps are optimizer steps.

- **Observable:** g(t) = `optim/total_grad_norm` at step t (pre-clip); y(t) = ln g(t). A non-positive or non-finite g(t) is counted (D.6 item 5) and is **not a gap**: y(t) at that step is carried forward from y(t−1) for every window and EMA, so every window length below counts steps, and steps equal observations (design review 2026-10-30, F15).
- **Loss:** L(t) = `train/CrossEntropyLoss` at step t.
- **Fast/slow averages:** simple moving averages of y over the last w_f = 32 and w_s = 128 steps (ratio 4, Divergence Theorem Thm 14 band). Sensitivity pairs (16, 64) and (64, 256), reported, no verdict.
- **Divergence:** D(t) = SMA_32(y)(t) − SMA_128(y)(t).
- **Gaps and state (design review 2026-10-30, F15):** a gap is a run of steps present in no segment (D.1). At each gap every window statistic (D, the spike baseline, B1), the B3 EMA state (re-initialized from the first 25 post-gap steps), the B4 accumulator and its median/MAD history, and the D_div percentile history reset; the 1,000-step minimum history applies again from the first post-gap step. Nothing else resets state.
- **Detector score D_div:** P_D(t) = empirical percentile of D(t) among all D(s), s ≤ t, since the last gap (F15); minimum history 1,000 steps (no score before). Alarm when P_D(t) ≥ θ_div.
- **Persistence-sign prediction (E1, fixed before any correlation is computed):** predicted sign of Corr(D_t, y_{t+16}) = sign[R̄(h, h+w_f) − R̄(h+w_f, h+w_s)] at h = 16 (The Divergence Theorem, Theorem 8b, eq. 63), with R̄(a, b) = (1/(b−a))∫ₐᵇ ρ_Y(τ)dτ (Definition 13, eq. 61). Discrete estimate: R̄(a, b) = mean of the sample ACF ρ̂_y(τ) over integer lags τ = a … b inclusive; ρ̂_y is computed on A1's assembled y at lags 0–256, each lag using all step pairs that do not cross a gap. Expected: positive. Scope: Theorem 8b assumes weak stationarity; y has a slow upward drift on OLMo-0424 (OLMo 2 paper §3), so E1 is labelled a consistency check under an approximate-stationarity condition.
- **Spike definition (mechanical):** a loss spike at step t if L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), where SMA_128(L) and σ_128(L) are computed over the finite values of L in the trailing 128 steps; a NaN/inf L(t) counts as exceeding the threshold and is excluded from later baselines. **Dedup (chained) (design review 2026-10-30, F18):** a spike is merged into the current event if it lies within 200 steps of the most recently merged spike; the event time t_e is the first step of the event (dedup 200, frozen 2026-10-30).
- **k ladder (construction pin P-KLAD, JAE 2026-10-30):** k = 4 is the primary rung (frozen 2026-10-30). The number of eligible events on A1 is computed from the loss series and the eligibility rule alone, BEFORE any detector score is computed. If A1 has fewer than 5 eligible events at k = 4, the secondary rung k = 3 applies, once. If A1 still has fewer than 5 eligible events at k = 3, the outcome is INSUFFICIENT EVENTS (D.3 E2, §K). The rung that resolves on A1 is used for every Leg A run and for E8, and the paper reports which rung resolved. No other k is ever used.
- **Baselines** (each produces a scalar score s_b(t); alarm when s_b(t) ≥ θ_b):
  - **B1 rolling z-score:** s_1(t) = (y(t) − mean_50(y)) / sd_50(y), trailing 50-step window. Window 50 is a **construction pin P-B1** (not attributed to any tool); sweep {25, 50, 100}, reported, no verdict.
  - **B2 fixed threshold:** s_2(t) = y(t).
  - **B3 ZClip EMA z-score (documented defaults, ZClip arXiv 2504.02507 / PyPI `zclip`):** on g (not y), EMA mean μ_t and EMA variance v_t with α = 0.97, initialized from the first 25 steps of the series and of each post-gap restart (documented warm-up); s_3(t) = (g(t) − μ_{t−1}) / sqrt(v_{t−1}). Statistics are updated with the raw g(t) (monitor mode, no clipping) — **construction pin P-B3**; sweep: update with ZClip's adjusted value instead, reported, no verdict. The documented decision threshold z = 2.5 is also reported as an un-matched operating point.
  - **B4 CUSUM (trainscope 1.10.0 default `ChangePointDetector`, source kaelvalen/trainscope @ 0651b25):** robust z(t) = (y(t) − median_200(y)) / (1.4826·MAD_200(y)) over the trailing 200 observations, minimum 30 observations; positive accumulator S⁺(t) = max(0, S⁺(t−1) + z(t) − k) with slack k = 1.0; s_4(t) = S⁺(t); accumulator reset to 0 at each alarm onset (P-HOLD) and at each gap (fix round 2026-10-30, F4). trainscope applies this to loss; here it is applied to y so every detector reads the same observable, and only the upward side is used because the target is a rise in gradient norm — **construction pin P-B4**; sweep: two-sided as in trainscope, and applied to g instead of y, reported, no verdict. The documented decision threshold h = 6.0 is also reported as an un-matched operating point.
- **Alarm onset and hold (P-HOLD; fix round 2026-10-30, N1, JAE decision fix (a)):** an alarm onset occurs at step t when the detector is not already in alarm, its score s(t) ≥ θ, and s(t−1) < θ (the first scored step of the series and of each post-gap restart counts as preceded by s < θ). Each onset puts the detector in alarm for exactly H = 32 steps, [t, t + H − 1]; no further onset is counted while in alarm; at t + H the detector leaves alarm unless a new onset (a fresh crossing from below) occurs there. A score that stays ≥ θ therefore produces one onset and H alarm steps, not a standing alarm. Lead and censoring (below) are computed on this alarm state. **Residual onset clustering (stated for the Methods; fix round 2, N1 note i):** matched onset counts equalise the expected number of alarm steps per scan window across detectors, but detectors whose onsets cluster differently still differ at second order in the chance of at least one alarm step in a window; the D.5 planted null with unequal alarm memory measures this, so it is bounded, and its measured false-REFUTE and false-SUPPORT rates are reported. No rule change.
- **False-alarm rate (onset count with hold; fix round 2026-10-30, N1; replaces the duty-cycle definition of the first review round):** FA = alarm onsets on out-of-window scored steps per 10,000 out-of-window scored steps, where N_out is the number of scored steps outside every event scan window — the scan windows of ALL events, eligible or not, are excluded from both count and denominator (F18). **FA grid:** {0.5, 1, 2, 5} per 10,000; **headline FA = 1 per 10,000**. Because every onset holds for H steps, matching the onset count also matches the realised duty cycle n*·H/N_out across detectors; it is reported.
- **Threshold matching (construction pin P-FA; F4; fix round 2026-10-30, N1):** for each detector and FA target, n* = round(FA_target × N_out / 10,000). The candidate thresholds are the distinct score values on out-of-window scored steps. For each candidate v the detector's score path and alarm state are recomputed (B4's path depends on v through its reset) and the out-of-window onset count c(v) is taken; θ = the smallest candidate v with c(v) ≤ n*. Every detector is thus matched at the same integer onset count n* except where ties or non-monotone regions of c(v) make the count fall below n*; the realised count, any shortfall, and any non-monotone region are reported per detector.
- **Scan window and lead (P-MISS, P-CENS; F1, F2):** for an event at t_e the scan window is [t_e − 128, t_e]. A detector's lead = t_e − (first step in the window at which it is in alarm). If it is already in alarm at t_e − 128 (and at t_e − 129), the event is **left-censored** for that detector: lead = 128, flagged censored. A detector with no alarm step in the window has lead 0 (miss). Per detector the paper reports: mean lead (the contrast statistic), median lead, detection rate, miss count and censored count. Sensitivity (E4): censored lead = 0; censored events excluded for every detector. **Meaning of P-CENS under P-HOLD (stated for the Methods; fix round 2, N1 note ii):** because alarm state is an onset held for H = 32 steps, "already in alarm at t_e − 128" means an onset in [t_e − 160, t_e − 129]; such an onset 129–160 steps ahead is awarded lead 128. Its rate is equalised across detectors by the matched onset count, and the censored-lead-0 sensitivity covers it. No rule change.
- **Event eligibility:** an event is eligible if every detector has a defined score over its whole scan window (at least 1,000 steps of post-gap history and no gap inside the window). Ineligible events are counted and reported; their scan windows are still excluded from the FA count (F18).
- **Control (E5; F6):** circular-shift null on D_div's alarm-state series (uniform random offset in [1,000, N − 1,000] steps, 1,000 draws), which keeps alarm density and clustering and breaks alignment with the real events; plus a 128-step block shuffle of y, reported as a second characterization.
- **Deseasonalization:** none (training-step series have no seasonal component). **Subsampling:** none — every logged step is used.

## D.3.0 Experiment index

| id | Leg | One-line purpose |
|---|---|---|
| E1 | A | Check that the sign of D's forward correlation with the gradient norm matches the Divergence Theorem's a-priori sign on A1. |
| E2 | A | Test whether D_div warns of loss spikes earlier than the best of four deployed-style baselines at matched false-alarm rate on A1 (primary; carries §K). |
| E3 | A | Replicate E2's direction on the other public runs (A2–A6). |
| E4 | A | Show how E2's contrast moves with window pair and construction pins (no verdict). |
| E5 | A | Test whether D_div's alarms are aligned with the real events beyond what a circularly shifted copy of the same alarm series achieves. |
| §K | A | Pre-registered stop rule on E2 with its grading day: KILL, close on INSUFFICIENT EVENTS, or proceed to Leg B. |
| E6 | B | Characterize spike rate across the β₂ × LR grid (runs only if §K does not stop the project; verdict withdrawn by D.4.1). |
| E7 | B | Characterize how well the A.4 robustness index b_g*(exp) orders spike rate within each LR. |
| E8 | B | Characterize E2's statistics on the Leg B runs (no label). |

## D.3.1 Classification and report form (Standard v1.9.7)

| id | Primary type (of the eleven) | Report form | Rule polarity / what a null means |
|---|---|---|---|
| E1 | hypothesis test (sign; consistency check on the Divergence Theorem) | CONSISTENT / INCONSISTENT / INDETERMINATE (F12) | Sign match with one-sided permutation p ≤ 0.05 = CONSISTENT; significant opposite sign = INCONSISTENT; otherwise (incl. a true null, or a zero predicted criterion) INDETERMINATE. E1 bears on Theorem 8b's sign prediction, not on Claim A, and is never counted as support for Claim A. |
| E2 | comparative / benchmark | four-way verdict: SUPPORT / INCONCLUSIVE / REFUTE / INSUFFICIENT EVENTS (D.3) | C_min ≤ 0 = REFUTE = §K KILL; fewer than 5 eligible events at both k rungs = INSUFFICIENT EVENTS (no verdict on Claim A); severity measured by the suite at the realised event count. |
| E3 | replication | SUPPORT / REFUTE / INCONCLUSIVE (tie) / NOT RUN | Qualifying run = ≥ 3 eligible events. Fewer than 3 qualifying runs, or E2 INSUFFICIENT EVENTS → NOT RUN (all runs descriptive). |
| E4 | robustness / sensitivity | no standalone verdict; qualifies E2 ("robust to X, sensitive to Y") | Never scored as a hypothesis test. |
| E5 | boundary-condition (alignment control) | characterization + flag | Expected: the real advance-ordering rate exceeds the 95th percentile of the circularly shifted distribution. The flag trips if it does not; the flag is reported as a characterization of the shift null, not as a verdict on Claim A (F14). |
| §K | decision rule on E2 (not an experiment) | STOP / CLOSE / PROCEED | REFUTE → STOP (null note); INSUFFICIENT EVENTS → CLOSE (null note on event count); SUPPORT or INCONCLUSIVE → PROCEED to Leg B. |
| E6 | descriptive / structural characterization | characterization (table + spike rate by β₂ and LR + Spearman vs b_g*(exp) with permutation interval); resolution stated from the suite's noise span (D.4.2) | No pass/fail (D.4.1 fallback). |
| E7 | descriptive characterization (ranking) | characterization (Kendall τ within each LR with permutation interval; planted-ties probe result) | No pass/fail. |
| E8 | descriptive characterization (F13, JAE) | characterization: E2's statistics on pooled Leg B events, cluster bootstrap over runs, no label | No pass/fail; does not feed §K and does not combine with E2. |

## D.3 Experiments (Leg A) — classification, severity, report form

- **E1 — Persistence-sign check on A1.** Type: hypothesis test (sign), labelled a consistency check (F12). Rule (outcome partition): **CONSISTENT** if the realised sign of Corr(D_t, y_{t+16}) equals the D.2 predicted sign AND the one-sided block-permutation p ≤ 0.05 in the predicted direction; **INCONSISTENT** if the realised sign is opposite AND the one-sided block-permutation p ≤ 0.05 in that opposite direction; **INDETERMINATE** otherwise, including when the predicted criterion R̄(h, h+w_f) − R̄(h+w_f, h+w_s) is exactly 0 (no prediction). Report: label + ρ with block-permutation z (1,000 permutations of 128-step blocks of y). Severity: near-identity on persistent y. E1 is not counted as support for Claim A.
- **E2 — Lead-time comparison on A1 (PRIMARY; carries §K).** Type: comparative/benchmark (verdict). Statistic (F1): for each baseline b, C_b = mean lead(D_div) − mean lead(B_b) over the eligible events, all at headline FA (1 onset per 10,000 out-of-window steps, hold H = 32), with misses entered as 0 and censored events as 128 (D.2); C_min = min over b in {1, 2, 3, 4} of C_b. The verdict is taken on the point estimate C_min over all eligible events; the resampled distribution separates SUPPORT from INCONCLUSIVE (F11). Uncertainty: 1,000 joint resamples of eligible events, each drawn with replacement (events are ≥ 200 steps apart and treated as independent; sensitivity: resampling blocks of 3 consecutive events, reported in E4); every detector's lead is taken on the same resampled events; C_min is computed **within each resample** (per-resample minimum contrast, Standard v1.9.11), never by comparing marginal intervals. Outcome partition (every result maps to exactly one label):
  - **SUPPORT:** C_min > 0 and the 5th percentile of the resampled C_min > 0 (90 % two-sided interval excludes zero).
  - **INCONCLUSIVE:** C_min > 0 but the 5th percentile ≤ 0; reported with the measured detection probability at the observed effect (Standard v1.9.11). Leg B proceeds.
  - **REFUTE (= §K KILL):** point-estimate C_min ≤ 0.
  - **INSUFFICIENT EVENTS:** fewer than 5 eligible events on A1 at both rungs of the k ladder (P-KLAD) → no verdict on Claim A (neither SUPPORT nor REFUTE); reported with the event count at each rung and the suite's power at that count; §K closes the project.
  Also reported: per detector, the mean and median lead with detection rate, miss count and censored count beside them; the k-ladder rung that resolved; rewind-event count; lead distributions; the full FA-grid frontier per detector (figure); and the per-resample argmax probability over {D_div, B1, B2, B3, B4}. If every detector's detection rate at headline FA is ≤ 50 %, that is stated in the result together with the suite's measured false-support rate at that detection rate (D.5) (F1). Severity: quantified by the synthetic suite (D.5) at the realised event count.
- **E3 — Replication on A2–A6 (F7).** Type: replication (verdict). E3 runs whenever E2 returns SUPPORT, INCONCLUSIVE or REFUTE; it returns NOT RUN on E2 INSUFFICIENT EVENTS. It replicates the direction of Claim A, not E2's label: same statistic as E2 (C_min of mean leads at headline FA). Qualifying run = a run with ≥ 3 eligible events. Rule: if fewer than 3 runs qualify → NOT RUN, all runs reported descriptively; otherwise SUPPORT if a strict majority of qualifying runs have C_min > 0, REFUTE if a strict majority have C_min ≤ 0 (C_min = 0 counts as not > 0), INCONCLUSIVE on a tie. A2/A3 are stabilized runs and may have few events; that is reported, not repaired.
- **E4 — Sensitivity.** Type: robustness (no verdict; qualifies E2). Window pairs (16, 64), (64, 256); construction-pin sweeps P-B1, P-B3, P-B4, P-SEG (keep-earlier; rewind events excluded); P-CENS variants (censored lead 0; censored events excluded for every detector); event-block resampling. Every sensitivity variant re-matches all thresholds to the same FA targets.
- **E5 — Alignment control (F6, F14).** Type: boundary/characterization (report form). Procedure: shift D_div's real alarm-state series circularly by a uniform random offset in [1,000, N − 1,000] steps (1,000 draws; offsets drawn from the registered RNG, D.7 P-RNG), keeping its alarm density and clustering; recompute the advance-ordering rate (share of eligible events with lead > 0) and the mean lead against the real events. Reporting commitment: real vs shifted advance-ordering rate and mean lead (median and 90 % range over draws). The flag trips if the real advance-ordering rate ≤ the 95th percentile of the shifted distribution; a tripped flag is reported as a characterization of the shift null and discussed in the Methods. Second characterization, no flag: D_div's mean lead and advance-ordering rate after a 128-step block shuffle of y with the threshold re-matched to headline FA on each shuffled series.

### §K — Kill rule (pre-registered)

**Grading day:** `prereg-v1` commit date + 21 days. The concrete calendar date is written here and in THESIS.md's Date station in the `prereg-v1` commit itself: **2026-11-20** (`prereg-v1` commit dated 2026-10-30). On that day the verdict is recorded in DECISIONS.md and RECORD.md whether or not E2 has run; an unrun E2 (including A1 unavailable under D.1) is itself recorded and the day is re-set once, by dated amendment. If E2 is still unrun on the re-set day, §K returns CLOSE with a short null note on data availability (F11).

**Rule:** after E2's single real run on A1: if E2 is **REFUTE (C_min ≤ 0)** — D_div's mean lead at headline FA (1 onset per 10,000 out-of-window steps, hold H = 32) does not exceed that of the best of B1–B4 (point estimate) — the project STOPS. The negative is written up as a short null note (Standard: the null is the paper), filed in the repo and on Zenodo, with RECORD.md as the closing artifact; Leg B does not run. If E2 is **INSUFFICIENT EVENTS** (fewer than 5 eligible events on A1 at k = 4 and at k = 3), the project also closes: a short null note on event count is filed (neither a pass nor a kill of Claim A), with RECORD.md, and Leg B does not run. INCONCLUSIVE or SUPPORT → Leg B proceeds. No re-tuning of windows, spike definition, baselines, construction pins, or FA grid after A1 is touched; E4's sensitivity results are reported as they fall and do not rescue the verdict.

## D.5 Synthetic validation suite (committed and ALL PASS before any hashed-data run)

- **Grid and pass criteria (F16).** Synthetic y(t) = AR(1) with φ_y ∈ {0.5, 0.8, 0.9, 0.95, 0.98}; 200 replicates per cell; all RNG per D.7 P-RNG. **Oracle (F10; fix round 2026-10-30, N2):** for each replicate, every detector's θ is matched on the noisy planted series by P-FA; that θ is then applied to the oracle series — the same planted series (same ramps, same events) with the noise amplitude scaled by 10⁻³, not zero, so every detector's score is finite (fix round 2, N4) — to obtain the oracle leads and the oracle C_min. The suite asserts that every detector's score is finite at every scored step of every oracle series; a non-finite score fails the cell. A cell passes if, comparing the noisy-series result to this oracle, |recovered mean lead − oracle mean lead| ≤ 8 steps for every detector and the recovered C_min has the oracle's sign in ≥ 95 % of replicates. verify.py tolerance for deterministic quantities: 1e-6 relative.
- Planted effect: spikes preceded by ramps of length L ∈ {64, 100, 150, 200} steps; the whole pipeline (assembly → detectors B1–B4 and D_div → onset-count threshold matching with hold → leads → C_min → rule) must meet the pass criteria above.
- Planted null: spikes with NO precursor ramp; D_div must not beat the best baseline (false-support rate ≤ 0.05 at the realised event count), including cells where every detector's detection rate at headline FA is between 30 % and 50 % (F1).
- Planted null with unequal alarm memory (fix round 2026-10-30, N1): spikes with no precursor ramp; two synthetic baselines whose raw alarm runs last 1 step and 40 steps respectively, matched with D_div at the same FA by P-FA; across 200 replicates per φ_y cell the rule's false-REFUTE rate and false-SUPPORT rate must each be ≤ 0.05.
- Planted decision flip: ramps shorter than the raw-reading baselines' response; the rule must return REFUTE.
- Dynamic range: lead distributions separate at planted L differences of 50 steps; a planted-ties probe for C_min; a planted-cluster probe (spikes 200–400 steps apart) exercising left-censoring (P-CENS) and chained dedup.
- k ladder: the suite exercises both rungs (k = 4 and k = 3) and the INSUFFICIENT EVENTS branch, and confirms the event count is computed before any detector score.
- Regime span (Standard v1.9.11): event counts {5, 10, 20, 40} × the φ_y grid above; the run reports which cell the realised A1 data lands in. If A1's realised φ̂_y falls outside [0.5, 0.98], the grid is extended by the next value in {0.3, 0.99} by dated amendment before any INCONCLUSIVE is interpreted.
- Alignment control (E5): the flag must trip on planted precursor-free spikes and must not trip at planted L = 100.
- Assembly probes: overlapping segments with a superseded tail containing a spike (rewind event), gaps, duplicate steps, a dropped non-finite g, a missing `optim/total_grad_norm` column, and a point-sampled (incomplete) segment — each must be handled as D.1/D.2 state.
- Leg B: synthetic AR(1) g² with known φ at gradient-noise levels spanning the GPT-2 reference batch to beyond the 98k-token level (D.4.2); the pipeline must recover planted spike-rate differences between cells and a planted ordering against b_g\*(exp) in which the planted φ values reorder at least two cells per LR column relative to β₂ (F9); planted-ties probe for E7; divergence probes (NaN, and a sustained +2.0-nat excursion) for P-DIV; the run reports which noise cell the realised Leg B data lands in.
- Broken fixture: verify.py must fail on a corrupted hash, an out-of-tolerance value, and an unsigned CIC flag.

## D.7 Construction-pin register

| Pin | Value | Sensitivity (reported, no verdict) |
|---|---|---|
| P-SEG | later segment wins on overlapping steps; no window crosses a gap; rewind events retained on their own segment (D.1) | keep-earlier; rewind events excluded |
| P-B1 | rolling window 50 | {25, 50, 100} |
| P-B3 | ZClip statistics updated with raw g (monitor mode) | update with ZClip's adjusted value |
| P-B4 | CUSUM upward side only, on y | two-sided; on g |
| P-FA | onset-count FA with hold; n* = round(FA × N_out / 10,000); θ = smallest candidate with out-of-window onset count ≤ n*, path recomputed per candidate | — (reported FA grid; realised counts, shortfalls, non-monotone regions and duty cycle n*·H/N_out reported) |
| P-MISS | missed event has lead 0; contrast on mean lead | median lead, detection rate, miss count reported beside each mean |
| P-CENS | alarm already on at t_e − 128 → lead 128, flagged censored | censored lead 0; censored events excluded for every detector |
| P-HOLD | each alarm onset holds the detector in alarm for H = 32 steps; onsets require a crossing from below; B4 resets at each onset | — |
| P-KLAD | spike k ladder: k = 4 primary; k = 3 once if < 5 eligible A1 events (counted before any detector score); < 5 at k = 3 → INSUFFICIENT EVENTS | rung that resolved reported |
| P-PHI | WITHDRAWN 2026-10-30 (D.4.1: D.4.0 moot) | — |
| P-BG | WITHDRAWN 2026-10-30 (D.4.1: no observable-only gain) | — |
| P-REP | replicate seeds at β₂ in {0.99, 0.995} × LR in {6e-4, 1.2e-3} | — (pre-specified) |
| P-DATA | FineWeb-Edu sample-10BT @ 87f09149…, shard 000 (+001 reserve), fixed token order, GPT-2 BPE | — (fixed identifiers; on-disk SHA-256 must match at staging) |
| P-BATCH | 96 × 1,024 = 98,304 tokens/step, constant across cells | none — budget (reason in D.4); threat to resolution stated in D.4.2; suite spans the noise level |
| P-DIV | Leg B divergence: NaN/inf loss, or loss > running minimum + 2.0 nats for 50 consecutive steps; analysis stops there | — |
| P-PHIHAT | φ̂ = lag-1 ACF of ln g² minus its trailing 128-step mean, steps 1,128–5,000 | raw-level φ̂ of g², steps 1,000–5,000 |
| P-RNG | every resample, permutation, shift and suite draw uses numpy `default_rng(20261030)`; Leg B seeds 1–24 (primary) and 101–104 (P-REP) | — |

Frozen (not pins): k = 4 as the primary rung of P-KLAD; spike dedup 200 steps; headline FA = 1 alarm onset per 10,000 out-of-window steps with hold H = 32 (fix round 2026-10-30; the first round's duty-cycle headline is withdrawn); windows (32, 128); scan window 128; minimum history 1,000 steps.

=== PART 3: Suite findings S-1 to S-6, with their evidence (verbatim) ===

## S-1 (BLOCKER) — the frozen oracle lead criterion cannot be met by the normalised detectors

**Frozen text (D.5, fix rounds N2/N4; restated in A1.7).** For each replicate, θ is matched on the noisy planted series by P-FA. That θ is then applied to the same planted series with the noise scaled by 10⁻³ (the oracle). A cell passes if |recovered mean lead − oracle mean lead| ≤ 8 steps for **every detector**, and the recovered C_min has the oracle's sign in ≥ 95 % of replicates.

**Finding.** Scaling the noise by 10⁻³ while keeping the ramp unchanged makes the ramp about 1,000 noise-SDs tall for every detector that normalises by a noise estimate. θ, however, was matched on the noisy series, where it is a few noise-SDs.
- **B1 (rolling z) and B3 (ZClip z).** In the oracle these alarm at the first ramp observation, so the oracle lead is L − 1 = 99. On the noisy series their recovered mean lead is 0.5–2.5 steps.
- **B2 (raw y).** θ matched on the noisy series sits above the noise-free ramp peak, so the oracle lead is 0. On the noisy series the ramp plus the noise does cross θ, giving a recovered lead of 11–38 steps.
- **D_div and B4.** These are closer, but still outside 8 steps in many replicates.
- The gap is the effect of noise on these detectors, not a pipeline error. The noise-free oracle is not the noisy pipeline's target, so no correct pipeline can meet the criterion for B1, B2 and B3.

**Evidence** (`scripts/tests/probe_oracle_criterion.py`; outputs in `scripts/outputs/probe_oracle_criterion_*.txt`). Setup: 20,000 per-step observations, 10 events, L = 100, P-FA top scan at headline FA, n* = 2.

| Cell | | D_div | B1 | B2 | B3 | B4 |
|---|---|---|---|---|---|---|
| A = 2, φ = 0.9, 8 reps | recovered mean lead | 6.9 | 2.5 | 11.0 | 1.4 | 9.7 |
| | oracle mean lead | 12.6 | 99.0 | 0.0 | 99.0 | 9.8 |
| | replicates with \|diff\| ≤ 8 | 0.62 | 0 | 0.38 | 0 | 0.75 |
| A = 3, φ = 0.5, 5 reps | recovered mean lead | 29.8 | 0.5 | 37.6 | 6.4 | 48.0 |
| | oracle mean lead | 31.4 | 99.0 | 0.0 | 99.0 | 9.9 |
| | replicates with \|diff\| ≤ 8 | 1.0 | 0 | 0 | 0 | 0 |

**Severity: BLOCKER.** D.5 must be "committed and ALL PASS before any hashed-data run". As frozen, the planted-effect cells (and the A1.7 ten-step grid cell) cannot pass, so no hashed-data run could ever happen. As with entry 17, the rule decides the outcome independently of the data. The design review (F10, N2, N4) adopted this oracle and the 10⁻³ scaling without testing it on the normalised detectors.

**Options (for JAE).**
1. **Reference-implementation oracle.** The oracle is an independent, plain per-observation re-implementation of the whole chain (scores → top-scan matching → hold → leads → C_min), written separately from `analysis/`, run on the **same noisy series**.
   - Pass: identical θ, onsets and leads for every detector (tolerance 1e-6), and the identical C_min sign in 100 % of replicates.
   - What it tests: that the pipeline computes what the design says. Every other D.5 criterion is kept (nulls, unequal memory, decision flip, dynamic range).
   - The planted-effect cells also report recovered leads and the rule's outcome rates per cell as power, with no pass threshold.
2. **Monte-Carlo-expectation oracle.** The oracle lead is the mean recovered lead over a large independent replicate set (for example 2,000) of the same cell; the criterion stays |recovered − oracle| ≤ 8.
   - This tests sampling stability only, not correctness.
3. **Restrict the noise-free oracle to the detectors it fits.** Keep the 10⁻³ oracle only for D_div and B4, and apply option 1 to B1–B3.
   - This is mixed and harder to defend.
4. **Keep as frozen.** The suite then fails and E2 cannot run.

## S-2 (BLOCKER) — the unequal-memory null's "false-REFUTE ≤ 0.05" is unattainable; JAE's proposed replacement fails on a point mass at C_b = 0

**Frozen text (D.5, fix round N1).** "spikes with no precursor ramp; two synthetic baselines whose raw alarm runs last 1 step and 40 steps respectively, matched with D_div at the same FA by P-FA; across 200 replicates per φ_y cell the rule's false-REFUTE rate and false-SUPPORT rate must each be ≤ 0.05."

**Measurement (item 17; DECISIONS entry 20).**
- Setup: Amendment 9.3(16) construction (S₁ = y, S₄₀ = 40-observation rolling max), `scripts/suite/umem.py`, 200 replicates per φ_y, 50,000 observations, 20 events, headline FA (n* = 5).
- Seeds: SeedSequence children 20,000,000+ (per φ: +0, +1,000, +2,000, +3,000, +4,000), disjoint from every evaluation and calibration range.
- Outputs: `scripts/outputs/item17_umem_phi*.jsonl`.

| φ_y | false-REFUTE | false-SUPPORT | INCONCLUSIVE | median C_S1, C_S40 | P(C_b > 0): S1, S40 | P(C_b = 0): S1, S40 | P(C_b > 0 \| C_b ≠ 0): S1, S40 | share of reps with \|C_S1 − C_S40\| ≤ 1 |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 0.735 | 0.000 | 0.265 | 0, 0 | 0.265, 0.265 | 0.490, 0.480 | 0.520, 0.510 | 0.980 |
| 0.8 | 0.755 | 0.000 | 0.245 | 0, 0 | 0.245, 0.245 | 0.570, 0.570 | 0.570, 0.570 | 1.000 |
| 0.9 | 0.770 | 0.000 | 0.230 | 0, 0 | 0.230, 0.230 | 0.465, 0.470 | 0.430, 0.434 | 0.990 |
| 0.95 | 0.800 | 0.000 | 0.200 | 0, 0 | 0.200, 0.205 | 0.580, 0.580 | 0.476, 0.488 | 0.995 |
| 0.98 | 0.800 | 0.005 | 0.195 | 0, 0 | 0.205, 0.200 | 0.510, 0.505 | 0.418, 0.404 | 0.970 |

Mean leads under the null are 1.2–1.7 steps for every detector.

**Findings.**
1. **False-REFUTE is 0.735–0.800 in every cell, so "≤ 0.05" is unattainable**, as JAE expected. Under a no-precursor null, C_min is the minimum of two near-zero contrasts, so it is ≤ 0 in most replicates. REFUTE is the correct outcome there, not an error.
2. **JAE's proposed replacement also fails as written.** |median C_b| ≤ 1 holds (the median is 0 everywhere), but P(C_b > 0) ∈ [0.40, 0.60] does not (0.20–0.27). The cause:
   - Detection under the null is rare, so 46–58 % of replicates have every lead equal to 0 and C_b exactly 0.
   - Conditional on C_b ≠ 0, P(C_b > 0) is 0.40–0.57 (S₄₀ at φ 0.98: 0.404).
3. **The two baselines barely differ.** |C_S1 − C_S40| ≤ 1 in 97–100 % of replicates.
   - Under P-HOLD, the alarm state is the H = 32 hold after a fresh crossing, not "score ≥ θ". S₄₀'s longer raw exceedance run therefore never reaches the alarm state.
   - S₄₀ crosses θ when y first crosses θ, unless y was already above θ within the previous 40 observations.
   - So the cell measures the invariance that the N1 fix built in, not a memory-driven bias.

**Severity: BLOCKER.** D.5 cannot be ALL PASS with the frozen criterion. As with S-1, the criterion was set at the fix round (N1) without being measured.

**Options (for JAE).**
1. **Invariance criterion** (states what the cell actually tests). For each φ_y cell:
   - (a) false-SUPPORT ≤ 0.05;
   - (b) |median C_b| ≤ 1 observation for each b;
   - (c) |C_S1 − C_S40| ≤ 1 observation in ≥ 95 % of replicates (measured 0.970–1.000).
2. **JAE's replacement, conditioned on C_b ≠ 0.**
   - Keep (a) false-SUPPORT ≤ 0.05 and (b) |median C_b| ≤ 1.
   - Replace P(C_b > 0) ∈ [0.40, 0.60] with P(C_b > 0 | C_b ≠ 0) ∈ [0.40, 0.60]. Measured 0.404–0.570; the S₄₀ φ 0.98 cell passes by 0.004, so this is fragile at n ≈ 100 non-zero replicates.
   - Also report the share of replicates with C_b = 0.
3. **Options 1 and 2 together.**
- In every option, false-REFUTE is reported and not required.

## S-3 (BLOCKER for one D.5 cell) — no single pulse height puts every detector's detection rate in 30–50 %

**Frozen text (D.5, F1).** The planted null must include "cells where every detector's detection rate at headline FA is between 30 % and 50 %". The construction is Amendment 8.2(13): a one-observation pulse of height h at a uniform offset in [1, scan] before each event, with h calibrated per φ_y.

**Measurement (2026-11-06; calibration seeds 10,000,000+, disjoint from evaluation; φ_y = 0.9; 50,000 obs; 20 events; headline FA).**

*Pulse*, `scripts/suite/probe_null3050_pulse.py`, 8 replicates → `scripts/outputs/s3_pulse_phi0.9.txt`:

| h | D_div | B1 | B2 | B3 | B4 |
|---|---|---|---|---|---|
| 3 | 0.013 | 0.381 | 0.331 | 0.613 | 0.025 |
| 6 | 0.013 | 0.956 | 1.000 | 1.000 | 0.025 |
| 10 | 0.025 | 1.000 | 1.000 | 1.000 | 0.050 |
| 20 | 0.044 | 1.000 | 1.000 | 1.000 | 0.087 |

- D_div averages over 32 and 128 observations, so a single observation barely moves it.
- B4's CUSUM resets and its median/MAD baseline absorb the pulse.
- The raw-reading detectors saturate by h = 6.
- **The construction is infeasible by mechanism**, not by tuning: no h gives all five detectors 30–50 %.

*Alternative: step of height h from a uniform offset in [1, scan] through t_e*, `scripts/suite/probe_null3050_step.py`, 6 replicates → `scripts/outputs/s3_step_phi0.9.txt`:

| h | D_div | B1 | B2 | B3 | B4 | mean lead D_div / B1 / B2 / B3 / B4 |
|---|---|---|---|---|---|---|
| 1.5 | 0.24 | 0.09 | 0.31 | 0.20 | 0.27 | 10.8 / 6.8 / 14.7 / 14.4 / 11.9 |
| 2.5 | 0.67 | 0.28 | 0.76 | 0.51 | 0.67 | 33.3 / 17.6 / 41.1 / 32.7 / 33.4 |

- All five detectors respond, but B1 (rolling z, which adapts to the step) stays well below the others.
- Interpolating, no h puts all five in 30–50 % at once. Around h ≈ 2, D_div, B2, B3 and B4 fall roughly in 0.35–0.55 while B1 sits near 0.2.
- A step is a sudden level shift, which favours the raw reading (B2 leads D_div). That is the right direction for a no-false-support null.

**Severity.** BLOCKER for this one cell: D.5 cannot be ALL PASS with it as written. Every other D.5 null criterion is unaffected.

**Options (for JAE).**
1. **Step construction with the band widened to [0.20, 0.80] for every detector.** Calibrate h per φ_y on the calibration seeds. Criterion: false-SUPPORT ≤ 0.05.
2. **Step construction with the band applied to the median detector.** The median detector's rate is calibrated into 30–50 %, and every detector's rate is reported. Criterion: false-SUPPORT ≤ 0.05.
3. **Keep the pulse construction and drop the 30–50 % requirement.** The cell becomes a reported characterization: detection rate by detector across h. The false-SUPPORT ≤ 0.05 criterion still applies at each h.

## Suite verdict run v1 (2026-11-06) — FAIL on the 15 decision-flip cells; everything else passes or is reported

Run on JAE's host at 6b5d7f5 (`run_suite.py --workers 16`, 170 cells × 200 replicates). Reference agreement on all 165 E2-chain cells: complete and identical. Single- vs multi-process identity check on cell 25: IDENTICAL. Graded by `grade_suite.py` → `verification/suite_verdict.md`.

| group | cells | result |
|---|---|---|
| planted null, surge null, t3 null, pulse-sweep null, null at 57 events | 45 | PASS; max false-SUPPORT 0.010 |
| unequal-memory null (10.1) | 5 | PASS; invariance 0.965–1.000; median C_b = 0; false-SUPPORT ≤ 0.010 (reported: false-REFUTE 0.760–0.795) |
| decision flip (20 events), t3 flip, flip at 57 events | 15 | **FAIL**: REFUTE 0.81–0.93 against ≥ 0.95; SUPPORT ≤ 0.005 |
| planted effect, regime span, surge effect, effect at 57, step | 105 | reported (see S-5) |

## S-4 (BLOCKER) — the decision flip at L = 8 cannot reach REFUTE ≥ 0.95 under the frozen lead statistic

**Mechanism** (replicates of cell 109 inspected).
- In every non-REFUTE replicate, D_div detected one event, about 5 %, through a chance alarm early in that event's 129-observation window. Its lead was about 120, giving a mean lead of about 6 over 20 events.
- The baselines' genuine detections of an 8-observation ramp can lead by at most L − 1 = 7.
- Under the frozen statistic (any in-window alarm is a lead; misses count 0), one chance D_div alarm can outweigh every baseline's genuine short leads, which makes C_min > 0 and the label INCONCLUSIVE. SUPPORT stays ≤ 0.005 because one chance alarm rarely survives resampling.

**Amplitude and length do not fix it.** Measured on child indices 40,000,000+ (never used), φ 0.9, 25 replicates, `scripts/suite/probe_flip_amplitude.py` → `scripts/outputs/s4_flip_phi0.9.txt`:

| L | A | REFUTE | INCONCLUSIVE | B2 detection |
|---|---|---|---|---|
| 8 | 5 | 0.88 | 0.12 | 0.81 |
| 8 | 8 | 0.96 | 0.04 | 1.00 |
| 8 | 12 | 0.96 | 0.04 | 1.00 |
| 16 | 6 | 0.96 | 0.04 | 0.99 |

The chance-alarm floor stays. Twenty-five replicates cannot resolve 0.95.

**Options (for JAE).**
1. **Longer, taller short ramp.** L ∈ {16, 24} (still shorter than w_f = 32) and A calibrated on calibration seeds so the best raw baseline detects ≥ 90 %. Graded at REFUTE ≥ 0.95 on fresh evaluation seeds, after a 200-replicate feasibility measurement.
2. **Reframe the flip as "the rule never supports when the raw reading wins".** Pass: SUPPORT ≤ 0.05 (measured ≤ 0.005); REFUTE reported. This loses the requirement that the rule actively return REFUTE.
3. **Both:** option 1's construction, with SUPPORT ≤ 0.05 as the binding criterion and REFUTE reported.

In every option the chance-alarm floor is reported as a property of the frozen statistic, because it applies to E2 on A1 as well.

## S-5 (severity record; not a pass criterion) — planted linear ramps mostly return REFUTE

The share of 200 replicates returning SUPPORT / REFUTE, planted effect at 20 events (`suite_v1`). Columns are φ_y = 0.5, 0.8, 0.9, 0.95, 0.98.

| (L, A) | 0.5 | 0.8 | 0.9 | 0.95 | 0.98 |
|---|---|---|---|---|---|
| (64, 1) | .05/.67 | .01/.78 | .00/.79 | .00/.83 | .01/.82 |
| (64, 3) | .04/.73 | .01/.80 | .00/.86 | .00/.91 | .01/.89 |
| (100, 2) | .10/.49 | .02/.79 | .01/.83 | .01/.86 | .01/.86 |
| (150, 3) | .12/.64 | .01/.95 | .00/.98 | .00/.98 | .01/.94 |
| (200, 3) | .05/.74 | .00/.99 | .00/1.00 | .00/1.00 | .00/.99 |

At A1's 57 events (L = 100, A = 2), SUPPORT / REFUTE by φ_y is:
- 0.5: .15/.55
- 0.8: .01/.79
- 0.9: .00/.92
- 0.95: .01/.91
- 0.98: .01/.85

Mean leads at 57 events and φ 0.9 are D_div 5.7, B2 8.7, B4 7.8.

**Reading.**
- On a linear ramp in y, the raw reading (B2) and the CUSUM (B4) cross their matched thresholds as early as D_div or earlier. E2 therefore returns REFUTE in most replicates, even though a precursor exists.
- The ramp is the D.5 / Amendment 7.7 planted effect. These numbers are its measured detection probability, which the Standard's severity check requires.
- What they say: under this construction, E2 has little power to return SUPPORT. A REFUTE on A1 would be consistent with both "no D_div advantage" and "a linear-ramp precursor that the raw reading catches as fast".
- §K's rule is frozen, since A1 has been touched. This record bears on how a REFUTE is interpreted and reported, not on the rule.

## S-6 (BLOCKER for the E2 gate) — dynamic range (Amendment 14.3) fails in all 10 groups

Graded run on evaluation seeds (`suite_v1`, cells 260–289), with the calibration-seed measurement run first (`scripts/outputs/dynamic_range_measure.json`, exploratory). Reference agreement is identical on every cell. The measurement predicted the graded result in every group.

**(a) Vacuous at (25, 75) in every group.** D_div's detection is below 80 % at L = 25 observations, per-step and grid-10, at every φ_y. The baselines at ≥ 80 % at both L: B2 in every group, B4 in some. Because of the no-vacuous-pass condition (JAE, Amendment 14.3), every group fails at this pair.

**(b) D_div's lead ranges overlap at (75, 125); the baselines separate.** 10th–90th percentile of the per-replicate mean lead, graded run:

| group | D_div L 75 vs L 125 | B2 L 75 vs L 125 | B4 L 75 vs L 125 |
|---|---|---|---|
| per-step φ 0.5 | [15, 48] vs [26, 82] overlap | [40, 46] vs [72, 82] sep | [47, 52] vs [83, 90] sep |
| per-step φ 0.9 | [21, 35] vs [32, 62] overlap | [34, 43] vs [63, 75] sep | [25, 35] vs [51, 67] sep |
| per-step φ 0.98 | [19, 32] vs [32, 56] overlap | [33, 42] vs [58, 71] sep | — (< 80 %) |
| grid-10 φ 0.5 (steps) | [64, 293] vs [148, 506] overlap | [402, 455] vs [719, 805] sep | [475, 523] vs [841, 892] sep |
| grid-10 φ 0.9 (steps) | [118, 296] vs [233, 532] overlap | [352, 411] vs [638, 730] sep | [263, 358] vs [558, 680] sep |

- On grid 10 at φ ≥ 0.95, D_div is below 80 % even at L = 75, so those pairs are vacuous too.
- D_div's median lead rises with L, but its replicate-to-replicate spread is several times the baselines'.

**Not a code fault.** Construction, criterion and seeds were all fixed before either run.

**Bearing.**
- The Standard's review menu flags "any saturating/tie-prone/no-dynamic-range metric" as verdict-invalid.
- As measured, D_div's lead does not resolve 50-step differences in precursor length at A = 6 × SD, while the raw-reading baselines do.
- Together with S-5, this bears on what an E2 verdict can mean.
- **Decision rule, fixed before the review (JAE):** pipeline-invalid or rescue → hold E2 and use §K's single re-set; method property → apply the bar to B2/B4 as the instrument check, and report D_div's flat lead response beside E2 as a limitation.

=== PART 4: Suite verdict (grader output, verbatim) ===

# D.5 suite verdict — statistical cells

Graded from `scripts/outputs/suite_v1` by `scripts/suite/grade_suite.py`.

**FAIL (10: ['dr_grid10 0.5', 'dr_grid10 0.8', 'dr_grid10 0.9', 'dr_grid10 0.95', 'dr_grid10 0.98', 'dr_step 0.5', 'dr_step 0.8', 'dr_step 0.9', 'dr_step 0.95', 'dr_step 0.98'])**

| cell | kind | result | verdict |
|---|---|---|---|
| licence | analysis/ops.py | unchanged since aad6cf7 | PASS |
| licence | analysis/pipeline.py | unchanged since aad6cf7 | PASS |
| licence | analysis/e2stat.py | unchanged since aad6cf7 | PASS |
| licence | reference/ref_e2.py | unchanged since aad6cf7 | PASS |
| agreement | reference agreement (8.1) on 260 E2-chain cells | complete and all identical | PASS |
| 0 | planted_effect (phi=0.5, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.050/0.280/0.670 | mean lead B1 1.6, B2 2.1, B3 1.5, B4 3.3, D_div 3.5 | REPORTED |
| 1 | planted_effect (phi=0.5, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.075/0.325/0.600 | mean lead B1 2.0, B2 6.2, B3 2.6, B4 13.0, D_div 12.6 | REPORTED |
| 2 | planted_effect (phi=0.5, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.040/0.225/0.735 | mean lead B1 2.1, B2 15.9, B3 2.9, B4 25.3, D_div 20.3 | REPORTED |
| 3 | planted_effect (phi=0.5, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.045/0.345/0.610 | mean lead B1 2.2, B2 3.5, B3 2.1, B4 6.1, D_div 6.3 | REPORTED |
| 4 | planted_effect (phi=0.5, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.100/0.410/0.490 | mean lead B1 2.1, B2 12.1, B3 3.3, B4 24.0, D_div 23.5 | REPORTED |
| 5 | planted_effect (phi=0.5, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.070/0.260/0.670 | mean lead B1 2.8, B2 29.3, B3 4.1, B4 44.1, D_div 37.3 | REPORTED |
| 6 | planted_effect (phi=0.5, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.020/0.440/0.540 | mean lead B1 1.7, B2 4.8, B3 1.9, B4 9.5, D_div 9.7 | REPORTED |
| 7 | planted_effect (phi=0.5, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.095/0.420/0.485 | mean lead B1 2.7, B2 24.9, B3 3.4, B4 37.4, D_div 37.7 | REPORTED |
| 8 | planted_effect (phi=0.5, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.125/0.240/0.635 | mean lead B1 3.6, B2 54.0, B3 5.9, B4 69.6, D_div 60.8 | REPORTED |
| 9 | planted_effect (phi=0.5, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.030/0.370/0.600 | mean lead B1 1.9, B2 8.0, B3 2.7, B4 10.8, D_div 10.7 | REPORTED |
| 10 | planted_effect (phi=0.5, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.060/0.315/0.625 | mean lead B1 2.3, B2 36.1, B3 4.1, B4 41.0, D_div 38.9 | REPORTED |
| 11 | planted_effect (phi=0.5, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.050/0.210/0.740 | mean lead B1 3.0, B2 73.2, B3 5.6, B4 79.3, D_div 66.8 | REPORTED |
| 12 | planted_effect (phi=0.8, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.015/0.210/0.775 | mean lead B1 1.6, B2 1.7, B3 1.7, B4 2.6, D_div 1.9 | REPORTED |
| 13 | planted_effect (phi=0.8, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.240/0.750 | mean lead B1 1.4, B2 5.3, B3 2.2, B4 5.9, D_div 4.9 | REPORTED |
| 14 | planted_effect (phi=0.8, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.195/0.795 | mean lead B1 1.7, B2 12.8, B3 2.6, B4 13.8, D_div 11.2 | REPORTED |
| 15 | planted_effect (phi=0.8, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.205/0.785 | mean lead B1 1.5, B2 3.2, B3 1.8, B4 4.1, D_div 3.2 | REPORTED |
| 16 | planted_effect (phi=0.8, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.020/0.195/0.785 | mean lead B1 1.9, B2 10.4, B3 2.6, B4 11.9, D_div 9.4 | REPORTED |
| 17 | planted_effect (phi=0.8, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.145/0.850 | mean lead B1 2.4, B2 25.2, B3 3.9, B4 26.7, D_div 21.2 | REPORTED |
| 18 | planted_effect (phi=0.8, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.015/0.155/0.830 | mean lead B1 2.0, B2 5.5, B3 2.6, B4 6.5, D_div 4.4 | REPORTED |
| 19 | planted_effect (phi=0.8, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.120/0.875 | mean lead B1 2.4, B2 20.2, B3 3.6, B4 19.7, D_div 14.4 | REPORTED |
| 20 | planted_effect (phi=0.8, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.045/0.950 | mean lead B1 2.8, B2 44.7, B3 4.5, B4 44.3, D_div 32.3 | REPORTED |
| 21 | planted_effect (phi=0.8, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | mean lead B1 1.9, B2 7.7, B3 3.2, B4 7.6, D_div 5.2 | REPORTED |
| 22 | planted_effect (phi=0.8, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.025/0.975 | mean lead B1 2.1, B2 31.7, B3 3.8, B4 24.0, D_div 14.7 | REPORTED |
| 23 | planted_effect (phi=0.8, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | mean lead B1 2.9, B2 63.4, B3 5.3, B4 52.5, D_div 31.3 | REPORTED |
| 24 | planted_effect (phi=0.9, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.215/0.785 | mean lead B1 1.3, B2 1.8, B3 1.4, B4 1.8, D_div 1.6 | REPORTED |
| 25 | planted_effect (phi=0.9, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.160/0.840 | mean lead B1 1.5, B2 4.7, B3 2.0, B4 4.0, D_div 3.1 | REPORTED |
| 26 | planted_effect (phi=0.9, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | mean lead B1 1.8, B2 11.2, B3 3.1, B4 7.7, D_div 6.9 | REPORTED |
| 27 | planted_effect (phi=0.9, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.185/0.810 | mean lead B1 1.6, B2 2.9, B3 2.0, B4 3.1, D_div 2.2 | REPORTED |
| 28 | planted_effect (phi=0.9, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.160/0.830 | mean lead B1 2.0, B2 8.5, B3 2.8, B4 6.5, D_div 5.7 | REPORTED |
| 29 | planted_effect (phi=0.9, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | mean lead B1 2.1, B2 21.6, B3 4.2, B4 15.7, D_div 13.4 | REPORTED |
| 30 | planted_effect (phi=0.9, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.170/0.830 | mean lead B1 2.0, B2 5.0, B3 2.3, B4 4.4, D_div 3.4 | REPORTED |
| 31 | planted_effect (phi=0.9, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | mean lead B1 2.5, B2 17.6, B3 3.9, B4 12.6, D_div 8.8 | REPORTED |
| 32 | planted_effect (phi=0.9, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | mean lead B1 3.1, B2 39.6, B3 5.5, B4 28.1, D_div 19.4 | REPORTED |
| 33 | planted_effect (phi=0.9, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.120/0.880 | mean lead B1 1.8, B2 7.1, B3 2.5, B4 5.3, D_div 3.7 | REPORTED |
| 34 | planted_effect (phi=0.9, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.030/0.970 | mean lead B1 2.6, B2 25.0, B3 3.8, B4 15.9, D_div 7.8 | REPORTED |
| 35 | planted_effect (phi=0.9, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 2.4, B2 54.9, B3 5.1, B4 34.6, D_div 18.7 | REPORTED |
| 36 | planted_effect (phi=0.95, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.165/0.835 | mean lead B1 1.6, B2 2.2, B3 1.7, B4 1.8, D_div 1.5 | REPORTED |
| 37 | planted_effect (phi=0.95, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.170/0.830 | mean lead B1 1.7, B2 4.6, B3 2.8, B4 2.6, D_div 2.9 | REPORTED |
| 38 | planted_effect (phi=0.95, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | mean lead B1 1.6, B2 10.7, B3 3.1, B4 4.8, D_div 5.5 | REPORTED |
| 39 | planted_effect (phi=0.95, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.195/0.805 | mean lead B1 1.5, B2 3.1, B3 2.3, B4 2.4, D_div 2.2 | REPORTED |
| 40 | planted_effect (phi=0.95, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | mean lead B1 1.7, B2 8.5, B3 2.4, B4 4.8, D_div 4.9 | REPORTED |
| 41 | planted_effect (phi=0.95, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | mean lead B1 2.2, B2 19.1, B3 3.9, B4 9.4, D_div 9.2 | REPORTED |
| 42 | planted_effect (phi=0.95, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | mean lead B1 1.6, B2 4.5, B3 2.2, B4 3.4, D_div 2.9 | REPORTED |
| 43 | planted_effect (phi=0.95, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.060/0.935 | mean lead B1 1.8, B2 14.3, B3 2.8, B4 8.1, D_div 5.8 | REPORTED |
| 44 | planted_effect (phi=0.95, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | mean lead B1 2.3, B2 34.6, B3 5.5, B4 16.1, D_div 13.9 | REPORTED |
| 45 | planted_effect (phi=0.95, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.110/0.890 | mean lead B1 1.6, B2 6.6, B3 2.0, B4 4.9, D_div 3.0 | REPORTED |
| 46 | planted_effect (phi=0.95, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | mean lead B1 2.6, B2 22.9, B3 4.3, B4 11.9, D_div 7.5 | REPORTED |
| 47 | planted_effect (phi=0.95, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 2.3, B2 47.3, B3 5.6, B4 22.0, D_div 12.4 | REPORTED |
| 48 | planted_effect (phi=0.98, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.170/0.820 | mean lead B1 1.3, B2 2.0, B3 1.4, B4 1.5, D_div 1.5 | REPORTED |
| 49 | planted_effect (phi=0.98, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.175/0.820 | mean lead B1 2.1, B2 4.2, B3 2.8, B4 2.3, D_div 2.9 | REPORTED |
| 50 | planted_effect (phi=0.98, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.110/0.885 | mean lead B1 1.8, B2 10.1, B3 3.8, B4 3.3, D_div 5.6 | REPORTED |
| 51 | planted_effect (phi=0.98, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.200/0.800 | mean lead B1 1.6, B2 2.9, B3 1.8, B4 2.1, D_div 2.4 | REPORTED |
| 52 | planted_effect (phi=0.98, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.130/0.860 | mean lead B1 2.2, B2 7.2, B3 3.3, B4 3.5, D_div 4.0 | REPORTED |
| 53 | planted_effect (phi=0.98, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.070/0.925 | mean lead B1 2.4, B2 17.2, B3 4.2, B4 7.0, D_div 9.0 | REPORTED |
| 54 | planted_effect (phi=0.98, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.165/0.835 | mean lead B1 1.7, B2 3.9, B3 2.4, B4 3.3, D_div 2.7 | REPORTED |
| 55 | planted_effect (phi=0.98, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.090/0.900 | mean lead B1 1.7, B2 12.9, B3 3.9, B4 5.5, D_div 5.9 | REPORTED |
| 56 | planted_effect (phi=0.98, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.050/0.945 | mean lead B1 2.4, B2 29.1, B3 5.8, B4 12.3, D_div 13.9 | REPORTED |
| 57 | planted_effect (phi=0.98, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.200/0.800 | mean lead B1 1.4, B2 5.5, B3 1.9, B4 4.2, D_div 3.6 | REPORTED |
| 58 | planted_effect (phi=0.98, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | mean lead B1 2.1, B2 18.3, B3 4.0, B4 8.5, D_div 6.9 | REPORTED |
| 59 | planted_effect (phi=0.98, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 2.1, B2 39.4, B3 5.3, B4 15.6, D_div 12.6 | REPORTED |
| 60 | regime_span (phi=0.5, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.110/0.400/0.490 | mean lead B1 2.5, B2 12.8, B3 3.2, B4 22.9, D_div 25.4 | REPORTED |
| 61 | regime_span (phi=0.5, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.120/0.455/0.425 | mean lead B1 2.4, B2 12.8, B3 3.3, B4 22.3, D_div 24.1 | REPORTED |
| 62 | regime_span (phi=0.5, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.110/0.370/0.520 | mean lead B1 1.9, B2 12.9, B3 2.5, B4 23.6, D_div 23.2 | REPORTED |
| 63 | regime_span (phi=0.5, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.190/0.305/0.505 | mean lead B1 2.0, B2 11.7, B3 2.9, B4 22.8, D_div 22.0 | REPORTED |
| 64 | regime_span (phi=0.8, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.235/0.760 | mean lead B1 2.2, B2 9.6, B3 2.9, B4 11.5, D_div 9.3 | REPORTED |
| 65 | regime_span (phi=0.8, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.020/0.245/0.735 | mean lead B1 2.0, B2 10.1, B3 2.4, B4 12.0, D_div 10.0 | REPORTED |
| 66 | regime_span (phi=0.8, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.165/0.830 | mean lead B1 1.9, B2 10.6, B3 2.9, B4 11.8, D_div 8.9 | REPORTED |
| 67 | regime_span (phi=0.8, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.220/0.775 | mean lead B1 1.5, B2 9.1, B3 2.4, B4 11.4, D_div 8.5 | REPORTED |
| 68 | regime_span (phi=0.9, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.160/0.840 | mean lead B1 1.7, B2 9.5, B3 3.2, B4 7.5, D_div 6.0 | REPORTED |
| 69 | regime_span (phi=0.9, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.160/0.830 | mean lead B1 1.6, B2 8.4, B3 2.3, B4 6.2, D_div 5.4 | REPORTED |
| 70 | regime_span (phi=0.9, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | mean lead B1 1.5, B2 8.9, B3 2.8, B4 7.2, D_div 5.8 | REPORTED |
| 71 | regime_span (phi=0.9, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.140/0.850 | mean lead B1 1.6, B2 8.5, B3 2.5, B4 6.8, D_div 5.3 | REPORTED |
| 72 | regime_span (phi=0.95, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | mean lead B1 1.6, B2 8.2, B3 2.3, B4 4.4, D_div 4.4 | REPORTED |
| 73 | regime_span (phi=0.95, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.195/0.805 | mean lead B1 1.5, B2 7.7, B3 2.3, B4 4.2, D_div 4.5 | REPORTED |
| 74 | regime_span (phi=0.95, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.145/0.850 | mean lead B1 1.9, B2 7.9, B3 3.0, B4 4.6, D_div 4.4 | REPORTED |
| 75 | regime_span (phi=0.95, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | mean lead B1 1.5, B2 7.6, B3 2.4, B4 4.3, D_div 4.3 | REPORTED |
| 76 | regime_span (phi=0.98, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.185/0.815 | mean lead B1 1.9, B2 7.6, B3 1.7, B4 4.0, D_div 4.5 | REPORTED |
| 77 | regime_span (phi=0.98, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.160/0.840 | mean lead B1 2.7, B2 7.5, B3 3.1, B4 4.0, D_div 4.3 | REPORTED |
| 78 | regime_span (phi=0.98, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.015/0.170/0.815 | mean lead B1 1.8, B2 7.9, B3 3.3, B4 4.1, D_div 5.1 | REPORTED |
| 79 | regime_span (phi=0.98, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.175/0.820 | mean lead B1 1.6, B2 7.0, B3 2.8, B4 3.8, D_div 4.3 | REPORTED |
| 80 | planted_null (phi=0.5, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.150/0.850 | PASS |
| 81 | planted_null (phi=0.8, n_events=20) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | PASS |
| 82 | planted_null (phi=0.9, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 83 | planted_null (phi=0.95, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 84 | planted_null (phi=0.98, n_events=20) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | PASS |
| 85 | surge_null (phi=0.5, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | PASS |
| 86 | surge_effect (phi=0.5, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.045/0.950 | mean lead B1 2.5, B2 8.7, B3 3.1, B4 0.6, D_div 2.8 | REPORTED |
| 87 | surge_null (phi=0.8, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 88 | surge_effect (phi=0.8, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.165/0.825 | mean lead B1 1.9, B2 8.5, B3 2.8, B4 2.2, D_div 4.2 | REPORTED |
| 89 | surge_null (phi=0.9, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | PASS |
| 90 | surge_effect (phi=0.9, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.115/0.885 | mean lead B1 2.0, B2 8.2, B3 2.7, B4 2.9, D_div 3.4 | REPORTED |
| 91 | surge_null (phi=0.95, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | PASS |
| 92 | surge_effect (phi=0.95, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.120/0.880 | mean lead B1 1.5, B2 6.9, B3 2.7, B4 2.9, D_div 3.4 | REPORTED |
| 93 | surge_null (phi=0.98, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | PASS |
| 94 | surge_effect (phi=0.98, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.150/0.850 | mean lead B1 2.3, B2 6.8, B3 2.9, B4 2.7, D_div 3.4 | REPORTED |
| 95 | t3_null (phi=0.5, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.150/0.850 | PASS |
| 96 | t3_null (phi=0.8, n_events=20, innov=t3) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | PASS |
| 97 | t3_null (phi=0.9, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 98 | t3_null (phi=0.95, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | PASS |
| 99 | t3_null (phi=0.98, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.125/0.875 | PASS |
| 115 | unequal_memory_null (phi=0.5, n_events=20) | false-SUPPORT 0.005 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 1.000 (>= 0.95); reported: false-REFUTE 0.775, P(C_b>0|C_b!=0) S1 0.511 S40 0.511; SUPPORT/INCONCL/REFUTE 0.005/0.220/0.775 | PASS |
| 116 | unequal_memory_null (phi=0.8, n_events=20) | false-SUPPORT 0.005 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 0.990 (>= 0.95); reported: false-REFUTE 0.795, P(C_b>0|C_b!=0) S1 0.471 S40 0.471; SUPPORT/INCONCL/REFUTE 0.005/0.200/0.795 | PASS |
| 117 | unequal_memory_null (phi=0.9, n_events=20) | false-SUPPORT 0.010 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 1.000 (>= 0.95); reported: false-REFUTE 0.790, P(C_b>0|C_b!=0) S1 0.467 S40 0.467; SUPPORT/INCONCL/REFUTE 0.010/0.200/0.790 | PASS |
| 118 | unequal_memory_null (phi=0.95, n_events=20) | false-SUPPORT 0.010 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 1.000 (>= 0.95); reported: false-REFUTE 0.770, P(C_b>0|C_b!=0) S1 0.517 S40 0.517; SUPPORT/INCONCL/REFUTE 0.010/0.220/0.770 | PASS |
| 119 | unequal_memory_null (phi=0.98, n_events=20) | false-SUPPORT 0.000 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 0.965 (>= 0.95); reported: false-REFUTE 0.760, P(C_b>0|C_b!=0) S1 0.551 S40 0.511; SUPPORT/INCONCL/REFUTE 0.000/0.240/0.760 | PASS |
| 120 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 121 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 122 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 123 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 124 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 125 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 126 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 127 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 128 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | PASS |
| 129 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 130 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 131 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 132 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 133 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 134 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 135 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 136 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 137 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 138 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 139 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 140 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 141 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 142 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 143 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 144 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 145 | step_characterization (phi=0.5, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.025/0.240/0.735 | mean lead B1 3.1, B2 22.6, B3 4.4, B4 42.6, D_div 37.1 | REPORTED |
| 146 | step_characterization (phi=0.5, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.030/0.970 | mean lead B1 5.7, B2 42.6, B3 9.5, B4 54.1, D_div 43.4 | REPORTED |
| 147 | step_characterization (phi=0.5, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | mean lead B1 10.8, B2 53.4, B3 15.8, B4 57.8, D_div 45.4 | REPORTED |
| 148 | step_characterization (phi=0.8, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.255/0.740 | mean lead B1 3.2, B2 19.1, B3 5.6, B4 20.9, D_div 17.8 | REPORTED |
| 149 | step_characterization (phi=0.8, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.135/0.860 | mean lead B1 5.9, B2 35.2, B3 11.1, B4 36.4, D_div 31.3 | REPORTED |
| 150 | step_characterization (phi=0.8, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | mean lead B1 11.8, B2 48.7, B3 20.8, B4 47.3, D_div 40.0 | REPORTED |
| 151 | step_characterization (phi=0.9, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.145/0.855 | mean lead B1 4.1, B2 15.9, B3 7.8, B4 12.0, D_div 10.7 | REPORTED |
| 152 | step_characterization (phi=0.9, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.060/0.940 | mean lead B1 8.7, B2 29.4, B3 15.7, B4 22.1, D_div 19.2 | REPORTED |
| 153 | step_characterization (phi=0.9, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | mean lead B1 16.4, B2 44.6, B3 28.7, B4 33.9, D_div 31.1 | REPORTED |
| 154 | step_characterization (phi=0.95, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 7.7, B2 14.4, B3 13.9, B4 8.2, D_div 7.9 | REPORTED |
| 155 | step_characterization (phi=0.95, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | mean lead B1 15.6, B2 25.1, B3 25.6, B4 13.5, D_div 14.3 | REPORTED |
| 156 | step_characterization (phi=0.95, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 26.5, B2 39.1, B3 39.1, B4 20.8, D_div 21.6 | REPORTED |
| 157 | step_characterization (phi=0.98, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 20.4, B2 12.9, B3 28.7, B4 5.8, D_div 9.0 | REPORTED |
| 158 | step_characterization (phi=0.98, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 33.3, B2 22.7, B3 42.3, B4 10.5, D_div 15.0 | REPORTED |
| 159 | step_characterization (phi=0.98, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 45.5, B2 37.1, B3 53.9, B4 15.4, D_div 24.1 | REPORTED |
| 160 | realised_count_null (phi=0.5, n_events=57) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.145/0.850 | PASS |
| 162 | realised_count_effect (phi=0.5, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.150/0.300/0.550 | mean lead B1 2.1, B2 11.7, B3 3.2, B4 24.1, D_div 22.2 | REPORTED |
| 163 | realised_count_null (phi=0.8, n_events=57) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.205/0.795 | PASS |
| 165 | realised_count_effect (phi=0.8, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.205/0.785 | mean lead B1 1.9, B2 9.7, B3 2.9, B4 12.5, D_div 9.3 | REPORTED |
| 166 | realised_count_null (phi=0.9, n_events=57) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.170/0.830 | PASS |
| 168 | realised_count_effect (phi=0.9, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 1.7, B2 8.7, B3 3.1, B4 7.8, D_div 5.7 | REPORTED |
| 169 | realised_count_null (phi=0.95, n_events=57) | false-SUPPORT 0.010 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.010/0.160/0.830 | PASS |
| 171 | realised_count_effect (phi=0.95, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.080/0.910 | mean lead B1 1.9, B2 7.5, B3 2.9, B4 4.8, D_div 4.2 | REPORTED |
| 172 | realised_count_null (phi=0.98, n_events=57) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.210/0.790 | PASS |
| 174 | realised_count_effect (phi=0.98, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.145/0.845 | mean lead B1 1.6, B2 7.2, B3 3.3, B4 4.1, D_div 4.8 | REPORTED |
| 175 | decision_flip (phi=0.5, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.865 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | PASS |
| 176 | t3_decision_flip (phi=0.5, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.825 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.175/0.825 | PASS |
| 177 | decision_flip (phi=0.8, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.870 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 178 | t3_decision_flip (phi=0.8, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.845 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | PASS |
| 179 | decision_flip (phi=0.9, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.890 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.110/0.890 | PASS |
| 180 | t3_decision_flip (phi=0.9, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.875 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.120/0.875 | PASS |
| 181 | decision_flip (phi=0.95, n_events=20, L=8, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.905 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.090/0.905 | PASS |
| 182 | t3_decision_flip (phi=0.95, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.865 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | PASS |
| 183 | decision_flip (phi=0.98, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.835 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.165/0.835 | PASS |
| 184 | t3_decision_flip (phi=0.98, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.890 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.110/0.890 | PASS |
| 185 | realised_count_flip (phi=0.5, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.845 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.155/0.845 | PASS |
| 186 | realised_count_flip (phi=0.8, n_events=57, L=8, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.865 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | PASS |
| 187 | realised_count_flip (phi=0.9, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.860 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 188 | realised_count_flip (phi=0.95, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.860 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 189 | realised_count_flip (phi=0.98, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.950 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | PASS |
| 190 | flip_long (phi=0.5, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.020/0.980 | mean lead B1 2.7, B2 6.6, B3 3.4, B4 6.9, D_div 0.9 | REPORTED |
| 191 | flip_long (phi=0.5, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.025/0.975 | mean lead B1 2.3, B2 7.3, B3 3.0, B4 9.2, D_div 2.2 | REPORTED |
| 192 | flip_long (phi=0.8, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.060/0.940 | mean lead B1 2.0, B2 6.1, B3 2.9, B4 3.2, D_div 1.3 | REPORTED |
| 193 | flip_long (phi=0.8, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.020/0.980 | mean lead B1 2.3, B2 9.1, B3 3.8, B4 6.4, D_div 2.3 | REPORTED |
| 194 | flip_long (phi=0.9, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | mean lead B1 1.8, B2 6.0, B3 3.6, B4 1.9, D_div 1.2 | REPORTED |
| 195 | flip_long (phi=0.9, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.045/0.955 | mean lead B1 1.8, B2 8.8, B3 3.8, B4 2.9, D_div 2.3 | REPORTED |
| 196 | flip_long (phi=0.95, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | mean lead B1 2.1, B2 6.2, B3 5.0, B4 1.5, D_div 1.5 | REPORTED |
| 197 | flip_long (phi=0.95, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.035/0.965 | mean lead B1 2.2, B2 9.4, B3 5.1, B4 2.0, D_div 1.8 | REPORTED |
| 198 | flip_long (phi=0.98, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.020/0.980 | mean lead B1 3.6, B2 6.7, B3 8.7, B4 1.5, D_div 1.2 | REPORTED |
| 199 | flip_long (phi=0.98, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | mean lead B1 3.1, B2 9.5, B3 9.3, B4 1.8, D_div 1.9 | REPORTED |
| 200 | grid10_null (phi=0.5) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | PASS |
| 201 | grid10_effect (phi=0.5, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.030/0.080/0.890 | mean lead B1 21.1, B2 60.9, B3 26.0, B4 138.3, D_div 74.0 | REPORTED |
| 202 | grid10_effect (phi=0.5, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.035/0.090/0.875 | mean lead B1 23.1, B2 125.8, B3 35.6, B4 244.6, D_div 157.9 | REPORTED |
| 203 | grid10_effect (phi=0.5, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.070/0.175/0.755 | mean lead B1 28.7, B2 243.0, B3 51.2, B4 394.6, D_div 307.5 | REPORTED |
| 204 | grid10_effect (phi=0.5, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.020/0.060/0.920 | mean lead B1 27.5, B2 335.0, B3 49.0, B4 376.7, D_div 230.0 | REPORTED |
| 206 | grid10_null (phi=0.8) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.035/0.965 | PASS |
| 207 | grid10_effect (phi=0.8, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.100/0.900 | mean lead B1 21.7, B2 55.9, B3 26.7, B4 65.3, D_div 39.1 | REPORTED |
| 208 | grid10_effect (phi=0.8, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.015/0.080/0.905 | mean lead B1 22.3, B2 105.0, B3 34.2, B4 136.2, D_div 82.3 | REPORTED |
| 209 | grid10_effect (phi=0.8, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 24.1, B2 201.2, B3 43.4, B4 227.6, D_div 133.6 | REPORTED |
| 210 | grid10_effect (phi=0.8, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 23.3, B2 274.8, B3 44.0, B4 251.2, D_div 97.6 | REPORTED |
| 212 | grid10_null (phi=0.9) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 213 | grid10_effect (phi=0.9, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.010/0.125/0.865 | mean lead B1 17.8, B2 48.2, B3 26.9, B4 41.0, D_div 26.3 | REPORTED |
| 214 | grid10_effect (phi=0.9, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.095/0.905 | mean lead B1 19.4, B2 91.9, B3 33.3, B4 82.6, D_div 48.1 | REPORTED |
| 215 | grid10_effect (phi=0.9, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.030/0.965 | mean lead B1 24.6, B2 176.3, B3 45.1, B4 147.3, D_div 73.3 | REPORTED |
| 216 | grid10_effect (phi=0.9, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 24.1, B2 237.7, B3 46.4, B4 179.1, D_div 58.8 | REPORTED |
| 218 | grid10_null (phi=0.95) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 219 | grid10_effect (phi=0.95, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.100/0.900 | mean lead B1 18.4, B2 45.1, B3 26.5, B4 31.5, D_div 17.8 | REPORTED |
| 220 | grid10_effect (phi=0.95, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 22.2, B2 84.8, B3 34.7, B4 55.3, D_div 30.9 | REPORTED |
| 221 | grid10_effect (phi=0.95, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | mean lead B1 20.6, B2 150.1, B3 42.9, B4 106.7, D_div 52.5 | REPORTED |
| 222 | grid10_effect (phi=0.95, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 23.2, B2 202.3, B3 46.3, B4 132.1, D_div 40.8 | REPORTED |
| 224 | grid10_null (phi=0.98) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.075/0.925 | PASS |
| 225 | grid10_effect (phi=0.98, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.145/0.855 | mean lead B1 19.6, B2 43.6, B3 31.6, B4 24.0, D_div 23.2 | REPORTED |
| 226 | grid10_effect (phi=0.98, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.125/0.875 | mean lead B1 20.3, B2 76.2, B3 36.1, B4 48.9, D_div 35.7 | REPORTED |
| 227 | grid10_effect (phi=0.98, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.085/0.915 | mean lead B1 22.4, B2 127.8, B3 46.1, B4 80.2, D_div 48.6 | REPORTED |
| 228 | grid10_effect (phi=0.98, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.025/0.975 | mean lead B1 22.5, B2 170.0, B3 49.2, B4 94.8, D_div 37.9 | REPORTED |
| 230 | e2e_null (phi=0.5) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.180/0.820 | PASS |
| 231 | e2e_effect (phi=0.5, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.125/0.375/0.500 | mean lead B1 2.2, B2 12.7, B3 3.1, B4 23.9, D_div 23.7 | REPORTED |
| 232 | e2e_null (phi=0.8) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.115/0.885 | PASS |
| 233 | e2e_effect (phi=0.8, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.025/0.185/0.790 | mean lead B1 1.7, B2 10.5, B3 2.3, B4 11.8, D_div 9.2 | REPORTED |
| 234 | e2e_null (phi=0.9) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | PASS |
| 235 | e2e_effect (phi=0.9, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | mean lead B1 1.9, B2 9.2, B3 2.9, B4 7.3, D_div 6.2 | REPORTED |
| 236 | e2e_null (phi=0.95) | false-SUPPORT 0.005 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.155/0.840 | PASS |
| 237 | e2e_effect (phi=0.95, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | mean lead B1 1.8, B2 8.2, B3 2.9, B4 4.8, D_div 4.8 | REPORTED |
| 238 | e2e_null (phi=0.98) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 239 | e2e_effect (phi=0.98, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.185/0.810 | mean lead B1 1.9, B2 7.3, B3 2.9, B4 3.9, D_div 4.7 | REPORTED |
| 240 | grid10_short (phi=0.5, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.965 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.035/0.965 | PASS |
| 241 | grid10_short (phi=0.8, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.955 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.045/0.955 | PASS |
| 242 | grid10_short (phi=0.9, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.960 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 243 | grid10_short (phi=0.95, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.940 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.060/0.940 | PASS |
| 244 | grid10_short (phi=0.98, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.985 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | PASS |
| 245 | a1s_null (phi=0.5) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 246 | a1s_flip (phi=0.5, L=80, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.920 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.075/0.920 | PASS |
| 247 | a1s_effect (phi=0.5, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.255/0.315/0.430 | mean lead B1 24.1, B2 121.3, B3 34.6, B4 242.5, D_div 250.6 | REPORTED |
| 248 | a1s_null (phi=0.8) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | PASS |
| 249 | a1s_flip (phi=0.8, L=80, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.900 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.095/0.900 | PASS |
| 250 | a1s_effect (phi=0.8, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.015/0.175/0.810 | mean lead B1 23.3, B2 106.8, B3 33.3, B4 126.9, D_div 101.3 | REPORTED |
| 251 | a1s_null (phi=0.9) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 252 | a1s_flip (phi=0.9, L=80, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.875 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.120/0.875 | PASS |
| 253 | a1s_effect (phi=0.9, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.155/0.845 | mean lead B1 19.0, B2 87.6, B3 30.8, B4 73.5, D_div 58.8 | REPORTED |
| 254 | a1s_null (phi=0.95) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | PASS |
| 255 | a1s_flip (phi=0.95, L=80, A=3.0) | SUPPORT 0.010 (<= 0.05); reported: REFUTE 0.930 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.010/0.060/0.930 | PASS |
| 256 | a1s_effect (phi=0.95, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.105/0.895 | mean lead B1 19.0, B2 90.2, B3 31.9, B4 52.4, D_div 50.8 | REPORTED |
| 257 | a1s_null (phi=0.98) | false-SUPPORT 0.010 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.010/0.100/0.890 | PASS |
| 258 | a1s_flip (phi=0.98, L=80, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.935 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | PASS |
| 259 | a1s_effect (phi=0.98, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.225/0.775 | mean lead B1 22.5, B2 74.7, B3 34.3, B4 42.4, D_div 50.6 | REPORTED |
| 260 | dr_step (phi=0.5, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | REPORTED |
| 261 | dr_step (phi=0.5, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | REPORTED |
| 262 | dr_step (phi=0.5, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.045/0.955 | REPORTED |
| 263 | dr_grid10 (phi=0.5, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 264 | dr_grid10 (phi=0.5, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 265 | dr_grid10 (phi=0.5, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 266 | dr_step (phi=0.8, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | REPORTED |
| 267 | dr_step (phi=0.8, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.095/0.905 | REPORTED |
| 268 | dr_step (phi=0.8, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.005/0.055/0.940 | REPORTED |
| 269 | dr_grid10 (phi=0.8, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 270 | dr_grid10 (phi=0.8, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 271 | dr_grid10 (phi=0.8, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 272 | dr_step (phi=0.9, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | REPORTED |
| 273 | dr_step (phi=0.9, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | REPORTED |
| 274 | dr_step (phi=0.9, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | REPORTED |
| 275 | dr_grid10 (phi=0.9, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 276 | dr_grid10 (phi=0.9, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 277 | dr_grid10 (phi=0.9, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 278 | dr_step (phi=0.95, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 279 | dr_step (phi=0.95, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | REPORTED |
| 280 | dr_step (phi=0.95, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 281 | dr_grid10 (phi=0.95, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 282 | dr_grid10 (phi=0.95, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 283 | dr_grid10 (phi=0.95, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 284 | dr_step (phi=0.98, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 285 | dr_step (phi=0.98, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | REPORTED |
| 286 | dr_step (phi=0.98, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | REPORTED |
| 287 | dr_grid10 (phi=0.98, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 288 | dr_grid10 (phi=0.98, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 289 | dr_grid10 (phi=0.98, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| dyn-range | dr_grid10 phi=0.5 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [64,293] vs [148,506] OVERLAP, B2 [402,455] vs [719,805] sep, B4 [475,523] vs [841,892] sep | FAIL |
| dyn-range | dr_grid10 phi=0.8 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [107,321] vs [183,566] OVERLAP, B2 [364,431] vs [678,759] sep, B4 [368,434] vs [696,779] sep | FAIL |
| dyn-range | dr_grid10 phi=0.9 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [118,296] vs [233,532] OVERLAP, B2 [352,411] vs [638,730] sep, B4 [263,358] vs [558,680] sep | FAIL |
| dyn-range | dr_grid10 phi=0.95 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']) | FAIL |
| dyn-range | dr_grid10 phi=0.98 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']) | FAIL |
| dyn-range | dr_step phi=0.5 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [15,48] vs [26,82] OVERLAP, B2 [40,46] vs [72,82] sep, B4 [47,52] vs [83,90] sep | FAIL |
| dyn-range | dr_step phi=0.8 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [20,41] vs [35,72] OVERLAP, B2 [37,44] vs [66,77] sep, B4 [36,43] vs [67,78] sep | FAIL |
| dyn-range | dr_step phi=0.9 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [21,35] vs [32,62] OVERLAP, B2 [34,43] vs [63,75] sep, B4 [25,35] vs [51,67] sep | FAIL |
| dyn-range | dr_step phi=0.95 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [18,32] vs [31,54] OVERLAP, B2 [33,42] vs [59,72] sep, B4 [14,26] vs [35,53] sep | FAIL |
| dyn-range | dr_step phi=0.98 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [19,32] vs [32,56] OVERLAP, B2 [33,42] vs [58,71] sep | FAIL |

=== PART 5: Amendments 1–6 (context only; not under review here — Amendments 2–6 are under a separate review) ===

## Amendment 1 (2026-10-30) — A1 on its native 10-step gradient-norm grid

**Status.** Appended below §D.9 under the append-only rule. Rationale: DECISIONS.md entries 5 and 6. Draft v2 (drafts/DESIGN_Amendment_1_DRAFT.md, MD5 ffd2b3008f80e40d5cf5302ee3860dd8, committed at ced1674) went to a scoped single-round independent check:
- prompt and package: verification/amendment1_review_prompt.md and verification/amendment1_review_package.md;
- reply, verbatim: verification/amendment1_review_transcript.md;
- adjudication: verification/amendment1_review.md.

Result: 16 findings (G1–G16), all adopted, five with a stated adaptation, plus one author-found item (S1). This text is the adjudicated version. Where it differs from draft v2, this text governs.

**Trigger.** First data contact on A1 (DECISIONS entry 5; Discrepancy Register D-01). A1 logs `optim/total_grad_norm` only on steps with step mod 10 = 0. The evidence:
- run config `optimizer.metrics_log_interval: 10`;
- `configs/official-0724/OLMo-7B-0424.yaml`;
- training commit `43a155f`, whose `clip_grads_and_collect_metrics` returns no optimizer metrics on other steps.

`train/CrossEntropyLoss` is logged every step. Before this amendment, only the following were read from A1: schema (column names), row count, step range, and the per-row null mask of those two columns. No metric value was read. This amendment is made and pushed publicly before any A1 metric value is read (Phase 2 override (3)).

**What it changes.**
- **Detector side (A1 only).** The time unit of every detector-side quantity for A1 changes from steps to grid observations. The numbers, ratios, grid points and rule partitions are unchanged.
- **One exception (A1 only):** A1's chained spike dedup rises from 200 to 2,000 steps (A1.3).
- **Unspecified frozen points.** It fills points the frozen text left unspecified for A1: gaps on the grid series, the event's grid anchor, and the n* = 0 guard.
- **Clarifications for every run.** Two clarifications apply to every run (A1.11); no frozen number changes.
- **Verbatim replacements.** It replaces, for A1, the step constants in D.0a, D.2, D.3 E2, §K and D.7 (A1.10).

**Choice (JAE, 2026-10-30, option (c)).**
- A1 remains the primary run (E2, §K), with its detectors run on its native 10-step grid.
- A2 and A3 (OLMo 2 stage 1) remain per-step replication runs under D.2 as frozen.
- A2 is confirmed every-step on run-08 (DECISIONS entry 5 item 7). A3 is to be confirmed at staging.

**A1.1 Grid, completeness, gaps and dropped observations.**
- **Grid.** A1's detector series is indexed by grid observation j at step t_j = 10·j; y_j = ln g(t_j).
- **Completeness (S1).** For A1, the D.1 completeness check applies to the step index unchanged: rows contiguous from a segment's first to last step, no duplicate steps, loss every step. `optim/total_grad_norm` must be present by name and is required on grid steps only.
  - For A1, D.1's "full per-step resolution" means every step for the loss and every grid step for the gradient norm.
  - A missing step inside a segment still fails D.1 for that segment. So on A1 a missing step can only lie in a gap between segments.
- **Gaps (G4).** A gap is a run of steps present in no segment (D.1).
  - **Detector series.** A gap resets detector state only if it contains at least one grid step. The reset follows D.2 "Gaps and state": every window, the B3 EMA, the B4 accumulator and its median/MAD history, the D_div percentile history, and the minimum history.
  - **Short non-grid gap.** A gap with no grid step (1–9 consecutive non-grid steps) leaves detector state and the minimum history unchanged.
  - **Loss series.** It follows D.2 as frozen: its windows restart at every gap, grid or not.
- **Dropped observations (G6).** A grid step present in the log with null, non-positive or non-finite g is a dropped observation. It is counted (D.6 item 5), y is carried forward from the previous scored grid observation, and it is not a gap.
  - If the first grid observation after a detector-series gap (or of the series) is dropped, the series and the minimum-history count begin at the first non-dropped grid observation.

**A1.2 Detector operators in grid observations.** Every window, hold and count in the detector space is expressed in grid observations, with the frozen numbers unchanged:
- **D_div:** SMA over w_f = 32 and w_s = 128 grid observations (320 and 1,280 steps); ratio 4, inside the Theorem 14 band. Percentile history since the last detector-series gap; minimum history 1,000 grid observations (A1.4).
- **B1:** rolling window 50 grid observations; P-B1 sweep {25, 50, 100}, also in grid observations.
- **B2:** unchanged.
- **B3 (G13):** α = 0.97 per grid observation, warm-up 25 grid observations. On A1 this is a construction choice under P-B3, not ZClip's documented per-step behaviour (EMA memory ≈ 330 steps rather than ≈ 33), and it is labelled so in the Methods.
- **B4:** median and MAD over 200 grid observations, minimum 30; k = 1.0; resets at each onset and at each detector-series gap.
- **Alarm onset and hold (P-HOLD):** H = 32 grid observations (320 steps).
- **FA:** alarm onsets per 10,000 out-of-window grid observations. Grid {0.5, 1, 2, 5}; headline 1.
  - n* = round(FA × N_out / 10,000), with N_out counted in grid observations and round(·) = round-half-up (A1.11). P-FA is otherwise unchanged.
  - **Guard (G1).** If n* = 0 at headline FA on A1, E2 is not run. §K records E2 as unrun for data availability under its re-set rule, never as REFUTE.
  - **Not matchable (G1).** A non-headline FA grid point with n* < 2 is reported with its n* as "not matchable" and enters no contrast.
  - **Upper bound (metadata only).** A1's last logged step is 543,360, so N ≤ 54,337 grid observations. Before any exclusion, n* ≤ 3, 5, 11 and 27 at FA 0.5, 1, 2 and 5. Headline matching on A1 is therefore coarse (n* of about 5), and this is stated in the Methods.
- **E1:** horizon h = 16 grid observations; R̄ windows [h, h + 32] and [h + 32, h + 128] in grid observations; ACF lags 0–256 grid observations, each lag using all pairs that do not cross a detector-series gap; permutation blocks of 128 grid observations.
- **E5:** circular-shift offsets in [1,000, N − 1,000] grid observations; block shuffle in blocks of 128 grid observations.
- **E4:** window pairs (16, 64) and (64, 256) in grid observations, as frozen. **Added:** a physical-scale pair (4, 16) grid observations (40 and 160 steps), which approximates the frozen per-step pair's step span. It is reported with no verdict. The scan window does not change with the pair (A1.4, G9).

**A1.3 Loss side.**
- **Spike definition.** The spike definition (L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), over finite values) stays on the per-step loss: k ladder P-KLAD, NaN rule, event time t_e in steps.
- **A1 dedup (changed): chained, 2,000 steps (200 grid observations).** A spike is merged into the current event if it lies within 2,000 steps of the most recently merged spike.
  - *Reason:* with the scan window at 1,280 steps (A1.4), the frozen 200-step dedup would let scan windows of consecutive events overlap. A 2,000-step dedup restores dedup > scan window, as in the frozen per-step design (200 > 128; the same ratio, 1.5625).
  - *Cost, stated:* clusters of spikes within 2,000 steps collapse into one event. A1's eligible-event count is therefore lower than under 200 steps, and the risk that both k-ladder rungs fall below 5 events — **INSUFFICIENT EVENTS → §K CLOSE** — is higher.
- **Event count.** The eligible-event count for the k ladder is computed with the 2,000-step dedup from the per-step loss, before any detector score.
- **Rung transport (G12), declared.** The rung is resolved on A1 under the 2,000-step dedup and transported to the per-step runs under the 200-step dedup. A2–A6 also report their eligible-event count at the other rung.
- **Per-step runs.** The per-step runs (A2–A6, Leg B) keep 200 steps.

**A1.4 Scan window, lead, minimum history and eligibility.**
- **Event anchor and scan window (G3, G9).**
  - Anchor: t_e^g = 10·⌊t_e/10⌋, the last grid step at or before the event.
  - Window: the 129 grid observations with t_j ∈ [t_e^g − 1,280, t_e^g]. This is the analogue of the frozen 129-step interval [t_e − 128, t_e].
  - The window is the same for every detector and every E4 window pair and does not vary with w_s.
  - *Reason:* the frozen scan window is a fixed 129-step closed interval. Keeping its length in observations keeps the window, the maximum lead, the left-censoring point and the hold in the frozen ratios.
  - t_e itself, in steps, remains the event time for dedup, the k ladder and reporting.
- **Lead.** Lead = t_e^g − t_j*, where t_j* is the first grid observation in the window at which the detector is in alarm. Leads are reported in steps at 10-step resolution.
  - A detector first in alarm at t_e^g has lead 0.
  - A missed event has lead 0 (P-MISS).
  - If the detector is in alarm at t_e^g − 1,280 and at t_e^g − 1,290, the event is left-censored: lead = 1,280 steps, flagged (P-CENS). Under P-HOLD that means an onset in [t_e^g − 1,600, t_e^g − 1,290].
  - C_b and C_min are computed on mean leads in steps.
- **FA exclusion (G16).** The scan windows of all events at the rung that resolved on A1 (P-KLAD), eligible or not, are excluded from the FA count and denominator.
- **Minimum history: 1,000 grid observations (10,000 steps).** It is counted from the first non-dropped grid observation after the last detector-series gap (A1.1).
  - *Reason:* the minimum history exists so that the expanding percentile score and B4's 200-observation median/MAD window are estimated from a stable number of observations. Those are counts, so it is kept as a count.
- **Event eligibility.** Every detector has a defined score at every grid observation in the scan window, and no detector-series gap lies inside it. Equivalently, the first observation of the window has at least 1,000 grid observations of post-gap history.
- **Cost, stated (G2).** No event with t_e^g within 11,280 steps (1,000 + 128 grid observations) of the series start or of a detector-series gap is eligible. The frozen figure is about 1,128 steps.
  - Events made ineligible by the minimum history are reported separately from spikes merged by the dedup and from rewind events made ineligible.
  - The number of assembled stretches longer than 11,280 steps is given in the structural report (A1.12).
- **Rewind events (G5).** A rewind event is scored on the series P-SEG assigns to it (D.1).
  - Its history is counted from the last detector-series gap on that series. A segment boundary that is not a gap does not reset the count.
  - The event is ineligible if the first observation of its scan window has fewer than 1,000 grid observations of post-gap history on that series.
  - The count of events made ineligible this way is reported beside the rewind-event count.

**A1.5 Consequences, stated rather than tuned.**
- **Window span.** On A1, D_div's windows span 320 and 1,280 steps. That is 16 and 64 times the optimizer's second-moment memory (W = 20 steps), against 1.6 and 6.4 times in the per-step design. S3 is restated accordingly.
- **Resolution.** A1's lead resolution is 10 steps; the maximum uncensored lead is 1,280 steps.
- **Scope condition on A1:** a precursor shorter than about one fast window (320 steps) favours the raw-reading baselines by construction.
  - **This is a statement for the Methods and THESIS only (G11).** It does not qualify E2's label or §K: a REFUTE on A1 STOPs the project whatever the realised precursor lengths.
- **E1 scope (G14).** E1's consistency-check label on A1 holds under approximate stationarity over 2,560-step horizons. The drift in y over that horizon is reported beside ρ.

**A1.6 E3 like-for-like sensitivity (G8).**
- A2 and A3 are scored per step as frozen.
- As an E4-type sensitivity with no verdict, E2's statistic is also reported on A2 and A3 with the gradient norm subsampled to step mod 10 = 0 and the loss kept per step, using the A1.1–A1.4 operators and the A1 dedup. This makes the A1 versus A2/A3 comparison like-for-like.

**A1.7 Suite (D.5), new cell: ten-step grid (G15).**
- **Pass criteria, restated verbatim from D.5:** "A cell passes if, comparing the noisy-series result to this oracle, |recovered mean lead − oracle mean lead| ≤ 8 steps for every detector and the recovered C_min has the oracle's sign in ≥ 95 % of replicates."
  - In this cell the lead tolerance is ±10 steps (one grid observation) in place of 8 steps. Every other D.5 criterion holds unchanged, including:
    - the oracle (θ matched on the noisy series, applied to the series with noise × 10⁻³, every score finite);
    - the planted null (false-support ≤ 0.05);
    - the unequal-memory null (false-REFUTE and false-SUPPORT each ≤ 0.05);
    - the decision flip (REFUTE).
- **Series.**
  - Planted per-step series observed only on step mod 10 = 0.
  - Each series is at least 33,840 steps long (3 × 11,280) and has at least two gaps that contain grid steps.
  - Planted events are placed so that all ten residues of t_e mod 10 occur.
- **Ramps.** Precursor ramps L ∈ {640, 1,000, 1,500, 2,000} steps (64–200 grid observations), plus one ramp shorter than a fast window (200 steps), which must show the A1.5 scope condition.
- **Loss spikes and pipeline.** Loss spikes are planted per step, with A1's 2,000-step dedup. The pipeline runs with the A1.1–A1.4 operators.
- **Exercised on the grid:** planted null, decision flip, unequal-memory null, P-CENS cluster probe and k ladder.
- **Probes:**
  - (i) a dropped grid observation (carry-forward), including a dropped first post-gap observation;
  - (ii) a rewind event at the minimum-history boundary, with a non-gap segment boundary that must not reset the count;
  - (iii) a missing non-grid step inside a segment, which must fail D.1 completeness for that segment;
  - (iv) a gap of 1–9 non-grid steps between two segments, which must leave detector state and eligibility unchanged and restart the loss windows;
  - (v) small-N_out series of N_out = 4,000 and 12,000 grid observations, reporting n* and realised onset counts at each FA grid point. The n* = 0 guard must fire at 4,000 (headline n* = round(0.4) = 0), and grid points with n* < 2 must be marked "not matchable";
  - (vi) a half-tie of FA × N_out / 10,000, which must round up.
- **Regime span.** The regime span reports which grid cell A1 lands in.

**A1.8 Unchanged.**
- **Frozen values.** k = 4 primary rung; dedup 200 steps for every per-step run; headline FA 1 per 10,000 (grid observations for A1); window pair (32, 128); ratio 4; H = 32; scan window 129 points; minimum history 1,000 observations; all rule partitions; §K grading day 2026-11-20.
- **Subsampling.** D.2 "Subsampling: none" holds for A1: every logged gradient-norm observation is used.
- **Per-step runs.** Leg B (own runs log every step) and A2–A6 per-step runs follow D.2 as frozen, apart from the clarifications in A1.11.

**A1.9 THESIS.** THESIS Amendment A4 (same commit) restates for A1:
- the false-alarm wording of A3(a);
- the window and lead scales;
- the scope condition with its non-bearing on the kill rule;
- the n* = 0 guard.

**A1.10 Verbatim replacements for A1 (G10, S1).** For A1 only, the following frozen phrases read as shown. Per-step runs keep the original phrase. No other D.0a, D.1, D.2, D.3 or §K text changes.
- **D.0a and D.3 E2 and §K:** "1 alarm onset per 10,000 out-of-window steps, alarm held H = 32 steps", "1 onset per 10,000 out-of-window steps, hold H = 32" → "1 onset per 10,000 out-of-window scored observations (grid observations on A1, steps elsewhere), hold H = 32 observations".
- **D.3 E2:** "censored events as 128" → "censored events as 1,280 steps on A1 (128 steps on per-step runs)".
- **D.3 E2:** "events are ≥ 200 steps apart" → "events are ≥ 2,000 steps apart on A1, ≥ 200 steps on per-step runs".
- **D.2 scan window:** "the scan window is [t_e − 128, t_e]" → "on A1, the 129 grid observations in [t_e^g − 1,280, t_e^g] (A1.4)"; "lead = 128" → "lead = 1,280 steps on A1".
- **D.2 eligibility:** "at least 1,000 steps of post-gap history" → "at least 1,000 grid observations of post-gap history on A1".
- **D.7 frozen line:** "spike dedup 200 steps", "scan window 128", "minimum history 1,000 steps" → for A1: "spike dedup 2,000 steps", "scan window 129 grid observations (1,280 steps)", "minimum history 1,000 grid observations".
- **D.1 completeness:** "full per-step resolution" → for A1, "every step for the loss and every grid step for the gradient norm" (A1.1).

**A1.11 Clarifications applying to every run (G7, G16).** These fix points the frozen text left unspecified; no frozen number changes.
- **(a) Rounding.** round(·) in P-FA is round-half-up for every run and FA target, implemented as ⌊x + 0.5⌋ (not Python's built-in round, which rounds half to even).
- **(b) "All events".** In the FA exclusion (D.2 "False-alarm rate", F18), "all events" means every event at the rung that resolved on A1 (P-KLAD).

**A1.12 Structural report before any A1 metric value enters the analysis.**
- **When.** After this amendment is pushed, and after the A1 history passes D.1 and the route gate of DECISIONS entry 2 Addendum B.
- **What.** A structural report computed from the step index and the per-row null masks only is committed to the repo, before loss events are enumerated and before any detector score. It contains:
  - per segment, its first and last step and row count;
  - P-SEG overlaps and every gap, with whether it contains a grid step;
  - N in grid observations;
  - the number of dropped grid observations and the longest consecutive run;
  - the assembled stretches longer than 11,280 steps;
  - the n* upper bounds at each FA grid point implied by N.
- **Later.** N_out, the realised n* and the event counts depend on the loss and are reported with E2.

## Amendment 2 (2026-10-31) — P-SEG clarification: ties, and segments superseded by an unused segment

**Status.** Appended below Amendment 1 under the append-only rule. Rationale: DECISIONS.md entry 10 (JAE decision 2026-10-31). Made and pushed before any A1 loss event is enumerated and before any detector score is computed. No A1 metric value has entered any analysis.

**Trigger.** D.1 P-SEG orders segments by first step and keeps the later segment's rows on overlapping steps, "because training resumed from the checkpoint and the later segment is the trajectory that continued". On A1 the rule is incomplete in two ways, shown by each run's resume checkpoint (`load_path` in the run config; resume step + 1 equals the measured first loss step for all six used segments that restarted; DECISIONS entry 10):
- **Ties.**
  - Runs 009 and 010 both resume from step 73,100.
  - Runs 012 and 013 both resume from 160,600.
  - Runs 014, 015 and 016 all resume from 212,000.
- **Unused superseders.** Segments that fail D.1 (not used) supersede steps of used segments:
  - 002 (resume 14,200) supersedes 001's steps 14,201–14,210;
  - 011 (resume 160,500) supersedes 010's 160,501–160,600;
  - 019 (resume 504,500) supersedes 018's 504,501–504,510.
  
  D.1 is silent on this case.

**Clarification (applies to every run assembled under P-SEG).**
- **(a) Ordering.** Segments are ordered by resume step (first step), and ties are broken by run order: the later run wins.
- **(b) Supersession by resume step.** A step s logged by segment X is superseded if any later segment Y (in the order of (a)), used or not, has resume step r_Y < s. Training restarted from r_Y, so everything X logged after r_Y was abandoned, however far Y itself logged; a sparse segment's last logged row is not used to bound it. The kept series takes each step s from the last segment in order whose resume step is below s.
- **(c) Unused owner.** A step whose owner under (b) is unused is a **gap** in the kept series (D.1, D.2 "Gaps and state"; for A1, a detector-series gap if it contains a grid step, Amendment 1 A1.1).
- **(d) Superseded tails of used segments** are rewind portions. Events in them are scored on that segment's own series, as frozen (D.1 F5).
- **(e) Superseded portions of unused segments** cannot be scored. They are reported as unscorable — segment unavailable (DECISIONS Addendum C item 5).

**Effect on A1.**
- **The kept series** is steps 1–14,200 | gap 14,201–52,300 | 52,301–160,500 | gap 160,501–160,600 | 160,601–504,500. The kept series ends at 504,500, where 019 (unused) takes over.
- **Under the literal reading** it would have been 1–14,210 | gap | 52,301–504,510.
- **Rewind portions of used segments** (scored on their own series):
  - 001: 14,201–14,210;
  - 008: 73,101–73,110;
  - 010: 160,501–160,851;
  - 013: 212,001–212,965;
  - 016: 337,001–337,339;
  - 018: 504,501–504,510.

**Costs, stated.**
- **(i) End steps.** 20 steps leave the kept series at segment ends: 14,201–14,210 and 504,501–504,510. They remain as rewind portions.
- **(ii) The new 100-step gap at 160,501–160,600.** It restarts every detector window, and the minimum history applies again (1,000 grid observations = 10,000 steps). No event whose scan window begins within that history is eligible. That covers t_e^g up to about 160,601 + 11,280 steps (Amendment 1 A1.4): roughly 11,280 steps of the kept series hold no eligible event.
- **(iii) The rejected alternative** (later-wins among used segments only) would have spliced 010's abandoned 160,501–160,600 onto 013, which restarted from a checkpoint on 011's trajectory. That would present a continuous series across a run boundary that did not exist.

**Unchanged.** Every other D.1, D.2 and Amendment 1 rule. The P-SEG sensitivity (keep-earlier; rewind events excluded, E4) is computed on the same segment set.

## Amendment 3 (2026-10-31) — Spike-rule construction details (every run)

**Status.** Appended below Amendment 2 under the append-only rule. Rationale: DECISIONS.md entry 12 (JAE decision 2026-10-31). Made and pushed before any loss value is read for event enumeration on any run. No A1 loss event has been enumerated, and no detector score has been computed.

**Trigger.** The D.2 spike definition — L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), over the finite values of L in the trailing 128 steps, with chained dedup (Amendment 1 A1.3: 2,000 steps on A1; 200 elsewhere) — leaves five construction details unstated. Each could change which steps are spikes, so each is fixed here before any loss value is read.

**Clarifications (every run: A1–A6, Leg B and the D.5 suite).**
- **(1) σ.** σ_128(L) is the sample standard deviation (ddof = 1) of the finite trailing values. This is the pandas `rolling().std()` default.
- **(2) Testable steps.** Step t is tested for a spike only if both hold:
  - all 128 trailing steps t−128 … t−1 lie on the same series since its start or its last gap;
  - at least **64** of them hold finite L values (half the window, so that σ is never estimated from a handful of points).
  
  Untested steps are not spikes. Their count is reported per series and in total, separately by cause: (a) inside the first 128 steps after a series start or gap; (b) finite-value floor not met.
- **(3) Dedup distance.** "Within D steps" is inclusive: a spike at step s joins the open event if s − (most recently merged spike) ≤ D.
- **(4) Gaps close chains.** A dedup chain never crosses a gap; the open event closes at the gap.
- **(5) Rewind series.** A rewind portion's own series is the kept series up to that segment's resume step, followed by the segment's own logged steps after it. Events are enumerated on this series with the same rules, and an event is a rewind event only if its event time t_e lies in the superseded portion. Events whose t_e lies before the resume step are kept-series events, enumerated on the kept series, and are not counted twice.
  - History for eligibility on this series is counted from the last gap on it (Amendment 1 A1.4, G5).

**D.5 suite additions (event enumeration).**
- (i) A NaN run that drops the finite count below 64. The affected steps must be untested and counted under cause (b), and the NaN steps themselves must still count as spikes when tested.
- (ii) A chain ending at a gap. The event must close at the gap, and a spike after the gap must open a new event.
- (iii) A rewind portion with an event at its first superseded step. It must be enumerated as a rewind event on its own series, not merged with a kept-series event, and not counted twice.

**Unchanged.** The spike inequality, k ladder (P-KLAD), NaN rule, event time t_e (the first step of the event), dedup distances and every other rule.

## Amendment 4 (2026-10-31) — Theorem checks (Phase 2 box 1): E1's R̄ made exact; P-PHIHAT primary moved to the level

**Status.** Appended below Amendment 3 under the append-only rule. Rationale: DECISIONS.md entry 15, the Phase 2 box 1 theorem checks against the as-published statements (JAE decisions 2026-10-31).
- No E1 input (y = ln g) has been read.
- No Leg B quantity exists.
- §K's thresholds, windows, spike definition and FA grid are untouched (DESIGN header rule).

**4.1 E1 — R̄ over half-open lag ranges (replaces the D.2 "Discrete estimate" sentence; applies on A1 in grid observations, Amendment 1 A1.2, and on every run where E1 or E3's sign check is computed).**
- **Definition.** R̄(a, b) = mean of the sample ACF ρ̂_y(τ) over integer lags τ = a, a+1, …, b−1 (b − a lags).
- **Criterion.** The predicted sign is sign[R̄(h, h+w_f) − R̄(h+w_f, h+w_s)]. At h = 16 with (w_f, w_s) = (32, 128), it averages lags 16–47 and 48–143 (in grid observations on A1).
- **Reason.** For a trailing SMA over w observations, Cov(SMA_w(y)_t, y_{t+h}) = σ²·(1/w)·Σ_{j=0}^{w−1} ρ(h+j) exactly. Theorem 8b's identity (The Divergence Theorem, eqs. 69–72) in discrete form is therefore sign[mean ρ over h…h+w_f−1 − mean ρ over h+w_f…h+w_s−1], with the common factor (1 − w_f/w_s) > 0. The registered inclusive form averages w + 1 lags and counts lag h + w_f in both intervals.
- **Sensitivity.** The registered inclusive form is reported as a sensitivity, with no verdict.
- **Unchanged.** Every other part of E1 (label partition, permutation, scope).

**4.2 P-PHIHAT — primary φ̂ on the level (replaces the D.4 "Measured inputs" first clause and the D.7 P-PHIHAT row).**
- **Primary.** φ̂ = lag-1 autocorrelation of the raw level of g²(t) over steps 1,000–5,000 (or up to the divergence step).
- **Sensitivity.** φ̂ of ln g²(t) after subtracting its trailing 128-step mean, over steps 1,128–5,000.
- **Reason.** The Measurement Trap's Appendix A.4 (EQ-5/EQ-6) is stated for the level persistence, and its scope condition S-4 says detrended persistence "is not interchangeable" with it.
- **Unchanged.** The index b_g*(exp)(φ̂, α_Adam) = (1−φ̂)/α_Adam + φ̂ remains a descriptive ordering only, with the D.4.1 caveats. Its stated direction, P-DIV and the planted-reorder suite case (F9) are unchanged.

**D.5 suite addition.** A probe on an AR(1) series with known ρ(τ) = φ^τ. The half-open R̄ must reproduce the exact discrete covariance sign. A constructed ACF on which the inclusive and half-open forms disagree must be reported as such.

## Amendment 5 (2026-10-31) — Detector construction details (every run)

**Status.** Appended below Amendment 4 under the append-only rule. Rationale: DECISIONS.md entry 16 (JAE decision 2026-10-31). Made and pushed before the D.5 suite is built or run, and before any gradient-norm value is read for scoring. No detector score exists for any run.

**Trigger.** D.2 specifies the detectors at the level of their defining formulas. Building the suite showed construction details that change scores, alarm onsets and therefore leads. B3 and B4 are defined as the documented behaviour of named tools, so their details come from the tools' source code at the pinned versions. The remaining details are choices, fixed here.

**5.1 Sources read (2026-10-31).**
- **ZClip:** PyPI `zclip` 1.0.0 (sdist SHA-256 8fd6098e4b7ba81884c2493b187cc87d527e2be5478e2c8d4d77ab85318e622f, the only release), file `zclip/zclip.py`.
- **trainscope:** `kaelvalen/trainscope` at commit 0651b25ea4817b7b04149f2532fb0f346f510cbe, file `trainscope/core/detectors/changepoint.py`.

**5.2 Definitions (replace the corresponding D.2 text; units are observations, which are grid observations on A1, Amendment 1).**

- **Observation index j.** j counts every observation of a series from the first non-dropped reading after the series start or last gap, starting at j = 0. **Dropped (carried-forward) observations count** (D.2 F15: observations equal steps, and a dropped reading is not a gap).
- **Minimum history.** A detector score is defined at observation j only if j ≥ 1,000. Before that, no detector has a score (no alarm can occur), whatever its own warm-up. This matches the A1.4 eligibility rule used in entries 11 and 13.
- **D_div.**
  - D(j) = SMA_{w_f}(y)(j) − SMA_{w_s}(y)(j). SMA_w(y)(j) is the mean of y over observations j−w+1 … j, **including** the current one. This is the trailing estimator of Theorem 8b's exact discrete identity (Amendment 4.1). D(j) is defined for j ≥ w_s − 1.
  - P_D(j) = #{s : w_s−1 ≤ s ≤ j, D(s) ≤ D(j)} / #{s : w_s−1 ≤ s ≤ j}. Ties count as ≤.
  - Score s_div(j) = P_D(j).
- **B1 (rolling z).**
  - s_1(j) = (y(j) − m)/sd, where m and sd are the mean and sample SD (ddof = 1) of y over the trailing 50 observations j−50 … j−1, **excluding** j.
  - If sd = 0, s_1(j) is undefined at that observation and is treated as no alarm. The count of such observations is reported.
  - The P-B1 sweep {25, 50, 100} uses the same convention.
- **B2 (raw reading).** s_2(j) = y(j).
- **B3 (ZClip, monitor mode; on g, not y).** ZClip 1.0.0 `zscore` mode, as coded:
  - **Warm-up.** The first 25 observations of a series (or after a gap) fill a buffer, with no score. At the 25th: μ = buffer mean, v = buffer population variance (ddof = 0).
  - **Score.** From the 26th observation on, s_3(j) = (g(j) − μ)/(√v + 1e-6), using μ and v **before** the update.
  - **Update.** μ ← 0.97·μ + 0.03·g(j), then v ← 0.97·v + 0.03·(g(j) − μ)², where the variance update uses the **updated** μ (as coded).
  - **P-B3 (unchanged).** Updates use the raw g(j) (monitor mode), not ZClip's clipped value. The sweep uses the clipped value, with the threshold at ZClip's `adaptive_scaling` default and clip_factor 1.0.
  - The documented decision threshold z = 2.5 is reported as an unmatched operating point.
  - **Replaces** the D.2 formula, which omitted the 1e-6 term and the update order.
- **B4 (trainscope CUSUM, upward; on y).** trainscope `ChangePointDetector` at 0651b25, as coded:
  - **Warm-up.** The first 30 observations of a series (or after a gap, or after a reset) are appended to the history, with no score.
  - **Robust z.** From then on, at each observation: median m and MAD over the history **before** the current observation is added (at most the 200 most recent; the current one excluded); σ = 1.4826·MAD, floored at 1e-12; z = (y(j) − m)/σ.
  - **Accumulator.** S⁺ ← max(0, S⁺ + z − k), with k = 1.0, and s_4(j) = S⁺.
  - **History.** The current observation is then appended and the history trimmed to 200. The history keeps every value, spikes included.
  - **P-B4 (unchanged).** Upward side only. Applied to y. S⁺ is reset to 0 at each alarm onset (P-HOLD) and at each gap. A reset does not clear the median/MAD history; a gap does.
  - trainscope's optional `ruptures` PELT step only rescales the score after a fire, never decides an alarm, and is not used.
  - The documented threshold h = 6.0 is reported as an unmatched operating point.
- **Alarm rule (unchanged).** s(j) ≥ θ, with onset and hold per P-HOLD. Undefined scores are never alarms.

**5.3 D.5 suite additions (hand-computed probes, committed as permanent suite probes; PRV pass 3).**
- (i) D_div on a short hand series: SMAs, D and P_D, including a tie.
- (ii) B1 with the current observation excluded, including the sd = 0 case.
- (iii) B3 against ZClip 1.0.0's own class, run in the suite on the same sequence; it must match to 1e-12.
- (iv) B4 against trainscope 0651b25's `ChangePointDetector` (upward accumulator, PELT absent); S⁺ must match to 1e-12 up to its first fire.
- (v) **A dropped reading inside the first 1,000 observations** (JAE). It must count toward j, carry y forward, and leave the first defined score at j = 1,000.

**Unchanged.** Windows (32, 128), ratio, H, the FA rule and grid, P-FA matching, leads, censoring, the spike rule and every outcome partition.

## Amendment 6 (2026-10-31) — P-FA threshold matching: scan from the top (defect fix)

**Status.** Appended below Amendment 5 under the append-only rule. Rationale: DECISIONS.md entry 17 (JAE decision 2026-10-31). Made and pushed before the D.5 suite is built and before any gradient-norm value is read for scoring. No detector threshold has been computed for any run.

**Defect.** D.2 "Threshold matching (P-FA)" sets θ = the smallest candidate v with out-of-window onset count c(v) ≤ n*. Under P-HOLD, an onset needs a fresh crossing from below, and "the first scored step of the series and of each post-gap restart counts as preceded by s < θ".
- At v = the minimum candidate the score never falls below v. Each scored block therefore has exactly one onset, and c(v_min) = the number of scored blocks (3 on A1), which is at or below n* (upper bound 5 at the headline FA; entry 11).
- The frozen rule therefore selects θ = v_min for every detector. Each detector would then be in alarm only for the first H observations of each block, every lead would be 0, C_min = 0, and E2 would return REFUTE (§K STOP) **whatever the data**.
- The frozen text's note on "non-monotone regions of c(v)" does not cover this: the low end of c(v) is always degenerate under P-HOLD.

**6.1 Replacement rule (replaces "θ = the smallest candidate v with c(v) ≤ n*" in D.2 and the D.7 P-FA row).**
- **Rule.** θ = the smallest candidate v such that **every** candidate u ≥ v has c(u) ≤ n*. Equivalently: scan the candidates from the highest down, and stop at the first candidate whose count exceeds n*. θ is the candidate immediately above it, or the lowest candidate if none exceeds n*.
- **No admissible candidate.** If the highest candidate already has c > n*, θ is set above the detector's maximum score. The detector never alarms; this is reported as "not matchable at this FA" for that detector, and its leads are 0.
- **Unchanged.** The candidate set (distinct score values on out-of-window scored observations), recomputing the score path and alarm state per candidate (B4), the realised count, any shortfall and any non-monotone region (all reported). Also unchanged: the FA grid, the headline, n* (round-half-up, A1.11) and the n* = 0 guard (A1.2).
- **Scope.** Every run (A1–A6, Leg B/E8), every FA grid point, every E4 sensitivity variant, and the D.5 suite, **including the oracle** (θ matched on the noisy series by this rule).

**6.2 Alarm-coverage check (new; every real run, per detector, per FA point).**
- **What is reported:** the fraction of out-of-window scored observations whose score is ≥ θ under the matched θ.
- **Stop rule:** at the headline FA, a fraction **above 10 %** for any detector is a **stop-and-report**. No lead is computed until JAE has seen the report.
- **Why:** this is the check that would have shown the defect above. A matched threshold that most of the series exceeds signals degenerate matching.

**6.3 D.5 suite additions.**
- (i) A series on which the minimum candidate satisfies c ≤ n*. Matching must not select it: θ must come from the top scan, and the coverage fraction must be small.
- (ii) A series whose top candidates are tied with c > n*. The detector must be reported as not matchable and never alarm.
- (iii) A non-monotone c(v) with a dip below n* at a mid-range value under a higher value with c > n*. The top scan must stop above the excursion.
