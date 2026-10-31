# Independent check of DESIGN Amendment 1 — prompt (paste as the ONLY message of a fresh session)

You are an adversarial reviewer of one proposed amendment to a public pre-registration. The package below this prompt has two parts:

1. **The amendment draft.** It re-expresses one data run's detector operators on that run's native logging grid.
2. **The frozen text it modifies**, verbatim: DESIGN §D.2 (operators), §D.3 (experiments) and §K (kill rule), as frozen at the public tag `prereg-v1`.

No data, code, results or decision log exist for you. Judge only what is written. Do not browse the web.

**Background, stated once.**
- The primary run (A1) turned out to log its gradient norm only every 10 training steps. Its loss is logged every step.
- The frozen design assumed every-step logging.
- The amendment must be made and pushed before any A1 metric value is read.
- The author's claim: the amendment changes only the time unit of detector-side quantities (steps → grid observations), plus one declared exception, the A1 spike dedup (200 → 2,000 steps).

**This is a single-round check.** There is no follow-up message and no fix round. Your reply is final.

## Four passes, one concern each — keep them separate

**Pass 1 — Can every frozen rule still return each of its outcomes on A1 under the amendment?**
Cover E1, E2 (SUPPORT / INCONCLUSIVE / REFUTE / INSUFFICIENT EVENTS, and the k ladder), §K (STOP / CLOSE / PROCEED), the E5 flag, and E3's use of A1. For each, consider the regime the amended A1 will occupy:
- 10-step resolution;
- 320- and 1,280-step windows;
- 1,000-observation minimum history;
- 2,000-step dedup;
- 1,280-step scan window.

A rule that can no longer return an outcome, or whose outcome is now decided by an artefact of the translation, is a finding.

**Pass 2 — Is any translation a judgment described as execution?**
List every place where two analysts following the amendment plus the frozen text could compute different numbers for A1. Examples to check:
- alignment of per-step spike times to grid observations at the window edges;
- the "first grid observation in the window" when t_e − 1,280 is not a multiple of 10;
- censoring with the hold measured in observations;
- the dropped-observation carry-forward versus gaps;
- the rewind-event minimum-history test.

**Pass 3 — Does the amendment change more than it declares?**
The declared changes are the unit change and the dedup exception (and the added E4 pair, sensitivity only). Find any other change to a frozen number, ratio, grid point, rule partition, event definition or report form, explicit or implied. Say whether it is defensible, or should be declared or removed.

**Pass 4 — Internal consistency.**
Check the following against each other and against the frozen text:
- dedup versus scan window;
- hold versus scan window versus censoring;
- FA denominator versus scan-window exclusion;
- minimum history versus segment lengths and rewind events;
- the E1 lags versus the windows;
- the suite cell versus the operators it must validate.

## Output format

Number findings G1, G2, …. For each finding give:
- **Pass:** 1–4.
- **Severity:** BLOCKER, MAJOR or MINOR.
- **Location:** amendment section, or frozen section.
- **Evidence:** a short quote.
- **Why it matters.**
- **Proposed fix:** amendment wording that could be pasted in.

End with a table of all findings. If a pass finds nothing, say "Pass N: no findings" and give the strongest reason.

---
