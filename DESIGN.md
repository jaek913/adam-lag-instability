# DESIGN — Measurement-Lag Instability in Adaptive Optimizers

Dated 2026-10-30. **Status: PRE-FREEZE integrated specification (JAE decision 2026-10-30, Option 2).** Built from planning doc v0.5 Part 3 (planning/adam-lag-instability_planning.md, MD5 b055fc5963206e5334d8bf35c1cbca07, committed at b64c451) with Phase 0 carry-forwards 1–10 folded in; every change from v0.5 is listed in §D.9. Before the `prereg-v1` commit this file may be revised in place. **From the `prereg-v1` commit onward it is append-only: every change is a dated amendment appended below §D.9, never an edit**, with its rationale in DECISIONS.md. No amendment to §K's thresholds, windows, spike definition, or false-alarm grid is permitted after A1 is touched.

Companion files: THESIS.md (claims, falsifiers, Date station), PRIOR_ART.md (novelty gate; §4 scope of Claim A; §5 edge-of-stability distinction), DECISIONS.md (entries 1–2 + Addendum A).

## D.0 Governing facts and scope

- **No data has been touched.** All A1–A6 staging happens after the public `prereg-v1` commit (DECISIONS entry 1). Everything below is fixed before any hashed input exists.
- **Realised β₂ of every Leg A run is 0.95** (OLMo-0424 and OLMo 2 7B/13B configs: AdamW betas [0.9, 0.95]; second-moment window W = 1/(1−β₂) = 20 steps; global clipping max_grad_norm = 1.0). Consequences: (i) Leg A tests Claim A's early warning *independent of β₂* — the detector reads the gradient norm, not the optimizer state; (ii) Claim B's mechanism is tested only on Leg B's β₂ grid (D.4), which includes 0.95; (iii) the window pair (32, 128) is longer than the optimizer's own 20-step second-moment memory, which is stated in the Methods and probed by E4.
- **Scope of Claim A** (PRIOR_ART §4): the deployed current-versus-EMA tests (ZClip, SPAM, trainscope z-score) are fast–slow divergences with a one-step fast window. This paper's contribution is the smoothed fast window (w_f = 32, r = w_s/w_f = 4, inside the Divergence Theorem's Theorem 14 band r* in [3, 7]) plus the Adaptation Rate Theorem lead bound. E2 tests whether smoothing beats the raw-reading tests at matched false-alarm rate; if it does not, that is a reportable finding against Claim A.
- **Scope of Claim B** (THESIS Amendment A1): a Hessian-free, closed-form, observable-only predictor of the established second-moment lag mechanism — not a new mechanism.

## D.0a Specification budget (anti-fishing disclosure, half 1)

- **Leg A:** 1 primary detector specification (D_div); 4 baselines (B1 rolling z-score, B2 fixed threshold, B3 ZClip EMA z-score, B4 CUSUM); 1 window pair (32, 128); 1 spike definition; 1 scan window; 1 headline false-alarm rate (1 per 10,000 steps) on a 4-point FA grid. Sensitivity (reported, no verdict): 2 alternate window pairs; baseline construction-pin sweeps listed in D.7; 1 alternate segment de-duplication rule.
- **Leg B:** 1 model configuration; 1 (β₂ × LR) grid of 6 × 4 = 24 runs; 1 seed per cell + 1 replicate seed on 4 boundary-adjacent cells (28 runs). Sensitivity: b_g ±50 %; φ-prior sweep (D.4.0).
- No other specifications are planned. Any addition is a dated amendment. The number actually tried is disclosed at Phase 4 (half 2).

## D.1 Data manifest (Leg A) — all public; staged and hashed only after `prereg-v1`

