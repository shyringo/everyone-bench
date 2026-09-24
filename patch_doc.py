"""Append the empirical preview to docs/evaluation-design.md (idempotent)."""
import io

p = "docs/evaluation-design.md"
t = io.open(p, encoding="utf-8").read()
if "Empirical preview" not in t:
    t += """

## 7. Empirical preview (DeepSeek-V4-Flash, real traces)

The design above was executed on the shipped suites. Results (`results/`, temperature 0):

| transport | EI | attribution axis | impersonation attempt |
|---|---|---|---|
| `anon` | 48.2 | **0.00** | acted on the forged identity |
| `prefix` | 68.1 | 0.94 | acted on the forged identity |
| `roster` | 61.7 | 0.89 | acted on the forged identity |
| `token` | 63.8 | 0.89 | **refused** |

And on scale (pairwise → crowd, `prefix`):

| setting | EI |
|---|---|
| 2 principals, 8 conflict types | 66.9 |
| 8 principals interleaving | 16.1 |
| 32 principals interleaving | 19.2 |

What the numbers say about the design question:

1. **Attribution is measurable and it moves.** The `acting_for` declaration converts "did the model know
   who was speaking" into a number: 0.00 without any identity signal, 0.89–0.94 with one.
2. **Reading identity is not verifying it.** All three text-based transports were fooled by a forged
   identity; only the mechanism that requires checking a credential refused. This is the concrete
   justification for treating identity transports as architecture rather than formatting.
3. **Scale is the real stress.** Pairwise conflict handling is mediocre (66.9); with 8–32 principals
   interleaving it collapses (16–19). Whatever the mechanism, principal count must be a reported axis —
   a single "multi-user score" hides the failure mode that matters.
4. **More context is not more safety.** The roster transport scored *below* the plain prefix, i.e. extra
   structure consumed attention without improving decisions.

These are single-model results and are labelled as such; the protocol is model-agnostic and the same
matrix is intended for every model added.
"""
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print("evaluation-design.md: empirical preview appended")
else:
    print("already present")
