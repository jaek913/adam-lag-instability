# OUTLINE.md — Paper Roadmap

Copied from the Research-to-Publication Standard's OUTLINE.md Template page (doc 2kydc08j-754, page 2kydc08j-514). Built from THESIS.md (MD5 532b7f062b26eda6c587a9362609928b) and DESIGN.md (MD5 eda8ea9806af114e48d06a9caf23614b, commit 7949f19), with citations from PRIOR_ART.md (MD5 0cf9c2cd8c413eed77564b8f8a1a44de). New work: every node is NEW. No values appear in this file; load-bearing numbers are named by LB-id and will live in claims.lock (Phase 3).

## Metadata

*   **Paper:** Measurement-Lag Instability in Adaptive Optimizers — A Fast–Slow Divergence Early-Warning Signal for Loss Spikes, Tested Against Deployed Alarms on Public Training Logs
*   **Archetype:** empirical-with-verified-theory (THESIS Amendment A2(f): no original theorem; The Measurement Trap Appendix A.4 used as a descriptive index)
*   **Source pin (rebuild only):** N/A — new work
*   **Standard:** v1.10.2
*   **Outline version:** v0.3 — 2026-10-30
*   **Status:** draft
*   **Format:** ML-format paper, 8–12 pages main text (page budget per section in §1); appendices outside the page count.
*   **Outcome branches (pre-registered, DESIGN §K):** this outline is the full paper (E2 SUPPORT or INCONCLUSIVE → Leg B runs). If §K returns STOP (E2 REFUTE) or CLOSE (INSUFFICIENT EVENTS), the deliverable is a short null note built from the Leg A nodes only (ARG-01–ARG-10, ARG-14; FIG-1–FIG-5; TBL-1–TBL-5; S1–S5, S7–S8, S10; L-01, L-03–L-07); Leg B nodes become DROPPED ("not necessary — §K did not proceed") by a dated outline version.

## Changelog

*   v0.1 2026-10-30 — initial roadmap from THESIS.md (A1, A2) and DESIGN.md at 7949f19; citations from PRIOR_ART.md §2–§5, §9, §10.
*   v0.2 2026-10-30 — The unauthored key for arXiv:2603.09581 resolved to its authors from the arXiv record (Bai, Zhao, Zhou, Xu & Zhang) and re-keyed Bai-2026b; the ICML paper by the same group re-keyed Bai-2026a with its full author list (arXiv record of 2506.04805). Lettered in this paper's citation order. JAE approved the v0.1 drafting choices (null-note subset; own-work key lettering; FIG-2 event rule; Phase 5b checks).
*   v0.3 2026-10-30 — Reconciled with DESIGN/THESIS after the design-stage adversarial review (verification/design_review.md; THESIS A3). The contrast is now on mean lead; FA counts alarm onsets per 10,000 out-of-window steps with a 32-step hold; left-censored events get lead 128 (P-CENS); rewind events are retained; E1 is relabelled a consistency check (CONSISTENT/INCONSISTENT/INDETERMINATE, not support for Claim A); E5 is an alignment control (circular-shift null); E8 is a characterization. ARG-06 and EQ-5 are restated because the Adaptation Rate Theorem bounds the fast average's lead over the slow average, not the detector's lead over a spike (THESIS A3(b)). LB-ids, displays, scope and limits are updated to match.

## 1. IMRaD structural map (the skeleton)

Required section run present: Abstract, Introduction, Methods, Results, Discussion, Conclusion, References; Related Work present because prior art is cited.

