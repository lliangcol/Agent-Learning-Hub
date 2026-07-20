"""One-time, auditable migration from the preserved V1 README structure."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).parents[1]
STAGE_TITLES = {
    "S00": "Agent 适用性与边界",
    "S01": "LLM API 与结构化契约",
    "S02": "Agent Loop 与工具调用",
    "S03": "RAG、上下文与记忆",
    "S04": "可靠性、权限与安全",
    "S05": "Harness、Trace 与 Evals",
    "S06": "Skills 与协议",
    "S07": "Browser 与 Computer Use",
    "S08": "Multi-Agent 协调",
    "S09": "Capstone",
}
OLD_TO_NEW: dict[tuple[int, int], str] = {
    **{(0, index): f"S00-T{index:02d}" for index in range(1, 6)},
    **{(1, index): f"S01-T{index:02d}" for index in range(1, 4)},
    **{(1, index): f"S02-T{index - 3:02d}" for index in range(4, 7)},
    (2, 1): "S03-T01",
    (2, 2): "S04-T01",
    (2, 3): "S03-T02",
    (2, 4): "S04-T02",
    (2, 5): "S03-T03",
    **{(3, index): f"S05-T{index:02d}" for index in range(1, 6)},
    **{(4, index): f"S08-T{index:02d}" for index in range(1, 6)},
    **{(5, index): f"S06-T{index:02d}" for index in range(1, 9)},
    **{(6, index): f"S07-T{index:02d}" for index in range(1, 6)},
    **{(7, index): f"S04-T{index + 2:02d}" for index in range(1, 7)},
    **{(8, index): f"S09-T{index:02d}" for index in range(1, 6)},
}
PROJECT_TRACKS = [
    "基础工具",
    "研究与 RAG",
    "研究与 RAG",
    "Coding Agent",
    "Browser 与 Computer Use",
    "Coding Agent",
    "Personal Agent",
    "Skills 与协议",
    "Multi-Agent",
    "Personal Agent",
    "Production Harness",
]


def parse_tasks(text: str) -> list[dict[str, object]]:
    tasks: list[dict[str, object]] = []
    stage: int | None = None
    per_stage = 0
    for line in text.splitlines():
        heading = re.match(r"### Stage (\d+):", line)
        if heading:
            stage = int(heading.group(1))
            per_stage = 0
            continue
        match = re.match(r"- \[([ xX])] (.+)", line)
        if match and stage is not None:
            per_stage += 1
            old_id = f"V1-S{stage}-T{per_stage:02d}"
            new_id = OLD_TO_NEW[(stage, per_stage)]
            tasks.append(
                {
                    "old_id": old_id,
                    "new_id": new_id,
                    "title": match.group(2).rstrip("。"),
                    "checked": match.group(1).lower() == "x",
                }
            )
    if len(tasks) != 50:
        raise ValueError(f"expected 50 V1 tasks, found {len(tasks)}")
    return tasks


def infer_stages(title: str, description: str) -> list[str]:
    value = f"{title} {description}".casefold()
    stages = []
    for keywords, stage in [
        (("rag", "retriev", "检索", "memory", "记忆"), "S03"),
        (("skill", "mcp", "protocol", "协议"), "S06"),
        (("browser", "computer", "webarena", "浏览器", "桌面"), "S07"),
        (("multi-agent", "subagent", "a2a", "多 agent", "多智能体"), "S08"),
        (("eval", "trace", "harness", "benchmark"), "S05"),
        (("security", "safety", "权限", "安全", "tool use", "function calling"), "S04"),
    ]:
        if any(keyword in value for keyword in keywords):
            stages.append(stage)
    return sorted(set(stages or ["S00"]))


def parse_resources(text: str) -> list[dict[str, Any]]:
    body = text.split("## Curated Resources", 1)[1]
    links: dict[str, tuple[str, str]] = {}
    for line in body.splitlines():
        descriptions = [part.strip() for part in line.strip().strip("|").split("|")]
        for match in re.finditer(r"\[([^]]+)]\((https://[^)]+)\)", line):
            title, url = match.groups()
            description = descriptions[-1] if descriptions else "V1 curated learning resource."
            description = re.sub(r"\[[^]]+]\([^)]+\)", title, description)
            links.setdefault(url, (title, description))
    resources = []
    for index, (url, (title, description)) in enumerate(links.items(), start=1):
        host = urlparse(url).hostname or "unknown"
        if "arxiv.org" in host:
            source_type, trust = "paper", "primary"
        elif "github.com" in host:
            source_type, trust = "repository", "maintainer"
        elif any(
            token in host for token in ("openai.com", "anthropic.com", "google", "claude.com")
        ):
            source_type, trust = "official_docs", "primary"
        else:
            source_type, trust = "technical_blog", "curated"
        resources.append(
            {
                "id": f"R{index:03d}",
                "title": title,
                "url": url,
                "source_type": source_type,
                "publisher": host,
                "stage_ids": infer_stages(title, description),
                "why_it_matters": description or "V1 课程保留资源。",
                "trust_level": trust,
                "last_verified_at": None,
                "status": "suspect",
                "replacement_id": None,
                "license_or_access_note": "仅提供链接；不在仓库中再分发外部内容。",
            }
        )
    return resources


def task_record(raw: dict[str, object], resources: list[dict[str, Any]]) -> dict[str, object]:
    task_id = str(raw["new_id"])
    stage_id = task_id.split("-")[0]
    prior = []
    task_number = int(task_id[-2:])
    if task_number > 1:
        prior = [f"{stage_id}-T{task_number - 1:02d}"]
    relevant = [str(item["id"]) for item in resources if stage_id in item["stage_ids"]][:3]
    lab_path = None if stage_id == "S00" else f"labs/stage-{stage_id[1:]}-{stage_slug(stage_id)}"
    return {
        "id": task_id,
        "title": raw["title"],
        "status": "active",
        "prerequisites": prior,
        "learning_outcomes": [f"能够解释并验证：{raw['title']}。"],
        "concepts": [STAGE_TITLES[stage_id]],
        "lab_path": lab_path,
        "artifact": f"workbook/local/evidence/{task_id}.md",
        "rubric": ["概念说明准确且边界清晰。", "验证命令通过，并记录至少一个失败场景。"],
        "validation_commands": [
            "uv run python tools/validate_content.py"
            if lab_path is None
            else f"uv run pytest {lab_path}/tests"
        ],
        "failure_cases": ["输入为空、无效或依赖不可用时给出可解释结果。"],
        "safety_notes": ["使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。"],
        "resources": relevant,
        "estimated_effort": "1-2h",
        "introduced_in": "2.0.0",
        "last_reviewed_at": "2026-07-20",
    }


def stage_slug(stage_id: str) -> str:
    return {
        "S01": "llm-contracts",
        "S02": "agent-loop",
        "S03": "rag-and-memory",
        "S04": "reliability-and-safety",
        "S05": "harness-and-evals",
        "S06": "skills-and-protocols",
        "S07": "browser-and-computer-use",
        "S08": "multi-agent",
        "S09": "capstone",
    }[stage_id]


def parse_projects(text: str) -> list[dict[str, object]]:
    block = text.split("## Project Ladder", 1)[1].split("## Curated Resources", 1)[0]
    rows = []
    for line in block.splitlines():
        match = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if not match:
            continue
        level, title, learning = match.groups()
        index = int(level)
        difficulty = "beginner" if index <= 3 else "intermediate" if index <= 8 else "advanced"
        rows.append(
            {
                "id": f"P{index:02d}",
                "title": title.strip(),
                "track": PROJECT_TRACKS[index - 1],
                "difficulty": difficulty,
                "required": False,
                "prerequisite_task_ids": ["S02-T03"] if index <= 3 else ["S04-T08"],
                "artifact": f"workbook/local/projects/P{index:02d}/README.md",
                "rubric": [f"产物展示 {learning.strip()}。", "验证命令、限制与回滚方式完整。"],
                "validation_commands": ["uv run pytest"],
                "safety_notes": ["只使用合成数据；外部发布或高风险动作需要用户批准。"],
                "estimated_effort": f"{max(2, index * 2)}-{max(4, index * 3)}h",
                "status": "active",
            }
        )
    if len(rows) != 11:
        raise ValueError(f"expected 11 V1 projects, found {len(rows)}")
    return rows


def write_yaml(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / "README.md")
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    raw_tasks = parse_tasks(source)
    resources = parse_resources(source)
    tasks = [task_record(raw, resources) for raw in raw_tasks]
    stages = []
    for stage_id, title in STAGE_TITLES.items():
        stages.append(
            {
                "id": stage_id,
                "title": title,
                "description": f"通过可复查证据学习 {title}。",
                "tasks": [task for task in tasks if str(task["id"]).startswith(stage_id)],
            }
        )
    write_yaml(
        ROOT / "curriculum" / "roadmap.yaml",
        {
            "roadmap_version": "2.0.0",
            "language_strategy": (
                "简体中文为叙述主语言；术语首次出现给出英文，slug 与代码标识保留英文。"
            ),
            "stages": stages,
        },
    )
    write_yaml(
        ROOT / "curriculum" / "resources.yaml", {"schema_version": "2.0.0", "resources": resources}
    )
    write_yaml(
        ROOT / "curriculum" / "projects.yaml",
        {"schema_version": "2.0.0", "projects": parse_projects(source)},
    )
    write_yaml(
        ROOT / "curriculum" / "migrations" / "v1-to-v2.yaml",
        {
            "schema_version": "1.0.0",
            "task_mappings": [
                {"old_id": raw["old_id"], "new_id": raw["new_id"], "was_checked": raw["checked"]}
                for raw in raw_tasks
            ],
            "project_mappings": [
                {"old_id": f"V1-P{index:02d}", "new_id": f"P{index:02d}"} for index in range(1, 12)
            ],
        },
    )


if __name__ == "__main__":
    main()
