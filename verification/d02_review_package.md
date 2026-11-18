# Package — second focused review of discrepancy D-02

Verbatim excerpts from the project's committed files. Nothing else is provided.

## 1. The dossier row (verification/Discrepancy_Register.md)

| id | opened | item | blast radius | method that answered | grade | adjudication | status |
|---|---|---|---|---|---|---|---|
| D-02 | 2026-10-30 | Route 1 (the wandb-history artifact parquet) is not the full run history: 383 rows vs the server's historyLineCount 22,361; steps 522,000–542,000 every 1,000, then 543,000–543,360. | Every A1 segment staged by route 1; the D.1 completeness check; staging route priority (DECISIONS entry 2 Addendum A). | (1) framing gate: the file is the artifact the route named, confirmed by matching MD5; (3) version reconciliation: artifact vs the run's own history count | ground truth | Route 1 fails D.1 completeness for run-025. The cause is not native cadence (D-01): A2 run-08's route-1 file is complete (736 = 736 server lines). The gap is specific to A1's copied segments. **Update 2026-10-30 (DECISIONS Addendum B item 8):** the shortfall is at the source. Every W&B interface returns 383 rows for run-025, so its historyLineCount of 22,361 has no retrievable rows. Of the 25 segments, 7 are complete server-side (001, 008, 010, 013, 016, 017, 018), 16 are sparse and 2 are empty. Route: per-segment gate, run-001 first; route-3 cutoff 2026-11-13 (Addendum C). | **CLOSED 2026-11-15 (JAE; DECISIONS 44–45), pending second focused review (DECISIONS 58): original unrecoverable from public sources.** The missing run-025 rows exist on no public interface, and route 3 (AI2) did not arrive by the 2026-11-13 cutoff. E2 uses the seven complete segments. The gap is a Methods limitation (Addendum C items 3–5) and bears on coverage, not on the correctness of any value used. |

## 2. DECISIONS.md entry 5 (where D-02 was found)

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

## 3. DECISIONS.md entry 2, Addendum B

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

## 4. DECISIONS.md entry 2, Addendum B item 8

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

## 5. DECISIONS.md entry 2, Addendum C

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

## 6. DECISIONS.md entry 9 (the seven complete segments)

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

## 7. DECISIONS.md entry 44 (route 3 did not arrive)

## Entry 44 (2026-11-15, JAE) — Route 3 did not arrive by the cutoff; E2 uses the gated W&B segments

1. **Route-3 status (JAE, 2026-11-15 23:06 CT).** AI2 (olmo@allenai.org) did not reply to the 2026-10-30 request (entry 2, item 7). Nothing was received by the 2026-11-13 cutoff. JAE's own Gmail also has no message from allenai.org since 2026-10-29.
2. **Data selection (Addendum C item 2; Amendment 17).** E2 uses the gated W&B segments: the seven route-1 files of runs 001, 008, 010, 013, 016, 017 and 018, assembled under Amendment 2 (`scripts/outputs/a1_structural_report.json`).
   - Run-025 fails D.1 and is not used.
   - The uncovered ranges (14,211–52,300 and 504,511–543,360) and the selection threat (Addendum C items 3–5) are stated in the Methods as limitations.
3. **The request is closed (JAE: "let's not wait on them any more").** No follow-up is sent.
   - Any later route-3 copy would be used only for a reported comparison, never for a second E2 run (§K: one real run).
   - **Discrepancy Register D-02, proposed adjudication (pending JAE):** "original unrecoverable from public sources". The missing rows are absent on every public interface (Addendum B item 8), and route 3 did not arrive.
     - E2 uses the seven complete segments.
     - The gap is stated as a Methods limitation (Addendum C items 3–5).
     - D-02 then closes. It bears on coverage, not on the correctness of any value used.

## 8. DECISIONS.md entry 45 (D-02 closed)

## Entry 45 (2026-11-15, JAE) — D-02 closed; licence re-earned on the final code state

1. **D-02 adjudicated (JAE "proceed as recommended", 23:11 CT): original unrecoverable from public sources.** The Discrepancy Register is updated. The gap is stated as a Methods limitation (entry 44).
2. **Licence re-earned (entry 43 reading), on the committed code at 085ebfd; working tree clean after the helper file was moved out of the repository.**
   - `run_e2_gate_tests.py` (scratch `C:\Users\jaek9\Documents\LaggingTruth\scratch\e2-gate-2026-11-16`): **E2 GATE TESTS: ALL PASS**, 11/11, including the PRV hash negative self-test.
   - `grade_suite.py`: **ALL PASS**. The licence check shows `analysis/ops.py`, `analysis/pipeline.py`, `analysis/e2stat.py` and `reference/ref_e2.py` unchanged since aad6cf7. The regenerated `verification/suite_verdict.md` is byte-identical to the committed file (MD5 05816e3a1b05009177fdb26a72e5deeb).
