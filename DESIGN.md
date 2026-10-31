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

## D.1 Data manifest (Leg A) — all public; staged and hashed only after `prereg-v1`

| id | Source and exact identifier | Metrics needed per step | Role |
|---|---|---|---|
| A1 | OLMo-0424 7B (formerly OLMo 1.7-7B). W&B (CoreWeave Forge) project `ai2-llm/OLMo-7B`, group `OLMo-1.7-7B` (pretraining only): **25 segment runs** `OLMo-1.7-7B-run-001` … `run-025`, created by AI2's copy_wandb_runs.py; each has a wandb-history artifact `run-<id>-history:vN` (e.g. run-025 = `u3obk6mj`, `run-u3obk6mj-history:v2`). Training config: allenai/OLMo `configs/official-0724/OLMo-7B-0424.yaml`. | `optim/total_grad_norm` (pre-clip, per trainer code), `train/CrossEntropyLoss`, learning rate, step | PRIMARY (spiky run). The anneal group `OLMo-1.7-7B-anneal` is excluded: different LR regime, not part of the registered question. |
| A2 | OLMo 2 7B stage 1. W&B project `ai2-llm/OLMo-2-1124-7B`; exact identifier = AI2's published report `https://wandb.ai/ai2-llm/OLMo-2-1124-7B/reports/OLMo-2-7B-Nov-2024--VmlldzoxMDUzMzE1OA` (linked from the allenai/OLMo README, stage-1 table, at commit 090253d; the HF model card at revision 7df9a82518afdecae4e8c026b27adccc8c1f0032 carries no OLMo 2 W&B link). The stage-1 run group and per-run list are read from the report's run set in the UI at staging; every run in that stage-1 group is included (no selection) and recorded in DECISIONS.md before the first analysis run, then closed (as A6). The report is not opened before `prereg-v1`. Config `configs/official-1124/OLMo2-7B-stage1.yaml`. | same | stabilized control |
| A3 | OLMo 2 13B stage 1. W&B project `ai2-llm/OLMo-2-1124-13B`; exact identifier = AI2's published report `https://wandb.ai/ai2-llm/OLMo-2-1124-13B/reports/OLMo-2-13B-Nov-2024--VmlldzoxMDUzMjQxNg` (same README table and commit; HF model card revision 3fefddc1bf18a30e1d9b91000271630718f2aa8b carries no OLMo 2 W&B link). Stage-1 run group and run list closed at staging exactly as A2. Config `configs/official-1124/OLMo2-13B-stage1.yaml`. | same | replication |
| A4 | OLMo 2 32B. Logs on **Comet** (`comet.com/ai2/olmo-2-0325-32b`), not W&B. **Included only if** a full-resolution per-step pre-clip gradient-norm series and per-step loss can be downloaded from the public Comet project; otherwise excluded, with the reason recorded in SOURCES.md before any analysis. | same | replication (conditional) |
| A5 | BLOOM 176B (tr11). Hugging Face repo `bigscience/tr11-176B-logs` @ `67ef5a3a19e97dd114efe55be55ffaca37683638`, files `tensorboard/main/events.out.tfevents.*`. **Included only if** a per-step gradient-norm scalar is present by name and logged every step; otherwise excluded, with the reason recorded in SOURCES.md before any analysis. | same | replication (conditional) |
| A6 | Further public runs with per-step pre-clip gradient norm, found at staging by the recorded searches "total_grad_norm" and "grad_norm" on W&B public projects, Comet public projects and the Hugging Face Hub; every hit is recorded in SOURCES.md. A hit is included only if it passes the D.1 completeness check, has ≥ 50,000 logged steps, and passes the pre-clip assertion. The list is closed before the first analysis run; nothing is added after (design review 2026-10-30, F19). | same | replication |

