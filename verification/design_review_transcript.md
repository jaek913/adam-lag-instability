# Design-stage adversarial review — transcript

Venue: fresh claude.ai incognito chat (no project, no memory, web search off), run by JAE 2026-10-30.
First message: verification/design_review_prompt.md (MD5 29bed842d88c6322bbcbbabfd2bbd0d0) + verification/design_review_package.md (MD5 bb9982df48b756e8fceae622859753b6), committed at 7194a21.
Reviewer reply pasted below verbatim (upload MD5 68ebe4fae6bc99e46dae2421fc7f4b44; CRLF line endings normalized to LF, no other change). The fix-round message and the reviewer's reply to it are appended below when they exist.

## Reviewer reply 1 (verbatim)

# Design-stage adversarial review — findings

## Pass 1 — Can every registered rule fire?

**F1**
- **Pass:** 1 · **Severity:** BLOCKER
- **Location:** DESIGN §D.2 (P-MISS, scan window), §D.3 E2 outcome partition, §D.7 P-MISS
- **Evidence:** "An event with no alarm onset in its window has lead 0"; "C_b = median lead(D_div) − median lead(B_b)"; "REFUTE (= §K KILL): C_min ≤ 0."
- **Why it matters:** At headline FA = 1 per 10,000 steps, a detector fires in roughly 1.3% of random 129-step windows. Unless a detector detects more than half of the eligible events, its median lead is exactly 0 by P-MISS. If D_div and the best baseline both sit at or below 50% detection, every C_b is a tie at 0, C_min = 0, and the rule returns REFUTE — which §K reads as "D_div's lead does not exceed the best baseline's". That is a kill delivered by a tie between two zeros, carrying no information about relative lead. On a spiky 7B run with k = 4 on per-step loss, the event set will include many noise-driven excursions with no precursor; a detection rate above 50% for D_div is not a safe assumption. Ties at 0 are also the likeliest outcome on A2/A3 and on Leg B, so E3 and E8 inherit the defect. The realistic modal outcome of E2 as written is REFUTE-by-artefact.
- **Proposed fix:** "C_b = mean lead(D_div) − mean lead(B_b) over eligible events, misses entered as 0 (so mean lead = detection rate × mean conditional lead). Median lead, detection rate and miss count are reported beside each mean. If every detector's detection rate at headline FA is ≤ 50%, that fact is stated in the result, and the suite's severity statement at that detection rate is quoted." The planted-null cell of D.5 must include a case at detection rates between 30% and 50% to confirm the mean-lead rule's false-support rate there.

**F2**
- **Pass:** 1 · **Severity:** BLOCKER
- **Location:** DESIGN §D.2 "Alarm onset", "Scan window and lead", "False-alarm rate"
- **Evidence:** "the first step of each run of consecutive steps with score ≥ θ. Only onsets count"; "Lead = t_e − (first alarm onset in the scan window)"; "Left-censoring (an alarm already active at t_e − 128) is reported per Adaptation Rate Theorem §5.2 conventions."
- **Why it matters:** An alarm that is already active at t_e − 128 and stays active to t_e has no onset in the window, so by the literal rule the event has lead 0 — a miss — while a detector that re-fires inside the window scores a lead. D_div is built from 32- and 128-step SMAs, so after one spike D stays elevated for ~128 steps; with spike clustering (dedup only merges within 200 steps), the second event of a 200–400-step cluster is scored as a D_div miss but as a B1/B2/B3 hit. The same onset also counts as a false alarm because it "falls outside every scan window". The detector the design favours is penalised exactly where the data is spiky. The number assigned to the censored case is left to a cited convention that is not in the package, so two analysts produce different C_min.
- **Proposed fix:** "An event whose scan window begins with a detector's score already ≥ θ at t_e − 128 is left-censored for that detector: its lead is recorded as 128 and flagged censored; censored events enter C_b at lead 128; censored counts are reported beside miss counts. An alarm run that intersects any scan window is not a false alarm. Sensitivity (E4): censored lead = 0." State this in D.2 and D.7 without reference to an external convention.

**F3**
- **Pass:** 1 · **Severity:** BLOCKER
- **Location:** DESIGN §D.4 E8, §D.2 P-FA, §D.3.1 E8
- **Evidence:** "thresholds matched to FA per run, leads pooled across runs"; "5,000 steps per run"; "realised FA closest to the target from below (≤ target)"; "FA grid: {0.5, 1, 2, 5} per 10,000 steps".
- **Why it matters:** A Leg B run has at most ~4,000 scorable steps (1,000-step minimum history). One out-of-window onset is a realised FA of ≥ 2.5 per 10,000. The only θ with realised FA ≤ 1 per 10,000 is one that produces zero out-of-window onsets, i.e. θ = the run's out-of-window score maximum. Grid points 0.5, 1 and 2 collapse to the same degenerate operating point; only 5/10,000 (two onsets) is realisable. E8's headline comparison is therefore a comparison of in-window excursions against each run's single largest noise excursion, not a matched-FA test; the partition SUPPORT / INCONCLUSIVE / REFUTE is being applied to a quantity the design does not actually compute.
- **Proposed fix:** "E8 matches thresholds by exact onset count per run: the FA grid for Leg B is {1, 2, 4} out-of-window onsets per run (≈ 2.5, 5, 10 per 10,000 steps), headline 1 onset per run; this is a stated regime difference from Leg A and is reported as such." Alternatively pool the 28 runs' out-of-window steps and match once per detector on the pool (then the per-run thresholds become one pooled θ per detector per score scale; only valid if scores are on a run-independent scale, which excludes B2 — say so).

