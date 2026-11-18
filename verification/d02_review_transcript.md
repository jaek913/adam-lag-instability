D-02 second focused review

1. Discrepancy

A1's route-1 history artifact for run-025 holds 383 rows against a server historyLineCount of 22,361. Every public W&B interface returns the same 383 rows, and 18 of the 25 A1 segments are incomplete or empty at the source.

2. Cascade

The stated blast radius (route-1 segments, the D.1 check, route priority) is incomplete. It is missing:

* The route-1b gate itself. Addendum B item 3 could not pass and was superseded by Addendum C.
* E2 data selection (entry 44) and the resulting coverage: steps 14,211–52,300 and 504,511–543,360 are uncovered.
* The selection threat, including the higher risk of INSUFFICIENT EVENTS (Addendum C item 4).
* Rewind events that become unscorable, reported only as a lower bound (Addendum C item 5).
* The A1.12 structural report and the Methods limitations.
* Exploratory X1–X3. Their event sets and per-block rates come from the covered ranges only.

The item text also names only run-025, although the adjudication covers all 18 unused segments.

3. Method and grade

The framing gate (MD5 match) and the artifact-versus-server count are direct observations. "Ground truth" is correct for the existence of the shortfall.
Two later claims rest on different evidence and should be graded separately:

* "Shortfall at the source" rests on a four-interface reconciliation (Addendum B item 8), which the method column does not list. Its grade is ground truth, but only for publicly visible interfaces.
* "The gap is specific to A1's copied segments" (entry 5, repeated in the adjudication) is weakened. Seven copied segments are complete, and the original project (mitchish7) cannot be seen. The cause is unverified, so this attribution is at most consistent-with.

4. Adjudication

Every route in the package is closed with a recorded reason:

* Route 1: fails D.1.
* Route 1b: fails at the source for 18 segments; the 7 that are complete pass the gate.
* Route 2: removed, because sampled data cannot pass D.1.
* Route 3: no reply by the 2026-11-13 cutoff, and JAE closed the request with no follow-up (entry 44).
* The original AI2 projects: not visible to an outside account.

The wording "from public sources" is accurate. Route 3 was private, and its closure is documented.
Scoping as a coverage limitation is correct for values. In the seven used segments, route 1 and route 1b agree on 1,029,564 cells with 0 mismatches.
However, "bears on coverage, not on the correctness of any value used" must not be read as "no reported quantity depends on it." These quantities are conditional on coverage:

* E2's eligible-event count and the headline n* = 4;
* X1's 57 events and its p-value;
* X3's per-block rates;
* the rewind-event count, which is a lower bound.

Entry 49's claim that route 3 would leave n* and D_div's unmatchability unchanged is a projection, not an observation.

5. Verdict: CONFIRMED, with these corrections

(a) Extend the blast radius to the items listed in section 2.
(b) Restate the item to cover all 18 unused segments, not only run-025.
(c) Add the cross-interface reconciliation (Addendum B item 8) as a method, graded ground truth for public interfaces.
(d) Downgrade or remove "specific to A1's copied segments" as a cause.
(e) Amend the adjudication's last sentence. It should state that the gap does not affect the correctness of values used, but that E2 and the X1–X3 inferences are conditional on the covered ranges, under the stated selection threat.