**Staging route (DECISIONS entry 2 Addendum A), in priority order:** (1) in-browser download of each segment run's wandb-history artifact files (run → Artifacts → `run-<id>-history:vN` → Files → parquet) — the full logged per-step table; (2) fallback, only if (1) fails: per-run chart CSV export (Workspace → chart ⋯ → Export CSV); (3) last resort: a full export requested from AI2 (olmo@allenai.org). The W&B public API is not a route: an outside key cannot read ai2-llm runs, listings, or artifacts (DECISIONS entry 2).

**Per-file record (SOURCES.md):** source URL; run name and id; artifact name and version (route 1) or chart and export settings (route 2); download timestamp (UTC); file size; SHA-256; project-local store path (`C:\Users\jaek9\Documents\LaggingTruth\data-stores\adam-lag-instability`). Replicator tolerance: exact (static copies).

**Completeness check (every segment, every route, before any analysis):** the set of logged steps must be contiguous between the segment's first and last step (count of rows = last − first + 1, no duplicate steps within a segment), and the column `optim/total_grad_norm` must be present by NAME. A segment failing this check is not used; if A1 cannot be assembled to full per-step resolution by routes 1–3, A1 is recorded as unavailable, E2 cannot run, and §K's grading day records that fact (D.3 §K).

**A1 assembly (construction pin P-SEG):** segments are ordered by first step. Where two segments overlap in step (a restart from a checkpoint), the rows of the **later** segment are kept for the overlapping steps, because training resumed from the checkpoint and the later segment is the trajectory that continued. Sensitivity: keep-earlier rule, reported in E4. **Rewind events (design review 2026-10-30, F5):** spike events are enumerated on every segment, including the portion of an earlier segment that a restart superseded. An event whose time lies in a superseded portion is a *rewind event*: it is retained, its scan window and every detector score are computed on that earlier segment's own series (which shares history with the kept trajectory up to the checkpoint step), and it is reported with a rewind flag and count. The assembled (later-wins) series is used for every other event and for the false-alarm denominator. Rewind events enter the k-ladder event count. Sensitivity: rewind events excluded, reported in E4. Dedup applies within a series; a rewind event and an assembled-series event are never merged (fix round 2026-10-30, F5). Gaps between segments (steps present in no segment) are recorded; no window (fast, slow, spike baseline, scan) is computed across a gap — windows restart after a gap and the minimum-history rule (D.2) applies again.

**Pre-clip assertion (per run):** `optim/total_grad_norm` is the global gradient norm computed before clipping in allenai/OLMo `olmo/optim.py` (verified at main 090253d, DECISIONS entry 2). At PRV the April-2024 training commit recorded in each run's config is checked for the same order; a run where the logged norm is post-clip is flagged and reported separately, never pooled.

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

## D.4 Leg B (pinned now; executes only if §K does not kill)

**Execution rule (JAE 2026-10-30):** Leg B runs whenever §K does not stop the project — E2 SUPPORT or INCONCLUSIVE. It is a characterization (D.4.1) and is **not dropped when Claim A passes**; its GPU cost (P-BATCH: ~38 GPU-hours) is accepted now. It does not run on §K KILL or INSUFFICIENT EVENTS.


