# OUTLINE.md — Paper Roadmap

Copied from the Research-to-Publication Standard's OUTLINE.md Template page (doc 2kydc08j-754, page 2kydc08j-514). Built from THESIS.md (MD5 532b7f062b26eda6c587a9362609928b) and DESIGN.md (MD5 eda8ea9806af114e48d06a9caf23614b, commit 7949f19), with citations from PRIOR_ART.md (MD5 0cf9c2cd8c413eed77564b8f8a1a44de). New work: every node is NEW. No values appear in this file; load-bearing numbers are named by LB-id and will live in claims.lock (Phase 3).

## Metadata

*   **Paper:** Measurement-Lag Instability in Adaptive Optimizers — A Fast–Slow Divergence Early-Warning Signal for Loss Spikes, Tested Against Deployed Alarms on Public Training Logs
*   **Archetype:** empirical-with-verified-theory (THESIS Amendment A2(f): no original theorem; The Measurement Trap Appendix A.4 used as a descriptive index)
*   **Source pin (rebuild only):** N/A — new work
*   **Standard:** v1.10.2
*   **Outline version:** v0.8.1 — 2026-11-18
*   **Status:** draft — **null-note shape** (§K STOP, 2026-11-15); reconciled with DESIGN Amendments 7–17 and DECISIONS 47–65 (Phase 4 open)
*   **Format:** null note for an ML readership (arXiv cs.LG), about 9–10 pages main text with 6 figures and 4 tables (revised v0.8.1 from an estimated 4–6 pages: the required content — verbatim kill rule, Amendment 15 reading rules, registered operators, AI disclosure — does not fit 4–6; DECISIONS 69); appendices outside the page count. Working title: "A Smoothed Fast–Slow Divergence Does Not Warn of Loss Spikes Earlier Than Deployed Alarms: A Pre-Registered Null on a Public 7B Training Log" (JAE to confirm).
*   **Registration cited in the paper:** `prereg-v1`, version DOI 10.5281/zenodo.23825294 (concept DOI 10.5281/zenodo.23825293); the §K kill rule and grading day are restated verbatim (Phase 4 override 3).
*   **Outcome branches (pre-registered, DESIGN §K):** this outline is the full paper (E2 SUPPORT or INCONCLUSIVE → Leg B runs). If §K returns STOP (E2 REFUTE) or CLOSE (INSUFFICIENT EVENTS), the deliverable is a short null note built from the Leg A nodes only (ARG-01–ARG-10, ARG-14; FIG-1–FIG-5; TBL-1–TBL-5; S1–S5, S7–S8, S10–S13; L-01, L-03–L-07); Leg B nodes become DROPPED ("not necessary — §K did not proceed") by a dated outline version. **Resolved 2026-11-15: §K STOP. E2 is REFUTE on A1 (DECISIONS entry 47; RECORD.md). The deliverable is the null note; the Leg B nodes are DROPPED in v0.6.**

## Changelog

*   v0.1 2026-10-30 — initial roadmap from THESIS.md (A1, A2) and DESIGN.md at 7949f19; citations from PRIOR_ART.md §2–§5, §9, §10.
*   v0.2 2026-10-30 — The unauthored key for arXiv:2603.09581 resolved to its authors from the arXiv record (Bai, Zhao, Zhou, Xu & Zhang) and re-keyed Bai-2026b; the ICML paper by the same group re-keyed Bai-2026a with its full author list (arXiv record of 2506.04805). Lettered in this paper's citation order. JAE approved the v0.1 drafting choices (null-note subset; own-work key lettering; FIG-2 event rule; Phase 5b checks).
*   v0.3 2026-10-30 — Reconciled with DESIGN/THESIS after the design-stage adversarial review (verification/design_review.md; THESIS A3). The contrast is now on mean lead; FA counts alarm onsets per 10,000 out-of-window steps with a 32-step hold; left-censored events get lead 128 (P-CENS); rewind events are retained; E1 is relabelled a consistency check (CONSISTENT/INCONSISTENT/INDETERMINATE, not support for Claim A); E5 is an alignment control (circular-shift null); E8 is a characterization. ARG-06 and EQ-5 are restated because the Adaptation Rate Theorem bounds the fast average's lead over the slow average, not the detector's lead over a spike (THESIS A3(b)). LB-ids, displays, scope and limits are updated to match.
*   v0.4 2026-10-30 — DESIGN Amendment 1 / THESIS A4 (A1 logs the gradient norm every 10 steps). For the primary run (OLMo-0424) the detector side runs on that grid. FA is counted per 10,000 out-of-window gradient-norm observations, with a 32-observation hold; windows are 320/1,280 steps; the scan window is 1,280 steps; censored lead is 1,280; dedup is 2,000 steps. ARG-08, EQ-3, EQ-4, EQ-7, EQ-11, S3 and S8 carry the A1 scales. New S11 covers the grid and its scope condition.
*   v0.5 2026-10-31 — DESIGN Amendments 2–6 and the A1 event stage (DECISIONS entries 10–17). Amendment 2: P-SEG clarified (later run wins ties; supersession by resume step; an unused owner leaves a gap), so the kept A1 series has a second internal gap (S5, S10, new S12). Amendment 3: spike-rule construction (EQ-4). Amendment 4: E1's R̄ over half-open lags (EQ-6); P-PHIHAT primary on the level (EQ-10). Amendment 5: detector construction, with B3 and B4 per the ZClip 1.0.0 and trainscope 0651b25 source (EQ-3, TBL-1). Amendment 6: P-FA threshold matching scans from the top, plus an alarm-coverage stop (EQ-11, S8). LB-A1-nevents-k4, LB-A1-nevents-k3, LB-A1-rung, LB-A1-ineligible and LB-A1-rewind have landed (entry 13). New S13: under chained dedup, lower-rung events are not a superset of higher-rung events.
*   v0.6 2026-11-15 — **§K STOP: E2 REFUTE on A1** (DECISIONS entry 47; RECORD.md; `scripts/outputs/e2/e2_result.json` SHA-256 49c942eb…). Re-versioned to the null-note shape in the same sitting as the verdict (Phase 2 checklist).
    *   **E2 results landed.** LB-E2-verdict, -Cmin, -Cb, -lead-det, -miss-det, -nstar, -argmax, LB-K-verdict and LB-suite-cell are LANDED; LB-suite-null is LANDED (suite ALL PASS, e7abad6). LB-E2-Cmin-p05 is N/A (REFUTE) and LB-E2-power is N/A (INCONCLUSIVE branch not reached).
    *   **Leg B dropped** ("not necessary — §K did not proceed"): ARG-11, ARG-12, ARG-13, ARG-15; FIG-6, FIG-7; TBL-6–TBL-8; S6, S9; L-02; LB-E6-table, LB-E6-spearman, LB-E7-tau, LB-B-noisecell, LB-B-replicates, LB-E8-Cmin, LB-E8-Nout.
    *   **Kept for the null note:** ARG-01–ARG-10, ARG-14; FIG-1–FIG-5; TBL-1–TBL-5; S1–S5, S7–S8, S10–S13; L-01, L-03–L-07. E1, E3, E4 and E5 keep their nodes; whether they run before the null note is a Phase 2 decision recorded in DECISIONS.
    *   **Not yet reconciled:** DESIGN Amendments 7–17 (suite, A1-structure cells, the 15.x reporting items, the re-set and run dates). They enter the nodes at the Phase 4-open reconciliation. ARG-08 must then carry the F-6 reading: D_div was not matchable at the headline FA, and no detector led any event.
