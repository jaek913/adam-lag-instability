# Planning Document — Measurement-Lag Instability in Adaptive Optimizers

Draft v0.5 — 2026-10-30 (v0.2: OSF dropped; public-repo-at-design-freeze adopted as the pre-registration timestamp. v0.3: RECORD.md deliverable and dated grading day added per the 2026-10-30 standing rule. v0.4: all six Part 6 decisions recorded. v0.5: repo cloned, data store created, wandb logged in, ClickUp list 901422814376 linked) — SETUP COMPLETE: paste Part 1 into a fresh conversation.
Status: PRE-PHASE-0, decisions complete 2026-10-30. Nothing here is committed yet. Every "PIN" is a construction choice that must be frozen before the first hashed-data run.

This file splits into three repo files once the repo exists: the Startup Prompt (paste as message 1 of the fresh conversation), `THESIS.md`, and `DESIGN.md`. `OUTLINE.md` is built after the prior-art scan (Phase 1).

---

## Part 0 — Pre-registration timestamp decision (answer to the question)

**OSF: skipped (JAE decision, 2026-09-14).** OSF pre-registration is a psychology/social-science convention with almost no footprint in machine learning; the ML audience does not check it.

**What the ML audience does check, and what this project does instead:**
- **Public repo at design freeze.** The repo is made PUBLIC when THESIS.md + DESIGN.md + OUTLINE.md are committed — before any hashed data is touched — so the pre-registration's commit history is publicly readable and cannot be rewritten after the fact. This deliberately inverts the Standard's origin-stays-private-until-launch rule (the same inversion the Standard prescribes for live papers), applied here to a terminal paper because the idea is not protectable and the plan is to publish regardless. Logged as DECISIONS.md entry 1.
- **Design-stage adversarial review BEFORE the public commit** (same venue and cap as 5a; package = THESIS.md + DESIGN.md + the synthetic-suite specification; passes: can every rule fire at a plausible effect in the realised regime, is every experiment in the right report form, is any rule a judgment described as execution). Once public, every change is a dated amendment on the record, so the design must be reviewed first.
- **Citable stamp (accepted 2026-10-30):** a Zenodo DOI on the pre-registration snapshot via the GitHub–Zenodo integration (tag `prereg-v1`); DOI recorded in THESIS.md at Phase 1 close.
- **arXiv v1 date** remains the priority stamp the ML community recognizes; pursued in parallel as endorsement permits.

Sequence: THESIS + DESIGN + OUTLINE drafted → design-stage review → fix round → git commit + tag `prereg-v1` → repo flipped public (+ optional Zenodo snapshot DOI) → Phase 2 opens.

---

## Part 1 — Filled Project Startup Prompt (paste as first message of the new conversation)

=================================================================

New research paper under the Discovery Lattice / Lagging Truth program. Get oriented before doing anything:

1. Read the canonical process — its principles, the contract, and the six-phase map: "Research-to-Publication Standard" — https://app.clickup.com/90141229330/docs/2kydc08j-754 . Follow it exactly; it is the single source of truth. The detailed specs (verify.py checks, the CIC classes, the reconciliation element list, the schemas) live with the phase that uses them — read them from that phase's preflight checklist when you reach it, not all up front.
2. Check MemPalace (wing: lagging-truth-research): run kg_query and search for program conventions and any prior work touching this topic (rooms: series-canon; the 2026-09-14 diary; the AI-application idea in the project memory /areas/ai-training-stability-idea.md). Update it as we go and at session end.
3. This project's task list: https://app.clickup.com/90141229330/v/li/901422814376 (copied from template list 901417149840). Six phases; we start at Phase 0 because this is new work from the thesis, not a rebuild.
4. CHECKLIST-FIRST: the preflight checklists on the phase tasks are the working surface. Before ANY phase work — at phase open and at every session resume — retrieve the current phase's task and read its preflight checklist in full. Work items one at a time, each to verified completion with its own evidence comment on the phase task. Close a phase only when every box is checked with evidence, the checklist has been re-read at close, and the phase gate is signed. Work done without the checklist read is a process defect: log it in DECISIONS.md and audit against the checklist before proceeding.