**F4**
- **Pass:** 1 · **Severity:** MAJOR
- **Location:** DESIGN §D.2 "Threshold matching (construction pin P-FA)", §D.7 P-FA
- **Evidence:** "θ is swept over the empirical quantiles of its score; the operating θ for a target FA is the one whose realised FA is closest to the target from below (≤ target); ties go to the larger θ."
- **Why it matters:** The quantile grid is unspecified (percentiles? permilles? all distinct values?). At 1 per 10,000 the relevant tail is above the 99.99th percentile; a percentile grid cannot reach it and "from below" then returns FA = 0 for some detectors (no alarms, all leads 0) and FA ≈ 0.9 for others. Even with a fine grid, "from below" leaves each detector at a different realised FA, and the onset count is not monotone in θ (raising θ can split one excursion into two onsets), so the "ties → larger θ" rule can pick a θ with a higher onset count than a lower θ did. C_min then depends on which detector's step function happens to land nearest the target. The comparison is not at matched FA.
- **Proposed fix:** "For each detector, n* = floor(FA_target × N_out / 10,000), where N_out is the number of scored steps outside every scan window. The candidate set is every distinct score value observed on out-of-window steps. The operating θ is the largest candidate at which the out-of-window onset count equals n*; if no candidate gives exactly n*, the largest candidate giving the largest count < n*, with the shortfall reported. Every detector is therefore compared at the identical integer onset count."

**F5**
- **Pass:** 1 · **Severity:** MAJOR
- **Location:** DESIGN §D.1 "A1 assembly (construction pin P-SEG)", §D.7 P-SEG
- **Evidence:** "Where two segments overlap in step (a restart from a checkpoint), the rows of the later segment are kept for the overlapping steps, because training resumed from the checkpoint and the later segment is the trajectory that continued."
- **Why it matters:** OLMo's restarts were made to escape loss spikes: the run was rewound to a checkpoint before the spike and resumed (with batch skipping). The spike that forced the rewind lives only in the discarded tail of the earlier segment; the kept later trajectory is the one that avoided it. P-SEG therefore deletes, by construction, precisely the severe events the paper is about, lowering the A1 event count toward the INSUFFICIENT EVENTS branch and biasing the remaining events toward mild ones. The "keep-earlier" sensitivity does not repair this; it discards a different set.
- **Proposed fix:** "Spike events are enumerated on every segment, including overlap regions. An event whose time lies in a portion of an earlier segment superseded by a restart is a 'rewind event': it is retained, its scan window and all detector scores are computed on that earlier segment's own series (which shares history with the kept trajectory up to the checkpoint step), and it is reported with a rewind flag and count. The assembled series (later-wins) is used for all other events and for FA. Sensitivity: rewind events excluded."

**F6**
- **Pass:** 1 · **Severity:** MAJOR
- **Location:** DESIGN §D.3 E5, §D.3.1 E5
- **Evidence:** "shuffle y only, in 128-step blocks (1,000 draws); keep the loss events from the real L; re-match D_div's threshold to headline FA on each shuffled series"; "a flag trips if the shuffled median lead ≥ the real median lead".
- **Why it matters:** After a block shuffle the alarm times are independent of the event times. At FA = 1 per 10,000 the probability of an onset inside a given 129-step window is ≈ 1.3%, so under P-MISS the shuffled median lead is 0 in essentially every draw. The flag can trip only if the real median lead is also 0, which is already REFUTE under F1. In every regime where E5 matters (E2 SUPPORT or INCONCLUSIVE) the flag cannot fire. It also does not test what it is labelled to test: whether the lead is "window arithmetic" is a question about how D responds to a ramp, which shuffling y away from the events does not probe.
- **Proposed fix:** "Null for E5: the real D_div onset times are circularly shifted by a uniform random offset in [1,000, N − 1,000] steps (1,000 draws), preserving the alarm density and clustering; the advance-ordering rate and mean lead are recomputed against the real events. The flag trips if the real advance-ordering rate ≤ the 95th percentile of the shifted distribution. The block-shuffle result is reported as a second characterization without a flag." Add a suite cell that confirms the flag trips on planted precursor-free spikes and does not trip at planted L = 100.

