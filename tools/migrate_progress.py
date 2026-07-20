from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from agent_learning_hub.progress import atomic_write_json, migrate_legacy_state

ROOT = Path(__file__).parents[1]


def mappings() -> tuple[dict[str, str], dict[str, str]]:
    value = yaml.safe_load(
        (ROOT / "curriculum" / "migrations" / "v1-to-v2.yaml").read_text(encoding="utf-8")
    )
    return (
        {item["old_id"]: item["new_id"] for item in value["task_mappings"]},
        {item["old_id"]: item["new_id"] for item in value["project_mappings"]},
    )


def repository_snapshot() -> dict[str, Any]:
    mapping = yaml.safe_load(
        (ROOT / "curriculum" / "migrations" / "v1-to-v2.yaml").read_text(encoding="utf-8")
    )
    state: dict[str, bool] = {}
    for item in mapping["task_mappings"]:
        if item["was_checked"]:
            old = item["old_id"]
            stage, task = old.split("-")[1:]
            state[f"stage{stage.removeprefix('S')}-{int(task.removeprefix('T')) - 1}"] = True
    state.update(
        {"stage2-0": True, "stage2-1": True, "stage2-2": True, "stage2-3": False, "stage2-4": False}
    )
    return {"origin": "repository-v1-snapshot", "state": state}


def validate_progress(data: dict[str, Any]) -> list[str]:
    schema = json.loads(
        (ROOT / "curriculum" / "schemas" / "progress.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    messages = [error.message for error in validator.iter_errors(data)]
    roadmap = yaml.safe_load((ROOT / "curriculum" / "roadmap.yaml").read_text(encoding="utf-8"))
    projects = yaml.safe_load((ROOT / "curriculum" / "projects.yaml").read_text(encoding="utf-8"))
    valid_tasks = {task["id"] for stage in roadmap["stages"] for task in stage["tasks"]}
    valid_projects = {project["id"] for project in projects["projects"]}
    messages.extend(
        f"unknown task ID {item}"
        for item in data.get("task_progress", {})
        if item not in valid_tasks
    )
    messages.extend(
        f"unknown project ID {item}"
        for item in data.get("project_progress", {})
        if item not in valid_projects
    )
    return messages


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path)
    source.add_argument("--repository-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    legacy = (
        repository_snapshot()
        if args.repository_snapshot
        else json.loads(args.input.read_text(encoding="utf-8"))
    )
    task_mapping, project_mapping = mappings()
    migrated, report = migrate_legacy_state(legacy, task_mapping, project_mapping)
    messages = validate_progress(migrated)
    if messages:
        print("\n".join(messages), file=sys.stderr)
        return 1
    print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))
    if args.apply:
        if args.output is None:
            parser.error("--apply requires --output")
        backup = atomic_write_json(args.output, migrated)
        print(f"wrote {args.output}")
        if backup:
            print(f"backup {backup}")
    else:
        print("dry-run only; no state was written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
