# Package — second focused review of discrepancies D-01 and D-05

Verbatim excerpts from the project's committed files. Nothing else is provided.

## 1. The two dossier rows (verification/Discrepancy_Register.md)

| id | opened | item | blast radius | method that answered | grade | adjudication | status |
|---|---|---|---|---|---|---|---|
| D-01 | 2026-10-30 | A1 `optim/total_grad_norm` is logged every 10 steps (`metrics_log_interval: 10`; training commit 43a155f returns no optimizer metrics on other steps). DESIGN D.1/D.2 and DECISIONS entry 2 assumed every step, based on main @ 090253d. | Leg A on A1: every D.2 operator on y (windows 32/128, 1,000-step minimum history, lead in steps, the hold H = 32, threshold matching); E1 lags; E2/§K; E4; E5; D.5 suite cadence; PRV item 4; OUTLINE S2/S8. Not Leg B, which logs its own runs every step. | (3) version reconciliation: code at the run's recorded training commit vs main, confirmed against the run config and the staged file's null mask | ground truth | Original (entry 2) wrong for this run's commit; data and code agree. Design consequence adjudicated: DESIGN Amendment 1 + THESIS A4 (JAE option (c); scoped independent check, verification/amendment1_review.md; DECISIONS entry 6). | ADJUDICATED — second focused review pending |
| D-05 | 2026-11-16 | DESIGN 15.9 contradicts itself on E2's real-data RNG. Its first bullet says E2's resamples on A1 use a fresh `default_rng(20261030)`, "exactly as the E2 run on A1 will"; its second says the real-data E2 generator is `default_rng(SeedSequence(20261030, spawn_key=(1,)))`. 7.4 agrees with the first bullet. `run_e2.py` used `default_rng(20261030)` (`pipeline.run` default). | E2 resampling outputs only: p05 and the argmax shares. The label is decided by the point estimate C_min = 0.0 ≤ 0 (no resampling), and p05 is not computed for REFUTE. With every lead 0, the argmax shares (0.2 each) are the same under any generator. E1 and E5 use the second bullet's streams, with the 7.4 stream reported beside them (entries 50–52). The suite is unaffected: within each replicate its resampling uses a fresh `default_rng(20261030)` (`scripts/suite/run_suite.py`), as 15.9's first bullet says. | (1) framing gate: both bullets are the registered text at 15.9, read verbatim; (2) stated-value triage: the code path that ran is `pipeline.run(seed=20261030)`, read from the committed code at f486ced | ground truth | Both readings are recorded. E2's reported quantities are identical under either stream, so no result changes. Disclosed in the null note's Methods (DECISIONS 50). | OPEN — second focused review pending |

## 2. DECISIONS.md entry 5 (first data contact; source of D-01)

## Entry 5 (2026-10-30) — First data contact on A1 (Phase 2 override 3): the column is present, but logged every 10 steps; route 1 is incomplete

1. **File staged.**
   - Source: W&B (CoreWeave Forge) artifact `ai2-llm/OLMo-7B/run-u3obk6mj-history:v2`, run `OLMo-1.7-7B-run-025`, created 2024-04-18. Its only file is `0000.parquet`, 1,527,446 bytes.
   - Manifest MD5 read from the artifact's file metadata in the logged-in page: `CEi3D6WMrZjt9kt3RIcTlA==` (base64), which is 0848b70fa58cad98edf64b7744871394 in hex.
   - Downloaded 2026-10-30 19:32 CT through the file's signed storage URL. The first click on W&B's download button saved nothing. Chrome saved the file under its storage object name, `0848b70fa58cad98edf64b7744871394`, with no extension.
   - Local hashes: MD5 0848b70fa58cad98edf64b7744871394 (matches the manifest); SHA-256 bd1a2f425bd018d56114524195468fe6c1fb7e7a90f76f384997f93a563559ee.
   - Recorded in scripts/outputs/a1_run025_schema.json.
2. **What was read.**
   - The parquet schema (column names), the row count, the `_step` index, and the per-row null mask of `optim/total_grad_norm` and `train/CrossEntropyLoss`.
   - From the run's W&B metadata: `historyLineCount`, the training commit, and `optimizer.metrics_log_interval`.
   - **No metric value was printed, saved or inspected.** To count non-null rows, one read loaded the two metric columns into memory, but no value was displayed.
   - The check ran on a copy JAE attached to the working session. The project-local store copy is still pending; see item 6.