**F7**
- **Pass:** 1 · **Severity:** MAJOR
- **Location:** DESIGN §D.3 E3, §D.3.1 E3
- **Evidence:** "on runs with ≥ 3 eligible events, SUPPORT if the sign of C_min matches E2's on a strict majority of those runs; REFUTE if it matches on a strict minority; INCONCLUSIVE on a tie"; "A2/A3 are stabilized runs and may have few events".
- **Why it matters:** Three gaps. (i) A2 and A3 are stabilized, A4 and A5 are conditional, A6 is open; it is plausible that zero or one run reaches 3 eligible events, and "strict majority of zero runs" has no label. (ii) The rule is defined relative to "E2's sign", but if E2 is REFUTE the project has stopped and if INSUFFICIENT EVENTS there is no sign; whether E3 runs at all is unstated. (iii) C_min = 0 on a run has sign 0, which neither matches nor mismatches. With 2 or 4 qualifying runs, ties are the likeliest result, so INCONCLUSIVE dominates by parity rather than by evidence.
- **Proposed fix:** "E3 runs only when §K returns PROCEED. If fewer than 3 runs have ≥ 3 eligible events, E3 returns NOT RUN and all runs are reported descriptively. A run with C_min = 0 counts as not matching. E3 uses the same contrast statistic as E2 (F1)."

**F8**
- **Pass:** 1 · **Severity:** MAJOR
- **Location:** DESIGN §D.4 "Measured per run", "Spike rate", E6; §D.2 spike definition
- **Evidence:** "divergence flag (loss > 2 × initial or NaN)"; "counted over steps 1,000–5,000"; "A run flagged as diverged … contributes its spikes up to the divergence step"; "NaN/inf loss at a step counts as exceeding the threshold"; "Spearman of spike rate against b_g*(exp) across cells".
- **Why it matters:** Initial loss for a 124M GPT-2 is ≈ 10.8 nats; "2 × initial" is ≈ 21.6, a level a run essentially never reaches except via NaN. A run that blows up to loss 8 and oscillates, or collapses back to the unigram floor, is "not diverged" and contributes a spike rate dominated by instability the flag was meant to isolate. Conversely, with clipping disabled, peak LR 2.4e-3 after a 200-step warm-up, and β₂ = 0.9999, divergence to NaN before step 1,000 is plausible in several cells; those cells have spike rate 0/0 and φ̂ undefined, so the committed "Spearman across 24 cells" is not computable as written. After a NaN, SMA_128(L) and σ_128(L) are NaN for 128 steps and every subsequent comparison is False, so spike counting silently stops. Which spikes "up to the divergence step" count is therefore decided by implementation, not by the text.
- **Proposed fix:** "A run is diverged at the first step t at which loss is NaN/inf, or at which loss exceeds the run's minimum loss to date by more than 2.0 nats for 50 consecutive steps. Analysis of a run stops at its divergence step. A cell with fewer than 1,000 completed steps in the window 1,000–5,000 has spike rate and φ̂ 'undefined (diverged)'. E6 reports Spearman twice: over cells with defined rate (N stated), and over all 24 with diverged cells assigned the top rank (ties). E7 does the same within each LR column."

**F9**
- **Pass:** 1 · **Severity:** MAJOR
- **Location:** DESIGN §D.4 "Measured inputs for the characterization", E7; §D.5 "Leg B" bullet
- **Evidence:** "φ̂ = lag-1 autocorrelation of g²(t) over steps 1,000–5,000 (levels, not differences)"; "b_g*(exp)(φ̂, α_Adam) = (1−φ̂)/α_Adam + φ̂"; "the pipeline must recover … a planted ordering against b_g*(exp)".
- **Why it matters:** Two computability problems. (i) With α ranging from 0.05 to 0.0001, the index is (1−φ̂)/α + φ̂; across the six β₂ cells of one LR column it reorders relative to plain β₂ only if 1 − φ̂ differs between cells by an amount comparable to α itself. Otherwise E7's "ordering by the A.4 index" is identical to ordering by β₂ and the Kendall τ measures spike rate against β₂, not against the index. (ii) g² in a training run has a strong downward trend over steps 1,000–5,000 (and the cosine schedule adds more); the lag-1 autocorrelation of levels will be ≈ 0.99+ in every cell, driven by trend, so the small cross-cell differences in φ̂ that could reorder the index are trend-noise. The suite's "planted ordering" is only informative if it plants φ values that reorder cells relative to β₂; the package does not say it does. The expected direction is also unstated: on A.4's reading, a larger index means more robust (fewer spikes), while the mechanism the paper cites (second-moment lag) predicts more spikes at higher β₂. Without a stated direction, "how well the index orders spike rate" can be read as confirmed by either sign.
- **Proposed fix:** "φ̂ is the lag-1 autocorrelation of ln g²(t) after subtracting its trailing 128-step mean, over steps 1,128–5,000; φ̂ on raw levels is reported as a sensitivity. E7 reports, within each LR column, Kendall τ of spike rate against b_g*(exp) and against β₂ alone, and states for each column whether the index reorders any cell relative to β₂. Expected direction stated now: A.4 predicts spike rate decreasing in b_g*(exp). The Leg B suite plants φ values that reorder at least two cells per column relative to β₂."

