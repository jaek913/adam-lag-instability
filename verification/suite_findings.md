# D.5 suite build — findings and pending construction items

Opened 2026-10-31, while building the D.5 suite after DESIGN Amendment 7 (DECISIONS entry 18). Synthetic data only. No gradient-norm or loss value has been read for scoring. No threshold has been computed for any real run.

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

## Pending suite construction items (unstated in D.5 / A1.7; proposals in the suite code, provisional)

| # | Item | Proposal | Alternative |
|---|---|---|---|
| 9 | Series length and event placement (sets N_out and n*) | Per-step cells: 50,000 observations (close to A1's 46,630). Events at uniform random positions with consecutive t_e at least scan + L_max + 1 = 329 apart, and the first t_e ≥ 1,000 + scan + L_max. Headline-FA n* is then about 4–5, as on A1. | Fixed even spacing; or a length set per event count. |
| 10 | What y does at the event | Nothing: the event is a label at t_e. The ramp ends at t_e and y returns to the AR(1) base. (Only alarms at or before t_e^g enter a lead.) | A spike in y at t_e. |
| 11 | Level of y | y = AR(1) with mean 0 and unit stationary SD; g = exp(y). | Level matched to A1's ln g. |
| 12 | Cell crossing | Planted effect: φ_y (5) × L (4) × A (3) at 20 events. Regime span: φ_y (5) × events {5, 10, 20, 40} at L = 100, A = 2. Nulls and the decision flip: φ_y (5) at 20 events. 200 replicates each. | Full cross of all factors. |
| 13 | Null with every detector's detection rate at 30–50 % (F1) | Plant a one-observation pulse of height h at a uniform random offset in [1, scan] before each event, in all events, with h tuned per φ_y by a committed calibration run so that every detector's detection rate at headline FA lands in 30–50 %. There is no ramp, so no precursor is persistent. | A random-onset step of fixed length. |
| 14 | Replicate execution | The suite runner uses multiprocessing (results are independent of the worker count, because seeds are per cell × replicate, Amendment 7.4). It is run on the Windows host. | Single process. |

## Decided 2026-10-31 (JAE) — DECISIONS entry 19, DESIGN Amendment 8

- **S-1:** option 1 (independent reference-implementation oracle), with JAE's conditions on independence and hand probes (Amendment 8.1). The 10⁻³ oracle is recorded as a design-stage error.
- **Items 9 and 12:** as proposed.
- **Items 10, 11, 13 and 14:** changed per JAE (Amendment 8.2):
  - 10: a surge cell is added;
  - 11: a Student-t cell is added;
  - 13: disjoint calibration seeds, with the calibration committed before the verdict run;
  - 14: seeds via `SeedSequence.spawn`, plus a single- versus multi-process identity check.

## Pending suite construction items 15–17 (found 2026-10-31 while building the cell table; not decided)

| # | Item | Proposal | Alternative |
|---|---|---|---|
| 15 | Decision flip: ramp length, amplitude and pass fraction. D.5 says "ramps shorter than the raw-reading baselines' response; the rule must return REFUTE". | L = 8 observations (a quarter of w_f), A = 3. Pass: REFUTE in ≥ 95 % of replicates (the same level as the other D.5 rate criteria). | L = 16; or REFUTE in every replicate. |
| 16 | Unequal-memory null: the two synthetic baselines. D.5 says "raw alarm runs last 1 step and 40 steps". | S₁(j) = y(j); S₄₀(j) = max(y(j−39 … j)), so one exceedance keeps S₄₀ above θ for 40 observations. In this cell the baseline set is {S₁, S₄₀}; both are matched with D_div by P-FA, and C_min is taken over these two. | Synthetic alarm streams with no score. |
| 17 | Whether the null false-rate criteria are attainable as written. The unequal-memory null requires false-REFUTE ≤ 0.05. With no precursor, C_min ≤ 0 (REFUTE) may be the typical outcome rather than a rare error. | Measure on the item-16 construction before it is decided. If unattainable, report it as finding S-2 with options, as for S-1. | — |

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

## Decided 2026-11-06 (JAE) — DECISIONS entry 23, DESIGN Amendment 10

- **S-2:** invariance criterion (|C_S1 − C_S40| ≤ 1 in ≥ 95 %; |median C_b| ≤ 1; false-SUPPORT ≤ 0.05), graded on the unused evaluation seeds of cells 115–119. False-REFUTE and P(C_b > 0 | C_b ≠ 0) are reported. The item-17 measurement is exploratory. JAE's proposed [0.40, 0.60] band failed because about half of replicates have C_b = 0 exactly.
- **S-3:** pulse with a per-detector calibration sweep. False-SUPPORT ≤ 0.05 at every calibrated h on evaluation seeds, with the detector × h table reported; this is the E2 lookup for detection rates ≤ 50 %. The step is a reported characterization only, labelled "step precursor, not a null".

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

## Pending construction items 19a–19f (ten-step grid cell A1.7 and end-to-end loss cell 7.8; provisional in `analysis/synth_e2e.py`)

A1.7 fixes the observation grid, the minimum length (≥ 33,840 steps), ≥ 2 gaps, all ten residues of t_e mod 10, the ramp lengths and the 200-step short ramp. It leaves the following unstated.

| # | Item | Proposal (provisional in code) |
|---|---|---|
| 19a | Geometry | Grid 10: three blocks of 155,000 steps with two 5,000-step gaps (no logged steps), giving 46,500 grid observations (A1: 46,630). Grid 1: one 50,000-step block (as in the other per-step cells). |
| 19b | Events | Grid 10: 57 (A1's count), split evenly across blocks, uniform positions with spacing ≥ L_max + scan + grid, each with ≥ 1,000 grid observations of history plus the scan window. Residues forced to cycle 0–9. Grid 1: 20 events. |
| 19c | Loss series | A deterministic period-4 base, 2.5 + 0.01·(0, 1, 0, −1), with a +0.1 spike at each planted t_e (the `test_a1_events.py` pattern, which produces no spurious spikes). The A1 spike rule (`a1_events.enumerate_series`, k = 4, dedup 2,000 on grid 10 and 200 on grid 1) must recover exactly the planted events, all eligible, in every replicate; the grader checks this. |
| 19d | Gradient norm | Per-step AR(1) for ln g with unit stationary SD and φ_step = φ_y^(1/grid), so the lag-1 autocorrelation on the observation grid is φ_y. Observed at step mod grid = 0. Ramps are linear in steps, A × SD. |
| 19e | Cells (200 replicates each) | Per φ_y: grid-10 null; grid-10 effect at L ∈ {640, 1,000, 1,500, 2,000} steps with A = 2; grid-10 short ramp L = 200, A = 2; grid-1 null; grid-1 effect at L = 100, A = 2. |
| 19f | Criteria | Nulls: false-SUPPORT ≤ 0.05. Effect and short-ramp cells: reported. The A1.7 "±10 steps" lead tolerance is superseded by Amendment 8.1's reference agreement, which these cells also run, with grid 10 and scan 1,280. The short-ramp cell's "must show the A1.5 scope condition" is read as reported REFUTE / lead rates; whether that needs a numeric bar is JAE's call. |

**Checks so far.**
- One replicate each, grid 10 and grid 1: events recovered exactly (57 and 20).
- Grid-parameterised eligibility = `a1_events.eligibility` at grid 10 on 311 sampled steps.
- Reference agreement identical on three grid-10 and grid-1 replicates.
- The grader's watch-to-fail test now also fails a grid-10 cell with one unrecovered event or a missing residue (12/12).

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
