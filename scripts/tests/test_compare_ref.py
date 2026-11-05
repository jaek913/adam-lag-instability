"""Watch-to-fail for the Amendment 8.1 comparison harness (scripts/suite/compare_ref.py): each compared
field, perturbed in the reference's output, must be reported as a difference; unperturbed must be identical.
Usage: python scripts/tests/test_compare_ref.py"""
import copy
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "reference"), os.path.join(ROOT, "scripts", "suite")]
import compare_ref  # noqa: E402
import ref_e2  # noqa: E402
import synth  # noqa: E402

CHECKS = []


def ok(n, c):
    CHECKS.append((n, bool(c)))


def main():
    blocks, events = synth.make_series(30_000_000, n=8000, phi=0.9, n_events=4, L=100, A=3.0)
    real = ref_e2.run_reference
    base = real([{"first_step": 0, "g": list(blocks[0]["g"])}], events, fa=1.0, grid=1, scan=128, hold=32)
    ok("unperturbed: identical", compare_ref.compare(blocks, events, 1, 128) == [])
    det = next(d for d in ("D_div", "B1", "B2", "B3", "B4") if base[d]["onsets"])
    lead0 = next((i for i, x in enumerate(base[det]["leads"]) if x == 0), 0)

    def perturbed(fn, name):
        def fake(*a, **k):
            r = copy.deepcopy(base)
            fn(r)
            return r
        ref_e2.run_reference = fake
        try:
            d = compare_ref.compare(blocks, events, 1, 128)
        finally:
            ref_e2.run_reference = real
        ok(f"WATCH-FAIL detects {name}", len(d) > 0)

    perturbed(lambda r: r[det]["onsets"].__setitem__(0, r[det]["onsets"][0] + 1), f"{det} onset shifted by one step")
    perturbed(lambda r: r[det]["concurrent"].__setitem__(lead0, not r[det]["concurrent"][lead0]), f"{det} concurrent flag flipped")
    perturbed(lambda r: r[det]["detected"].__setitem__(0, not r[det]["detected"][0]), f"{det} detected flag flipped")
    perturbed(lambda r: r[det]["censored"].__setitem__(0, not r[det]["censored"][0]), f"{det} censored flag flipped")
    perturbed(lambda r: r[det]["leads"].__setitem__(0, r[det]["leads"][0] + 1), f"{det} lead +1")
    perturbed(lambda r: r[det].__setitem__("theta", r[det]["theta"] * (1 + 1e-5)), f"{det} theta x (1+1e-5)")
    perturbed(lambda r: r[det].__setitem__("realised", r[det]["realised"] + 1), f"{det} realised +1")
    perturbed(lambda r: r.__setitem__("C_min", r["C_min"] + 1e-3), "C_min + 1e-3")
    perturbed(lambda r: r.__setitem__("N_out", r["N_out"] + 1), "N_out + 1")
    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print("ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
