"""PRV data-integrity check (DESIGN D.6 item 7; Amendment 14.2): re-hash every store file listed in SOURCES.md
against its recorded SHA-256. Exit 0 only if every listed file exists and matches; exit 1 (HALT) otherwise.
Usage: python scripts/prv_hash_check.py <store_root> [--sources SOURCES.md] [--only <relative store path>]"""
import argparse
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROW = re.compile(r"^\| `([^`]+)` \|.*\| ([0-9a-f]{64}) \|")


def listed(sources):
    out = []
    for line in open(sources, encoding="utf-8"):
        m = ROW.match(line)
        if m:
            out.append((m.group(1).replace("\\", "/"), m.group(2)))
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("store")
    ap.add_argument("--sources", default=os.path.join(ROOT, "SOURCES.md"))
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    rows = listed(a.sources)
    if a.only:
        rows = [r for r in rows if r[0] == a.only.replace("\\", "/")]
    if not rows:
        print("HALT: no SOURCES.md rows selected")
        sys.exit(1)
    bad = 0
    for rel, want in rows:
        p = os.path.join(a.store, *rel.split("/"))
        if not os.path.exists(p):
            print(f"MISSING  {rel}")
            bad += 1
            continue
        got = sha256(p)
        ok = got == want
        bad += not ok
        print(f"{'OK      ' if ok else 'MISMATCH'} {rel}")
    print(f"{len(rows)} files checked, {bad} failed ->", "PASS" if bad == 0 else "HALT")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