PROJECT
- Title: Measurement-Lag Instability in Adaptive Optimizers
- Subtitle: A Fast–Slow Divergence Early-Warning Signal for Loss Spikes and a Closed-Form Stability Check for Adam's Second-Moment Window
- Thesis (the claim + the single result that would falsify it): see THESIS.md — read it in full.
- Archetype: empirical-with-verified-theory (JAE, 2026-10-30). The Adam→criterion mapping is a cited application of The Measurement Trap's exponential-kernel result, not an original proposition.
- Lifecycle: terminal — the confirmatory result (Leg A on public logs, Leg B on committed runs) exists before publication; the forward prediction is a standing claim, not a scored cadence.
- Names a tradeable security: no
- GitHub: https://github.com/jaek913/adam-lag-instability (private origin until the prereg-v1 commit, then PUBLIC)
- Repo (all committable work): C:\Users\jaek9\Documents\Repos\adam-lag-instability
- Project-local data store (restricted/large, git-ignored): C:\Users\jaek9\Documents\LaggingTruth\data-stores\adam-lag-instability
- Existing work to draw from: none — new from Phase 0. Cited inputs: The Measurement Trap (π²/2 criterion; exponential-kernel closed form §3.5), The Adaptation Rate Theorem (lead-time bound), The Divergence Theorem (Persistence-Sign Theorem 8b; r* ∈ [3,7]), Cross-Domain Validation (flu-onset detector construction SMA_f − SMA_s > threshold).

REMEMBER (everything else is in the Standard + MemPalace):
- Contract: no committed script on hashed data, no number. Done = verify.py green AND the outline reconciliation green. No outside human gatekeeper.
- Every paper has an OUTLINE.md roadmap, built early from the thesis and versioned in git; the manuscript is written FROM it and reconciled AGAINST it. The outline names load-bearing numbers by LB-id, never their values.
- Verify before concluding: hash-gate and read back after every write; trust nothing unverified.
- You do file edits on my computer; I run git and the PDF build. edit_file collapses $$ to $ — send $$$$ when you need $$ to land. Only an MD5 match confirms disk state.
- Each paper stands alone. Keep DECISIONS.md append-only. Don't suggest breaks or stopping points.
- RECORD IN MIND (standing rule 2026-10-30): the Standard's artifacts are the RECORD record; no second process. At Phase 0 open, set a calendar grading day for the §K kill-rule verdict (THESIS.md Date station). At project close, whichever way Leg A goes, write RECORD.md (one page, six stations, for the reasonofrecord.com lay reader) extracted from THESIS/prereg commit/claims.lock/review package/DECISIONS. RECORD is never named in the paper itself.
- THIS PROJECT: Leg A (public logs, CPU) runs first and carries a pre-registered KILL RULE (DESIGN.md §K). Leg B (own GPU runs) is pinned now but executes only if Leg A does not kill. NO OSF. The repo flips PUBLIC at the design freeze (after the design-stage review, before Phase 2) — the public commit history is the pre-registration (DECISIONS.md entry 1); origin-stays-private-until-launch is deliberately inverted for this paper.

First: restate the project and its current state (from MemPalace + the Standard), confirm which phase we are starting at and why, retrieve and display the starting phase's preflight checklist, then give me the first concrete action (which must be the first unchecked checklist item).

=================================================================

---

## Part 2 — THESIS.md (draft)

**Title.** Measurement-Lag Instability in Adaptive Optimizers.

**The claim.** Adam-family optimizers steer training off exponential trailing averages of gradient statistics (β₁ ≈ 0.9 → ~10-step memory; β₂ ≈ 0.999 → ~1,000-step memory) and feed those averages back into the parameters that generate the next gradients. This is a measurement-feedback loop of the class analyzed in *The Measurement Trap*: a lagged estimate of a persistent variable driving a controller that changes the variable. Two consequences follow and are tested here.

