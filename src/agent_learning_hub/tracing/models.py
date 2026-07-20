from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class StepTrace:
    step: int
    event: str
    latency_ms: float
    tool_name: str | None = None
    error_code: str | None = None
    cost: float | None = None


@dataclass(slots=True)
class TraceLog:
    steps: list[StepTrace] = field(default_factory=list)

    def add(self, trace: StepTrace) -> None:
        self.steps.append(trace)
