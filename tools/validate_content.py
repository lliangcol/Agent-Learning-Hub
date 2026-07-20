from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).parents[1]
CURRICULUM = ROOT / "curriculum"


class ValidationErrors:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def add(self, file: Path, field: str, message: str) -> None:
        self.messages.append(f"{file.relative_to(ROOT)}:{field}: {message}")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected mapping")
    return value


def validate_schema(data_path: Path, schema_path: Path, errors: ValidationErrors) -> None:
    data = load_yaml(data_path)
    schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        field = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.add(data_path, field, error.message)


def detect_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(node: str, path: list[str]) -> list[str] | None:
        if node in visiting:
            return [*path, node]
        if node in visited:
            return None
        visiting.add(node)
        for target in graph.get(node, []):
            if cycle := walk(target, [*path, node]):
                return cycle
        visiting.remove(node)
        visited.add(node)
        return None

    for node in graph:
        if cycle := walk(node, []):
            return cycle
    return None


def semantic_validation(errors: ValidationErrors) -> None:
    roadmap_path = CURRICULUM / "roadmap.yaml"
    projects_path = CURRICULUM / "projects.yaml"
    resources_path = CURRICULUM / "resources.yaml"
    roadmap = load_yaml(roadmap_path)
    projects = load_yaml(projects_path)
    resources = load_yaml(resources_path)

    stage_ids: set[str] = set()
    tasks: dict[str, dict[str, Any]] = {}
    all_ids: dict[str, list[str]] = defaultdict(list)
    for stage in roadmap["stages"]:
        stage_id = stage["id"]
        stage_ids.add(stage_id)
        all_ids[stage_id].append("roadmap.stage")
        for task in stage["tasks"]:
            task_id = task["id"]
            tasks[task_id] = task
            all_ids[task_id].append("roadmap.task")
            if not task_id.startswith(f"{stage_id}-"):
                errors.add(roadmap_path, task_id, "task ID does not match parent stage")

    project_items = {item["id"]: item for item in projects["projects"]}
    resource_items = {item["id"]: item for item in resources["resources"]}
    for identifier in project_items:
        all_ids[identifier].append("projects")
    for identifier in resource_items:
        all_ids[identifier].append("resources")
    for identifier, locations in all_ids.items():
        if len(locations) > 1:
            errors.add(roadmap_path, identifier, f"duplicate global ID in {locations}")

    graph: dict[str, list[str]] = {}
    for task_id, task in tasks.items():
        graph[task_id] = task["prerequisites"]
        for prerequisite in task["prerequisites"]:
            if prerequisite not in tasks:
                errors.add(roadmap_path, task_id, f"unknown prerequisite {prerequisite}")
        for resource_id in task["resources"]:
            if resource_id not in resource_items:
                errors.add(roadmap_path, task_id, f"unknown resource {resource_id}")
        lab_path = task["lab_path"]
        if lab_path is None and not task_id.startswith("S00-"):
            errors.add(roadmap_path, task_id, "only S00 concept tasks may omit lab_path")
        if lab_path and not (ROOT / lab_path).is_dir():
            errors.add(roadmap_path, task_id, f"missing lab directory {lab_path}")
    if cycle := detect_cycle(graph):
        errors.add(roadmap_path, "prerequisites", f"cycle detected: {' -> '.join(cycle)}")

    for project_id, project in project_items.items():
        for prerequisite in project["prerequisite_task_ids"]:
            if prerequisite not in tasks:
                errors.add(projects_path, project_id, f"unknown task {prerequisite}")
    replacement_graph: dict[str, list[str]] = {}
    for resource_id, resource in resource_items.items():
        for stage_id in resource["stage_ids"]:
            if stage_id not in stage_ids:
                errors.add(resources_path, resource_id, f"unknown stage {stage_id}")
        replacement = resource["replacement_id"]
        replacement_graph[resource_id] = [replacement] if replacement else []
        if replacement and replacement not in resource_items:
            errors.add(resources_path, resource_id, f"unknown replacement {replacement}")
        if replacement == resource_id:
            errors.add(resources_path, resource_id, "replacement cannot reference itself")
    if cycle := detect_cycle(replacement_graph):
        errors.add(resources_path, "replacement_id", f"cycle detected: {' -> '.join(cycle)}")

    migration = load_yaml(CURRICULUM / "migrations" / "v1-to-v2.yaml")
    mapped_tasks = migration["task_mappings"]
    mapped_projects = migration["project_mappings"]
    if len(mapped_tasks) != 50 or {item["new_id"] for item in mapped_tasks} != set(tasks):
        errors.add(roadmap_path, "migrations", "V1 task mapping must cover exactly all 50 tasks")
    if len(mapped_projects) != 11 or {item["new_id"] for item in mapped_projects} != set(
        project_items
    ):
        errors.add(projects_path, "migrations", "V1 project mapping must cover all 11 projects")

    stage_docs = list((CURRICULUM / "stages").glob("stage-*.md"))
    if len(stage_docs) != 10:
        errors.add(CURRICULUM, "stages", f"expected 10 stage documents, found {len(stage_docs)}")


def run() -> list[str]:
    errors = ValidationErrors()
    for name in ("roadmap", "projects", "resources"):
        validate_schema(
            CURRICULUM / f"{name}.yaml",
            CURRICULUM / "schemas" / f"{name}.schema.json",
            errors,
        )
    semantic_validation(errors)
    return errors.messages


def main() -> int:
    messages = run()
    if messages:
        print("\n".join(messages), file=sys.stderr)
        return 1
    print("Content validation passed: 10 stages, 50 tasks, 11 projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