**F10**
- **Pass:** 1 · **Severity:** MINOR
- **Location:** DESIGN §D.5 "Planted effect", "Dynamic range"; THESIS "The claim" (A)
- **Evidence:** "ramps of length L in {25, 50, 100, 200} … must recover lead(D_div) ≈ L − (w_s − w_f)/2"; THESIS: "lead ≈ (w_s − w_f)/2 at midpoint".
- **Why it matters:** With (32, 128), (w_s − w_f)/2 = 48, so the suite's own target lead at L = 25 is −23 and at L = 50 is 2 — the first cell cannot be recovered and the second is within a step of a miss. The THESIS states the lead bound as a constant 48 while D.5 states it as L − 48; the design depends on a theorem it quotes two different ways, and the suite will be graded against one of them.
- **Proposed fix:** "Planted ramp lengths L ∈ {64, 100, 150, 200}; expected lead(D_div) = max(0, L − 48) under the Adaptation Rate Theorem as applied here; THESIS Claim A text amended to the same expression."

**F11**
- **Pass:** 1 · **Severity:** MINOR
- **Location:** DESIGN §K "Grading day"; THESIS Amendment A2(a)
- **Evidence:** "an unrun E2 … is itself recorded and the day is re-set once, by dated amendment"; THESIS: "judged on the per-resample minimum contrast".
- **Why it matters:** §K's STOP/CLOSE/PROCEED has no outcome if E2 is still unrun on the re-set day. THESIS A2(a) says the kill is "judged on the per-resample minimum contrast", but D.3 E2 defines REFUTE on the point estimate C_min and uses the resample only for SUPPORT vs INCONCLUSIVE; the resample median of a minimum is biased below the point estimate, so the two readings can disagree at the kill boundary.
- **Proposed fix:** "If E2 remains unrun on the re-set grading day, §K returns CLOSE with a null note on data availability." THESIS A2(a): "judged on the point-estimate C_min over all eligible events (REFUTE if ≤ 0), with the per-resample C_min distribution separating SUPPORT from INCONCLUSIVE."

## Pass 2 — Is every experiment in the right report form?

**F12**
- **Pass:** 2 · **Severity:** MAJOR
- **Location:** DESIGN §D.3.1 E1, §D.3 E1
- **Evidence:** "hypothesis test (sign) | SUPPORT / REFUTE / INCONCLUSIVE"; "Severity: near-identity on persistent y; labelled a consistency check."
- **Why it matters:** E1 is explicitly a near-identity consistency check on a cited theorem under an approximate-stationarity caveat, and the THESIS lists no E1 falsifier. Giving it the same SUPPORT label as E2 lets a reader (or the abstract) count "two experiments supported". A check whose SUPPORT is nearly guaranteed should not share a label with a genuine test.
- **Proposed fix:** "E1 report form: CONSISTENT / INCONSISTENT / INDETERMINATE, with the permutation rule unchanged. D.3.1 states: E1 bears on the Divergence Theorem's sign prediction, not on Claim A, and is not counted as support for Claim A."

**F13**
- **Pass:** 2 · **Severity:** MAJOR
- **Location:** DESIGN §D.4 E8, §D.3.1 E8
- **Evidence:** "E2's partition (SUPPORT / INCONCLUSIVE / REFUTE on the per-resample C_min) applied to the pooled eligible events"; "E8 does not feed §K."
- **Why it matters:** E8 carries Claim A's verdict labels on a 124M model with clipping disabled, 5,000-step runs and (per F3) a degenerate FA operating point. The design states no rule for E2 SUPPORT with E8 REFUTE, or the reverse; the paper will have two verdicts on the same claim and the prose decides which one counts. A replication that cannot feed the decision rule and has no combination rule is a verdict in form only.
- **Proposed fix:** Either "E8 is a characterization: E2's statistics are reported on the pooled Leg B events with no label" or "E8's label is a verdict on Claim A in the Leg B regime only; the paper reports E2 and E8 side by side, a disagreement is reported as a regime-dependence finding, and neither overrides the other." Pick one before the freeze.

**F14**
- **Pass:** 2 · **Severity:** MINOR
- **Location:** DESIGN §D.3 E5 (parenthetical), §D.4.2
- **Evidence:** "(the 'lead' would be window arithmetic with no data content)"; "a realised level outside the span means the resolution claim does not transfer and is re-measured before E6 is interpreted".
- **Why it matters:** The E5 parenthetical pre-writes the interpretation of a tripped flag as a negative verdict on Claim A, contradicting "the flag is reported, not a verdict". The D.4.2 clause permits extending the suite after seeing where Leg B lands, with no bound on how.
- **Proposed fix:** Delete the E5 parenthetical; state "a tripped flag is reported as a characterization of the shuffle null and is discussed in Methods". D.4.2: "re-measured by extending the suite's noise grid by one pre-specified step (×2 in noise variance) per extension, at most twice, with the extension recorded as a dated amendment."

## Pass 3 — Is any rule a judgment described as execution?

