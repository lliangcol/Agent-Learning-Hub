from __future__ import annotations

import inspect
import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from threading import Event, Lock
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
        self._idempotent_inflight: dict[str, tuple[str, Event]] = {}
        self._cache_lock = Lock()

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
        if tool.read_only and tool.cacheable:
            with self._cache_lock:
                if signature_key in self._read_cache:
                    return self._read_cache[signature_key]
        idempotency_slot = f"{name}:{idempotency_key}" if idempotency_key else None
        owner = False
        wait_for: Event | None = None
        if idempotency_slot:
            with self._cache_lock:
                previous = self._idempotent_results.get(idempotency_slot)
                if previous is not None:
                    previous_signature, previous_result = previous
                    if previous_signature != signature_key:
                        return _idempotency_conflict()
                    return previous_result
                inflight = self._idempotent_inflight.get(idempotency_slot)
                if inflight is not None:
                    previous_signature, wait_for = inflight
                    if previous_signature != signature_key:
                        return _idempotency_conflict()
                else:
                    wait_for = Event()
                    self._idempotent_inflight[idempotency_slot] = (signature_key, wait_for)
                    owner = True
        if wait_for is not None and not owner:
            wait_for.wait()
            # A retryable result is deliberately not cached. Re-entering lets this caller
            # perform the next safe retry while completed results remain deduplicated.
            return self.run(
                name,
                arguments,
                allow_side_effects=allow_side_effects,
                idempotency_key=idempotency_key,
            )
        try:
            result = tool.function(**arguments)
        except Exception:
            result = ToolResult(
                ToolStatus.FATAL_ERROR, error_code="tool_failed", message="工具执行失败。"
            )
        except BaseException:
            if idempotency_slot and owner:
                with self._cache_lock:
                    _, event = self._idempotent_inflight.pop(idempotency_slot)
                    event.set()
            raise
        with self._cache_lock:
            if tool.read_only and tool.cacheable:
                self._read_cache[signature_key] = result
            if idempotency_slot and owner:
                _, event = self._idempotent_inflight.pop(idempotency_slot)
                if result.status is not ToolStatus.RETRYABLE_ERROR:
                    self._idempotent_results[idempotency_slot] = (signature_key, result)
                event.set()
        return result


def _idempotency_conflict() -> ToolResult:
    return ToolResult(
        ToolStatus.DENIED,
        error_code="idempotency_conflict",
        message="同一幂等 key 不能用于不同参数。",
    )