3. **Columns.**
   - `optim/total_grad_norm` and `train/CrossEntropyLoss` are present by name.
   - Also present: `optim/learning_rate_group0`, `optim/clipping_rate`, `_step`, throughput columns, 45 `eval/` columns and 2,080 per-parameter `optim/` columns (2,137 columns in total).
4. **Finding A — route 1 is not the full history.**
   - The artifact parquet has 383 rows: step 0; steps 522,000–542,000 every 1,000 (21 rows); and steps 543,000–543,360 every step (361 rows).
   - The run's own `historyLineCount` on the server is 22,361.
   - The D.1 completeness check fails: 383 ≠ 543,360 − 0 + 1, and the steps are not contiguous.
   - Under D.1, this segment cannot be used by route 1. Discrepancy Register D-02.
5. **Finding B — A1 logs `optim/total_grad_norm` every 10 steps, not every step.**
   - In the contiguous block, the gradient norm is non-null on 37 of 361 rows, spaced exactly 10 steps apart. The loss is non-null on every row.
   - The run's config has `optimizer.metrics_log_interval: 10`, which matches allenai/OLMo `configs/official-0724/OLMo-7B-0424.yaml`.
   - The training commit recorded on the run is `43a155faf0c41c849fc2e14fe375a6bc57ed89fb` (2024-04-18). In that commit's `olmo/optim.py`, `clip_grads_and_collect_metrics` returns `{}` when `collect_param_metrics` is False. So `total_grad_norm` is logged only on optimizer-metric steps, every 10 steps.
   - Entry 2's "expected every step" was read from main at 090253d, where a later change (`# total_grad_norm is computed at all steps…`) logs it every step.
   - This is a version-reconciliation result: the code at the training commit and the data agree.
   - Consequence: DESIGN D.2's per-step operators (SMA_32/SMA_128 on y, the minimum history, leads in steps) cannot be applied to A1 as written.
   - Discrepancy Register D-01, graded *ground truth*: code at the recorded commit, config and data all agree.
   - The OLMo 2 stage-1 configs (A2/A3) set `metrics_log_interval: 1`. This is unconfirmed until their own training commits are read at staging.
6. **Status and what follows.**
   - Phase 2 override (3) applies: "if A1 lacks it, that is a dated amendment before anything else runs." The column is present but not at per-step cadence. Any change to D.1, D.2 or §K for this is a dated public amendment and is decided by JAE before any further A1 file is staged or read.
   - No §K threshold, window, spike definition or FA grid has been applied to A1 data.
   - The file was moved into the project-local store at 2026-10-30 19:38 CT and re-hashed there: `C:\Users\jaek9\Documents\LaggingTruth\data-stores\adam-lag-instability\A1\run-025_u3obk6mj_history-v2_0000.parquet`, 1,527,446 bytes, MD5 0848b70fa58cad98edf64b7744871394, SHA-256 bd1a2f425bd018d56114524195468fe6c1fb7e7a90f76f384997f93a563559ee (the store copy's hashes equal the attached copy's). Its SOURCES.md entry waits for the route decision (D-02).
7. **Cadence confirmation and A2 comparison (2026-10-30 19:45 CT, JAE's instruction; step index and null mask only).**
   - `scripts/cadence_check.py` was run on the stored A1 file and on one A2 file. Outputs: scripts/outputs/cadence_A1_run025.json and cadence_A2_run08.json.
   - **A1 run-025:**
     - The whole file is not contiguous (383 rows over steps 0–543,360, in 23 blocks).
     - Its largest block, steps 543,000–543,360, is contiguous (361 rows).
     - The loss is present on every row of that block.
     - The gradient norm is present on 37 of those rows, spaced exactly 10 steps apart, and only where step mod 10 = 0.
     - The config files agree: `OLMo-7B-0424.yaml` sets `metrics_log_interval: 10`; `OLMo2-7B-stage1.yaml` and `OLMo2-13B-stage1.yaml` set 1.
     - D-01 is therefore native cadence.
   - **A2 run-08:**
     - Source: OLMo 2 7B stage-1, run `9p3ai3he`, artifact `run-9p3ai3he-history:v0`, file `0000.parquet`, 21,921,161 bytes.
     - Manifest MD5 34aa317bb993dc3b49ca5363ac75900e matches the local MD5. SHA-256 19445a50594a154b74ed8bf65a1c124e6198e796845f6ae554a99ec08aaa2545.
     - Stored at `A2\run-08_9p3ai3he_history-v0_0000.parquet`.
     - The run's W&B config has `metrics_log_interval: 1`.
     - 736 rows: step 0, then steps 2,151–2,885, which are contiguous (735 rows). Loss and gradient norm are present on every row of that block. So A2 logs the gradient norm every step.
     - The file's 736 rows equal the run's server history count of 736. So route 1 is complete for this A2 run.
   - **The A2 run list** (stage-1 runs 01–11) was read from W&B run metadata, not by opening the report. It is recorded here for completeness: syfuxa45, h42rnl7m, acmz6z47, poh1jr99, 4cgzd4cu, zxl4esoc, x5hb6a3f, 9p3ai3he, y4x2f1ci, awwjyi5w, uwjy7cji. Inclusion is still closed at staging per D.1.
   - **D-02 is not explained by the native cadence.** A1's route-1 file holds 383 of the run's 22,361 history lines; only every 1,000th step survives over steps 522,000–542,999. A2's route-1 file holds all of its run's lines. The gap is specific to A1's copied segments (AI2's `copy_wandb_runs.py`). D-02 stays OPEN pending JAE's route decision.

