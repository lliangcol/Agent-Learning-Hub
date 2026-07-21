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
_SECRET_KEY_PATTERN = re.compile(r"(?i)^(api[_-]?key|password|passwd|secret|token)$")


def missing_fields(manifest: dict[str, object]) -> set[str]:
    return {field for field in REQUIRED_FIELDS if not manifest.get(field)}


def validate_manifest(manifest: dict[str, object], root: Path) -> list[str]:
    issues = [f"missing:{field}" for field in sorted(missing_fields(manifest))]
    issues.extend(f"unknown:{field}" for field in sorted(set(manifest) - REQUIRED_FIELDS))
    for field in sorted(REQUIRED_FIELDS & set(manifest)):
        value = manifest[field]
        if not isinstance(value, str) or not value.strip():
            issues.append(f"invalid_type:{field}")
    if manifest.get("direction") not in DIRECTIONS:
        issues.append("invalid:direction")
    if _contains_secret_like_data(manifest):
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


def _contains_secret_like_data(value: object) -> bool:
    if isinstance(value, dict):
        return any(
            _SECRET_KEY_PATTERN.fullmatch(str(key)) is not None or _contains_secret_like_data(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return any(_contains_secret_like_data(item) for item in value)
    return isinstance(value, str) and _SECRET_PATTERN.search(value) is not None


def run_research_case(case: dict[str, object]) -> dict[str, object]:
    """Execute one deterministic, read-only local research-assistant case."""
    query = case.get("query")
    if not isinstance(query, str) or not query.strip():
        return _outcome("invalid_input", "stopped")
    if _contains_secret_like_data(query):
        return _outcome("sensitive_input_rejected", "stopped")
    if case.get("request_external") is True:
        return _outcome("permission_denied", "stopped")
    raw_sources = case.get("sources")
    if not isinstance(raw_sources, list):
        return _outcome("invalid_input", "stopped")
    sources: list[tuple[str, str]] = []
    for source in raw_sources:
        if not isinstance(source, dict):
            return _outcome("invalid_input", "stopped")
        source_id = source.get("id")
        text = source.get("text")
        if not isinstance(source_id, str) or not isinstance(text, str):
            return _outcome("invalid_input", "stopped")
        sources.append((source_id, text))
    terms = {term for term in re.findall(r"[a-z0-9]+", query.lower()) if len(term) > 2}
    ranked = sorted(
        sources,
        key=lambda item: len(terms & set(re.findall(r"[a-z0-9]+", item[1].lower()))),
        reverse=True,
    )
    if not ranked or not terms.intersection(re.findall(r"[a-z0-9]+", ranked[0][1].lower())):
        return _outcome("no_sources", "stopped")
    source_id, text = ranked[0]
    return _outcome("complete", "cited_answer", citations=[source_id], answer=text)


def _outcome(
    stop_reason: str,
    status: str,
    *,
    citations: list[str] | None = None,
    answer: str | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "stop_reason": stop_reason,
        "citations": citations or [],
        "answer": answer,
    }