| id | Source and exact identifier | Metrics needed per step | Role |
|---|---|---|---|
| A1 | OLMo-0424 7B (formerly OLMo 1.7-7B). W&B (CoreWeave Forge) project `ai2-llm/OLMo-7B`, group `OLMo-1.7-7B` (pretraining only): **25 segment runs** `OLMo-1.7-7B-run-001` … `run-025`, created by AI2's copy_wandb_runs.py; each has a wandb-history artifact `run-<id>-history:vN` (e.g. run-025 = `u3obk6mj`, `run-u3obk6mj-history:v2`). Training config: allenai/OLMo `configs/official-0724/OLMo-7B-0424.yaml`. | `optim/total_grad_norm` (pre-clip, per trainer code), `train/CrossEntropyLoss`, learning rate, step | PRIMARY (spiky run). The anneal group `OLMo-1.7-7B-anneal` is excluded: different LR regime, not part of the registered question. |
| A2 | OLMo 2 7B stage 1. W&B project `ai2-llm/OLMo-2-1124-7B`; runs enumerated at staging from the project's public stage-1 group/report. Config `configs/official-1124/OLMo2-7B-stage1.yaml`. | same | stabilized control |
| A3 | OLMo 2 13B stage 1. W&B project `ai2-llm/OLMo-2-1124-13B`; enumerated as A2. Config `configs/official-1124/OLMo2-13B-stage1.yaml`. | same | replication |
| A4 | OLMo 2 32B. Logs on **Comet** (`comet.com/ai2/olmo-2-0325-32b`), not W&B. **Included only if** a full-resolution per-step pre-clip gradient-norm series and per-step loss can be downloaded from the public Comet project; otherwise excluded, with the reason recorded in SOURCES.md before any analysis. | same | replication (conditional) |
| A5 | BLOOM 176B TensorBoard logs. Included only if a per-step gradient norm is logged; decided at staging, recorded before any analysis. | same | replication (conditional) |
| A6 | Any further public run with per-step pre-clip gradient norm, enumerated at staging. The list is closed before the first analysis run; nothing is added after. | same | replication |

**Staging route (DECISIONS entry 2 Addendum A), in priority order:** (1) in-browser download of each segment run's wandb-history artifact files (run → Artifacts → `run-<id>-history:vN` → Files → parquet) — the full logged per-step table; (2) fallback, only if (1) fails: per-run chart CSV export (Workspace → chart ⋯ → Export CSV); (3) last resort: a full export requested from AI2 (olmo@allenai.org). The W&B public API is not a route: an outside key cannot read ai2-llm runs, listings, or artifacts (DECISIONS entry 2).

**Per-file record (SOURCES.md):** source URL; run name and id; artifact name and version (route 1) or chart and export settings (route 2); download timestamp (UTC); file size; SHA-256; project-local store path (`C:\Users\jaek9\Documents\LaggingTruth\data-stores\adam-lag-instability`). Replicator tolerance: exact (static copies).

**Completeness check (every segment, every route, before any analysis):** the set of logged steps must be contiguous between the segment's first and last step (count of rows = last − first + 1, no duplicate steps within a segment), and the column `optim/total_grad_norm` must be present by NAME. A segment failing this check is not used; if A1 cannot be assembled to full per-step resolution by routes 1–3, A1 is recorded as unavailable, E2 cannot run, and §K's grading day records that fact (D.3 §K).

**A1 assembly (construction pin P-SEG):** segments are ordered by first step. Where two segments overlap in step (a restart from a checkpoint), the rows of the **later** segment are kept for the overlapping steps, because training resumed from the checkpoint and the later segment is the trajectory that continued. Sensitivity: keep-earlier rule, reported in E4. Gaps between segments (steps present in no segment) are recorded; no window (fast, slow, spike baseline, scan) is computed across a gap — windows restart after a gap and the minimum-history rule (D.2) applies again.

**Pre-clip assertion (per run):** `optim/total_grad_norm` is the global gradient norm computed before clipping in allenai/OLMo `olmo/optim.py` (verified at main 090253d, DECISIONS entry 2). At PRV the April-2024 training commit recorded in each run's config is checked for the same order; a run where the logged norm is post-clip is flagged and reported separately, never pooled.