---

## 3. DECISIONS.md entry 40 (the recorded commit is the copy job's, not training's)

## Entry 40 (2026-11-10) — PRV item 3 (pre-clip): the public runs do not record the training commit

1. **What was read.** On 2026-11-10, W&B GraphQL metadata for the seven runs E2 uses and for run-025, read in JAE's Chrome: `commit`, `createdAt`, `runInfo` and `config`. No history value was read. Saved as `scripts/outputs/prv_item3_metadata.json` (MD5 5637c4e601521bc9e9ac208eaaa328b4).
2. **Finding: the recorded commit is the copy job's, not training's.** Every run's `runInfo.program` is `scripts/copy_wandb_runs.py`, created 2024-04-17/18. Its `commit` is the commit the copy script ran from:
   - `bd7cf5f4` for runs 001–018;
   - `43a155fa` for run-025.
   Both commits are on `origin/epwalsh/wandb-wrangling`. The training commit of the original runs is not recorded on the public copies, and the original projects are not visible to an outside account (entry 2, Addendum B item 8).
   - **Correction:** entry 5 item 5 and SOURCES.md call `43a155faf0c4…` "the training commit recorded on the run". It is the copy job's commit. Entry 5's cadence finding still holds: `metrics_log_interval: 10` is in the copied config, and the logged steps agree with it.
3. **Config (copied from training).** Every used run has AdamW with betas [0.9, 0.95] (D.6 item 6 confirmed per run), `metrics_log_interval` 10, `max_grad_norm` 1 and `max_grad_norm_ratio` null, so clipping is global and fixed.
4. **Code evidence.** In every version of `olmo/optim.py` from d4744d08 (2023-10-12, "Bring back global gradient clipping") through d2afcaaf (2024-04-12), and at bd7cf5f4 and 43a155fa:
   - `total_grad_norm` is computed from the unclipped gradients and stored in the metrics before any clipping call;
   - `_do_global_fixed_clipping` reads that stored value;
   - the wrangling branch has no `optim.py` change of its own.
   Any training commit from that window therefore logs the pre-clip norm.
5. **Item 3 cannot be met as written.** D.6 item 3 asks for a check against the training commit in each run's config, and no such commit is recorded. **Proposed resolution, pending JAE:** item 3 is closed on the code evidence in item 4 together with the copied config. The Methods state that the training commit is unrecorded on the public copies, and that the pre-clip status rests on every `optim.py` version of the training period.

## 4. scripts/outputs/prv_item3_metadata.json