| § | Section | Content | Page budget |
|---|---|---|---|
| — | Abstract | Claim A (early warning vs best deployed alarm at matched FA, primary run, verdict as E2 resolves); Claim B as a characterization of spike rate across the β₂ × LR grid ordered by the A.4 index; pre-registration (public `prereg-v1`, DOI) | 0.25 |
| 1 | Introduction | Cost of loss spikes; gradient norm as precursor; deployed alarms are one-step fast–slow tests; the question: does a smoothed fast window warn earlier at matched FA; contributions; what the paper does not claim | 1 |
| 2 | Related Work | 2.1 Spike precursors and deployed alarms; 2.2 Second-moment lag mechanism; 2.3 Edge of stability and the curvature boundary (complementary) | 1 |
| 3 | Framework | 3.1 Adam as a measurement-feedback loop; 3.2 The fast–slow divergence on the log gradient norm; 3.3 Lead bound; 3.4 Persistence-sign prediction | 1.25 |
| 4 | Methods | 4.1 Data (Leg A manifest, staging, completeness, pre-clip); 4.2 Spike definition and k ladder; 4.3 Detectors D_div and B1–B4; 4.4 Alarm onset and hold, onset-count threshold matching, leads, misses, censoring; 4.5 Experiments E1–E5 and the stop rule; 4.6 Leg B design (grid, data, batch, measured inputs); 4.7 Synthetic validation suite; 4.8 Pre-registration and amendments | 2.5 |
| 5 | Results | 5.1 Event counts and rung; 5.2 E1 sign check; 5.3 E2 primary comparison; 5.4 E3 replication; 5.5 E4 sensitivity; 5.6 E5 alignment control; 5.7 Leg B characterization (E6, E7); 5.8 E8 early warning on own runs | 2.75 |
| 6 | Discussion | 6.1 What smoothing buys and costs; 6.2 Relation to the curvature boundary; 6.3 Why the A.4 index is descriptive only; 6.4 Threats to validity; 6.5 Practical use | 1 |
| 7 | Conclusion | Verdicts and characterizations as resolved; limits-of-claim restated; data/code availability | 0.25 |
| — | References | §3 below | — |
| A | Appendix A | Synthetic validation suite: probes, regime span, realised cell | — |
| B | Appendix B | Mapping assessment (D.4.1): why A.4 EQ-5/EQ-6 does not map onto Adam's loop in observable-only terms | — |
| C | Appendix C | Construction pins and full sensitivity tables; FA-grid frontiers | — |
| D | Appendix D | Data provenance: per-file sources and hashes; amendment log since `prereg-v1` | — |

## 2. Argument chain (the spine)

| ID | Claim (one line) | § | Depends on | Support (LB-id / proof / cite key) | Status |
|---|---|---|---|---|---|
| ARG-01 | Loss spikes cost compute through rewinds and skips, and gradient-norm spikes tend to precede them | 1 | — | Chowdhery-2023, Walsh-2025, Takase-2025 | NEW |
| ARG-02 | Adam steers off trailing averages whose estimates feed back into the gradients they measure — a measurement-feedback loop | 3.1 | — | Kingma-2015, Kim-2026d (Measurement Trap) | NEW |
| ARG-03 | That the second-moment estimate lags the squared gradients and destabilizes training is established; this paper does not claim it | 2.2 | ARG-02 | Shazeer-2018, Wortsman-2023, Bai-2026a, Tang-2026, Molybog-2023 | NEW |
| ARG-04 | Deployed alarms (ZClip, SPAM, trainscope) are fast–slow divergences with a one-step fast window | 2.1 | ARG-01 | Kumar-2025, Huang-2025a, trainscope-2026 | NEW |
| ARG-05 | The smoothed divergence D = SMA_32(y) − SMA_128(y) on y = ln g, ratio 4 inside the Theorem 14 band, trades single-step response for noise rejection | 3.2 | ARG-04 | Kim-2026c (Thm 14), EQ-1, EQ-2 | NEW |
| ARG-06 | After a level change the fast average crosses a threshold ahead of the slow average (by (w_s − w_f)/2 at the midpoint); this motivates watching their difference but does not bound the detector's lead over a spike, which E2 measures | 3.3 | ARG-05 | Kim-2026a (Thm 3.1), EQ-5 | NEW |
| ARG-07 | The sign of D's forward correlation with y is fixed in advance by the ACF (Theorem 8b); on A1 it is checked as a consistency condition | 3.4, 5.2 | ARG-05 | Kim-2026c (Thm 8b, Def 13), EQ-6, LB-E1-label, LB-E1-rho, LB-E1-p | NEW |
| ARG-08 | At matched false-alarm rate (alarm onsets per 10,000 out-of-window steps, each held 32 steps), D_div's mean lead on the primary run (misses 0, left-censored 128) is compared with the best of four baselines on the minimum contrast; the point estimate decides REFUTE and the per-resample distribution separates SUPPORT from INCONCLUSIVE; the result is the pre-registered verdict and stop rule | 4.4–4.5, 5.3 | ARG-04, ARG-05, ARG-06 | EQ-7, EQ-11, TBL-3, FIG-3, FIG-4, LB-E2-verdict, LB-E2-Cmin, LB-E2-Cmin-p05, LB-K-verdict | NEW |
| ARG-09 | The direction of the E2 contrast replicates (or not) across the other public runs | 5.4 | ARG-08 | TBL-4, LB-E3-verdict, LB-E3-nruns | NEW |
| ARG-10 | Whether D_div's alarms align with the events beyond what a circularly shifted copy of the same alarm series achieves is measured by the E5 alignment control, and the contrast's dependence on windows, pins and censoring is reported without verdict | 5.5–5.6 | ARG-08 | FIG-5, TBL-5, LB-E5-aor-real, LB-E5-aor-shifted, LB-E5-flag, LB-E4-variants | NEW |
| ARG-11 | The A.4 exponential-kernel boundary does not map onto Adam's loop in observable-only terms, so Claim B is a characterization, not a verdict | 6.3, App. B | ARG-02, ARG-03 | Kim-2026d (App. A.4, EQ-5/EQ-6), EQ-8, EQ-9 | NEW |
| ARG-12 | Across the β₂ × LR grid, spike rate is characterized and its ordering by the A.4 robustness index is reported within each LR | 5.7 | ARG-11, ARG-08 | EQ-10, TBL-6, FIG-6, FIG-7, LB-E6-spearman, LB-E7-tau, LB-B-noisecell | NEW |
| ARG-13 | E2's statistics are characterized on the Leg B runs (no label; does not combine with E2) | 5.8 | ARG-08 | TBL-7, LB-E8-Cmin, LB-E8-Nout | NEW |
| ARG-14 | The lag view and the curvature boundary are complementary: the boundary says where instability is; the divergence watches the logged scalar that precedes the crossing | 6.2 | ARG-03, ARG-08 | Cohen-2021, Cohen-2022, Bai-2026a | NEW |
| ARG-15 | A detector computed from one logged scalar can ship as a lightweight monitor; its value is bounded to avoided rewinds, not a share of hyperscale compute | 6.5 | ARG-08 | PKG-01, Chowdhery-2023 | NEW |

