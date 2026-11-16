# PRV for E2 (DESIGN D.6; Amendments 14.2 and 17)

Pre-run verification for E2's single real run on A1. Each item is checked before the run command is given. No gradient-norm value is read before the run (15.20); every item below uses metadata, hashes, step indices or null masks only.

**Status:** items 1–4 and 6 done; items 5 and 7 are checked at run time; the sign-off is pending.

| D.6 item | Check | Evidence | Status |
|---|---|---|---|
| 1 | Columns resolved by NAME across segment copies | SOURCES.md series fields; `scripts/a1_schema_check.py`; `analysis/a1_loader.py` reads `_step` and `optim/total_grad_norm` by name; all seven segments processed by name (entry 9) | done |
| 2 | Step monotonicity and duplicates within and across segments (P-SEG) | DESIGN Amendment 2; `verification/A1_structural_report.md`; DECISIONS entries 10–11 | done (entries 10–11) |
| 3 | Pre- vs post-clip gradient norm, against the training commit in each run's config | No training commit is recorded on the public copies: the recorded commit is AI2's copy job's (`bd7cf5f4`; run-025 `43a155fa`). Every `olmo/optim.py` version 2023-10-12 → 2024-04-12, and both copy commits, compute `total_grad_norm` before clipping. Config: AdamW, global fixed clipping at max_grad_norm 1 (entry 40; `scripts/outputs/prv_item3_metadata.json`) | done on the code evidence (entries 40–41); limitation stated in the Methods |
| 4 | Loss cadence (per step vs per micro-batch) | loss every step in all seven used segments (entry 9; SOURCES.md) | done |
| 5 | NaN / non-positive g counted | counted at read time by `analysis/a1_loader.py` (`dropped_total`, `leading_dropped` per kept block) and written to `e2_result.json` | at run |
| 6 | Realised β₂ from each run's config | β₂ = 0.95 (AdamW betas [0.9, 0.95]) read from each of the seven used runs' configs (entry 40) | done |
| 7 | D.1 completeness and SHA-256 re-verification at read time | D.1: entry 9 (seven segments pass). SHA-256: `scripts/prv_hash_check.py`, called by `scripts/run_e2.py` before loading, halts on any mismatch | at run |

**Data selection (DECISIONS entry 2, Addendum C; Amendment 17).** On 2026-11-14 record whether route 3 arrived by 2026-11-13.
- If it did not, E2 uses the gated W&B segments. These are the seven route-1 files listed in SOURCES.md; run-025 fails D.1 and is not used.
- If it did, D.1 and the match against the gated segments are run on it first, with the |rows − historyLineCount| > 1 hard stop added to `a1_process_segment.py` before it is used.

**Run-time guards in `scripts/run_e2.py`** (exercised by `scripts/tests/test_run_e2_dryrun.py` on a synthetic store):
- halts if guarded paths have uncommitted changes;
- halts if `--sources` is overridden;
- halts if `e2_result.json` already exists (one real run);
- halts if the PRV hash check fails, or if there are fewer than 5 eligible events.

**Sign-off (Standard D.6).** Before the run command, JAE confirms in DECISIONS.md:
- every item above is done;
- the data selection;
- the commit at which E2 runs.

## Standard six-pass audit (v1.9.12), 2026-11-15

Findings are F-numbered in DECISIONS.md entry 43. No store file was opened for this audit.

### Pass 1 — Environment / schema contact
- **What E2 reads, by name only:**
  - from each kept segment's route-1 parquet: `_step` and `optim/total_grad_norm`, through `pyarrow.parquet.read_table(columns=[...])` in `analysis/a1_loader.py`;
  - the committed `scripts/outputs/a1_structural_report.json` (segments, owner intervals, kept blocks);
  - the committed `scripts/outputs/a1_events.json` (rung `4.0`: 61 events, 57 eligible, all on series `kept`).
- **File resolution.** `A1/<seg>_<id>_history-*_0000.parquet`, and the loader halts unless exactly one file matches. Seven segments: 001, 008, 010, 013, 016, 017, 018. These are the seven D.1-passing rows of SOURCES.md. Run-025 is not in the structural report's segment list, so it is never read.
- **Names checked against the hashed files** in entries 5 and 9: by name, the same column set in all seven files. OLMo 2 schemas are not read by E2.

### Pass 2 — Spec-to-code line trace (DESIGN rule → code)