*   v0.7 2026-11-18 — Post-verdict results landed (DECISIONS entries 48–54). LB-E1-* LANDED (E1 INDETERMINATE). LB-E5-* LANDED (degenerate at headline: D_div never alarms; stated in advance). LB-E4-variants LANDED (no registered variant makes D_div matchable; P-SEG keep-earlier not run). LB-E3-* and LB-A-included NOT RUN (§K stop; A2–A6 not staged). New EXPLORATORY LB-ids LB-X1-precursor, LB-X2-matchability, LB-X3-events (entry 48 plan, committed before computation). For ARG-08 in the null note: the precursor is confined to the last 10-step logging interval (X1), and D_div is unmatchable on every sub-series (X2), so route 3 could not have changed E2. Amendments 7–17 still enter the nodes at the Phase 4-open reconciliation.
*   v0.8 2026-11-18 — **Phase 4-open reconciliation (DESIGN Amendments 7–17; DECISIONS 47–65).** Re-shaped to the null note: §1 is the null-note IMRaD map (Framework folded into Methods; Results, Discussion and appendices renumbered), and §8 cross-references follow it.
    *   **Amendments entering the nodes.** 7 (construction items: B4 candidates, N_out, fresh crossing after an undefined score, RNG streams, percentile method, detected/concurrent/miss) → EQ-11, S8, TBL-3. 8–9 (independent reference implementation; B4/B3 to source) → App. A, TBL-1. 10–14 (suite: unequal-memory null, A1-structure cells, decision flip, ten-step grid, dynamic range, broken fixture to Phase 3) → App. A, 3.7. 15 (adjudicated review; reading rules 15.3–15.21 stated beside E2) → ARG-16, TBL-9, new LB-ids. 16–17 (grading day re-set; E2 run date; the 2026-11-20 record) → 3.5, 3.8, App. D.
    *   **ARG-08 carries the F-6 reading:** D_div was not matchable at the headline FA and no detector led any event; E2 is REFUTE by a tie at zero. E2 and X1–X3 are stated as conditional on the covered ranges (entry 59; S14).
    *   **New LB-ids** (ledgered at Phase 4 open, entry 65, no new computation): LB-E2-frontier, LB-E2-severity, LB-E2-flip-power, LB-E2-F1-fallback, LB-E2-chance-asym, LB-E2-ddiv-response; LB-suite-cell gains the extension cell. LB-X1-precursor is the v2 result (entries 62–63; v1 superseded, not quoted).
    *   **New nodes.** ARG-16 (how to read REFUTE: severity, power, D_div response), ARG-17 (EXPLORATORY: precursor confined to the last logging interval; unmatchability is a detector property). TBL-9 (reported beside E2), FIG-8 (X1 event-locked curve, EXPLORATORY). S14–S18 (covered ranges; RNG stream deviation D-05; E1 null likely narrow; E5 shift crosses gaps; X1 p approximate). C-05 (exploratory). L-08–L-10.
    *   **Status changes.** ARG-09, TBL-4, LB-E3-* NOT RUN (§K stop). C-02 restated as "E3 not run". C-03, EQ-9, EQ-10 DROPPED (Leg B). PKG-01, PKG-02 DROPPED (DECISIONS 61: refuted detector not shipped); IMG-01 (stand-alone E2 figure) added. Leg B-only citations (Wortsman-2024, Lozhkov-2024, Radford-2019) and the A.4-index contrasts (Reddi-2018, Kourkoutas-2025) DROPPED; BigScience-2022 DROPPED (A5 not staged).
*   v0.8.1 2026-11-18 — Page estimate corrected to about 9–10 pages main text after the first full draft (DECISIONS 69); no node changed.

## 1. IMRaD structural map (the skeleton)

Required section run present: Abstract (+ Keywords), Introduction, Related Work (prior art cited), Methods, Results, Discussion, Conclusion, References. Null-note shape (v0.8): the Framework is folded into Methods §3.1.

| § | Section | Content | Page budget |
|---|---|---|---|
| — | Abstract | Question (does a smoothed fast–slow divergence on the log gradient norm warn of loss spikes earlier than deployed one-step alarms at matched false-alarm rate); pre-registration; primary run; E2 REFUTE with the F-6 reading; what the null does and does not say; keywords (no JEL) | 0.25 |
| 1 | Introduction | Cost of loss spikes; gradient norm as a precursor; deployed alarms are one-step fast–slow tests; the pre-registered question and kill rule; contribution: a clean, ledgered null with its severity | 0.5 |
| 2 | Related Work | 2.1 Spike precursors and deployed alarms; 2.2 Second-moment lag mechanism (not claimed); 2.3 Edge of stability and the curvature boundary (complementary) | 0.5 |
| 3 | Methods | 3.1 The detector D_div (Adam as a measurement-feedback loop; y = ln g; D = SMA_32 − SMA_128; expanding-percentile score; motivation, not a bound); 3.2 Baselines B1–B4; 3.3 Data: primary run A1 (OLMo-0424), 10-step grid, P-SEG kept series and covered ranges; 3.4 Spike events and the k ladder; 3.5 Alarm onset and hold, P-FA matching, lead, contrast C_min, the kill rule and grading day (verbatim); 3.6 Pre-registered secondary analyses (E1, E4, E5; E3 not run); 3.7 Synthetic validation suite and the reading rules fixed before E2; 3.8 Deviations, amendments and discrepancies | 1.75 |
| 4 | Results | 4.1 Events; 4.2 E2 verdict; 4.3 Reading the verdict (severity, kill-rule power, D_div response, chance leads); 4.4 FA-grid frontier; 4.5 E1; 4.6 E4; 4.7 E5; 4.8 Exploratory diagnostics X1–X3 | 1.5 |
| 5 | Discussion | 5.1 Why D_div could not be matched; 5.2 What the null does and does not say; 5.3 Relation to the curvature boundary; 5.4 Threats to validity | 0.75 |
| 6 | Conclusion | Verdict restated with limits-of-claim; registered forward claim (the kill rule and grading day, as registered); data and code availability; AI-assistance disclosure | 0.25 |
| — | References | §3 below | — |
| A | Appendix A | Synthetic validation suite: cells, reference agreement, A1-structure layout, reading-rule cells | — |
| C | Appendix C | Construction pins, E4 sensitivity tables, FA-grid frontier detail | — |
| D | Appendix D | Data provenance (per-file sources and hashes); amendment log since `prereg-v1`; Discrepancy Register summary | — |

