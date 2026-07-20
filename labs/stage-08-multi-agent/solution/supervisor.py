from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkItem:
    id: str
    instruction: str


@dataclass(frozen=True, slots=True)
class WorkResult:
    id: str
    output: str
    approved: bool
    stop_reason: str
    rounds: int
    messages: int
    latency_ms: float
    cost_units: int
    errors: tuple[str, ...] = ()


def single_agent_baseline(item: WorkItem) -> WorkResult:
    started = time.perf_counter()
    output = item.instruction.strip()
    approved = bool(output)
    return WorkResult(
        item.id,
        output,
        approved,
        "completed" if approved else "no_progress",
        rounds=1,
        messages=1,
        latency_ms=round((time.perf_counter() - started) * 1000, 3),
        cost_units=1,
        errors=() if approved else ("empty_instruction",),
    )


def supervised_flow(item: WorkItem, *, max_rounds: int = 3, total_budget: int = 6) -> WorkResult:
    started = time.perf_counter()
    if max_rounds < 2 or total_budget < 2:
        return WorkResult(
            item.id,
            "",
            False,
            "budget_denied",
            rounds=0,
            messages=0,
            latency_ms=round((time.perf_counter() - started) * 1000, 3),
            cost_units=0,
            errors=("insufficient_budget",),
        )
    worker_output = item.instruction.strip()
    if not worker_output:
        return WorkResult(
            item.id,
            "",
            False,
            "no_progress",
            rounds=1,
            messages=1,
            latency_ms=round((time.perf_counter() - started) * 1000, 3),
            cost_units=1,
            errors=("worker_no_progress",),
        )
    reviewer_approved = len(worker_output) <= 200
    return WorkResult(
        item.id,
        worker_output,
        reviewer_approved,
        "completed" if reviewer_approved else "review_rejected",
        rounds=2,
        messages=2,
        latency_ms=round((time.perf_counter() - started) * 1000, 3),
        cost_units=2,
        errors=() if reviewer_approved else ("output_too_long",),
    )


def compare(items: list[WorkItem]) -> dict[str, object]:
    baseline = [single_agent_baseline(item) for item in items]
    supervised = [supervised_flow(item) for item in items]

    def metrics(results: list[WorkResult]) -> dict[str, float | int]:
        return {
            "success_rate": sum(result.approved for result in results) / len(results)
            if results
            else 0.0,
            "rounds": sum(result.rounds for result in results),
            "messages": sum(result.messages for result in results),
            "latency_ms": round(sum(result.latency_ms for result in results), 3),
            "cost_units": sum(result.cost_units for result in results),
            "errors": sum(len(result.errors) for result in results),
        }

    baseline_metrics = metrics(baseline)
    supervised_metrics = metrics(supervised)
    return {
        "baseline": baseline_metrics,
        "supervised": supervised_metrics,
        "error_amplification": int(supervised_metrics["errors"]) - int(baseline_metrics["errors"]),
        "recommendation": "single_agent"
        if supervised_metrics["success_rate"] <= baseline_metrics["success_rate"]
        else "multi_agent",
    }
