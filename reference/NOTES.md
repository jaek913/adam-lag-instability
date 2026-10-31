# Reference implementation of E2: interpretation notes

Source: `/home/claude/refimpl/in/DESIGN.md` only. The first version was written from MD5 e785ceedec02bccf9e9d73fc89fcf4b5 (D.0–D.7, Amendments 1–8). It was updated from MD5 92d33da52ad20b4c25f9ceb12e00d36f, which adds Amendment 9; only Amendment 9's changes were applied (N10, N12, N36–N38). I read no other file, repository or conversation. Where an amendment and the frozen text disagree, the amendment wins. Each note gives the section, the issue, what I chose, and why. Notes marked **[RISK]** are the ones most likely to cause a mismatch with an independent implementation.

## Scope and inputs

**N1. Scope of the function (Amendment 8.1, D.1, Amendments 2 and 3).** `run_reference` starts from blocks that are already assembled and gap-free, plus a given event list. It does **not** do P-SEG assembly, Amendment 2 supersession, the spike rule, dedup, the k ladder, rewind series (Amendment 3(5)) or event eligibility. The caller does those. Each block is treated as its own detector series, and every boundary between blocks is a full reset. That assumes every between-block gap contains a grid step. A1.1 says a gap of 1–9 non-grid steps does **not** reset detector state, so the caller has to merge such segments into one block. A rewind event's series has to be passed in as its own block.

**N2. Dropped reading (D.2 Observable; A1.1 G6; Amendment 5.2).** These count as dropped: `None`; values that `float()` cannot convert; NaN; ±inf; and any value ≤ 0, including 0.0 and −0.0.

**N3. Leading dropped readings (A1.1 G6; Amendment 5.2 "Observation index j").** If the first reading(s) of a block are dropped, the series starts at the first non-dropped reading, and that reading is j = 0. The leading dropped readings are not observations. They have no j, are not in N_out, and get no score. Their steps can still fall inside an event window; nothing there can alarm.

**N4. What carry-forward means (D.2 F15: "carried forward … for every window and EMA"; A1.1).** At a dropped observation, y takes the previous observation's y, and g takes the previous observation's g. B3 reads g, so it sees the carried g. I carry the stored previous values rather than recomputing exp(y), so y = ln g holds exactly at every observation. Dropped observations count toward j (Amendment 5.2) and are ordinary members of every window, EMA and median/MAD history (B1, B4 and D_div included).

**N5. Observation step.** Raw index i of a block is at step first_step + i·grid, as the task interface says. j = i − (index of the first non-dropped reading).

## Minimum history and internal state

**N6. State before the minimum history (Amendment 5.2 "Minimum history"; D.2 F15). [RISK]** The text says a score is defined only at j ≥ 1,000, "whatever its own warm-up". I read that as gating which scores are exposed, not when state starts:
- D_div's SMAs and percentile history, B3's buffer and EMA, and B4's median/MAD history and S⁺ all evolve from j = 0.
- B3 is initialised at j = 24 and updated from j = 25 onward.
- B4's S⁺ accumulates from j = 30. No onset can happen before j = 1,000, so there is no reset before then, and S⁺ at j = 1,000 can already be large. Amendment 9.1 confirms the warm-up runs only while the history holds fewer than 30 values, which is consistent with this note.

The alternative, starting each detector's state or S⁺ at 0 at j = 1,000, is not supported by the text: Amendment 5.2 gives warm-ups of 25 and 30 counted from the series start, which would be meaningless if state began at 1,000.

**N7. Arithmetic for means and SDs (Amendment 5.2). [RISK, numerical]** Every mean and variance (SMA_32, SMA_128, B1 mean and SD, B3 warm-up mean and variance) is computed as `math.fsum(window)/n`, the correctly rounded sum of the explicit window. An implementation that uses running or cumulative sums, or `np.mean`, can differ in the last bits. That matters in two places:
- D_div's tie rule (D(s) ≤ D(j)), because exactly equal D values (for example on constant stretches) may come out unequal;
- equality between a candidate and a recomputed score.

A comparison should treat 1e-12-level D differences as a known source of percentile mismatch.

## Detector scores

