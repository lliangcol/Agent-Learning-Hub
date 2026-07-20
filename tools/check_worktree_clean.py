from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        print(completed.stderr.strip() or "git status failed")
        return completed.returncode
    if completed.stdout:
        print("Generated checks left the worktree dirty:")
        print(completed.stdout, end="")
        return 1
    print("Worktree is clean after generated checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
