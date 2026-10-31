**Independent check of DESIGN Amendment 1 — findings**

Judged on the package text only. D.1, D.5, D.6, D.7, P-SEG and the THESIS are referenced but not supplied, so anything that depends on them is noted as unverifiable rather than passed.

---

## Pass 1 — Can every frozen rule still return each outcome on A1?

**G1 — FA threshold matching can collapse to n\* = 0 (or 1–2) on the grid, which manufactures REFUTE**
- **Pass:** 1
- **Severity:** MAJOR
- **Location:** A1.2 "FA"; frozen D.2 "Threshold matching"
- **Evidence:** "n\* = round(FA × N_out / 10,000), with N_out counted in grid observations."
- **Why it matters:** N_out in grid observations is one-tenth of N_out in steps. If A1 has fewer than 5,000 scored out-of-window grid observations (≈50,000 steps), n\* at headline FA rounds to 0; θ then becomes the smallest candidate with c(v) ≤ 0, i.e. no alarms for any detector, every lead is 0, C_min = 0, E2 returns REFUTE and §K STOPs — decided by the translation, not the data. Even for a run of ~50k grid observations, n\* ≈ 5 at FA = 1 and ≈ 2 at FA = 0.5, so the matching is coarse and the 0.5 grid point is nearly degenerate. The row count and step range of A1 have already been read, so the amendment can state N and the implied n\* per grid point without touching a metric value.
- **Proposed fix:** Add to A1.2: "A1 has N = ___ grid observations (from the row count already read). The implied n\* at FA ∈ {0.5, 1, 2, 5} is therefore ___ before scan-window exclusion. If n\* at headline FA would be 0, E2 is not run on A1 and §K records E2 as unrun (data availability), not as REFUTE. FA grid points at which n\* < 2 are reported but not used for any contrast."

**G2 — Per-segment eligibility warm-up is now 11,280 steps and its cost is undeclared**
- **Pass:** 1
- **Severity:** MAJOR
- **Location:** A1.4 "Minimum history" and "Event eligibility"; A1.3 "Cost, stated"
- **Evidence:** "Minimum history: 1,000 grid observations (10,000 steps), from the first post-gap observation."
- **Why it matters:** An event is eligible only if every grid observation in [t_e − 1,280, t_e] has ≥ 1,000 observations of post-gap history, so no event in the first ~11,280 steps of any segment is eligible (frozen: ~1,128 steps). A1.3 declares the dedup cost to the event count but not this one, which can be larger on a run with several rewinds or short segments. INSUFFICIENT EVENTS → CLOSE can therefore be produced by the warm-up alone, and the reader cannot tell which cost did it.
- **Proposed fix:** Add to A1.4: "Cost, stated: no event whose scan window begins within 1,000 grid observations (10,000 steps) of a gap is eligible, so A1 events in the first ~11,280 steps after any gap are lost. From the step range and segment list already read (no metric values), ___ segments exceed 11,280 steps. The count of events made ineligible by the minimum history is reported separately from the count merged by the dedup."

Reachability otherwise: E1 (CONSISTENT / INCONSISTENT / INDETERMINATE), the E5 flag, E3's NOT RUN gate and §K's three outcomes all remain reachable; nothing in A1 restricts them beyond G1–G2.

---

## Pass 2 — Is any translation a judgment described as execution?

**G3 — Scan window and lead are not well defined when t_e mod 10 ≠ 0**
- **Pass:** 2
- **Severity:** BLOCKER
- **Location:** A1.4 "Scan window" and "Lead"
- **Evidence:** "the grid observations with t_j ∈ [t_e − 1,280, t_e]" ... "Lead = t_e − t_j\*".
- **Why it matters:** t_e is a per-step loss time and will usually not be a multiple of 10. Then (i) the window holds 128 observations, not 129 as when aligned (the text also says "the w_s grid observations" = 128 while the interval gives 129 when aligned, an inherited off-by-one now made visible); (ii) the maximum uncensored lead varies between 1,271 and 1,280 by event; (iii) an alarm at the last in-window observation yields lead 1–9 steps, which is > 0 and so counts as a detection and in E5's advance-ordering rate, whereas the frozen analogue (alarm at t_e) is lead 0; (iv) the censored lead is a flat 1,280 even when the first in-window observation is at t_e − 1,275. Two analysts will compute different leads, detection rates and C_b on the same data. Lead and detection are the verdict statistic.
- **Proposed fix:** Replace the two bullets with: "Let t_e^g = 10·⌊t_e/10⌋ (the last grid step at or before the event). The scan window is the 129 grid observations with t_j ∈ [t_e^g − 1,280, t_e^g], the analogue of the frozen 129-step interval [t_e − 128, t_e]. Lead = t_e^g − t_j\*, where t_j\* is the first in-window observation at which the detector is in alarm; a detector first in alarm at t_e^g has lead 0; a miss has lead 0; a left-censored event (in alarm at t_e^g − 1,280 and at t_e^g − 1,290) has lead 1,280. t_e itself, in steps, remains the event time for dedup and reporting."