- **A (early warning).** The divergence D(t) = M_f(t) − M_s(t) between a fast and a slow trailing average of the per-step gradient norm turns positive before loss spikes, with a lead that exceeds that of the rolling-statistics alarms in current use at matched false-alarm rate. Mechanism: *Adaptation Rate Theorem* (lead ≈ (w_s − w_f)/2 at midpoint) plus *Persistence-Sign Theorem* (gradient-norm autocorrelation is positive and decaying → D predicts the forward level with positive sign).
- **B (stability boundary).** The stability of the second-moment loop is governed by the persistence φ of the squared gradient norm, the effective window W = 1/(1−β₂), and the feedback strength b_g set by the learning rate, through the exponential-kernel criterion of *The Measurement Trap* §3.5. Runs the criterion classifies as unstable exhibit more spikes/divergence than runs it classifies as stable, at matched everything else.

**Why it matters.** Loss spikes force checkpoint rewinds and batch skips (PaLM: >20 rewinds; a documented 65B run: +30 days, +129 MWh). A signal that fires ahead of them, and a pre-flight check that says which (β₂, LR) pairs are inside the stable region, converts wasted compute into avoided compute. Sized in the session of 2026-09-14 at low single-digit percent of frontier training compute — material to a tool, not to a hyperscaler's budget; stated as such.

**The gap.** Prior work (a) documents that gradient-norm spikes precede loss spikes (OLMo 2; ZClip; SPAM), (b) attributes spikes to Adam's assumption of time-domain gradient independence (Molybog et al. 2023), and (c) characterizes instability via curvature at the "edge of stability" (Cohen et al. 2021, 2022) and small-scale proxies (Wortsman et al. 2023). None states the fast–slow divergence as the alarm with a lead-time bound, and none gives a closed-form window/persistence/gain criterion for the second-moment loop. The prior-art scan (Part 4) must confirm this gap survives before any data work.

**The single result that would falsify it.**
- Claim A is falsified if, on the OLMo-0424 run (the designated primary), the divergence detector's median lead over recorded loss spikes does not exceed the rolling-z-score baseline's median lead at matched false-alarm rate (DESIGN §K). This is also the KILL RULE for the project.
- Claim B is falsified if, across the pre-registered (β₂, LR) grid, the criterion-classified unstable group's spike rate is not greater than the stable group's (one-sided Mann-Whitney, α = 0.05), or if the criterion's continuous diagnostic b_g·S fails to rank-order spike rate (Spearman ≤ 0).

**Archetype.** Empirical-with-verified-theory (JAE, 2026-10-30). The linearized mapping from Adam's update to the criterion's (φ, W, b_g) is a cited application of The Measurement Trap §3.5; the Phase-5a pass is the empirical-archetype pass.

**Lifecycle.** Terminal.

**Date (grading day).** Leg A kill-rule verdict (§K) is graded on the calendar day 21 days after the `prereg-v1` commit (JAE accepted the default 2026-10-30; the exact date is written in at the commit). Leg B verdict (E6/E7) graded on [CALENDAR DATE — set at Phase 2 open if Leg A passes]. Both dates are stated in RECORD.md.

**Registration.** git commit of THESIS+DESIGN+OUTLINE, tagged `prereg-v1`, in a repo made public at that commit and before the first analysis commit; Zenodo snapshot DOI on the prereg-v1 tag: YES (JAE, 2026-10-30), recorded here at Phase 1 close: [DOI]. No OSF.

---

## Part 3 — DESIGN.md (draft)

### D.0 Specification budget (anti-fishing disclosure, half 1)
- Leg A: 1 primary detector specification; 2 baselines; 1 window pair; 1 spike definition; 1 scan window. Robustness: 2 alternate window pairs (reported as sensitivity, no verdict).
- Leg B: 1 model configuration; 1 (β₂ × LR) grid of 6 × 4 = 24 runs; 1 seed per cell + 1 replicate seed on the 4 boundary-adjacent cells (28 runs). No other specifications planned. Any addition = dated amendment.

