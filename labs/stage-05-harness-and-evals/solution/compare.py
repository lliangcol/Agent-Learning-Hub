from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

from agent_learning_hub.core import AgentRunner, ProviderResponse, StopReason
from agent_learning_hub.providers import SequenceProvider
from agent_learning_hub.tools import ToolRegistry, ToolResult, ToolSpec, ToolStatus

_EXPECTED_STOPS = {
    "success": StopReason.COMPLETED,
    "empty_result": StopReason.COMPLETED,
    "tool_error": StopReason.COMPLETED,
    "repeated_call": StopReason.REPEATED_CALL,
    "denied": StopReason.COMPLETED,
    "unknown_response": StopReason.UNKNOWN_RESPONSE,
    "provider_error": StopReason.PROVIDER_ERROR,
    "deadline": StopReason.DEADLINE,
    "tool_budget": StopReason.TOOL_BUDGET,
}
_EXPECTED_TOOL_STATUSES = {
    "empty_result": ToolStatus.EMPTY.value,
    "tool_error": ToolStatus.RETRYABLE_ERROR.value,
    "denied": ToolStatus.DENIED.value,
}


class _FailingProvider:
    def respond(self, messages, tools, *, timeout):  # type: ignore[no-untyped-def]
        del messages, tools, timeout
        raise RuntimeError("synthetic provider failure")


def _tool(status: ToolStatus, *, read_only: bool = True) -> ToolSpec:
    return ToolSpec(
        "fixture_tool",
        "Deterministic offline fixture tool.",
        {"type": "object", "additionalProperties": False},
        lambda: ToolResult(status, {"fixture": True}, error_code="synthetic_error"),
        read_only=read_only,
    )


def _typed_runner(scenario: str) -> AgentRunner:
    registry = ToolRegistry([_tool(ToolStatus.OK)])
    options: dict[str, Any] = {}
    if scenario == "success":
        provider = SequenceProvider([ProviderResponse(kind="text", text="synthetic success")])
    elif scenario in {"empty_result", "tool_error", "denied"}:
        status = {
            "empty_result": ToolStatus.EMPTY,
            "tool_error": ToolStatus.RETRYABLE_ERROR,
            "denied": ToolStatus.OK,
        }[scenario]
        registry = ToolRegistry([_tool(status, read_only=scenario != "denied")])
        provider = SequenceProvider(
            [
                ProviderResponse(kind="tool_call", tool_name="fixture_tool", tool_arguments={}),
                ProviderResponse(kind="text", text=f"handled {scenario}"),
            ]
        )
    elif scenario == "repeated_call":
        call = ProviderResponse(kind="tool_call", tool_name="fixture_tool", tool_arguments={})
        provider = SequenceProvider([call, call, call])
    elif scenario == "unknown_response":
        provider = SequenceProvider([ProviderResponse(kind="unknown")])
    elif scenario == "provider_error":
        provider = _FailingProvider()
    elif scenario == "deadline":
        provider = SequenceProvider([ProviderResponse(kind="text", text="too late")])
        options["total_deadline"] = 0
    elif scenario == "tool_budget":
        provider = SequenceProvider(
            [ProviderResponse(kind="tool_call", tool_name="fixture_tool", tool_arguments={})]
        )
        options["tool_budget"] = 0
    else:
        raise ValueError(f"unsupported scenario: {scenario}")
    return AgentRunner(provider, registry, **options)


def _tool_statuses(result) -> list[str]:  # type: ignore[no-untyped-def]
    return [
        str(message.content["status"])
        for message in result.state.messages
        if message.role == "tool" and isinstance(message.content, dict)
    ]


def _run_typed_case(case: dict[str, Any]) -> dict[str, Any]:
    scenario = str(case["scenario"])
    started = time.perf_counter()
    result = _typed_runner(scenario).run("run the same deterministic fixture task")
    latency_ms = round((time.perf_counter() - started) * 1000, 3)
    tool_statuses = _tool_statuses(result)
    expected_status = _EXPECTED_TOOL_STATUSES.get(scenario)
    passed = result.stop_reason is _EXPECTED_STOPS[scenario] and (
        expected_status is None or expected_status in tool_statuses
    )
    return {
        "id": case["id"],
        "scenario": scenario,
        "passed": passed,
        "stop_reason": result.stop_reason.value,
        "steps": result.state.step,
        "tool_calls": result.state.tool_calls,
        "latency_ms": latency_ms,
        "errors": [trace.error_code for trace in result.trace.steps if trace.error_code],
        "cost": None,
    }


def _run_bare_case(case: dict[str, Any]) -> dict[str, Any]:
    scenario = str(case["scenario"])
    passed = scenario == "success"
    return {
        "id": case["id"],
        "scenario": scenario,
        "passed": passed,
        "stop_reason": "completed" if passed else "unsupported_scenario",
        "steps": 1,
        "tool_calls": 0,
        "latency_ms": 0.0,
        "errors": [] if passed else ["unhandled_scenario"],
        "cost": None,
    }


def evaluate(cases: list[dict[str, Any]], *, harness: bool) -> dict[str, Any]:
    outcomes = [(_run_typed_case(case) if harness else _run_bare_case(case)) for case in cases]
    passed = sum(bool(outcome["passed"]) for outcome in outcomes)
    return {
        "runner": "typed-agent-runner" if harness else "bare-loop",
        "total": len(outcomes),
        "passed": passed,
        "success_rate": passed / len(outcomes) if outcomes else 0,
        "total_steps": sum(int(outcome["steps"]) for outcome in outcomes),
        "total_tool_calls": sum(int(outcome["tool_calls"]) for outcome in outcomes),
        "latency_ms": round(sum(float(outcome["latency_ms"]) for outcome in outcomes), 3),
        "stop_reasons": dict(Counter(str(outcome["stop_reason"]) for outcome in outcomes)),
        "failures": [str(outcome["id"]) for outcome in outcomes if not outcome["passed"]],
        "errors": [error for outcome in outcomes for error in outcome["errors"]],
        "cost": None,
        "outcomes": outcomes,
    }


def load_cases(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("eval dataset must be a list")
    return value
