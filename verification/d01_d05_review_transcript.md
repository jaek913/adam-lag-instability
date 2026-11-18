**D-01**

1. **Restatement.** In A1, `optim/total_grad_norm` is logged every 10 steps, not every step as DESIGN D.1/D.2 and DECISIONS entry 2 assumed.

2. **Cascade.** The listed operator, procedure and outline consequences look complete. Three things are missing:
   - The register row still describes 43a155f as the "training commit". Entry 40 corrected this in entry 5 and SOURCES.md, but not in D-01's own item and method text.
   - The row confirms cadence only for run-025. E2 uses runs 001–018. For those runs, the cadence rests on the copied config (`metrics_log_interval` 10, entry 40). The package contains no null mask for them, so the row should say which runs are data-confirmed and which are config-confirmed.
   - PRV item 3 (entry 40) belongs in the cascade. The same wrong premise, that the recorded commit is the training commit, is what made item 3 unmeetable.

3. **Method and grade.** The cited method fails as written. 43a155fa is the copy job's commit, so its `optim.py` is not the training code. It is at most a contemporaneous sibling, and the gating behaviour was not checked across the training period the way the pre-clip order was. That code evidence is therefore consistent-with, not ground truth.

   The finding still stands on two direct observations:
   - The copied training config sets `metrics_log_interval: 10`.
   - In the staged file's contiguous block, the gradient norm is non-null on exactly the rows where step mod 10 = 0 (37 of 361), while the loss is present on every row. Because the rows are retained and only that column is null, the copy job thinned no rows in this block.

   What the analysis consumes is this data, so the cadence of the data is ground truth for run-025. The grade "ground truth" survives, but the method should read: "direct observation of the staged file's null mask, agreeing with the copied run config; code at the copy-job commit is consistent-with only." For runs 001–018, the grade is consistent-with (config only) unless their null masks were read at staging.

4. **Adjudication.** It is supported in principle. Entry 5 records that no threshold, window or spike definition had touched A1 data before the amendment. Correcting the method changes no reported quantity. I cannot assess the content of Amendment 1 from this package.

5. **Verdict: CONFIRMED**, with the method and grade corrected as in item 3 and the register text fixed.

**D-05**

1. **Restatement.** DESIGN 15.9 names two different generators for E2's resamples on real data. `run_e2.py` used `default_rng(20261030)`, which matches 7.4 and 15.9's first bullet.

2. **Cascade.** For E2 the cascade is complete, and the code confirms it:
   - In `label()`, REFUTE is decided on `cmin_point`, which `contrasts(idx=None)` computes without any RNG. p05 is never reached.
   - With every lead 0, each resample gives C_min = 0 and all detectors tie, so each gets 1/5 = 0.2 under any index draw.

   The discrepancy itself is stated too narrowly. 7.4 also gives E1 and E5 `default_rng(20261030)`, which contradicts 15.9's second bullet (spawn keys 2 and 3). This is a 7.4-vs-15.9 conflict across all three procedures, not just an internal 15.9 conflict about E2. It is partly mitigated:
   - Entry 50 pinned E1's primary stream before any E1 quantity was computed, with the 7.4 stream reported beside it.
   - E5 uses the same scheme.

   Unlike E2, the E1 and E5 p-values do depend on the stream, so the dual reporting is load-bearing and should be named in the row. The suite claim matches 15.9's first bullet. It is not inconsistent with 7.4's per-replicate `[20261030, c, r]` generator, provided that generator governs only data generation.

3. **Method and grade.** Reading both registered bullets verbatim and reading the executed code path are direct evidence of what the text says and what ran. Ground truth is appropriate.

4. **Adjudication.** It is supported. No E2 reported quantity changes, and the inconsistency is disclosed in Methods (entry 50). Status can move from OPEN to ADJUDICATED.

5. **Verdict: CONFIRMED.** The statement should be widened to the 7.4/15.9 conflict for E1 and E5, with their dual-stream reporting recorded as the resolution.