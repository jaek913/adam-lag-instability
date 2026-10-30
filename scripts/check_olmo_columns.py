"""Read-only existence check: metric NAMES for the OLMo-0424 and OLMo 2 W&B runs.

Phase 0 of adam-lag-instability (DECISIONS.md entry 2). Lists, for each run,
the metric names present in the run summary and flags any gradient-norm
metric. It NEVER calls run.history() or run.scan_history(), and it never
prints or saves metric values -- only names, run metadata, and logging-interval
config keys. Output: printed report + scripts/outputs/check_olmo_columns.json.

Usage:
    python check_olmo_columns.py [--base-url https://api.wandb.ai] [--max-runs 200]
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

import wandb

TARGETS = [
    # (label, path, filters)
    ("A1 OLMo-0424 7B pretraining", "ai2-llm/OLMo-7B", {"group": "OLMo-1.7-7B"}),
    ("A1b OLMo-0424 7B anneal", "ai2-llm/OLMo-7B", {"group": "OLMo-1.7-7B-anneal"}),
    ("A2 OLMo 2 7B", "ai2-llm/OLMo-2-1124-7B", {}),
    ("A3 OLMo 2 13B", "ai2-llm/OLMo-2-1124-13B", {}),
]

GRAD_RE = re.compile(r"grad.*norm|norm.*grad", re.IGNORECASE)
CLIP_RE = re.compile(r"clip", re.IGNORECASE)
INTERVAL_RE = re.compile(r"interval|log_every|log_freq|logging_steps", re.IGNORECASE)


def flatten(d, prefix=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, dict) and "value" not in v:
                out.update(flatten(v, key))
            elif isinstance(v, dict) and "value" in v:
                out.update(flatten(v["value"], key) if isinstance(v["value"], dict) else {key: v["value"]})
            else:
                out[key] = v
    return out


def clip_status(name):
    n = name.lower()
    if "pre" in n and "clip" in n:
        return "pre-clip (per name)"
    if "post" in n and "clip" in n or "clipped" in n:
        return "post-clip (per name)"
    return "not stated by name"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=None,
                    help="W&B API host; default = your wandb settings. Public ai2-llm projects live on https://api.wandb.ai")
    ap.add_argument("--max-runs", type=int, default=200)
    args = ap.parse_args()

    overrides = {"base_url": args.base_url} if args.base_url else {}
    api = wandb.Api(overrides=overrides, timeout=60)
    base = getattr(api.settings, "get", lambda k, d=None: d)("base_url", None) if hasattr(api, "settings") else None
    print(f"wandb {wandb.__version__} | API base_url: {base or args.base_url or '(default)'}")
    print("READ-ONLY: no history rows requested; metric values are not printed or saved.\n")

    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "wandb_version": wandb.__version__,
        "base_url": base or args.base_url,
        "targets": [],
    }

    for label, path, filters in TARGETS:
        entry = {"label": label, "path": path, "filters": filters, "runs": [], "error": None}
        print("=" * 78)
        print(f"{label}  ::  {path}  filters={filters}")
        try:
            runs = api.runs(path, filters=filters or None, per_page=50)
            n = 0
            for run in runs:
                if n >= args.max_runs:
                    print(f"  (stopped at --max-runs {args.max_runs})")
                    break
                n += 1
                try:
                    keys = sorted(k for k in run.summary.keys() if not k.startswith("_"))
                except Exception as e:  # summary unavailable
                    keys = []
                    print(f"  ! {run.id}: summary keys unavailable: {e}")
                grad_keys = [k for k in keys if GRAD_RE.search(k)]
                clip_keys = [k for k in keys if CLIP_RE.search(k)]
                cfg = flatten(dict(run.config))
                interval_cfg = {k: v for k, v in cfg.items() if INTERVAL_RE.search(k) and isinstance(v, (int, float, str))}
                last_step = getattr(run, "lastHistoryStep", None)
                rec = {
                    "id": run.id, "name": run.name, "group": run.group, "state": run.state,
                    "created_at": str(run.created_at), "last_history_step": last_step,
                    "n_metric_names": len(keys), "grad_norm_metric_names": grad_keys,
                    "clip_metric_names": clip_keys, "logging_interval_config": interval_cfg,
                    "all_metric_names": keys,
                }
                entry["runs"].append(rec)
                print(f"  run {run.id}  name={run.name!r}  state={run.state}  lastHistoryStep={last_step}")
                print(f"    metric names: {len(keys)}")
                if grad_keys:
                    for k in grad_keys:
                        print(f"    GRAD-NORM METRIC: {k!r}  [{clip_status(k)}]")
                else:
                    print("    GRAD-NORM METRIC: none found in summary keys")
                if clip_keys:
                    print(f"    clip-related names: {clip_keys}")
                if interval_cfg:
                    print(f"    logging-interval config: {interval_cfg}")
                else:
                    print("    logging cadence: not visible in config metadata")
            entry["n_runs"] = n
            print(f"  runs listed: {n}")
        except Exception as e:
            entry["error"] = f"{type(e).__name__}: {e}"
            print(f"  ERROR: {entry['error']}")
        report["targets"].append(entry)

    print("\n" + "=" * 78)
    a1 = report["targets"][0]
    found = sorted({k for r in a1["runs"] for k in r["grad_norm_metric_names"]})
    if not a1["runs"]:
        verdict = "UNDETERMINED -- no runs listed (" + str(a1.get("error")) + ")"
    elif found:
        verdict = "PRESENT: " + ", ".join(found)
    else:
        verdict = "NOT FOUND in summary keys of any listed run"
    report["a1_verdict"] = verdict
    print(f"A1 VERDICT: per-step gradient-norm metric {verdict}")
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "check_olmo_columns.json")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=2, sort_keys=True, default=str)
        f.write("\n")
    print(f"Report written: {out_path}")
    return 0 if a1["runs"] else 2


if __name__ == "__main__":
    sys.exit(main())
