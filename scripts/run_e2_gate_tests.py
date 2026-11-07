"""E2 gate (DESIGN Amendment 12.2 as corrected by 14.1-14.2): run every committed hand-probe / unit test and the
PRV hash self-test; print one line per test and ALL PASS only if all pass. The statistical cells are graded
separately (scripts/suite/grade_suite.py).
Usage: python scripts/run_e2_gate_tests.py <data_store_root> <scratch_dir>"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "scripts", "tests")


def main():
    store, scratch = sys.argv[1], sys.argv[2]
    os.makedirs(scratch, exist_ok=True)
    runs = [
        ("operators (Amendments 5-6, vendored ZClip/trainscope)", [os.path.join(T, "test_ops.py")]),
        ("E2 statistic (leads, flags, C_min, label)", [os.path.join(T, "test_e2stat.py")]),
        ("spike rule / events (Amendment 3)", [os.path.join(T, "test_a1_events.py"), os.path.join(scratch, "events")]),
        ("A1 loader (ownership, dropped obs)", [os.path.join(T, "test_a1_loader.py"), os.path.join(scratch, "loader")]),
        ("reference implementation self-test", [os.path.join(ROOT, "reference", "selftest.py")]),
        ("cross hand probes (Amendment 8.1)", [os.path.join(T, "test_hand_probes_cross.py")]),
        ("comparison harness watch-to-fail", [os.path.join(T, "test_compare_ref.py")]),
        ("grader watch-to-fail", [os.path.join(T, "test_grade_suite.py")]),
        ("assembly probes (D.5)", [os.path.join(T, "test_assembly_probes.py"), os.path.join(scratch, "assembly")]),
        ("dynamic range: cluster + ties (D.5)", [os.path.join(T, "test_dynamic_range_cluster.py")]),
        ("PRV hash negative self-test (Amendment 14.2)", [os.path.join(T, "test_prv_hash_selftest.py"), store,
                                                         os.path.join(scratch, "prv")]),
    ]
    bad = 0
    for name, cmd in runs:
        r = subprocess.run([sys.executable] + cmd, capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or [r.stderr.strip()[-200:]])[-1]
        ok = r.returncode == 0 and "ALL PASS" in last
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}  [{last}]", flush=True)
    print("E2 GATE TESTS: ALL PASS" if bad == 0 else f"E2 GATE TESTS: {bad} FAILED")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