## 2. Argument chain (the spine)

| ID | Claim (one line) | § | Depends on | Support (LB-id / proof / cite key) | Status |
|---|---|---|---|---|---|
| ARG-01 | Loss spikes cost compute through rewinds and skips, and gradient-norm spikes tend to precede them | 1 | — | Chowdhery-2023, Walsh-2025, Takase-2025 | NEW |
| ARG-02 | Adam steers off trailing averages whose estimates feed back into the gradients they measure — a measurement-feedback loop | 3.1 | — | Kingma-2015, Kim-2026d (Measurement Trap) | NEW |
| ARG-03 | That the second-moment estimate lags the squared gradients and destabilizes training is established; this paper does not claim it | 2.2 | ARG-02 | Shazeer-2018, Wortsman-2023, Bai-2026a, Tang-2026, Molybog-2023 | NEW |
| ARG-04 | Deployed alarms (ZClip, SPAM, trainscope) are fast–slow divergences with a one-step fast window | 2.1 | ARG-01 | Kumar-2025, Huang-2025a, trainscope-2026 | NEW |
| ARG-05 | The smoothed divergence D = SMA_32(y) − SMA_128(y) on y = ln g, ratio 4 inside the Theorem 14 band, trades single-step response for noise rejection | 3.1 | ARG-04 | Kim-2026c (Thm 14), EQ-1, EQ-2 | NEW |
| ARG-06 | After a level change the fast average crosses a threshold ahead of the slow average (by (w_s − w_f)/2 at the midpoint); this motivates watching their difference but does not bound the detector's lead over a spike, which E2 measures | 3.1 | ARG-05 | Kim-2026a (Thm 3.1), EQ-5 | NEW |
| ARG-07 | The sign of D's forward correlation with y is fixed in advance by the ACF (Theorem 8b); on A1 it is checked as a consistency condition | 3.1, 4.5 | ARG-05 | Kim-2026c (Thm 8b, Def 13), EQ-6, LB-E1-label, LB-E1-rho, LB-E1-p | NEW |
| ARG-08 | At matched false-alarm rate (on A1: alarm onsets per 10,000 out-of-window gradient-norm observations, hold 32 observations, censored lead 1,280 steps — Amendment 1), D_div's mean lead is compared with the best of four baselines on the minimum contrast; the point estimate decides REFUTE. Result (F-6 reading): D_div could not be matched at the headline FA (it never alarmed), no detector led any event, and E2 is REFUTE by a tie at zero; §K STOP. Conditional on A1's covered ranges (S14) | 3.5, 4.2 | ARG-04, ARG-05, ARG-06 | EQ-7, EQ-11, TBL-3, FIG-2, FIG-4, LB-E2-verdict, LB-E2-Cmin, LB-E2-Cb, LB-E2-lead-det, LB-E2-miss-det, LB-E2-nstar, LB-E2-argmax, LB-K-verdict, LB-A1-nevents-k4 | NEW |
| ARG-09 | The direction of the E2 contrast replicates (or not) across the other public runs | — | ARG-08 | TBL-4, LB-E3-verdict, LB-E3-nruns | NOT RUN — §K stopped the project; A2–A6 not staged (DECISIONS 48); stated in 3.6 |
| ARG-10 | The E5 alignment control is degenerate at the headline FA (D_div never alarms; stated in advance) and the E4 sensitivity variants (windows, pins, censoring, resampling) re-match every threshold and none makes D_div matchable; E4 is reported as sensitivity, never rescue. E1, the persistence-sign consistency check, is INDETERMINATE | 4.5–4.7 | ARG-08, ARG-07 | FIG-5, TBL-5, LB-E5-aor-real, LB-E5-aor-shifted, LB-E5-flag, LB-E4-variants, LB-E1-label | NEW |
| ARG-11 | The A.4 exponential-kernel boundary does not map onto Adam's loop in observable-only terms, so Claim B is a characterization, not a verdict | 6.3, App. B | ARG-02, ARG-03 | Kim-2026d (App. A.4, EQ-5/EQ-6), EQ-8, EQ-9 | DROPPED — not necessary, §K did not proceed (v0.6) |
| ARG-12 | Across the β₂ × LR grid, spike rate is characterized and its ordering by the A.4 robustness index is reported within each LR | 5.7 | ARG-11, ARG-08 | EQ-10, TBL-6, FIG-6, FIG-7, LB-E6-spearman, LB-E7-tau, LB-B-noisecell | DROPPED — not necessary, §K did not proceed (v0.6) |
| ARG-13 | E2's statistics are characterized on the Leg B runs (no label; does not combine with E2) | 5.8 | ARG-08 | TBL-7, LB-E8-Cmin, LB-E8-Nout | DROPPED — not necessary, §K did not proceed (v0.6) |
| ARG-14 | The lag view and the curvature boundary are complementary: the boundary says where instability is; a logged-scalar alarm watches what precedes the crossing; this null bears on the alarm, not on the boundary | 5.3 | ARG-03, ARG-08 | Cohen-2021, Cohen-2022, Bai-2026a | NEW |
| ARG-15 | A detector computed from one logged scalar can ship as a lightweight monitor; its value is bounded to avoided rewinds, not a share of hyperscale compute | 6.5 | ARG-08 | PKG-01, Chowdhery-2023 | DROPPED — not necessary, §K did not proceed (v0.6) |
| ARG-16 | Beside REFUTE, the registered reading rules (Amendment 15.3–15.21): REFUTE is the planted null's modal outcome on the A1 layout; the kill rule's measured power against short precursors; the planted-effect and positive-control rates; D_div's lead response; the chance-lead asymmetry; and, since every detection rate on A1 is at most 50 %, the F1 fallback rates. REFUTE says D_div's mean lead did not exceed the best baseline's at matched FA, not that precursors are absent | 3.7, 4.3 | ARG-08 | TBL-9, LB-E2-severity, LB-E2-flip-power, LB-E2-F1-fallback, LB-E2-chance-asym, LB-E2-ddiv-response, LB-suite-cell, LB-suite-null, LB-E2-frontier | NEW |
| ARG-17 | EXPLORATORY (plan fixed before computation, DECISIONS 48): a gradient-norm rise before A1's spikes is present but concentrated in the last 10-step logging interval (X1 v2), and D_div is unmatchable on every sub-series (X2), so the failure is a property of the detector at this cadence, not of data coverage | 4.8, 5.1 | ARG-08 | FIG-8, LB-X1-precursor, LB-X2-matchability, LB-X3-events | NEW |

