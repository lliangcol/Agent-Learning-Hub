from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chunk:
    id: str
    document_id: str
    title: str
    uri: str
    start: int
    end: int
    text: str


@dataclass(frozen=True, slots=True)
class SearchResult:
    chunk: Chunk
    score: float
    reason: str


def character_ngrams(text: str, size: int = 2) -> list[str]:
    normalized = re.sub(r"\s+", "", text.casefold())
    if not normalized:
        return []
    if len(normalized) < size:
        return [normalized]
    return [normalized[index : index + size] for index in range(len(normalized) - size + 1)]


class RetrievalIndex:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = tuple(chunks)
        self._vectors = [Counter(character_ngrams(chunk.text)) for chunk in chunks]

    def search(self, query: str, *, top_k: int = 3, threshold: float = 0.1) -> list[SearchResult]:
        query_vector = Counter(character_ngrams(query))
        scored: list[SearchResult] = []
        for chunk, vector in zip(self.chunks, self._vectors, strict=True):
            score = _cosine(query_vector, vector)
            if score >= threshold:
                scored.append(
                    SearchResult(
                        chunk=chunk,
                        score=score,
                        reason=f"字符二元组余弦相似度 {score:.3f}",
                    )
                )
        scored.sort(key=lambda item: (-item.score, item.chunk.id))
        return scored[:top_k]


def _cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(value * right.get(key, 0) for key, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0
