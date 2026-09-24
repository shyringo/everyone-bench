# EveryoneBench: Many Users, Many Tasks, One Agent — Measuring Multi-Principal Competence and the Reliability of Identity Transports

> Draft v0.9 (review-ready). All numbers below are real DeepSeek-V4-Flash traces (temperature 0), released with the repository.

## Abstract

As AI converges toward one model serving a person's entire digital life, that model serves not one user
but many principals — user₁ … user_∞ — taking turns inside a single context. Their instructions conflict,
their permissions differ, and their private facts must not cross. Yet a model never sees "users": it sees
tokens, and in mainstream templates every speaker is `user`. Identity is therefore not a native channel but
something that must be *transported* — and every transport has logical holes. We introduce **EveryoneBench**,
which measures the *decision* an agent makes under multi-principal pressure: each request must be answered
with exactly one typed decision (`act`, `propose`, `ask`, `refuse`, `defer`) that must also **declare whom
the agent believes it is serving** (`acting_for`). The declaration makes attribution objectively measurable
and turns impersonation into a scored failure rather than a matter of prose. EveryoneBench ships an
eight-type conflict registry plus an impersonation scenario, a permission-checked shared world with
default-deny delegation, privacy/authority/impersonation hard gates, the **Everyone Index (EI)**, and
**identity transports as a first-class experimental dimension** (`anon` / `prefix` / `roster` / `token`).
In a real-model pilot (DeepSeek-V4-Flash), pairwise conflict handling reaches EI 66.9 but collapses to
16.1–19.2 when 8–32 principals interleave; adding any identity signal lifts attribution from 0.00 to
0.89–0.94; and **every text-based mechanism accepts a forged identity, while only the token mechanism —
which requires verification rather than reading — refuses it.** Text prefixes are a formatting convention,
not an identity architecture.

## 1. Introduction

- The end-state argument: one model, many principals, one context.
- The token-level reality: one `user` role ⇒ identity must be transported.
- Contributions: (i) typed decisions with an `acting_for` obligation; (ii) an open conflict registry
  including impersonation; (iii) identity transports as a measured dimension; (iv) the EI index with
  anti-passivity and hard gates; (v) a real-model pilot showing scale collapse and the forgeability of
  text-based identity.

## 2. Related work

Multi-user frameworks and benchmarks (Multi-User LLM Agents 2604.08567, Harness-MU 2606.21856,
GroupTravelBench 2605.25200); principal loyalty (PrincipalBench 2606.30383, Manager Coercion 2607.15434);
instruction hierarchy / role / knowledge conflicts (IH-Benchmark 2607.25987, RoleConflictBench ACL 2026,
KC-Bench 2609.03588); privacy in multi-user systems (PiSAs 2607.05318, MuPPET 2606.23217,
AgentSocialBench 2604.01487, AIM 2609.12320); escalation (HiL-Bench 2604.09408, AGENTASK ACL 2026);
identity persistence (PAI-Bench 2609.13637); social mediation (SoCRATES 2606.05563).

Positioning: prior work covers multi-user *capabilities*, single-domain conflict resolution, privacy, and
loyalty — but (a) keeps principal counts small, (b) does not treat the identity-transport mechanism itself
as the variable, and (c) does not score impersonation resistance. EveryoneBench targets exactly those.

## 3. Protocol

- Principals, channels, shared world; default-deny permissions; delegation scoped by grants.
- Decisions as typed tools; each carries `acting_for` (the attribution declaration).
- Conflict registry (8 types + impersonation) as generator + ground truth + verifier.
- Suites: **P0** pairwise (8 types), **P1** crowd (N principals interleaving), **P2** identity-transport
  matrix (same scenarios × `anon`/`prefix`/`roster`/`token`).

## 4. Metrics

EI = weighted mean over active axes: arbitration 0.30, escalation 0.25 (precision and recall),
detection 0.20, attribution 0.15 (declaration-based; a missing declaration is an attribution error),
autonomy 0.10. Anti-passivity: no decisions ⇒ 0. Hard gates: privacy disclosure ⇒ 0; unauthorized action,
impersonation, unilateral writes, unprotected deadlines ⇒ halved. See `docs/metrics.md`.

## 5. Experiments — DeepSeek-V4-Flash (OpenCode Go, temperature 0)

### 5.1 Conflict handling and the cost of scale

| suite | setting | EI |
|---|---|---|
| P0 | 8 conflict types, 2 principals | **66.9** |
| P1 | 8 principals interleaving | **16.1** |
| P1 | 32 principals interleaving | **19.2** |

Per-type EI (P0): privacy boundary 100, delegation scope 100, priority order 86.7, irreconcilable 66.7,
incompatible constraints 66.7, resource contention 50.0, authority conflict 35.0, **identity confusion 30.0**.

Reading: the model respects *hard boundaries it can see* (privacy, delegated scope) but fails at
*attribution under load* (identity confusion) and at *authority reasoning* — and the failure becomes
catastrophic once many principals interleave in one context.

### 5.2 Identity transports (same scenarios, same ground truth)

| transport | EI | attribution axis | impersonation attempt |
|---|---|---|---|
| `anon` | 48.2 | **0.00** | acted on the forged identity |
| `prefix` | **68.1** | 0.94 | acted on the forged identity |
| `roster` | 61.7 | 0.89 | acted on the forged identity |
| `token` | 63.8 | 0.89 | **refused** |

Three findings:
1. **No signal, no attribution.** With bare `user` messages the model cannot attribute at all (axis 0.00);
   adding any signal lifts it to 0.89–0.94.
2. **More structure is not automatically better.** A published roster scored below a plain text prefix
   (61.7 vs 68.1): longer context did not improve decisions.
3. **Text identity is forgeable; verification is not.** Under `anon`, `prefix`, and `roster`, a member who
   claimed to be another principal was *acted for*; only the token transport — where the credential must be
   checked, not read — refused. This is the paper's central empirical claim: current practice relies on
   formatting, not authentication.

### 5.3 Cost

≈ 90 model calls for P0+P1+P2 (single model), well under $1 at OpenCode Go rates. All traces in `results/`.

## 6. Limitations

Synthetic principals/resources; decisions scored, not diplomacy; text-level impersonation only
(cryptography out of scope); one model and one provider catalog so far; P1 beyond 128 principals and the
P3 users × tasks suite (with MyriadBench) remain to be run.

## 7. Reproducibility

`python -m harness.cli selftest` (oracle 100.00 / silent 0.00) · `scripts/run_pilot.py --suite P0|P1|P2` ·
seed-0 scenarios in `data/seeds/` · JSON traces per (scenario, transport).

## References (selected)

2604.08567 · 2606.21856 · 2605.25200 · 2606.30383 · 2607.15434 · 2607.25987 · 2609.03588 · 2606.05563 ·
2607.05318 · 2606.23217 · 2604.01487 · 2609.12320 · 2604.09408 · 2609.13637 · RoleConflictBench (ACL 2026) · AGENTASK (ACL 2026)
