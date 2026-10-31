# DECISIONS — Measurement-Lag Instability in Adaptive Optimizers

Append-only. Never edit or delete a committed entry; correct by a new dated entry that names the one it supersedes.

---

## Entry 1 — 2026-10-30 — Public pre-registration by public repository at `prereg-v1`; origin-stays-private inverted (JAE)

**Decision.** This terminal paper elects a public pre-registration under Standard v1.10.2 ("Terminal papers electing a public pre-registration"). THESIS.md + DESIGN.md + OUTLINE.md are committed and tagged `prereg-v1`; at that commit the GitHub repository https://github.com/jaek913/adam-lag-instability is flipped from private to PUBLIC, and a Zenodo DOI is minted on the `prereg-v1` tag through the GitHub–Zenodo integration and recorded in THESIS.md. No OSF registration is filed.

**Inversion.** The Standard's default that the origin stays private until the coordinated launch is deliberately inverted for this paper: the origin is private only until the `prereg-v1` commit. From then on every change is a public, dated commit.

**Reason.** The audience is machine learning, which checks public commit history and arXiv v1 dates, not OSF registrations. A public, timestamped commit of the frozen thesis, design and outline — made before any hashed data is touched — is the pre-registration that audience can verify. The idea is not protectable and the plan is to publish regardless, so nothing is lost by making the plan public early.

**Conditions.** The design-stage adversarial review (same venue and cap as 5a) runs and completes its fix round BEFORE the public commit. The public commit timestamp precedes the first data pull. The Phase 0 "Public pre-registration" box closes at Phase 1 close with evidence: `prereg-v1` commit hash + public-flip timestamp + Zenodo DOI.

**History.** Decided 2026-09-14 (OSF dropped in favour of public repo at design freeze); Zenodo DOI on the tag accepted 2026-10-30.

---

## Entry 2 — 2026-10-30 — Existence check: does the public OLMo-0424 log carry a per-step gradient-norm metric? (column names only)

**Scope.** Read-only metadata check before any data work: list metric NAMES for the Leg A runs and report whether a per-step gradient-norm metric exists, its exact name, pre- vs post-clip if the name says so, and logging cadence if visible from run metadata. No history rows are downloaded; no metric values are printed or saved. This is not a data pull and touches no hashed input.

