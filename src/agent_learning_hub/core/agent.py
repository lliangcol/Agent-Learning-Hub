from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass

from agent_learning_hub.core.models import AgentState, Message, StopReason
from agent_learning_hub.providers.base import LLMClient
from agent_learning_hub.tools.registry import ToolRegistry
from agent_learning_hub.tracing import StepTrace, TraceLog


@dataclass(frozen=True, slots=True)
class AgentRunResult:
    stop_reason: StopReason
    answer: str | None
    state: AgentState
    trace: TraceLog


class AgentRunner:
    def __init__(
        self,
        provider: LLMClient,
        registry: ToolRegistry,
        *,
        max_steps: int = 8,
        total_deadline: float = 30.0,
        provider_timeout: float = 10.0,
        tool_timeout: float = 5.0,
        tool_budget: int = 6,
        repeat_limit: int = 2,
    ) -> None:
        self.provider = provider
        self.registry = registry
        self.max_steps = max_steps
        self.total_deadline = total_deadline
        self.provider_timeout = provider_timeout
        self.tool_timeout = tool_timeout
        self.tool_budget = tool_budget
        self.repeat_limit = repeat_limit

    def run(self, user_input: str) -> AgentRunResult:
        state = AgentState(
            messages=[
                Message("system", "你是离线教学助手；只使用已注册工具并遵守停止条件。"),
                Message("user", user_input),
            ]
        )
        trace = TraceLog()
        started = time.monotonic()
        for step in range(1, self.max_steps + 1):
            state.step = step
            if time.monotonic() - started >= self.total_deadline:
                return AgentRunResult(StopReason.DEADLINE, None, state, trace)
            call_started = time.monotonic()
            try:
                response = self.provider.respond(
                    state.messages,
                    self.registry.specs,
                    timeout=self.provider_timeout,
                )
            except Exception:
                trace.add(
                    StepTrace(
                        step,
                        "provider_error",
                        _elapsed_ms(call_started),
                        error_code="provider_failed",
                    )
                )
                return AgentRunResult(StopReason.PROVIDER_ERROR, None, state, trace)
            trace.add(StepTrace(step, f"provider_{response.kind}", _elapsed_ms(call_started)))
            if response.kind == "text" and response.text is not None:
                state.messages.append(Message("assistant", response.text))
                return AgentRunResult(StopReason.COMPLETED, response.text, state, trace)
            if response.kind != "tool_call" or response.tool_name is None:
                return AgentRunResult(StopReason.UNKNOWN_RESPONSE, None, state, trace)
            if state.tool_calls >= self.tool_budget:
                return AgentRunResult(StopReason.TOOL_BUDGET, None, state, trace)
            signature = json.dumps(
                [response.tool_name, response.tool_arguments], ensure_ascii=False, sort_keys=True
            )
            state.repeated_calls[signature] = state.repeated_calls.get(signature, 0) + 1
            if state.repeated_calls[signature] > self.repeat_limit:
                return AgentRunResult(StopReason.REPEATED_CALL, None, state, trace)
            state.tool_calls += 1
            tool_started = time.monotonic()
            executor = ThreadPoolExecutor(max_workers=1)
            future = executor.submit(self.registry.run, response.tool_name, response.tool_arguments)
            try:
                tool_result = future.result(timeout=self.tool_timeout)
            except TimeoutError:
                future.cancel()
                trace.add(
                    StepTrace(
                        step,
                        "tool_timeout",
                        _elapsed_ms(tool_started),
                        response.tool_name,
                        "timeout",
                    )
                )
                return AgentRunResult(StopReason.DEADLINE, None, state, trace)
            finally:
                executor.shutdown(wait=False, cancel_futures=True)
            trace.add(
                StepTrace(
                    step,
                    "tool_result",
                    _elapsed_ms(tool_started),
                    response.tool_name,
                    tool_result.error_code,
                )
            )
            state.messages.append(
                Message(
                    "assistant",
                    {
                        "type": "tool_call",
                        "name": response.tool_name,
                        "arguments": response.tool_arguments,
                        "call_id": response.call_id or f"local-call-{step}",
                    },
                )
            )
            state.messages.append(
                Message(
                    "tool",
                    {
                        **tool_result.as_dict(),
                        "call_id": response.call_id or f"local-call-{step}",
                    },
                    name=response.tool_name,
                )
            )
        return AgentRunResult(StopReason.MAX_STEPS, None, state, trace)


def _elapsed_ms(started: float) -> float:
    return round((time.monotonic() - started) * 1000, 3)
