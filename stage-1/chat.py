# chat.py — Task 1: 用 mock 模拟一次 LLM 对话
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def mock_llm(messages):
    """
    模拟 LLM 返回。真实 API 调用时，这里换成 client.chat() 或 client.messages.create()。
    messages 是一个列表，每条是 {"role": "...", "content": "..."}。
    """
    last_user_message = messages[-1]["content"]
    return f"[mock 回复] 你说的是：「{last_user_message}」"


def chat(user_input):
    messages = [
        {"role": "system", "content": "你是一个助手。"},
        {"role": "user",   "content": user_input},
    ]

    reply = mock_llm(messages)

    print(f"用户：{user_input}")
    print(f"助手：{reply}")


chat("你好，什么是 AI agent？")
