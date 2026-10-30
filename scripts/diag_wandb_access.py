"""Read-only W&B access diagnostic (DECISIONS.md entry 2, attempt 3 prep).

Prints which identity the configured API key resolves to, then tries three
metadata-only reads against the public ai2-llm/OLMo-7B project:
  (a) the project object, (b) one known run by direct path, (c) a one-run
  listing of the OLMo-1.7-7B group. Prints only names/ids/states -- never
  summary values, never history.

Usage:
    python diag_wandb_access.py [--base-url URL]
"""
import argparse
import sys

import wandb

KNOWN_RUN = "ai2-llm/OLMo-7B/u3obk6mj"   # OLMo-1.7-7B-run-025, seen in the web UI 2026-10-30
KNOWN_ARTIFACT = "ai2-llm/OLMo-7B/run-u3obk6mj-history:v2"   # named by JAE from the web UI 2026-10-30


def attempt(label, fn):
    try:
        print(f"[OK]   {label}: {fn()}")
        return True
    except Exception as e:
        print(f"[FAIL] {label}: {type(e).__name__}: {e}")
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=None)
    args = ap.parse_args()
    api = wandb.Api(overrides={"base_url": args.base_url} if args.base_url else {}, timeout=60)
    print(f"wandb {wandb.__version__} | base_url: {api.settings.get('base_url')}")

    def viewer():
        v = api.viewer
        teams = getattr(v, "teams", None)
        return f"username={getattr(v, 'username', None)!r} entity={getattr(v, 'entity', None)!r} teams={teams!r}"

    attempt("key identity (viewer)", viewer)
    attempt("default entity", lambda: api.default_entity)
    attempt("project ai2-llm/OLMo-7B", lambda: api.project("OLMo-7B", entity="ai2-llm").name)
    attempt(f"direct run {KNOWN_RUN}", lambda: (lambda r: f"name={r.name!r} state={r.state} group={r.group!r}")(api.run(KNOWN_RUN)))

    def one_listing():
        for r in api.runs("ai2-llm/OLMo-7B", filters={"group": "OLMo-1.7-7B"}, per_page=1):
            return f"first run name={r.name!r} id={r.id}"
        return "no runs returned"

    attempt("group listing (1 run)", one_listing)

    # Artifact route -- METADATA ONLY. Never call .download(): downloading the
    # history artifact is a data pull of A1 and must come after the public
    # prereg-v1 commit (DECISIONS.md entries 1-2).
    def artifact_meta():
        a = api.artifact(KNOWN_ARTIFACT)
        files = [(e.path, e.size) for e in a.manifest.entries.values()]
        return (f"name={a.name!r} type={a.type!r} size={a.size} created={a.created_at} "
                f"files={len(files)} first={files[:3]}")

    attempt(f"artifact metadata {KNOWN_ARTIFACT} (no download)", artifact_meta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
