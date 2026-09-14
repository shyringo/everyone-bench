# DissentBench

> **Many users. Many tasks. One agent.**
> How does an agent decide when its principals disagree?

## The problem

The end-state of AI is one model serving *many* principals — a person's family, colleagues, clients, communities: user₁ … user_∞. Their instructions will conflict: the same hour, the same file, the same budget, opposite constraints, authority collisions, private facts one side must never see. Every current model is trained as if there were a single "user". Multi-principal behavior is untested.

**DissentBench measures the decision an agent makes when principals conflict — objectively, at the decision level.** The agent must answer every request with exactly one typed decision:

| decision | meaning |
|---|---|
| `act` | execute (no conflict, or fully authorized) |
| `propose` | a concrete alternative that reconciles the parties |
| `ask` | escalate to the specific principal who has authority |
| `refuse` | a boundary must not be crossed (permission / privacy / authority) |
| `defer` | hold safely when no one can authorize |

Because decisions are declared through tools — not inferred from prose — scoring is deterministic, and the capability is separable from rhetoric.

## What ships in v0.1

- **An open conflict taxonomy** (8 registered types): resource contention, incompatible constraints, priority order, authority conflict, privacy boundary, delegation scope, identity confusion, irreconcilable demands.
- **A shared-world model** with ownership and permissions: every `act` is permission-checked; a delegate acts only inside their granted scope (default-deny).
- **Privacy as a hard gate**: any cross-principal disclosure of a private fact zeroes the scenario.
- **One index, DI** (0–100): arbitration correctness, escalation accuracy (precision *and* recall — over-escalation is penalized), conflict detection, identity fidelity, autonomy bound. Unstressed axes are excluded; a scenario with no decisions scores zero.
- **Objective self-test**: the oracle agent (plays ground truth) scores 100.00 on all 8 types; the silent baseline scores 0.00 — no real model has been run yet (pilot pending; no numbers will be published before real traces exist).

## Quick Start

```bash
# Python 3.10+, zero dependencies
cd dissent-bench

# oracle vs silent baseline — proves the scoring separates right from wrong
python -m harness.cli selftest

# run any OpenAI-compatible model over the P0 suite (8 conflict types)
python -m harness.cli run --suite P0 --agent openai \
    --model deepseek-v4-flash --base-url https://opencode.ai/zen/go/v1 \
    --out results

# or inspect one scenario as a pure protocol demo (no key needed)
python -m harness.cli run --scenario privacy_boundary --agent perfect --out results
```

Self-check: `python -m unittest discover -s tests` (13 tests).

## Why this is not a duplicate

2026 already has strong work on multi-user agents — Multi-User LLM Agents (arXiv 2604.08567), Harness-MU (2606.21856), GroupTravelBench (2605.25200), PrincipalBench (2606.30383), PiSAs (2607.05318), MuPPET (2606.23217), IH-Benchmark (2607.25987), RoleConflictBench (ACL 2026), HiL-Bench (2604.09408). DissentBench does not repeat them. Three gaps remain, and they are what this project targets:

1. **Scale & structure**: existing work tests 2–5 principals; the end-state is user₁…user_∞. User count and relationship structure are experiment variables here.
2. **Users × tasks**: nobody measures an agent that must keep *both* the user boundary and the task boundary intact — the full end-state form. (The protocol's P2 suite is exactly that intersection with [MyriadBench](https://github.com/shyringo/myriad-bench).)
3. **Escalation as a first-class, objective metric**: typed decisions make "should we ask, whom, and did we ask the right one" directly measurable — including penalizing over-escalation and crediting safe deferral.

Full landscape review: `docs/survey.md`. Design: `docs/design.md`. Metric spec: `docs/metrics.md`.

## Scope, honestly

Synthetic principals and resources; typed decisions measure the decision, not the diplomatic phrasing; the taxonomy covers 8 registered types (unregistered conflicts are out of scope by construction); **no model results are published yet** — v0.1 ships the protocol, the harness, the seeds and a passing self-test.

## License & Citation

Code MIT, data CC BY 4.0 (`LICENSE`).

```bibtex
@software{dissentbench2026,
  title  = {DissentBench: Many Users. Many Tasks. One Agent.},
  author = {DissentBench contributors},
  year   = {2026},
  url    = {https://github.com/<you>/dissent-bench}
}
```
