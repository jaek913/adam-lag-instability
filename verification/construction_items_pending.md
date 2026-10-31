# Construction details found while building the D.5 suite — pending decision

Opened 2026-10-31. These are points the frozen text plus Amendments 1–6 leave unstated, found while writing `analysis/ops.py` and `analysis/e2stat.py`. Each is held for one amendment, together with the adjudicated findings of the Amendments 2–6 review (`verification/amendments2-6_review_prompt.md`). None is settled by the code. Where the code needs a value now, it carries the **proposal**, marked provisional; the suite is not frozen or run for the record until these are decided.

| # | Item | Where | Proposal (provisional in code) | Alternative |
|---|---|---|---|---|
| 1 | B4 candidate thresholds. B4's score path depends on θ through its reset at each onset, so "the distinct score values on out-of-window scored observations" is path-dependent. | P-FA (D.2), Amendment 6 | Candidates are taken from B4's reset-free path (θ = none). c(v) is evaluated on the path recomputed at each candidate v. | Iterate candidates from each recomputed path; or use a fixed fine grid. |
| 2 | N_out: per detector or common. | D.2 "False-alarm rate" | One common denominator for all detectors: observations with j ≥ 1,000 outside every scan window. | Per detector, counting only observations where that detector's score is defined (B1's sd = 0 observations would move its n*). |
| 3 | Fresh crossing after an undefined score. | P-HOLD | An undefined s(j−1) counts as below θ, the same convention as the first scored observation. | An undefined s(j−1) blocks an onset at j. |
| 4 | P-RNG stream. "Every resample, permutation, shift and suite draw uses `default_rng(20261030)`" does not say whether one generator is shared in sequence (results would depend on run order) or created per procedure. | D.7 P-RNG | A fresh `default_rng(20261030)` per procedure (E2 resamples; E1 permutation; E5 shifts; each suite cell × replicate uses a documented seed derivation). | One shared generator, with a fixed procedure order. |
| 5 | Percentile method for the 5th percentile of resampled C_min. | D.3 E2 | numpy default (`method="linear"`). | Nearest rank. |
| 6 | "Detected" for the detection rate. | D.3 E2 reporting | Detected = any in-window observation in alarm, including at t_e^g (lead 0). | Lead > 0 (the E5 advance-ordering definition). |
| 7 | Planted precursor: shape and amplitude. D.5 gives ramp lengths L ∈ {64, 100, 150, 200} (A1 grid cell: {640, 1,000, 1,500, 2,000} steps) but no shape or amplitude. That choice sets the power the suite measures. | D.5 "Planted effect" | A linear rise in y from 0 to A over the L observations ending at the event, then back to baseline. A ∈ {1, 2, 3} × the stationary SD of y. Every A reported; pass criteria applied at each. Synthetic g = exp(y) (y = ln g by definition). | One fixed A; or an exponential or step precursor. |
| 8 | Suite events: planted directly, or found by the spike rule on a generated loss. | D.5 | Planted directly in the detector cells. The spike rule is validated separately (`scripts/tests/test_a1_events.py`; Amendment 3 suite cases). One end-to-end cell generates loss spikes and runs the spike rule. | Generated loss in every cell. |

## Decided 2026-10-31 (JAE) — DECISIONS entry 18, DESIGN Amendment 7

| # | Decision |
|---|---|
| 1 | Accepted as proposed (Amendment 7.1). |
| 2 | Accepted as proposed (Amendment 7.2). |
| 3 | Accepted as proposed (Amendment 7.3). |
| 4 | Accepted as proposed, with the suite seed derivation `default_rng([20261030, cell, replicate])` (Amendment 7.4). |
| 5 | Accepted as proposed (Amendment 7.5). |
| 6 | **Changed:** detected requires lead > 0; an alarm first at t_e^g is reported separately as "concurrent"; the mean lead is unaffected (Amendment 7.6). |
| 7 | Accepted as proposed (Amendment 7.7). |
| 8 | Accepted, with the end-to-end loss-series cell run in both a planted-effect and a planted-null case (Amendment 7.8). |

Status: all eight items are closed; the code no longer carries provisional values for them.
