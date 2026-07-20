"""Validate the required Stage 1-9 Lab topology and README contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
LABS = ROOT / "labs"
REQUIRED_ENTRIES = {"README.md", "starter", "solution", "tests", "fixtures", "expected"}
REQUIRED_SECTIONS = {
    "## 目标",
    "## 前置条件",
    "## 运行命令",
    "## 预期输出",
    "## 失败场景",
    "## 安全限制",
    "## 完成标准",
    "## 扩展任务",
}


def main() -> None:
    expected = {f"stage-{index:02d}" for index in range(1, 10)}
    lab_dirs = {path.name[:8]: path for path in LABS.glob("stage-??-*") if path.is_dir()}
    if set(lab_dirs) != expected:
        raise SystemExit(f"Stage Lab set mismatch: {sorted(lab_dirs)}")
    for stage_id, lab in sorted(lab_dirs.items()):
        names = {path.name for path in lab.iterdir()}
        missing_entries = REQUIRED_ENTRIES - names
        if missing_entries:
            raise SystemExit(f"{stage_id}: missing entries {sorted(missing_entries)}")
        for directory in REQUIRED_ENTRIES - {"README.md"}:
            if not any((lab / directory).iterdir()):
                raise SystemExit(f"{stage_id}: {directory} must not be empty")
        readme = (lab / "README.md").read_text(encoding="utf-8")
        missing_sections = REQUIRED_SECTIONS - set(readme.splitlines())
        if missing_sections:
            raise SystemExit(f"{stage_id}: missing README sections {sorted(missing_sections)}")

    cases = json.loads(
        (LABS / "stage-05-harness-and-evals" / "fixtures" / "eval-cases.json").read_text(
            encoding="utf-8"
        )
    )
    if len(cases) < 20:
        raise SystemExit("Stage 05 requires at least 20 fixed eval cases")
    required_paths = [
        LABS / "stage-06-skills-and-protocols" / "solution" / "mcp_server.py",
        LABS / "stage-06-skills-and-protocols" / "solution" / "research-brief" / "SKILL.md",
        ROOT / "tests" / "e2e" / "browser-lab.spec.js",
        LABS / "stage-09-capstone" / "solution" / "templates" / "RELEASE_CHECKLIST.md",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required_paths if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required Lab evidence: {missing}")
    print("Lab validation passed: Stage 1-9 topology, README contracts, and baseline evidence.")


if __name__ == "__main__":
    main()
