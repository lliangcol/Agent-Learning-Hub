import sqlite3
from datetime import UTC, datetime, timedelta

import pytest

from agent_learning_hub.core import Message
from agent_learning_hub.memory import SessionMemory, SQLiteMemory


def test_session_memory_summarizes_only_newly_dropped_messages() -> None:
    memory = SessionMemory(window_size=2)
    for index in range(4):
        memory.add(Message("user", f"message-{index}"))
    calls: list[tuple[str, list[str]]] = []

    def summarize(previous: str, messages: list[Message]) -> str:
        calls.append((previous, [str(message.content) for message in messages]))
        return previous + ",".join(str(message.content) for message in messages)

    first = memory.context(summarize)
    assert calls == [("", ["message-0", "message-1"])]
    assert len(first) == 3
    memory.add(Message("assistant", "message-4"))
    memory.context(summarize)
    assert calls[-1][1] == ["message-2"]


def test_sqlite_memory_persists_updates_expires_exports_and_deletes(tmp_path) -> None:
    path = tmp_path / "memory.sqlite3"
    now = datetime(2026, 7, 20, tzinfo=UTC)
    store = SQLiteMemory(path, allow_persistence=True)
    first = store.write("role", "合成用户喜欢 Python", source="fixture", ttl_seconds=60, now=now)
    assert first.record_version == 1
    reopened = SQLiteMemory(path, allow_persistence=True)
    assert reopened.get("role", now=now).content == "合成用户喜欢 Python"  # type: ignore[union-attr]
    updated = reopened.write("role", "合成用户喜欢 Rust", source="fixture", now=now)
    assert updated.record_version == 2
    assert reopened.search("Rust", now=now)[0].key == "role"
    assert "合成用户喜欢 Rust" in reopened.export_json(now=now)
    assert store.write("temp", "临时偏好", source="fixture", ttl_seconds=1, now=now)
    assert store.get("temp", now=now + timedelta(seconds=2)) is None
    assert store.delete("role")
    assert store.get("role", now=now) is None
    assert store.clear() == 1


def test_sqlite_memory_requires_consent_and_rejects_secrets(tmp_path) -> None:
    with pytest.raises(PermissionError):
        SQLiteMemory(tmp_path / "denied.sqlite3", allow_persistence=False)
    store = SQLiteMemory(tmp_path / "memory.sqlite3", allow_persistence=True)
    with pytest.raises(ValueError, match="不得写入"):
        store.write("credential", "API_KEY=secret-value", source="fixture")


def test_sqlite_memory_parameterizes_injection_shaped_keys(tmp_path) -> None:
    store = SQLiteMemory(tmp_path / "memory.sqlite3", allow_persistence=True)
    shaped_key = "x'; DROP TABLE memories;--"
    store.write(shaped_key, "synthetic harmless content", source="fixture")
    assert store.get(shaped_key) is not None
    store.write("still-present", "table survived", source="fixture")
    assert store.get("still-present") is not None


def test_sqlite_memory_backs_up_migrations_and_rejects_future_schema(tmp_path) -> None:
    path = tmp_path / "legacy.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE legacy (value TEXT)")
    SQLiteMemory(path, allow_persistence=True)
    assert path.with_suffix(".sqlite3.bak").is_file()
    with sqlite3.connect(path) as connection:
        connection.execute("UPDATE metadata SET value = '999' WHERE key = 'schema_version'")
    with pytest.raises(RuntimeError, match="不兼容"):
        SQLiteMemory(path, allow_persistence=True)


def test_sqlite_memory_validates_empty_and_explicit_secret_records(tmp_path) -> None:
    store = SQLiteMemory(tmp_path / "memory.sqlite3", allow_persistence=True)
    with pytest.raises(ValueError, match="must not be empty"):
        store.write("", "content", source="fixture")
    with pytest.raises(ValueError, match="不得写入"):
        store.write("key", "harmless", source="fixture", sensitivity="secret")
