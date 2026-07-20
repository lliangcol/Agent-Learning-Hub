from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class ActionRecord:
    step: int
    observation: str
    action: str
    result: str
    stop_reason: str | None = None


def is_allowed_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.hostname in {"localhost", "127.0.0.1"}


def enforce_step_budget(records: list[ActionRecord], max_steps: int = 8) -> bool:
    return len(records) < max_steps
