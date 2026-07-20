from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ToolStatus(StrEnum):
    OK = "ok"
    EMPTY = "empty"
    RETRYABLE_ERROR = "retryable_error"
    FATAL_ERROR = "fatal_error"
    DENIED = "denied"


@dataclass(frozen=True, slots=True)
class ToolResult:
    status: ToolStatus
    data: dict[str, Any] = field(default_factory=dict)
    error_code: str | None = None
    message: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "data": self.data,
            "error_code": self.error_code,
            "message": self.message,
        }