### D.1 Data manifest (Leg A) — all public; hash-pinned at staging into SOURCES.md
| id | Source | Metrics needed per step | Role |
|---|---|---|---|
| A1 | OLMo-0424 7B, W&B run export | train loss, global grad norm (pre-clip), LR, step | PRIMARY (unstable run; spikes recorded) |
| A2 | OLMo 2 7B W&B export | same | stabilized control |
| A3 | OLMo 2 13B W&B export | same | replication |
| A4 | OLMo 2 32B W&B export | same | replication |
| A5 | BLOOM 176B TensorBoard logs (if grad norm present) | same | replication; include only if grad norm is logged — PIN at staging |
| A6 | [any further public run with per-step grad norm — enumerate at staging; none added after first real run] | | |
Export path: W&B public API → CSV per run; SHA-256 per file; store location recorded. Replicator tolerance: exact (static exports).

### D.2 Operators (Leg A)
- Observable: y(t) = log(global gradient norm) at step t. [PIN: pre-clip norm; if only post-clip is logged for a run, the run is flagged and reported separately.]
- Fast/slow averages: SMA windows (w_f, w_s) = (32, 128) steps — ratio 4:1 per *Divergence Theorem* Theorem 14 (r* ∈ [3,7]). Sensitivity pairs: (16, 64), (64, 256) — reported, no verdict.
- Divergence: D(t) = SMA_{32}(y, t) − SMA_{128}(y, t). Expanding one-sided percentile P_D(t) with minimum history 1,000 steps, no look-ahead.
- Persistence-sign prediction (fixed before any correlation is computed): ACF of y measured on A1; predicted sign of Corr(D_t, y_{t+h}) from Theorem 8b's criterion R̄(h, h+w_f) − R̄(h+w_f, h+w_s) at h = 16 steps. [Expected: positive.]
- Spike definition (mechanical, no hand labels): loss spike at step t if loss(t) > SMA_{128}(loss, t−1) + k·σ_{128}(loss, t−1) with k = 4 [PIN]; spikes within 200 steps of a prior spike are merged into one event (dedup); first step of the event is the event time.
- Detector D_div: alarm when P_D(t) ≥ θ_div. Advance notice = event time − first alarm step inside the scan window [t_event − w_s, t_event]; level check (first bar above θ), left-censoring reported (per *Adaptation Rate Theorem* §5.2 conventions).
- Baseline B1 (rolling z-score, the deployed-tool convention): alarm when (y(t) − mean_{50}(y)) / sd_{50}(y) ≥ θ_z. Window 50 matches the published default of trainpulse-class monitors.
- Baseline B2 (fixed threshold): alarm when y(t) ≥ θ_abs.
- Matching: each detector's threshold is swept; comparison is made at matched false-alarm rate — alarms per 10,000 steps outside any scan window — on a common grid of FA rates {0.5, 1, 2, 5}. Lead is the median advance (steps) across events at each FA rate. The headline comparison is at FA = 1 per 10k steps [PIN].
- Control: block-shuffle null on y (block 128 steps, 1,000 draws) — the divergence's advance ordering under permutation, reported per the *Adaptation Rate Theorem* shuffle-control convention (the mechanism is arithmetic; the shuffle shows what part of the lead is arithmetic vs data-structural).

