# EveryoneBench — release checklist (internal)

## Before publishing

- [ ] `python -m unittest discover -s tests` → 16 tests OK
- [ ] `python -m harness.cli selftest` → oracle 100.00 / silent 0.00 on all 9 scenarios
- [ ] README numbers re-checked against `results/summary-*.json` (never hand-written)
- [ ] no internal notes in the public tree (`docs/release-checklist.md` excluded by the assembler)
- [ ] `python scripts/make_release.py` → clean repo assembled, single commit

## GitHub metadata

- [ ] repo name: `everyone-bench`
- [ ] description (EN first line, CN second):
      `Many users, many tasks, one agent. Measures whether a model can tell its principals apart:
       identity transports, conflict decisions, impersonation. Real pilot traces included. | 一个模型、
       许多用户、无数任务:它能否分清谁在说话?身份传递机制 × 冲突决策 × 冒充抵抗,含真实 pilot 数据。`
- [ ] topics: `llm-evaluation`, `benchmark`, `llm-agents`, `multi-user`, `identity`, `agents`,
      `evaluation`, `privacy`
- [ ] social preview: a 1280×640 card (build with the campaign art script pattern)
- [ ] landing page (optional): same structure as MyriadBench's `docs/index.html`

## Release assets

- [ ] zip `results/` (all traces for P0/P1/P2) and attach to the GitHub release
- [ ] release notes: state the three headline findings (scale collapse; attribution 0.00 → 0.94;
      text identity forgeable, only token verification refused the impersonation)

## Promotion (after the user approves)

- [ ] the same platform set prepared for MyriadBench (X / HN / Reddit / LinkedIn / 知乎 / 掘金 / 微博)
- [ ] one credible community-native post first; do not cross-post identical text
- [ ] disclose authorship; never request stars/votes

## Open items for the user

- [ ] review `papers/arxiv_v1.md` (v0.9 with real data) and `docs/evaluation-design.md`
- [ ] decide whether to run the wider matrix (P1 at 128/1024 principals; a second model)
- [ ] arXiv: confirm the old account (login/password reset with the NJU or 163 mailbox)