## 3. Citations

Own-work keys are lettered in this paper's own reference order (the paper stands alone; no series numbering).

| Key (Surname-YEAR) | Reference (or "→ References") | Role | Supports (ARG / §) | Status |
|---|---|---|---|---|
| Kim-2026a | Kim, J. (2026). The Adaptation Rate Theorem: Predictable Lead Times in Multi-Scale Trailing Measures. DOI 10.5281/zenodo.20650165 | foundation (cited, not re-proved): Thm 3.1 fast-over-slow crossing lead, used as motivation only (THESIS A3(b)) | ARG-06, ARG-10; 3.3, 4.4, 4.5 | NEW |
| Kim-2026b | Kim, J. (2026). Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology. DOI 10.5281/zenodo.21081981 | method-precedent: a fast–slow divergence onset detector compared against a level rule (§5.1.2, fixed threshold on D); the expanding-percentile score used here is new to this paper | ARG-05; 4.3 | NEW |
| Kim-2026c | Kim, J. (2026). The Divergence Theorem for Regime Transition Detection. DOI 10.5281/zenodo.20820524 | foundation: Theorem 8b (eq. 63), Definition 13 (eq. 61), Theorem 14 window-ratio band | ARG-05, ARG-07; 3.2, 3.4 | NEW |
| Kim-2026d | Kim, J. (2026). The Measurement Trap: How Backward-Looking Measurements Destabilize the Systems They Were Designed to Protect. DOI 10.5281/zenodo.21206946 | foundation: measurement-feedback class; Appendix A.4 EQ-5/EQ-6 as descriptive index | ARG-02, ARG-11, ARG-12; 3.1, 6.3, App. B | NEW |
| Kingma-2015 | Kingma & Ba, Adam, ICLR 2015 | foundation (optimizer definition) | ARG-02; 3.1 | NEW |
| Reddi-2018 | Reddi, Kale & Kumar, On the Convergence of Adam and Beyond, ICLR 2018 | contrast (AMSGrad changes the kernel) | 6.3 | NEW |
| Walsh-2025 | OLMo team (Walsh et al.), 2 OLMo 2 Furious, arXiv:2501.00656 | motivating-anomaly; primary data source (OLMo-0424 gradient-norm precursors, §3) | ARG-01; 1, 4.1 | NEW |
| Chowdhery-2023 | Chowdhery et al., PaLM, 2023, §5 | motivating-anomaly (rewind-and-skip cost) | ARG-01, ARG-15; 1, 6.5 | NEW |
| Takase-2025 | Takase et al., Spike No More, COLM 2025, arXiv:2312.16903 | corroboration (spikes tied to gradient-norm growth) | ARG-01; 2.1 | NEW |
| Kumar-2025 | Kumar et al., ZClip, arXiv:2504.02507 | prior-art; baseline B3 source of defaults | ARG-04; 2.1, 4.3 | NEW |
| Huang-2025a | Huang et al., SPAM, ICLR 2025, arXiv:2501.06842 | prior-art (same-step ratio test) | ARG-04; 2.1 | NEW |
| Huang-2026 | Huang et al., GradientStabilizer, ICML 2026, arXiv:2502.17055 | prior-art (mitigation, not warning) | 2.1 | NEW |
| Wang-2025 | Wang et al., AdaGC, arXiv:2502.11034 | prior-art (mitigation, not warning) | 2.1 | NEW |
| trainscope-2026 | trainscope (PyPI; kaelvalen/trainscope @ 0651b25) | prior-art; baseline B4 source of defaults | ARG-04; 2.1, 4.3 | NEW |
| Fatima-2025 | Fatima, A Proactive Reliability Metric…, EMNLP 2025 Industry Track, 2897–2913 | contrast (failure-risk score with lead times; targets failures, not spikes) | 2.1 | NEW |
| Shazeer-2018 | Shazeer & Stern, Adafactor, ICML 2018, arXiv:1804.04235 | prior-art (out-of-date second-moment estimator) | ARG-03; 2.2 | NEW |
| Wortsman-2023 | Wortsman, Dettmers et al., Stable and low-precision training…, NeurIPS 2023, arXiv:2304.13013 | prior-art (second-moment underestimation precedes spikes; lower β₂) | ARG-03; 2.2 | NEW |
| Wortsman-2024 | Wortsman et al., Small-scale proxies for large-scale Transformer training instabilities, ICLR 2024, arXiv:2309.14322 | method-precedent (small-model proxy for Leg B) | 4.6 | NEW |
| Molybog-2023 | Molybog et al., A Theory on Adam Instability…, arXiv:2304.09871 | prior-art (time-domain gradient correlation) | ARG-03; 2.2 | NEW |
| Ma-2022 | Ma, Wu & E, MSML 2022, PMLR 145:671–692 | prior-art (qualitative (β₁, β₂) regimes) | 2.2 | NEW |
| Bai-2026a | Bai, Zhou, Zhao, Li, Li, Xiong, Yang, Zhang & Xu, Adaptive Preconditioners Trigger Loss Spikes in Adam, ICML 2026, arXiv:2506.04805 | prior-art (closest precedent; curvature boundary) | ARG-03, ARG-14; 2.2, 2.3, 6.2 | NEW |
| Tang-2026 | Tang, Chen & Liu, Beyond Quadratic Loss: The Stability Phase Diagram of Adam, arXiv:2609.18314 | prior-art (fitted (β₁, β₂) boundary) | ARG-03; 2.2 | NEW |
| Bai-2026b | Bai, Zhao, Zhou, Xu & Zhang, Towards Understanding Adam Convergence on Highly Degenerate Polynomials, arXiv:2603.09581 (2026) | prior-art (derived phase diagram on toy objectives) | 2.2 | NEW |
| Kourkoutas-2025 | Kourkoutas-beta, arXiv:2508.12996 | contrast (online β₂ adaptation as remedy) | 6.3 | NEW |
| Cohen-2021 | Cohen et al., Gradient Descent … Edge of Stability, ICLR 2021 | contrast (curvature boundary, non-adaptive) | ARG-14; 2.3 | NEW |
| Cohen-2022 | Cohen et al., Adaptive Gradient Methods at the Edge of Stability, arXiv:2207.14484 | contrast (preconditioned sharpness; preconditioner held fixed) | ARG-14; 2.3, 6.2 | NEW |
| Lozhkov-2024 | FineWeb-Edu (HuggingFaceFW/fineweb-edu @ 87f09149…) | data source (Leg B corpus) | 4.6 | NEW |
| Radford-2019 | GPT-2 (model class and BPE tokenizer) | method-precedent (Leg B model and tokenizer) | 4.6 | NEW |
| BigScience-2022 | BigScience tr11-176B training logs (HF bigscience/tr11-176B-logs @ 67ef5a3) | data source (A5, conditional) | 4.1 | NEW |