**G4 — What a gap is for the grid series is undefined; a missing non-grid step can reset everything**
- **Pass:** 2
- **Severity:** MAJOR
- **Location:** A1.1; frozen D.2 "Gaps and state"
- **Evidence:** "A step absent from the log altogether is a gap (D.1)."
- **Why it matters:** Under D.1 a gap is a run of steps present in no segment. A single missing non-grid step (e.g. step 12,345) leaves the detector series intact but, read literally, resets every window, EMA, B4 and percentile history and restarts the 10,000-step minimum history; it also splits ACF pairs in E1. One analyst will treat it as a gap for the detector side, another will not. The row count versus step range already read tells the author whether any steps are missing.
- **Proposed fix:** Add to A1.1: "For A1's detector series a gap is a run of one or more grid steps (step mod 10 = 0) absent from the log. A missing non-grid step is a gap for the loss series only: L is treated as non-finite there (excluded from SMA_128(L) and σ_128(L), not a spike) and it does not reset detector state or the minimum history. The step range and row count already read show ___ missing steps, of which ___ are grid steps."

**G5 — The rewind-event rule introduces a reset point that the frozen text does not have**
- **Pass:** 2
- **Severity:** MAJOR
- **Location:** A1.4 "Rewind events"
- **Evidence:** "If fewer than 1,000 grid observations separate that segment's first observation (or its last gap) from the start of the event's scan window, the event is ineligible."
- **Why it matters:** Frozen D.2 counts history from the last gap and says "Nothing else resets state." A segment's first observation is a reset point only if it follows a gap. By naming "that segment's first observation" the amendment lets an analyst count history from a segment join that is not a gap; another analyst will count across it. P-SEG is not in the package, so which series a rewind event is scored on cannot be checked either.
- **Proposed fix:** Replace with: "A rewind event is scored on the series P-SEG assigns to it. Its history is counted from the last gap (D.1) on that series; a segment boundary that is not a gap does not reset the count. The event is ineligible if the first observation of its scan window has fewer than 1,000 grid observations of post-gap history on that series. The count of events made ineligible this way is reported beside the rewind-event count." If a reset at segment start is intended, declare it as a change to D.2.

**G6 — Dropped-observation edge cases**
- **Pass:** 2
- **Severity:** MINOR
- **Location:** A1.1
- **Evidence:** "it is counted, y is carried forward, and it is not a gap"
- **Why it matters:** (i) A dropped first post-gap observation has nothing to carry forward from; (ii) non-positive or non-finite g on a grid step (frozen D.6 item 5) is not mentioned, only null; (iii) a long run of dropped observations is flat y that still counts toward the 1,000-observation history and feeds the ACF. The null mask has been read, so the longest null run is known.
- **Proposed fix:** "A grid observation with null, non-positive or non-finite g is dropped: y is carried forward from the previous scored observation; if it is the first post-gap observation, scoring and the minimum-history count begin at the first non-dropped observation. The longest run of dropped observations on A1 is ___ (from the null mask already read) and is reported."

**G7 — Rounding of n\* is unspecified and now binding**
- **Pass:** 2
- **Severity:** MINOR
- **Location:** A1.2 "FA"; frozen D.2 "Threshold matching"
- **Evidence:** "n\* = round(FA × N_out / 10,000)"
- **Why it matters:** Inherited, but with n\* in the single digits a half-tie (e.g. 2.5 at FA = 0.5) now changes the matched count by 50 %; half-to-even and half-up give different thresholds.
- **Proposed fix:** "round(·) is round-half-up for every run and FA target."

**G8 — A1.6: is the loss also subsampled on A2/A3?**
- **Pass:** 2
- **Severity:** MINOR
- **Location:** A1.6
- **Evidence:** "A2 and A3 subsampled to step mod 10 = 0, with the A1.2–A1.4 operators and the A1 dedup."
- **Proposed fix:** "...with the gradient norm subsampled to step mod 10 = 0, the loss kept per step, and the A1.2–A1.4 operators and A1 dedup."