**F15**
- **Pass:** 3 · **Severity:** MAJOR
- **Location:** DESIGN §D.2 "Observable", "Fast/slow averages", B3, B4; §D.1 "A1 assembly"
- **Evidence:** "Non-positive or non-finite g(t) is dropped and counted"; "no window … is computed across a gap — windows restart after a gap and the minimum-history rule (D.2) applies again"; B3 "initialized from the first 25 steps"; B4 "accumulator reset to 0 after each alarm".
- **Why it matters:** Unbounded discretions that change every lead: (i) whether a dropped g(t) is a "gap" (if so, one bad step resets 1,000 steps of eligibility and every window); (ii) whether "last 32 steps" means 32 steps or 32 retained observations; (iii) whether B3's EMA state and B4's accumulator persist across a segment gap or reset, and whether "first 25 steps" means the series start or each post-gap restart; (iv) whether the spike baseline SMA_128(L) is computed over steps containing a dropped g. Two analysts will produce different C_min.
- **Proposed fix:** "A dropped g(t) is not a gap; for every window and EMA, y(t) at a dropped step is carried forward from y(t−1) and the step is counted (D.6 item 5). At each gap, all window statistics, the B3 EMA (re-initialized from the first 25 post-gap steps), the B4 accumulator and the B4 median/MAD history reset; the 1,000-step minimum history applies from the first post-gap step."

**F16**
- **Pass:** 3 · **Severity:** MAJOR
- **Location:** DESIGN §D.5 (all bullets), header
- **Evidence:** "committed and ALL PASS before any hashed-data run"; "AR(1) persistence in the measured range"; "within tolerance"; "the planted margin over each baseline"; "AR(1) persistence spanning the plausible range"; "an out-of-tolerance value".
- **Why it matters:** The suite must pass before data is touched, but its persistence band is "the measured range" — which cannot be measured before data is touched — and its pass criteria ("within tolerance", "planted margin") have no numbers. The suite is the sole source of E2's severity statement and of the INSUFFICIENT EVENTS power figure; an unbounded tolerance lets the suite be declared passing at whatever precision the pipeline happens to achieve.
- **Proposed fix:** "AR(1) φ_y ∈ {0.5, 0.8, 0.9, 0.95, 0.98}; planted baselines at expected lead(D_div) − {10, 25, 50} steps; pass if |recovered mean lead − expected| ≤ 8 steps and the recovered C_min has the planted sign in ≥ 95% of 200 suite replicates per cell; verify.py tolerance 1e-6 relative for deterministic quantities. If A1's realised φ̂_y falls outside [0.5, 0.98], the band is extended by the next value in {0.3, 0.99} by dated amendment before any INCONCLUSIVE is interpreted."

**F17**
- **Pass:** 3 · **Severity:** MAJOR
- **Location:** DESIGN §D.3 E2 "Uncertainty"; §D.4 P-DATA, E6, E8
- **Evidence:** "events are ≥ 200 steps apart and treated as independent"; "Every Leg B run sees the identical token order"; "leads pooled across runs"; "1,000-draw permutation interval".
- **Why it matters:** Identical token order means a hard batch produces a spike at the same step in many cells. Pooled E8 events are then clustered by step index, not independent, and the 1,000-draw resample interval is too narrow; E6's permutation interval across cells likewise treats cells as exchangeable when they share spike times. The choice of resampling unit is a judgment left to the analyst.
- **Proposed fix:** "E8 resamples runs (cluster bootstrap over the 28 runs, all of a run's eligible events taken together), 1,000 draws. E6/E7 report, beside the permutation interval, the fraction of spike events that occur at the same step index in ≥ 3 cells."

**F18**
- **Pass:** 3 · **Severity:** MINOR
- **Location:** DESIGN §D.2 "Spike definition", "False-alarm rate", "Event eligibility"
- **Evidence:** "Spikes within 200 steps of a prior spike are merged into one event"; "alarm onsets per 10,000 steps falling outside every scan window"; "Ineligible events are counted and reported."
- **Why it matters:** "Within 200 steps of a prior spike" is ambiguous between the event's first step (fixed anchor) and the most recent merged spike (chain); a run of spikes at 0, 150, 300 is one event or two depending on the reading. Whether scan windows of ineligible events are excluded from the FA denominator is unstated; it changes every matched θ.
- **Proposed fix:** "A spike is merged into the current event if it is within 200 steps of the most recently merged spike (chained). Scan windows of all events, eligible or not, are excluded from the FA count and denominator."

**F19**
- **Pass:** 3 · **Severity:** MINOR
- **Location:** DESIGN §D.1 A2, A3, A6; §D.4 "Grid"; §D.3 E2
- **Evidence:** "The stage-1 run group and per-run list are read from the report's run set in the UI at staging"; "Any further public run with per-step pre-clip gradient norm, enumerated at staging"; "seeds fixed and listed"; "1,000 joint resamples".
- **Why it matters:** A6 inclusion is bounded by nothing but the enumerator's search; A2/A3's run list is read from a page that renders the curves (the design admits this). Seeds are "listed" but the package lists none; the resample and permutation RNG seeds are unstated. None of these can steer the §K verdict, but each is a post-freeze choice.
- **Proposed fix:** "A6 candidates are those found by a stated search string on W&B, Comet and Hugging Face recorded in SOURCES.md; inclusion requires the D.1 completeness check and ≥ 50,000 logged steps. Leg B seeds: 1–24 for primary cells, 101–104 for P-REP cells. All resampling and permutations use numpy default_rng(20261030)."

