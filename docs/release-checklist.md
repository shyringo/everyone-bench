# EveryoneBench — release checklist (internal)

## Before publishing

> 自检回填：2026-11-04，Python 3.10.20，`D:/Projects_PyCharm/everyone-bench`。下面每条后面的 `2026-11-04` 行是实跑摘要。

- [x] `python -m unittest discover -s tests` → 16 tests OK
      `2026-11-04`: `Ran 16 tests in 0.010s` / `OK`；源仓库与发布树（`everyone-bench-release-2`）各跑一次，均 OK。
- [x] `python -m harness.cli selftest` → oracle 100.00 / silent 0.00 on all 9 scenarios
      `2026-11-04`: 9/9 行全为 `OK ... oracle=100.00 silent=  0.00`，末行 `selftest: PASS`；源仓库与发布树各一次。
- [ ] README numbers re-checked against `results/summary-*.json` (never hand-written) —— **⚠ 部分通过：P2 全通过；P0 靠固定评分器版本可复现；P1 两档待补（2026-11-04 M64 复核）**
      · 逐数字来源表：`docs/numbers-provenance.md`（38 行，一行一个数字）；机器可复核：`results/provenance-checks.json`。
      · **P2 矩阵：通过。** README 的 48.2 / 68.1 / 61.7 / 63.8 与 identity 0.00 / 0.94 / 0.89 / 0.89，
        与 `results/summary-P2-deepseek-v4-flash.json`（48.15 / 68.10 / 61.67 / 63.75；0.0 / 0.9444 / 0.8889 / 0.8889）逐项吻合；
        “acted on the forged identity” ×3 与“token refused”也在 `results/impersonation_1-*-{anon,prefix,roster,token}.trace.json` 里逐条对上。
      · **P0 headline 66.9 + 逐类表：可复现，但绑定评分器版本。** 用冻结 trace（`results/*_1-deepseek-v4-flash.trace.json`，2026-09-16 实跑）
        配 `git show 0c4f0ee:harness/metrics.py`（v0.1 评分器，那批 trace 就是它打的分）重打分 → **66.88**，
        逐类 100 / 100 / 86.67 / 66.67 / 66.67 / 50.0 / 35.0 / 30.0，与 README 逐项吻合；产物 `results/summary-P0-deepseek-v4-flash.json`。
        换成现行评分器重打同一批 trace 是 50.0（评分器 09-24 重写过），两者不可混用。
      · **P1 两档 16.1 / 19.2：待补。** 没有任何产物落盘单档 EI，只有 `results/summary-deepseek-v4-flash.json` 的聚合
        EI 17.62（2 个场景）。README 已改为报聚合 17.6 并挂 † 脚注，不再声称单档数字。
        补的办法是重跑 pilot，但 `deepseek-v4-flash` 已下线（API 400 `Model is unavailable`），本机只剩 `deepseek-v4.1-flash`（换模型＝改结论，不能私自换）。
      · **另记两条待补（不算 README 数字，但挡发布）：** ① `scripts/run_pilot.py` 仍写 `summary-{model}.json`，同名覆盖是这次事故根因，
        应改成 `summary-{suite}-{model}.json`；② `docs/evaluation-design.md`（104–124 行）、`papers/arxiv_v1.md`（19–20/68–70/83–84 行）
        仍带 66.9 / 16.1 / 19.2，`docs/README-zh.md` 更旧（“13 tests”“尚无真实模型数据”），需同步或撤稿。
      · 补的一步（不阻塞其它条）：等所用模型可用后重跑 P0/P1，用新产物替换 `results/summary-P0-deepseek-v4-flash.json` 的 v0.1 绑定，并删掉 README 的 † 脚注。
- [ ] no internal notes in the public tree (`docs/release-checklist.md` excluded by the assembler)
      `2026-11-04` 粗核：发布树 27 个文件里没有 `docs/release-checklist.md`、没有 `papers/`、没有 `results/`、没有 `__pycache__`（仍留人工复核）。
      本轮新增 `docs/numbers-provenance.md`（应随发布树走，发布树将变 28 个文件，需重跑 `make_release.py`）。
- [x] `python scripts/make_release.py` → clean repo assembled, single commit
      `2026-11-04`: `release repo -> D:/Projects_PyCharm/everyone-bench-release-2 (27 files)`。
      目标 `everyone-bench-release` 已被 09-24 那次占用，脚本按设计自动加序号、未覆盖未删除；
      新库单提交 `7963633 EveryoneBench v0.1: multi-principal conflict benchmark with identity transports`，`git status` 干净。

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
- [ ] arXiv: 确认旧账号可用（凭据由 Huan-Yi 本人处理，不写入仓库）
