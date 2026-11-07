"""Amendment 14.2 negative self-test of the PRV hash check, in SCRATCH only (the data store is only read).
Copies one A1 file listed in SOURCES.md from the store into a scratch store with the same relative path, then:
(1) the intact copy must PASS; (2) the copy with one byte flipped must HALT (exit 1); (3) a missing file must HALT.
Usage: python scripts/tests/test_prv_hash_selftest.py <data_store_root> <scratch_dir> [relative path]"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHK = os.path.join(ROOT, "scripts", "prv_hash_check.py")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import prv_hash_check as P  # noqa: E402


def run(store, rel):
    r = subprocess.run([sys.executable, CHK, store, "--only", rel], capture_output=True, text=True)
    return r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr


def main():
    store, scratch = sys.argv[1], sys.argv[2]
    rel = sys.argv[3] if len(sys.argv) > 3 else "A1/run-025_u3obk6mj_history-v2_0000.parquet"   # smallest A1 file
    if os.path.abspath(scratch).startswith(os.path.abspath(store)):
        raise SystemExit("scratch must be outside the data store")
    rel = rel.replace("\\", "/")
    assert rel in dict(P.listed(os.path.join(ROOT, "SOURCES.md"))), "file not listed in SOURCES.md"
    src = os.path.join(store, *rel.split("/"))
    dst = os.path.join(scratch, "store", *rel.split("/"))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    checks = []
    rc, out = run(os.path.join(scratch, "store"), rel)
    checks.append(("intact copy passes", rc == 0, out))
    with open(dst, "r+b") as f:
        f.seek(os.path.getsize(dst) // 2)
        b = f.read(1)
        f.seek(-1, 1)
        f.write(bytes([b[0] ^ 0xFF]))
    rc, out = run(os.path.join(scratch, "store"), rel)
    checks.append(("WATCH-FAIL one flipped byte halts (exit 1)", rc == 1, out))
    os.remove(dst)
    rc, out = run(os.path.join(scratch, "store"), rel)
    checks.append(("WATCH-FAIL missing file halts (exit 1)", rc == 1, out))
    for n, c, o in checks:
        print(("PASS " if c else "FAIL ") + n + "  [" + o + "]")
    ok = all(c for _, c, _ in checks)
    print("ALL PASS" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
