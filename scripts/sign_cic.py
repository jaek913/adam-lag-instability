"""Sign the 7-point CIC in verification/cic_signoff.json (author sign-off; run by JAE only). Signs every reviewed script
whose seven flags all pass and whose current SHA-256 equals the reviewed one; refuses otherwise. Then rebuild claims.lock.
Usage: python scripts/sign_cic.py --signer "JAE" [--date YYYY-MM-DD]"""
import argparse
import datetime
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "verification", "cic_signoff.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signer", required=True)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    d = json.load(open(P, encoding="utf-8"))
    problems = []
    for s, e in d["scripts"].items():
        cur = hashlib.sha256(open(os.path.join(ROOT, s), "rb").read()).hexdigest()
        if cur != e["script_sha256"]:
            problems.append(f"{s}: changed since review")
        for h, hv in e.get("helpers_sha256", {}).items():
            if hashlib.sha256(open(os.path.join(ROOT, h), "rb").read()).hexdigest() != hv:
                problems.append(f"{s}: helper {h} changed since review")
        bad = [k for k in map(str, range(1, 8)) if e["flags"].get(k, {}).get("pass") is not True]
        if bad:
            problems.append(f"{s}: flags not passed {bad}")
    if problems:
        print("REFUSED:\n  " + "\n  ".join(problems))
        sys.exit(1)
    for e in d["scripts"].values():
        e["signed"] = f"{a.signer} {a.date}"
    with open(P, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, indent=1)
        f.write("\n")
    print(f"signed {len(d['scripts'])} scripts as '{a.signer} {a.date}'. Now run: python scripts/build_claims.py")


if __name__ == "__main__":
    main()
