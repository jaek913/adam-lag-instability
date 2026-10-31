# Discrepancy Register

Opened 2026-10-30 at Phase 2 open (no entries). Each discrepancy found in Phase 2 — a stated result that our recomputation disagrees with, a source figure that contradicts another source figure, or a required spec the source does not state — gets a dossier here.

Each dossier runs the Discrepancy-Resolution Methods playbook in its three steps:
1. **Cascade.**
2. **Method recovery,** using the twelve-method ladder in its fixed order.
3. **Adjudication.**

Each dossier records the method that answered, its grade (ground truth / consistent-with / new-construction), and the second focused review (CONFIRMED / WITHDRAWN). A trivially explained gap, such as a typo or obvious rounding, is corrected and noted without a dossier.

| id | opened | item | blast radius | method that answered | grade | adjudication | status |
|---|---|---|---|---|---|---|---|
| D-01 | 2026-10-30 | A1 `optim/total_grad_norm` is logged every 10 steps (`metrics_log_interval: 10`; training commit 43a155f returns no optimizer metrics on other steps). DESIGN D.1/D.2 and DECISIONS entry 2 assumed every step, based on main @ 090253d. | Leg A on A1: every D.2 operator on y (windows 32/128, 1,000-step minimum history, lead in steps, the hold H = 32, threshold matching); E1 lags; E2/§K; E4; E5; D.5 suite cadence; PRV item 4; OUTLINE S2/S8. Not Leg B, which logs its own runs every step. | (3) version reconciliation: code at the run's recorded training commit vs main, confirmed against the run config and the staged file's null mask | ground truth | Original (entry 2) wrong for this run's commit; data and code agree. Design consequence adjudicated: DESIGN Amendment 1 + THESIS A4 (JAE option (c); scoped independent check, verification/amendment1_review.md; DECISIONS entry 6). | ADJUDICATED — second focused review pending |
| D-02 | 2026-10-30 | Route 1 (the wandb-history artifact parquet) is not the full run history: 383 rows vs the server's historyLineCount 22,361; steps 522,000–542,000 every 1,000, then 543,000–543,360. | Every A1 segment staged by route 1; the D.1 completeness check; staging route priority (DECISIONS entry 2 Addendum A). | (1) framing gate: the file is the artifact the route named, confirmed by matching MD5; (3) version reconciliation: artifact vs the run's own history count | ground truth | Route 1 fails D.1 completeness for run-025. The cause is not native cadence (D-01): A2 run-08's route-1 file is complete (736 = 736 server lines). The gap is specific to A1's copied segments. **Update 2026-10-30 (DECISIONS Addendum B item 8):** the shortfall is at the source. Every W&B interface returns 383 rows for run-025, so its historyLineCount of 22,361 has no retrievable rows. Of the 25 segments, 7 are complete server-side (001, 008, 010, 013, 016, 017, 018), 16 are sparse and 2 are empty. Route: per-segment gate, run-001 first; route-3 cutoff 2026-11-13 (Addendum C). | OPEN — awaiting per-segment gate and route 3 |
