from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).parents[1]


def load(name: str) -> dict[str, Any]:
    value = yaml.safe_load((ROOT / "curriculum" / name).read_text(encoding="utf-8"))
    return cast(dict[str, Any], value)


def render() -> str:
    roadmap = load("roadmap.yaml")
    projects = load("projects.yaml")
    resources = load("resources.yaml")
    lines = [
        "# Agent Learning Hub",
        "",
        "> 一个离线优先、可验证、可迁移的 AI Agent 学习实验室。",
        "",
        "## 快速开始",
        "",
        "Python 3.11+；推荐使用 uv。核心路径不需要 API key。",
        "",
        "```powershell",
        "uv sync --all-extras --dev --locked",
        "uv run pytest",
        "uv run python tools/validate_content.py",
        "npm ci",
        "npm run build",
        "uv run mkdocs serve",
        "```",
        "",
        "使用标准 venv：",
        "",
        "```powershell",
        "python -m venv .venv",
        '.venv\\Scripts\\python -m pip install -e ".[dev,site,protocol]"',
        ".venv\\Scripts\\python -m pytest",
        "```",
        "",
        "真实 OpenAI Provider 是可选扩展。复制 `.env.example` 的变量名到本地环境；不要提交密钥。",
        "",
        "## 课程路线",
        "",
        f"Roadmap version: `{roadmap['roadmap_version']}`。个人进度不写回本列表。",
        "",
        "| 阶段 | 主题 | 任务数 | 正文 |",
        "| --- | --- | ---: | --- |",
    ]
    stage_files = sorted((ROOT / "curriculum" / "stages").glob("stage-*.md"))
    for stage, path in zip(roadmap["stages"], stage_files, strict=True):
        relative = path.relative_to(ROOT).as_posix()
        task_count = len(stage["tasks"])
        lines.append(
            f"| `{stage['id']}` | {stage['title']} | {task_count} | [{path.stem}]({relative}) |"
        )
    lines.extend(
        [
            "",
            "## Project Ladder",
            "",
            "项目进度与课程进度分开统计；所有项目均为可选。",
            "",
            "| ID | 项目 | 轨道 | 难度 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for project in projects["projects"]:
        project_id = project["id"]
        title = project["title"]
        track = project["track"]
        difficulty = project["difficulty"]
        lines.append(f"| `{project_id}` | {title} | {track} | {difficulty} |")
    active = sum(item["status"] == "active" for item in resources["resources"])
    suspect = sum(item["status"] == "suspect" for item in resources["resources"])
    lines.extend(
        [
            "",
            "## 事实源与个人数据",
            "",
            "- `curriculum/roadmap.yaml`、`projects.yaml`、`resources.yaml` 是唯一结构化事实源。",
            "- `workbook/local/`、浏览器笔记、导出进度和 SQLite 记忆默认不进入 Git。",
            "- V1 资产与迁移证据保存在 `workbook/archive/legacy-v1/`。",
            f"- 资源目录当前有 {active} 个 active、{suspect} 个待外链复核项；状态不会被隐藏。",
            "",
            "## 质量与安全",
            "",
            "- 默认 Labs 离线运行，不执行任意不可信代码。",
            "- 普通子进程不被称为沙箱；详见 `SECURITY.md` 与 ADR-0005。",
            "- CI 验证 Python、内容、前端、MkDocs、链接与浏览器核心路径。",
            "",
            "## 贡献与上游",
            "",
            "参见 [CONTRIBUTING.md](CONTRIBUTING.md)。项目保留 Datawhale 上游、原维护者及",
            "外部贡献者署名；上游同步只生成差异报告，不自动合并。",
            "",
            "## Maintainer",
            "",
            "Curated by [陈思州](https://github.com/jjyaoao), Datawhale member。",
            "",
            "## License",
            "",
            "MIT。外部链接内容仍受各自许可证和访问条款约束。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = render()
    path = ROOT / "README.md"
    if args.check:
        if path.read_text(encoding="utf-8") != output:
            print("README.md is out of date; run tools/build_readme.py", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0
    path.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