## D.2 Operators (Leg A)

All operators are causal (use data at or before step t only). Steps are optimizer steps.

- **Observable:** g(t) = `optim/total_grad_norm` at step t (pre-clip); y(t) = ln g(t). Non-positive or non-finite g(t) is dropped and counted (D.6).
- **Loss:** L(t) = `train/CrossEntropyLoss` at step t.
- **Fast/slow averages:** simple moving averages of y over the last w_f = 32 and w_s = 128 steps (ratio 4, Divergence Theorem Thm 14 band). Sensitivity pairs (16, 64) and (64, 256), reported, no verdict.
- **Divergence:** D(t) = SMA_32(y)(t) − SMA_128(y)(t).
- **Detector score D_div:** P_D(t) = empirical percentile of D(t) among all D(s), s ≤ t, in the assembled series; minimum history 1,000 steps (no score before). Alarm when P_D(t) ≥ θ_div.
- **Persistence-sign prediction (E1, fixed before any correlation is computed):** predicted sign of Corr(D_t, y_{t+16}) from the Divergence Theorem's Theorem 8b criterion R̄(h, h+w_f) − R̄(h+w_f, h+w_s) at h = 16, using the ACF of y measured on A1. Expected: positive.
- **Spike definition (mechanical, frozen 2026-10-30):** a loss spike at step t if L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), k = 4. Spikes within 200 steps of a prior spike are merged into one event; the event time is the first step of the event. NaN/inf loss at a step counts as exceeding the threshold.
- **Baselines** (each produces a scalar score s_b(t); alarm when s_b(t) ≥ θ_b):
  - **B1 rolling z-score:** s_1(t) = (y(t) − mean_50(y)) / sd_50(y), trailing 50-step window. Window 50 is a **construction pin P-B1** (not attributed to any tool); sweep {25, 50, 100}, reported, no verdict.
  - **B2 fixed threshold:** s_2(t) = y(t).
  - **B3 ZClip EMA z-score (documented defaults, ZClip arXiv 2504.02507 / PyPI `zclip`):** on g (not y), EMA mean μ_t and EMA variance v_t with α = 0.97, initialized from the first 25 steps (documented warm-up); s_3(t) = (g(t) − μ_{t−1}) / sqrt(v_{t−1}). Statistics are updated with the raw g(t) (monitor mode, no clipping) — **construction pin P-B3**; sweep: update with ZClip's adjusted value instead, reported, no verdict. The documented decision threshold z = 2.5 is also reported as an un-matched operating point.
  - **B4 CUSUM (trainscope 1.10.0 default `ChangePointDetector`, source kaelvalen/trainscope @ 0651b25):** robust z(t) = (y(t) − median_200(y)) / (1.4826·MAD_200(y)) over the trailing 200 observations, minimum 30 observations; positive accumulator S⁺(t) = max(0, S⁺(t−1) + z(t) − k) with slack k = 1.0; s_4(t) = S⁺(t); accumulator reset to 0 after each alarm. trainscope applies this to loss; here it is applied to y so every detector reads the same observable, and only the upward side is used because the target is a rise in gradient norm — **construction pin P-B4**; sweep: two-sided as in trainscope, and applied to g instead of y, reported, no verdict. The documented decision threshold h = 6.0 is also reported as an un-matched operating point.