Not cited (recorded so the omission is deliberate): trainpulse — no detector parameter confirmable from its public docs (PRIOR_ART §2); DROPPED ("not necessary — no parameter attributed to it").

Accuracy note for Phase 5b: Chowdhery-2023 and Cohen-2021 are seed entries "not re-read" in PRIOR_ART; Lozhkov-2024, Radford-2019 and BigScience-2022 bibliographic details are to be confirmed. All are checked at Phase 5b before the manuscript cites them.

## 4. Load-bearing findings

Names only; values live in claims.lock (Phase 3).

| LB-id (ledger) | Finding (one line, no value) | Supports (ARG) | Status |
|---|---|---|---|
| LB-A1-nevents-k4 | Eligible event count on A1 at k = 4 | ARG-08 | NEW |
| LB-A1-nevents-k3 | Eligible event count on A1 at k = 3 (if the ladder steps down) | ARG-08 | NEW |
| LB-A1-rung | k-ladder rung that resolved | ARG-08 | NEW |
| LB-A1-ineligible | Ineligible events counted, with reasons | ARG-08 | NEW |
| LB-A1-rewind | Rewind events retained on their own segment (count) | ARG-08 | NEW |
| LB-E1-label | E1 label (CONSISTENT / INCONSISTENT / INDETERMINATE; not support for Claim A) | ARG-07 | NEW |
| LB-E1-predsign | A-priori predicted sign from the ACF criterion | ARG-07 | NEW |
| LB-E1-rho | Realised forward correlation | ARG-07 | NEW |
| LB-E1-p | One-sided block-permutation p | ARG-07 | NEW |
| LB-E2-verdict | E2 four-way label | ARG-08 | NEW |
| LB-E2-Cmin | Minimum contrast of mean leads (point estimate; decides REFUTE) | ARG-08 | NEW |
| LB-E2-Cmin-p05 | 5th percentile of resampled C_min | ARG-08 | NEW |
| LB-E2-Cb | Contrast against each baseline B1–B4 | ARG-08 | NEW |
| LB-E2-lead-det | Mean and median lead per detector at headline FA | ARG-08 | NEW |
| LB-E2-miss-det | Detection rate, miss count and censored count per detector | ARG-08 | NEW |
| LB-E2-nstar | Matched onset count n*, realised count, shortfall, non-monotone regions and realised duty cycle per detector | ARG-08 | NEW |
| LB-E2-argmax | Per-resample argmax probability over detectors | ARG-08 | NEW |
| LB-E2-power | Measured detection probability at the observed effect (INCONCLUSIVE branch) | ARG-08 | NEW |
| LB-K-verdict | §K outcome (STOP / CLOSE / PROCEED) and grading-day record | ARG-08 | NEW |
| LB-E3-verdict | E3 replication label | ARG-09 | NEW |
| LB-E3-nruns | Runs with ≥ 3 eligible events; runs reported descriptively | ARG-09 | NEW |
| LB-E4-variants | Contrast under each window pair, pin sweep and resampling variant | ARG-10 | NEW |
| LB-E5-aor-real | D_div advance-ordering rate and mean lead on the real alarm series | ARG-10 | NEW |
| LB-E5-aor-shifted | Same under circular shift (median and 90 % range); block-shuffle result beside it | ARG-10 | NEW |
| LB-E5-flag | Alignment-control flag state | ARG-10 | NEW |
| LB-suite-cell | Regime cell the realised A1 data lands in (event count × persistence) | ARG-08 | NEW |
| LB-suite-null | Suite false-REFUTE and false-SUPPORT rates for the planted nulls, incl. unequal alarm memory | ARG-08 | NEW |
| LB-E6-table | 24-cell spike-rate / divergence / φ̂ / b_g*(exp) table | ARG-12 | NEW |
| LB-E6-spearman | Spearman of spike rate vs b_g*(exp) with permutation interval | ARG-12 | NEW |
| LB-E7-tau | Kendall τ within each LR with permutation interval | ARG-12 | NEW |
| LB-B-noisecell | Gradient-noise cell the realised Leg B data lands in | ARG-12 | NEW |
| LB-B-replicates | Replicate-seed spike rates at the four P-REP cells | ARG-12 | NEW |
| LB-E8-Cmin | E8 pooled minimum contrast with cluster-bootstrap interval over runs (no label) | ARG-13 | NEW |
| LB-E8-Nout | N_out and n* per run; runs "FA not matchable" counted | ARG-13 | NEW |
| LB-A-included | Which of A2–A6 were included or excluded at staging, with reasons | ARG-09 | NEW |

