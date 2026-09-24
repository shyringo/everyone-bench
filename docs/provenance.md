# Provenance & Originality

## A. Project-specific original work

- **Decision-level multi-principal evaluation**: the protocol requires the agent to answer every
  request with exactly one typed decision (`act` / `propose` / `ask` / `refuse` / `defer`), making
  arbitration, escalation targeting, and boundary behavior deterministically scorable without
  LLM judges. To our knowledge no prior multi-user benchmark scores decisions at this level.
- **The 8-type open conflict registry** (resource contention, incompatible constraints, priority
  order, authority conflict, privacy boundary, delegation scope, identity confusion, irreconcilable)
  as a pluggable generator + ground-truth + verifier unit.
- **Scale & structure as experiment variables** (user count and relationship structure), plus the
  planned P2 suite: users × tasks (the intersection with MyriadBench).
- **Privacy/identity hard gates**: cross-principal disclosure zeroes a scenario; cross-talk is
  detected inside decision bodies, not only in prose.
- **The Everyone Index (EI)** with active-axis policy and anti-passivity rules (no decisions ⇒ 0;
  silence earns no axis credit).
- The harness implementation (world/permission model, runner, verifiers, metrics, CLI, tests).

## B. Adaptations of published ideas / formats (credited)

| idea | source | adaptation |
|---|---|---|
| multi-principal framework & capability axes | Multi-User LLM Agents (arXiv:2604.08567) | we adopt the problem framing and add scale/structure variables and decision-level scoring |
| governance harness concerns (permissions, conflict arbitration, non-disclosure) | Harness-MU (arXiv:2606.21856) | we implement them as benchmark mechanics rather than a system |
| multi-user conflict resolution in a domain | GroupTravelBench (arXiv:2605.25200) | domain-general, typed-decision protocol |
| principal loyalty | PrincipalBench / Whose Side (arXiv:2606.30383) | extended from 1 principal + 1 counterparty to N principals with relationship graphs |
| privacy / contextual integrity in multi-user systems | PiSAs (arXiv:2607.05318), MuPPET (arXiv:2606.23217), AgentSocialBench (arXiv:2604.01487) | privacy becomes a hard gate inside conflict scenarios |
| escalation/ask-when-uncertain | HiL-Bench (arXiv:2604.09408), AGENTASK (ACL 2026) | escalation target choice among multiple principals, precision/recall scored |
| instruction hierarchy conflicts | IH-Benchmark (arXiv:2607.25987) | user-vs-user conflicts instead of system-vs-user trust levels |
| role conflict / social mediation | RoleConflictBench (ACL 2026), SoCRATES (arXiv:2606.05563) | objective decision classes instead of subjective mediation quality |
| evaluation-suite conventions (index + active axes + anti-passivity + frozen suites) | MyriadBench (this project's sibling) | reused design pattern, not code |

## C. Reused code/data

None. No external code or data is vendored. The harness is original; the sibling project
(MyriadBench) shares design conventions only.

## D. What we are NOT claiming

- Not a social-intelligence or negotiation-quality benchmark (phrasing is not scored).
- Not a complete taxonomy of human conflict (8 registered types; open to extension).
- No model results yet: v0.1 publishes protocol + harness + seeds + self-test only.
