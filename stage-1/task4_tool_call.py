# task4_tool_call.py — Task 4: 解析模型的 tool call

import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ── mock：模拟模型的两种输出 ────────────────────────────────────────

def mock_llm_text(messages):
    """模拟普通文字回复"""
    return {
        "type": "text",
        "content": "AI agent 是一个能观察环境、做决策、执行动作的系统。",
    }


def mock_llm_tool_call(messages):
    """模拟模型决定调用工具"""
    return {
        "type": "tool_use",
        "name": "calculator",
        "input": {"expression": "(2 + 3) * 4"},
    }


# ── 解析函数 ────────────────────────────────────────────────────────

def parse_response(response):
    """
    解析模型输出，返回：
      ("text", 文字内容)       — 普通回复
      ("tool_use", name, input) — 工具调用
    """
    if response["type"] == "text":
        return ("text", response["content"])

    if response["type"] == "tool_use":
        return ("tool_use", response["name"], response["input"])

    raise ValueError(f"未知的响应类型：{response['type']}")


# ── 测试 ────────────────────────────────────────────────────────────

print("=== 情况 1：模型返回普通文字 ===")
response = mock_llm_text(messages=[])
parsed = parse_response(response)

if parsed[0] == "text":
    print(f"模型直接回答：{parsed[1]}")

print()

print("=== 情况 2：模型返回 tool call ===")
response = mock_llm_tool_call(messages=[])
parsed = parse_response(response)

if parsed[0] == "tool_use":
    _, tool_name, tool_input = parsed
    print(f"模型要调用工具：{tool_name}")
    print(f"参数：{tool_input}")
    print(f"下一步：去 TOOL_REGISTRY 找到 {tool_name} 并执行（Task 5）")