- **Alarm onset:** the first step of each run of consecutive steps with score ≥ θ. Only onsets count (for every detector).
- **False-alarm rate:** alarm onsets per 10,000 steps falling outside every scan window. **FA grid:** {0.5, 1, 2, 5} per 10,000 steps; **headline FA = 1 per 10,000** (frozen 2026-10-30).
- **Threshold matching (construction pin P-FA):** for each detector, θ is swept over the empirical quantiles of its score; the operating θ for a target FA is the one whose realised FA is closest to the target from below (≤ target); ties go to the larger θ.
- **Scan window and lead:** for an event at t_e, the scan window is [t_e − 128, t_e]. Lead = t_e − (first alarm onset in the scan window). An event with no alarm onset in its window has lead 0 (no warning) — **construction pin P-MISS**; the miss rate is reported per detector. Left-censoring (an alarm already active at t_e − 128) is reported per Adaptation Rate Theorem §5.2 conventions.
- **Event eligibility:** an event is eligible if every detector has a defined score over its whole scan window (i.e., at least 1,000 steps of history and no gap inside the window). Ineligible events are counted and reported.
- **Control:** block-shuffle null on y (block 128 steps, 1,000 draws): D_div's lead ordering under permutation, per the Adaptation Rate Theorem shuffle-control convention.

## D.3 Experiments (Leg A) — classification, severity, report form

- **E1 — Persistence-sign check on A1.** Type: hypothesis test (sign). Rule: realised sign of Corr(D_t, y_{t+16}) equals the D.2 predicted sign → SUPPORT; opposite sign → REFUTE. Report: verdict + ρ with block-permutation z. Severity: near-identity on persistent y; labelled a consistency check.
- **E2 — Lead-time comparison on A1 (PRIMARY; carries §K).** Type: comparative/benchmark (verdict). Statistic: for each baseline b, C_b = median lead(D_div) − median lead(B_b), all at headline FA; C_min = min over b in {1, 2, 3, 4} of C_b. Uncertainty: 1,000 joint resamples of eligible events (block bootstrap over events; every detector re-evaluated on the same resample); C_min is computed **within each resample** (per-resample minimum contrast, Standard v1.9.11), never by comparing marginal intervals. Outcome partition (every result maps to exactly one label):
  - **SUPPORT:** C_min > 0 and the 5th percentile of the resampled C_min > 0 (90 % two-sided interval excludes zero).
  - **INCONCLUSIVE:** C_min > 0 but the 5th percentile ≤ 0; reported with the measured detection probability at the observed effect (Standard v1.9.11). Leg B proceeds.
  - **REFUTE (= §K KILL):** C_min ≤ 0.
  - **INSUFFICIENT EVENTS:** fewer than 5 eligible events on A1 → no verdict; reported as such with the suite's power at that count; §K records the condition on its grading day.
  Also reported: lead distributions, miss rates, censoring rates, the full FA-grid frontier per detector (figure), and the per-resample argmax probability over {D_div, B1, B2, B3, B4}. Severity: quantified by the synthetic suite (D.5) at the realised event count.
- **E3 — Replication on A2–A6.** Type: replication (verdict). Rule: on runs with ≥ 3 eligible events, SUPPORT if the sign of C_min matches E2's on a majority; otherwise REFUTE; runs with < 3 events are reported descriptively. A2/A3 are stabilized runs and may have few events; that is reported, not repaired.
- **E4 — Sensitivity.** Type: robustness (no verdict; qualifies E2). Window pairs (16, 64), (64, 256); construction-pin sweeps P-B1, P-B3, P-B4, P-SEG.
- **E5 — Shuffle control.** Type: boundary/characterization (report form). Reporting commitment: pooled advance-ordering rate on shuffled vs real y; a flag trips if the shuffled lead exceeds the real lead (the "lead" would be window arithmetic with no data content).

### §K — Kill rule (pre-registered)

**Grading day:** `prereg-v1` commit date + 21 days. The concrete calendar date is written here and in THESIS.md's Date station in the `prereg-v1` commit itself: **[written at the prereg-v1 commit]**. On that day the verdict is recorded in DECISIONS.md and RECORD.md whether or not E2 has run; an unrun E2 (including A1 unavailable under D.1) is itself recorded and the day is re-set once, by dated amendment.