## 5. Figures, tables & equations

| ID (FIG- / TBL- / EQ-) | What it shows (one line) | § | Referenced by (ARG / §) | Status |
|---|---|---|---|---|
| FIG-1 | Adam as a measurement-feedback loop, and the fast–slow divergence read off the gradient norm | 3.1 | ARG-02, ARG-05; 1, 3 | NEW |
| FIG-2 | One A1 event: g, D, loss, and each detector's first alarm onset in the scan window (event chosen by a rule fixed before data: the median-lead event) | 5.3 | ARG-08; 5.3 | NEW |
| FIG-3 | False-alarm-rate frontier per detector on A1 (mean lead vs FA over the grid) | 5.3 | ARG-08; 5.3, 6.1 | NEW |
| FIG-4 | Lead distributions per detector at headline FA, miss count beside each | 5.3 | ARG-08; 5.3 | NEW |
| FIG-5 | E5: D_div advance-ordering rate, real vs circularly shifted alarm series | 5.6 | ARG-10; 5.6 | NEW |
| FIG-6 | Leg B spike rate across β₂ × LR (heatmap, diverged cells marked) | 5.7 | ARG-12; 5.7 | NEW |
| FIG-7 | Spike rate vs b_g*(exp) within each LR | 5.7 | ARG-12; 5.7, 6.3 | NEW |
| TBL-1 | Detector definitions: D_div and B1–B4, parameters, source or pin | 4.3 | ARG-04, ARG-05; 4.3 | NEW |
| TBL-2 | Leg A data: A1–A6, identifier, role, inclusion outcome | 4.1 | ARG-09; 4.1, App. D | NEW |
| TBL-3 | E2: mean and median lead, detection rate, misses and censored counts per detector, C_b, C_min with interval, verdict | 5.3 | ARG-08; 5.3, 7 | NEW |
| TBL-4 | E3: per-run event count and sign of C_min | 5.4 | ARG-09; 5.4 | NEW |
| TBL-5 | E4: contrast under each sensitivity variant | 5.5 | ARG-10; 5.5, App. C | NEW |
| TBL-6 | E6: 24-cell Leg B table (spike rate, divergence flag, φ̂, b_g*(exp)) | 5.7 | ARG-12; 5.7 | NEW |
| TBL-7 | E8: pooled Leg B characterization (no label) | 5.8 | ARG-13; 5.8 | NEW |
| TBL-8 | Construction-pin register with sweeps | App. C | ARG-10; 4.8, App. C | NEW |
| EQ-1 | y(t) = ln g(t), g = pre-clip global gradient norm | 3.2 | ARG-05; 3.2, 4.3 | NEW |
| EQ-2 | D(t) = SMA_32(y)(t) − SMA_128(y)(t) | 3.2 | ARG-05; 3.2, 4.3 | NEW |
| EQ-3 | Detector score: expanding empirical percentile of D, minimum history 1,000 steps | 4.3 | ARG-05; 4.3 | NEW |
| EQ-4 | Spike rule L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), dedup 200 | 4.2 | ARG-08; 4.2 | NEW |
| EQ-5 | Fast-over-slow crossing lead α(w_s − w_f), (w_s − w_f)/2 at the midpoint (cited; motivation, not a bound on spike lead) | 3.3 | ARG-06; 3.3, 6.1 | NEW |
| EQ-6 | Persistence-sign criterion sign[R̄(h, h+w_f) − R̄(h+w_f, h+w_s)] with R̄ as mean ACF (cited) | 3.4 | ARG-07; 3.4, 5.2 | NEW |
| EQ-7 | C_b = mean lead(D_div) − mean lead(B_b) over eligible events (misses 0, censored 128); C_min = min_b C_b | 4.5 | ARG-08; 4.5, 5.3 | NEW |
| EQ-8 | Adam second-moment update v_t = β₂ v_{t−1} + (1−β₂) g_t² and step η/√v_t | 3.1 | ARG-02, ARG-11; 3.1, App. B | NEW |
| EQ-9 | The Measurement Trap App. A.4 characteristic polynomial (its EQ-5), cited | App. B | ARG-11; 6.3, App. B | NEW |
| EQ-10 | Robustness index b_g*(exp) = (1−φ)/α + φ (its EQ-6), with α = 1−β₂ | 4.6 | ARG-12; 4.6, 5.7 | NEW |
| EQ-11 | Alarm onset with hold H = 32; FA = out-of-window onsets per 10,000 out-of-window steps; n* = round(FA × N_out / 10,000) | 4.4 | ARG-08; 4.4 | NEW |