## 3. Citations

Own-work keys are lettered in this paper's own reference order (the paper stands alone; no series numbering).

| Key (Surname-YEAR) | Reference (or "→ References") | Role | Supports (ARG / §) | Status |
|---|---|---|---|---|
| Kim-2026a | Kim, J. (2026). The Adaptation Rate Theorem: Predictable Lead Times in Multi-Scale Trailing Measures. DOI 10.5281/zenodo.20650165 | foundation (cited, not re-proved): Thm 3.1 fast-over-slow crossing lead, used as motivation only (THESIS A3(b)) | ARG-06; 3.1 | NEW |
| Kim-2026b | Kim, J. (2026). Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology. DOI 10.5281/zenodo.21081981 | method-precedent: a fast–slow divergence onset detector compared against a level rule (§5.1.2, fixed threshold on D); the expanding-percentile score used here is new to this paper | ARG-05; 4.3 | NEW |
| Kim-2026c | Kim, J. (2026). The Divergence Theorem for Regime Transition Detection. DOI 10.5281/zenodo.20820524 | foundation: Theorem 8b (eq. 63), Definition 13 (eq. 61), Theorem 14 window-ratio band | ARG-05, ARG-07; 3.2, 3.4 | NEW |
| Kim-2026d | Kim, J. (2026). The Measurement Trap: How Backward-Looking Measurements Destabilize the Systems They Were Designed to Protect. DOI 10.5281/zenodo.21206946 | foundation: measurement-feedback class (motivation for D_div) | ARG-02; 3.1 | NEW |
| Kingma-2015 | Kingma & Ba, Adam, ICLR 2015 | foundation (optimizer definition) | ARG-02; 3.1 | NEW |
| Reddi-2018 | Reddi, Kale & Kumar, On the Convergence of Adam and Beyond, ICLR 2018 | contrast (AMSGrad changes the kernel) | 6.3 | DROPPED — A.4-index discussion dropped with Leg B (v0.8) |
| Walsh-2025 | OLMo team (Walsh et al.), 2 OLMo 2 Furious, arXiv:2501.00656 | motivating-anomaly; primary data source (OLMo-0424 gradient-norm precursors, §3) | ARG-01; 1, 4.1 | NEW |
| Chowdhery-2023 | Chowdhery et al., PaLM, 2023, §5 | motivating-anomaly (rewind-and-skip cost) | ARG-01; 1 | NEW |
| Takase-2025 | Takase et al., Spike No More, COLM 2025, arXiv:2312.16903 | corroboration (spikes tied to gradient-norm growth) | ARG-01; 2.1 | NEW |
| Kumar-2025 | Kumar et al., ZClip, arXiv:2504.02507 | prior-art; baseline B3 source of defaults | ARG-04; 2.1, 4.3 | NEW |
| Huang-2025a | Huang et al., SPAM, ICLR 2025, arXiv:2501.06842 | prior-art (same-step ratio test) | ARG-04; 2.1 | NEW |
| Huang-2026 | Huang et al., GradientStabilizer, ICML 2026, arXiv:2502.17055 | prior-art (mitigation, not warning) | 2.1 | NEW |
| Wang-2025 | Wang et al., AdaGC, arXiv:2502.11034 | prior-art (mitigation, not warning) | 2.1 | NEW |
| trainscope-2026 | trainscope (PyPI; kaelvalen/trainscope @ 0651b25) | prior-art; baseline B4 source of defaults | ARG-04; 2.1, 4.3 | NEW |
| Fatima-2025 | Fatima, A Proactive Reliability Metric…, EMNLP 2025 Industry Track, 2897–2913 | contrast (failure-risk score with lead times; targets failures, not spikes) | 2.1 | NEW |
| Shazeer-2018 | Shazeer & Stern, Adafactor, ICML 2018, arXiv:1804.04235 | prior-art (out-of-date second-moment estimator) | ARG-03; 2.2 | NEW |
| Wortsman-2023 | Wortsman, Dettmers et al., Stable and low-precision training…, NeurIPS 2023, arXiv:2304.13013 | prior-art (second-moment underestimation precedes spikes; lower β₂) | ARG-03; 2.2 | NEW |
| Wortsman-2024 | Wortsman et al., Small-scale proxies for large-scale Transformer training instabilities, ICLR 2024, arXiv:2309.14322 | method-precedent (small-model proxy for Leg B) | 4.6 | DROPPED — Leg B not run (v0.8) |
| Molybog-2023 | Molybog et al., A Theory on Adam Instability…, arXiv:2304.09871 | prior-art (time-domain gradient correlation) | ARG-03; 2.2 | NEW |
| Ma-2022 | Ma, Wu & E, MSML 2022, PMLR 145:671–692 | prior-art (qualitative (β₁, β₂) regimes) | 2.2 | NEW |
| Bai-2026a | Bai, Zhou, Zhao, Li, Li, Xiong, Yang, Zhang & Xu, Adaptive Preconditioners Trigger Loss Spikes in Adam, ICML 2026, arXiv:2506.04805 | prior-art (closest precedent; curvature boundary) | ARG-03, ARG-14; 2.2, 2.3, 6.2 | NEW |
| Tang-2026 | Tang, Chen & Liu, Beyond Quadratic Loss: The Stability Phase Diagram of Adam, arXiv:2609.18314 | prior-art (fitted (β₁, β₂) boundary) | ARG-03; 2.2 | NEW |
| Bai-2026b | Bai, Zhao, Zhou, Xu & Zhang, Towards Understanding Adam Convergence on Highly Degenerate Polynomials, arXiv:2603.09581 (2026) | prior-art (derived phase diagram on toy objectives) | 2.2 | NEW |
| Kourkoutas-2025 | Kourkoutas-beta, arXiv:2508.12996 | contrast (online β₂ adaptation as remedy) | 6.3 | DROPPED — A.4-index discussion dropped with Leg B (v0.8) |
| Cohen-2021 | Cohen et al., Gradient Descent … Edge of Stability, ICLR 2021 | contrast (curvature boundary, non-adaptive) | ARG-14; 2.3 | NEW |
| Cohen-2022 | Cohen et al., Adaptive Gradient Methods at the Edge of Stability, arXiv:2207.14484 | contrast (preconditioned sharpness; preconditioner held fixed) | ARG-14; 2.3, 6.2 | NEW |
| Lozhkov-2024 | FineWeb-Edu (HuggingFaceFW/fineweb-edu @ 87f09149…) | data source (Leg B corpus) | 4.6 | DROPPED — Leg B not run (v0.8) |
| Radford-2019 | GPT-2 (model class and BPE tokenizer) | method-precedent (Leg B model and tokenizer) | 4.6 | DROPPED — Leg B not run (v0.8) |
| BigScience-2022 | BigScience tr11-176B training logs (HF bigscience/tr11-176B-logs @ 67ef5a3) | data source (A5, conditional) | 4.1 | DROPPED — A5 not staged; §K stop (v0.8) |

