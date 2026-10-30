# Design-stage adversarial review — adjudication

Review prompt and package committed at 7194a21 (prompt MD5 29bed842d88c6322bbcbbabfd2bbd0d0; package MD5 bb9982df48b756e8fceae622859753b6, built from THESIS.md 532b7f062b26eda6c587a9362609928b and DESIGN.md dd8170c9176c307d7c40288bee827154). Reviewer: fresh claude.ai incognito chat, no project, no memory, web search off, run by JAE 2026-10-30. Reviewer reply: verification/design_review_transcript.md. Each finding below is adjudicated as AMENDED (reviewer's fix adopted), AMENDED-ADAPTED (fix adopted with a stated change), or REBUTTED (with reason). All amendments were made before the `prereg-v1` freeze; DESIGN.md §D.9's last entry and THESIS.md Amendment A3 record them. JAE decided F2/F3/F4 (FA definition), F10 (lead mechanism) and F13 (E8 form) on 2026-10-30.

| id | sev | disposition | where amended | note |
|---|---|---|---|---|
| F1 | BLOCKER | AMENDED | D.2 lead; D.3 E2; D.5 planted null; THESIS A3(a) | Contrast on mean lead, misses entered as 0; median, detection rate, miss and censored counts reported beside it; a ≤ 50 % detection rate for every detector is stated with the suite's false-support rate there; the suite's planted null covers 30–50 % detection. |
| F2 | BLOCKER | AMENDED-ADAPTED (JAE) | D.2 alarm state, FA, lead; D.7 P-CENS | Left-censored lead 128, flagged; sensitivities lead 0 and excluded-for-all. Adopted only together with a redefinition of FA as alarm duty cycle on out-of-window steps (grid {0.5, 1, 2, 5} %, headline 1 %) and lead defined on alarm state. The reviewer's "an alarm run that intersects any scan window is not a false alarm" is NOT adopted: under onset counting it lets an always-on detector win; under duty cycle every in-window step is already outside the FA numerator and denominator. |
| F3 | BLOCKER | AMENDED-ADAPTED (JAE) | D.4 E8 | Closed by the duty-cycle FA: at ~4,000 scorable steps per Leg B run, 1 % is ~40 alarm steps, so every grid point is realisable; the onset-count grid the reviewer proposed is not needed. |
| F4 | MAJOR | AMENDED-ADAPTED (JAE) | D.2 P-FA; D.7 | Exact-count matching kept, applied to alarm steps: n* = round(FA × N_out); θ = smallest candidate with out-of-window alarm-step count ≤ n*; alarm-step count is monotone in θ, which removes the non-monotonicity the reviewer found for onsets; shortfalls from tied scores reported. |
| F5 | MAJOR | AMENDED | D.1 P-SEG; D.7; D.5 assembly probe | Rewind events retained on their own segment's series, flagged and counted; enter the k-ladder count; sensitivity excluded. |
| F6 | MAJOR | AMENDED | D.2 control; D.3 E5; D.3.0; D.3.1; D.5 | Circular-shift null on the alarm series with a 95th-percentile flag; block shuffle kept as a second characterization without a flag; suite cell added. E5's purpose restated as alignment beyond chance. |
| F7 | MAJOR | AMENDED-ADAPTED | D.3 E3; D.3.1 | NOT RUN below 3 qualifying runs; C_min = 0 counts as not > 0; same statistic as E2. Changed from the reviewer's fix: E3 replicates the direction (C_min > 0) rather than "E2's sign", and runs on any E2 label except INSUFFICIENT EVENTS (not only on PROCEED), so a kill's replication is still reported. |
| F8 | MAJOR | AMENDED | D.4 measured per run, spike rate, E6; D.2 spike definition; D.7 P-DIV; D.5 | Divergence = NaN/inf or > running minimum + 2.0 nats for 50 steps; analysis stops there; < 1,000 completed steps → undefined; Spearman reported over defined cells and over all 24 with diverged cells top-ranked; spike baselines use finite values only. |
| F9 | MAJOR | AMENDED | D.4 measured inputs, E7; D.7 P-PHIHAT; D.5 Leg B | φ̂ on detrended ln g²; raw-level φ̂ as sensitivity; τ against the index and against β₂ with a per-column reorder statement; direction stated (A.4 predicts spike rate decreasing in the index); planted reorder in the suite. |
| F10 | MINOR | AMENDED-ADAPTED (JAE) | D.5; THESIS A3(b) | The reviewer's max(0, L − 48) is NOT adopted: the Adaptation Rate Theorem (Thm 3.1, read from the source) gives the fast average's lead over the slow average after a level change, not a detector's lead over a spike. The suite is graded against a noiseless oracle of the pipeline's own operators (±8 steps); ramps {64, 100, 150, 200}; THESIS's mechanism sentence corrected. |
| F11 | MINOR | AMENDED | §K; D.3 E2; THESIS A3(a) | Still unrun on the re-set day → CLOSE; REFUTE on the point estimate, resamples separate SUPPORT from INCONCLUSIVE. |
| F12 | MAJOR | AMENDED | D.3 E1; D.3.1; THESIS A3(c) | CONSISTENT / INCONSISTENT / INDETERMINATE; never counted as support for Claim A. |
| F13 | MAJOR | AMENDED (JAE: characterization) | D.4 E8; D.3.0; D.3.1; THESIS A3(c) | No label; cluster bootstrap over runs; does not combine with E2. |
| F14 | MINOR | AMENDED | D.3 E5; D.3.1; D.4.2 | Parenthetical removed; extension bounded to one ×2 noise-variance step, at most twice, each a dated amendment. |
| F15 | MAJOR | AMENDED | D.2 observable, gaps and state, B3, B4 | Dropped g is not a gap (carried forward; windows count steps); gap resets enumerated. |
| F16 | MAJOR | AMENDED | D.5 | φ_y grid {0.5, 0.8, 0.9, 0.95, 0.98}; 200 replicates; ±8 steps vs oracle; ≥ 95 % sign agreement; 1e-6 relative; out-of-band extension rule. The reviewer's "planted baselines at expected lead − {10, 25, 50}" is replaced by the oracle (baselines are deterministic functions of y and cannot be planted independently). |
| F17 | MAJOR | AMENDED | D.4 E6, E8 | Cluster bootstrap over the 28 runs for E8; same-step co-occurrence fraction beside E6/E7's permutation intervals. |
| F18 | MINOR | AMENDED | D.2 spike definition, FA, eligibility | Chained dedup; scan windows of all events excluded from FA count and denominator. |
| F19 | MINOR | AMENDED | D.1 A2, A6; D.4 grid; D.7 P-RNG | A6 search strings and inclusion rule; A2/A3 include every stage-1 run in the report's group; seeds 1–24 and 101–104; `default_rng(20261030)`. The reviewer's point that the A2/A3 report renders curves is accepted as a residual risk: inclusion is now mechanical (every run in the group), so viewing it cannot steer selection. |

Fix round: the message in verification/design_review_fixround.md (this adjudication + amended THESIS.md and DESIGN.md in full) is sent once to the same reviewer session; its reply is appended to the transcript and each finding's final state (closed / rebuttal stands / open) is recorded below.

## Fix-round outcome (reviewer reply 2, 2026-10-30)

Fix-round message 1: verification/design_review_fixround.md (MD5 859f060b72adb30e9f62df957183c574, committed at a685b37). Reviewer reply 2 is in the transcript.

**F1–F19 — CLOSED and not reopened.** Closed outright: F1, F2 (censoring; the rebuttal of "touching runs are not false alarms" stands), F3 (mechanically), F6, F7 (adaptation judged sound), F8, F9, F11, F12, F13, F14, F16 (except via N2), F17, F18, F19 (the residual was correctly accepted). F10: the rebuttal of max(0, L − 48) stands. Three closed findings had a one-line residual each, amended in the second round as below: F4 (B4), F5 (cross-series dedup) and F15 (the D_div line).

**Defects introduced by the round-1 amendments, adjudicated by JAE 2026-10-30:**

| id | sev | disposition | where amended | note |
|---|---|---|---|---|
| N1 | BLOCKER | AMENDED — fix (a) | D.2 alarm onset and hold, FA, P-FA; D.3 E2; §K; D.5 new planted null; D.7 P-FA, P-HOLD, frozen line; THESIS A3(a) | Duty cycle made each detector's chance hit rate depend on its alarm-run length. Fix: hold-time alarm H = 32; FA = onsets per 10,000 out-of-window steps (grid {0.5, 1, 2, 5}, headline 1); exact onset-count matching; realised duty cycle n*·H/N_out reported (identical across detectors); P-CENS kept; B4 resets at each onset. D.5 planted null with 1-step and 40-step baselines must give false-REFUTE and false-SUPPORT ≤ 0.05. |
| N2 | MAJOR | AMENDED | D.5 oracle | θ matched on the noisy series by P-FA, then applied to the noiseless series. |
| N3 | MINOR | AMENDED | D.4 E8 | N_out and n* reported per run and FA target; n* < 5 at headline → "FA not matchable", excluded and counted. |
| F4 residual | — | AMENDED | D.2 P-FA, B4; D.7 P-FA | Score path and alarm state recomputed per candidate θ; θ = smallest candidate with onset count ≤ n*; shortfalls and non-monotone regions reported. |
| F5 residual | — | AMENDED | D.1 P-SEG | Dedup applies within a series; a rewind event and an assembled-series event are never merged. |
| F15 residual | — | AMENDED | D.2 D_div | Percentile history "since the last gap". |

**Second fix round (scoped; DECISIONS entry 3).** N1 is a BLOCKER introduced by the fix round itself, so it falls under the Standard's load-bearing-defect exception to the one-round cap. A second message, verification/design_review_fixround2.md, is sent once to the same session and is scoped strictly to N1, N2, N3 and the F4, F5 and F15 residuals. F1–F19 are not reopened.

## Second fix-round outcome (reviewer reply 3, 2026-10-30) — REVIEW CLOSED

Fix-round message 2: verification/design_review_fixround2.md (MD5 b97e3c92e9c444007a251f44060f71ab, committed at 1492a04). Reviewer reply 3 is in the transcript.

| id | reviewer | final disposition |
|---|---|---|
| N1 | CLOSED, with two notes | CLOSED. Note (i), residual onset clustering, and note (ii), the meaning of P-CENS under P-HOLD, are stated in DESIGN §D.2 as Methods statements; no rule change (JAE). |
| N2 | CLOSED (matching), introduced N4 | CLOSED. |
| N3 | CLOSED | CLOSED. |
| F4 residual | CLOSED | CLOSED. |
| F5 residual | CLOSED | CLOSED. |
| F15 residual | CLOSED | CLOSED. |
| N4 | NEW — MINOR | AMENDED without further review (DECISIONS entry 3 item 5 and Addendum A). The oracle series is the planted series with noise amplitude × 10⁻³; D.5 asserts every score on it is finite. |

**Final state:** every finding (F1–F19, N1–N4 and the three residuals) is closed or amended. No rebuttal is outstanding, and no finding is open. The design-stage adversarial review is CLOSED on 2026-10-30, before the `prereg-v1` public commit.
