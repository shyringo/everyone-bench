"""DissentBench CLI.

    python -m harness.cli selftest                 # oracle must score 100; echo must score ~0
    python -m harness.cli run --suite P0 --agent echo --out results
    python -m harness.cli run --suite P0 --agent openai --model deepseek-v4-flash --out results
    python -m harness.cli report --traces results
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .agents import EchoAgent, OpenAICompatAgent, PerfectAgent, ReplayAgent
from .metrics import aggregate, verify_scenario
from .runner import run_scenario
from .scenarios import GENERATORS, generate_scenario


def suite_scenarios(suite: str) -> list[dict]:
    if suite.upper() == "P0":
        return [generate_scenario(t, seed=0) for t in GENERATORS]
    raise SystemExit(f"unknown suite {suite!r} (P0 is the only shipped suite in v0.1)")


def build_agent(kind: str, args, scenario=None):
    if kind == "echo":
        return EchoAgent()
    if kind == "perfect":
        return PerfectAgent(scenario)
    if kind == "replay":
        actions = json.load(open(args.replay, encoding="utf-8")) if args.replay else [{"type": "reply", "text": "ok"}]
        return ReplayAgent(actions)
    if kind == "openai":
        return OpenAICompatAgent(args.model, base_url=args.base_url, api_key=args.api_key)
    raise SystemExit(f"unknown agent {kind!r}")


def cmd_selftest(args):
    ok = True
    for ctype in GENERATORS:
        sc = generate_scenario(ctype, seed=0)
        oracle = run_scenario(sc, PerfectAgent(sc))
        rep_o = verify_scenario(sc, oracle)
        silent = run_scenario(sc, EchoAgent())
        rep_e = verify_scenario(sc, silent)
        flag = "OK " if rep_o["DI"] >= 99 and rep_e["DI"] <= 20 else "FAIL"
        if flag == "FAIL":
            ok = False
        print(f"{flag} {ctype:24s} oracle={rep_o['DI']:6.2f}  silent={rep_e['DI']:6.2f}")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def cmd_run(args):
    scenarios = suite_scenarios(args.suite)
    if args.scenario:
        scenarios = [generate_scenario(args.scenario, seed=args.seed)]
    reports = []
    os.makedirs(args.out, exist_ok=True)
    for sc in scenarios:
        agent = build_agent(args.agent, args, sc)
        trace = run_scenario(sc, agent)
        rep = verify_scenario(sc, trace)
        reports.append(rep)
        with open(os.path.join(args.out, f"{sc['scenario_id']}-{agent.name}.trace.json"), "w",
                  encoding="utf-8") as f:
            json.dump(trace, f, ensure_ascii=False, indent=2, default=str)
        print(f"{sc['scenario_id']:32s} DI={rep['DI']:6.2f}  "
              f"gates_failed={len(rep['gates_failed'])}")
    agg = aggregate(reports)
    with open(os.path.join(args.out, f"summary-{args.agent}.json"), "w", encoding="utf-8") as f:
        json.dump({"agent": args.agent, "model": args.model, "aggregate": agg,
                   "reports": reports}, f, ensure_ascii=False, indent=2)
    print(json.dumps(agg, ensure_ascii=False, indent=2))
    return 0


def cmd_report(args):
    summaries = [f for f in os.listdir(args.traces) if f.startswith("summary-")]
    if not summaries:
        sys.exit("no summary files found")
    for fn in summaries:
        data = json.load(open(os.path.join(args.traces, fn), encoding="utf-8"))
        print(fn, "->", json.dumps(data["aggregate"], ensure_ascii=False))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="dissent", description="DissentBench harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    st = sub.add_parser("selftest", help="oracle vs silent baseline sanity run")
    st.set_defaults(fn=cmd_selftest)

    r = sub.add_parser("run", help="run a suite with an agent")
    r.add_argument("--suite", default="P0")
    r.add_argument("--scenario", default=None, help=f"one of: {', '.join(GENERATORS)}")
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--agent", default="perfect", choices=["perfect", "echo", "replay", "openai"])
    r.add_argument("--replay", default=None)
    r.add_argument("--model", default="deepseek-v4-flash")
    r.add_argument("--base-url", default=None)
    r.add_argument("--api-key", default=None)
    r.add_argument("--out", default="results")
    r.set_defaults(fn=cmd_run)

    rep = sub.add_parser("report", help="print summaries from a results dir")
    rep.add_argument("--traces", default="results")
    rep.set_defaults(fn=cmd_report)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