### D.3 Experiments (Leg A) — classification, severity, report form
- **E1 — Persistence-sign check on A1.** Type: hypothesis test (sign). Rule: realized sign of Corr(D_t, y_{t+16}) matches the pre-registered ACF-criterion sign. Report: verdict + ρ with block-permutation z. Severity: the criterion is near-identity on persistent y; this is a consistency check and is labeled as such (mirrors *Divergence Theorem* §4.3 framing).
- **E2 — Lead-time comparison on A1 (PRIMARY; carries the kill rule).** Type: comparative/benchmark. Rule: at FA = 1/10k, median lead(D_div) > median lead(B1) AND > median lead(B2), with the paired difference's block-bootstrap 90% interval excluding zero (1,000 joint resamples over events; contrast computed within resample, never marginal overlap). Report: verdict + lead distributions + censoring rates + FA-rate curve (the full ROC-style frontier as a figure). Severity: quantified by the synthetic suite at the realized event count on A1 (planted precursor ramps of controlled length; measured detection probability of the rule at lead differences of 25, 50, 100 steps).
- **E3 — Replication on A2–A6.** Type: replication. Rule: sign of the lead advantage matches E2 on a majority of runs with ≥ 3 events; runs with < 3 events are reported descriptively. Report: verdict + per-run table.
- **E4 — Window-pair sensitivity.** Type: robustness. No verdict; qualifies E2.
- **E5 — Shuffle control.** Type: boundary/characterization. Reporting commitment: pooled advance-ordering rate on shuffled vs real; flag trips if the shuffled lead exceeds the real lead (would mean the "lead" is pure window arithmetic with no data content — reported honestly if so).

### D.4 Leg B (pinned now; executes only if Leg A does not kill)
- Model: GPT-2-small class, 124M parameters, nanoGPT-style code committed; data: [FineWeb-Edu 10B subset — PIN exact shard list + hash]; sequence 1,024; batch [PIN]; steps 5,000 per run; bf16; AdamW, β₁ = 0.9, weight decay 0.1, warmup 200, cosine to 10%; grad-clip DISABLED (clipping is itself a controller and would confound the loop) [PIN].
- Grid: β₂ ∈ {0.95, 0.98, 0.99, 0.995, 0.999, 0.9999} × peak LR ∈ {3e-4, 6e-4, 1.2e-3, 2.4e-3}. Seeds fixed and listed. 24 primary runs + 4 replicate seeds at the cells adjacent to the criterion's predicted boundary (identified from the pre-run criterion computation, not from results).
- Measured quantities per run: per-step loss, global grad norm, per-step squared grad norm g²(t); spike count (D.2 definition); divergence flag (loss > 2× initial or NaN).
- Criterion inputs: φ = lag-1 autocorrelation of g²(t) over steps 500–5,000 (levels, not differences — *Measurement Trap* S-4 convention); W_eff = 1/(1−β₂); kernel = exponential (Measurement Trap §3.5 closed form; NOT the uniform-kernel π²/2 constant — the exponential-kernel boundary is the as-proven statement to use); b_g = [PIN — the linearized feedback gain of the Adam update in units of the criterion; this is the weakest link and is declared as a construction pin with a ±50% sensitivity sweep reported. Candidate: b_g ∝ LR / sqrt(v̄) evaluated at the run's steps-500 state. If no defensible linearization exists at Phase 2, Leg B is re-classified as a characterization of spike rate vs (φ, W_eff, LR) with the criterion's ordering as the reporting commitment, and the verdict is withdrawn — dated amendment].
- **E6 — Criterion classification test.** Type: hypothesis test (comparative). Rule: spike rate (spikes per 1,000 steps) of criterion-unstable cells > criterion-stable cells, one-sided Mann-Whitney, α = 0.05; requires ≥ 6 cells in each class (if the pre-run classification yields fewer, the grid is amended before the run — dated). Report: verdict + per-cell table.
- **E7 — Diagnostic ordering.** Type: characterization. Reporting commitment: Spearman of b_g·S against spike rate across all cells, with permutation interval; the graded object is reported regardless of E6.
- **E8 — Early warning on own runs.** Replication of E2 on the Leg B runs pooled (events ≥ 3 required).