**Rule:** after E2's single real run on A1: if E2 is **REFUTE (C_min ≤ 0)** — D_div's median lead at FA = 1 per 10,000 steps does not exceed that of the best of B1–B4 — the project STOPS. The negative is written up as a short null note (Standard: the null is the paper), filed in the repo and on Zenodo, with RECORD.md as the closing artifact; Leg B does not run. INCONCLUSIVE or SUPPORT → Leg B proceeds. No re-tuning of windows, spike definition, baselines, construction pins, or FA grid after A1 is touched; E4's sensitivity results are reported as they fall and do not rescue the verdict.

## D.4 Leg B (pinned now; executes only if §K does not kill)

- **D.4.0 Pre-run classification (completed BEFORE `prereg-v1`).** A committed script computes the criterion's stable/unstable classification of all 24 grid cells from prior φ values (no data), across a φ-prior sweep **P-PHI = {0.5, 0.8, 0.9, 0.95, 0.99}** with b_g at its pin (below) and ±50 %. The trigger is evaluated at the sweep's median (φ = 0.9): **if fewer than 6 cells classify as unstable, the D.4 fallback applies** (E6 re-characterized as a characterization of spike rate vs (φ, W, LR) with the criterion's ordering as the reporting commitment; the E6 verdict is withdrawn), recorded here before `prereg-v1`. The script, its output, and the boundary-adjacent cells it identifies (for the 4 replicate seeds) are committed with the pre-registration. Result: **[filled by the committed pre-classification run before prereg-v1]**. Context: in The Measurement Trap the exponential kernel was one of the stability-restoring reforms, so the criterion may classify most cells stable.
- **Model and data:** GPT-2-small class, 124M parameters, nanoGPT-style code committed; data FineWeb-Edu 10B subset — **exact shard list + hashes: to resolve before prereg-v1**; sequence 1,024; **batch size: to resolve before prereg-v1**; 5,000 steps per run; bf16; AdamW, β₁ = 0.9, weight decay 0.1, warm-up 200, cosine to 10 %; gradient clipping DISABLED (clipping is itself a controller and would confound the loop).
- **Grid:** β₂ in {0.95, 0.98, 0.99, 0.995, 0.999, 0.9999} × peak LR in {3e-4, 6e-4, 1.2e-3, 2.4e-3}; seeds fixed and listed; 24 primary runs + 4 replicate seeds at the boundary-adjacent cells from D.4.0 (identified from the pre-run computation, not from results). β₂ = 0.95 matches the realised β₂ of every Leg A run.
- **Measured per run:** per-step loss, global gradient norm, per-step squared gradient norm g²(t); spike count (D.2 definition); divergence flag (loss > 2 × initial or NaN).
- **Criterion inputs:** φ = lag-1 autocorrelation of g²(t) over steps 500–5,000 (levels, not differences; The Measurement Trap S-4 convention); W_eff = 1/(1−β₂); kernel = exponential (The Measurement Trap §3.5 closed form; not the uniform-kernel π²/2 constant); b_g = linearized feedback gain of the Adam update in the criterion's units — **construction pin P-BG**, candidate b_g ∝ LR / sqrt(v̄) at the step-500 state, with a ±50 % sweep reported. If no defensible linearization exists at Phase 2, E6 is re-classified as the characterization above and its verdict withdrawn, by dated amendment.
- **E6 — Criterion classification test.** Type: hypothesis test (comparative). Rule: spike rate (spikes per 1,000 steps) of criterion-unstable cells > criterion-stable cells, one-sided Mann-Whitney, α = 0.05; requires ≥ 6 cells in each class (enforced by D.4.0). SUPPORT / REFUTE accordingly. Report: verdict + per-cell table.
- **E7 — Diagnostic ordering.** Type: characterization. Reporting commitment: Spearman of b_g·S against spike rate across all cells, with permutation interval; reported regardless of E6.
- **E8 — Early warning on own runs.** Replication of E2 on the Leg B runs pooled (≥ 3 eligible events required), same operators and baselines.

## D.5 Synthetic validation suite (committed and ALL PASS before any hashed-data run)

- Planted effect: synthetic y(t) with AR(1) persistence in the measured range, planted spikes preceded by ramps of length L in {25, 50, 100, 200}; the whole pipeline (assembly → detectors B1–B4 and D_div → threshold matching → leads → C_min → rule) must recover lead(D_div) ≈ L − (w_s − w_f)/2 within tolerance and the planted margin over each baseline.
- Planted null: spikes with NO precursor ramp; D_div must not beat the best baseline (false-support rate ≤ 0.05 at the realised event count).
- Planted decision flip: ramps shorter than the raw-reading baselines' response; the rule must return REFUTE.
- Dynamic range: lead distributions separate at planted L differences of 25 steps; a planted-ties probe for C_min.
- Regime span (Standard v1.9.11): event counts {5, 10, 20, 40} and AR(1) persistence spanning the plausible range; the run reports which cell the realised A1 data lands in; outside the span → resolution re-measured before any INCONCLUSIVE is interpreted.
- Assembly probes: overlapping segments, gaps, duplicate steps, a missing `optim/total_grad_norm` column, and a point-sampled (incomplete) segment — each must be caught by D.1's checks.
- Leg B: synthetic AR(1) g² with known φ under a simulated exponential-kernel loop at known gain; the criterion must classify planted-stable/unstable correctly across the boundary; planted-ties probe for E7.
- Broken fixture: verify.py must fail on a corrupted hash, an out-of-tolerance value, and an unsigned CIC flag.

## D.6 Pre-Run Verification Protocol

Standard v1.9.12 six-pass audit per experiment, F-numbered in DECISIONS.md, sign-off comment before each run command. Project-specific items: (1) column names resolved by NAME across segment copies and across OLMo v1 vs v2 schemas; (2) step monotonicity and duplicates within and across segments (P-SEG); (3) pre- vs post-clip gradient norm asserted per run against the training commit in the run config; (4) loss cadence (per step vs per micro-batch) asserted; (5) NaN / non-positive g handling counted; (6) realised β₂ read from each run's config and stated; (7) completeness check of D.1 re-run at read time with SHA-256 re-verification.

## D.7 Construction-pin register

| Pin | Value | Sensitivity (reported, no verdict) |
|---|---|---|
| P-SEG | later segment wins on overlapping steps; no window crosses a gap | keep-earlier |
| P-B1 | rolling window 50 | {25, 50, 100} |
| P-B3 | ZClip statistics updated with raw g (monitor mode) | update with ZClip's adjusted value |
| P-B4 | CUSUM upward side only, on y | two-sided; on g |
| P-FA | operating θ = realised FA closest to target from below; ties → larger θ | — (reported FA grid) |
| P-MISS | missed event has lead 0 | miss rate reported |
| P-PHI | φ-prior sweep {0.5, 0.8, 0.9, 0.95, 0.99}; trigger at 0.9 | full sweep reported |
| P-BG | b_g ∝ LR / sqrt(v̄) at step 500 | ±50 % |

Frozen (not pins): k = 4; spike dedup 200 steps; headline FA = 1 per 10,000 steps; windows (32, 128); scan window 128; minimum history 1,000 steps.

## D.8 Open before `prereg-v1` (not yet resolved; each closes by an edit to this file before the freeze)

1. D.4.0 pre-classification run and result.
2. Leg B FineWeb-Edu shard list + hashes; batch size.
3. THESIS.md amendments in the same change set: (a) Claim A falsifier sentence → "best of the four baselines" (matches §K); (b) β₂ framing (CF 10).
4. §K and THESIS Date station concrete grading date — written in the `prereg-v1` commit itself.

## D.9 Pre-freeze change log (2026-10-30) — differences from planning doc v0.5 Part 3

Each entry: carry-forward (CF) number; what motivated it; the v0.5 text it replaces (v0.5 = planning/adam-lag-instability_planning.md, MD5 b055fc5963206e5334d8bf35c1cbca07).

- **CF 1 — Baselines B3/B4; §K against the best baseline on the per-resample minimum contrast.** Motivated by PRIOR_ART.md §2 and §4 (ZClip and trainscope CUSUM are the deployed tools) and Standard v1.9.11. Replaces v0.5 D.0 "2 baselines", D.2 "Baseline B1 … Baseline B2", D.3 E2 "median lead(D_div) > median lead(B1) AND > median lead(B2), with the paired difference's block-bootstrap 90% interval excluding zero", and §K "does NOT exceed median lead(B1)". Now D.0a, D.2 (B1–B4), D.3 E2 (C_min), §K.
- **CF 2 — Strike the "trainpulse-class default" attribution.** Motivated by PRIOR_ART.md §2 (trainpulse's window not confirmable). Replaces v0.5 D.2 "Window 50 matches the published default of trainpulse-class monitors." Now construction pin P-B1 with sweep.
- **CF 3 — Leg B pre-run classification; fallback below 6 unstable cells.** Motivated by PRIOR_ART.md §8 item 3 (The Measurement Trap's exponential kernel was a stability-restoring reform). Adds D.4.0; the v0.5 E6 clause "if the pre-run classification yields fewer, the grid is amended before the run" is replaced by the D.4.0 trigger and fallback.
- **CF 4 — Claim A scope relative to w_f = 1 detectors.** Motivated by PRIOR_ART.md §4 (JAE, 2026-10-30). New text in D.0 and D.5 (planted decision flip against raw-reading baselines). No v0.5 text replaced.
- **CF 5/6 — A1 data route, segmented structure, completeness check.** Motivated by DECISIONS.md entry 2 and Addendum A. Replaces v0.5 D.1 A1 row "OLMo-0424 7B, W&B run export" and "Export path: W&B public API → CSV per run; SHA-256 per file". Now D.1 A1 row (25 segments), staging-route priority, per-file record, completeness check, P-SEG.
- **CF 7 — A4 is Comet, not W&B.** Motivated by DECISIONS.md entry 2. Replaces v0.5 D.1 "A4 | OLMo 2 32B W&B export". Now conditional inclusion on Comet.
- **CF 8 — Realised β₂ = 0.95.** Motivated by DECISIONS.md entry 2 (OLMo configs). New D.0 consequences (i)–(iii); D.6 item 6; D.4 note that the grid includes 0.95. No v0.5 text replaced in DESIGN; THESIS amendment pending (D.8 item 3b).
- **CF 9 — Metric name and pre-clip status from trainer code; training commit at PRV.** Motivated by DECISIONS.md entry 2 (allenai/OLMo @ 090253d). Replaces v0.5 D.2 "[PIN: pre-clip norm; if only post-clip is logged for a run, the run is flagged and reported separately.]" Now D.1 pre-clip assertion and D.6 item 3.
- **CF 10 — THESIS β₂ amendment.** Motivated by DECISIONS.md entry 2 (JAE, 2026-10-30). Recorded as D.8 item 3b (a THESIS change, landing with this DESIGN before the freeze).
- **Completions required by the Phase 1 checklist (not carry-forwards; JAE to confirm at review of this draft):** alarm-onset definition; threshold-matching rule P-FA; missed-event rule P-MISS; event eligibility; E2 INSUFFICIENT EVENTS branch (< 5 eligible events); E3 REFUTE branch made explicit; ZClip warm-up 25 and B3 score definition; CUSUM parameters from trainscope source; anneal group excluded from A1; φ-prior sweep P-PHI; suite regime-span and assembly probes; D.6 items 1–7. v0.5 left these unstated.
