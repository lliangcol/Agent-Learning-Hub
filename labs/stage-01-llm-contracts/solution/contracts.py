from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StructuredAnswer:
    answer: str
    confidence: float


def parse_structured_answer(text: str, *, max_length: int = 2000) -> StructuredAnswer:
    if len(text) > max_length:
        raise ValueError("output_too_long")
    decoder = json.JSONDecoder()
    stripped = text.strip()
    try:
        value, end = decoder.raw_decode(stripped)
    except json.JSONDecodeError as exc:
        raise ValueError("invalid_json") from exc
    if stripped[end:].strip():
        raise ValueError("multiple_or_trailing_values")
    if not isinstance(value, dict) or set(value) != {"answer", "confidence"}:
        raise ValueError("invalid_fields")
    answer = value["answer"]
    confidence = value["confidence"]
    if (
        not isinstance(answer, str)
        or isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
    ):
        raise ValueError("invalid_types")
    if not 0 <= float(confidence) <= 1:
        raise ValueError("confidence_out_of_range")
    return StructuredAnswer(answer=answer, confidence=float(confidence))