Not cited (recorded so the omission is deliberate): trainpulse — no detector parameter confirmable from its public docs (PRIOR_ART §2); DROPPED ("not necessary — no parameter attributed to it").

Accuracy note for Phase 5b: Chowdhery-2023 and Cohen-2021 are seed entries "not re-read" in PRIOR_ART; Lozhkov-2024, Radford-2019 and BigScience-2022 bibliographic details are to be confirmed. All are checked at Phase 5b before the manuscript cites them.

## 4. Load-bearing findings

Names only; values live in claims.lock (Phase 3).

| LB-id (ledger) | Finding (one line, no value) | Supports (ARG) | Status |
|---|---|---|---|
| LB-A1-nevents-k4 | Eligible event count on A1 at k = 4 | ARG-08 | LANDED (DECISIONS entry 13; scripts/outputs/a1_events.json) |
| LB-A1-nevents-k3 | Eligible event count on A1 at k = 3 (if the ladder steps down) | ARG-08 | LANDED (DECISIONS entry 13; scripts/outputs/a1_events.json) |
| LB-A1-rung | k-ladder rung that resolved | ARG-08 | LANDED (DECISIONS entry 13; scripts/outputs/a1_events.json) |
| LB-A1-ineligible | Ineligible events counted, with reasons | ARG-08 | LANDED (DECISIONS entry 13; scripts/outputs/a1_events.json) |
| LB-A1-rewind | Rewind events retained on their own segment (count) | ARG-08 | LANDED (DECISIONS entry 13; scripts/outputs/a1_events.json) |
| LB-E1-label | E1 label (CONSISTENT / INCONSISTENT / INDETERMINATE; not support for Claim A) | ARG-07 | LANDED (DECISIONS 51; analysis/outputs/post/e1_result.json) |
| LB-E1-predsign | A-priori predicted sign from the ACF criterion | ARG-07 | LANDED (DECISIONS 51) |
| LB-E1-rho | Realised forward correlation | ARG-07 | LANDED (DECISIONS 51) |
| LB-E1-p | One-sided block-permutation p | ARG-07 | LANDED (DECISIONS 51) |
| LB-E2-verdict | E2 four-way label | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E2-Cmin | Minimum contrast of mean leads (point estimate; decides REFUTE) | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E2-Cmin-p05 | 5th percentile of resampled C_min | ARG-08 | N/A — REFUTE: p05 is not computed (Amendment 7.5) |
| LB-E2-Cb | Contrast against each baseline B1–B4 | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E2-lead-det | Mean and median lead per detector at headline FA | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E2-miss-det | Detection rate, miss count and censored count per detector | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E2-nstar | Matched onset count n*, realised count, shortfall, non-monotone regions and realised duty cycle per detector | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E2-argmax | Per-resample argmax probability over detectors | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E2-power | Measured detection probability at the observed effect (INCONCLUSIVE branch) | ARG-08 | N/A — the INCONCLUSIVE branch was not reached |
| LB-K-verdict | §K outcome (STOP / CLOSE / PROCEED) and grading-day record | ARG-08 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-E3-verdict | E3 replication label | ARG-09 | NOT RUN — §K stopped the project; A2–A6 not staged (DECISIONS 48) |
| LB-E3-nruns | Runs with ≥ 3 eligible events; runs reported descriptively | ARG-09 | NOT RUN — as LB-E3-verdict |
| LB-E4-variants | Contrast under each window pair, pin sweep and resampling variant | ARG-10 | LANDED (DECISIONS 54; analysis/outputs/post/e4/); P-SEG keep-earlier not run (DECISIONS 53) |
| LB-E5-aor-real | D_div advance-ordering rate and mean lead on the real alarm series | ARG-10 | LANDED (DECISIONS 52; degenerate at headline, stated in advance) |
| LB-E5-aor-shifted | Same under circular shift (median and 90 % range); block-shuffle result beside it | ARG-10 | LANDED (DECISIONS 52) |
| LB-E5-flag | Alignment-control flag state | ARG-10 | LANDED (DECISIONS 52; tripped by construction) |
| LB-X1-precursor | Gradient-norm precursor before loss spikes (event vs disjoint-tile control rise; event-locked mean curve) — EXPLORATORY | ARG-17 | LANDED v2 (DECISIONS 62–63; analysis/outputs/post/x_diag.json; v1 superseded, not quoted) |
| LB-X2-matchability | D_div top-score onset count vs n* per sub-series and at projected full-run n* — EXPLORATORY | ARG-17 | LANDED (DECISIONS 49) |
| LB-X3-events | Event density and rise by block — EXPLORATORY | ARG-17 | LANDED (DECISIONS 49) |
| LB-suite-cell | φ̂_y on A1, the selected suite cell (15.5) and the extension cell | ARG-16 | LANDED (DECISIONS entry 47; scripts/outputs/e2/e2_result.json) |
| LB-suite-null | Suite verdict (every graded cell) | ARG-16 | LANDED (suite verdict ALL PASS, e7abad6; verification/suite_verdict.md) |
| LB-E2-frontier | FA-grid frontier: n*, C_min, D_div matchability, mean lead and detection rate per detector at each reported FA | ARG-16 | LANDED (DECISIONS 47, 65; e2_result.json fa_grid) |
| LB-E2-severity | E2 label rates on the A1 layout at the selected and extension cells: planted null, planted effect, positive control; cells with no positive-control construction (15.3, 15.4, 15.6) | ARG-16 | LANDED (DECISIONS 65; verification/suite_verdict.md) |
| LB-E2-flip-power | Decision-flip REFUTE rates: per-step range, A1-layout range, and at the selected and extension cells (15.21) | ARG-16 | LANDED (DECISIONS 65; verification/suite_verdict.md) |
| LB-E2-F1-fallback | Step-precursor label rates at the selected φ (15.15; every detection rate on A1 ≤ 50 %) | ARG-16 | LANDED (DECISIONS 65; verification/suite_verdict.md) |
| LB-E2-chance-asym | Largest between-detector difference in mean chance lead and its cell; the A1-layout null value (15.17) | ARG-16 | LANDED (DECISIONS 65; verification/chance_leads_15_17.md) |
| LB-E2-ddiv-response | D_div lead response at the selected φ on the 10-step grid: matched and fixed-θ 10–90 % ranges per detector, history regression, detection rates by precursor length (15.8) | ARG-16 | LANDED (DECISIONS 65; verification/ddiv_response_15_8.md, verification/suite_verdict.md) |
| LB-E6-table | 24-cell spike-rate / divergence / φ̂ / b_g*(exp) table | ARG-12 | DROPPED — not necessary, §K did not proceed (v0.6) |
| LB-E6-spearman | Spearman of spike rate vs b_g*(exp) with permutation interval | ARG-12 | DROPPED — not necessary, §K did not proceed (v0.6) |
| LB-E7-tau | Kendall τ within each LR with permutation interval | ARG-12 | DROPPED — not necessary, §K did not proceed (v0.6) |
| LB-B-noisecell | Gradient-noise cell the realised Leg B data lands in | ARG-12 | DROPPED — not necessary, §K did not proceed (v0.6) |
| LB-B-replicates | Replicate-seed spike rates at the four P-REP cells | ARG-12 | DROPPED — not necessary, §K did not proceed (v0.6) |
| LB-E8-Cmin | E8 pooled minimum contrast with cluster-bootstrap interval over runs (no label) | ARG-13 | DROPPED — not necessary, §K did not proceed (v0.6) |
| LB-E8-Nout | N_out and n* per run; runs "FA not matchable" counted | ARG-13 | DROPPED — not necessary, §K did not proceed (v0.6) |
| LB-A-included | Which of A2–A6 were included or excluded at staging, with reasons | ARG-09 | NOT RUN — A2–A6 not staged (DECISIONS 48) |

