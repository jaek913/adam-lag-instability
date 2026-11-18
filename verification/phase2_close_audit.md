# Phase 2 close audit (draft, 2026-11-18)

Checklist: ClickUp task 86bcvnnva (Phase 2 — Research / Experiment), read in full on 2026-11-16. Status of each box, its evidence, and what is still needed before the box can be flipped and the gate signed.

| # | Box | Status | Evidence | Needed before flip |
|---|---|---|---|---|
| 1 | Theorem checks (operators vs as-published theorems) | done | DECISIONS 15 (T1–T4), before the suite's first run | flip with entry 15 |
| 2 | SOURCES.md complete | done for A1 | SOURCES series fields (entry 14 gap fixed), pre-clip line corrected (entries 40–41) | state A2–A6 not staged (E3 not run, entry 48); flip |
| 3 | Data pulled + hashed | done for A1, with a recorded deviation | entries 7–9 (manifest MD5 + SHA-256); PRV re-hash at every real run (77/77); deviation: no `data/pull.py` — browser route documented by `scripts/a1_process_segment.py` + manifests (entry 14) | flip with the deviation stated |
| 4 | Discrepancy Register + ladder | **open** | D-02, D-03, D-04 closed | **D-01: second focused review still pending.** Its method cites "code at the run's recorded training commit 43a155f"; entry 40 showed that commit is AI2's copy job, not training, so D-01's method/grade must be re-checked (the 10-step finding itself rests on the copied config + the null mask and stands). **New D-05:** DESIGN 15.9's two RNG bullets disagree for E2 (entry 50; no effect on the label) — needs a dossier |
| 5 | Design-stage adversarial review | flipped | 2026-10-30 evidence | — |
| 6 | Experiment-validation gate (every experiment) | done for E2, E1, E4, E5 | E2: suite ALL PASS (e7abad6) + licence re-earned (entry 45); E1/E4/E5: gate tests ALL PASS committed before each real run (entries 50, 51, 53); E3 not run | flip with per-experiment evidence; E3 "not run" stated |
| 7 | PRV (every experiment) | done for E2; abbreviated for E1, E4, E5 | E2: six-pass audit (entry 43) + sign-off (46); E1: six-pass check in entry 50; E5/E4: pins + gates + synthetic dry runs (51, 53) | decide whether E1/E4/E5's checks meet the box or need a written six-pass each |
| 8 | §K kill checkpoint | flipped 2026-11-16 | entries 47; RECORD.md; e2_result.json | 2026-11-20 Amendment 17 line still due |
| 9 | One script per experiment | done, location deviates | E2 `scripts/run_e2.py` → `scripts/outputs/e2/`; E1/E4/E5 `analysis/post/` → `analysis/outputs/post/` | state the location deviation for E2; flip |
| 10 | Rebuild coverage | flipped (N/A) | — | — |
| 11 | OUTLINE kept current | done | v0.6 (f9d3ba0, same sitting as the verdict), v0.7 (e71abc1) | flip |
| 12 | All clean runs committed | done | every real run committed: E2 (6b35777), X1–X3 (2f5168f), E1 (97de969), E5 (9f074d0), E4 (a794365); superseded 15.8(b) v1 kept | flip |
| 13 | DECISIONS current | done | entries 1–54, append-only, prefix checked at each append | flip |
| 14 | Pushed off-machine | **open** | every commit pushed (origin public) | **the data store (`data-stores\adam-lag-instability`) has no off-machine backup** (entry 14) |
| 15 | Close-read | open | — | last, after 1–14 |

Process note: the Standard flips boxes item by item as evidence lands. Boxes 1–3, 6, 7, 9 and 11–13 were not flipped when their evidence landed; that is a process defect to log at close, remediated by flipping each with its evidence reference.