**N8. D_div (Amendment 5.2 replaces D.2).**
- SMA_w(j) is the mean of y over j−w+1 … j, including the current observation. D is defined from j = w_s − 1 = 127.
- P_D(j) counts D(s) ≤ D(j) over s from 127 to j, with j itself included and ties counting as ≤.
- The history includes the D values at j < 1,000, which are computed but not exposed (N6). D.2's "all D(s), s ≤ t, since the last gap" agrees with this.

**N9. B1 (Amendment 5.2 replaces D.2's ambiguous mean_50/sd_50).**
- The trailing window is j−50 … j−1, with the current observation excluded. SD is the sample SD (ddof = 1).
- "sd = 0" is tested exactly: the score is undefined when all 50 window values are bit-identical, which is when the mathematical SD is 0. I do not use a computed floating SD == 0 test, because the computed SD of identical floats can be a tiny non-zero number. An implementation that tests `np.std(ddof=1) == 0` could disagree on long runs of carried-forward readings. **[RISK]**
- Undefined B1 is a non-alarm (Amendment 5.2), stays in N_out (7.2), is not a candidate threshold, and counts as below θ for the next observation's fresh-crossing test (7.3).
- An undefined B1 inside a scan window does **not** make an event ineligible. A1.4 states eligibility in its equivalent form (≥ 1,000 observations of post-gap history), and 7.2 treats an undefined score as a non-alarm.

**N10. B3 (Amendment 5.2 replaces D.2; weight resolved by Amendment 9.2). RESOLVED.**
- The warm-up buffer is the first 25 observations of the series (j = 0 … 24), carried-forward ones included.
- At the 25th observation: μ = buffer mean and v = population variance. There is no score and no EMA update at that observation.
- From j = 25: s = (g − μ)/(√v + 1e-6), using μ and v from before the update. Then μ ← α·μ + (1 − α)·g, then v ← α·v + (1 − α)·(g − μ_new)².
- **Weight.** The first version used the literal 0.03 printed in Amendment 5.2. **Amendment 9.2 resolves this:** the weight is ZClip's coded expression (1 − α) with α = 0.97, evaluated in float64 (0.030000000000000027), and the code now computes `1.0 - alpha`. The literal-0.03 option was removed, not kept as a switch: Amendment 9.2 says the coded expression governs, and a second constant would only invite misuse. Self-test T4 uses an input (g = 10) where the two readings give different floats (μ = 2.24 versus 2.2399999999999998) and requires exact equality with the (1 − α) form.
- If v = 0 the denominator is 1e-6. That is permitted and needs no special case.
- P-B3 monitor mode: updates use the raw (or carried) g, never a clipped value.

**N11. B2.** s_2(j) = y(j), including carried-forward y.

**N12. B4 after a reset (Amendment 5.2 B4 warm-up bullet, corrected by Amendment 9.1). RESOLVED.**
- **First version:** I took the literal 5.2 text ("or after a reset"), so the 30 observations after each onset reset had no score.
- **Amendment 9.1 strikes "or after a reset".** The warm-up applies only while the history holds fewer than 30 values, which happens only at the series start (= after a gap, i.e. a new block). A P-B4 reset only zeroes S⁺ and keeps the history, and "scoring continues at the next observation with S⁺ = 0".
- **Code:** `FROZEN["b4_warm_after_reset"] = False` is now the frozen default. The superseded reading is kept only as that one-line flag, because the switch is trivial. It is never used by `run_reference`.
- **Meaning of "continues with S⁺ = 0" (new interpretation, N37).** At the observation after an onset at j0, S⁺(j0+1) = max(0, 0 + z(j0+1) − k): S⁺ = 0 is the state going into the update, not the reported score. Self-test T5b checks this (after an onset at j = 3, the score at j = 4 is 11 = 0 + 12 − 1, not 0).

**N13. B4's robust z does not depend on θ (Amendment 5.2; P-B4).** The history is cleared only by a gap (a new block). Every observation is appended to it, including observations during alarm. Under Amendment 9.1 there is no post-reset warm-up; the flag-only superseded reading also appended those observations. So z(j) is the same for every θ, and I compute it once per block. Only S⁺ and the warm-up gating are recomputed per candidate. This is an exact consequence of the text, not an approximation.

**N14. B4 arithmetic details (Amendment 5.2).**
- The median and MAD use `numpy.median`, so for an even count they average the two middle values. MAD = median(|x − m|) over the same ≤ 200 values. Scale constant 1.4826.
- The floor applies to σ = 1.4826·MAD (σ < 1e-12 → 1e-12), as written ("σ = 1.4826·MAD, floored at 1e-12"), not to the MAD.
- The accumulator is evaluated left to right as `max(0, (S + z) − k)`.
- The history before the current observation is the last ≤ 200 values. The current value is appended after scoring, then the history is trimmed to 200.
- Warm-up: at j = 0 … 29 there is no score and the value is appended. The first z is at j = 30, using 30 history values.

**N15. Upward-only B4 on y (P-B4).** There is no downward accumulator, and the `ruptures` PELT step is not used (Amendment 5.2).

## Alarm onset and hold

**N16. n* rounding (A1.11(a); D.2 P-FA).**
- n* = ⌊FA·N_out/10,000 + ½⌋, computed in exact rational arithmetic.
- FA is taken as its decimal string value (`Fraction(str(fa))`), so fa = 0.5 is exactly ½ and a half-tie rounds up (A1.7 probe (vi)).

**N17. Onset rule (D.2 P-HOLD; Amendment 7.3).**
- An onset at j needs four things: j is past the current hold end; s(j) is defined; s(j) ≥ θ; and s(j−1) < θ, or s(j−1) is undefined, or j is the block's first observation.
- s(j−1) is the score at the immediately preceding observation, even if that observation was dropped and carried forward. It is the raw score comparison, whatever the alarm state at j−1.
- A hold covers [j, j+H−1] in observations.
- "At t + H the detector leaves alarm unless a new onset occurs there" is implemented as the ordinary onset test at j = end+1, which needs s(end) < θ.
- The first scored observation (j = 1,000) has s(999) undefined, so it counts as preceded by below, as D.2 and Amendment 7.3 say.
- A hold is cut off at the block end and never carries into another block.

**N18. B4 reset (P-HOLD, P-B4, F4).** S⁺ is set to 0 immediately after an onset at j0. The score recorded at j0 is the pre-reset S⁺ (the value that crossed). Resets happen at every onset, in-window or out-of-window. In-window onsets therefore shape the later out-of-window path, and so c(v).

## Threshold matching

**N19. Candidate set (D.2 P-FA; Amendments 6.1 and 7.1).**
- The candidates are the distinct values of the detector's defined scores at out-of-window observations with j ≥ 1,000.
- B4's candidates come from its reset-free path, which is the path at θ = +∞: no onsets, no resets and no post-reset warm-up.
- Values are deduplicated by float equality, so 0.0 and −0.0 merge.
- In-window scores and undefined scores are not candidates.
- **Not stated in the text:** an empty candidate set (every out-of-window score undefined) is treated as not matchable, with θ = +∞.

**N20. c(v) (D.2; Amendment 6.1).**
- c(v) is the number of onsets at out-of-window observations, summed over all blocks, on the path at v. For B4 the path is recomputed with resets.
- The counting loop stops once the count passes n*. This changes no result, because the scan only needs to know whether c > n*.
- The reported "realised" count is the full count at θ.

**N21. Top scan (Amendment 6.1).**
- Candidates are visited in descending order.
- At the first candidate with c > n*, θ is the candidate immediately above it in the sorted distinct list. "Immediately above" means the next-higher candidate value, not a value in between.
- If the highest candidate already has c > n*, the detector is not matchable. θ is +∞ ("above the detector's maximum score"), it never alarms, and every lead is 0. Its leads still enter the mean and C_b as 0s, as Amendment 6.1 says ("its leads are 0"); the detector is not dropped from C_min. **[RISK]**
- If no candidate exceeds n*, θ is the lowest candidate.
- The rule is applied the same way to D_div, whose candidates are percentiles in (0, 1].
- Output: `matchable` = (θ finite). The same convention is used when `thetas` is given.

**N22. N_out (Amendment 7.2; D.2 F18; A1.4 G16; A1.11(b)).**
- N_out is one common denominator: observations with j ≥ 1,000, summed over all blocks, whose step is outside every event's scan window [t_e^g − scan, t_e^g].
- Every event passed in counts, eligible or not. I assume the caller passes exactly the events at the rung that resolved (A1.11(b)).
- Dropped (carried) observations and observations with an undefined score are in N_out.
- Events whose window falls in a gap or in the minimum-history zone still define windows; they just exclude nothing.

**N23. n* = 0 and G1 not-matchable (A1.2 G1; task spec).**
- If n* = 0, the function returns `{"N_out", "nstar", "label": "UNRUN (n* = 0)"}` for **any** FA value, as the task interface asks.
- The design states the guard for the headline FA only. At a non-headline point, n* = 0 would fall under G1's "n* < 2 → not matchable".
- For a non-headline FA (fa ≠ 1.0) with n* = 1, the per-detector results are computed and reported, `fa_point_not_matchable_G1` is True, and `C` and `C_min` are None, because the point "enters no contrast".

**N24. Coverage (Amendment 6.2).**
- Coverage = (number of out-of-window observations with a defined score ≥ θ) / N_out.
- The scores are those on the path at the matched θ. For B4 that is the reset path, not the reset-free path.
- The denominator is the common N_out (7.2), so undefined-score observations are in it.
- If θ = +∞, coverage is 0.
- `coverage_stop` (> 10 %) is reported for every FA, but the stop rule is defined only at the headline FA.

## Scan window, leads, flags

**N25. Event anchor (A1.4 G3). [RISK if blocks are not aligned]**
- t_e^g = grid·⌊t_e/grid⌋ for any grid. At grid = 1 it is t_e.
- The text's formula assumes grid steps are multiples of 10 (true on A1). If a block's first_step is not a multiple of grid, the anchor and window edges may not be observation steps, and the window can hold fewer than scan/grid + 1 observations. The reference applies the formula literally and walks the window in grid-sized step increments from t_e^g − scan.
- Scan windows are defined in steps (default 1,280 = 128 × 10), and the window is the same for every detector (A1.4).

**N26. Eligibility (D.2; A1.4).**
- Eligibility comes from the input `eligible` flag. Leads are computed only for those events, in input order.
- As a cross-check, the reference returns `eligibility_check`, which tests the A1.4 equivalent form: the observations at t_e^g − scan and at t_e^g both exist in the same block, and the first has j ≥ 1,000. The check is reported only; it does not override the flag, and leads are still computed. A missing step in the window counts as "not in alarm".

**N27. Lead (D.2 P-MISS/P-CENS; A1.4; Amendment 7.6).**
- Lead = t_e^g − (step of the first in-window observation in alarm), in steps.
- Left-censored: in alarm at t_e^g − scan **and** at t_e^g − scan − grid. Then lead = scan, censored = True.
- If the detector is in alarm at t_e^g − scan but not at the observation before it (an onset exactly at the window start), lead = scan and censored = False. Both cases are detected.
- If the observation at t_e^g − scan − grid doesn't exist (block start or gap), it counts as not in alarm. For an eligible event this cannot happen with a scored observation, because j = 999 has no score.
- Alarm state is the held state (P-HOLD), not the raw s ≥ θ. An onset up to H − 1 observations before the window start therefore produces a censored lead (D.2 N1 note ii).

**N28. Flags (Amendment 7.6).**
- detected = lead > 0, which includes censored events.
- concurrent = the first in-window alarm is at t_e^g, so lead 0 with an alarm.
- miss = no in-window alarm. It is returned as the extra key `miss`.
- Concurrent events and misses both enter the mean lead as 0.

**N29. C_b and C_min (D.3 E2; A1.4).**
- C_b = mean lead(D_div) − mean lead(B_b) over the eligible events, using `math.fsum`. C_min = min over B1–B4.
- With no eligible events, C and C_min are None.
- The reference computes no resampling, percentiles or labels; those are outside the requested chain.

## Precedence and conflicts resolved by amendments (for the record)

**N30.**
- D.2's B1 "mean_50(y)/sd_50(y)" is ambiguous about including the current observation → Amendment 5.2 excludes it.
- D.2's B3 formula omitted the 1e-6 term and the update order → Amendment 5.2.
- D.2's P-FA "smallest v with c(v) ≤ n*" → replaced by the Amendment 6.1 top scan.
- D.2's step units → observations on A1 (A1.2), scan window in steps (A1.4).
- D.2 B4 "minimum 30 observations" → the Amendment 5.2 warm-up as corrected by Amendment 9.1: series start or gap only, not after a reset (N12).
- Amendment 5.2's literal B3 weight 0.03 → float64 (1 − α) (Amendment 9.2, N10).
- D.2 "1,000-step minimum history" → j ≥ 1,000 observations, counted from the first non-dropped observation after the gap (A1.1, A1.4, 5.2).
- The D.5 oracle with noise × 1e-3 is withdrawn (8.1). It is not implemented.

## Defaults and interface

**N31. Defaults.** fa = 1.0 (headline), grid = 10, scan = 1,280 steps, hold = 32 observations. These match A1. For per-step runs, call with grid = 1, scan = 128. The minimum history (1,000 observations), windows (32, 128), B1 50, B3 (α = 0.97 with weight 1 − α, 25, 1e-6) and B4 (200, 30, 1.0, 1.4826, 1e-12) are fixed in `FROZEN`. `_run(..., P)` exists only so the self-test can use small hand-sized parameters.

**N32. Extra output keys** (beyond the specification):
- top level: `fa_point_not_matchable_G1`, `eligibility_check`;
- per detector: `shortfall` (n* − realised), `coverage_stop`, `candidates_scanned`, `miss`.

**N33. Overlapping blocks.** These are not supported. Steps are assumed unique across blocks, because blocks are separated by gaps.

**N34. Score comparisons.** These are exact float comparisons (s ≥ θ). Because θ is an actual score value, observations with a score exactly equal to θ alarm.

**N35. Not implemented (outside the requested chain):**
- the E2 resampling, its percentile and the SUPPORT/INCONCLUSIVE/REFUTE label;
- the k ladder and the spike rule;
- E1, E4 and E5;
- the sensitivity sweeps (P-B1 {25, 100}, the P-B3 clipped update, P-B4 two-sided or on g) and the window pairs other than (32, 128).

## Added with Amendment 9

**N36. B3 grouping of the variance term (Amendment 9.2; Amendment 5.2 "v ← 0.97·v + 0.03·(g(j) − μ)²").** Amendment 9.2 fixes the weight as float64 (1 − α) but does not give the grouping of the product. I compute `alpha*v + (1.0 - alpha) * ((g - mu) * (g - mu))`: the square first, then the weight, following the printed form "(1 − α)·(g − μ)²". The first version computed `beta*(g-mu)*(g-mu)` left to right, which can differ in the last bit. `(g − μ)**2` and `(g − μ)*(g − μ)` are identical in IEEE float64. μ is `alpha*mu + (1.0 - alpha)*g`. **[RISK, numerical, about 1e-16 relative]**

**N37. "Scoring continues at the next observation with S⁺ = 0" (Amendment 9.1).** Read as: S⁺ is 0 before the update at j0+1, so s(j0+1) = max(0, z(j0+1) − k). It is not read as forcing s(j0+1) = 0. "A fire zeroes the accumulators" (plural) refers to trainscope's two-sided state. Under P-B4 (upward only) only S⁺ exists, so only S⁺ is zeroed. Because s(j0) ≥ θ, no fresh crossing can occur at j0+1 in any case, and none is counted during the hold. After the hold, an onset still needs s(j−1) < θ (T5b: S⁺ = 25 at j = 5 after the hold ends does not fire, because s(4) = 11 ≥ 10).

**N38. Amendment 9.3 (suite items 15–16) is not implemented.** The decision-flip parameters and the unequal-memory baselines S₁ = y and S₄₀ = max(y(j−39) … y(j)) belong to the D.5 suite cells. They are not part of `run_reference`'s detector set for real data, which Amendment 9 leaves unchanged ("Unchanged. Everything else in Amendments 5–8 and the frozen text"). Nothing in 9.3 requires a change inside `run_reference`. S₁ coincides with B2 if a suite harness wants it.
