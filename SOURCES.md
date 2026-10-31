# SOURCES — Measurement-Lag Instability in Adaptive Optimizers

Per-file record required by DESIGN §D.1 ("Per-file record (SOURCES.md)"). Opened 2026-10-30 at first data staging.

- **Store:** project-local, `C:\Users\jaek9\Documents\LaggingTruth\data-stores\adam-lag-instability`. Paths below are relative to it.
- **Download time:** the store copy's LastWriteTimeUtc, which is when the browser finished writing the file. Moving the file within the same volume keeps it.
- **Replicator tolerance:** exact (static copies).
- **What the hashes are:** MD5 and SHA-256 are of the local file. "Manifest MD5" is the digest W&B lists for the artifact file, read from GraphQL metadata (base64, converted to hex).

## Leg A — A1 (OLMo-0424 7B; W&B `ai2-llm/OLMo-7B`, group `OLMo-1.7-7B`)

| store path | route | source | run (name / id) | artifact : file | bytes | downloaded (UTC) | MD5 (= manifest?) | SHA-256 | status |
|---|---|---|---|---|---|---|---|---|---|
| `A1\run-025_u3obk6mj_history-v2_0000.parquet` | 1 | https://wandb.ai/ai2-llm/OLMo-7B/runs/u3obk6mj | OLMo-1.7-7B-run-025 / u3obk6mj | run-u3obk6mj-history:v2 : 0000.parquet | 1,527,446 | 2026-10-31T00:32:36Z | 0848b70fa58cad98edf64b7744871394 (yes) | bd1a2f425bd018d56114524195468fe6c1fb7e7a90f76f384997f93a563559ee | **Fails D.1.** 383 rows against 22,361 server lines; the server itself holds only 383 rows (D-02; DECISIONS Addendum B item 8). Not used. |
| `A1\run-001_ucv77bvt_history-v0_0000.parquet` | 1 | https://wandb.ai/ai2-llm/OLMo-7B/runs/ucv77bvt | OLMo-1.7-7B-run-001 / ucv77bvt | run-ucv77bvt-history:v0 : 0000.parquet | 22,056,943 | 2026-10-31T01:25:24Z | e3942b58581e1fa10afdf096fdf6cb4a (yes) | f85eebb9ee25a5905af9335124fad59e60252ee6709cdc24150f5fe3609b95c9 | **Passes D.1** under the bookkeeping-only row rule (DECISIONS entry 7): steps 1–14,210, loss every step, gradient norm on every grid step; step 0 is bookkeeping only. Source for run-001; route-1b cross-check pending. |

Retrieval for route 1: the artifact file's `directUrl` (a signed storage.googleapis.com link) was read from W&B GraphQL in JAE's logged-in browser and opened by an anchor click. The file arrives named by its object name, the manifest MD5 in hex, with no extension, and is renamed on the move into the store.

## Leg A — A2 (OLMo 2 7B stage 1; W&B `ai2-llm/OLMo-2-1124-7B`)

| store path | route | source | run (name / id) | artifact : file | bytes | downloaded (UTC) | MD5 (= manifest?) | SHA-256 | status |
|---|---|---|---|---|---|---|---|---|---|
| `A2\run-08_9p3ai3he_history-v0_0000.parquet` | 1 | https://wandb.ai/ai2-llm/OLMo-2-1124-7B/runs/9p3ai3he | stage-1 run-08 / 9p3ai3he | run-9p3ai3he-history:v0 : 0000.parquet | 21,921,161 | 2026-10-31T00:41:49Z | 34aa317bb993dc3b49ca5363ac75900e (yes) | 19445a50594a154b74ed8bf65a1c124e6198e796845f6ae554a99ec08aaa2545 | Cadence check only (DECISIONS entry 5 item 7): rows = server lines (736 = 736), every step. The D.1 check is still to run. |
