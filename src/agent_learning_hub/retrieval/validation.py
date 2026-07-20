from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CitationIssue:
    claim_id: str
    code: str
    message: str


def validate_claim_citations(
    claims: dict[str, str],
    claim_to_chunk_ids: dict[str, list[str]],
    chunks: dict[str, str],
    required_claim_ids: set[str],
    supported_pairs: set[tuple[str, str]],
) -> list[CitationIssue]:
    issues: list[CitationIssue] = []
    for claim_id in claims:
        cited_ids = claim_to_chunk_ids.get(claim_id, [])
        if claim_id in required_claim_ids and not cited_ids:
            issues.append(CitationIssue(claim_id, "missing_citation", "必需结论没有引用。"))
            continue
        for chunk_id in cited_ids:
            chunk_text = chunks.get(chunk_id)
            if chunk_text is None:
                issues.append(
                    CitationIssue(claim_id, "unknown_citation", f"引用 {chunk_id} 不存在。")
                )
                continue
            if (claim_id, chunk_id) not in supported_pairs:
                issues.append(
                    CitationIssue(claim_id, "unsupported_claim", f"引用 {chunk_id} 不支持结论。")
                )
    return issues
