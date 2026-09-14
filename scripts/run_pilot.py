"""One-command pilot for DissentBench P0 (run only after the user's go-ahead).

    python scripts/run_pilot.py --model deepseek-v4-flash
    python scripts/run_pilot.py --model mimo-v2.5 --suite P0

Key resolution: --api-key, DISSENT_API_KEY, OPENCODE_API_KEY, ~/.pi/agent/auth.json.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harness.agents import OpenAICompatAgent  # noqa: E402
from harness.cli import suite_scenarios  # noqa: E402
from harness.metrics import aggregate, verify_scenario  # noqa: E402
from harness.runner import run_scenario  # noqa: E402

BASE_URL = "https://opencode.ai/zen/go/v1"


def resolve_key(cli_key):
    if cli_key:
        return cli_key
    for env in ("DISSENT_API_KEY", "MYRIAD_API_KEY", "OPENCODE_API_KEY", "OPENAI_API_KEY"):
        v = os.environ.get(env)
        if v:
            return v
    auth = os.path.expanduser("~/.pi/agent/auth.json")
    if os.path.exists(auth):
        data = json.load(open(auth, encoding="utf-8"))
        go = data.get("opencode-go") or {}
        if go.get("key"):
            return go["key"]
    raise SystemExit("no API key: pass --api-key or set DISSENT_API_KEY")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--base-url", default=BASE_URL)
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--suite", default="P0")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    key = resolve_key(args.api_key)
    agent = OpenAICompatAgent(args.model, base_url=args.base_url, api_key=key)
    os.makedirs(args.out, exist_ok=True)
    reports = []
    for sc in suite_scenarios(args.suite):
        trace = run_scenario(sc, agent)
        rep = verify_scenario(sc, trace)
        reports.append(rep)
        with open(os.path.join(args.out, f"{sc['scenario_id']}-{args.model}.trace.json"), "w",
                  encoding="utf-8") as f:
            json.dump(trace, f, ensure_ascii=False, indent=2, default=str)
        print(f"{sc['scenario_id']:32s} DI={rep['DI']:6.2f} gates={len(rep['gates_failed'])}", flush=True)
    summary = {"model": args.model, "suite": args.suite, "aggregate": aggregate(reports)}
    with open(os.path.join(args.out, f"summary-{args.model}.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary["aggregate"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
