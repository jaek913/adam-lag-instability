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
