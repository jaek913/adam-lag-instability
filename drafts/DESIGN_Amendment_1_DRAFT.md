## Amendment 1 (DRAFT v2, 2026-10-30; not yet appended to DESIGN.md) — A1 on its native 10-step gradient-norm grid

**Trigger.** First data contact on A1 (DECISIONS entry 5; Discrepancy Register D-01). A1 logs `optim/total_grad_norm` only on steps with step mod 10 = 0. The evidence:
- run config `optimizer.metrics_log_interval: 10`;
- `configs/official-0724/OLMo-7B-0424.yaml`;
- training commit `43a155f`, whose `clip_grads_and_collect_metrics` returns no optimizer metrics on other steps.

`train/CrossEntropyLoss` is logged every step. Before this amendment, only the following were read from A1: schema (column names), row count, step range, and the per-row null mask of those two columns. No metric value was read. This amendment is made and pushed publicly before any A1 metric value is read (Phase 2 override (3)).

**What it changes.** It changes the time unit of every detector-side quantity for A1 from steps to grid observations. The numbers, ratios, grid points and rule partitions are unchanged. There is **one exception**: A1's chained spike dedup rises from 200 to 2,000 steps (A1.3).

**Choice (JAE, 2026-10-30, option (c)).** A1 remains the primary run (E2, §K), with its detectors run on its native 10-step grid. A2 and A3 (OLMo 2 stage 1) remain per-step replication runs under D.2 as frozen. A2 is confirmed every-step on run-08 (DECISIONS entry 5 item 7); A3 is to be confirmed at staging.

**A1.1 Grid.**
- A1's detector series is indexed by grid observation j at step t_j = 10·j.
- y_j = ln g(t_j).
- A grid step present in the log but without `optim/total_grad_norm` is a dropped observation: it is counted, y is carried forward, and it is not a gap (D.2, F15).
- A step absent from the log altogether is a gap (D.1).

**A1.2 Detector operators in grid observations.** Every window, hold and count in the detector space is expressed in grid observations, with the frozen numbers unchanged:
- **D_div:** SMA over w_f = 32 and w_s = 128 grid observations (320 and 1,280 steps); ratio 4, inside the Theorem 14 band. Percentile history since the last gap; minimum history 1,000 grid observations (A1.4).
- **B1:** rolling window 50 grid observations; P-B1 sweep {25, 50, 100}, also in grid observations.
- **B2:** unchanged.
- **B3:** α = 0.97 per grid observation; warm-up 25 grid observations.
- **B4:** median and MAD over 200 grid observations, minimum 30; k = 1.0; resets at each onset and at each gap.
- **Alarm onset and hold (P-HOLD):** H = 32 grid observations (320 steps).
- **FA:** alarm onsets per 10,000 out-of-window grid observations. Grid {0.5, 1, 2, 5}; headline 1. n* = round(FA × N_out / 10,000), with N_out counted in grid observations. P-FA is otherwise unchanged.
- **E1:** horizon h = 16 grid observations; R̄ windows [h, h + 32] and [h + 32, h + 128] in grid observations; ACF lags 0–256 grid observations; permutation blocks of 128 grid observations.
- **E5:** circular-shift offsets in [1,000, N − 1,000] grid observations; block shuffle in blocks of 128 grid observations.
- **E4:** window pairs (16, 64) and (64, 256) in grid observations, as frozen. **Added:** a physical-scale pair (4, 16) grid observations (40 and 160 steps), which approximates the frozen per-step pair's step span. It is reported with no verdict.

**A1.3 Loss side.**
- The spike definition (L(t) > SMA_128(L)(t−1) + k·σ_128(L)(t−1), over finite values) stays on the per-step loss: k ladder P-KLAD, NaN rule, event time t_e in steps.
- **A1 dedup (changed): chained, 2,000 steps (200 grid observations).** A spike is merged into the current event if it lies within 2,000 steps of the most recently merged spike.
  - *Reason:* with the scan window at 1,280 steps (A1.4), the frozen 200-step dedup would let scan windows of consecutive events overlap. A 2,000-step dedup restores dedup > scan window, which the frozen per-step design had (200 > 128). Consecutive A1 event times are then more than 2,000 steps apart, and no event's scan window contains another event's spike.
  - *Cost, stated:* clusters of spikes within 2,000 steps collapse into one event. A1's eligible-event count is therefore lower than under 200 steps, and the risk that both k-ladder rungs fall below 5 events — **INSUFFICIENT EVENTS → §K CLOSE** — is higher.
