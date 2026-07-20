from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).parents[1]
GENERATED = ROOT / "site" / "generated"


def load(name: str) -> dict[str, Any]:
    value = yaml.safe_load((ROOT / "curriculum" / name).read_text(encoding="utf-8"))
    return cast(dict[str, Any], value)


def render_roadmap(roadmap: dict[str, Any]) -> str:
    lines = [
        "---",
        "title: 课程路线",
        "description: Stage 0-9 课程任务、前置条件与验收入口",
        "---",
        "",
        "# 课程路线",
        "",
        '<p data-progress-summary role="status" aria-live="polite">课程进度正在加载…</p>',
        "",
        (
            "课程任务与可选项目分别统计。复选框只记录本地学习状态；"
            "`complete` 仍需工作簿证据和 review。"
        ),
        "",
    ]
    for stage in roadmap["stages"]:
        stage_id = stage["id"]
        lines.extend(
            [
                f"## {stage_id} {stage['title']} {{ #{stage_id.lower()} }}",
                "",
                stage["description"],
                "",
                '<ul class="task-list">',
            ]
        )
        for task in stage["tasks"]:
            task_id = task["id"]
            title = escape_html(str(task["title"]))
            lines.append(
                f'<li class="progress-item" id="{task_id.lower()}">'
                f'<input type="checkbox" id="check-{task_id}" data-task-id="{task_id}" disabled>'
                f'<label for="check-{task_id}"><code>{task_id}</code> {title}</label></li>'
            )
        lines.extend(["</ul>", ""])
    return "\n".join(lines)


def render_projects(projects: dict[str, Any]) -> str:
    lines = [
        "---",
        "title: 项目阶梯",
        "description: 可选项目与独立进度",
        "---",
        "",
        "# 项目阶梯",
        "",
        '<p data-progress-summary role="status" aria-live="polite">项目进度正在加载…</p>',
        "",
        '<ul class="project-list">',
    ]
    for project in projects["projects"]:
        project_id = project["id"]
        lines.append(
            f'<li class="progress-item" id="{project_id.lower()}">'
            f'<input type="checkbox" id="check-{project_id}" '
            f'data-project-id="{project_id}" disabled>'
            f'<label for="check-{project_id}"><code>{project_id}</code> '
            f"{escape_html(str(project['title']))} · "
            f"{escape_html(str(project['track']))}</label></li>"
        )
    lines.extend(["</ul>", "", "项目全部可选，不计入课程任务总完成率。", ""])
    return "\n".join(lines)


def render_resources(resources: dict[str, Any]) -> str:
    lines = [
        "---",
        "title: 资源目录",
        "description: 带来源、状态和复核时间的学习资源",
        "---",
        "",
        "# 资源目录",
        "",
        "`suspect` 表示尚未完成本轮外链复核，不代表内容被推荐为当前事实。",
        "",
        "| ID | 资源 | Stage | 状态 | 最后验证 | 学习价值 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for resource in resources["resources"]:
        verified = resource["last_verified_at"] or "待复核"
        stages = ", ".join(resource["stage_ids"])
        title = str(resource["title"]).replace("|", "\\|")
        why = str(resource["why_it_matters"]).replace("|", "\\|")
        lines.append(
            f'| <span id="{str(resource["id"]).lower()}"></span>`{resource["id"]}` | '
            f"[{title}]({resource['url']}) | {stages} | "
            f"{resource['status']} | {verified} | {why} |"
        )
    return "\n".join(lines) + "\n"


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def generated_outputs() -> dict[Path, str]:
    roadmap = load("roadmap.yaml")
    projects = load("projects.yaml")
    resources = load("resources.yaml")
    migration = load("migrations/v1-to-v2.yaml")
    outputs = {
        GENERATED / "roadmap.md": render_roadmap(roadmap),
        GENERATED / "projects.md": render_projects(projects),
        GENERATED / "resources.md": render_resources(resources),
        GENERATED / "data" / "roadmap.json": json.dumps(roadmap, ensure_ascii=False, indent=2)
        + "\n",
        GENERATED / "data" / "projects.json": json.dumps(projects, ensure_ascii=False, indent=2)
        + "\n",
        GENERATED / "data" / "v1-to-v2.json": json.dumps(migration, ensure_ascii=False, indent=2)
        + "\n",
    }
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failed = []
    for path, content in generated_outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                failed.append(path)
        else:
            if path.exists() and path.read_text(encoding="utf-8") == content:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if failed:
        for path in failed:
            print(f"out of date: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    print("Site content is up to date." if args.check else "Site content generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
