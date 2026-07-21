from __future__ import annotations

import json
import re
import shutil
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

SCHEMA_VERSION = 1
_SENSITIVE_PATTERN = re.compile(
    r"(?i)(api[_ -]?key|password|passwd|secret|token|验证码|-----BEGIN [A-Z ]+ PRIVATE KEY-----)"
)


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    key: str
    content: str
    source: str
    created_at: str
    updated_at: str
    expires_at: str | None
    record_version: int
    sensitivity: str


class SQLiteMemory:
    def __init__(self, path: str | Path, *, allow_persistence: bool) -> None:
        if not allow_persistence:
            raise PermissionError("长期记忆需要显式持久化许可。")
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._prepare_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _prepare_schema(self) -> None:
        existed = self.path.exists()
        with self._connection() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            row = connection.execute(
                "SELECT value FROM metadata WHERE key = 'schema_version'"
            ).fetchone()
            version = int(row["value"]) if row else 0
        if version > SCHEMA_VERSION:
            raise RuntimeError(f"不兼容的记忆 schema 版本：{version}")
        if existed and version < SCHEMA_VERSION:
            shutil.copy2(self.path, self.path.with_suffix(self.path.suffix + ".bak"))
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    key TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    expires_at TEXT,
                    record_version INTEGER NOT NULL,
                    sensitivity TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "INSERT OR REPLACE INTO metadata(key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )

    def write(
        self,
        key: str,
        content: str,
        *,
        source: str,
        ttl_seconds: int | None = None,
        sensitivity: str = "normal",
        now: datetime | None = None,
    ) -> MemoryRecord:
        if not key.strip() or not content.strip():
            raise ValueError("key and content must not be empty")
        if ttl_seconds is not None and (
            isinstance(ttl_seconds, bool) or not isinstance(ttl_seconds, int) or ttl_seconds <= 0
        ):
            raise ValueError("ttl_seconds must be a positive integer")
        if sensitivity == "secret" or _SENSITIVE_PATTERN.search("\n".join((key, content, source))):
            raise ValueError("秘密、凭据和验证码不得写入长期记忆。")
        if sensitivity not in {"normal", "private"}:
            raise ValueError("sensitivity must be normal or private")
        timestamp = (now or datetime.now(UTC)).astimezone(UTC)
        expires = timestamp + timedelta(seconds=ttl_seconds) if ttl_seconds is not None else None
        with self._connection() as connection:
            existing = connection.execute(
                "SELECT created_at, record_version FROM memories WHERE key = ?", (key,)
            ).fetchone()
            created_at = existing["created_at"] if existing else timestamp.isoformat()
            record_version = int(existing["record_version"]) + 1 if existing else 1
            connection.execute(
                """
                INSERT INTO memories (
                    key, content, source, created_at, updated_at,
                    expires_at, record_version, sensitivity
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    content=excluded.content,
                    source=excluded.source,
                    updated_at=excluded.updated_at,
                    expires_at=excluded.expires_at,
                    record_version=excluded.record_version,
                    sensitivity=excluded.sensitivity
                """,
                (
                    key,
                    content,
                    source,
                    created_at,
                    timestamp.isoformat(),
                    expires.isoformat() if expires else None,
                    record_version,
                    sensitivity,
                ),
            )
        record = self.get(key, now=timestamp)
        if record is None:
            raise RuntimeError("persisted memory record could not be read back")
        return record

    def get(self, key: str, *, now: datetime | None = None) -> MemoryRecord | None:
        timestamp = (now or datetime.now(UTC)).astimezone(UTC)
        with self._connection() as connection:
            row = connection.execute("SELECT * FROM memories WHERE key = ?", (key,)).fetchone()
        if row is None:
            return None
        record = _record_from_row(row)
        if record.expires_at and datetime.fromisoformat(record.expires_at) <= timestamp:
            return None
        return record

    def search(self, query: str, *, now: datetime | None = None) -> list[MemoryRecord]:
        timestamp = (now or datetime.now(UTC)).astimezone(UTC)
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM memories
                WHERE content LIKE ? OR key LIKE ?
                ORDER BY updated_at DESC
                """,
                (f"%{query}%", f"%{query}%"),
            ).fetchall()
        return [
            record
            for row in rows
            if (record := _record_from_row(row)).expires_at is None
            or datetime.fromisoformat(record.expires_at) > timestamp
        ]

    def delete(self, key: str) -> bool:
        with self._connection() as connection:
            cursor = connection.execute("DELETE FROM memories WHERE key = ?", (key,))
        return cursor.rowcount > 0

    def clear(self) -> int:
        with self._connection() as connection:
            count = int(connection.execute("SELECT COUNT(*) FROM memories").fetchone()[0])
            connection.execute("DELETE FROM memories")
        return count

    def export_json(self, *, now: datetime | None = None) -> str:
        timestamp = (now or datetime.now(UTC)).astimezone(UTC)
        with self._connection() as connection:
            rows = connection.execute("SELECT * FROM memories ORDER BY key").fetchall()
        records = [
            asdict(record)
            for row in rows
            if (record := _record_from_row(row)).expires_at is None
            or datetime.fromisoformat(record.expires_at) > timestamp
        ]
        return json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "exported_at": timestamp.isoformat(),
                "records": records,
            },
            ensure_ascii=False,
            indent=2,
        )


def _record_from_row(row: sqlite3.Row) -> MemoryRecord:
    return MemoryRecord(
        key=str(row["key"]),
        content=str(row["content"]),
        source=str(row["source"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
        expires_at=str(row["expires_at"]) if row["expires_at"] else None,
        record_version=int(row["record_version"]),
        sensitivity=str(row["sensitivity"]),
    )
