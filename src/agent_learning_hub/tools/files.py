from __future__ import annotations

import os
import tempfile
from pathlib import Path

from agent_learning_hub.tools.registry import ToolSpec
from agent_learning_hub.tools.result import ToolResult, ToolStatus


class WorkspaceFiles:
    """UTF-8 file tools confined to one explicit workspace root."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("workspace root must be a directory")

    def _resolve(self, relative_path: str) -> Path:
        candidate = Path(relative_path)
        if candidate.is_absolute() or not relative_path.strip():
            raise ValueError("invalid relative path")
        resolved = (self.root / candidate).resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError("path escapes workspace root")
        return resolved

    def read_text(self, relative_path: str) -> ToolResult:
        try:
            path = self._resolve(relative_path)
            if not path.is_file():
                return ToolResult(
                    ToolStatus.FATAL_ERROR,
                    error_code="file_not_found",
                    message="文件不存在。",
                )
            return ToolResult(
                ToolStatus.OK,
                {
                    "path": path.relative_to(self.root).as_posix(),
                    "content": path.read_text(encoding="utf-8"),
                },
            )
        except (OSError, UnicodeError, ValueError):
            return ToolResult(
                ToolStatus.FATAL_ERROR,
                error_code="invalid_path_or_encoding",
                message="无法读取工作区文件。",
            )

    def write_text(
        self, relative_path: str, content: str, *, overwrite: bool = False
    ) -> ToolResult:
        try:
            path = self._resolve(relative_path)
            if path.exists() and not overwrite:
                return ToolResult(
                    ToolStatus.DENIED,
                    error_code="overwrite_denied",
                    message="目标已存在；需要显式覆盖策略。",
                )
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
            )
            temporary = Path(temporary_name)
            try:
                with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
                    stream.write(content)
                os.replace(temporary, path)
            finally:
                temporary.unlink(missing_ok=True)
            return ToolResult(ToolStatus.OK, {"path": path.relative_to(self.root).as_posix()})
        except (OSError, UnicodeError, ValueError):
            return ToolResult(
                ToolStatus.FATAL_ERROR,
                error_code="invalid_path_or_encoding",
                message="无法写入工作区文件。",
            )

    def specs(self) -> tuple[ToolSpec, ToolSpec]:
        read_schema = {
            "type": "object",
            "properties": {"relative_path": {"type": "string"}},
            "required": ["relative_path"],
            "additionalProperties": False,
        }
        write_schema = {
            "type": "object",
            "properties": {
                "relative_path": {"type": "string"},
                "content": {"type": "string"},
                "overwrite": {"type": "boolean"},
            },
            "required": ["relative_path", "content"],
            "additionalProperties": False,
        }
        return (
            ToolSpec("read_file", "Read one UTF-8 workspace file.", read_schema, self.read_text),
            ToolSpec(
                "write_file",
                "Atomically write one UTF-8 workspace file.",
                write_schema,
                self.write_text,
                read_only=False,
            ),
        )