```json
{
 "read_utc": "2026-11-10T14:50Z",
 "source": "W&B (CoreWeave Forge) GraphQL https://api.forge.coreweave.com/graphql, project ai2-llm/OLMo-7B, JAE's signed-in Chrome; fields commit, createdAt, runInfo.program, runInfo.git.commit, config (optimizer, max_grad_norm, max_grad_norm_ratio). Metadata only; no history value read.",
 "runs": {
  "run-001": {"id": "ucv77bvt", "commit": "bd7cf5f4f39749a91e47271b0e64edcd111e19c3", "created": "2024-04-17T23:16:04Z", "program": "/home/petew/OLMo/scripts/copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "max_grad_norm_ratio": null, "optimizer": "adamw"},
  "run-008": {"id": "bnzb4pmk", "commit": "bd7cf5f4f39749a91e47271b0e64edcd111e19c3", "created": "2024-04-18T00:36:17Z", "program": "/home/petew/OLMo/scripts/copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "max_grad_norm_ratio": null, "optimizer": "adamw"},
  "run-010": {"id": "wqjq7xzw", "commit": "bd7cf5f4f39749a91e47271b0e64edcd111e19c3", "created": "2024-04-18T01:08:33Z", "program": "/home/petew/OLMo/scripts/copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "max_grad_norm_ratio": null, "optimizer": "adamw"},
  "run-013": {"id": "7lr31kjd", "commit": "bd7cf5f4f39749a91e47271b0e64edcd111e19c3", "created": "2024-04-18T03:25:20Z", "program": "copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "max_grad_norm_ratio": null, "optimizer": "adamw"},
  "run-016": {"id": "0g0rjkxo", "commit": "bd7cf5f4f39749a91e47271b0e64edcd111e19c3", "created": "2024-04-18T04:51:53Z", "program": "copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "max_grad_norm_ratio": null, "optimizer": "adamw"},
  "run-017": {"id": "d4g44zcc", "commit": "bd7cf5f4f39749a91e47271b0e64edcd111e19c3", "created": "2024-04-18T08:26:45Z", "program": "copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "max_grad_norm_ratio": null, "optimizer": "adamw"},
  "run-018": {"id": "50br7dzw", "commit": "bd7cf5f4f39749a91e47271b0e64edcd111e19c3", "created": "2024-04-18T10:53:10Z", "program": "copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "max_grad_norm_ratio": null, "optimizer": "adamw"},
  "run-025": {"id": "u3obk6mj", "commit": "43a155faf0c41c849fc2e14fe375a6bc57ed89fb", "created": "2024-04-18T15:20:05Z", "program": "copy_wandb_runs.py", "betas": [0.9, 0.95], "metrics_log_interval": 10, "max_grad_norm": 1, "optimizer": "adamw", "note": "not used by E2 (fails D.1)"}
 },
 "code": {
  "repo": "https://github.com/allenai/OLMo (blobless clone 2026-11-10)",
  "commit_branch": "bd7cf5f4 'update for OLMo-1.7-7B' (2024-04-17) and 43a155fa 'add annealing run' (2024-04-18) are on origin/epwalsh/wandb-wrangling; that branch has no olmo/optim.py change of its own relative to origin/main",
  "optim_py_order": "in every version of olmo/optim.py from d4744d08 (2023-10-12, 'Bring back global gradient clipping') through 6c0e4196, c205912b, 0c58beed, d2afcaaf (2024-04-12), bd7cf5f4 and 43a155fa: total_grad_norm is computed from the unclipped gradients and stored in the metrics dict (line ~170-199) before _do_global_fixed_clipping / _do_adaptive_clipping is called (line ~204-206), and the clipping reads that stored value"
 }
}
```

## 5. DESIGN.md Amendment 7.4 (P-RNG streams)

**7.4 P-RNG streams.** Each procedure creates its own generator; no generator is shared across procedures.
- The E2 resamples, the E1 permutation and the E5 shifts each use a fresh `default_rng(20261030)`.
- Each D.5 suite cell × replicate uses `default_rng([20261030, c, r])`, where c is the cell's index in the committed suite cell table and r the replicate index (0-based).
- Results therefore do not depend on the order in which procedures run.

## 6. DESIGN.md 15.9 (RNG)

**15.9 RNG (R9, partly withdrawn).**
- Within a suite replicate, the E2 resamples use a fresh `default_rng(20261030)`, exactly as the E2 run on A1 will, because the suite validates the procedure as it will run. That part of R9 is withdrawn.
- On real data, the E2, E1 and E5 generators are `default_rng(SeedSequence(20261030, spawn_key=(k,)))` with k = 1, 2, 3 respectively.

## 7. DECISIONS.md entry 50 (D-05 found)

## Entry 50 (2026-11-16) — E1 build and pre-run check; RNG discrepancy in 15.9 found (no effect on E2's label)

**E1 code** (written before any E1 quantity is computed):
- `analysis/post/e1.py` (MD5 667b8f16935e5dbe01b26b03d4525bc7);
- gate test `scripts/tests/test_e1.py` (MD5 0a1f1d3845f45a909dfe8fbd860bf80b), ALL PASS:
  - R̄ half-open and inclusive indexing on a hand ACF;
  - the Amendment 4.1 SMA-covariance identity, exact on a finite sample;
  - planted AR(1) at 0.9 per observation → predicted sign + and CONSISTENT;
  - white noise → not CONSISTENT.
