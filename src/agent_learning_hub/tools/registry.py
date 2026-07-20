from __future__ import annotations

import inspect
import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from agent_learning_hub.tools.result import ToolResult, ToolStatus


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    function: Callable[..., ToolResult]
    read_only: bool = True
    cacheable: bool = False

    def as_openai_tool(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": True,
        }


class ToolRegistry:
    def __init__(self, tools: Sequence[ToolSpec] = ()) -> None:
        self._tools = {tool.name: tool for tool in tools}
        self._read_cache: dict[str, ToolResult] = {}
        self._idempotent_results: dict[str, tuple[str, ToolResult]] = {}

    @property
    def specs(self) -> tuple[ToolSpec, ...]:
        return tuple(self._tools.values())

    def run(
        self,
        name: str,
        arguments: dict[str, Any],
        *,
        allow_side_effects: bool = False,
        idempotency_key: str | None = None,
    ) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(
                ToolStatus.FATAL_ERROR, error_code="unknown_tool", message="工具不存在。"
            )
        if not tool.read_only and not allow_side_effects:
            return ToolResult(
                ToolStatus.DENIED, error_code="approval_required", message="该工具需要明确批准。"
            )
        if not tool.read_only and not idempotency_key:
            return ToolResult(
                ToolStatus.DENIED,
                error_code="idempotency_key_required",
                message="副作用工具需要幂等 key。",
            )
        signature = inspect.signature(tool.function)
        try:
            Draft202012Validator(tool.parameters).validate(arguments)
            signature.bind(**arguments)
            signature_key = json.dumps([name, arguments], ensure_ascii=False, sort_keys=True)
        except (SchemaError, TypeError, ValueError, ValidationError):
            return ToolResult(
                ToolStatus.FATAL_ERROR, error_code="invalid_arguments", message="工具参数无效。"
            )
        if tool.read_only and tool.cacheable and signature_key in self._read_cache:
            return self._read_cache[signature_key]
        idempotency_slot = f"{name}:{idempotency_key}" if idempotency_key else None
        if idempotency_slot and idempotency_slot in self._idempotent_results:
            previous_signature, previous_result = self._idempotent_results[idempotency_slot]
            if previous_signature != signature_key:
                return ToolResult(
                    ToolStatus.DENIED,
                    error_code="idempotency_conflict",
                    message="同一幂等 key 不能用于不同参数。",
                )
            return previous_result
        try:
            result = tool.function(**arguments)
        except Exception:
            return ToolResult(
                ToolStatus.FATAL_ERROR, error_code="tool_failed", message="工具执行失败。"
            )
        if tool.read_only and tool.cacheable:
            self._read_cache[signature_key] = result
        if idempotency_slot:
            self._idempotent_results[idempotency_slot] = (signature_key, result)
        return result
