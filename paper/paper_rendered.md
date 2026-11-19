# Abstract

> seed (map): Question (does a smoothed fast–slow divergence on the log gradient norm warn of loss spikes earlier than deployed one-step alarms at matched false-alarm rate); pre-registration; primary run; E2 REFUTE with the F-6 reading; what the null does and does not say; keywords (no JEL)

**Keywords:** loss spikes; training instability; early warning; Adam; gradient norm; pre-registration; negative result

# 1 Introduction {#sec-1}

> seed (map): Cost of loss spikes; gradient norm as a precursor; deployed alarms are one-step fast–slow tests; the pre-registered question and kill rule; contribution: a clean, ledgered null with its severity

> seed: **ARG-01.** Loss spikes cost compute through rewinds and skips, and gradient-norm spikes tend to precede them [@Walsh-2025] [@Chowdhery-2023] [@Takase-2025]
> seed: `L-01` Does NOT propose a new instability mechanism; the second-moment lag is prior art {#L-01}
> seed: See @sec-4.2 @TBL-3 (headline result).

# 2 Related Work {#sec-2}

> seed (map): 2.1 Spike precursors and deployed alarms; 2.2 Second-moment lag mechanism (not claimed); 2.3 Edge of stability and the curvature boundary (complementary)

## 2.1 Spike precursors and deployed alarms {#sec-2.1}

> seed: **ARG-04.** Deployed alarms (ZClip, SPAM, trainscope) are fast–slow divergences with a one-step fast window [@Kumar-2025] [@Huang-2025a] [@trainscope-2026]
> seed: See @sec-3.2 @TBL-1 (deployed alarms become B3/B4).
> seed: [@Huang-2026] prior-art (mitigation, not warning).
> seed: [@Wang-2025] prior-art (mitigation, not warning).
> seed: [@Fatima-2025] contrast (failure-risk score with lead times; targets failures, not spikes).

## 2.2 Second-moment lag mechanism {#sec-2.2}

> seed: **ARG-03.** That the second-moment estimate lags the squared gradients and destabilizes training is established; this paper does not claim it [@Shazeer-2018] [@Wortsman-2023] [@Molybog-2023] [@Bai-2026a] [@Tang-2026]
> seed: [@Ma-2022] prior-art (qualitative (β₁, β₂) regimes).
> seed: [@Bai-2026b] prior-art (derived phase diagram on toy objectives).

## 2.3 Edge of stability and the curvature boundary {#sec-2.3}

> seed: See @sec-5.3 (complementarity with the curvature boundary).

# 3 Methods {#sec-3}

> seed (map): 3.1 The detector D_div (Adam as a measurement-feedback loop; y = ln g; D = SMA_32 − SMA_128; expanding-percentile score; motivation, not a bound); 3.2 Baselines B1–B4; 3.3 Data: primary run A1 (OLMo-0424), 10-step grid, P-SEG kept series and covered ranges; 3.4 Spike events and the k ladder; 3.5 Alarm onset and hold, P-FA matching, lead, contrast C_min, the kill rule and grading day (verbatim); 3.6 Pre-registered secondary analyses (E1, E4, E5; E3 not run); 3.7 Synthetic validation suite and the reading rules fixed before E2; 3.8 Deviations, amendments and discrepancies

## 3.1 The detector D_div {#sec-3.1}

> seed: **ARG-02.** Adam steers off trailing averages whose estimates feed back into the gradients they measure — a measurement-feedback loop [@Kim-2026d] [@Kingma-2015]
> seed: **ARG-05.** The smoothed divergence D = SMA_32(y) − SMA_128(y) on y = ln g, ratio 4 inside the Theorem 14 band, trades single-step response for noise rejection [@Kim-2026c] @EQ-1 @EQ-2
> seed: **ARG-06.** After a level change the fast average crosses a threshold ahead of the slow average (by (w_s − w_f)/2 at the midpoint); this motivates watching their difference but does not bound the detector's lead over a spike, which E2 measures [@Kim-2026a] @EQ-5
> seed: **ARG-07.** The sign of D's forward correlation with y is fixed in advance by the ACF (Theorem 8b); on A1 it is checked as a consistency condition [@Kim-2026c] @EQ-6 INDETERMINATE 0.02369 0.08891
> seed: Figure @FIG-1 — Adam as a measurement-feedback loop, and the fast–slow divergence read off the gradient norm {#FIG-1}
> seed: Equation @EQ-1 — y(t) = ln g(t), g = pre-clip global gradient norm {#EQ-1}
> seed: Equation @EQ-2 — D(t) = SMA_32(y)(t) − SMA_128(y)(t) {#EQ-2}
> seed: Equation @EQ-3 — Detector score: expanding empirical percentile of D (ties counted ≤; SMAs include the current reading), defined only at j ≥ 1,000 observations, dropped readings counted (Amendment 5) {#EQ-3}
> seed: Equation @EQ-5 — Fast-over-slow crossing lead α(w_s − w_f), (w_s − w_f)/2 at the midpoint (cited; motivation, not a bound on spike lead) {#EQ-5}
> seed: Equation @EQ-8 — Adam second-moment update v_t = β₂ v_{t−1} + (1−β₂) g_t² and step η/√v_t {#EQ-8}
> seed: `S1` Every operator is causal and reads only scalars already in a training log; no curvature is computed {#S1}
> seed: `L-05` Does NOT claim an analytical bound on the lead over a spike; the Adaptation Rate Theorem is used as motivation only {#L-05}
> seed: See @EQ-1 @EQ-2 @EQ-3 @FIG-1 @L-05 (operator definition and its limit).
> seed: **LB-E1-predsign** (ARG-07). A-priori predicted sign from the ACF criterion 1

## 3.2 Baselines B1–B4 {#sec-3.2}

> seed: Table @TBL-1 — Detector definitions: D_div and B1–B4, parameters, source or pin; B3 as coded in ZClip 1.0.0 (monitor mode, raw g) and B4 as coded in trainscope 0651b25 (upward CUSUM on y, reset at onsets and gaps), both vendored (Amendments 5, 9) {#TBL-1}

## 3.3 Data: primary run A1 {#sec-3.3}

> seed: Table @TBL-2 — Leg A data: A1 identifier, segments, kept blocks, covered ranges and gaps; A2–A6 not staged (§K stop) {#TBL-2}
> seed: `S2` g is the pre-clip global gradient norm; a run logging post-clip norm is reported separately, never pooled {#S2}
> seed: `S3` Every Leg A run used β₂ = 0.95 (second-moment window 20 steps); Leg A tests the alarm independent of β₂, and the (32, 128) windows exceed the optimizer's own memory (1.6×/6.4× per step; 16×/64× on A1's 10-step grid) {#S3}
> seed: `S5` Leg A data are the public logs as staged after `prereg-v1`, hash-pinned; segments assembled by P-SEG as clarified in DESIGN Amendment 2 (later run wins ties; supersession by resume step); the kept series has two internal gaps; no window crosses a gap {#S5}
> seed: `S11` On the primary run the gradient norm is logged every 10 steps, so its detectors run on that grid (windows 320/1,280 steps, lead resolution 10 steps, dedup 2,000 steps). A precursor shorter than about 320 steps favours raw-reading baselines by construction; this scope statement does not qualify the kill rule (DESIGN Amendment 1, THESIS A4) {#S11}
> seed: `S12` The primary run's kept series follows each restart: a later run wins ties, and any step a later run superseded leaves the kept series. Where the superseding run's log is incomplete this leaves a gap, and its minimum-history cost is stated (DESIGN Amendment 2; structural report) {#S12}
> seed: `S14` E2's eligible-event count, n*, the verdict and X1–X3 are conditional on A1's covered ranges (steps 1–14,210 and 52,301–504,510, kept blocks plus rewind portions); the uncovered range is a stated selection threat, and route 3 would not change n* or D_div's unmatchability only as a projection (DECISIONS 59) {#S14}
> seed: See @TBL-2 @S14 @app-D (data, covered ranges, provenance).

## 3.4 Spike events and the k ladder {#sec-3.4}

> seed: Equation @EQ-4 — Spike rule L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), σ sample SD; tested only with a full 128-step trailing window holding ≥ 64 finite values; chained dedup 2,000 on A1, inclusive, closed at gaps (Amendment 3) {#EQ-4}
> seed: `S10` Spikes that a checkpoint restart superseded are retained as rewind events on their own series (the kept series up to the resume step plus the superseded steps); rewind portions on unused segments are counted as unscorable; dedup applies within a series (Amendment 2, Amendment 3) {#S10}
> seed: `S13` Under chained dedup, events at a lower spike threshold are not a superset of events at a higher one: dense lower-rung spikes merge into long chains (DECISIONS entry 13) {#S13}
> seed: See @EQ-4 @sec-4.1 (spike rule and event counts).

## 3.5 Alarm onset and hold, P-FA matching, lead, contrast C_min, the kill rule and grading day {#sec-3.5}

> seed: **ARG-08.** At matched false-alarm rate (on A1: alarm onsets per 10,000 out-of-window gradient-norm observations, hold 32 observations, censored lead 1,280 steps — Amendment 1), D_div's mean lead is compared with the best of four baselines on the minimum contrast; the point estimate decides REFUTE. Result (F-6 reading): D_div could not be matched at the headline FA (it never alarmed), no detector led any event, and E2 is REFUTE by a tie at zero; §K STOP. Conditional on A1's covered ranges (S14)  @EQ-7 @EQ-11 @TBL-3 @FIG-2 @FIG-4 REFUTE 0 0 0 0 False 0.2 STOP 57
> seed: Equation @EQ-7 — C_b = mean lead(D_div) − mean lead(B_b) over eligible events (misses and concurrent 0, censored 1,280 steps on A1); C_min = min_b C_b {#EQ-7}
> seed: Equation @EQ-11 — Alarm onset with hold H = 32; FA = out-of-window onsets per 10,000 out-of-window grid observations on A1 (common N_out, Amendment 7.2); n* = round-half-up(FA × N_out / 10,000); θ by top scan (Amendment 6) with B4 candidates on the reset-free path (7.1); a detector is unmatchable when even its top score yields more than n* onsets (θ = ∞) {#EQ-11}
> seed: `S7` Events at least 200 steps apart are treated as independent for resampling (block-of-3 sensitivity) {#S7}
> seed: `S8` Lead is measured inside a 128-step scan window; FA is out-of-window alarm onsets per 10,000 out-of-window steps (headline 1), each onset held 32 steps; a missed event has lead 0; an alarm already on at the window start gives lead 128, flagged (A1: 129 grid observations ending at the event's grid step, censored lead 1,280 steps, hold 32 observations) {#S8}
> seed: See @EQ-7 @EQ-11 @sec-4.2 (contrast, matching and result).
> seed: **LB-A1-nevents-k3** (ARG-08). Eligible event count on A1 at k = 3 (if the ladder steps down) 17
> seed: **LB-A1-rung** (ARG-08). k-ladder rung that resolved k=4
> seed: **LB-A1-ineligible** (ARG-08). Ineligible events counted, with reasons 4
> seed: **LB-A1-rewind** (ARG-08). Rewind events retained on their own segment (count) 0
> seed: Registered kill rule and grading day, verbatim from `prereg-v1` (DOI 10.5281/zenodo.23825294); the grading day was later re-set once (Amendments 16–17, @sec-3.8):
> **Grading day:** `prereg-v1` commit date + 21 days. The concrete calendar date is written here and in THESIS.md's Date station in the `prereg-v1` commit itself: **2026-11-20** (`prereg-v1` commit dated 2026-10-30). On that day the verdict is recorded in DECISIONS.md and RECORD.md whether or not E2 has run; an unrun E2 (including A1 unavailable under D.1) is itself recorded and the day is re-set once, by dated amendment. If E2 is still unrun on the re-set day, §K returns CLOSE with a short null note on data availability (F11).
>
> **Rule:** after E2's single real run on A1: if E2 is **REFUTE (C_min ≤ 0)** — D_div's mean lead at headline FA (1 onset per 10,000 out-of-window steps, hold H = 32) does not exceed that of the best of B1–B4 (point estimate) — the project STOPS. The negative is written up as a short null note (Standard: the null is the paper), filed in the repo and on Zenodo, with RECORD.md as the closing artifact; Leg B does not run. If E2 is **INSUFFICIENT EVENTS** (fewer than 5 eligible events on A1 at k = 4 and at k = 3), the project also closes: a short null note on event count is filed (neither a pass nor a kill of Claim A), with RECORD.md, and Leg B does not run. INCONCLUSIVE or SUPPORT → Leg B proceeds. No re-tuning of windows, spike definition, baselines, construction pins, or FA grid after A1 is touched; E4's sensitivity results are reported as they fall and do not rescue the verdict.

## 3.6 Pre-registered secondary analyses {#sec-3.6}

> seed: Equation @EQ-6 — Persistence-sign criterion sign[R̄(h, h+w_f) − R̄(h+w_f, h+w_s)] with R̄ the mean ACF over half-open lags [a, b), the exact discrete form of Thm 8b (cited; Amendment 4.1) {#EQ-6}
> seed: `S4` E1 assumes approximate weak stationarity of y; y drifts upward on A1, so E1 is a consistency check {#S4}

## 3.7 Synthetic validation suite and the reading rules fixed before E2 {#sec-3.7}

> seed: **ARG-16.** Beside REFUTE, the registered reading rules (Amendment 15.3–15.21): REFUTE is the planted null's modal outcome on the A1 layout; the kill rule's measured power against short precursors; the planted-effect and positive-control rates; D_div's lead response; the chance-lead asymmetry; and, since every detection rate on A1 is at most 50 %, the F1 fallback rates. REFUTE says D_div's mean lead did not exceed the best baseline's at matched FA, not that precursors are absent  @TBL-9 0 0.825 0.025 15.5 [77, 311] 0.4925 ALL PASS 2
> seed: See @app-A @sec-4.3 @TBL-9 (suite and the reading rules).

## 3.8 Deviations, amendments and discrepancies {#sec-3.8}

> seed: `S15` E2's resampling stream was `default_rng(20261030)` (Amendment 7.4) rather than the 15.9 spawned stream; it affects only p05 (not computed for REFUTE) and argmax (identical under any draw when every lead is 0); E1 and E5 report both streams (D-05) {#S15}
> seed: See @app-D @S15 (amendments and discrepancies).

# 4 Results {#sec-4}

> seed (map): 4.1 Events; 4.2 E2 verdict; 4.3 Reading the verdict (severity, kill-rule power, D_div response, chance leads); 4.4 FA-grid frontier; 4.5 E1; 4.6 E4; 4.7 E5; 4.8 Exploratory diagnostics X1–X3

## 4.1 Events {#sec-4.1}

## 4.2 E2 verdict {#sec-4.2}

> seed: Figure @FIG-2 — One A1 event: g, D, loss, and each detector's alarm state in the scan window (event chosen by a rule fixed before data: the median-lead event) {#FIG-2}
> seed: Figure @FIG-4 — Lead distributions per detector at headline FA, with detected, concurrent and miss counts beside each {#FIG-4}
> seed: Table @TBL-3 — E2 at headline FA: per detector matchable, θ, realised/n*, mean and median lead, detected, concurrent, misses; C_b, C_min, verdict {#TBL-3}

## 4.3 Reading the verdict {#sec-4.3}

> seed: Table @TBL-9 — Reported beside E2 (15.3–15.21): label rates under planted null, planted effect and positive control at the selected and extension cells; decision-flip power; F1 fallback; chance-lead asymmetry; D_div lead response {#TBL-9}
> seed: [@Kim-2026b] method-precedent: a fast–slow divergence onset detector compared against a level rule (§5.1.2, fixed threshold on D); the expanding-percentile score used here is new to this paper.

## 4.4 FA-grid frontier {#sec-4.4}

> seed: Figure @FIG-3 — False-alarm-rate frontier per detector on A1 (mean lead and detection rate vs FA over the reported grid; D_div's unmatchable points marked); also the stand-alone image IMG-01 {#FIG-3}
> seed: See @FIG-3 @app-C (frontier detail).

## 4.5 E1 {#sec-4.5}

> seed: **ARG-10.** The E5 alignment control is degenerate at the headline FA (D_div never alarms; stated in advance) and the E4 sensitivity variants (windows, pins, censoring, resampling) re-match every threshold and none makes D_div matchable; E4 is reported as sensitivity, never rescue. E1, the persistence-sign consistency check, is INDETERMINATE  @FIG-5 @TBL-5 0 0 True 0 INDETERMINATE
> seed: `S16` E1's 128-observation block-permutation null is likely too narrow (y remains autocorrelated beyond 128 lags), which can only make its p too small; it cannot turn INDETERMINATE into CONSISTENT (DECISIONS 64) {#S16}

## 4.6 E4 {#sec-4.6}

> seed: Table @TBL-5 — E4: C_min and D_div matchability under each sensitivity variant {#TBL-5}
> seed: See @TBL-5 @app-C (sensitivity detail).

## 4.7 E5 {#sec-4.7}

> seed: Figure @FIG-5 — E5: D_div advance-ordering rate, real vs circularly shifted alarm series (degenerate at headline; shown as such) {#FIG-5}
> seed: `S17` E5's registered circular shift runs over the concatenated kept series and so crosses its gaps; immaterial here because D_div never alarms at headline FA {#S17}

## 4.8 Exploratory diagnostics X1–X3 {#sec-4.8}

> seed: **ARG-17.** EXPLORATORY (plan fixed before computation, DECISIONS 48): a gradient-norm rise before A1's spikes is present but concentrated in the last 10-step logging interval (X1 v2), and D_div is unmatchable on every sub-series (X2), so the failure is a property of the detector at this cadence, not of data coverage  @FIG-8 0.08444 10 1
> seed: Figure @FIG-8 — X1 (EXPLORATORY): event-locked mean of y before and after the spike, events vs disjoint-tile controls {#FIG-8}
> seed: `S18` X1–X3 are EXPLORATORY; X1's controls are disjoint tiles but abut, so the Mann–Whitney p is approximate; the v1 result (overlapping controls) is superseded and not quoted (DECISIONS 62–63) {#S18}
> seed: See @FIG-8 @sec-5.1 (exploratory diagnostics and their reading).

# 5 Discussion {#sec-5}

> seed (map): 5.1 Why D_div could not be matched; 5.2 What the null does and does not say; 5.3 Relation to the curvature boundary; 5.4 Threats to validity

## 5.1 Why D_div could not be matched {#sec-5.1}

## 5.2 What the null does and does not say {#sec-5.2}

> seed: `L-08` Does NOT show that gradient-norm precursors are absent; REFUTE is the planted null's modal outcome on this layout, and the kill rule's power is stated beside it {#L-08}

## 5.3 Relation to the curvature boundary {#sec-5.3}

> seed: **ARG-14.** The lag view and the curvature boundary are complementary: the boundary says where instability is; a logged-scalar alarm watches what precedes the crossing; this null bears on the alarm, not on the boundary [@Bai-2026a] [@Cohen-2021] [@Cohen-2022]
> seed: `L-06` Does NOT replace curvature-based analysis; no Hessian quantity is measured {#L-06}

## 5.4 Threats to validity {#sec-5.4}

> seed: `L-03` Does NOT claim the result for β₂ other than 0.95, or for architectures, scales or logging cadences other than A1's {#L-03}
> seed: `L-04` Does NOT claim savings of any size; no detector warned at the headline rate {#L-04}
> seed: `L-07` Does NOT evaluate mitigation (clipping, rewinds) {#L-07}
> seed: `L-09` Does NOT extend beyond A1's covered ranges and 10-step logging cadence (S11, S14) {#L-09}

# 6 Conclusion {#sec-6}

> seed (map): Verdict restated with limits-of-claim; registered forward claim (the kill rule and grading day, as registered); data and code availability; AI-assistance disclosure

> seed: `C-01` Claim A on the primary run: E2 REFUTE (C_min ≤ 0) by a tie at zero — D_div was not matchable at headline FA and no detector led any event; §K STOP; stated with the reading rules beside it {#C-01}
> seed: `C-02` E3 (replication on A2–A6) was not run: the registered stop rule ended the project before the other runs were staged; no replication claim is made {#C-02}
> seed: `C-04` E5 alignment control is degenerate at headline FA (no D_div alarms); E4 variants do not make D_div matchable; E1 is INDETERMINATE {#C-04}
> seed: `C-05` EXPLORATORY: a gradient-norm rise precedes A1's spikes but sits in the last logging interval; at a 10-step cadence a 320-step fast window cannot exploit it {#C-05}
> seed: `L-10` Does NOT offer D_div as a deployable monitor; the refuted detector is not shipped as a tool (DECISIONS 61) {#L-10}

# Appendix A {#app-A}

> seed (map): Synthetic validation suite: cells, reference agreement, A1-structure layout, reading-rule cells

# Appendix C {#app-C}

> seed (map): Construction pins, E4 sensitivity tables, FA-grid frontier detail

# Appendix D {#app-D}

> seed (map): Data provenance (per-file sources and hashes); amendment log since `prereg-v1`; Discrepancy Register summary

# References

[Bai-2026a] Bai, Zhou, Zhao, Li, Li, Xiong, Yang, Zhang & Xu, Adaptive Preconditioners Trigger Loss Spikes in Adam, ICML 2026, arXiv:2506.04805
[Bai-2026b] Bai, Zhao, Zhou, Xu & Zhang, Towards Understanding Adam Convergence on Highly Degenerate Polynomials, arXiv:2603.09581 (2026)
[Chowdhery-2023] Chowdhery et al., PaLM, 2023, §5
[Cohen-2021] Cohen et al., Gradient Descent … Edge of Stability, ICLR 2021
[Cohen-2022] Cohen et al., Adaptive Gradient Methods at the Edge of Stability, arXiv:2207.14484
[Fatima-2025] Fatima, A Proactive Reliability Metric…, EMNLP 2025 Industry Track, 2897–2913
[Huang-2025a] Huang et al., SPAM, ICLR 2025, arXiv:2501.06842
[Huang-2026] Huang et al., GradientStabilizer, ICML 2026, arXiv:2502.17055
[Kim-2026a] Kim, J. (2026). The Adaptation Rate Theorem: Predictable Lead Times in Multi-Scale Trailing Measures. DOI 10.5281/zenodo.20650165
[Kim-2026b] Kim, J. (2026). Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology. DOI 10.5281/zenodo.21081981
[Kim-2026c] Kim, J. (2026). The Divergence Theorem for Regime Transition Detection. DOI 10.5281/zenodo.20820524
[Kim-2026d] Kim, J. (2026). The Measurement Trap: How Backward-Looking Measurements Destabilize the Systems They Were Designed to Protect. DOI 10.5281/zenodo.21206946
[Kingma-2015] Kingma & Ba, Adam, ICLR 2015
[Kumar-2025] Kumar et al., ZClip, arXiv:2504.02507
[Ma-2022] Ma, Wu & E, MSML 2022, PMLR 145:671–692
[Molybog-2023] Molybog et al., A Theory on Adam Instability…, arXiv:2304.09871
[Shazeer-2018] Shazeer & Stern, Adafactor, ICML 2018, arXiv:1804.04235
[Takase-2025] Takase et al., Spike No More, COLM 2025, arXiv:2312.16903
[Tang-2026] Tang, Chen & Liu, Beyond Quadratic Loss: The Stability Phase Diagram of Adam, arXiv:2609.18314
[trainscope-2026] trainscope (PyPI; kaelvalen/trainscope @ 0651b25)
[Walsh-2025] OLMo team (Walsh et al.), 2 OLMo 2 Furious, arXiv:2501.00656
[Wang-2025] Wang et al., AdaGC, arXiv:2502.11034
[Wortsman-2023] Wortsman, Dettmers et al., Stable and low-precision training…, NeurIPS 2023, arXiv:2304.13013