- A dry run on the synthetic store completes (INDETERMINATE).

**Construction pins.** These are points the registered text leaves open, fixed here before computation:
1. **ACF.** Pooled over the three kept blocks: one global mean, lag-k products only within blocks, each lag normalised by its own pair count, divided by the pooled lag-0 variance.
2. **Correlation.** Pearson Corr(D_t, y_{t+16}) over every t with D defined (from the 128th observation of a block) and t + 16 in the same block. D = SMA_32 − SMA_128 on y (`ops.divergence`, the E2 operator).
3. **Block permutation.** D is held fixed. Within each block, the target series y_{t+16} is cut into consecutive 128-observation pieces and the pieces are permuted. There are 1,000 permutations. One-sided p = (1 + #{null ≥ ρ}) / 1,001 in the predicted direction (≤ for a negative prediction), and likewise for the opposite direction.
4. **RNG.** `default_rng(SeedSequence(20261030, spawn_key=(2,)))` (15.9, real data, k = 2) is primary. The 7.4 stream `default_rng(20261030)` is reported as a sensitivity.
5. **G14 drift.** For each block, the median absolute change in mean y between consecutive 256-observation segments (2,560 steps). Reported beside ρ.

**Six-pass check (E1).**
- Schema: E1 reads only y through `a1_loader`, the same loader as E2, after the hash check.
- Spec trace: h, (w_f, w_s), half-open R̄, inclusive sensitivity, label partition and permutation are as in D.3, Amendment 1 G-items and Amendment 4.1.
- Hand battery: `test_e1.py`.
- Boundaries: pairs never cross a block. D is undefined for the first 127 observations of each block.
- Assumptions: approximate stationarity (G14; drift reported).
- Adversarial: a permutation that also moved D would destroy the alignment it tests. That is why D is held fixed (pin 3).

**Discrepancy found in DESIGN 15.9 (recorded; it does not change E2's label).**
- 15.9's first bullet says E2's resamples on A1 use `default_rng(20261030)`, "exactly as the E2 run on A1 will". Its second bullet says real-data E2 uses `default_rng(SeedSequence(20261030, spawn_key=(1,)))`.
- `run_e2.py` used `pipeline.run`'s `default_rng(20261030)`, per 7.4 and 15.9's first bullet.
- The E2 label is REFUTE on the point estimate C_min = 0.0 ≤ 0, which no resampling enters. p05 is not computed for REFUTE. Every detector's leads are all 0, so the argmax shares (0.2 each) are the same under any generator.
- The verdict is therefore unaffected. The inconsistency is stated in the null note's Methods.
- E1 and E5 use the 15.9 second-bullet streams (k = 2, 3), with the 7.4 stream reported beside them.

## 8. The E2 resampling and label code (analysis/e2stat.py, lines as committed)

```python
def contrasts(lead_arrays, idx=None):
    """C_b = mean lead(D_div) - mean lead(B_b); returns (C dict, C_min)."""
    sel = (lambda a: a) if idx is None else (lambda a: a[idx])
    md = sel(lead_arrays["D_div"]).mean()
    C = {b: float(md - sel(lead_arrays[b]).mean()) for b in BASELINES}
    return C, min(C.values())


def resample(lead_arrays, n_draws, rng):
    """Joint resamples of events with replacement; C_min within each resample; argmax counts."""
    n = len(lead_arrays["D_div"])
    cmins = np.empty(n_draws)
    argmax = {d: 0 for d in DETECTORS}
    for r in range(n_draws):
        idx = rng.integers(0, n, size=n)
        _, cmins[r] = contrasts(lead_arrays, idx)
        means = {d: lead_arrays[d][idx].mean() for d in DETECTORS}
        top = max(means.values())
        winners = [d for d in DETECTORS if means[d] == top]
        for w in winners:
            argmax[w] += 1.0 / len(winners)
    return cmins, {d: argmax[d] / n_draws for d in DETECTORS}


def label(cmin_point, cmins):
    """D.3 E2 outcome partition (INSUFFICIENT EVENTS is decided before this, by P-KLAD)."""
    if cmin_point <= 0:
        return "REFUTE", None
    p05 = float(np.percentile(cmins, 5))              # numpy default (linear); Amendment 7.5
    return ("SUPPORT" if p05 > 0 else "INCONCLUSIVE"), p05
```