### D.5 Synthetic validation suite (committed and ALL PASS before any hashed-data run)
- Planted effect: synthetic y(t) with AR(1) persistence in the measured range, planted spikes preceded by ramps of length L ∈ {25, 50, 100, 200}; the pipeline must recover lead(D_div) ≈ L − (w_s − w_f)/2 within tolerance and beat B1 by the planted margin.
- Planted null: spikes with NO precursor ramp; D_div must not beat B1 (false-support rate ≤ 0.05 at the real event count).
- Planted decision flip: ramps shorter than the B1 window; rule must return REFUTE.
- Dynamic range: lead distributions must separate at planted L differences of 25 steps.
- Leg B suite: synthetic AR(1) g² with known φ under a simulated exponential-kernel loop at known gain; the criterion must classify planted-stable/unstable correctly across the boundary; a planted-ties probe for E7.
- Broken fixture: verify.py must fail on a corrupted hash, an out-of-tolerance value, and an unsigned CIC flag.

### D.6 Pre-Run Verification Protocol
Standard v1.9.12 six-pass audit per experiment, F-numbered in DECISIONS.md, sign-off comment before each run command. Specific adversarial items to enumerate: W&B export column naming across OLMo v1 vs v2 (by-NAME resolution, never position); step-index gaps from restarts (dedup on step; assert monotone); grad-norm logged pre- vs post-clip (assert per run); loss logged per micro-batch vs per step (assert cadence); NaN handling in the spike rule.

### §K — Kill rule (pre-registered)
Grading day: [CALENDAR DATE from THESIS.md Date station]. On that day the verdict is recorded in DECISIONS.md and RECORD.md whether or not E2 has run; an unrun E2 on the grading day is itself recorded (and the day re-set by dated amendment, once).
After E2's single real run on A1: if median lead(D_div) at FA = 1/10k does NOT exceed median lead(B1), the project STOPS. The negative is written up as a short null note (Standard: "if the central thesis is falsified, the null is the paper"), filed in the repo and on Zenodo, with RECORD.md completed as the project's closing artifact, and Leg B does not run. No re-tuning of windows, spike definition, or FA grid after seeing A1 — E4's sensitivity pairs are reported as they fall and do not rescue the verdict.

---

## Part 4 — Prior-art scan: seed list (Phase 0 deliverable; must be completed before any data work)

Must-read, closest to each claim:
- Cohen, Kaur, Li, Kolter, Talwalkar (2021) "Gradient Descent on Neural Networks Typically Occurs at the Edge of Stability"; Cohen et al. (2022) "Adaptive Gradient Methods at the Edge of Stability" — curvature-based stability boundary for Adam. **The scan must state precisely how the EMA-window/persistence criterion differs from the sharpness/(2/η) boundary, or the gap does not survive.**
- Molybog et al. (2023) "A Theory on Adam Instability in Large-Scale Machine Learning" — time-domain independence assumption; closest mechanistic precedent.
- Wortsman et al. (2023) "Small-scale proxies for large-scale Transformer training instabilities" — Leg B's closest design precedent (LR sensitivity, small models).
- OLMo 2 (Walsh et al. 2025, arXiv 2501.00656) §3 — grad-norm spikes precede loss spikes; the data source.
- ZClip (arXiv 2504.02507), SPAM (arXiv 2501.06842) — adaptive spike mitigation; rolling-statistics baselines; the "65B run + 30 days + 129 MWh" citation chain.
- Takase et al. (2023) "Spike No More"; Zhai et al. (2023) attention-logit growth; Chowdhery et al. (2023) PaLM §5 (20 spikes); Zhang et al. (2022) OPT logbook.
- Kingma & Ba (2015) Adam; Reddi et al. (2018) AMSGrad (non-decreasing v — a kernel change, relevant to reform options).
- Deployed monitors as prior art for baselines: trainpulse / trainscope (PyPI) rolling-window spike alarms.
- Own program: The Measurement Trap (§3.5 exponential kernel), Adaptation Rate Theorem, Divergence Theorem (Thm 8b, Thm 14), Cross-Domain Validation (§5.1.2 onset detector).

