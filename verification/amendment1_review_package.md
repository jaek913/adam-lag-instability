# PACKAGE — independent check of DESIGN Amendment 1

Frozen text taken from DESIGN.md at tag prereg-v1 (commit 5bd193a; DESIGN.md MD5 a9d051ac65fde38d5001a433b5d11506). Amendment draft MD5 ffd2b3008f80e40d5cf5302ee3860dd8.

=== PART 1: Amendment 1 draft ===

## Amendment 1 (DRAFT v2, 2026-10-30; not yet appended to DESIGN.md) — A1 on its native 10-step gradient-norm grid

**Trigger.** First data contact on A1 (DECISIONS entry 5; Discrepancy Register D-01). A1 logs `optim/total_grad_norm` only on steps with step mod 10 = 0. The evidence:
- run config `optimizer.metrics_log_interval: 10`;
- `configs/official-0724/OLMo-7B-0424.yaml`;
- training commit `43a155f`, whose `clip_grads_and_collect_metrics` returns no optimizer metrics on other steps.

`train/CrossEntropyLoss` is logged every step. Before this amendment, only the following were read from A1: schema (column names), row count, step range, and the per-row null mask of those two columns. No metric value was read. This amendment is made and pushed publicly before any A1 metric value is read (Phase 2 override (3)).

**What it changes.** It changes the time unit of every detector-side quantity for A1 from steps to grid observations. The numbers, ratios, grid points and rule partitions are unchanged. There is **one exception**: A1's chained spike dedup rises from 200 to 2,000 steps (A1.3).

**Choice (JAE, 2026-10-30, option (c)).** A1 remains the primary run (E2, §K), with its detectors run on its native 10-step grid. A2 and A3 (OLMo 2 stage 1) remain per-step replication runs under D.2 as frozen. A2 is confirmed every-step on run-08 (DECISIONS entry 5 item 7); A3 is to be confirmed at staging.

**A1.1 Grid.**
- A1's detector series is indexed by grid observation j at step t_j = 10·j.
- y_j = ln g(t_j).
- A grid step present in the log but without `optim/total_grad_norm` is a dropped observation: it is counted, y is carried forward, and it is not a gap (D.2, F15).
- A step absent from the log altogether is a gap (D.1).

**A1.2 Detector operators in grid observations.** Every window, hold and count in the detector space is expressed in grid observations, with the frozen numbers unchanged:
- **D_div:** SMA over w_f = 32 and w_s = 128 grid observations (320 and 1,280 steps); ratio 4, inside the Theorem 14 band. Percentile history since the last gap; minimum history 1,000 grid observations (A1.4).
- **B1:** rolling window 50 grid observations; P-B1 sweep {25, 50, 100}, also in grid observations.
- **B2:** unchanged.
- **B3:** α = 0.97 per grid observation; warm-up 25 grid observations.
- **B4:** median and MAD over 200 grid observations, minimum 30; k = 1.0; resets at each onset and at each gap.
- **Alarm onset and hold (P-HOLD):** H = 32 grid observations (320 steps).
- **FA:** alarm onsets per 10,000 out-of-window grid observations. Grid {0.5, 1, 2, 5}; headline 1. n* = round(FA × N_out / 10,000), with N_out counted in grid observations. P-FA is otherwise unchanged.
- **E1:** horizon h = 16 grid observations; R̄ windows [h, h + 32] and [h + 32, h + 128] in grid observations; ACF lags 0–256 grid observations; permutation blocks of 128 grid observations.
- **E5:** circular-shift offsets in [1,000, N − 1,000] grid observations; block shuffle in blocks of 128 grid observations.
- **E4:** window pairs (16, 64) and (64, 256) in grid observations, as frozen. **Added:** a physical-scale pair (4, 16) grid observations (40 and 160 steps), which approximates the frozen per-step pair's step span. It is reported with no verdict.

**A1.3 Loss side.**
- The spike definition (L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), over finite values) stays on the per-step loss: k ladder P-KLAD, NaN rule, event time t_e in steps.
- **A1 dedup (changed): chained, 2,000 steps (200 grid observations).** A spike is merged into the current event if it lies within 2,000 steps of the most recently merged spike.
  - *Reason:* with the scan window at 1,280 steps (A1.4), the frozen 200-step dedup would let scan windows of consecutive events overlap. A 2,000-step dedup restores dedup > scan window, which the frozen per-step design had (200 > 128). Consecutive A1 event times are then more than 2,000 steps apart, and no event's scan window contains another event's spike.
  - *Cost, stated:* clusters of spikes within 2,000 steps collapse into one event. A1's eligible-event count is therefore lower than under 200 steps, and the risk that both k-ladder rungs fall below 5 events — **INSUFFICIENT EVENTS → §K CLOSE** — is higher.
- The eligible-event count for the k ladder is computed with the 2,000-step dedup from the per-step loss, before any detector score.
- The per-step runs (A2–A6, Leg B) keep 200 steps.