3. **Remaining before the run command:** JAE's D.6 sign-off entry, dated the run day.

## 9. DECISIONS.md entry 49 (X1-X3; bears on what the missing data could change)

## Entry 49 (2026-11-16) — X1–X3 results (exploratory; plan in entry 48, committed at 44fbbe3 before computation)

**Run.** `analysis/post/x_diag.py` at 44fbbe3. PRV hash check: 77 files, 0 failed. Output `analysis/outputs/post/x_diag.json`, MD5 4784018d84b59df423ada566d5e2bf1d (SHA-256 95c02ca7d50a908ccb42bc558006da229b63c361e323e82f338e94cd403f075d).

**X1 — precursor existence. Fixed reading: "precursor present (p < 0.05)", but it is short.**
- Rise statistic: events median +0.084 SD against controls −0.103 SD. One-sided Mann–Whitney p = 8.4 × 10⁻⁵ (57 events, 2,000 controls).
- Share of rises above 2 SD: events 6/57 (10.5 %), controls 3.3 %. Above 1 SD: 14/57.
- **Event-locked mean of y** (ln-units above baseline; offsets in steps before t_e^g):

  | offset | events | control |
  |---|---|---|
  | −1,280 | −0.06 | +0.01 |
  | −320 | −0.04 | +0.01 |
  | −130 | +0.06 | +0.01 |
  | −60 | +0.01 | 0.00 |
  | −30 | +0.04 | −0.01 |
  | −10 | **+0.20** | 0.00 |
  | 0 | **+1.15** | 0.00 |
  | +10 | **+2.11** | −0.01 |

- **Shape.** The gradient norm is flat until the last logged observation before the loss spike (10 steps earlier, +0.20). It jumps with the spike itself (+1.15 at t_e^g; about ×8 in g at +10 steps). The statistically detectable precursor is confined, on average, to the final grid observation, one 10-step logging interval. A few events show earlier rises (6 above 2 SD).

**X2 — D_div's unmatchability. Fixed reading: "unmatchable in every sub-series with n* ≥ 1: a detector property, not data coverage".**

| sub-series | N_out | c_top | n* | unmatchable |
|---|---|---|---|---|
| whole | 36,277 | 10 | 4 | yes |
| block 1 (52,301–160,500) | 7,498 | 5 | 1 | yes |
| block 2 (160,601–504,500) | 28,488 | 4 | 3 | yes |
| block 2, first half | 13,744 | 2 | 1 | yes |
| block 2, second half | 13,873 | 3 | 1 | yes |
| block 0 (1–14,200) | 291 | 1 | 0 | not read (n* = 0) |

- **Projection.** With route 3, A1 would gain about 7,694 grid observations, and n* stays 4 (N_out ≈ 43,971). The whole series' c_top = 10 > 4, so D_div would still be unmatchable.

**X3 — event representativeness (reported, no verdict).**

| block | eligible events | per 10,000 observations | median rise |
|---|---|---|---|
| block 0 | 1 | 7.0 | +0.96 |
| block 1 | 18 | 16.6 | −0.03 |
| block 2 | 38 | 11.0 | +0.10 |

- Block 0 has a single event, so nothing can be said about the missing early range 14,211–52,300 beyond its absence.

**Bearing on JAE's question (summary for the null note; exploratory).**
1. **D_div's failure does not depend on the missing data.** It is unmatchable in every sub-series that can be matched at all, and at the projected full-run n*. Its percentile score reaches its ceiling outside spike windows more often than the false-alarm budget allows.
2. **Why no baseline led either.** The gradient-norm rise arrives, on average, within the last 10-step logging interval before the loss spike. A precursor that short leaves almost no room for a lead at grid 10, and the headline budget (n* = 4) forces thresholds above all but a handful of excursions.
3. **What route 3 could not have changed.** It would have been AI2's full export of the same runs. The gradient norm is logged every 10 steps by the training config (`metrics_log_interval: 10`, entry 40), so route 3 would have filled coverage, not cadence.
4. **What route 3 could have changed.** Whether the early range 14,211–52,300 holds more, or longer-precursor, spikes is unknown. It is stated as the remaining limitation.

