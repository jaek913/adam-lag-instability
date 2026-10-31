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
