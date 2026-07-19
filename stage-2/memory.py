"""Stage 2 Task 3: 短期上下文 / 会话记忆 / 长期记忆的最小实现。

用整数 step 计数器代替真实时间戳，方便演示可复现，不依赖真实时钟。
"""

import math
import re
from collections import Counter


# ---------- 复用 Task 1 的简化 embedding，用于长期记忆检索 ----------
# 这里用字符 bigram 代替 Task 1 的按词切分：中文没有空格分词，
# "用户在哪工作" 会被 \w+ 整体当成一个词，导致和任何别的中文短语都匹配不上。
# 按字符两两滑窗切分，query 和内容之间只要有局部重叠的字符对，就能算出非零相似度。

def tokenize(text):
    cleaned = re.sub(r"[^\w]", "", text.lower())
    if len(cleaned) < 2:
        return [cleaned] if cleaned else []
    return [cleaned[i:i + 2] for i in range(len(cleaned) - 1)]


def embed(text, vocab):
    counts = Counter(tokenize(text))
    return [counts.get(word, 0) for word in vocab]


def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ---------- 会话记忆：滑动窗口 + 摘要压缩 ----------

class SessionMemory:
    """管理一次对话内的多轮消息；超过窗口的老消息压缩成摘要，而不是无限累积。"""

    def __init__(self, window_size=4):
        self.window_size = window_size
        self.messages = []  # 完整历史，仅用于记录/审计
        self.summary = ""   # 被裁剪掉的老消息的摘要

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def _mock_summarize(self, dropped_messages):
        """真实系统会用 LLM 摘要，这里用简单拼接代替，只保留每条消息的前 20 字。"""
        pieces = [f"{m['role']}: {m['content'][:20]}" for m in dropped_messages]
        return "（早期对话摘要）" + " | ".join(pieces)

    def get_context(self):
        """返回喂给下一次模型调用的短期上下文：[摘要] + 最近 window_size 条原文。"""
        if len(self.messages) <= self.window_size:
            return list(self.messages)

        dropped = self.messages[: -self.window_size]
        recent = self.messages[-self.window_size:]
        self.summary = self._mock_summarize(dropped)
        return [{"role": "system", "content": self.summary}] + recent


# ---------- 长期记忆：跨会话持久化 + 检索 + 覆盖更新 + 过期 ----------

class LongTermMemory:
    """按 key 去重存储；同 key 写入直接覆盖旧值，而不是无限追加造成重复/矛盾记录。"""

    def __init__(self, ttl_steps=None):
        self.store = {}      # key -> {"content", "vector", "written_at", "expires_at"}
        self.vocab = []
        self.ttl_steps = ttl_steps  # 多少个 step 后视为过期；None 表示不过期

    def _rebuild_vocab(self):
        self.vocab = sorted({w for e in self.store.values() for w in tokenize(e["content"])})
        for e in self.store.values():
            e["vector"] = embed(e["content"], self.vocab)

    def write(self, key, content, now):
        """写入/更新一条长期记忆。同 key 直接覆盖，避免旧事实和新事实同时存在造成冲突。"""
        expires_at = now + self.ttl_steps if self.ttl_steps else None
        self.store[key] = {"content": content, "written_at": now, "expires_at": expires_at}
        self._rebuild_vocab()

    def retrieve(self, query, now, top_k=2, threshold=0.1):
        """检索前先过滤掉已过期的记忆，避免用陈旧事实回答问题。"""
        query_vec = embed(query, self.vocab)
        candidates = []
        for key, entry in self.store.items():
            if entry["expires_at"] is not None and now >= entry["expires_at"]:
                continue
            score = cosine_similarity(query_vec, entry["vector"])
            if score >= threshold:
                candidates.append((key, entry["content"], score))
        candidates.sort(key=lambda item: item[2], reverse=True)
        return candidates[:top_k]


if __name__ == "__main__":
    print("=== 1. 会话记忆：滑动窗口 + 摘要压缩 ===")
    session = SessionMemory(window_size=2)
    for i in range(5):
        session.add_message("user", f"这是第 {i} 轮用户消息，内容比较长，占用不少 token")
        session.add_message("assistant", f"这是第 {i} 轮模型回复")
    for m in session.get_context():
        print(f"[{m['role']}] {m['content']}")

    print("\n=== 2. 长期记忆：写入、检索、覆盖更新、过期 ===")
    memory = LongTermMemory(ttl_steps=5)
    memory.write("user_job", "用户在 A 公司担任工程师", now=0)
    print("检索 '用户在哪工作' (step=1):", memory.retrieve("用户在哪工作", now=1))

    memory.write("user_job", "用户在 B 公司担任工程师", now=2)
    print("覆盖后检索 (step=3):", memory.retrieve("用户在哪工作", now=3))
    print("store 里 user_job 只有一条记录，长度:", len(memory.store))

    print("过期后检索 (step=8):", memory.retrieve("用户在哪工作", now=8))
