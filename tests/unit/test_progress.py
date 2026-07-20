import json
from datetime import UTC, datetime

import pytest

from agent_learning_hub.progress import atomic_write_json, migrate_legacy_state


def test_progress_migration_reconciles_all_inputs() -> None:
    migrated, report = migrate_legacy_state(
        {
            "origin": "file://",
            "state": json.dumps(
                {
                    "stage0-0": True,
                    "stage1-0": True,
                    "stage2-0": True,
                    "ladder-1": True,
                    "unknown": True,
                    "bad-value": "yes",
                }
            ),
        },
        {"V1-S0-T01": "S00-T01", "V1-S1-T01": "S01-T01", "V1-S2-T01": "S03-T01"},
        {"V1-P01": "P01"},
        now=datetime(2026, 7, 20, tzinfo=UTC),
    )
    assert report.total == 6
    assert migrated["task_progress"]["S00-T01"]["state"] == "complete"
    assert migrated["task_progress"]["S01-T01"]["state"] == "lab_verified_offline"
    assert migrated["task_progress"]["S03-T01"]["state"] == "needs_revalidation"
    assert migrated["project_progress"]["P01"]["state"] == "needs_revalidation"


def test_progress_migration_rejects_invalid_state() -> None:
    with pytest.raises(ValueError, match="valid JSON"):
        migrate_legacy_state({"state": "{"}, {}, {})
    with pytest.raises(ValueError, match="must be an object"):
        migrate_legacy_state({"state": []}, {}, {})


def test_atomic_write_creates_backup(tmp_path) -> None:
    path = tmp_path / "progress.json"
    path.write_text('{"old": true}', encoding="utf-8")
    backup = atomic_write_json(path, {"new": True}, now=datetime(2026, 7, 20, tzinfo=UTC))
    assert backup is not None
    assert json.loads(path.read_text(encoding="utf-8")) == {"new": True}
    assert backup.read_text(encoding="utf-8") == '{"old": true}'