## Findings table

| id | pass | severity | location | summary |
|---|---|---|---|---|
| F1 | 1 | BLOCKER | D.2 P-MISS, D.3 E2 | Median lead with misses = 0 makes a 0–0 tie → REFUTE the modal outcome at FA 1/10k |
| F2 | 1 | BLOCKER | D.2 alarm onset / scan window | Alarm active at window start scores as a miss; penalises smoothed detector in clusters; censoring value outsourced to a citation |
| F3 | 1 | BLOCKER | D.4 E8, D.2 P-FA | FA ≤ 1/10k on 5,000-step runs forces zero-alarm thresholds; FA grid degenerate for Leg B |
| F4 | 1 | MAJOR | D.2 P-FA | Quantile grid unspecified; from-below leaves detectors at unequal realised FA; onset count non-monotone in θ |
| F5 | 1 | MAJOR | D.1 P-SEG | Later-wins deletes the rewind-causing spikes the paper targets |
| F6 | 1 | MAJOR | D.3 E5 | Block-shuffle null gives median lead 0 always; flag can only trip when E2 is already REFUTE |
| F7 | 1 | MAJOR | D.3 E3 | No label for zero qualifying runs, for E2 non-PROCEED, or for C_min = 0 |
| F8 | 1 | MAJOR | D.4 divergence/spike rate | Divergence flag essentially unfirable; early-diverged cells make E6 Spearman incomputable; NaN propagation halts spike counting |
| F9 | 1 | MAJOR | D.4 inputs, E7, D.5 Leg B | Index degenerates to β₂ ordering; φ̂ on trending levels ≈ 1; expected direction unstated |
| F10 | 1 | MINOR | D.5, THESIS Claim A | Suite's expected lead is negative at L = 25; THESIS and D.5 state different lead formulas |
| F11 | 1 | MINOR | §K, THESIS A2(a) | No §K outcome after the single re-set; point-estimate vs per-resample wording conflict |
| F12 | 2 | MAJOR | D.3.1 E1 | Near-identity consistency check carries a SUPPORT label |
| F13 | 2 | MAJOR | D.4 E8, D.3.1 E8 | Replication verdict with no combination rule against E2 |
| F14 | 2 | MINOR | D.3 E5, D.4.2 | Prose pre-interprets a flag as a verdict; unbounded post-hoc suite extension |
| F15 | 3 | MAJOR | D.2 operators, D.1 gaps | Dropped-g handling, step-vs-observation windows, EMA/CUSUM state across gaps undefined |
| F16 | 3 | MAJOR | D.5 | "Measured range", "within tolerance", "planted margin" unbounded and circular with "before any data" |
| F17 | 3 | MAJOR | D.3 E2, D.4 E6/E8 | Identical token order makes Leg B events dependent across cells; resampling unit unspecified |
| F18 | 3 | MINOR | D.2 dedup, FA | Dedup chaining ambiguous; ineligible windows in FA denominator unstated |
| F19 | 3 | MINOR | D.1 A2/A3/A6, D.4 seeds | A6 inclusion unbounded; seeds and RNG unstated |

## Author fix-round message 1

verification/design_review_fixround.md (MD5 859f060b72adb30e9f62df957183c574), sent once to the same session.

## Reviewer reply 2 (verbatim; upload MD5 63e09e69c95b1644519a862586482c1c; CRLF normalized to LF, no other change)

# Fix-round reply — disposition of F1–F19 and defects introduced by the amendments

**F1 — CLOSED.** Mean lead with misses at 0, censored at 128, detection rate and the ≤ 50 % statement reported, suite null at 30–50 % detection. The tie-at-zero kill is gone. (The statistic is now exposed to the chance-hit asymmetry in N1 below, which is a property of the FA redefinition, not of the mean-lead rule.)

**F2 — CLOSED as to censoring; the FA redefinition it was bundled with introduces N1.** Lead 128 flagged, with the two sensitivities, removes the "active alarm = miss" artefact and the external-convention dependency. The rebuttal of "alarm runs touching a window are not false alarms" stands on its own terms: under duty cycle the in-window steps are already out of both numerator and denominator, and the author is right that pure onset counting lets a monotone-drifting score (B2 on rising y) sit in alarm for most of the run at a trivial onset count. But the replacement — duty cycle alone — fails in the opposite direction; see N1.

**F3 — CLOSED mechanically, with a residual that is part of N1/N3.** At 1 % of ~4,000 out-of-window steps, 40 alarm steps are realisable. Two residuals: (i) N_out is not ~4,000 in spiky cells, because every event's 129-step window is removed from the denominator; a cell with 20 events has N_out ≈ 1,400 and n* = 14 — still realisable but the realised N_out per run must be reported; (ii) the chance-hit asymmetry of N1 is at its most severe on 5,000-step runs.

