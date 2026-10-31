"""Process one A1 segment end to end (JAE 2026-10-30, after entry 8):
route-1 file -> manifest MD5 -> SHA-256 -> store -> D.1 check -> route-1b windows (by SHA-256)
-> stitch cross-check. HARD STOP (exit 1) on any MD5 mismatch, missing file, D.1 failure,
or stitch/cell failure. Counts, flags and hashes only; no metric value is printed.

It calls the committed check scripts unchanged:
  scripts/a1_d1_check.py, scripts/a1_route1b_stitch.py

Usage:
  python scripts/a1_process_segment.py <manifest_json> <downloads_dir> <store_root>

Manifest (written from W&B GraphQL metadata and the in-page window hashes):
  {"seg": "run-008", "id": "bnzb4pmk", "artifact": "run-bnzb4pmk-history:v0",
   "route1_md5": "...", "route1_bytes": 31778101, "server_lines": 20811,
   "windows": [{"name": "A1_run-008_bnzb4pmk_route1b_w01_52300-60299.json",
                "bytes": 123, "sha256": "...", "fetched_utc": "..."}, ...]}
Files in downloads_dir are identified by content hash only (never by name). Duplicate
copies are left in place; exactly one copy is moved.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def digest(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_mtime(path):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stop(msg, summary):
    summary["HARD_STOP"] = msg
    print(json.dumps(summary, indent=2))
    sys.exit(1)


def find_by_hash(dirpath, size, algo, want):
    """Return the first file in dirpath with this size and digest (or None)."""
    for name in sorted(os.listdir(dirpath)):
        p = os.path.join(dirpath, name)
        if not os.path.isfile(p) or os.path.getsize(p) != size:
            continue
        if digest(p, algo) == want.lower():
            return p
    return None


def main():
    man_path, dl, store = sys.argv[1:4]
    with open(man_path, encoding="utf-8") as f:
        m = json.load(f)
    seg, rid = m["seg"], m["id"]
    ver = m["artifact"].split(":")[-1]
    summ = {"seg": seg, "id": rid, "manifest": os.path.basename(man_path)}

    # 1. route-1 file by manifest MD5 (size first)
    a1 = os.path.join(store, "A1")
    dest1 = os.path.join(a1, f"{seg}_{rid}_history-{ver}_0000.parquet")
    if os.path.exists(dest1):
        if digest(dest1, "md5") != m["route1_md5"]:
            stop("route-1 file already in store with a different MD5", summ)
    else:
        src = find_by_hash(dl, m["route1_bytes"], "md5", m["route1_md5"])
        if src is None:
            stop("route-1 file not found in downloads by size+MD5 (still downloading, or MD5 mismatch)", summ)
        os.replace(src, dest1)
    summ["route1"] = {"store": dest1, "bytes": os.path.getsize(dest1),
                      "md5": digest(dest1, "md5"), "sha256": digest(dest1, "sha256"),
                      "md5_matches_manifest": digest(dest1, "md5") == m["route1_md5"],
                      "landed_utc": utc_mtime(dest1)}

    # 2. D.1 check (committed script, unchanged)
    out_dir = os.path.join(HERE, "outputs")
    tag = seg.replace("-", "")
    d1_json = os.path.join(out_dir, f"d1_A1_{tag}.json")
    r = subprocess.run([sys.executable, os.path.join(HERE, "a1_d1_check.py"), dest1,
                        f"A1-{seg}", str(m["server_lines"]), m["route1_md5"], d1_json],
                       capture_output=True, text=True)
    if r.returncode != 0:
        stop("D.1 check script error: " + r.stderr.strip().splitlines()[-1], summ)
    with open(d1_json, encoding="utf-8") as f:
        d1 = json.load(f)
    keep = ["md5_matches_manifest", "rows", "server_historyLineCount", "rows_minus_server_lines",
            "first_step", "last_step", "n_contiguous_blocks", "duplicate_steps", "non_integral_steps",
            "loss_rows", "loss_first", "loss_last", "loss_n_contiguous_blocks",
            "bookkeeping_only_rows", "rows_without_loss_not_bookkeeping",
            "gn_rows", "gn_off_grid_count", "grid_steps_in_loss_span", "grid_steps_missing_gn_count",
            "D1_pass_strict", "D1_pass"]
    summ["D1"] = {k: d1.get(k) for k in keep}
    if not d1.get("D1_pass"):
        stop("D.1 FAILED", summ)

    # 3. route-1b windows by SHA-256
    wdir = os.path.join(a1, "route1b", seg)
    os.makedirs(wdir, exist_ok=True)
    moved = []
    for w in m["windows"]:
        dest = os.path.join(wdir, w["name"])
        if os.path.exists(dest):
            if digest(dest, "sha256") != w["sha256"]:
                stop(f"window {w['name']} in store with a different SHA-256", summ)
        else:
            src = find_by_hash(dl, w["bytes"], "sha256", w["sha256"])
            if src is None:
                stop(f"window {w['name']} not found in downloads by size+SHA-256", summ)
            os.replace(src, dest)
        moved.append({"name": w["name"], "bytes": os.path.getsize(dest),
                      "md5": digest(dest, "md5"), "sha256": digest(dest, "sha256"),
                      "fetched_utc": w.get("fetched_utc"),
                      "landed_utc": utc_mtime(dest)})
    summ["route1b_windows"] = moved

    # 4. stitch cross-check (committed script, unchanged)
    st_json = os.path.join(out_dir, f"route1b_stitch_A1_{tag}.json")
    st_parq = os.path.join(wdir, f"{seg}_{rid}_route1b_stitched.parquet")
    r = subprocess.run([sys.executable, os.path.join(HERE, "a1_route1b_stitch.py"), f"A1-{seg}", wdir,
                        f"A1_{seg}_{rid}_route1b_w*.json", st_parq, st_json, dest1],
                       capture_output=True, text=True)
    if r.returncode != 0:
        stop("stitch script error: " + (r.stderr.strip().splitlines() or ["?"])[-1], summ)
    with open(st_json, encoding="utf-8") as f:
        st = json.load(f)
    summ["stitch"] = {"asserts": st["asserts"], "rows_per_column": st["counts"]["rows_per_column"],
                      "per_column": st.get("route1_compare", {}).get("per_column"),
                      "stitched_md5_sha256": st["stitched_parquet"]["md5_sha256"],
                      "stitch_pass": st["stitch_pass"]}
    if not st["stitch_pass"]:
        stop("STITCH / CELL CROSS-CHECK FAILED", summ)
    summ["SEGMENT_PASS"] = True
    with open(os.path.join(out_dir, f"process_A1_{tag}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summ, f, indent=2)
        f.write("\n")
    print(json.dumps(summ, indent=2))


if __name__ == "__main__":
    main()