**G9 — Scan window under the E4 window-pair sensitivities**
- **Pass:** 2
- **Severity:** MINOR
- **Location:** A1.4 "Reason"; A1.2 "E4"
- **Evidence:** "in the frozen design the scan window equals w_s"
- **Why it matters:** The frozen scan window is a fixed 128 steps and does not move with the (16, 64), (64, 256) pairs. The amendment's rationale ties it to w_s, so an analyst running the (4, 16) or (64, 256) pair could rescale the window.
- **Proposed fix:** Add: "The scan window is 129 grid observations (G3) for every detector and every E4 window pair; it does not vary with w_s."

---

## Pass 3 — Does the amendment change more than it declares?

**G10 — D.3 E2 and §K constants are left in step units and are not restated**
- **Pass:** 3
- **Severity:** MAJOR
- **Location:** frozen D.3 E2, §K; amendment "What it changes"
- **Evidence:** E2: "misses entered as 0 and censored events as 128"; "events are ≥ 200 steps apart"; §K: "1 onset per 10,000 out-of-window steps, hold H = 32".
- **Why it matters:** The amendment amends D.2 operators but the verdict text in D.3 and §K still reads 128, 200 and "steps". An analyst applying D.3 literally enters censored A1 events as 128 while leads run to 1,280 — a tenfold error in C_b at exactly the point that decides the verdict. A1.9 restates THESIS wording but not D.3/§K.
- **Proposed fix:** Add "A1.10 Verbatim replacements for A1 in D.3 and §K: E2 'censored events as 128' → 'censored events as 1,280 steps on A1 (128 steps on per-step runs)'; E2 'events are ≥ 200 steps apart' → '≥ 2,000 steps on A1, ≥ 200 on per-step runs'; E2 and §K 'per 10,000 out-of-window steps, hold H = 32' → 'per 10,000 out-of-window scored observations (grid observations on A1, steps elsewhere), hold H = 32 observations'. No other D.3 or §K text changes."

**G11 — A1.5 scope condition on the primary run must be stated not to qualify §K**
- **Pass:** 3
- **Severity:** MAJOR
- **Location:** A1.5
- **Evidence:** "a precursor shorter than about one fast window (320 steps) favours the raw-reading baselines by construction."
- **Why it matters:** This is a new interpretive clause on the run that carries the kill rule. Left as written it can be read after a REFUTE as "the precursors were short, so the kill does not count", which §K forbids ("No re-tuning ... after A1 is touched"). Defensible as a Methods statement only if its non-bearing on §K is explicit.
- **Proposed fix:** Append: "This scope condition is a statement for the Methods and THESIS. It does not qualify E2's label or §K: a REFUTE on A1 STOPs the project whatever the realised precursor lengths."

**G12 — The k-ladder rung now resolves under a different dedup from the runs it governs**
- **Pass:** 3
- **Severity:** MINOR
- **Location:** A1.3; frozen D.2 "k ladder"
- **Evidence:** "The rung that resolves on A1 is used for every Leg A run and for E8".
- **Why it matters:** A1's 2,000-step dedup lowers its event count, making k = 3 more likely to resolve; that rung is then applied to A2–A6 at 200-step dedup, where it yields more events than it would have under frozen A1. The coupling is changed, not merely re-expressed. Defensible, but it is a change to how E3's inputs are set.
- **Proposed fix:** Add: "Declared: the rung is resolved on A1 under the 2,000-step dedup and transported to per-step runs under the 200-step dedup. The eligible-event count on A2–A6 at the other rung is also reported."

**G13 — B3's "documented defaults" label no longer holds in time units**
- **Pass:** 3
- **Severity:** MINOR
- **Location:** A1.2 "B3"
- **Evidence:** "α = 0.97 per grid observation; warm-up 25 grid observations."
- **Why it matters:** ZClip's documented default is per update step; on the grid the EMA memory is ~330 steps, not ~33. Applying the detector-side unit rule is consistent, but the attribution "documented defaults" is now partly a construction choice and should be labelled as such (P-B3 extension).
- **Proposed fix:** "On A1, α = 0.97 and warm-up 25 are applied per grid observation; this is a construction choice under P-B3, not ZClip's documented per-step behaviour, and is so labelled in the Methods."

**G14 — E1's stationarity scope is tightened tenfold and not restated**
- **Pass:** 3
- **Severity:** MINOR
- **Location:** A1.2 "E1"; frozen D.2 "Persistence-sign prediction"
- **Evidence:** "ACF lags 0–256 grid observations".
- **Why it matters:** The R̄ windows now span up to 1,440 steps and lags to 2,560 steps; y's slow upward drift bears far more on the ACF at these horizons than at 0–256 steps, so the "approximate-stationarity" caveat is weaker on A1. A1.5 restates S3 but not E1's scope.
- **Proposed fix:** Add to A1.5: "E1's consistency-check label on A1 holds under approximate stationarity over 2,560-step horizons; the drift in y over that horizon is reported beside ρ."