**F4 — CLOSED for B1, B2, B3 and D_div; OPEN for B4.** Alarm-step count is monotone in θ for a score series that does not depend on θ. B4's series does: "accumulator reset to 0 after each alarm", with alarm now defined as S⁺ ≥ θ, means the score path is recomputed for each candidate θ, so monotonicity is not guaranteed and the candidate set is itself θ-dependent. It also makes every B4 alarm run exactly one step long (S⁺ resets to 0 on the alarm step, so the next step cannot be in alarm unless z − k ≥ θ), which bears on N1. Fix: "For B4, the alarm-step count is computed by rerunning the accumulator at each candidate θ; θ is the smallest candidate at which that count ≤ n*; monotonicity is checked and any non-monotone region reported. B4's alarm state is held for H steps after each alarm (see N1 fix)."

**F5 — CLOSED, one wording gap.** Rewind events retained on the earlier segment's own series, entering the k-ladder count, with the excluded-sensitivity. Unstated: whether a rewind event and a kept-trajectory event at nearby step indices (the restart re-encountering the same batch) are two events or one. They are on different series, so by the text they are two; say so in one line in P-SEG: "Dedup applies within a series; a rewind event and an assembled-series event are never merged."

**F6 — CLOSED.** Circular shift of the alarm-state series with a 95th-percentile flag and a suite cell that must trip/not trip. The flag can now fire in the regime that matters.

**F7 — CLOSED; the adaptation is sound.** Replicating the direction C_min > 0 rather than "E2's sign" removes the undefined-sign case, NOT RUN covers < 3 qualifying runs, and running E3 on a REFUTE so the null note carries its replication is better than my proposal.

**F8 — CLOSED.** P-DIV with a running-minimum + 2.0 nat / 50-step rule and NaN, analysis stopping at divergence, undefined cells, Spearman both ways, finite-only spike baselines.

**F9 — CLOSED.** Detrended φ̂ with raw-level sensitivity, τ against β₂ beside τ against the index, the per-column "identical to β₂ ordering" statement, stated direction, planted reorder. With detrended φ̂ most columns will likely report "identical to ordering by β₂"; that is now an honest characterization rather than a hidden one.

**F10 — AMENDMENT INTRODUCES A DEFECT (N2); the rebuttal of max(0, L − 48) stands.** The author's reading that Thm 3.1 bounds the fast average's lead over the slow average, not a detector's lead over a spike, is correct and A3(b) states it properly. But the oracle as written is not computable: see N2.

**F11 — CLOSED.** Unrun-after-re-set → CLOSE; REFUTE on the point estimate; THESIS A3(a) now matches §K.

**F12 — CLOSED.** Relabelled, and both D.3.1 and THESIS A3(c) say E1 is never counted as support for Claim A.

**F13 — CLOSED.** E8 is a characterization with no label and no combination rule needed.

**F14 — CLOSED.** Parenthetical removed; D.4.2 extension bounded to ×2 steps, at most twice, each a dated amendment.

**F15 — CLOSED, one stale sentence.** The gap-reset list and carry-forward rule are complete. D.2's D_div line still reads "among all D(s), s ≤ t, in the assembled series", which the new "Gaps and state" bullet overrides (percentile history resets at a gap). Edit the D_div line to "since the last gap" so the two sentences agree.

**F16 — CLOSED except where it depends on N2.** φ_y grid, replicate count, ±8-step tolerance, ≥ 95 % sign agreement, 1e-6 relative, extension rule are all bounded. The author's point that baselines cannot be planted independently is right; the oracle replaces them — so F16's pass criterion inherits N2.

**F17 — CLOSED.** Cluster bootstrap over runs for E8; co-occurrence fraction for E6/E7.

**F18 — CLOSED.** Chained dedup; all event windows out of the FA count and denominator.

**F19 — CLOSED; residual accepted correctly.** Mechanical inclusion of every stage-1 run makes viewing the report incapable of steering selection.

---

## Defects introduced by the amendments

