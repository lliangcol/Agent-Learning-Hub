from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal


class StopReason(StrEnum):
    COMPLETED = "completed"
    MAX_STEPS = "max_steps"
    DEADLINE = "deadline"
    TOOL_BUDGET = "tool_budget"
    REPEATED_CALL = "repeated_call"
    PROVIDER_ERROR = "provider_error"
    UNKNOWN_RESPONSE = "unknown_response"


@dataclass(frozen=True, slots=True)
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str | dict[str, Any]
    name: str | None = None


@dataclass(frozen=True, slots=True)
class ProviderResponse:
    kind: Literal["text", "tool_call", "unknown"]
    text: str | None = None
    tool_name: str | None = None
    tool_arguments: dict[str, Any] = field(default_factory=dict)
    call_id: str | None = None


@dataclass(slots=True)
class AgentState:
    messages: list[Message]
    step: int = 0
    tool_calls: int = 0
    repeated_calls: dict[str, int] = field(default_factory=dict)
