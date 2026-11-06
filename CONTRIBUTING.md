# Contributing to EveryoneBench

EveryoneBench is small on purpose: a scenario is a JSON file, a decision is one of five types, and every
number in the paper can be rebuilt from files in this repository. Contributions are welcome in three
shapes — pick whichever matches what you have.

## 1. A new scenario (most useful)

A scenario is one file in `data/seeds/<type>_<n>.json` and describes a **world** plus the requests the
principals make in it. To propose one:

1. Read `data/seeds/privacy_boundary.json` — it is the shortest complete example.
2. Keep the world *small and checkable*: 2–4 principals (`frank`, `ivan`, …), explicit `policies`
   (default-deny), and requests that are decidable **without** knowing the model's mood.
3. Every request must have exactly one defensible answer among `act | propose | ask | refuse | defer`,
   plus the `acting_for` declaration it should carry. If two answers are both defensible, the scenario
   is under-specified — that is a bug in the scenario, not a hard question.
4. Include the `expected` block and run `python -m harness.cli selftest` — the oracle must score 100 and
   the silent agent 0. If the oracle fails, the scenario contradicts the rubric.
5. Open a PR with: the JSON file, one sentence on which real situation it comes from, and the selftest
   output pasted in the description.

## 2. A new decision rubric or metric

Rubric changes are the expensive kind: they invalidate published numbers. Open an **issue first** and
state (a) what the current rubric gets wrong, (b) which of the nine scenarios now score differently,
(c) whether existing traces in `results/` can be re-scored without new model calls. `docs/metrics.md`
and `docs/evaluation-design.md` are the specification; changes there need a matching re-score.

## 3. A new identity transport

Transports live in `harness/runner.py` (`TRANSPORTS`). A new one must be implementable *in the prompt
alone* (that is the point of the experiment: identity is not a native channel). Add the transport, run
the P2 matrix, and include the new traces — a transport without traces is a claim, not a result.

## Ground rules

- **No personal data.** Scenarios are fiction: names are invented, facts are synthetic. Do not paste
  real conversations, real customer data, or anything you would not publish.
- **No new runtime dependencies** in the harness (standard library only). Benchmark tooling that needs
  packages goes under `scripts/` and must degrade gracefully when they are missing.
- **Every number must be reproducible.** If you add a figure, add the artifact and the command that
  rebuilds it; `docs/numbers-provenance.md` is the index and `docs/provenance.md` explains the format.
- **Do not re-run the model to "fix" a number.** If an endpoint no longer serves a model id, say so
  (see the `†` rows in the README) rather than swapping in a different model silently.

## What to expect from review

Small scenario PRs usually get a yes/no within a few days. Rubric changes take longer, because they
need re-scoring. If a PR sits unanswered, ping it — that is not rude here.

## License

By contributing you agree that code is released under MIT (`LICENSE`) and scenario data / traces under
CC BY 4.0 (`DATA-LICENSE.md`).
