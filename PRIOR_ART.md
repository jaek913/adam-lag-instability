# PRIOR_ART — Measurement-Lag Instability in Adaptive Optimizers

Phase 0 novelty and significance gate. Dated 2026-10-30. Scan performed 2026-10-30 from the planning-doc Part 4 seed list plus a live web search for work newer than the September 2026 seed list. Verdict and the scope decisions in §6–§7 were made by JAE on 2026-10-30 after reading the scan.

## 1. Method

- Seed list: planning/adam-lag-instability_planning.md Part 4.
- Live search (2026-10-30), aimed at three things the seed list could have missed: (a) fast/slow averages of gradient statistics used as a spike alarm; (b) window-based or beta2-based stability criteria for Adam's second moment; (c) the current deployed training monitors (trainpulse, trainscope, ZClip).
- Bibliographic accuracy of every entry is re-checked at Phase 5b (all-tier citation check); entries marked [seed, not re-read] were carried from the seed list without a fresh read this session.

## 2. Prior art bearing on Claim A (fast–slow divergence as a loss-spike early warning)

| Work | What it establishes | What it leaves open |
|---|---|---|
| OLMo 2 (Walsh et al. 2025, arXiv 2501.00656) §3 | On OLMo-0424, larger gradient-norm spikes often came before loss spikes; slow growth of the gradient norm over training went with more frequent spikes. | No alarm, no lead-time measurement, no detector comparison. Supplies Leg A's primary data and the precursor premise. |
| ZClip (Kumar et al. 2025, arXiv 2504.02507; PyPI `zclip`) | Deployed adaptive clipping: EMA of the gradient-norm mean and variance, spike flagged when the current norm's z-score exceeds a threshold. Documented defaults alpha = 0.97, z_thresh = 2.5. | Built to clip, not to warn; no lead time reported; the fast side is the raw single-step reading. See §4. |
| SPAM (Huang et al., ICLR 2025, arXiv 2501.06842) | Gradient Spike Score = current gradient magnitude relative to its running average; spikes up to ~1000x typical; momentum reset + spike-aware clipping. | A same-step ratio test; no lead time. |
| AdaGC (arXiv 2502.11034); GradientStabilizer (arXiv 2502.17055, ICML 2026) | Per-tensor or global EMA statistics of gradient norms used to bound or rescale updates. | Mitigation, not early warning; single EMA against the current reading. |
| trainscope (PyPI, 0.3–0.8, 2026) | Post-mortem spike debugger. Spike detector: rolling-window z-score (threshold 3.5) in early versions; CUSUM change-point by default in later versions, with the package claiming CUSUM catches slow loss drifts 5–10 steps before the loss explodes. Also logs Adam second-moment (v) norm as a "stale momentum" indicator. | No published validation of lead time; no matched false-alarm comparison. CUSUM is the strongest existing competitor for drift-type precursors. |
| trainpulse (GitHub stef41/trainpulse; PyPI) | Lightweight monitor with loss-spike, gradient-explosion, NaN and plateau detectors. | Detector windows/thresholds for loss and gradient spikes NOT confirmed in its public docs this session — so no parameter is attributed to it. |
| R-Metric (Fatima, EMNLP 2025 Industry Track, pp. 2897–2913) | Composite failure-risk score (hardware events, cross-worker gradient-norm variance, validation drift) with empirical lead times; baselines include z-score loss-spike detection and a gradient-norm threshold. | Targets failures (loss >100 / NaN), not spikes; no fast/slow construction; no analytical lead bound. |
| Takase et al., "Spike No More" (COLM 2025, arXiv 2312.16903) | Loss spikes tied to sudden gradient-norm growth; architectural conditions (small sub-layers, large shortcut) that prevent them. | Prevention by design; no detector. |
| Practitioner guidance (e.g. Chowdhery et al. 2023 PaLM §5 rewind-and-skip, ~20 spikes) [seed, not re-read] | Gradient norm is the standard leading indicator; rewinds cost compute. | Motivation only. |