**N1 — Duty-cycle matching lets chance alarms decide E2**
- **Severity:** BLOCKER
- **Location:** DESIGN §D.2 "Alarm state", "False-alarm rate (duty cycle)", §D.3 E2, §K; THESIS A3(a)
- **Evidence:** "FA = (number of out-of-window scored steps in alarm) / N_out"; "FA grid {0.5 %, 1 %, 2 %, 5 %}; headline FA = 1 %"; "A detector's lead = t_e − (first step in the window at which it is in alarm)".
- **Why it matters:** Duty cycle fixes the fraction of steps in alarm, not the number of alarm episodes. Detectors differ enormously in alarm-run length: B1, B2 and B3 read y or g with 1–50-step memory and produce short runs; B4 as written produces 1-step runs (F4); D_div is a difference of 32- and 128-step SMAs and produces runs of tens of steps. At 1 % duty cycle a detector with ~1-step runs has an onset on ~1 % of steps, so the chance that it is in alarm somewhere in a 129-step scan window is ≈ 1 − 0.99^129 ≈ 73 %, with the first chance alarm uniformly placed in the window — a chance mean lead of roughly 0.73 × 64 ≈ 47 steps on every event, precursor or not. A detector with ~40-step runs at the same duty cycle has an onset on ~0.025 % of steps and a chance hit rate of ~3 %. D_div therefore has to carry a true precursor lead averaging > ~45 steps across all eligible events to produce C_min > 0 against baselines that need no precursor at all. E5's shift null measures this chance lead for D_div only; nothing measures or removes it for the baselines. The verdict is steered by the autocorrelation of each score, not by early warning. This is the same class of artefact as the original onset-only rule, with the sign reversed, and it applies with full force on Leg B (E8) and in the suite — the suite's planted null will show it as a false-REFUTE rate, which the suite does not currently grade.
- **Proposed fix (choose one; both are bounded):**
  (a) *Hold-time alarm.* "An alarm onset is the first step at which score ≥ θ after a step with score < θ. Each onset puts the detector in alarm for exactly H = 32 steps, during which further onsets are not counted; the detector leaves alarm at onset + H unless a new onset occurs there. FA = onsets per 10,000 out-of-window steps, matched by exact onset count n* = round(FA × N_out / 10,000), grid {0.5, 1, 2, 5}, headline 1; realised duty cycle = n*·H/N_out is then identical for every detector and is reported. Lead and censoring are computed on this alarm state (lead 128 if in alarm at t_e − 128). B4's reset occurs at each onset." This matches onset count and duty cycle simultaneously, defeats the drifting-B2 pathology the author identified (B2 cannot stay in alarm past H steps per onset), and preserves P-CENS.
  (b) *Null-corrected contrast.* Keep duty cycle but apply the E5 circular-shift null to every detector and define each detector's lead statistic as mean lead minus the mean of its own shifted distribution; C_b is the difference of these excess leads. More complex and makes E2's verdict depend on 1,000 shifts; (a) is preferable.
  Add to D.5: a planted-null cell with baselines of 1-step and 40-step alarm-run length at the same matched FA, which must return false-REFUTE and false-SUPPORT rates ≤ 0.05.

**N2 — The suite's oracle cannot be computed as written**
- **Severity:** MAJOR
- **Location:** DESIGN §D.5 "Grid and pass criteria (F16)", "Oracle (F10)"
- **Evidence:** "the expected lead of every detector is the lead the pipeline's own operators give on the same planted series with the noise removed; the oracle C_min is computed the same way."
- **Why it matters:** The pipeline includes threshold matching. On a noiseless series the out-of-window scores are constant (or a smooth drift), so the candidate set is a handful of tied values, round(FA × N_out) is unreachable, and P-FA returns a θ that gives either zero alarm steps or essentially all of them. The oracle lead is then 0 or 128 for every detector, and "|recovered − oracle| ≤ 8" is unpassable or trivially passable depending on the tie. The 95 % sign-agreement criterion inherits the same degeneracy.
- **Proposed fix:** "Oracle: for each replicate, θ for every detector is matched on the noisy planted series by P-FA; that θ is then applied to the noiseless series (same ramps, same events, noise set to zero) to obtain the oracle leads and oracle C_min. The ±8-step and 95 %-sign criteria compare the noisy-series result to this oracle."

**N3 — N_out and n* on Leg B depend on the spike rate**
- **Severity:** MINOR
- **Location:** DESIGN §D.4 E8; §D.2 FA denominator
- **Evidence:** "at ~4,000 scorable steps per run, 1 % is ~40 alarm steps, so every grid point is realisable"; "the scan windows of ALL events, eligible or not, are excluded from both count and denominator".
- **Why it matters:** The ~4,000 figure ignores the exclusion of every event's 129-step window. In spiky cells (the ones E8 cares about) N_out can fall to a few hundred steps and n* to single digits; at 0.5 % it can round to 1 or 0. Realisability is cell-dependent and the statement in E8 overclaims it.
- **Proposed fix:** "E8 reports N_out and n* per run and per FA target; a run with n* < 5 at headline FA is reported as 'FA not matchable' and excluded from the pooled E8 statistics, with the count of such runs stated." (Under N1 fix (a), n* is an onset count and the same rule applies.)

---

## Summary table

| id | disposition | note |
|---|---|---|
| F1 | closed | mean lead; exposed to N1 via FA definition |
| F2 | closed (censoring); FA redefinition → N1 | rebuttal of "touching runs not FA" stands |
| F3 | closed mechanically; residual in N1/N3 | N_out shrinks with events |
| F4 | closed except B4 | B4 series is θ-dependent; 1-step runs |
| F5 | closed | add cross-series dedup sentence |
| F6 | closed | — |
| F7 | closed | adaptation sound |
| F8 | closed | — |
| F9 | closed | — |
| F10 | rebuttal stands; amendment → N2 | oracle not computable |
| F11 | closed | — |
| F12 | closed | — |
| F13 | closed | — |
| F14 | closed | — |
| F15 | closed | reconcile D_div line with gap reset |
| F16 | closed except via N2 | — |
| F17 | closed | — |
| F18 | closed | — |
| F19 | closed | residual correctly accepted |
| N1 | NEW — BLOCKER | duty cycle makes chance-hit rate detector-dependent; verdict steered by score autocorrelation |
| N2 | NEW — MAJOR | noiseless oracle has no matchable threshold |
| N3 | NEW — MINOR | Leg B N_out/n* cell-dependent; E8 realisability overclaimed |