## 5. Figures, tables & equations

| ID (FIG- / TBL- / EQ-) | What it shows (one line) | § | Referenced by (ARG / §) | Status |
|---|---|---|---|---|
| FIG-1 | Adam as a measurement-feedback loop, and the fast–slow divergence read off the gradient norm | 3.1 | ARG-02, ARG-05; 1, 3.1 | NEW |
| FIG-2 | One A1 event: g, D, loss, and each detector's alarm state in the scan window (event chosen by a rule fixed before data: the median-lead event) | 4.2 | ARG-08; 4.2 | NEW |
| FIG-3 | False-alarm-rate frontier per detector on A1 (mean lead and detection rate vs FA over the reported grid; D_div's unmatchable points marked); also the stand-alone image IMG-01 | 4.4 | ARG-16; 4.4, 5.1 | NEW |
| FIG-4 | Lead distributions per detector at headline FA, with detected, concurrent and miss counts beside each | 4.2 | ARG-08; 4.2 | NEW |
| FIG-5 | E5: D_div advance-ordering rate, real vs circularly shifted alarm series (degenerate at headline; shown as such) | 4.7 | ARG-10; 4.7 | NEW |
| FIG-6 | Leg B spike rate across β₂ × LR (heatmap, diverged cells marked) | — | — | DROPPED — not necessary, §K did not proceed (v0.6) |
| FIG-7 | Spike rate vs b_g*(exp) within each LR | — | — | DROPPED — not necessary, §K did not proceed (v0.6) |
| FIG-8 | X1 (EXPLORATORY): event-locked mean of y before and after the spike, events vs disjoint-tile controls | 4.8 | ARG-17; 4.8, 5.1 | NEW (v0.8) |
| TBL-1 | Detector definitions: D_div and B1–B4, parameters, source or pin; B3 as coded in ZClip 1.0.0 (monitor mode, raw g) and B4 as coded in trainscope 0651b25 (upward CUSUM on y, reset at onsets and gaps), both vendored (Amendments 5, 9) | 3.2 | ARG-04; 3.2 | NEW |
| TBL-2 | Leg A data: A1 identifier, segments, kept blocks, covered ranges and gaps; A2–A6 not staged (§K stop) | 3.3 | ARG-08; 3.3, App. D | NEW |
| TBL-3 | E2 at headline FA: per detector matchable, θ, realised/n*, mean and median lead, detected, concurrent, misses; C_b, C_min, verdict | 4.2 | ARG-08; 4.2, 6 | NEW |
| TBL-4 | E3: per-run event count and sign of C_min | — | ARG-09 | NOT RUN — §K stop; A2–A6 not staged (DECISIONS 48) |
| TBL-5 | E4: C_min and D_div matchability under each sensitivity variant | 4.6 | ARG-10; 4.6, App. C | NEW |
| TBL-6 | E6: 24-cell Leg B table (spike rate, divergence flag, φ̂, b_g*(exp)) | — | — | DROPPED — not necessary, §K did not proceed (v0.6) |
| TBL-7 | E8: pooled Leg B characterization (no label) | — | — | DROPPED — not necessary, §K did not proceed (v0.6) |
| TBL-8 | Construction-pin register with sweeps | — | — | DROPPED — not necessary, §K did not proceed (v0.6) |
| TBL-9 | Reported beside E2 (15.3–15.21): label rates under planted null, planted effect and positive control at the selected and extension cells; decision-flip power; F1 fallback; chance-lead asymmetry; D_div lead response | 4.3 | ARG-16; 4.3, 3.7 | NEW (v0.8) |
| EQ-1 | y(t) = ln g(t), g = pre-clip global gradient norm | 3.1 | ARG-05; 3.1 | NEW |
| EQ-2 | D(t) = SMA_32(y)(t) − SMA_128(y)(t) | 3.1 | ARG-05; 3.1 | NEW |
| EQ-3 | Detector score: expanding empirical percentile of D (ties counted ≤; SMAs include the current reading), defined only at j ≥ 1,000 observations, dropped readings counted (Amendment 5) | 3.1 | ARG-05; 3.1 | NEW |
| EQ-4 | Spike rule L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), σ sample SD; tested only with a full 128-step trailing window holding ≥ 64 finite values; chained dedup 2,000 on A1, inclusive, closed at gaps (Amendment 3) | 3.4 | ARG-08; 3.4 | NEW |
| EQ-5 | Fast-over-slow crossing lead α(w_s − w_f), (w_s − w_f)/2 at the midpoint (cited; motivation, not a bound on spike lead) | 3.1 | ARG-06; 3.1, 5.1 | NEW |
| EQ-6 | Persistence-sign criterion sign[R̄(h, h+w_f) − R̄(h+w_f, h+w_s)] with R̄ the mean ACF over half-open lags [a, b), the exact discrete form of Thm 8b (cited; Amendment 4.1) | 3.6 | ARG-07; 3.6, 4.5 | NEW |
| EQ-7 | C_b = mean lead(D_div) − mean lead(B_b) over eligible events (misses and concurrent 0, censored 1,280 steps on A1); C_min = min_b C_b | 3.5 | ARG-08; 3.5, 4.2 | NEW |
| EQ-8 | Adam second-moment update v_t = β₂ v_{t−1} + (1−β₂) g_t² and step η/√v_t | 3.1 | ARG-02; 3.1 | NEW |
| EQ-9 | The Measurement Trap App. A.4 characteristic polynomial (its EQ-5), cited | — | — | DROPPED — Leg B / App. B not in the null note (v0.8) |
| EQ-10 | Robustness index b_g*(exp) = (1−φ)/α + φ | — | — | DROPPED — Leg B not run (v0.8) |
| EQ-11 | Alarm onset with hold H = 32; FA = out-of-window onsets per 10,000 out-of-window grid observations on A1 (common N_out, Amendment 7.2); n* = round-half-up(FA × N_out / 10,000); θ by top scan (Amendment 6) with B4 candidates on the reset-free path (7.1); a detector is unmatchable when even its top score yields more than n* onsets (θ = ∞) | 3.5 | ARG-08; 3.5, 5.1 | NEW |