**Gap for Claim A — SURVIVES.** No work found states the difference between a smoothed fast and a slow trailing average of the gradient norm as a spike alarm, gives an analytical lead-time bound for it, or compares detectors' lead time at matched false-alarm rate on public training logs.

## 3. Prior art bearing on Claim B (stability of the second-moment loop)

| Work | What it establishes | What it leaves open |
|---|---|---|
| Shazeer & Stern 2018, Adafactor (arXiv 1804.04235) §5 | First names the "out-of-date second moment estimator": with slow decay (high beta2) the estimate lags the gradients and training becomes unstable without warm-up; RMS of the normalized update far from 1 signals it. | Diagnosis and a remedy (update clipping); no stability boundary. |
| Wortsman, Dettmers et al. 2023, "Stable and low-precision training…" (NeurIPS 2023, arXiv 2304.13013) | In CLIP training, loss spikes follow 1–8 steps after squared gradients are underestimated by the AdamW second moment; lowering beta2 reduces spikes; per-layer RMS ratio as the indicator. | Mechanism + indicator; no closed-form boundary in beta2 and learning rate. |
| Molybog et al. 2023 (arXiv 2304.09871) | At 7B–546B, Adam can enter a state where the update is large and uncorrelated with the descent direction; attributed to time-domain correlation of early-layer gradient estimates (breaking Adam's independence assumption). | Qualitative theory; no criterion. |
| Ma, Wu & E (MSML 2022, PMLR 145; arXiv 2009.06125) | Late-phase Adam shows oscillation, spike, or divergence regimes depending on (beta1, beta2); smoother when the two are close. | Qualitative regimes. |
| Cohen et al. 2021, "Gradient Descent … Edge of Stability" (ICLR 2021) [seed, not re-read] | Sharpness rises to and hovers at 2/eta under full-batch GD. | Non-adaptive. |
| Cohen et al., "Adaptive Gradient Methods at the Edge of Stability" (arXiv 2207.14484; NeurIPS 2023 workshop) | Full-batch Adam trains where the preconditioned sharpness equilibrates at the frozen-preconditioner threshold (38/eta for beta1 = 0.9); adaptive methods keep entering high-curvature regions by adapting the preconditioner. | Stability judged on the parameter loop with the preconditioner held fixed; preconditioner dynamics not modeled as a loop. |
| **Bai et al., "Adaptive Preconditioners Trigger Loss Spikes in Adam" (arXiv 2506.04805 v2 2026-05-25; ICML 2026)** | **Closest precedent.** With large beta2 the second-moment estimate decouples from current squared gradients and decays by itself; this pushes the preconditioned-Hessian maximum eigenvalue past 2/eta for sustained periods → spikes; spike occurs when gradient-directional curvature exceeds 2/eta; proposes a curvature-based spike predictor; reducing beta2 suppresses spikes. | Boundary stated in curvature (Hessian) terms; no closed form in the second-moment window, gradient-statistic persistence, and learning-rate gain; predictor needs curvature information, not just logged scalars. |
| **Tang, Chen & Liu, "Beyond Quadratic Loss: The Stability Phase Diagram of Adam" (arXiv 2609.18314, 2026-09-25)** | Maps spiky vs stable training over the (beta1, beta2) plane; finds an approximately power-law boundary (1−beta2) ≈ C·(1−beta1)^p, fitted per setting; mechanism attributed to second-moment decay in calm phases plus super-quadratic loss geometry; local condition uses the Cohen/Bai threshold. | Boundary is fitted, not derived; axes are (beta1, beta2), not (beta2, learning rate, persistence); no early-warning signal. |
| "Towards Understanding Adam Convergence on Highly Degenerate Polynomials" (arXiv 2603.09581, 2026) | Derived local-stability phase diagram on degenerate polynomials (stable / spikes / sign-GD oscillation regimes as powers of beta2 vs beta1); same decoupling mechanism. | Toy objectives; no observable-only criterion. |
| Kourkoutas-beta (arXiv 2508.12996) | Adapts beta2 online to gradient "spikiness". | A remedy, not a criterion. |
| Own program: The Measurement Trap (§3.5 exponential kernel), The Adaptation Rate Theorem, The Divergence Theorem (Thm 8b, Thm 14), Cross-Domain Validation (§5.1.2 onset detector) | Cited inputs (see THESIS.md). | — |

**Gap for Claim B — SURVIVES ONLY AS NARROWED.** The mechanism — Adam's second moment lags the squared gradients and the lag destabilizes training — is established prior art (Shazeer & Stern 2018; Wortsman et al. 2023; Bai et al. 2026; Tang, Chen & Liu 2026). This paper does not claim it. What no work found provides is a **Hessian-free, closed-form, observable-only** check: a criterion computed from quantities already in a training log (persistence phi of the squared gradient norm, effective window W = 1/(1−beta2), feedback gain b_g set by the learning rate) that classifies (beta2, learning-rate) settings as stable or unstable **before** the runs. Claim B is restated accordingly (THESIS.md Amendment A1).

## 4. The deployed z-score test is itself a fast/slow divergence with w_f = 1 (added by JAE, 2026-10-30)

ZClip's test compares the current gradient-norm reading against its EMA (alpha = 0.97, an effective window of about 33 steps), scaled by the EMA standard deviation. That is a fast–slow divergence whose fast window is a single step (w_f = 1). The same holds for SPAM's spike score and trainscope's rolling z-score. This paper's contribution on Claim A is therefore narrower than "a divergence alarm": it is the **smoothed fast window** — w_f = 32 against w_s = 128, ratio r = 4 inside the Divergence Theorem's Theorem 14 band r* in [3, 7] — together with the **analytical lead bound** from the Adaptation Rate Theorem. Smoothing trades single-step responsiveness for noise rejection; whether that trade wins is exactly what experiment E2 tests at matched false-alarm rate. **If D_div does not beat the raw-reading tests at matched false-alarm rate, that is a reportable finding against this paper's Claim A, not a null to be explained away.**

## 5. The edge-of-stability distinction (Phase 0 gate requirement)

- **Cohen et al. boundary:** a curvature condition on the parameter-update loop. Instability occurs when the largest eigenvalue of the preconditioned Hessian exceeds the frozen-preconditioner threshold (2/eta without momentum; 38/eta for beta1 = 0.9). The preconditioner is held fixed; its own dynamics are outside the condition. Measuring it requires curvature (Hessian or Hessian-vector products).
- **This paper's criterion:** a condition on the preconditioner's own feedback loop — the second-moment EMA as a lagged measurement of a persistent variable (squared gradient norm) whose estimate feeds back into the process generating it — the measurement-feedback class analyzed in The Measurement Trap. Inputs are time-series quantities from the training log (phi, W, b_g); no curvature is computed.
- **How they relate:** complementary, not competing. Bai et al. show the preconditioner's lag is what pushes the system across the curvature boundary. The curvature boundary says where instability is; the lag criterion is proposed as an observable-only predictor of when the preconditioner's lag will carry the system there. Where the two disagree on a Leg B cell, both are reported.

## 6. Verdict (Phase 0 novelty gate)

- **Claim A: gap survives as written** (with the §4 scope statement).
- **Claim B: gap survives only as narrowed** — a Hessian-free, closed-form, observable-only predictor of the established second-moment lag mechanism; not a new mechanism.
- **Project proceeds.** No STOP condition is met.
- *(Corrected 2026-10-30, Phase 1, after the design-stage review — see §10 "Verdict correction". Both verdict lines above are superseded in part. The Claim A gap no longer includes an analytical lead-time bound, and the Claim B predictor is not delivered: Claim B is a characterization.)*

## 7. Why closing the gap matters

Spike handling today is reactive: deployed tools clip or flag on the step the gradient norm jumps, and rewinds cost compute after the fact. A warning with measured lead time at a known false-alarm rate, built from one scalar every run already logs, can be wired into existing callbacks with no extra computation. A pre-flight check from logged quantities that says which beta2/learning-rate settings sit near the lag-driven boundary — without Hessian computations — would let practitioners avoid unstable configurations before spending the run. Either result, positive or negative, is measured against the tools practitioners actually use.

## 8. Carried to Phase 1 (DESIGN amendments required before `prereg-v1`; JAE decisions 2026-10-30)

1. **Baselines.** Add B3 = ZClip EMA z-score at its documented defaults (alpha = 0.97, z = 2.5) and B4 = CUSUM at trainscope's documented default. §K compares D_div against the BEST baseline using the per-resample minimum contrast (Standard v1.9.11), not B1 alone.
2. **Attribution.** Strike "window 50 matches the published default of trainpulse-class monitors" from DESIGN D.2. Every baseline parameter is either a cited documented default or a declared construction pin with a sensitivity sweep.
3. **Leg B pre-run classification.** Before the Leg B grid is frozen, compute the criterion's classification of all 24 cells from literature-typical phi. If fewer than 6 cells classify as unstable, trigger DESIGN D.4's fallback (E6 re-characterized, verdict withdrawn) by dated amendment before `prereg-v1`. Context: in The Measurement Trap, moving to an exponential kernel was one of the reforms that restored stability, so the exponential-kernel criterion may classify most Adam settings as stable.

## 9. References (seed for OUTLINE.md and the literature review)

- Bai, Zhou, Zhao, Li, Li, Xiong, Yang, Zhang, Xu. Adaptive Preconditioners Trigger Loss Spikes in Adam. ICML 2026. arXiv:2506.04805.
- Cohen, Kaur, Li, Kolter, Talwalkar. Gradient Descent on Neural Networks Typically Occurs at the Edge of Stability. ICLR 2021. [seed, not re-read]
- Cohen, Ghorbani, Krishnan, Agarwal, Medapati, Badura, Suo, Cardoze, Nado, Dahl, Gilmer. Adaptive Gradient Methods at the Edge of Stability. arXiv:2207.14484.
- Fatima. A Proactive Reliability Metric for Detecting Failures in Large Language Model Training. EMNLP 2025 Industry Track, 2897–2913.
- Huang, Zhu, Jin, Liu, Wang, Liu. SPAM: Spike-Aware Adam with Momentum Reset for Stable LLM Training. ICLR 2025. arXiv:2501.06842.
- Huang et al. GradientStabilizer: Fix the Norm, Not the Gradient. ICML 2026. arXiv:2502.17055.
- Kumar, Owen, Roy Chowdhury, Güra. ZClip: Adaptive Spike Mitigation for LLM Pre-Training. arXiv:2504.02507.
- Ma, Wu, E. A Qualitative Study of the Dynamic Behavior for Adaptive Gradient Algorithms. MSML 2022, PMLR 145:671–692. arXiv:2009.06125.
- Molybog et al. A Theory on Adam Instability in Large-Scale Machine Learning. arXiv:2304.09871.
- OLMo team (Walsh et al.). 2 OLMo 2 Furious. arXiv:2501.00656.
- Shazeer, Stern. Adafactor: Adaptive Learning Rates with Sublinear Memory Cost. ICML 2018. arXiv:1804.04235.
- Takase, Kiyono, Kobayashi, Suzuki. Spike No More: Stabilizing the Pre-training of Large Language Models. COLM 2025. arXiv:2312.16903.
- Tang, Chen, Liu. Beyond Quadratic Loss: The Stability Phase Diagram of Adam. arXiv:2609.18314.
- Towards Understanding Adam Convergence on Highly Degenerate Polynomials. arXiv:2603.09581.
- Wang et al. AdaGC: Improving Training Stability for Large Language Model Pretraining. arXiv:2502.11034.
- Wortsman, Dettmers, Zettlemoyer, Morcos, Farhadi, Schmidt. Stable and low-precision training for large-scale vision-language models. NeurIPS 2023. arXiv:2304.13013.
- Wortsman et al. Small-scale proxies for large-scale Transformer training instabilities. ICLR 2024. arXiv:2309.14322.
- Kourkoutas-beta: a sunspike-driven Adam optimizer. arXiv:2508.12996.
- Chowdhery et al. PaLM. 2023, §5. [seed, not re-read]
- Kingma, Ba. Adam. ICLR 2015; Reddi, Kale, Kumar. On the Convergence of Adam and Beyond (AMSGrad). ICLR 2018. [seed, not re-read]
- Software: trainscope (PyPI); trainpulse (PyPI / github.com/stef41/trainpulse); zclip (PyPI).
- Own program: The Measurement Trap; The Adaptation Rate Theorem; The Divergence Theorem; Cross-Domain Validation.

## 10. Correction note (2026-10-30, Phase 1 — after reading the source)

- **Citation.** Every reference above to "The Measurement Trap §3.5 (exponential kernel)" should read **The Measurement Trap, Appendix A.4 (PRF-A4), EQ-5/EQ-6**. §3.5 of that paper is the cross-disciplinary correspondence with Campbell & Jessop (2009); the exponential-kernel closed form is in Appendix A.4. The error came from the planning doc and is corrected in DESIGN.md D.4.1 and, by amendment, in THESIS.md.
- **Claim B gap (§3).** DESIGN.md D.4.1 finds that the A.4 exponential-kernel boundary does not map cleanly onto Adam's second-moment loop in observable-only terms (feedback is multiplicative and curvature-dependent; Adam's v_t includes the current gradient; S and π²/2 are uniform-kernel quantities). The "Hessian-free, closed-form, observable-only predictor" stated in §3's gap verdict is therefore not delivered as a verdict-bearing claim; Claim B is carried as a characterization of spike rate across the β₂ × LR grid, ordered by the A.4 robustness index. The §6 verdict for Claim A is unchanged.
- **Authors (2026-10-30, Phase 1).** §3 and §9 list arXiv:2603.09581 without authors; per its arXiv record the authors are Zhiwei Bai, Jiajie Zhao, Zhangchen Zhou, Zhi-Qin John Xu and Yaoyu Zhang (submitted 2026-03-10) — the same group as Bai et al., arXiv:2506.04805. OUTLINE.md keys them Bai-2026b and Bai-2026a.
- **Verdict correction (§6; 2026-10-30, Phase 1, after the design-stage review).** **Claim A:** §2's gap statement, §4 ("together with the analytical lead bound from the Adaptation Rate Theorem") and §6 ("survives as written") all credit the paper with an analytical lead-time bound. That credit is withdrawn. The Adaptation Rate Theorem (Thm 3.1) gives the lead of the fast average over the slow average after a level change, not a detector's lead over a loss spike (THESIS Amendment A3(b); design review F10). The Claim A gap that survives: no work found states the difference between a smoothed fast and a slow trailing average of the gradient norm as a spike alarm, or compares detectors' lead time at matched false-alarm rate on public training logs. The scope statement of §4 (deployed tests are w_f = 1 divergences) stands. **Claim B:** as §10's Claim B bullet already records, the "Hessian-free, closed-form, observable-only predictor" of §3 and §6 is not delivered. Claim B is a characterization of spike rate across the β₂ × LR grid, ordered by the A.4 index (THESIS A2(d)). The project-proceeds verdict is unchanged: Claim A's narrowed gap still survives and is tested by E2.