- The eligible-event count for the k ladder is computed with the 2,000-step dedup from the per-step loss, before any detector score.
- The per-step runs (A2–A6, Leg B) keep 200 steps.

**A1.4 Scan window, lead and minimum history.**
- **Scan window.** The window is the w_s grid observations up to the event: the grid observations with t_j ∈ [t_e − 1,280, t_e].
  - *Reason:* in the frozen design the scan window equals w_s (128 = w_s). It is the span over which the slow average still carries pre-event information, and it sets the longest lead D_div can register. Keeping it equal to w_s, now counted in grid observations, keeps the scan window, the maximum lead, the left-censoring point and the hold in the same ratios as frozen.
  - The FA exclusion (all events' scan windows) uses this window.
- **Lead.** Lead = t_e − t_j*, where t_j* is the step of the first grid observation in the window at which the detector is in alarm. It is reported in steps at 10-step resolution.
  - If the detector is already in alarm at the first grid observation of the window (and at the one before), the event is left-censored: lead = 1,280 steps, flagged (P-CENS).
  - A missed event has lead 0 (P-MISS).
  - C_b and C_min are computed on mean leads in steps.
- **Minimum history: 1,000 grid observations (10,000 steps), from the first post-gap observation.**
  - *Reason:* the minimum history exists so that the expanding percentile score and B4's 200-observation median/MAD window are estimated from a stable number of observations. Those are counts, so it is kept as a count.
- **Event eligibility.** Every detector has a defined score at every grid observation in the scan window, with no gap inside it.
- **Rewind events (P-SEG) made ineligible by the minimum history.** A rewind event's scores are computed on its own earlier segment. If fewer than 1,000 grid observations separate that segment's first observation (or its last gap) from the start of the event's scan window, the event is ineligible. The count of such events is reported beside the rewind-event count.

**A1.5 Consequences, stated rather than tuned.**
- On A1, D_div's windows span 320 and 1,280 steps. That is 16 and 64 times the optimizer's second-moment memory (W = 20 steps), against 1.6 and 6.4 times in the per-step design. S3 is restated accordingly.
- A1's lead resolution is 10 steps.
- **Scope condition on A1:** a precursor shorter than about one fast window (320 steps) favours the raw-reading baselines by construction.

**A1.6 E3 like-for-like sensitivity.**
- A2 and A3 are scored per step as frozen.
- As an E4-type sensitivity with no verdict, E2's statistic is also reported on A2 and A3 subsampled to step mod 10 = 0, with the A1.2–A1.4 operators and the A1 dedup. This makes the A1 versus A2/A3 comparison like-for-like.

**A1.7 Suite (D.5), new cell.** Ten-step-grid cell:
- Planted per-step series observed only on step mod 10 = 0.
- Precursor ramps L ∈ {640, 1,000, 1,500, 2,000} steps (64–200 grid observations), plus one ramp shorter than a fast window (200 steps), which must show the A1.5 scope condition.
- Loss spikes planted per step, with A1's 2,000-step dedup.
- The pipeline runs with the A1.2–A1.4 operators.
- Pass criteria as D.5, with the lead tolerance set to ±10 steps (one grid observation).
- Planted null, decision flip, unequal-memory null, P-CENS cluster probe and k ladder are all exercised on the grid.
- A carry-forward probe for a missing grid observation.
- A rewind-event probe at the minimum-history boundary.
- The regime span reports which grid cell A1 lands in.

**A1.8 Unchanged.**
- Frozen: k = 4 primary rung; dedup 200 steps for every per-step run; headline FA 1 per 10,000 (grid observations for A1); window pair (32, 128); ratio 4; H = 32; all rule partitions; §K grading day 2026-11-20.
- Leg B (own runs log every step) and A2–A6 per-step runs follow D.2 as frozen.

**A1.9 THESIS.** A matching THESIS amendment, A4, is required. For A1 it restates:
- A3(a)'s false-alarm wording as "alarm onsets per 10,000 out-of-window gradient-norm observations (A1 logs the gradient norm every 10 steps), each onset held 32 observations";
- the scope condition in A1.5.
