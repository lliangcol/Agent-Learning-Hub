# task2_json.py — Task 2: 让模型输出结构化 JSON

import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def mock_llm(messages):
    # 模拟模型在 JSON 前后加了多余文字（真实场景常见）
    return '当然，这是结果：{"answer": "AI agent 是一个能观察环境、做决策、执行动作的系统。", "confidence": 0.9} 希望对你有帮助！'


def extract_json(text):
    """从模型输出里提取第一个 JSON 对象"""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError(f"模型输出里没有找到 JSON：{text}")
    return json.loads(match.group())


def chat(user_input):
    messages = [
        {"role": "system", "content": "你是一个助手。请用 JSON 格式回复，包含 answer 和 confidence 两个字段。"},
        {"role": "user",   "content": user_input},
    ]

    raw = mock_llm(messages)
    print(f"模型原始输出：{raw}")
    print()

    result = extract_json(raw)

    print(f"解析后的回答：{result['answer']}")
    print(f"置信度：{result['confidence']}")


chat("什么是 AI agent？")