## 6. Assumptions & scope conditions

| ID | Statement | Where stated (anchor) | Status |
|---|---|---|---|
| S1 | Every operator is causal and reads only scalars already in a training log; no curvature is computed | 4.3 `S1` | NEW |
| S2 | g is the pre-clip global gradient norm; a run logging post-clip norm is reported separately, never pooled | 4.1 `S2` | NEW |
| S3 | Every Leg A run used β₂ = 0.95 (second-moment window 20 steps); Leg A tests the alarm independent of β₂, and the (32, 128) windows exceed the optimizer's own memory | 4.1 `S3` | NEW |
| S4 | E1 assumes approximate weak stationarity of y; y drifts upward on A1, so E1 is a consistency check | 3.4 `S4` | NEW |
| S5 | Leg A data are the public logs as staged after `prereg-v1`, hash-pinned; segments assembled by P-SEG; no window crosses a gap | 4.1 `S5` | NEW |
| S6 | Leg B: 124M GPT-2-class model, 5,000 steps, 98,304 tokens/step (smaller than the reference batch; more gradient noise), clipping disabled, identical token order across cells | 4.6 `S6` | NEW |
| S7 | Events at least 200 steps apart are treated as independent for resampling (block-of-3 sensitivity) | 4.5 `S7` | NEW |
| S8 | Lead is measured inside a 128-step scan window; FA is out-of-window alarm onsets per 10,000 out-of-window steps (headline 1), each onset held 32 steps; a missed event has lead 0; an alarm already on at the window start gives lead 128, flagged | 4.4 `S8` | NEW |
| S9 | The A.4 index is a descriptive ordering only; no feedback gain is estimated | 4.6 `S9` | NEW |
| S10 | Spikes that a checkpoint restart superseded are retained as rewind events on their own segment; dedup applies within a series | 4.1 `S10` | NEW |