| Rule (DESIGN) | Code | Independent check |
|---|---|---|
| y = ln g; dropped g carried forward; block starts at first non-dropped reading (D.2, A1.1, 5.2) | `a1_loader.load_blocks`, `ops.prepare_block` | `test_a1_loader` (dropped reading at 300,000 carried forward) |
| P-SEG ownership, later run wins; kept blocks (Amendment 2) | `a1_loader._owner_map`, kept_blocks from the structural report | `test_a1_loader` ownership checks (73,100 / 73,110 / 212,000 / 212,010 / 337,010 / 408,930) |
| D = SMA_32 − SMA_128, current observation included (D.2) | `ops.sma_incl`, `ops.divergence` | reference `ref_e2.py` (written from DESIGN alone), 269/269 cells identical |
| P_D: expanding percentile since block start, ties ≤, 1,000-observation minimum history (D.2, F15) | `ops.expanding_percentile_le`, `ops.score_div`, `ops._gate` | reference agreement; hand probes |
| B1 z over 50; B2 = y; B3 ZClip α 0.97, warm-up 25, on g; B4 robust-z CUSUM, window 200, min 30, k 1, reset at onset (D.2, Amendments 5 and 9) | `ops.score_b1`, `score_b2`, `score_b3`, `b4_z`, `b4_free_state`, `b4_alarm` | `test_ops` (vendored ZClip and trainscope); reference agreement; `b4_*_loop` reference versions |
| Onset needs a crossing from below; hold H = 32 (P-HOLD) | `ops.alarm_from_scores`, `ops.b4_alarm` | hand probes; reference agreement |
| N_out excludes every event's scan window; n* = round-half-up(FA·N_out/10⁴); n* = 0 guard (D.2, A1.2, A1.11) | `pipeline.run`, `pipeline.scan_mask`, `ops.round_half_up` | assembly probes 16/16 |
| P-FA: smallest candidate with every higher candidate c ≤ n*, scanned from the top (Amendment 6.1) | `ops.match_threshold` | hand probes; reference agreement |
| Coverage stop above 10 % (Amendment 6.2) | `pipeline.run` (`coverage_stop=0.10` default; E2 uses the default) | `test_e2stat`; the suite reports coverage with the stop off, as designed |
| Scan window of SCAN/grid + 1 observations ending at t_e^g; left-censoring; misses = 0; detected needs lead > 0; concurrent (A1.4, P-MISS, P-CENS, Amendment 7 item 6) | `e2stat.lead`, `e2stat.leads_table` | `test_e2stat`; hand probes |
| C_b and C_min on mean lead; joint resampling, 1,000 draws, `default_rng(20261030)`; label (D.3, 7.4, 7.5) | `e2stat.contrasts`, `resample`, `label` | `test_e2stat`; reference agreement |
| Grid 10, scan 1,280, headline FA 1, FA grid {0.5, 2, 5} reported, G1 not-matchable when n* < 2 | `scripts/run_e2.py` constants; FA-grid loop | dry run (`test_run_e2_dryrun.py`) |
| φ̂_y and cell selection (15.5) | `run_e2.phi_hat`, `run_e2.select_cell` | dry run: AR(1) at 0.9 per step, sampled every 10 steps → 0.347 ≈ 0.9¹⁰ |

The suite's A1-structure cells use the same `pipeline.run` call as E2: grid 10, scan 1,280, 1,000 draws, seed 20261030, and A1's own kept-block layout read from the same structural report. The one difference is `coverage_stop`: the suite reports coverage with the stop off, and E2 applies it, as designed.

### Pass 3 — Hand-computation battery
Committed and passing (gate tests, 11/11 on 2026-11-09):
- cross hand probes 56/56;
- assembly probes 16/16;
- dynamic-range cluster and ties probes 10/10;
- the `test_ops`, `test_e2stat` and reference self-test (58 checks) units.

### Pass 4 — Boundary audit
- **Scan-window edges:** inclusive [t_e^g − 1,280, t_e^g]; t_e^g = 10·⌊t_e/10⌋ (`e2stat.lead`). Hand-probed, including the concurrent case.
- **Dedup:** 2,000 steps on A1 (entry 6). Applied in the committed event list (entry 13), not inside E2.
- **Minimum history:** the first 1,000 observations of each block are unscored (`ops._gate`). Eligibility needs every detector to be defined over the whole scan window; the 4 ineligible events (2/1/1 by block) are reproduced by the A1-structure cells in every replicate.
- **Left-censoring:** in alarm at ws and at ws − 10 → lead 1,280, censored (hand-probed).
- **NaN / non-positive g:** carried forward and counted (`dropped_total`). A1 has none on its grid steps (entry 9). A block that is entirely dropped would give `first_step = None`, which cannot occur on A1.
- **Block edges:** no window crosses a gap (each block is scored independently).

### Pass 5 — Assumption inventory

| Assumption | Evidence |
|---|---|
| g is the pre-clip norm | entry 40 (code of the training period) |
| loss logged once per step | entry 9 |
| step index monotone after restarts; ownership by P-SEG | entries 10–11 |
| gradient norm on every grid step of every used segment | entry 9 |
| β₂ = 0.95 | entry 40 |
| the events were enumerated from loss only, before any detector score | entries 12–13 |
| no gradient-norm value read before E2 | 15.20; entry 42 |
| the store files are the hashed ones | PRV hash check inside `run_e2.py` |

### Pass 6 — Adversarial pass: how the run could come out green but be wrong

| Way to be wrong | Guard |
|---|---|
| A different or changed data file | SHA-256 check of all 77 SOURCES rows before loading; halts on any mismatch |
| Wrong segment or ownership stitching | `test_a1_loader` on A1's real step structure |
| Code changed after the ALL PASS | clean-tree guard on `analysis/`, `scripts/`, `reference/`, DESIGN, DECISIONS, SOURCES; grader licence check on the E2-chain files against aad6cf7 |
| Run early, twice, or without sign-off | date window, sign-off entry, and one-run guard (entry 42) |
| **D_div unmatchable on A1.** On grid-10 null series D_div was matchable in only 3–4 of 20 (15.8). If its matched θ is non-finite, D_div never alarms, its leads are all 0, and E2 returns REFUTE for a reason the label does not show. | `run_e2.py` now prints matchable, θ, realised count against n*, and coverage for every detector next to the label, and they are written to `e2_result.json`. Any unmatchable detector is stated in the verdict record beside the label. |
| A coverage stop read as a verdict | the label string is STOP-AND-REPORT and is recorded as such (Amendment 6.2) |
| The A1 layout differs from the suite's | the A1-structure cells read the same `a1_structural_report.json` |
| The selected severity cell is chosen after seeing the result | φ̂_y is computed inside the same run, and the rule is fixed in 15.5 |
