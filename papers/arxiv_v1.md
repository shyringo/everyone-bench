# DissentBench: Many Users, Many Tasks, One Agent — Decision-Level Evaluation of Multi-Principal Conflict

> Draft skeleton for review. Status: protocol + harness complete; **no model results yet** (pilot pending authorization).

## Abstract (draft)

As AI converges toward one model serving a person's entire digital life, that model serves not one user but many principals — family, colleagues, clients, communities — whose instructions conflict. Current models are trained under a single-principal assumption; multi-principal behavior is untested. We introduce **DissentBench**, which measures the *decision* an agent makes under conflicting instructions: every request must be answered with exactly one typed decision — `act`, `propose`, `ask`, `refuse`, or `defer` — enabling deterministic scoring without LLM judges. DissentBench ships an open eight-type conflict taxonomy (resource contention, incompatible constraints, priority order, authority conflict, privacy boundary, delegation scope, identity confusion, irreconcilable demands), a permission-checked shared world, privacy and identity hard gates, and a single index (**DI**) whose axes are arbitration, escalation targeting, detection, identity fidelity and autonomy bounds. Where existing multi-user work covers 2–5 principals, DissentBench makes user count and relationship structure experiment variables, and its P2 suite measures the end-state intersection: many users × many tasks, one agent. v0.1 ships protocol, harness, seeds and an objective self-test (oracle 100.00, silent baseline 0.00); model pilots follow.

## 1. Introduction

- The end-state argument: one model, many principals (user₁ … user_∞).
- The single-principal training assumption and why it breaks under real social contact.
- Contributions: (i) typed decisions as the measurement interface; (ii) an open conflict registry; (iii) scale & structure as experiment variables; (iv) the users × tasks intersection (P2, with MyriadBench); (v) DI with anti-passivity rules and hard gates.

## 2. Related work

- Multi-user frameworks and benchmarks: Multi-User LLM Agents (2604.08567), Harness-MU (2606.21856), GroupTravelBench (2605.25200).
- Principal loyalty / multi-party agents: PrincipalBench (2606.30383), Manager Coercion (2607.15434).
- Instruction hierarchy, role and knowledge conflicts: IH-Benchmark (2607.25987), RoleConflictBench (ACL 2026), KC-Bench (2609.03588).
- Privacy in multi-user systems: PiSAs (2607.05318), MuPPET (2606.23217), AgentSocialBench (2604.01487), AIM (2609.12320).
- Escalation / asking: HiL-Bench (2604.09408), AGENTASK (ACL 2026).
- Social mediation: SoCRATES (2606.05563).
- Positioning: the three uncovered gaps (scale/structure; users × tasks; escalation as objective metric).

## 3. Protocol

- Principals, channels, shared world; permissions are default-deny; delegation scoped by grants.
- Decisions as tools; trace format; deterministic verification.
- The 8-type conflict registry (generator + ground truth + verifier per type).
- Suites: **P0** pairwise (shipped), **P1** crowd (8–64 principals, planned), **P2** crowd × tasks (with MyriadBench, planned).

## 4. Metrics

- DI definition and axes; active-axis policy (unstressed axes excluded); anti-passivity (no decisions ⇒ 0); privacy hard gate; other gate penalties. See `docs/metrics.md`.

## 5. Experiments (to fill after pilot)

- Models: OpenCode Go cheap tier (DeepSeek-V4-Flash, MiMo-V2.5), temperature 0; per-type DI and axes; gate failures; decision transcripts.
- Hypotheses to test: H1 silent-act is rare but over-escalation is common; H2 privacy gates fail rarely yet catastrophically; H3 identity cross-talk grows with user count; H4 authority boundaries are the weakest axis.
- Scale curves via P1/P2 once P0 is validated.

## 6. Limitations

- Synthetic principals and resources; decision classes do not score phrasing.
- Taxonomy covers eight registered types; unregistered conflicts out of scope by construction.
- No real-model results yet; P1/P2 are specified but not executed.

## 7. Reproducibility

Seed-0 scenarios in `data/seeds/`; `python -m harness.cli selftest`; three-command CLI; JSON traces per scenario.

## References (selected)

2604.08567 · 2606.21856 · 2605.25200 · 2606.30383 · 2607.15434 · 2607.25987 · 2609.03588 · 2606.05563 · 2607.05318 · 2606.23217 · 2604.01487 · 2609.12320 · 2604.09408 · RoleConflictBench (ACL 2026) · AGENTASK (ACL 2026)