## 7. Conclusions & limits-of-claim

| ID | Conclusion or limit-of-claim | Where (anchor) | Status |
|---|---|---|---|
| C-01 | Claim A verdict on the primary run as E2 resolved, stated with C_min, its interval, and each detector's miss count | 7 `C-01` | NEW |
| C-02 | Replication outcome across the included public runs, with runs too sparse to score named | 7 `C-02` | NEW |
| C-03 | Leg B characterization: how spike rate varies with β₂ and LR, and how well the A.4 index orders it, with resolution stated | 7 `C-03` | NEW |
| C-04 | How far D_div's alarms align with the events beyond the circular-shift null | 7 `C-04` | NEW |
| L-01 | Does NOT propose a new instability mechanism; the second-moment lag is prior art | 1, 6 `L-01` | NEW |
| L-02 | Does NOT claim a stability criterion for Adam; Claim B carries no pass/fail | 6.3 `L-02` | NEW |
| L-03 | Does NOT claim the Leg A result for β₂ other than 0.95, or for architectures and scales outside the included runs | 6.4 `L-03` | NEW |
| L-04 | Does NOT claim savings beyond avoided rewinds and skips; low single-digit share of training compute at most | 6.5 `L-04` | NEW |
| L-05 | Does NOT claim an analytical bound on the lead over a spike; the Adaptation Rate Theorem is used as motivation only | 3.3, 6.1 `L-05` | NEW |
| L-06 | Does NOT replace curvature-based analysis; no Hessian quantity is measured | 6.2 `L-06` | NEW |
| L-07 | Does NOT evaluate mitigation (clipping, rewinds); the detector only warns | 6.5 `L-07` | NEW |

