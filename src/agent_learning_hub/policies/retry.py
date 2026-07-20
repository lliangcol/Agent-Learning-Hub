from __future__ import annotations

import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from agent_learning_hub.tools.result import ToolResult, ToolStatus

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 0.05
    max_delay: float = 1.0
    jitter: float = 0.1


def run_with_retry(
    operation: Callable[[], ToolResult],
    policy: RetryPolicy,
    *,
    sleep: Callable[[float], None] = time.sleep,
    random_value: Callable[[], float] = random.random,
) -> ToolResult:
    if policy.max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    result = ToolResult(ToolStatus.FATAL_ERROR, error_code="not_started")
    for attempt in range(policy.max_attempts):
        result = operation()
        if result.status is not ToolStatus.RETRYABLE_ERROR:
            return result
        if attempt + 1 < policy.max_attempts:
            delay = min(policy.base_delay * (2**attempt), policy.max_delay)
            sleep(delay * (1 + policy.jitter * random_value()))
    return result