**A1.4 Scan window, lead and minimum history.**
- **Scan window.** The window is the w_s grid observations up to the event: the grid observations with t_j ∈ [t_e − 1,280, t_e].
  - *Reason:* in the frozen design the scan window equals w_s (128 = w_s). It is the span over which the slow average still carries pre-event information, and it sets the longest lead D_div can register. Keeping it equal to w_s, now counted in grid observations, keeps the scan window, the maximum lead, the left-censoring point and the hold in the same ratios as frozen.
  - The FA exclusion (all events' scan windows) uses this window.
- **Lead.** Lead = t_e − t_j*, where t_j* is the step of the first grid observation in the window at which the detector is in alarm. It is reported in steps at 10-step resolution.
  - If the detector is already in alarm at the first grid observation of the window (and at the one before), the event is left-censored: lead = 1,280 steps, flagged (P-CENS).
  - A missed event has lead 0 (P-MISS).
  - C_b and C_min are computed on mean leads in steps.
- **Minimum history: 1,000 grid observations (10,000 steps), from the first post-gap observation.**
  - *Reason:* the minimum history exists so that the expanding percentile score and B4's 200-observation median/MAD window are estimated from a stable number of observations. Those are counts, so it is kept as a count.
- **Event eligibility.** Every detector has a defined score at every grid observation in the scan window, with no gap inside it.
- **Rewind events (P-SEG) made ineligible by the minimum history.** A rewind event's scores are computed on its own earlier segment. If fewer than 1,000 grid observations separate that segment's first observation (or its last gap) from the start of the event's scan window, the event is ineligible. The count of such events is reported beside the rewind-event count.

**A1.5 Consequences, stated rather than tuned.**
- On A1, D_div's windows span 320 and 1,280 steps. That is 16 and 64 times the optimizer's second-moment memory (W = 20 steps), against 1.6 and 6.4 times in the per-step design. S3 is restated accordingly.
- A1's lead resolution is 10 steps.
- **Scope condition on A1:** a precursor shorter than about one fast window (320 steps) favours the raw-reading baselines by construction.

**A1.6 E3 like-for-like sensitivity.**
- A2 and A3 are scored per step as frozen.
- As an E4-type sensitivity with no verdict, E2's statistic is also reported on A2 and A3 subsampled to step mod 10 = 0, with the A1.2–A1.4 operators and the A1 dedup. This makes the A1 versus A2/A3 comparison like-for-like.

**A1.7 Suite (D.5), new cell.** Ten-step-grid cell:
- Planted per-step series observed only on step mod 10 = 0.
- Precursor ramps L ∈ {640, 1,000, 1,500, 2,000} steps (64–200 grid observations), plus one ramp shorter than a fast window (200 steps), which must show the A1.5 scope condition.
- Loss spikes planted per step, with A1's 2,000-step dedup.
- The pipeline runs with the A1.2–A1.4 operators.
- Pass criteria as D.5, with the lead tolerance set to ±10 steps (one grid observation).
- Planted null, decision flip, unequal-memory null, P-CENS cluster probe and k ladder are all exercised on the grid.
- A carry-forward probe for a missing grid observation.
- A rewind-event probe at the minimum-history boundary.
- The regime span reports which grid cell A1 lands in.

**A1.8 Unchanged.**
- Frozen: k = 4 primary rung; dedup 200 steps for every per-step run; headline FA 1 per 10,000 (grid observations for A1); window pair (32, 128); ratio 4; H = 32; all rule partitions; §K grading day 2026-11-20.
- Leg B (own runs log every step) and A2–A6 per-step runs follow D.2 as frozen.

**A1.9 THESIS.** A matching THESIS amendment, A4, is required. For A1 it restates:
- A3(a)'s false-alarm wording as "alarm onsets per 10,000 out-of-window gradient-norm observations (A1 logs the gradient norm every 10 steps), each onset held 32 observations";
- the scope condition in A1.5.

=== PART 2a: frozen DESIGN §D.2 (verbatim) ===

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

=== PART 2b: frozen DESIGN §D.3 (verbatim) ===

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

=== PART 2c: frozen DESIGN §K (verbatim) ===

### §K — Kill rule (pre-registered)

**Grading day:** `prereg-v1` commit date + 21 days. The concrete calendar date is written here and in THESIS.md's Date station in the `prereg-v1` commit itself: **2026-11-20** (`prereg-v1` commit dated 2026-10-30). On that day the verdict is recorded in DECISIONS.md and RECORD.md whether or not E2 has run; an unrun E2 (including A1 unavailable under D.1) is itself recorded and the day is re-set once, by dated amendment. If E2 is still unrun on the re-set day, §K returns CLOSE with a short null note on data availability (F11).

**Rule:** after E2's single real run on A1: if E2 is **REFUTE (C_min ≤ 0)** — D_div's mean lead at headline FA (1 onset per 10,000 out-of-window steps, hold H = 32) does not exceed that of the best of B1–B4 (point estimate) — the project STOPS. The negative is written up as a short null note (Standard: the null is the paper), filed in the repo and on Zenodo, with RECORD.md as the closing artifact; Leg B does not run. If E2 is **INSUFFICIENT EVENTS** (fewer than 5 eligible events on A1 at k = 4 and at k = 3), the project also closes: a short null note on event count is filed (neither a pass nor a kill of Claim A), with RECORD.md, and Leg B does not run. INCONCLUSIVE or SUPPORT → Leg B proceeds. No re-tuning of windows, spike definition, baselines, construction pins, or FA grid after A1 is touched; E4's sensitivity results are reported as they fall and do not rescue the verdict.

=== END OF PACKAGE ===