## 8. Internal cross-references

| From | To | Purpose | Status |
|---|---|---|---|
| 1 Contributions | 5.3, TBL-3 | headline result | NEW |
| 2.1 | 4.3, TBL-1 | deployed alarms become B3/B4 | NEW |
| 2.3 | 6.2 | complementarity with the curvature boundary | NEW |
| 3.2 | EQ-1, EQ-2, FIG-1 | operator definition | NEW |
| 3.3 | EQ-5, L-05 | crossing-lead motivation and its limit | NEW |
| 3.4 | EQ-6, 5.2 | sign prediction and its check | NEW |
| 4.1 | TBL-2, App. D | data provenance | NEW |
| 4.2 | EQ-4, 5.1 | spike rule and event counts | NEW |
| 4.5 | EQ-7, 5.3 | contrast definition and result | NEW |
| 4.6 | EQ-10, App. B, 5.7 | Leg B index and its mapping caveat | NEW |
| 4.7 | App. A | suite detail | NEW |
| 4.8 | TBL-8, App. C, App. D | pins and amendments | NEW |
| 5.5 | TBL-5, App. C | sensitivity detail | NEW |
| 6.3 | App. B, EQ-8, EQ-9 | why the index is descriptive | NEW |

## 9. Companion artifacts (nodes outside the 8–12 page manuscript)

| ID | Artifact | Content | Depends on | Status |
|---|---|---|---|---|
| COMP-01 | Plain-English companion | Per the Companion Standard (BINDING page 2kydc08j-614): what was asked, what was registered before looking, what was found (C-01–C-04), what is not claimed (L-01–L-07) | C-01–C-04, L-01–L-07 | NEW |
| PKG-01 | `pip install` monitor — README | What the monitor computes (EQ-1–EQ-3), how to attach it (plain loop and Hugging Face Trainer callback), how to set the threshold to a target false-alarm rate (P-FA), what the paper did and did not show (C-01, L-03, L-07), citation and DOI | ARG-15, EQ-1–EQ-3, C-01 | NEW |
| PKG-02 | Monitor package code | D_div score, alarm onset, FA-matched threshold; same operators as the analysis code, tested against the synthetic suite | PKG-01, App. A | NEW |

## Reconciliation (run before signing; re-run at Phase 4 open/close and Phase 5)

- [x] Every ARG node has ≥1 support and a valid `Depends on` (or "—" for a premise).
- [x] Every citation key maps to ≥1 ARG node or section (no orphan citations; no argument citing a missing reference).
- [ ] Every load-bearing finding names a real LB-id in claims.lock; no values in this file. — No values here; claims.lock does not exist until Phase 3, so the LB-ids above are proposed names, confirmed at Phase 3.
- [ ] Every figure/table/equation (`FIG-`/`TBL-`/`EQ-`) is present at its anchor in the manuscript AND referenced in the text — manuscript not yet written (Phase 4).
- [ ] Every scope condition (`S-`) and limit-of-claim (`L-`) appears at its anchor in the manuscript — Phase 4.
- [ ] Every internal cross-reference resolves to an element that exists — Phase 4; §8 lists the intended ones.
- [x] Every node has a status; every DROPPED carries a valid reason.
- [x] REQUIRED SECTION RUN — Abstract, Introduction, Methods, Results, Discussion, Conclusion, References present in §1, plus Related Work (prior art cited) and Framework.
- [ ] The IMRaD map matches the manuscript's actual section list — Phase 4.
- [x] (Rebuild) every COVERAGE KEEP/TRANSFORM row maps to ≥1 node here — N/A, new work.

## Author sign-off

> The roadmap captures the paper's full argument, every citation, every load-bearing finding, every figure/table/equation, the assumptions/scope, and the conclusions; every node has a status and (where applicable) a manuscript anchor; no values are hard-coded. Accurate as of commit [filled at commit], outline v0.1.

**Signed:** [JAE at Phase 1 close] — **Date:** [at signing]