- **D.4.0 Pre-run classification — NOT RUN (moot under D.4.1).** The pre-run classification of the 24 cells required a gain b_g in observable terms. D.4.1 finds none, so the fallback below is applied now and D.4.0, its φ-prior sweep (P-PHI), and the A1-measured-φ replacement rule (JAE 2026-10-30) are withdrawn. They are kept in §D.9 for the record.
- **D.4.1 Criterion source and mapping assessment (2026-10-30).** Source: The Measurement Trap, **Appendix A.4 (PRF-A4)** — not §3.5 (§3.5 is the cross-disciplinary correspondence with Campbell & Jessop). As published: the exponential kernel m(t) = α·x(t−1) + (1−α)·m(t−1) with α = 2/(W+1); companion matrix rows (φ, −b_g) and (α, 1−α); characteristic polynomial **EQ-5:** λ² − (φ + 1 − α)λ + φ(1−α) + α·b_g = 0; boundary φ(1−α) + α·b_g = 1, i.e. **EQ-6:** b_g*(exp) = (1 − φ(1−α))/α = (1−φ)/α + φ. The cumulative persistence memory **EQ-2** S = (1−φ^W)/(1−φ) and the threshold **EQ-1** b_g·S > π²/2 belong to the **uniform** kernel only. **Assessment: the A.4 boundary does not map cleanly onto Adam's second-moment loop in observable-only terms**, for three reasons: (1) in A.4 the measurement feeds back as an additive linear term −b_g·m on the measured variable; in Adam, v_t acts multiplicatively through the step size η/√v_t, and its effect on the next squared gradient runs through local curvature, so any linearized gain depends on the Hessian — which contradicts the Hessian-free scope of Claim B and is not readable from training logs; (2) timing: A.4's kernel uses x(t−1), while Adam's v_t = β₂·v_{t−1} + (1−β₂)·g_t² includes the current g_t², which changes the characteristic polynomial; (3) E7's diagnostic b_g·S is a uniform-kernel quantity with no counterpart in A.4. No mapping is constructed here. **Consequence (D.4 fallback, applied pre-freeze):** Leg B carries no Claim B verdict; E6 and E7 are characterizations; THESIS.md's Claim B falsifier is withdrawn by THESIS Amendment A2(d).
- **D.4.2 Threat to resolution from P-BATCH (stated so the design-stage review sees it).** At 98,304 tokens per step the gradient noise is several times that of the GPT-2 reference batch (~0.5M tokens). Higher noise raises the spike floor in every cell and may compress the separation in spike rate between cells the A.4 index ranks as fragile and robust. The Leg B synthetic suite (D.5) therefore spans gradient-noise levels from the reference batch up to and beyond the 98k-token level, and the run reports which noise cell the realised Leg B runs land in; a realised level outside the span means the resolution claim does not transfer and is re-measured before E6 is interpreted, by extending the suite's noise grid one pre-specified step (×2 in gradient-noise variance) per extension, at most twice, each extension a dated amendment (F14).
- **Model and data:** GPT-2-small class, 124M parameters, nanoGPT-style code committed; data per **P-DATA** (below); sequence 1,024; batch per **P-BATCH** (below); 5,000 steps per run; bf16; AdamW, β₁ = 0.9, weight decay 0.1, warm-up 200, cosine to 10 %; gradient clipping DISABLED (clipping is itself a controller and would confound the loop).
- **P-DATA — Leg B corpus, pinned without download (2026-10-30).** Hugging Face dataset `HuggingFaceFW/fineweb-edu`, revision (commit) `87f09149ef4734204d70ed1d046ddc9ca3f2b8f9` (2025-07-11), config `sample-10BT`, directory `sample/10BT/`. Identifiers and SHA-256 are as reported by the Hugging Face tree API (`/api/datasets/HuggingFaceFW/fineweb-edu/tree/<revision>/sample/10BT?expand=true`, field `lfs.oid`) on 2026-10-30; the on-disk SHA-256 of each downloaded file must match at Phase 2 staging, else the file is not used.

  | file | bytes | SHA-256 (HF-reported) | use |
  |---|---|---|---|
  | `sample/10BT/000_00000.parquet` | 2152819114 | b1ba7b2ce4cb5ea6ef42dca40263eabb85f37700d01693a68e9b30a31d78e871 | training stream (primary) |
  | `sample/10BT/001_00000.parquet` | 2152222432 | 3fcf2dc69cd52503986276d3d2d26a8c356d0f2ea28a0de4fdbda8cf87755693 | reserve — read only if 000 is exhausted |

  Not used: shards 002–013 of the same directory (the remaining twelve files; listing with sizes and hashes retained in the staging record). Token stream: documents in file row order, field `text`, tokenized with the GPT-2 BPE (`tiktoken` "gpt2"), an end-of-text token after each document, packed contiguously into 1,024-token sequences. **Every Leg B run sees the identical token order**; the seed changes initialization only. Sizing: the 10BT sample is ~10B GPT-2 tokens over 28.5 GB, so shard 000 (2.15 GB) holds ~0.75B tokens, more than one run's 0.49B under P-BATCH; the exact token count is verified at staging.