Novelty statement to defend (draft): "To our knowledge, no prior work (i) states the fast-minus-slow divergence of the gradient-norm as a loss-spike alarm with an analytical lead bound, or (ii) gives a closed-form stability criterion for Adam's second-moment loop in terms of the gradient-statistic persistence, the EMA window, and the learning-rate gain. The edge-of-stability literature characterizes instability through curvature; this work characterizes it through measurement lag. The two are complementary, not competing, and the scan records where they overlap."

---

## Part 5 — Timeline and resources (from the 2026-09-14 sizing)

| Phase | Deliverable | Calendar | JAE hours |
|---|---|---|---|
| 0 | THESIS.md, prior-art scan, archetype/lifecycle decision | 1 wk | 8 |
| 1 | DESIGN.md, OUTLINE.md, design-stage review, git commit + tag, repo flipped public | 1–2 wk | 10 |
| 2 (Leg A) | Staging + hashes, suite ALL PASS, PRV, single real run, KILL decision | 2 wk | 20 |
| 2 (Leg B) | 28 runs on JAE's fleet GPU or a friend's GPU (committed code + seeds, logs returned hashed), criterion computation, E6–E8 | 1–2 wk wall-clock | 10 |
| 3 | claims.lock, CIC, verify.py green | 1 wk | 10 |
| 4 | Manuscript (8–12 pp), companion, `pip install` monitor + HF Trainer callback | 1–2 wk | 15 |
| 5 | Adversarial review, clean-room repro, PDF, Zenodo, arXiv (if endorsed) / HF + W&B report (if not); RECORD.md (one page, six stations, lay-reader) | 1 wk | 10 |
| close | RECORD.md written whichever way §K resolves — also the sole closing deliverable on a kill, alongside the null note | — | 0.5 |

Compute: Leg A CPU only. Leg B: one NVIDIA GPU ≥ 16 GB, ~40–80 GPU-hours total at 124M/5k steps; rented H100 equivalent ≈ $300–800. Cash ceiling: $1,000.

Parallel, from day 1: arXiv endorsement asks (authors of the seed list, EleutherAI Discord, any academic contact), sent with the E2 figure once it exists.

---

## Part 6 — Decisions (all answered by JAE, 2026-10-30)
1. Archetype: empirical-with-verified-theory (cited application).
2. Repo: https://github.com/jaek913/adam-lag-instability ; paths as in Part 1.
3. GPU (Leg B only): JAE's fleet, or a friend's machine if he participates — either way runs execute from committed code and seeds, and logs return hashed.
4. Public at design freeze: YES. Zenodo snapshot DOI on prereg-v1: YES.
5. Pins accepted: k = 4, dedup 200 steps, headline FA = 1 per 10k steps. Frozen; cannot change after A1 is touched.
6. Grading day for §K: prereg-v1 commit + 21 days.

---

## Part 7 — RECORD.md template (filled at project close; lay-reader voice, no math)

```
# [Project title] — Reason of Record

## Register — what we asked, and what we expected before looking
[The question in one sentence. The expected answer, stated before any data was touched. Source: THESIS.md.]

## Enter evidence — the dated, sealed copy
[Commit tag and date the plan was frozen and made public; where the data came from and its fingerprints. Source: prereg-v1 commit, SOURCES.md.]

## Cite — where every number comes from
[The data sets, by name and link; the one or two headline numbers and the file they come from. Source: claims.lock.]

## Oppose — the strongest case against, heard first
[The best objection on record before the test ran, who raised it, what changed because of it. Source: design-stage review package and fix log.]

## Rectify — what we changed, with the original left visible
[Every dated amendment, in one line each; what we got wrong and corrected in public. Source: DECISIONS.md.]

## Date — the grading day and the grade
[The calendar day set in advance; what the rule said; what happened; the verdict in one word (PASS / KILL / AMENDED) and what it cost to honor it.]
```
