from __future__ import annotations

from pathlib import Path

from agent_learning_hub.memory import SQLiteMemory
from agent_learning_hub.retrieval import Chunk, RetrievalIndex


def build_index() -> RetrievalIndex:
    return RetrievalIndex(
        [
            Chunk(
                "rag-1",
                "guide",
                "RAG",
                "local://guide",
                0,
                18,
                "RAG 先检索相关片段，再生成带引用的回答。",
            ),
            Chunk(
                "memory-1",
                "guide",
                "Memory",
                "local://guide",
                19,
                40,
                "长期记忆需要持久化、过期和删除策略。",
            ),
        ]
    )


def open_synthetic_memory(path: Path) -> SQLiteMemory:
    return SQLiteMemory(path, allow_persistence=True)
