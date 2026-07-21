from __future__ import annotations

import argparse
import json
import re
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
            "勾选只表示 `concept_verified`，`complete` 仍需工作簿证据和 review。"
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
            title = render_inline_links(str(task["title"]))
            prerequisites = task["prerequisites"]
            resources = task["resources"]
            lines.extend(
                [
                    f'<li class="progress-item" id="{task_id.lower()}">',
                    f'<input type="checkbox" id="check-{task_id}" '
                    f'data-task-id="{task_id}" disabled>',
                    f'<label for="check-{task_id}"><code>{task_id}</code> {title}</label>',
                    '<details class="acceptance-details">',
                    "<summary>查看前置条件与验收</summary>",
                    "<dl>",
                    f"<dt>前置任务</dt><dd>{render_codes(prerequisites, empty='无')}</dd>",
                    f"<dt>学习成果</dt><dd>{render_items(task['learning_outcomes'])}</dd>",
                    f"<dt>Lab</dt><dd>{render_code_value(task['lab_path'], empty='无')}</dd>",
                    f"<dt>产出</dt><dd><code>{escape_html(str(task['artifact']))}</code></dd>",
                    f"<dt>Rubric</dt><dd>{render_items(task['rubric'])}</dd>",
                    f"<dt>验证命令</dt><dd>{render_codes(task['validation_commands'])}</dd>",
                    f"<dt>失败场景</dt><dd>{render_items(task['failure_cases'])}</dd>",
                    f"<dt>安全说明</dt><dd>{render_items(task['safety_notes'])}</dd>",
                    f"<dt>资源</dt><dd>{render_resource_links(resources)}</dd>",
                    "</dl>",
                    "</details>",
                    "</li>",
                ]
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
        lines.extend(
            [
                f'<li class="progress-item" id="{project_id.lower()}">',
                f'<input type="checkbox" id="check-{project_id}" '
                f'data-project-id="{project_id}" disabled>',
                f'<label for="check-{project_id}"><code>{project_id}</code> '
                f"{escape_html(str(project['title']))} · "
                f"{escape_html(str(project['track']))}</label>",
                '<details class="acceptance-details">',
                "<summary>查看前置条件与验收</summary>",
                "<dl>",
                f"<dt>难度</dt><dd>{escape_html(str(project['difficulty']))}</dd>",
                "<dt>前置任务</dt><dd>"
                f"{render_codes(project['prerequisite_task_ids'], empty='无')}</dd>",
                f"<dt>产出</dt><dd><code>{escape_html(str(project['artifact']))}</code></dd>",
                f"<dt>Rubric</dt><dd>{render_items(project['rubric'])}</dd>",
                f"<dt>验证命令</dt><dd>{render_codes(project['validation_commands'])}</dd>",
                f"<dt>安全说明</dt><dd>{render_items(project['safety_notes'])}</dd>",
                f"<dt>预计投入</dt><dd>{escape_html(str(project['estimated_effort']))}</dd>",
                "</dl>",
                "</details>",
                "</li>",
            ]
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


_INLINE_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def render_inline_links(text: str) -> str:
    parts: list[str] = []
    cursor = 0
    for match in _INLINE_LINK.finditer(text):
        parts.append(escape_html(text[cursor : match.start()]))
        label, url = match.groups()
        parts.append(f'<a href="{escape_html(url)}">{escape_html(label)}</a>')
        cursor = match.end()
    parts.append(escape_html(text[cursor:]))
    return "".join(parts)


def render_items(items: list[object]) -> str:
    return "<ul>" + "".join(f"<li>{escape_html(str(item))}</li>" for item in items) + "</ul>"


def render_codes(items: list[object], *, empty: str = "无") -> str:
    if not items:
        return escape_html(empty)
    return "<br>".join(f"<code>{escape_html(str(item))}</code>" for item in items)


def render_code_value(value: object, *, empty: str) -> str:
    if value is None:
        return escape_html(empty)
    return f"<code>{escape_html(str(value))}</code>"


def render_resource_links(resources: list[object]) -> str:
    if not resources:
        return "无"
    return ", ".join(
        f'<a href="../resources/#{escape_html(str(resource).lower())}">'
        f"<code>{escape_html(str(resource))}</code></a>"
        for resource in resources
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
