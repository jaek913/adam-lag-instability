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
