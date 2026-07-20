"""Stage 2 Task 1: 最小 RAG pipeline（chunk -> embed -> retrieve -> answer with citations）

无真实 API key，用词频向量代替 embedding，用 mock_llm_answer 代替真实 LLM。
"""

import math
import re
from collections import Counter

DOCUMENTS = [
    (
        "doc1",
        "Agent 是能够感知环境、做出决策并执行动作以达成目标的系统。"
        "一个典型的 agent loop 包括：接收任务、模型决策、可选的工具调用、"
        "执行工具、把结果喂回模型、模型继续或给出最终答案。",
    ),
    (
        "doc2",
        "检索增强生成（RAG）用来解决模型参数记忆静态、不包含私有数据的问题。"
        "RAG 的核心步骤是 chunk、embed、retrieve、answer with citations。"
        "chunk 太大会让检索精度下降，太小会丢失上下文。",
    ),
    (
        "doc3",
        "短期上下文指当前这一次对话或这一次 agent loop 里传给模型的 messages 列表；"
        "会话记忆跨越多轮对话但会话结束后可能丢失；长期记忆持久化到会话之外，"
        "通常存在向量数据库或文件中。",
    ),
]


def chunk_text(doc_id, text, chunk_size=40, overlap=10):
    """按字符数切块，块之间留 overlap，避免关键信息正好被切断在边界上。"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append({"id": f"{doc_id}#{len(chunks)}", "text": text[start:end]})
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def tokenize(text):
    return re.findall(r"\w+", text.lower())


def embed(text, vocab):
    """用词频向量代替真实 embedding：向量维度 = 词表大小，每维是该词的出现次数。"""
    counts = Counter(tokenize(text))
    return [counts.get(word, 0) for word in vocab]


def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b, strict=True))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_index(documents, chunk_size=40, overlap=10):
    all_chunks = []
    for doc_id, text in documents:
        all_chunks.extend(chunk_text(doc_id, text, chunk_size, overlap))

    vocab = sorted({word for c in all_chunks for word in tokenize(c["text"])})
    for c in all_chunks:
        c["vector"] = embed(c["text"], vocab)
    return all_chunks, vocab


def retrieve(query, chunks, vocab, top_k=3, threshold=0.1):
    """取相似度最高的 top_k 个 chunk，低于 threshold 的直接过滤掉。

    这是应对"检索到不相关内容/知识库完全不相关"场景的关键：
    不能让分数进了 top-k 但内容对不上的 chunk 硬凑进上下文。
    """
    query_vec = embed(query, vocab)
    scored = [(c, cosine_similarity(query_vec, c["vector"])) for c in chunks]
    scored = [item for item in scored if item[1] >= threshold]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]


def mock_llm_answer(query, retrieved):
    """用检索到的 chunk 生成带引用编号的回答；检索为空时明确说没找到，不编造。"""
    if not retrieved:
        return "没有找到相关信息。"

    lines = [f"关于「{query}」，参考资料如下："]
    for chunk, score in retrieved:
        lines.append(f"[{chunk['id']}] (相似度 {score:.2f}) {chunk['text']}")
    lines.append("以上内容均标注了来源 chunk id，可据此核实。")
    return "\n".join(lines)


def validate_citations(answer_text, retrieved):
    """程序化校验：回答里出现的引用编号必须都在检索结果里，否则视为幻觉引用。

    只"要求模型引用来源"不足以防止幻觉——模型仍可能编一个看似合理的编号，
    真正兜底的是这一步：生成之后校验引用 id 是否真的在检索结果集合里。
    """
    valid_ids = {chunk["id"] for chunk, _ in retrieved}
    cited_ids = set(re.findall(r"\[([\w#]+)\]", answer_text))
    return cited_ids - valid_ids


def ask(query, chunks, vocab, top_k=3, threshold=0.1):
    retrieved = retrieve(query, chunks, vocab, top_k, threshold)
    answer = mock_llm_answer(query, retrieved)
    hallucinated = validate_citations(answer, retrieved)
    if hallucinated:
        raise ValueError(f"发现未在检索结果中出现的引用编号: {hallucinated}")
    return answer


if __name__ == "__main__":
    chunks, vocab = build_index(DOCUMENTS)

    print("=== 场景 1：知识库里有相关内容 ===")
    print(ask("RAG 的核心步骤是什么？", chunks, vocab))

    print("\n=== 场景 2：问题和知识库完全不相关 ===")
    print(ask("今天天气怎么样？", chunks, vocab))