**How the runs were found (2026-10-30).**
- OLMo-0424 (A1, primary): Hugging Face model card `allenai/OLMo-7B-0424` (https://huggingface.co/allenai/OLMo-7B-0424), section "W&B Logs": pretraining = https://wandb.ai/ai2-llm/OLMo-7B/groups/OLMo-1.7-7B ; annealing = https://wandb.ai/ai2-llm/OLMo-7B/groups/OLMo-1.7-7B-anneal . The W&B object is a GROUP (entity `ai2-llm`, project `OLMo-7B`, group `OLMo-1.7-7B`), i.e. potentially several runs (restarts), not one run-id. The same card lists gradient clipping "global 1.0" and QKV clipping for this model. OLMo-0424 was formerly named OLMo 1.7-7B.
- OLMo 2 7B / 13B (A2, A3): allenai/OLMo GitHub README, Stage 1 table, "WandB" row: https://wandb.ai/ai2-llm/OLMo-2-1124-7B/reports/OLMo-2-7B-Nov-2024--VmlldzoxMDUzMzE1OA and https://wandb.ai/ai2-llm/OLMo-2-1124-13B/reports/OLMo-2-13B-Nov-2024--VmlldzoxMDUzMjQxNg → projects `ai2-llm/OLMo-2-1124-7B`, `ai2-llm/OLMo-2-1124-13B`. The OLMo 2 paper (arXiv 2501.00656) front matter links the 7B/13B logs via api.wandb.ai/links/ai2-llm/… short links.
- OLMo 2 32B (A4): the OLMo 2 paper links its 32B training logs to **Comet** (comet.com/ai2/olmo-2-0325-32b), not W&B. DESIGN D.1 row A4 ("OLMo 2 32B W&B export") is therefore wrong as drafted → Phase 1 manifest amendment (Comet export, or drop A4 with reason). Not checked by this script.

**Script.** `scripts/check_olmo_columns.py` (read-only; wandb public API `runs()` with group/project filters; reads run metadata, summary KEYS and config; never calls `history()` / `scan_history()`).

**Attempt 1 (2026-10-30 16:25 CT) — FAILED, no information.** Run against the wandb client's configured host `https://api.forge.coreweave.com` (wandb 0.31.0). All four targets returned `WandbApiFailedError: the provided API key cannot access this resource`. The ai2-llm projects are public on `wandb.ai`; the key/host pair did not reach them. The script's verdict line wrongly printed "NOT FOUND" when no run was listed; corrected to print UNDETERMINED (and exit non-zero) in that case before attempt 2. No metric names were obtained; nothing was learned about the data.

**Attempt 2 (2026-10-30 16:28 CT) — FAILED, no information.** Same script (MD5 0d9df4fa8c1bcb70271e4c437bcd1c56) with `--base-url https://api.wandb.ai`; the client prompted for and stored a key for api.wandb.ai (key issued at forge.coreweave.com/wandb/authorize). All four targets again returned `WandbApiFailedError: the provided API key cannot access this resource`; verdict printed UNDETERMINED. Context found 2026-10-30: https://wandb.ai/ai2-llm/OLMo-7B/groups/OLMo-1.7-7B now 302-redirects to https://forge.coreweave.com/wandb/ai2-llm/OLMo-7B/groups/OLMo-1.7-7B (W&B hosted under CoreWeave Forge), so the host is not the cause; open question is whether the ai2-llm projects are still publicly readable.

**Web UI observation (2026-10-30 ~16:30 CT, JAE's signed-in Chrome, overview panel only — no charts, no values viewed).** https://forge.coreweave.com/wandb/ai2-llm/OLMo-7B/groups/OLMo-1.7-7B loads for JAE's account: group OLMo-1.7-7B lists 25 runs (OLMo-1.7-7B-run-001 … run-025); run-025 path ai2-llm/OLMo-7B/u3obk6mj; author epwalsh; job "allenai_OLMo.git_scripts_copy_wandb_runs.py" — i.e., the public runs are copies made by AI2's copy_wandb_runs.py script, not the original live runs (provenance note for SOURCES.md).

**Attempt 3 — access diagnostic (2026-10-30 16:32 CT).** `scripts/diag_wandb_access.py` (MD5 997d3c29f347507633894b173bad35f0), default host https://api.forge.coreweave.com. Key identity OK: username jaek913, entity jaek913-laggingtruth-com (a personal key, not an org/service key). Project object ai2-llm/OLMo-7B: readable. Direct run read ai2-llm/OLMo-7B/u3obk6mj: FAIL (CommError: key cannot access this resource). One-run group listing: FAIL (same). **Finding: the public project is visible to the API, but its runs are not readable by an outside personal key on Forge; the browser UI can show them.** No metric names obtained via API.

**JAE direction (2026-10-30 16:44 CT).** Try the history-artifact route (run-025 artifact `ai2-llm/OLMo-7B/run-u3obk6mj-history:v2`); if artifacts are readable, A1 = all 25 segment history artifacts ordered by step with restart overlaps de-duplicated on step (rule declared in DESIGN as a construction pin); if blocked, A1 is staged by manual UI export (Workspace → chart ⋯ → Export CSV, per run) with URL + export timestamp + SHA-256 per file in SOURCES.md. The segmented structure is a dated DESIGN D.1 amendment to the A1 row before prereg-v1.

**Pre-registration guard (Claude, 2026-10-30, applied to that direction).** `artifact.download()` on a history artifact IS the A1 data pull. Phase 0 box 7 / entry 1 require the public prereg-v1 commit timestamp to precede the first data pull. Attempt 4 therefore reads artifact METADATA and file manifest only (name, type, size, file list) — no download. The column-name check on downloaded tables, and the UI-export alternative, both move to after prereg-v1. Caveat on the UI-export route, to resolve in Phase 1: W&B chart CSV exports are commonly point-sampled rather than every logged step; full per-step resolution must be confirmed (row count vs step range) before that route is adopted.

**Code reading — OLMo trainer (allenai/OLMo @ main 090253dac6688f2532509daa7aa2eb5fae50e956; code, not data).**
- `olmo/optim.py` `clip_grads_and_collect_metrics`: `total_grad_norm` is computed from the per-parameter gradient norms (lines ~192–195) BEFORE `_do_global_fixed_clipping` scales the gradients (line ~234); it is added to the returned metrics unconditionally (line 221; comment line 251: computed at all steps, even when `collect_param_metrics` is False). → **`optim/total_grad_norm` is the PRE-CLIP global norm.**
- `olmo/train.py` lines 862–899: the returned optimizer metrics are written to the step metrics as `optim/{key}` on every step; `optimizer.metrics_log_interval` only gates the per-parameter metrics (`collect_param_metrics`). W&B logging cadence = `wandb.log_interval` (default 1 in `olmo/config.py` line 700; not overridden in the 0424 config). → expected cadence of `optim/total_grad_norm`: **every step**, subject to what the copy script preserved.
- `configs/official-0724/OLMo-7B-0424.yaml`: wandb group OLMo-1.7-7B (original project olmo-medium); AdamW lr 3.0e-4, **betas [0.9, 0.95]**, metrics_log_interval 10, max_grad_norm 1.0, global batch 1024. OLMo 2 7B/13B stage-1 configs: betas [0.9, 0.95], eps 1e-8, metrics_log_interval 1, max_grad_norm 1.0.
- Caveats: (i) verified against current main, not the April-2024 training commit — the training commit is to be read from the run config at PRV; (ii) `scripts/copy_wandb_runs.py` is not on current main, so whether the copies kept every logged step is unverified until the artifact row count is compared with the step range (after prereg-v1).
- **Phase 1 consequence:** every Leg A run uses β₂ = 0.95 (second-moment window W = 1/(1−β₂) = 20 steps), not 0.999. THESIS.md's claim text cites β₂ ≈ 0.999 as typical; DESIGN must state the realised β₂ of each Leg A run, and the window pair (32, 128) is then longer than the optimizer's own second-moment memory — to be addressed in the Phase 1 validity review.

**Attempt 4 — artifact metadata, no download (2026-10-30 16:47 CT).** `scripts/diag_wandb_access.py` (MD5 cb808b4ffc08aaab07702504afa1e307): identity OK (jaek913 / jaek913-laggingtruth-com); project object readable; direct run FAIL; group listing FAIL; artifact metadata `ai2-llm/OLMo-7B/run-u3obk6mj-history:v2` FAIL (CommError: key cannot access this resource). Nothing downloaded.

**Result (2026-10-30).**
1. **API route: BLOCKED.** On CoreWeave Forge (where wandb.ai now redirects) a valid outside personal key can read the ai2-llm project object but not its runs, run listings, or history artifacts. Same for the OLMo 2 7B/13B projects (runs). The public web UI shows the runs.
2. **A1 structure:** group OLMo-1.7-7B = 25 copied segment runs (OLMo-1.7-7B-run-001 … run-025), created by AI2's copy_wandb_runs.py, each with a wandb-history artifact (run-025: u3obk6mj, artifact run-u3obk6mj-history:v2). DESIGN D.1 A1 row needs a dated amendment before prereg-v1 (25 segments; ordering by step; restart-overlap de-duplication rule declared as a construction pin).
3. **Staging route for A1 (JAE direction): manual web-UI export per run, AFTER the public prereg-v1 commit** — URL + export timestamp + SHA-256 per file in SOURCES.md. Open risk carried to Phase 1: UI CSV exports may be point-sampled; per-step completeness must be shown (row count vs step range per segment) at staging, and DESIGN must state what happens if it fails (alternative route, e.g. a full export requested from AI2, or A1 re-classified).
4. **Gradient-norm metric:** name `optim/total_grad_norm`, PRE-CLIP, expected every step — established from AI2's trainer code (see code reading above), NOT yet observed in the copied logs. Presence in the copied A1 history is confirmed at the first post-prereg staging step; if absent, Leg A as designed cannot run and that is recorded before any analysis.
5. **Phase 1 carry-forwards from this entry:** A1 segmented-structure amendment; staging-route resolution check and fallback; A4 = Comet not W&B; realised β₂ = 0.95 in all Leg A runs (W = 20 steps) — THESIS claim text and DESIGN validity review; verify the April-2024 training commit at PRV.
6. No metric value was read, printed, or saved at any point in this entry. scripts/outputs/check_olmo_columns.json is the attempt-2 output (errors only, zero runs listed).

---

## Entry 2 — Addendum A (2026-10-30, JAE) — A1 staging-route priority

Entry 2 (committed at 3c5ff93) is left unchanged; this addendum supersedes its Result item 3 on route priority only.

1. **Primary route:** in-browser download of each segment run's wandb-history artifact files (run page → Artifacts → `run-<id>-history:vN` → Files tab → the parquet file). This is the full logged per-step history table, not a chart rendering, so it avoids chart point-sampling.
2. **Fallback:** per-run chart CSV export (Workspace → chart ⋯ → Export CSV), only if the artifact files cannot be downloaded, and then subject to the per-segment completeness check (row count vs step range).
3. **Last resort:** request a full export from AI2 (olmo@allenai.org).

Every route is a data pull and therefore runs only AFTER the public `prereg-v1` commit (entry 1). Each downloaded file is recorded in SOURCES.md with its source URL, artifact name and version, download timestamp, and SHA-256. The column-name confirmation for `optim/total_grad_norm` is made on the first staged file, before any analysis.

---

## Entry 3 (2026-10-30, JAE) — Design-stage review: a second, scoped fix round

1. **What happened.** The design-stage adversarial review (prompt and package committed at 7194a21) returned F1–F19. All 19 were adjudicated and the amendments, with fix-round message 1, were committed at a685b37. The reviewer's reply to that round (verification/design_review_transcript.md, reply 2) closed F1–F19. It also found three defects introduced by the amendments themselves: N1 (BLOCKER), N2 (MAJOR) and N3 (MINOR), plus one-line residuals on F4, F5 and F15.
2. **Why a second round.** The Standard caps the design-stage review at three passes and ONE fix-or-rebut round. N1 is a BLOCKER that the fix round itself introduced: the duty-cycle false-alarm rate made each detector's chance hit rate depend on its alarm-run length, so the E2 verdict and §K could be decided by score autocorrelation rather than early warning. A defect of that class in the kill rule is load-bearing. Freezing without a check of its fix would put an unreviewed rule on the public record. This is the load-bearing-defect exception, used once.
3. **Scope.** The second message (verification/design_review_fixround2.md) covers only N1, N2 and N3 and the F4, F5 and F15 residuals. F1–F19 are closed and are not reopened. The reviewer is asked only whether each amendment closes its item and whether any amendment introduces a defect.
4. **Decisions (JAE).**
   - N1: fix (a), a hold-time alarm with H = 32. FA is alarm onsets per 10,000 out-of-window steps, matched at an exact onset count n*; the realised duty cycle n*·H/N_out is reported; P-CENS is kept; B4 resets at each onset. D.5 adds a planted null with 1-step and 40-step alarm-run baselines, which must give false-REFUTE and false-SUPPORT rates ≤ 0.05.
   - N2: accepted as proposed.
   - N3: accepted as proposed.
   - F4, F5 and F15 residuals: accepted.
   
   DESIGN.md §D.9's last entry and THESIS Amendment A3(a) carry the amendments.
5. **Cap.** Whatever reply 3 says, there is no third round. A finding still open after reply 3 is either amended without further review, with the reason recorded in verification/design_review.md, or the freeze waits for a JAE decision.

---

## Entry 3 — Addendum A (2026-10-30, JAE) — N4 amended without further review

Entry 3 is left unchanged. Reviewer reply 3 (verification/design_review_transcript.md) closed N1, N2, N3 and the F4, F5 and F15 residuals. It raised one new finding, N4 (MINOR), introduced by the N2 amendment. On a zero-noise oracle series, B1's rolling SD, B3's EMA variance and B4's MAD are exactly 0, so their scores become 0/0 or x/0, and the oracle they are graded against would be set by floating-point handling rather than by the text.

Per entry 3 item 5 there is no third round. N4 is amended without further review, for three reasons:
1. The reviewer supplied a specific fix and judged either of two forms sufficient.
2. The fix touches only the synthetic suite's reference series, not any verdict rule, threshold, window, spike definition or FA grid.
3. The chosen form adds a check that fails loudly if it is wrong.

The amendment: the oracle series is the planted series with the noise amplitude scaled by 10⁻³ (not zero), and D.5 asserts that every detector's score is finite at every scored step of every oracle series. The reviewer's two N1 notes — (i) residual onset clustering and (ii) the meaning of P-CENS under P-HOLD — are added to DESIGN §D.2 as Methods statements, with no rule change. The design-stage review is closed.

---

## Entry 4 (2026-10-30) — Pre-registration freeze record; Phase 2 opened

1. **Freeze.**
   - `prereg-v1` commit `5bd193a56c18893fd3f21ab76ce88ed57ef3de80`, 2026-10-30 18:53:45 −0500. It holds THESIS.md (d31525ec8e6b8de043954a65a77f88ec), DESIGN.md (a9d051ac65fde38d5001a433b5d11506) and OUTLINE.md (2f15cbae97168515fac477e1f61f773f).
   - Annotated tag `prereg-v1`, tag object `09d5b8048d24c833639a99ca357a9c3bed9dae24`, pushed with --follow-tags.
   - §K grading day: **2026-11-20**, written in THESIS's Date station and DESIGN §K in that commit.
2. **Public.** The repo was flipped public in the GitHub web UI. The anonymous GitHub API returned `visibility: public` at 2026-10-30 19:00:03 −05:00. This entry 4 is the inversion of origin-stays-private that entry 1 elected.
3. **Zenodo.**
   - Version DOI 10.5281/zenodo.23825294 (record https://zenodo.org/records/23825294); concept DOI 10.5281/zenodo.23825293.
   - Archive `adam-lag-instability-prereg-v1.zip`, md5 4705043696ec3a562955bb6e97a1b1dd.
   - Zenodo shows the record as published 2026-10-31. That is the UTC date: it archived after 00:00 UTC.
   - The first GitHub release of `prereg-v1` was published before the Zenodo integration was switched on, so Zenodo did not archive it. JAE deleted that release page; the tag and commit were untouched. It was re-published from the same tag, and Zenodo archived the re-publication.
4. **DOI recorded.** Commit `a624c86c1357b9b2189944d1fe192837f2cd2cde` (2026-10-30 19:10:49 −0500) changes one line of THESIS.md, the Registration line. That is the DOI-only follow-up the Pre-registration box allows.
5. **Gates.** Phase 1 gate signed 2026-10-30 19:14 CT; Phase 0 box 7 closed at the same time. Phase 2 opened 2026-10-30 19:22 CT on JAE's instruction.
6. **Task text versus the frozen design.** The Phase 1 and Phase 2 ClickUp task texts still carry pre-review wording:
   - headline FA "1 per 10k steps";
   - §K "median lead … B1" with PASS/KILL only;
   - ramps 25/50/100/200;
   - "Measurement Trap §3.5";
   - E6 and b_g as verdict items.
   
   Each box is judged against the frozen DESIGN.md. Where the two differ, DESIGN governs.
7. **No data has been pulled.** Per Phase 2 override (3), the first data contact is a column-name-only existence check on A1, recorded in the next entry.

---

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

## Entry 2 — Addendum B (2026-10-30, JAE) — A1 staging route after D-02

Entry 2 and Addendum A are unchanged. This addendum governs A1 only; for A2–A6, route 1 stands where it passes the D.1 completeness check.

1. **Route 1 fails for A1.** The wandb-history artifact parquet is incomplete for A1's copied segments: run-025 holds 383 of 22,361 history lines (Discrepancy Register D-02).
2. **New A1 route (route 1b).** Each A1 segment's complete run history is pulled through W&B's own data interface (the GraphQL history/parquet-history service) in JAE's logged-in browser session.
   - The pulled files are saved to the project-local store.
   - Each file is recorded in SOURCES.md with the query, the run id, the download time (UTC), its size and its SHA-256.
3. **Gate before route 1b is used for any analysis**, checked on run-025 first. Both conditions must hold:
   - **(a)** The pulled history reproduces the 383 rows of route 1's `run-u3obk6mj-history:v2/0000.parquet` (MD5 0848b70fa58cad98edf64b7744871394) exactly. Same `_step` values, same columns, identical cells on those rows, compared by script; no value is displayed.
   - **(b)** Its row count equals the run's server `historyLineCount` of 22,361.

   If either condition fails, route 1b is not used and A1 waits for route 3.
4. **Timing.** The gate compares metric cells, so it runs only after DESIGN Amendment 1 is pushed publicly. No A1 metric value is read before then.
5. **Route 2 (chart CSV export) is removed for A1.** It is sampled and cannot pass D.1.
6. **Route 3, a full export requested from AI2, is pursued in parallel.** JAE sends the request on 2026-10-30, citing the pre-registration DOI 10.5281/zenodo.23825294. If both route 1b and route 3 deliver, the two copies are compared on overlapping steps and any difference opens a Discrepancy Register dossier.
7. **Route 3 request sent (2026-10-30, by 19:55 CT, JAE).**
   - From jae@laggingtruth.com to the AI2 OLMo team, olmo@allenai.org.
   - Subject: "Request: full per-step W&B history for OLMo-1.7-7B (OLMo-0424) pretraining runs".
   - It cites the pre-registration DOI 10.5281/zenodo.23825294 and the repository.
   - It describes D-02 (run-025: 383 artifact rows against 22,361 history lines).
   - It asks for the complete history of runs 001–025 with `_step`, `train/CrossEntropyLoss`, `optim/total_grad_norm`, `optim/learning_rate_group0` and `optim/clipping_rate`.
   - Any reply, and any files received, are recorded here and in SOURCES.md.

## Entry 6 (2026-10-30, JAE) — DESIGN Amendment 1 adopted after a scoped independent check; THESIS Amendment A4

1. **Decision (JAE, 2026-10-30, option (c), with four changes).** A1 stays the primary run, with its detectors on the native 10-step gradient-norm grid (D-01, entry 5). JAE's four changes to draft v1:
   - (1) A1 dedup 2,000 steps;
   - (2) wording;
   - (3) E4 pair (4, 16);
   - (4) rewind events made ineligible are reported.

   These produced draft v2 (drafts/DESIGN_Amendment_1_DRAFT.md, MD5 ffd2b3008f80e40d5cf5302ee3860dd8, committed at ced1674).
2. **Scoped independent check, single round.**
   - Prompt: verification/amendment1_review_prompt.md (MD5 832fbc0407af8a4ed4e2476ebdd54920).
   - Package: verification/amendment1_review_package.md (MD5 e152bb703c253fb9dd0f4cf5cbd91506).
   - Run in a fresh claude.ai incognito chat with web search off, 2026-10-30.
   - Reply saved verbatim as verification/amendment1_review_transcript.md (MD5 619a6766b38e2bd9cbfb795f13026d89).
3. **Adjudication** (verification/amendment1_review.md, MD5 9e2eaa6b1e6710504963f543781251cb).
   - Findings: 16 (1 BLOCKER: G3; 7 MAJOR; 8 MINOR). All adopted.
   - G1, G2, G4, G6 and G15 are adopted with a stated adaptation:
     - blanks needing full-A1 metadata go to a pre-metric structural report;
     - the loss side keeps the frozen gap rule;
     - the missing-step probe is made consistent with D.1.
   - Author-found S1: D.1's "full per-step resolution" is restated for A1.
   - No rebuttals. No second round (fixed in Addendum B). REVIEW CLOSED.
4. **Appended:**
   - DESIGN.md Amendment 1 (A1.1–A1.12) below §D.9. The pre-amendment content is byte-identical to `prereg-v1` (MD5 a9d051ac65fde38d5001a433b5d11506), and the file is now d5be7ef59fee2a641a12e6f2870ccf80.
   - THESIS.md Amendment A4 (a)–(d). The prefix is unchanged (83d93409591bac0032c41f05f69eef32), and the file is now 54c55e7ad6080cb4d739d2d463981a72.
5. **Two clarifications apply to every run (A1.11):**
   - P-FA's round(·) is round-half-up;
   - "all events" in the FA exclusion means the events at the rung that resolved on A1.

   No frozen number changes.
6. **Metric-value embargo.** No A1 metric value has been read. The embargo lifts when this entry, Amendment 1 and A4 are pushed to the public repository. The route 1b gate on run-025 (Addendum B item 3) is then the first step that touches A1 metric cells, compared by script with no value displayed. After it comes the A1.12 structural report, before any loss event or detector score.
7. **Discrepancy Register:** D-01's design consequence is adjudicated by this amendment. The dossier stays open for its second focused review (Register header). D-02 is unchanged: OPEN, awaiting route 1b or route 3.

## Entry 2 — Addendum B, item 8 (2026-10-30, ~20:30 CT) — Route 1b gate on run-025: FAILS condition (b) at the source; seven other segments are complete server-side

Run after Amendment 1 was public at f66e67d. All checks were done in JAE's logged-in browser via W&B GraphQL (forge.coreweave.com). Only step indices and non-null counts were computed; no metric value was displayed, saved or downloaded.

1. **Run-025 (u3obk6mj): the server holds 383 rows, not 22,361.** All four interfaces return the same 383 rows; the server's `historyLineCount` of 22,361 is not backed by retrievable rows.
   - `parquetHistory` returns a single URL: the route-1 artifact object `0848b70fa58cad98edf64b7744871394`.
   - The legacy `history` returns 383 rows (steps 0–543,360).
   - `sampledHistory` returns 382 loss rows and 58 gradient-norm rows.
   - The route 1b gate therefore fails condition (b) for run-025 at the source. Route 3 is the only route for run-025's missing steps.
2. **Origin.** The run config gives the original run as `mitchish7`:
   - `remote_save_folder` = s3://ai2-llm/checkpoints/OLMo-medium/mitchish7;
   - run-025 resumed from `.../step521000`.
   
   The projects `ai2-llm/olmo-medium`, `OLMo-medium`, `OLMo-7B-mitchish` and `olmo` are not visible to an outside account.
3. **All 25 segments: server history versus served rows.** A `sampledHistory` call returns at most 10,000 rows. Segments at that cap were re-counted by paging in 8,000-step windows; no window exceeded 8,001 rows, so those counts are exact.
   - **Complete and contiguous (served loss steps = last − first + 1):**

     | Segment | Steps | Server lines | Loss rows |
     |---|---|---|---|
     | run-001 | 1–14,210 | 14,211 | 14,210 |
     | run-008 | 52,301–73,110 | 20,811 | 20,810 |
     | run-010 | 73,101–160,851 | 87,752 | 87,751 |
     | run-013 | 160,601–212,965 | 52,366 | 52,365 |
     | run-016 | 212,001–337,339 | 125,340 | 125,339 |
     | run-017 | 337,001–408,923 | 71,924 | 71,923 |
     | run-018 | 408,924–504,510 | 95,587 | 95,587 |

     The loss rows are complete. The one-line difference against the server lines is unexplained until the pull reads `_step` directly.
   - **Gradient norm on these seven:** present on every grid step in each span, none off-grid (1,421; 2,081; 8,775; 5,236; 12,533; 7,192; 9,559 rows = grid steps in span). This matches D-01 and Amendment 1 A1.1, with no dropped observations.
   - **Sparse (served rows ≪ server lines):** runs 002–007, 009, 011, 012 and 019–025. Typical pattern: every 1,000 steps, then a short every-step block.
   - **Empty:** runs 014 and 015 (1 server line, no served loss row).
4. **Consequence under the frozen rules.** By D.1, a segment failing the completeness check is not used, and gaps between used segments are recorded, with windows restarting after them. From route 1b alone, A1 would be assembled (P-SEG) from runs 001, 008, 010, 013, 016, 017 and 018:
   - steps 1–14,210;
   - a gap 14,211–52,300;
   - 52,301–504,510 contiguous;
   - nothing after 504,510.
   
   Route 3 could fill both missing ranges.
5. **The gate as written (item 3) names run-025 and cannot pass.** Re-specifying it, for example to apply per segment, is a decision for JAE. No data pull has been made.

## Entry 2 — Addendum C (2026-10-30, JAE) — Per-segment route 1b gate; route-3 cutoff; coverage record and selection threat

Supersedes Addendum B item 3 (the run-025 gate), which cannot pass (item 8). Addendum B items 1, 2 and 4–7 stand. This addendum is committed and pushed publicly before the gate runs. No A1 metric value enters any analysis until Amendment 1 (public at f66e67d) and this addendum are both pushed.

1. **Per-segment gate.** Route 1b is accepted for an A1 segment only if both conditions hold:
   - **(a)** its pulled rows reproduce that segment's route-1 artifact rows (`run-<id>-history:vN`, file `0000.parquet`) exactly: same `_step` values, same columns, identical cells on those rows, compared by script, with no value displayed;
   - **(b)** it passes the D.1 completeness check: served steps contiguous, count = last − first + 1, no duplicate steps.
   
   **Order:** run-001 first. Only if run-001 passes are the other six complete segments (008, 010, 013, 016, 017, 018) pulled and gated. **A failing segment is not used** (D.1 as frozen). Each pull and each route-1 artifact needed for (a) is a download stated to JAE first (file name and size) and approved before it is made.
2. **Route-3 cutoff: 2026-11-13.**
   - **Route 3 arrives by 2026-11-13, passes D.1 and matches the gated segments:** E2 uses route 3. Matching means cells identical on every step the gated W&B segments hold, compared by script.
   - **Route 3 arrives by then but does not match:** a Discrepancy Register dossier is opened, and E2 uses the gated W&B segments. *(Author's fill-in for a case JAE's rule left open; JAE to confirm.)*
   - **Route 3 has not arrived by 2026-11-13:** E2 uses the gated W&B segments. A later route-3 copy is used only for a reported comparison, never for a second E2 run (§K: one real run).
   - The §K grading day stays 2026-11-20.
3. **Coverage record (from item 8; step index and non-null counts only).**
   - If all seven complete segments pass, A1 under P-SEG covers steps **1–14,210** and **52,301–504,510**.
   - This leaves **one internal gap, 14,211–52,300**. The run's logged range continues to 543,360, so steps **504,511–543,360** are also not covered.
   - **Segments not used** (fail D.1, or empty): 002, 003, 004, 005, 006, 007, 009, 011, 012, 014, 015, 019, 020, 021, 022, 023, 024, 025.
   - **Method note:** the counts in item 8 were computed in the browser from GraphQL responses that carried the loss and gradient-norm columns in page memory. Step indices and non-null flags were counted; no value was printed, inspected or saved.
4. **Selection threat (stated now, before any loss value is read).** The incomplete segments are mostly short restart segments: 002, 004, 005, 007, 009, 011, 012, 014, 015 and 019–023 each span a few hundred to a few thousand steps. They are concentrated in the uncovered ranges: 14,211–52,300 and the run's last ~39k steps, where seven restarts fall within 504,511–543,360.
   - Short segments after a restart are where crashes, loss spikes and rewinds are most likely. Dropping them may therefore drop disproportionately many spike events, and the hardest ones.
   - **Effects:**
     - A1's eligible-event count falls, so INSUFFICIENT EVENTS is likelier.
     - The events that remain may be unrepresentative of instability in this run.
   - **Reporting:** this is a Methods limitation and an E2 caveat. The structural report (Amendment 1, A1.12) lists the uncovered step ranges beside the restart points. Route 3, if it arrives by the cutoff, removes the threat.
5. **Rewind events that become unscorable.** A rewind event lies in a portion of an earlier segment that a restart superseded (D.1 P-SEG).
   - **In a used segment:** it is scored on that segment's own series, as frozen.
   - **In an unused segment:** it cannot be scored. It also cannot be counted, because the spike rule needs 128 contiguous trailing loss steps (D.2), which a sparse segment does not have.
   - **Reported instead:**
     - (i) every superseded step range that lies in an unused segment, with its total length in steps;
     - (ii) the count of rewind events found in the superseded portions of used segments.
   - **Placement:** both are reported beside the rewind-event count and the A1.4 ineligibility counts, and stated as a lower-bound limitation: the true number of unscorable rewind events is unknown unless route 3 arrives.
   - **When:** (i) comes from the step index in the A1.12 structural report. (ii) comes from the loss series after this addendum is pushed, before any detector score.

## Entry 6 — note (2026-10-30) — transcript hash as committed

`.gitattributes` sets `* text=auto eol=lf`, so the committed blob of verification/amendment1_review_transcript.md at f66e67d is the reviewer reply with its CRLF line endings normalised to LF.
- **Committed blob:** MD5 346dcf90d4dcb15e1e6e867839679d54, 18,072 bytes.
- **Raw attachment:** MD5 619a6766b38e2bd9cbfb795f13026d89, 18,246 bytes, as cited in entry 6.
- The two differ only by the 174 carriage returns. No character of the text differs.

## Entry 2 — Addendum D (2026-10-30, JAE) — Source priority per segment (route 1 first); route-1b storage and stitch

Refines Addendum C item 1 (the per-segment gate); Addendum C items 2–5 stand. Committed and pushed publicly before any A1 segment download.

1. **Route 1 first, per segment.** For each of the seven complete segments, the route-1 history artifact is downloaded and checked against D.1 completeness:
   - rows contiguous from first to last step, no duplicate steps;
   - row count compared with the server's `historyLineCount`, with any one-line difference explained from `_step` (item 8 found one per segment);
   - `optim/total_grad_norm` and `train/CrossEntropyLoss` present by name.
   
   **Outcomes:**
   - **The artifact passes:** route 1 is the source for that segment, and route 1b is a cross-check only, requiring cell identity on every step, compared by script.
   - **The artifact fails:** route 1b is the candidate source, gated by Addendum C item 1 (a) and (b).
2. **Route-1b storage.**
   - Each server window (one GraphQL `sampledHistory` response) is saved raw, as returned, as its own file: `A1_<seg>_<id>_route1b_w<NN>_<minStep>-<maxStep>.json`. Each has its own MD5 and SHA-256, recorded in SOURCES.md with the query text, the window bounds and the download time (UTC).
   - Windows are requested so that no window exceeds 8,000 steps, below the server's 10,000-row sampling cap. Each file is checked to hold fewer rows than the cap.
   - Whether `maxStep` is inclusive is determined from the first two windows and recorded.
3. **Stitch by committed script.** `scripts/a1_route1b_stitch.py` is committed before it is run on any segment. It builds a segment's series from its window files only and asserts:
   - (i) every window is below the sampling cap;
   - (ii) the union of steps is contiguous from first to last;
   - (iii) no step appears in more than one window. If the window bounds overlap, a step appearing twice fails the stitch rather than being silently deduplicated.
   - (iv) where route 1 is available, cells are identical to route 1 on every shared step.
   
   It writes the stitched parquet, a JSON report of the asserts, and the MD5 and SHA-256 of every input and output. No metric value is printed.
4. **Route-1 artifacts (from W&B GraphQL metadata, 2026-10-30; sizes in bytes; MD5 = manifest digest).** The sizes grow with each segment's server line count, at about 1.5 KB per line; run-025's artifact is about 4 KB per row. Completeness is decided only by the downloaded file.

   | seg | id | artifact | file | bytes | MiB | MD5 |
   |---|---|---|---|---|---|---|
   | run-001 | ucv77bvt | run-ucv77bvt-history:v0 | 0000.parquet | 22,056,943 | 21.0 | e3942b58581e1fa10afdf096fdf6cb4a |
   | run-008 | bnzb4pmk | run-bnzb4pmk-history:v0 | 0000.parquet | 31,778,101 | 30.3 | 9dc7505753996ddd07841f49dbd01dca |
   | run-010 | wqjq7xzw | run-wqjq7xzw-history:v1 | 0000.parquet | 135,471,623 | 129.2 | 49ee8e2c7058d604e6cd405f6e97bc54 |
   | run-013 | 7lr31kjd | run-7lr31kjd-history:v0 | 0000.parquet | 79,773,595 | 76.1 | 6efbccaac9a7ab9660e20d7c02a8d642 |
   | run-016 | 0g0rjkxo | run-0g0rjkxo-history:v1 | 0000.parquet | 192,839,290 | 183.9 | a2795e7d079cafab921041a0a7e3d173 |
   | run-017 | d4g44zcc | run-d4g44zcc-history:v1 | 0000.parquet | 109,425,733 | 104.4 | f22cbd63928fd2d6ecc2a9b7d2557ba1 |
   | run-018 | 50br7dzw | run-50br7dzw-history:v1 | 0000.parquet | 147,571,822 | 140.7 | fac3463a023deba976b20c91b1b96006 |

   Total 718,917,107 bytes (685.6 MiB).
5. **Order (Addendum C item 1).** Run-001 first; the other six only after run-001's outcome is recorded. Each download is stated to JAE (file name and size) and approved before it is made.

## Entry 7 (2026-10-30, JAE) — Run-001 route-1 artifact passes D.1; bookkeeping-only row rule

1. **Download (Addendum D item 5; approved by JAE before the download).**
   - File: `run-ucv77bvt-history:v0/0000.parquet`.
   - Retrieved through the signed GCS link that W&B GraphQL returned. It arrived in Downloads under its object name and was moved to the store as `A1\run-001_ucv77bvt_history-v0_0000.parquet`.
   - 22,056,943 bytes; MD5 e3942b58581e1fa10afdf096fdf6cb4a, matching the manifest; SHA-256 f85eebb9ee25a5905af9335124fad59e60252ee6709cdc24150f5fe3609b95c9.
2. **D.1 check** (scripts/a1_d1_check.py; output scripts/outputs/d1_A1_run001.json). Step index and non-null masks only; no metric value was read.
   - **Columns:** 2,129, with the required columns present by name.
   - **Steps:** `_step` is stored as double, and all values are integral.
   - **Rows:** 14,211 rows = the server's `historyLineCount` of 14,211. Steps 0–14,210 are contiguous, with no duplicates.
   - **Loss:** on every step 1–14,210, in one block.
   - **Gradient norm:** on all 1,421 grid steps in that span, none off-grid, none dropped.
   - **Exceptions:** the only row without loss is step 0.
   - **Item 8's one-line difference** between server lines and loss rows is this row.
3. **Step 0's contents** (scripts/a1_rows_without_loss.py; output scripts/outputs/rows_without_loss_A1_run001.json). Its non-null columns are exactly `System/Peak GPU Memory (MB)`, `_runtime`, `_step` and `_timestamp`. There is no `train/`, `optim/` or `eval/` column: it is a log row written before training.
4. **Rule (proposed by the author; approved by JAE 2026-10-30 22:27 CT by rerunning the check as conditioned).**
   - **Bookkeeping-only row.** A history row with no `train/CrossEntropyLoss` whose only non-null columns are `_step`, `_runtime`, `_timestamp` or `System/…` is a non-training log row.
   - **Handling.** Such rows are counted and reported, then removed before the D.1 completeness check. Any other row without loss fails D.1, and so does any hole left by removing bookkeeping rows. In effect, only rows at the edges can be removed.
   - **Strict result.** `D1_pass_strict`, without the rule, is reported beside the result.
   - **Scope.** The rule applies to every A1 segment and every other run checked by this script.
5. **Outcome.**
   - **Run-001 passes D.1 under the rule** (`D1_pass` true; `D1_pass_strict` false; 1 bookkeeping-only row; 0 other rows without loss).
   - **Under Addendum D item 1, route 1 is run-001's source.** Route 1b is its cross-check: two raw windows stitched by scripts/a1_route1b_stitch.py, which is committed before it runs, with cell identity on every shared step.
   - **The other six segments** (Addendum C item 1) follow after this entry is pushed, each download approved first.
6. **Scripts committed with this entry:** a1_d1_check.py (MD5 23c2388881217360335df745a94ac180), a1_rows_without_loss.py (41058084bea0626513ee3f8d9d3e6203) and a1_route1b_stitch.py (574295fd4571adf5e443af5823d39c8c). Each was tested on synthetic files before use. Route-1b requests carry one spec per column, because W&B returns a multi-key spec's rows only where every key is present (item 8).

## Entry 8 (2026-10-30, JAE) — Run-001 route-1b cross-check: every cell identical to route 1

1. **Pull (approved by JAE before the download; Addendum D item 2).** Two raw GraphQL `sampledHistory` responses for run-001 (`ucv77bvt`), one spec per column (loss, gradient norm, learning rate, clipping rate), `samples` 10,000, saved byte for byte as returned:
   - `A1_run-001_ucv77bvt_route1b_w01_0-7999.json`: 1,060,646 bytes, MD5 7e4f807ccb57a4e63612b930f4c750b8, SHA-256 cea975e7d5484444e5a8cbc3efb9e5abf0b2ec2494b9c666836fc80492d153f2. Rows per column: 7,999 / 799 / 7,999 / 799.
   - `A1_run-001_ucv77bvt_route1b_w02_8000-14210.json`: 845,817 bytes, MD5 372125ca69c949841657f2571bd92442, SHA-256 9a4ec687f85cc92635d1847552fc124ae2c169a90eb124800828833d98902340. Rows per column: 6,211 / 622 / 6,211 / 622.
   - **`maxStep` is inclusive** (Addendum D item 2): row counts over [0, 7,999] and [8,000, 14,210] equal the route-1 counts. Every list is below the 10,000-row cap.
2. **Delivery to disk.**
   - **What happened:** the browser saves were delayed by several minutes, and each window arrived three times (one scripted save that appeared to fail, one button save, one frame save). All copies of a window have the same SHA-256, equal to the SHA-256 computed in the page on the exact response text before saving.
   - **Where they went:** one copy of each was moved to the store (`A1\route1b\run-001\`), by checksum match. The duplicates are left in Downloads for JAE to delete; nothing references them.
   - **Rule from now on:** route-1b files are identified by SHA-256 against the in-page hash, never by file name.
3. **Stitch and cross-check** (scripts/outputs/route1b_stitch_A1_run001.json): `stitch_pass` true, with all six asserts true.
   - The windows are below the cap, inside their bounds, and do not overlap, with no duplicate steps.
   - Loss is contiguous over steps 1–14,210.
   - **Cells are identical to route 1 on every step:** loss 14,210, learning rate 14,210, gradient norm 1,421, clipping rate 1,421. No step appears in only one copy, and no cell is mismatched (31,262 cells).
   - **Stitched parquet:** `A1\route1b\run-001\run-001_ucv77bvt_route1b_stitched.parquet`, 14,210 rows, MD5 95c936862dfcfd2b2fd413762a810c6d, SHA-256 c3aa08e196c35c2b8f9c80413d980428e8d46497855da072ece2c20c5fb7a688.
4. **Script-version disclosure.** Addendum D requires the stitch script to be committed before it runs.
   - **The committed version (MD5 574295fd4571adf5e443af5823d39c8c, at 300c534)** first ran on an empty folder, because the downloads had not landed. It reported vacuous asserts and `stitch_pass` false, and the report was discarded and overwritten.
   - **The real stitch** ran on a hardened version (MD5 fb3d0289b42f3015a262234fb4e3c7ae), which adds two input guards: stop if no window file matches, and stop if a matching file is not named as a window. The assert logic is unchanged.
   - **Equivalence:** the committed version, run on the same inputs (scripts/outputs/route1b_stitch_A1_run001_committed300c534.json), gives identical asserts, counts, pass flag, window hashes, per-column comparison and stitched-parquet hashes. The hardened version is committed with this entry.
5. **Outcome.** Run-001 is accepted for A1. Route 1 (`run-001_ucv77bvt_history-v0_0000.parquet`) is the source, and route 1b confirms it cell for cell. Next under Addendum C item 1: the other six complete segments (008, 010, 013, 016, 017, 018), each download approved first.

## Entry 9 (2026-10-31, JAE) — All seven complete A1 segments pass: route 1 is the source, route 1b identical cell for cell

1. **Approval (JAE, 2026-10-30 23:30 CT).** JAE approved the route-1 files and route-1b windows of runs 008, 010, 013, 016, 017 and 018 in one batch, on condition that run-001 had passed the MD5 check, D.1 and the cross-check (entries 7–8; met).
   - **Order, per segment:** route-1 download → manifest MD5 → SHA-256 → store → D.1 → route-1b windows → stitch cross-check.
   - **Hard stop** on any MD5 mismatch, D.1 failure or cell mismatch. Counts and flags only.
2. **Processing.** `scripts/a1_process_segment.py` (MD5 0d81d58d96e806d0dc959a372cb73829), tested on synthetic segments: one passing, and one each with a wrong MD5, a tampered cell and a missing window.
   - It reads one manifest per segment (`scripts/manifests/a1_<seg>.json`): the route-1 manifest MD5 and size, the server line count, and each window's size and in-page SHA-256.
   - It identifies downloaded files by content hash only, and calls the committed `a1_d1_check.py` and `a1_route1b_stitch.py` unchanged.
   - **Window plan:** windows of at most 8,000 steps, from loss_first − 1 to loss_last + 100.
3. **Results.** Every segment returned `SEGMENT_PASS` true. Outputs: `scripts/outputs/process_A1_<seg>.json`, `d1_A1_<seg>.json` and `route1b_stitch_A1_<seg>.json`.

   | seg | id | loss steps | rows = server lines | bookkeeping row | gn grid steps | windows | cells compared, all identical |
   |---|---|---|---|---|---|---|---|
   | run-001 | ucv77bvt | 1–14,210 | 14,211 = 14,211 | step 0 | 1,421 | 2 | 31,262 |
   | run-008 | bnzb4pmk | 52,301–73,110 | 20,811 = 20,811 | step 0 | 2,081 | 3 | 45,782 |
   | run-010 | wqjq7xzw | 73,101–160,851 | 87,752 = 87,752 | step 0 | 8,775 | 11 | 193,052 |
   | run-013 | 7lr31kjd | 160,601–212,965 | 52,366 = 52,366 | step 0 | 5,236 | 7 | 115,202 |
   | run-016 | 0g0rjkxo | 212,001–337,339 | 125,340 = 125,340 | step 0 | 12,533 | 16 | 275,744 |
   | run-017 | d4g44zcc | 337,001–408,923 | 71,924 = 71,924 | step 0 | 7,192 | 10 | 158,230 |
   | run-018 | 50br7dzw | 408,924–504,510 | 95,587 = 95,587 | none (strict pass) | 9,559 | 12 | 210,292 |

   **Totals:** 1,029,564 cells compared, 0 mismatches, 0 one-sided steps.
   - **In every segment:** every route-1 MD5 matched its manifest; the gradient norm was present on every grid step and never off-grid; and no row without loss existed other than a bookkeeping-only edge row.
   - **Run-017** has an empty tail window (`w10_409000-409023`, 61 bytes, 0 rows), the margin past its last step; it is checked like every other window.
4. **Coverage (step index only; formalised in the A1.12 structural report).** Under P-SEG (later segment wins):
   - **Before the first gap:** steps 1–14,210 (run-001).
   - **The gap:** 14,211–52,300 (Addendum C item 3).
   - **After the gap:** 52,301–504,510 contiguous.
   - **Overlaps where a later segment supersedes an earlier one's tail (rewind portions, both segments used):**
     - 008/010: 73,101–73,110 (10 steps);
     - 010/013: 160,601–160,851 (251);
     - 013/016: 212,001–212,965 (965);
     - 016/017: 337,001–337,339 (339);
     - 017/018: none (contiguous at 408,923 | 408,924).
   - **Scorability:** these superseded tails lie in used segments, so events in them are scorable on their own series (Addendum C item 5).
   - **Not covered:** 504,511–543,360 (segments 019–025, sparse).
5. **Records.** SOURCES.md rows for the six route-1 files, all 59 route-1b windows (fetch and landing UTC, MD5, SHA-256) and the seven stitched files (derived; not sources).
6. **Next (JAE's sequence):** the Amendment 1, A1.12 structural report, from the step index and null masks of the seven route-1 files, before any loss event is enumerated or any detector score is computed. Route 3 (AI2) remains open until the 2026-11-13 cutoff (Addendum C item 2).

## Entry 10 (2026-10-31, JAE) — P-SEG clarified for A1 (DESIGN Amendment 2): ties to the later run; any superseding segment removes steps from the kept series

1. **Evidence (W&B GraphQL run metadata only: `createdAt`, `historyLineCount`, config `load_path`; no metric value).**
   - Each A1 segment's `load_path` names the checkpoint it resumed from.
   - For all six used segments that restarted, resume step + 1 equals the first loss step measured in entries 7–9: 52,300→52,301; 73,100→73,101; 160,600→160,601; 212,000→212,001; 337,000→337,001; 408,923→408,924. Run-001 has no `load_path`; it starts at step 1.
   - **Resume steps:**

     | run | resume step | run | resume step |
     |---|---|---|---|
     | 001 | — (start) | 014 | 212,000 |
     | 002 | 14,200 | 015 | 212,000 |
     | 003 | 14,500 | 016 | 212,000 |
     | 004 | 39,350 | 017 | 337,000 |
     | 005 | 41,400 | 018 | 408,923 |
     | 006 | 42,200 | 019 | 504,500 |
     | 007 | 51,450 | 020 | 505,550 |
     | 008 | 52,300 | 021 | 507,000 |
     | 009 | 73,100 | 022 | 508,500 |
     | 010 | 73,100 | 023 | 509,200 |
     | 011 | 160,500 | 024 | 511,350 |
     | 012 | 160,600 | 025 | 521,000 |
     | 013 | 160,600 | | |

   - The copies' `createdAt` runs in the same order as the run numbers.
2. **The gap in D.1 P-SEG.** First-step ordering ties for 009/010, 012/013 and 014/015/016. Unused segments (002, 011, 019) supersede steps of used segments, a case D.1 does not address.
3. **Decision (JAE, 2026-10-31): option 1, faithful.** Literal later-wins among used segments only was rejected.
   - **JAE's rationale:** P-SEG's stated reason — the later segment is the trajectory that continued — applies whether or not the superseding segment is used. Option 2 would splice 010's abandoned 160,501–160,600 onto 013, which restarted from a checkpoint on 011's trajectory, fabricating a continuous series across a run boundary.
   - **Rules:**
     - ties go to the later run;
     - any superseding segment, used or not, removes the superseded steps from the kept series;
     - an unused owner makes a gap;
     - superseded tails of used segments are rewind portions, scored on their own series;
     - superseded portions of unused segments are unscorable.
4. **Rule (b) as written (DESIGN Amendment 2).** Supersession is decided by resume step, not by how far the superseding segment logged.
   - **Reason:** sparse segments' last logged rows understate their reach. 011's last logged row is 160,599, yet 012 and 013 resume from its checkpoint at 160,600.
   - **Check:** this rule, computed from the resume steps and the seven used spans by script, reproduces the kept series and the six rewind portions in Amendment 2 exactly.
5. **Kept A1 series:**
   - 1–14,200 | gap 14,201–52,300 | 52,301–160,500 | gap 160,501–160,600 | 160,601–504,500;
   - the uncovered remainder runs to 543,360.
   
   **Rewind portions** (used segments, scored on their own series):
   - 001: 14,201–14,210 (10 steps);
   - 008: 73,101–73,110 (10);
   - 010: 160,501–160,851 (351);
   - 013: 212,001–212,965 (965);
   - 016: 337,001–337,339 (339);
   - 018: 504,501–504,510 (10).
6. **Costs (stated in Amendment 2).**
   - 20 end steps leave the kept series (14,201–14,210 and 504,501–504,510).
   - The 160,501–160,600 gap restarts the detector windows, and the minimum history (1,000 grid observations = 10,000 steps) applies again. No event is eligible within about 11,280 steps after 160,601 (Amendment 1 A1.4).
7. **Sequence (JAE).** Amendment 2 and this entry are pushed before any loss event is enumerated. Then comes the A1.12 structural report on this assembly, from the step index and null masks only; its script is committed before it runs.

## Entry 11 (2026-10-31) — A1 structural report (Amendment 1 A1.12) on the Amendment 2 assembly

1. **Script and outputs.**
   - The script, `scripts/a1_structural_report.py` (MD5 ea401c188862ea2466d5d63c4ae160e4), was committed and pushed at 9b50801 before it ran on A1.
   - It was synthetic-tested on the real step spans with three planted dropped readings. The test reproduced Amendment 2's kept series, gaps and rewind portions, and caught the planted drops.
   - Outputs: `verification/A1_structural_report.md` (MD5 2941e9e23bd0fe6d77c4722e8d7d9acf) and `scripts/outputs/a1_structural_report.json` (MD5 acded6f4e5112644b6252b15cf9395a9).
   - Inputs: the step index and per-row non-null masks of `train/CrossEntropyLoss` and `optim/total_grad_norm` from the seven route-1 files (entry 9), and `scripts/outputs/a1_segment_metadata.json` (entry 10). No metric value was read. No loss event has been enumerated, and no detector score computed.
2. **Kept series (Amendment 2).**

   | block | steps | grid observations | earliest eligible t_e^g (A1.4) | eligible-anchor span |
   |---|---|---|---|---|
   | 1–14,200 | 14,200 | 1,420 | 11,290 | 2,920 steps |
   | 52,301–160,500 | 108,200 | 10,820 | 63,590 | 96,920 steps |
   | 160,601–504,500 | 343,900 | 34,390 | 171,890 | 332,620 steps |

   - **N = 46,630 grid observations.** Dropped grid observations: 0. Kept steps without a loss value: 0.
   - All three blocks are longer than 11,280 steps.
3. **Gaps.** All three contain grid steps, so all are detector-series gaps.
   - **14,201–52,300 (38,100 steps).** Owners: unused runs 002–007, with restarts at 14,200, 14,500, 39,350, 41,400, 42,200 and 51,450.
   - **160,501–160,600 (100 steps).** Owner: unused run 011.
   - **504,501–543,360 (38,860 steps).** Owners: unused runs 019–025, with restarts at 504,500, 505,550, 507,000, 508,500, 509,200, 511,350 and 521,000.
4. **False-alarm budget.** n* upper bounds before any scan-window exclusion (round-half-up of FA × N / 10,000) are **2, 5, 9 and 23** at FA 0.5, 1, 2 and 5.
   - These are tighter than Amendment 1's metadata bound (≤ 3, 5, 11, 27 from N ≤ 54,337), because the gaps remove grid observations.
   - The n* = 0 guard (A1.2) cannot fire at the headline FA: its upper bound is 5. The realised n* is set by N_out after events are enumerated.
   - FA 0.5 (upper bound 2) is at the "not matchable" edge (n* < 2) and may fall below it once scan windows are excluded.
5. **Rewind portions of used segments** (scored on their own series):
   - 001: 14,201–14,210 (1 grid step);
   - 008: 73,101–73,110 (1);
   - 010: 160,501–160,851 (35);
   - 013: 212,001–212,965 (96);
   - 016: 337,001–337,339 (33);
   - 018: 504,501–504,510 (1).
6. **Unscorable superseded portions of unused segments** (Addendum C item 5(i)): 14 ranges, 1,043 steps in total. These are lower bounds: unused segments' logged ends are taken from their served sparse rows, and the true ends may be later.
7. **Provenance note.** The served last steps of the unused segments come from the 2026-10-30 browser query that produced item 8. Item 8 summarised them as "sparse"; the report script now records each value explicitly, as `UNUSED_SERVED_LAST`.
8. **Next.** Enumerate A1 loss events (P-KLAD k ladder, A1 dedup 2,000 steps, NaN rule) on the kept series and on each rewind portion's own series. Then compute eligibility and the counts that A1.4 and Addendum C require, before any detector score. This requires a committed, synthetic-tested event script, run after this entry is pushed.

## Entry 12 (2026-10-31, JAE) — Spike-rule construction details fixed before any loss value is read (DESIGN Amendment 3)

1. **Gap in the frozen text.** D.2's spike rule leaves five details open, any of which could change which steps are spikes:
   - the σ convention;
   - when a trailing window is full enough to test;
   - whether the dedup distance is inclusive;
   - whether chains cross gaps;
   - how a rewind portion's own series is formed.
2. **Proposal (author) and decision (JAE, 2026-10-31).**
   - **(1)** σ is the sample SD (ddof = 1). Adopted.
   - **(2)** Proposed: a full 128-step trailing window on the same series, with at least 2 finite values. **Changed by JAE:** at least **64** finite values (half the window), "so σ is never estimated from a handful of points". Steps that the floor blocks are counted and reported.
   - **(3)** The dedup distance is inclusive (Δ ≤ D). Adopted.
   - **(4)** A dedup chain never crosses a gap. Adopted.
   - **(5)** A rewind portion's own series is the kept series up to the segment's resume step, plus the segment's own steps. Events on it are rewind events only if t_e lies in the superseded portion. Adopted.
3. **Suite cases (JAE), added to D.5 by Amendment 3:**
   - (i) a NaN run that drops the finite count below 64;
   - (ii) a chain ending at a gap;
   - (iii) a rewind portion with an event at its first superseded step.
4. **Scope.** Every run (A1–A6, Leg B) and the D.5 suite. Recorded as DESIGN Amendment 3 and pushed before any loss value is read for event enumeration.
5. **Next.** Write `scripts/a1_events.py` and test it on synthetic series covering cases (i)–(iii), plus the k ladder and the eligibility counts. Commit it before it runs on A1. Then enumerate A1 events at k = 4 and k = 3 and resolve the ladder, before any detector score.