- **P-BATCH — batch size (construction pin, 2026-10-30).** 96 sequences × 1,024 tokens = 98,304 tokens per optimizer step (gradient accumulation allowed; micro-batch is a hardware choice and is logged); 5,000 steps = 491,520,000 tokens per run; 28 runs = 13.8B tokens. **Reason:** the planning budget (planning doc v0.5 Part 5) is one ≥ 16 GB GPU for ~40–80 GPU-hours; at a sustained ~100k tokens/s for a 124M model that is ~38 GPU-hours, inside budget, whereas the GPT-2 reference batch (~0.5M tokens/step) would need ~5× the compute. The batch is identical in every cell, so it cannot confound the β₂ × LR comparison. **No sweep:** a second batch size would double Leg B's compute; the smaller-than-reference batch (more gradient noise) is stated as a scope condition in the Methods.
- **Grid:** β₂ in {0.95, 0.98, 0.99, 0.995, 0.999, 0.9999} × peak LR in {3e-4, 6e-4, 1.2e-3, 2.4e-3}; seeds 1–24 for the 24 primary cells (in row-major order of the grid as written) and 101–104 for the P-REP cells (F19); 24 primary runs + 4 replicate seeds at the pre-specified central cells β₂ in {0.99, 0.995} × LR in {6e-4, 1.2e-3} (construction pin P-REP; replaces the D.4.0 boundary-adjacent rule, which D.4.1 made moot). β₂ = 0.95 matches the realised β₂ of every Leg A run.
- **Measured per run:** per-step loss, global gradient norm, per-step squared gradient norm g²(t); spike count (D.2 definition). **Divergence (P-DIV; F8):** a run diverges at the first step at which loss is NaN/inf, or at which loss exceeds the run's minimum loss to date by more than 2.0 nats for 50 consecutive steps; analysis of the run stops at that step.
- **Measured inputs for the characterization (P-PHIHAT; F9):** φ̂ = lag-1 autocorrelation of ln g²(t) after subtracting its trailing 128-step mean, over steps 1,128–5,000 (or to the divergence step); φ̂ on raw levels of g²(t) over steps 1,000–5,000 is reported as a sensitivity. α_Adam = 1 − β₂ (Adam's own EMA weight — reported beside the A.4 convention α = 2/(W+1), which would correspond to W = 2/(1−β₂) − 1); A.4 robustness index **b_g\*(exp)(φ̂, α_Adam) = (1−φ̂)/α_Adam + φ̂** (EQ-6), used only as a descriptive ordering of cells, with the D.4.1 mapping caveats stated beside it. No b_g is estimated. **Direction stated now:** on A.4's reading a larger index means a more robust loop, so A.4 predicts spike rate decreasing in b_g\*(exp).
- **Spike rate:** spikes per 1,000 steps (D.2 definition at the k-ladder rung that resolved on A1), counted over steps 1,000–5,000 or to the divergence step. A cell with fewer than 1,000 completed steps in that window has spike rate and φ̂ "undefined (diverged)" (F8). Diverged cells are reported separately.
- **E6 — Spike rate across the grid (characterization; verdict withdrawn by D.4.1).** Reporting commitment: the 24-cell table of spike rate, divergence flag and step, φ̂ and b_g\*(exp); spike rate vs β₂ at each LR and vs LR at each β₂; Spearman of spike rate against b_g\*(exp) reported twice (F8) — over cells with defined spike rate (N stated) and over all 24 cells with diverged cells assigned the top rank (ties) — each with a 1,000-draw permutation interval; beside it, the fraction of spike events that occur at the same step index in ≥ 3 cells (shared token order, F17). Reported as a characterization (no pass/fail).
- **E7 — Ordering by the A.4 index (characterization; F9).** Reporting commitment: within each LR column, Kendall τ of spike rate against b_g\*(exp) and against β₂ alone, each with a permutation interval and each computed both ways for diverged cells as in E6; a statement per column of whether the index reorders any cell relative to β₂ (if it reorders none, E7 for that column is reported as identical to ordering by β₂); and the planted-ties and planted-reorder probe results from the suite. Replaces the withdrawn uniform-kernel diagnostic b_g·S.
- **E8 — Early warning on own runs (characterization; F3, F13, F17; JAE).** Same operators and baselines as E2; thresholds matched per run by the D.2 onset-count rule; N_out and n* are reported per run and per FA target, and a run with n* < 5 at headline FA is reported as "FA not matchable" and excluded from the pooled E8 statistics, with the count of such runs stated (fix round 2026-10-30, N3); leads pooled across runs. Reporting commitment: per detector mean and median lead, detection rate, miss and censored counts; C_b and C_min with a cluster bootstrap over the 28 runs (all of a run's eligible events resampled together, 1,000 draws). No label. E8 does not feed §K and is not combined with E2; a difference from E2 is reported as a regime difference.

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

## D.6 Pre-Run Verification Protocol

Standard v1.9.12 six-pass audit per experiment, F-numbered in DECISIONS.md, sign-off comment before each run command. Project-specific items: (1) column names resolved by NAME across segment copies and across OLMo v1 vs v2 schemas; (2) step monotonicity and duplicates within and across segments (P-SEG); (3) pre- vs post-clip gradient norm asserted per run against the training commit in the run config; (4) loss cadence (per step vs per micro-batch) asserted; (5) NaN / non-positive g handling counted; (6) realised β₂ read from each run's config and stated; (7) completeness check of D.1 re-run at read time with SHA-256 re-verification.

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

## D.8 Open before `prereg-v1` (not yet resolved; each closes by an edit to this file before the freeze)

1. ~~D.4.0 pre-classification run and result.~~ **Closed 2026-10-30:** moot under D.4.1 (fallback applied).
2. ~~Leg B FineWeb-Edu shard list + hashes; batch size.~~ **Resolved 2026-10-30:** P-DATA (pinned from Hugging Face metadata, no download) and P-BATCH (D.4, D.7).
3. ~~THESIS.md amendments in the same change set:~~ **Done 2026-10-30: THESIS Amendment A2 (a)–(g)** — (a) Claim A falsifier sentence → "best of the four baselines" (matches §K); (b) β₂ framing (CF 10); (c) the INSUFFICIENT EVENTS closure under the k ladder (P-KLAD) stated beside the Claim A falsifier, as an outcome that neither passes nor kills Claim A; (d) Claim B re-scoped per D.4.1 — its falsifier (Mann-Whitney / Spearman ≤ 0) withdrawn, Claim B stated as a characterization of spike rate across the β₂ × LR grid ordered by the A.4 index; (e) citation corrected throughout from "The Measurement Trap §3.5" to "Appendix A.4 (PRF-A4), EQ-5/EQ-6" (Claim B text and Archetype line).
4. ~~§K and THESIS Date station concrete grading date.~~ **Resolved in the `prereg-v1` commit:** 2026-11-20 (2026-10-30 + 21 days), written in §K and in THESIS.md's Date station.

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
- **Completions required by the Phase 1 checklist (not carry-forwards; confirmed by JAE 2026-10-30, with the notes in the next entry):** alarm-onset definition; threshold-matching rule P-FA; missed-event rule P-MISS; event eligibility; E2 INSUFFICIENT EVENTS branch (< 5 eligible events); E3 REFUTE branch made explicit; ZClip warm-up 25 and B3 score definition; CUSUM parameters from trainscope source; anneal group excluded from A1; φ-prior sweep P-PHI; suite regime-span and assembly probes; D.6 items 1–7. v0.5 left these unstated.
- **JAE review of the completions (2026-10-30, after commit e06e338).** Accepted: P-MISS, P-FA, B3/B4 monitor-mode pins, P-PHI — with two notes applied: the miss count is reported beside each detector's median lead (D.2, D.3 E2, D.7); the source of φ = 0.9 is named (construction choice, no literature value found) and A1-measured φ replaces it by dated amendment if |Δ| > 0.05 (D.4.0, D.7). **Changed:** the < 5-event branch — replaced the single-k INSUFFICIENT EVENTS rule by the pre-registered k ladder P-KLAD (k = 4 primary, k = 3 once, then INSUFFICIENT EVENTS → project closes with a null note on event count, neither pass nor kill of Claim A), which closes the gap where §K could not fire (D.2, D.3 E2, §K, D.5, D.7). Replaces the e06e338 text "fewer than 5 eligible events on A1 → no verdict; … §K records the condition on its grading day." Also added: D.3.0 experiment index.
- **D.8 item 2 resolved (2026-10-30, JAE direction).** Leg B data pinned WITHOUT download: Hugging Face repo + revision 87f09149ef4734204d70ed1d046ddc9ca3f2b8f9 + exact shard filenames + HF-reported SHA-256 (P-DATA); on-disk re-hash at Phase 2 staging. Batch size declared as construction pin P-BATCH with its reason (budget; constant across cells). Replaces the v0.5 text "data: [FineWeb-Edu 10B subset — PIN exact shard list + hash]; … batch [PIN]".
- **JAE decisions 2026-10-30 (box 3 audit) and the D.4.1 finding.** Accepted as proposed: E1 ACF/R̄ estimation and 128-step permutation blocks; E2 event-level resampling with block-of-3 sensitivity; E5 procedure; E8 per-run matching with pooled leads; Leg B spike-rate window 1,000–5,000 with diverged cells reported separately; explicit none for deseasonalization and subsampling; thresholds re-matched in every sensitivity variant. **Changed by JAE:** E3 — strict majority SUPPORT, strict minority REFUTE, tie INCONCLUSIVE (replaces "SUPPORT if … a majority; otherwise REFUTE"). **P-BATCH:** kept, with the D.4.2 threat-to-resolution statement and a suite span covering the realised noise level. **D.4.1 (from reading The Measurement Trap source):** the cited closed form is Appendix A.4 EQ-5/EQ-6, not §3.5; it does not map cleanly onto Adam's loop in observable-only terms (multiplicative curvature-dependent feedback; current-gradient timing; S and π²/2 are uniform-kernel only); per JAE's instruction no mapping was invented and D.4's fallback was applied pre-freeze — E6/E7 recast as characterizations; D.4.0, P-PHI and P-BG withdrawn; replicate cells re-pinned as P-REP (the D.4.0 boundary-adjacent rule was moot). Replaces the e06e338/ac6c7f0 text of D.4.0, "Criterion inputs", E6, E7 and the P-PHI/P-BG rows. Source files read: project copies of The Measurement Trap (MD5 d82507b9f1cab7d991de618556e91d02) and The Divergence Theorem (MD5 c27021dd16652b1f5a88a411084dfad3), extracted with pdftotext (both are true PDFs).
- **JAE decisions 2026-10-30 (after ab5dd47).** Subtitle → "A Fast–Slow Divergence Early-Warning Signal for Loss Spikes, Tested Against Deployed Alarms on Public Training Logs" (Claim B's characterization goes in the abstract). THESIS amendments 3(a)–(e) applied as THESIS Amendment A2 (a)–(g), with Claim B's falsifier replaced by its reporting commitment. Archetype unchanged, wording "Appendix A.4, used as a descriptive index". Leg B execution rule stated at the head of D.4: runs on E2 SUPPORT or INCONCLUSIVE; not dropped at PASS; GPU cost accepted. D.8 item 3 closed.
- **Box 4 (2026-10-30).** Added §D.3.1, a one-table restatement of each experiment's type, report form and rule polarity (no rule changed except E8). **E8 (proposed, JAE to confirm):** E2's four-way partition on pooled Leg B events with a 5-event floor, replacing "≥ 3 eligible events pooled" with no stated partition.
- **Box 5 audit (2026-10-30).** Every verdict experiment checked for a complete outcome partition and an honest null. One defect found and fixed: E1's sign-only rule returned SUPPORT on a true null half the time; E1 now requires a one-sided block-permutation p ≤ 0.05 for SUPPORT or REFUTE, else INCONCLUSIVE (incl. a zero predicted criterion). Replaces "realised sign … equals the D.2 predicted sign → SUPPORT; opposite sign → REFUTE". (JAE to confirm.)
- **Box 6 (2026-10-30, JAE-confirmed).** D.1 A5 identifier pinned to HF repo + revision (metadata lookup only, no event files read). Replaces "BLOOM 176B TensorBoard logs. Included only if a per-step gradient norm is logged; decided at staging, recorded before any analysis."
- **Box 6 (2026-10-30, JAE-decided).** A2/A3 identifiers pinned to AI2's published W&B report URLs (allenai/OLMo README @ 090253d), because the OLMo 2 model cards carry no OLMo 2 W&B link (only a commented-out copy of the OLMo-1.7 links and "logs (coming soon)"). Group URLs were not taken now: reading them requires opening the reports, which render A2/A3 curves before `prereg-v1`. Stage-1 group and run list are read from each report at staging and recorded in DECISIONS.md before the first analysis run. Replaces "runs enumerated at staging from the project's public stage-1 group/report" and "enumerated as A2".
- **Stale cross-references corrected (2026-10-30, before the design-stage review; JAE direction).** §D.0 ("THESIS amendment pending (D.8 item 3d)") and §D.4.1 ("withdrawn by amendment (D.8 item 3d)") now point to THESIS Amendment A2(d), which landed at commit 958c564. No rule changed. The CF 8 entry above ("THESIS amendment pending (D.8 item 3b)") is left as written because it records the state at that time; that item closed as THESIS Amendment A2(b).
- **Design-stage adversarial review (2026-10-30; prompt + package committed at 7194a21; reviewer reply in verification/design_review_transcript.md; adjudication in verification/design_review.md).** 19 findings (3 BLOCKER, 11 MAJOR, 5 MINOR); all adjudicated before the freeze, none rebutted in full. **F1** contrast on mean lead (misses 0) instead of median; low-detection statement; suite null at 30–50 % detection. **F2 + F3 + F4 (JAE decision):** FA redefined as alarm duty cycle on out-of-window steps (grid {0.5, 1, 2, 5} %, headline 1 %), replacing onsets per 10,000 steps; thresholds matched at an exact alarm-step count n*; lead defined on alarm state; left-censored events lead 128 flagged (P-CENS), sensitivities lead 0 and excluded; the reviewer's "alarm runs touching a window are not false alarms" NOT adopted (under onset counting it lets an always-on detector win; under duty cycle all in-window steps are outside the denominator anyway); duty-cycle matching applies to E8. **F5** rewind events retained on their own segment. **F6** E5 null replaced by a circular shift of the alarm series; block shuffle kept as a second characterization. **F7** E3 replicates the direction (C_min > 0), adds NOT RUN; adapted from the reviewer's fix (E3 runs on any E2 label except INSUFFICIENT EVENTS, rather than only on PROCEED, so a kill still gets its replication reported). **F8** P-DIV divergence rule, undefined cells, Spearman twice. **F9** P-PHIHAT detrended φ̂, τ against index and against β₂, direction stated, planted reorder. **F10** suite graded against a noiseless oracle of the pipeline itself, ramps {64, 100, 150, 200}; the reviewer's max(0, L − 48) NOT adopted because the Adaptation Rate Theorem (Thm 3.1) gives the fast average's lead over the slow average, not a detector's lead over a spike — THESIS Amendment A3(b) corrects the Claim A mechanism sentence. **F11** REFUTE on point-estimate C_min; unrun-after-re-set → CLOSE. **F12** E1 relabelled CONSISTENT / INCONSISTENT / INDETERMINATE, not support for Claim A. **F13 (JAE)** E8 a characterization. **F14** E5 parenthetical removed; D.4.2 extension bounded. **F15** dropped g carried forward, gap resets listed. **F16** suite numbers fixed. **F17** cluster bootstrap over runs for E8; co-occurrence fraction for E6. **F18** chained dedup; all event windows out of FA. **F19** A6 search and inclusion rule; A2/A3 take every stage-1 run; seeds and RNG pinned (P-RNG). Replaced texts are those of DESIGN.md at 7194a21 (MD5 dd8170c9176c307d7c40288bee827154) in D.0a, D.1 (A2, A6, P-SEG), D.2, D.3.0, D.3.1, D.3, §K, D.4, D.5, D.7.
- **Design-review fix round (2026-10-30; reviewer reply 2 in verification/design_review_transcript.md; JAE decisions).** F1–F19 closed except where noted. Defects introduced by the round-1 amendments, amended before the freeze: **N1 (BLOCKER)** duty-cycle FA let each detector's alarm-run length set its chance hit rate → fix (a): alarm onset with hold H = 32 (P-HOLD), FA = onsets per 10,000 out-of-window steps (grid {0.5, 1, 2, 5}, headline 1), exact onset-count matching, realised duty cycle n*·H/N_out reported, P-CENS kept, B4 resets at each onset; D.5 adds a planted null with 1-step and 40-step baselines (false-REFUTE and false-SUPPORT ≤ 0.05). Replaces the round-1 "Alarm state", duty-cycle "False-alarm rate", alarm-step P-FA and the frozen duty-cycle headline. **N2** oracle θ matched on the noisy series and applied to the noiseless one. **N3** E8 reports N_out and n* per run; n* < 5 at headline → "FA not matchable", excluded and counted. **F4 residual** B4 path recomputed per candidate θ; non-monotone regions reported. **F5 residual** dedup within a series; rewind and assembled events never merged. **F15 residual** D_div percentile history "since the last gap". Scoped second fix-round message: verification/design_review_fixround2.md (DECISIONS entry 3).
- **Design-review fix round 2 closed (2026-10-30; reviewer reply 3 in verification/design_review_transcript.md; JAE decisions; no third round per DECISIONS entry 3 item 5).** N1, N2, N3 and the F4, F5 and F15 residuals closed. **N4 (MINOR, introduced by the N2 amendment)** amended without further review: the oracle series is the planted series with the noise amplitude scaled by 10⁻³ (not zero), and D.5 asserts every score on it is finite; replaces "noise set to zero". N1 notes (i) residual onset clustering and (ii) the meaning of P-CENS under P-HOLD are stated in D.2 as Methods statements; no rule changed. Reason recorded in DECISIONS entry 3 Addendum A.
- **Stale lines corrected before the freeze (2026-10-30, JAE; no rule change).** DESIGN §D.0 Claim A scope: "plus the Adaptation Rate Theorem lead bound" → "motivated by the Adaptation Rate Theorem (no lead bound is claimed; THESIS A3(b))"; DESIGN header: "DECISIONS.md (entries 1–2 + Addendum A)" → "entries 1–3 with addenda"; THESIS "Why it matters" pre-flight-check sentence and THESIS "Lifecycle" confirmatory-result sentence given superseded markers pointing to A2(d) and A3(c).

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
