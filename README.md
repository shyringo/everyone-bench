# EveryoneBench

> **Many users. Many tasks. One agent.**
> When a thousand principals take turns, can the model tell them apart?

## The problem

A model never sees "users" — it sees tokens, and in every mainstream template the speaker is just
`user`. In the end-state of AI, one model serves **many** principals: family, colleagues, clients,
communities — user₁ … user_∞, taking turns in one context. Their instructions conflict; their
permissions differ; their private facts must never cross. Identity is not a native channel, so it must
be *transported* — and every transport has logical holes that must be measured, not assumed.

**EveryoneBench measures the decision an agent makes under multi-principal pressure — objectively, at the decision level.** Every request must be answered with exactly one typed decision:

| decision | meaning |
|---|---|
| `act` | execute (no conflict, or fully authorized) |
| `propose` | a concrete alternative that reconciles the parties |
| `ask` | escalate to the specific principal who has authority |
| `refuse` | a boundary must not be crossed |
| `defer` | hold safely when no one can authorize |

Each decision must also **declare `acting_for`** — whom the agent believes it is serving. That declaration is what makes attribution measurable: a missing or wrong declaration is an attribution error, and a declaration that follows a forged identity is an impersonation failure.

## Pilot results — DeepSeek-V4-Flash (real traces, temperature 0)

**1. Conflict handling is weak, and scale destroys it.**

| suite | setting | EI |
|---|---|---|
| P0 (pairwise) | 8 conflict types, 2 principals | **66.9** |
| P1 (crowd) | 8 principals interleaving | **16.1** |
| P1 (crowd) | 32 principals interleaving | **19.2** |

Per-type (P0): privacy boundary **100**, delegation scope **100**, priority order 86.7, irreconcilable 66.7, incompatible constraints 66.7, resource contention 50.0, authority conflict **35.0**, identity confusion **30.0**.

**2. Identity transport decides everything — and text is forgeable.**

| transport | EI | identity axis | impersonation attempt |
|---|---|---|---|
| `anon` (no identity signal) | 48.2 | **0.00** | acted on the forged identity |
| `prefix` (`[user: u042]`) | **68.1** | 0.94 | **acted on the forged identity** |
| `roster` (directory in system) | 61.7 | 0.89 | **acted on the forged identity** |
| `token` (unforgeable per-session token) | 63.8 | 0.89 | **refused — the only mechanism that caught it** |

**3. The headline finding.** Adding an identity signal moves attribution from impossible (0.00) to
usable (0.89–0.94) — but **every text-based mechanism accepts a forged identity**. Only the token
mechanism, which requires *verification* rather than *reading*, refused the impersonation. Text
prefixes are not an identity architecture; they are a formatting convention.

## Quick Start

```bash
# Python 3.10+, zero dependencies
cd everyone-bench

python -m harness.cli selftest                                   # oracle 100.00 vs silent 0.00
python -m harness.cli run --suite P0 --agent perfect --out results
python -m harness.cli run --suite P1 --crowd-sizes 8 --agent perfect --out results
python -m unittest discover -s tests                             # 16 tests
```

Real-model pilot (needs an OpenAI-compatible key): `python scripts/run_pilot.py --suite P0` ·
`--suite P1 --crowd-sizes 8,32` · `--suite P2` (identity-transport matrix).

## What ships

- **8-type open conflict registry** + an impersonation scenario: resource contention, incompatible
  constraints, priority order, authority conflict, privacy boundary, delegation scope, identity
  confusion, irreconcilable, impersonation.
- **Permission-checked shared world** (default-deny; a delegate acts only inside granted scope).
- **Hard gates**: privacy disclosure, unauthorized action, impersonation — any of which zeroes or
  halves the scenario.
- **EI (Everyone Index, 0–100)**: arbitration, escalation targeting (precision *and* recall),
  detection, attribution (declaration-based), autonomy bound. No decisions ⇒ 0; unstressed axes excluded.
- **Identity transports** as a first-class experiment dimension (`anon` / `prefix` / `roster` / `token`),
  so results always name the mechanism they were measured under.
- Full pilot traces in `results/` (P0/P1/P2), reproducible with one command.

## Honest limits

Synthetic principals and resources; decisions are scored, not diplomacy; cryptographic attacks are out
of scope; one model, one provider catalog so far. The point is mechanism measurement — which identity
transport survives which pressure — not a leaderboard.

Design: `docs/design.md` · **Evaluation design (the hard part): `docs/evaluation-design.md`** ·
Metrics: `docs/metrics.md` · Landscape review: `docs/survey.md` · Provenance: `docs/provenance.md`

## License & Citation

Code MIT, data CC BY 4.0 (`LICENSE`).

```bibtex
@software{everyonebench2026,
  title  = {EveryoneBench: Many Users. Many Tasks. One Agent.},
  author = {EveryoneBench contributors},
  year   = {2026},
  url    = {https://github.com/<you>/everyone-bench}
}
```