---

## Pass 4 — Internal consistency

Consistent as written: dedup 2,000 > scan window 1,280 (ratio 1.5625, identical to 200/128); hold 32 obs < window 128 obs, and the censoring note ("onset in [t_e − 160, t_e − 129]") translates one-for-one to grid observations; the E1 lags (0–256) cover the R̄ windows [16, 48] and [48, 144]; B4's 200-observation window and 30-observation minimum sit inside the 1,000-observation minimum history. The two gaps are:

**G15 — The suite cell does not exercise the places where the translation can go wrong**
- **Pass:** 4
- **Severity:** MAJOR
- **Location:** A1.7
- **Evidence:** "Pass criteria as D.5, with the lead tolerance set to ±10 steps."
- **Why it matters:** The cell plants grid-observed series and probes carry-forward and the minimum-history boundary, but it does not plant (i) events with t_e mod 10 ≠ 0 (G3), (ii) a missing non-grid step (G4), (iii) a series short enough that n\* ≤ 2 at some FA grid point (G1), or (iv) a planted series whose length relative to the 11,280-step warm-up and 2,000-step dedup is stated. D.5 pass criteria are not in the package, so "as D.5" cannot be checked here.
- **Proposed fix:** Add to A1.7: "Planted events are placed at t_e with all ten residues mod 10 represented. One probe removes a single non-grid step and must leave detector state and eligibility unchanged. One probe uses a series with N_out = 4,000 and 12,000 grid observations and reports n\* and realised onset counts at each FA grid point. Each planted series is at least 3 × 11,280 steps long with at least two gaps. The D.5 pass criteria are restated verbatim in this cell."

**G16 — FA exclusion: which rung's events are excluded**
- **Pass:** 4
- **Severity:** MINOR
- **Location:** A1.4 "The FA exclusion"; frozen D.2 "False-alarm rate"
- **Evidence:** "the scan windows of ALL events, eligible or not, are excluded".
- **Why it matters:** Inherited ambiguity: k = 3 events are a superset of k = 4 events, so N_out depends on which rung's event set defines "all events". With n\* in the single digits on A1, a few hundred grid observations of denominator can change n\*.
- **Proposed fix:** "'All events' means every event at the rung that resolved on A1 (P-KLAD)."

---

## Summary table

| # | Pass | Severity | Location | One-line issue |
|---|---|---|---|---|
| G1 | 1 | MAJOR | A1.2 FA | n\* in grid obs can round to 0–2; n\* = 0 forces REFUTE by artefact |
| G2 | 1 | MAJOR | A1.4 min history | 11,280-step per-segment warm-up cost to eligibility undeclared |
| G3 | 2 | BLOCKER | A1.4 scan window/lead | Window size, max lead, lead-at-event and censored lead vary with t_e mod 10 |
| G4 | 2 | MAJOR | A1.1 | Gap undefined for grid series; missing non-grid step may reset all state |
| G5 | 2 | MAJOR | A1.4 rewind events | "Segment's first observation" is a reset point frozen text lacks |
| G6 | 2 | MINOR | A1.1 | Dropped-observation edge cases (first post-gap, non-finite g, long runs) |
| G7 | 2 | MINOR | A1.2 FA | Rounding convention for n\* now binding |
| G8 | 2 | MINOR | A1.6 | Whether loss is subsampled on A2/A3 |
| G9 | 2 | MINOR | A1.4 reason / E4 | Scan window must not track w_s in E4 pairs |
| G10 | 3 | MAJOR | D.3 E2, §K | "128", "200 steps", "per 10,000 steps" not restated for A1 |
| G11 | 3 | MAJOR | A1.5 | Scope condition must be declared not to qualify §K |
| G12 | 3 | MINOR | A1.3 / k ladder | Rung resolved at 2,000 dedup governs runs at 200 dedup |
| G13 | 3 | MINOR | A1.2 B3 | "Documented defaults" label inaccurate per grid obs |
| G14 | 3 | MINOR | A1.2 E1 | Stationarity scope at 10× horizon not restated |
| G15 | 4 | MAJOR | A1.7 | Suite lacks t_e mod 10 ≠ 0, non-grid gap, small-N_out and length probes |
| G16 | 4 | MINOR | A1.4 FA exclusion | Which rung's events define "all events" |

The one blocker (G3) and G10 are the two that can change C_min's sign between two careful analysts; both have paste-in fixes above and neither requires reading a metric value.