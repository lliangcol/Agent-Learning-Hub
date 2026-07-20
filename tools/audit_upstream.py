"""Clone the declared upstream into a temporary directory and write a read-only audit report."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).parents[1]
CONFIG = ROOT / "curriculum" / "upstream.yaml"
COMPARE_PATHS = ("README.md", "CONTRIBUTING.md", "LICENSE", ".gitignore", "index.html")
git_executable = shutil.which("git")
if git_executable is None:
    raise RuntimeError("git executable was not found")
GIT: str = git_executable


def run(*args: str, cwd: Path | None = None) -> str:
    # Arguments are passed as a list without a shell; the repository is declared in reviewed YAML.
    result = subprocess.run(  # noqa: S603
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    return result.stdout.strip()


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baseline_content(commit: str, name: str) -> bytes | None:
    result = subprocess.run(  # noqa: S603
        (GIT, "show", f"{commit}:{name}"),
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=20,
    )
    return result.stdout if result.returncode == 0 else None


def content_digest(content: bytes | None) -> str | None:
    return hashlib.sha256(content).hexdigest() if content is not None else None


def line_delta(before: bytes | None, after: bytes | None) -> str:
    before_lines = (before or b"").decode("utf-8", errors="replace").splitlines()
    after_lines = (after or b"").decode("utf-8", errors="replace").splitlines()
    added = removed = 0
    for tag, first_start, first_end, second_start, second_end in difflib.SequenceMatcher(
        None, before_lines, after_lines
    ).get_opcodes():
        if tag in {"replace", "delete"}:
            removed += first_end - first_start
        if tag in {"replace", "insert"}:
            added += second_end - second_start
    return f"+{added}/-{removed}"


def classify(name: str, local_hash: str | None, upstream_hash: str | None) -> str:
    if local_hash == upstream_hash:
        return "unchanged"
    if upstream_hash is None:
        return "local-only"
    if local_hash is None:
        return "upstream-only"
    if name in {"README.md", "index.html"}:
        return "needs-v2-mapping"
    return "local-conflict-review"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "reports" / "upstream-audit.md")
    args = parser.parse_args()
    config = cast(dict[str, Any], yaml.safe_load(CONFIG.read_text(encoding="utf-8")))
    repository = str(config["repository"])
    branch = str(config["default_branch"])

    with tempfile.TemporaryDirectory(prefix="alh-upstream-") as temporary:
        upstream = Path(temporary) / "upstream"
        run("git", "clone", "--quiet", "--branch", branch, repository, str(upstream))
        upstream_commit = run("git", "rev-parse", "HEAD", cwd=upstream)
        local_commit = run("git", "rev-parse", "HEAD", cwd=ROOT)
        baseline_available = (
            subprocess.run(  # noqa: S603
                (GIT, "cat-file", "-e", f"{local_commit}^{{commit}}"),
                cwd=upstream,
                capture_output=True,
                check=False,
                timeout=20,
            ).returncode
            == 0
        )
        if baseline_available:
            commit_log = run(
                "git",
                "log",
                "--format=%h %ad %s",
                "--date=short",
                f"{local_commit}..HEAD",
                cwd=upstream,
            )
            diff_stat = run("git", "diff", "--stat", f"{local_commit}..HEAD", cwd=upstream)
        else:
            commit_log = "Local baseline is not present in upstream history."
            diff_stat = "A history-based diff is unavailable; file hashes were compared."
        rows = []
        content_deltas: dict[str, list[str]] = {}
        for name in COMPARE_PATHS:
            baseline = baseline_content(local_commit, name)
            upstream_content = (
                (upstream / name).read_bytes() if (upstream / name).is_file() else None
            )
            baseline_hash = content_digest(baseline)
            local_hash = digest(ROOT / name)
            upstream_hash = content_digest(upstream_content)
            upstream_delta = "unchanged" if baseline_hash == upstream_hash else "changed"
            action = (
                "none"
                if upstream_delta == "unchanged"
                else classify(name, local_hash, upstream_hash)
            )
            rows.append((name, upstream_delta, line_delta(baseline, upstream_content), action))
            if upstream_delta == "changed":
                before_lines = (baseline or b"").decode("utf-8", errors="replace").splitlines()
                after_lines = (
                    (upstream_content or b"").decode("utf-8", errors="replace").splitlines()
                )
                content_deltas[name] = list(
                    difflib.unified_diff(
                        before_lines,
                        after_lines,
                        fromfile=f"baseline/{name}",
                        tofile=f"upstream/{name}",
                        lineterm="",
                        n=1,
                    )
                )

    generated = datetime.now(UTC).replace(microsecond=0).isoformat()
    lines = [
        "# Upstream audit report",
        "",
        f"- Generated: `{generated}`",
        f"- Local source commit: `{local_commit}`",
        f"- Upstream: [{config['name']}]({config['attribution_url']})",
        f"- Upstream commit: `{upstream_commit}`",
        "- Policy: report-only; this audit never merges, pushes, or opens issues.",
        "",
        "| Path | Upstream vs baseline | Line delta | V2 action |",
        "| --- | --- | ---: | --- |",
    ]
    actions = {
        "none": "none",
        "unchanged": "none",
        "local-only": "retain local V2 asset",
        "upstream-only": "review for relevance",
        "needs-v2-mapping": "map semantic changes into curriculum sources",
        "local-conflict-review": "manual content and license review",
    }
    lines.extend(
        f"| `{name}` | {upstream_delta} | {delta} | {actions[action]} |"
        for name, upstream_delta, delta, action in rows
    )
    lines.extend(
        [
            "",
            "## Upstream changes since local baseline",
            "",
            "```text",
            commit_log or "No upstream commits after the local baseline.",
            "```",
            "",
            "```text",
            diff_stat or "No file changes after the local baseline.",
            "```",
        ]
    )
    if content_deltas:
        lines.extend(["", "## Content delta requiring review"])
        for name, delta_lines in content_deltas.items():
            clean_delta_lines = ["" if line == " " else line for line in delta_lines]
            lines.extend(["", f"### `{name}`", "", "```diff", *clean_delta_lines, "```"])
    lines.extend(
        [
            "",
            "## Review boundary",
            "",
            "Absorbing content requires schema validation, attribution and license review.",
            "A maintainer must approve the PR. Add the remote only for interactive comparison:",
            "",
            "```powershell",
            "git remote add upstream https://github.com/datawhalechina/Agent-Learning-Hub.git",
            "git fetch --no-tags upstream main",
            "```",
            "",
            "The audit command itself does not change Git remotes or the working tree.",
        ]
    )
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
