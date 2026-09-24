"""Assemble a clean public release repository for EveryoneBench.

    python scripts/make_release.py [--dest D:/Projects_PyCharm/everyone-bench-release]

Never deletes anything: if the destination exists, a numeric suffix is used.
Excludes: internal notes, results (shipped as release assets), papers (until submission),
generated data, caches.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["README.md", "LICENSE", ".gitignore"]
DIRS = ["data", "docs", "harness", "tests", "scripts"]
EXCLUDE_FILES = {"docs/release-checklist.md"}
EXCLUDE_DIRS = {"__pycache__", ".git", "results", "data/generated", "data/pilot", "papers"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default="D:/Projects_PyCharm/everyone-bench-release")
    args = ap.parse_args()

    dest = args.dest
    n = 2
    while os.path.exists(dest):
        dest = f"{args.dest}-{n}"
        n += 1
    os.makedirs(dest)

    def excluded(frel: str) -> bool:
        if frel in EXCLUDE_FILES:
            return True
        if "/__pycache__/" in "/" + frel:
            return True
        return any(frel.startswith(e) for e in EXCLUDE_DIRS)

    copied = []
    for name in FILES:
        src = os.path.join(SRC, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest, name))
            copied.append(name)
    for name in DIRS:
        src = os.path.join(SRC, name)
        if not os.path.exists(src):
            continue
        for dirpath, dirnames, filenames in os.walk(src):
            rel = os.path.relpath(dirpath, SRC).replace(os.sep, "/")
            dirnames[:] = [d for d in dirnames
                           if d != "__pycache__"
                           and not any((rel + "/" + d).startswith(e) for e in EXCLUDE_DIRS)]
            for fn in filenames:
                frel = (rel + "/" + fn) if rel != "." else fn
                if excluded(frel):
                    continue
                os.makedirs(os.path.join(dest, rel), exist_ok=True)
                shutil.copy2(os.path.join(dirpath, fn), os.path.join(dest, rel, fn))
                copied.append(frel)

    subprocess.run(["git", "init", "-b", "main"], cwd=dest, check=True, capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True, capture_output=True)
    subprocess.run(["git", "-c", "user.name=shy", "-c", "user.email=shyringo@163.com",
                    "commit", "-m",
                    "EveryoneBench v0.1: multi-principal conflict benchmark with identity transports"],
                   cwd=dest, check=True, capture_output=True)
    print(f"release repo -> {dest} ({len(copied)} files)")
    print("next: gh repo create everyone-bench --public --source . --remote origin --push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
