from __future__ import annotations

import json
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class MigrationReport:
    successful: list[str] = field(default_factory=list)
    downgraded: list[str] = field(default_factory=list)
    unmapped: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(
            len(items)
            for items in (
                self.successful,
                self.downgraded,
                self.unmapped,
                self.conflicts,
                self.rejected,
            )
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "successful": self.successful,
            "downgraded": self.downgraded,
            "unmapped": self.unmapped,
            "conflicts": self.conflicts,
            "rejected": self.rejected,
            "total": self.total,
        }


def status_for_task(new_id: str, *, checked: bool) -> tuple[str, bool]:
    fixed = {
        "S03-T01": "needs_revalidation",
        "S04-T01": "validation_failed",
        "S03-T02": "lab_verified_offline",
        "S04-T02": "learning",
        "S03-T03": "not_started",
    }
    if new_id in fixed:
        state = fixed[new_id]
        return state, checked and state not in {"complete", "lab_verified_live"}
    if not checked:
        return "not_started", False
    if new_id.startswith("S00-"):
        return "complete", False
    return "lab_verified_offline", True


def migrate_legacy_state(
    legacy: dict[str, Any],
    task_mapping: dict[str, str],
    project_mapping: dict[str, str],
    *,
    now: datetime | None = None,
) -> tuple[dict[str, Any], MigrationReport]:
    timestamp = (now or datetime.now(UTC)).astimezone(UTC).isoformat()
    state = legacy.get("state", {})
    if isinstance(state, str):
        try:
            state = json.loads(state)
        except json.JSONDecodeError as exc:
            raise ValueError("legacy state is not valid JSON") from exc
    if not isinstance(state, dict):
        raise ValueError("legacy state must be an object or JSON object string")
    report = MigrationReport()
    task_progress: dict[str, Any] = {}
    project_progress: dict[str, Any] = {}
    for key, raw_value in state.items():
        if not isinstance(key, str) or not isinstance(raw_value, bool):
            report.rejected.append(str(key))
            continue
        if key.startswith("ladder-"):
            old_id = (
                f"V1-P{int(key.removeprefix('ladder-')):02d}"
                if key.removeprefix("ladder-").isdigit()
                else key
            )
            new_id = project_mapping.get(old_id)
            if not new_id:
                report.unmapped.append(key)
                continue
            project_progress[new_id] = progress_record(
                "needs_revalidation" if raw_value else "not_started",
                timestamp,
                "V1 项目只有布尔状态，需要按 rubric 重新验证。",
            )
            (report.downgraded if raw_value else report.successful).append(key)
            continue
        match = key.split("-")
        if len(match) != 2 or not match[0].startswith("stage") or not match[1].isdigit():
            report.unmapped.append(key)
            continue
        old_id = f"V1-S{match[0].removeprefix('stage')}-T{int(match[1]) + 1:02d}"
        new_id = task_mapping.get(old_id)
        if not new_id:
            report.unmapped.append(key)
            continue
        state_name, downgraded = status_for_task(new_id, checked=raw_value)
        task_progress[new_id] = progress_record(
            state_name,
            timestamp,
            "从 V1 布尔状态迁移；只有证据充分的状态才保留完成语义。",
        )
        (report.downgraded if downgraded else report.successful).append(key)
    output = {
        "schema_version": "2.0.0",
        "roadmap_version": "2.0.0",
        "updated_at": timestamp,
        "origin": legacy.get("origin"),
        "task_progress": task_progress,
        "project_progress": project_progress,
    }
    return output, report


def progress_record(state: str, timestamp: str, review: str) -> dict[str, Any]:
    return {
        "state": state,
        "updated_at": timestamp,
        "evidence_paths": ["workbook/archive/legacy-v1/learning-notes/PROGRESS.md"],
        "review": review,
        "environment": "V1 legacy snapshot; environment evidence incomplete",
        "next_anchor": "按 V2 task rubric 复核并记录新证据",
    }


def atomic_write_json(
    path: Path, data: dict[str, Any], *, now: datetime | None = None
) -> Path | None:
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = (now or datetime.now(UTC)).strftime("%Y%m%dT%H%M%SZ")
    backup = None
    if path.exists():
        backup = path.with_suffix(path.suffix + f".bak-{timestamp}")
        shutil.copy2(path, backup)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temp_path, path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        if backup is not None:
            shutil.copy2(backup, path)
        raise
    return backup
