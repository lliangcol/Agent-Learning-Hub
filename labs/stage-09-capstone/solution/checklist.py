from __future__ import annotations

import re
from pathlib import Path

REQUIRED_FIELDS = {
    "direction",
    "user",
    "task",
    "success_criteria",
    "eval_dataset",
    "permissions",
    "logging",
    "deployment",
    "limitations",
    "rollback",
}
DIRECTIONS = {
    "research-assistant",
    "code-review-assistant",
    "personal-knowledge-assistant",
}
_SECRET_PATTERN = re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]")


def missing_fields(manifest: dict[str, object]) -> set[str]:
    return {field for field in REQUIRED_FIELDS if not manifest.get(field)}


def validate_manifest(manifest: dict[str, object], root: Path) -> list[str]:
    issues = [f"missing:{field}" for field in sorted(missing_fields(manifest))]
    if manifest.get("direction") not in DIRECTIONS:
        issues.append("invalid:direction")
    if _SECRET_PATTERN.search(str(manifest)):
        issues.append("secret_like_value")
    dataset_value = manifest.get("eval_dataset")
    if isinstance(dataset_value, str):
        root = root.resolve()
        dataset = (root / dataset_value).resolve()
        if not dataset.is_relative_to(root):
            issues.append("invalid:eval_dataset_path")
        elif not dataset.is_file():
            issues.append("missing:eval_dataset_file")
    return issues
