from agent_learning_hub.retrieval import Chunk, RetrievalIndex, validate_claim_citations


def test_chinese_character_ngram_retrieval_and_metadata() -> None:
    chunks = [
        Chunk("rag-1", "rag", "RAG", "local://rag", 0, 12, "检索增强生成包含检索与引用。"),
        Chunk("agent-1", "agent", "Agent", "local://agent", 0, 10, "智能体会调用工具。"),
    ]
    results = RetrievalIndex(chunks).search("检索引用", threshold=0.05)
    assert results
    assert results[0].chunk.id == "rag-1"
    assert results[0].reason.startswith("字符二元组余弦相似度")
    assert RetrievalIndex(chunks).search("完全无关天气", threshold=0.4) == []


def test_claim_citation_validation() -> None:
    issues = validate_claim_citations(
        {
            "c1": "RAG 使用检索",
            "c2": "天气晴朗",
            "c3": "没有引用",
            "c4": "可选结论",
            "c5": "火星天气",
        },
        {"c1": ["rag-1"], "c2": ["missing"], "c5": ["rag-1"]},
        {"rag-1": "RAG 通过检索补充上下文"},
        {"c1", "c2", "c3"},
        {("c1", "rag-1")},
    )
    assert {(issue.claim_id, issue.code) for issue in issues} == {
        ("c2", "unknown_citation"),
        ("c3", "missing_citation"),
        ("c5", "unsupported_claim"),
    }