## 6. Assumptions & scope conditions

| ID | Statement | Where stated (anchor) | Status |
|---|---|---|---|
| S1 | Every operator is causal and reads only scalars already in a training log; no curvature is computed | 3.1 `S1` | NEW |
| S2 | g is the pre-clip global gradient norm; a run logging post-clip norm is reported separately, never pooled | 3.3 `S2` | NEW |
| S3 | Every Leg A run used β₂ = 0.95 (second-moment window 20 steps); Leg A tests the alarm independent of β₂, and the (32, 128) windows exceed the optimizer's own memory (1.6×/6.4× per step; 16×/64× on A1's 10-step grid) | 3.3 `S3` | NEW |
| S4 | E1 assumes approximate weak stationarity of y; y drifts upward on A1, so E1 is a consistency check | 3.6 `S4` | NEW |
| S5 | Leg A data are the public logs as staged after `prereg-v1`, hash-pinned; segments assembled by P-SEG as clarified in DESIGN Amendment 2 (later run wins ties; supersession by resume step); the kept series has two internal gaps; no window crosses a gap | 3.3 `S5` | NEW |
| S6 | Leg B: 124M GPT-2-class model, 5,000 steps, 98,304 tokens/step (smaller than the reference batch; more gradient noise), clipping disabled, identical token order across cells | 4.6 `S6` | DROPPED — not necessary, §K did not proceed (v0.6) |
| S7 | Events at least 200 steps apart are treated as independent for resampling (block-of-3 sensitivity) | 3.5 `S7` | NEW |
| S8 | Lead is measured inside a 128-step scan window; FA is out-of-window alarm onsets per 10,000 out-of-window steps (headline 1), each onset held 32 steps; a missed event has lead 0; an alarm already on at the window start gives lead 128, flagged (A1: 129 grid observations ending at the event's grid step, censored lead 1,280 steps, hold 32 observations) | 3.5 `S8` | NEW |
| S9 | The A.4 index is a descriptive ordering only; no feedback gain is estimated | 4.6 `S9` | DROPPED — not necessary, §K did not proceed (v0.6) |
| S10 | Spikes that a checkpoint restart superseded are retained as rewind events on their own series (the kept series up to the resume step plus the superseded steps); rewind portions on unused segments are counted as unscorable; dedup applies within a series (Amendment 2, Amendment 3) | 3.4 `S10` | NEW |
| S11 | On the primary run the gradient norm is logged every 10 steps, so its detectors run on that grid (windows 320/1,280 steps, lead resolution 10 steps, dedup 2,000 steps). A precursor shorter than about 320 steps favours raw-reading baselines by construction; this scope statement does not qualify the kill rule (DESIGN Amendment 1, THESIS A4) | 3.3 `S11` | NEW |
| S12 | The primary run's kept series follows each restart: a later run wins ties, and any step a later run superseded leaves the kept series. Where the superseding run's log is incomplete this leaves a gap, and its minimum-history cost is stated (DESIGN Amendment 2; structural report) | 3.3 `S12` | NEW |
| S13 | Under chained dedup, events at a lower spike threshold are not a superset of events at a higher one: dense lower-rung spikes merge into long chains (DECISIONS entry 13) | 3.4 `S13` | NEW |
| S14 | E2's eligible-event count, n*, the verdict and X1–X3 are conditional on A1's covered ranges (steps 1–14,210 and 52,301–504,510, kept blocks plus rewind portions); the uncovered range is a stated selection threat, and route 3 would not change n* or D_div's unmatchability only as a projection (DECISIONS 59) | 3.3 `S14` | NEW (v0.8) |
| S15 | E2's resampling stream was `default_rng(20261030)` (Amendment 7.4) rather than the 15.9 spawned stream; it affects only p05 (not computed for REFUTE) and argmax (identical under any draw when every lead is 0); E1 and E5 report both streams (D-05) | 3.8 `S15` | NEW (v0.8) |
| S16 | E1's 128-observation block-permutation null is likely too narrow (y remains autocorrelated beyond 128 lags), which can only make its p too small; it cannot turn INDETERMINATE into CONSISTENT (DECISIONS 64) | 4.5 `S16` | NEW (v0.8) |
| S17 | E5's registered circular shift runs over the concatenated kept series and so crosses its gaps; immaterial here because D_div never alarms at headline FA | 4.7 `S17` | NEW (v0.8) |
| S18 | X1–X3 are EXPLORATORY; X1's controls are disjoint tiles but abut, so the Mann–Whitney p is approximate; the v1 result (overlapping controls) is superseded and not quoted (DECISIONS 62–63) | 4.8 `S18` | NEW (v0.8) |

## 7. Conclusions & limits-of-claim

| ID | Conclusion or limit-of-claim | Where (anchor) | Status |
|---|---|---|---|
| C-01 | Claim A on the primary run: E2 REFUTE (C_min ≤ 0) by a tie at zero — D_div was not matchable at headline FA and no detector led any event; §K STOP; stated with the reading rules beside it | 6 `C-01` | NEW |
| C-02 | E3 (replication on A2–A6) was not run: the registered stop rule ended the project before the other runs were staged; no replication claim is made | 6 `C-02` | NEW (restated v0.8) |
| C-03 | Leg B characterization | — | DROPPED — Leg B not run (v0.8) |
| C-04 | E5 alignment control is degenerate at headline FA (no D_div alarms); E4 variants do not make D_div matchable; E1 is INDETERMINATE | 6 `C-04` | NEW |
| C-05 | EXPLORATORY: a gradient-norm rise precedes A1's spikes but sits in the last logging interval; at a 10-step cadence a 320-step fast window cannot exploit it | 6 `C-05` | NEW (v0.8) |
| L-01 | Does NOT propose a new instability mechanism; the second-moment lag is prior art | 1, 5 `L-01` | NEW |
| L-02 | Does NOT claim a stability criterion for Adam | — | DROPPED — not necessary, §K did not proceed (v0.6) |
| L-03 | Does NOT claim the result for β₂ other than 0.95, or for architectures, scales or logging cadences other than A1's | 5.4 `L-03` | NEW |
| L-04 | Does NOT claim savings of any size; no detector warned at the headline rate | 5.4 `L-04` | NEW |
| L-05 | Does NOT claim an analytical bound on the lead over a spike; the Adaptation Rate Theorem is used as motivation only | 3.1 `L-05` | NEW |
| L-06 | Does NOT replace curvature-based analysis; no Hessian quantity is measured | 5.3 `L-06` | NEW |
| L-07 | Does NOT evaluate mitigation (clipping, rewinds) | 5.4 `L-07` | NEW |
| L-08 | Does NOT show that gradient-norm precursors are absent; REFUTE is the planted null's modal outcome on this layout, and the kill rule's power is stated beside it | 5.2 `L-08` | NEW (v0.8) |
| L-09 | Does NOT extend beyond A1's covered ranges and 10-step logging cadence (S11, S14) | 5.4 `L-09` | NEW (v0.8) |
| L-10 | Does NOT offer D_div as a deployable monitor; the refuted detector is not shipped as a tool (DECISIONS 61) | 6 `L-10` | NEW (v0.8) |

## 8. Internal cross-references

| From | To | Purpose | Status |
|---|---|---|---|
| 1 | 4.2, TBL-3 | headline result | NEW |
| 2.1 | 3.2, TBL-1 | deployed alarms become B3/B4 | NEW |
| 2.3 | 5.3 | complementarity with the curvature boundary | NEW |
| 3.1 | EQ-1, EQ-2, EQ-3, FIG-1, L-05 | operator definition and its limit | NEW |
| 3.3 | TBL-2, S14, App. D | data, covered ranges, provenance | NEW |
| 3.4 | EQ-4, 4.1 | spike rule and event counts | NEW |
| 3.5 | EQ-7, EQ-11, 4.2 | contrast, matching and result | NEW |
| 3.7 | App. A, 4.3, TBL-9 | suite and the reading rules | NEW |
| 3.8 | App. D, S15 | amendments and discrepancies | NEW |
| 4.4 | FIG-3, App. C | frontier detail | NEW |
| 4.6 | TBL-5, App. C | sensitivity detail | NEW |
| 4.8 | FIG-8, 5.1 | exploratory diagnostics and their reading | NEW |

## 9. Companion artifacts (nodes outside the 8–12 page manuscript)

| ID | Artifact | Content | Depends on | Status |
|---|---|---|---|---|
| COMP-01 | Plain-English companion | Per the Companion Standard (BINDING page 2kydc08j-614): what was asked, what was registered before looking, what was found (C-01, C-02, C-04, C-05), what is not claimed (L-01, L-03–L-10); written from the shipping paper's numbers | C-01–C-05, L-01–L-10 | NEW |
| IMG-01 | Stand-alone E2 figure | FIG-3 rendered as a stand-alone image for the HF/W&B posts (Phase 4 override 5); numbers from the ledger | FIG-3, LB-E2-frontier | NEW (v0.8) |
| PKG-01 | `pip install` monitor — README | — | — | DROPPED — refuted detector not shipped (DECISIONS 61) |
| PKG-02 | Monitor package code | — | — | DROPPED — refuted detector not shipped (DECISIONS 61) |

## Reconciliation (run before signing; re-run at Phase 4 open/close and Phase 5)

- [x] Every ARG node has ≥1 support and a valid `Depends on` (or "—" for a premise).
- [x] Every citation key maps to ≥1 ARG node or section (no orphan citations; no argument citing a missing reference).
- [x] Every load-bearing finding names a real LB-id in claims.lock; no values in this file. — Confirmed at Phase 3 (DECISIONS 64) and re-confirmed for the v0.8 LB-ids by the outline/ledger set check at Phase 4 open (DECISIONS 65).
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
