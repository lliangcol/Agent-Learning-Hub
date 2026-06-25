# task5_execute.py — Task 5: 执行工具，把结果喂回模型

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ── 工具函数（来自 Task 3） ─────────────────────────────────────────

def calculator(expression):
    try:
        return {"result": eval(expression)}
    except Exception as e:
        return {"error": str(e)}

TOOL_REGISTRY = {
    "calculator": calculator,
}


# ── mock LLM（模拟两轮对话） ────────────────────────────────────────

def mock_llm(messages):
    # 第一轮：用户问了需要计算的问题，模型决定调用工具
    if len(messages) == 2:
        return {
            "type": "tool_use",
            "name": "calculator",
            "input": {"expression": "1024 * 1024"},
        }
    # 第二轮：模型看到工具结果后，给出最终回答
    return {
        "type": "text",
        "content": "1024 × 1024 = 1,048,576，也就是 1 MB 等于 1,048,576 字节。",
    }


# ── 核心：执行工具并把结果加回 messages ────────────────────────────

def run_tool(tool_name, tool_input):
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"未知工具：{tool_name}"}
    return TOOL_REGISTRY[tool_name](**tool_input)


def add_tool_result(messages, tool_name, tool_input, tool_output):
    # 把模型的 tool call 记录进去（assistant 说的）
    messages.append({
        "role": "assistant",
        "content": {"type": "tool_use", "name": tool_name, "input": tool_input},
    })
    # 把工具执行结果记录进去（tool 返回的）
    messages.append({
        "role": "tool",
        "name": tool_name,
        "content": str(tool_output),
    })
    return messages


# ── 主流程 ──────────────────────────────────────────────────────────

def chat(user_input):
    messages = [
        {"role": "system", "content": "你是一个助手，可以使用 calculator 工具。"},
        {"role": "user",   "content": user_input},
    ]

    print(f"用户：{user_input}")
    print()

    # 第一轮：模型决定调用工具
    response = mock_llm(messages)
    print(f"[第一轮] 模型输出类型：{response['type']}")

    if response["type"] == "tool_use":
        tool_name  = response["name"]
        tool_input = response["input"]
        print(f"  → 调用工具：{tool_name}，参数：{tool_input}")

        tool_output = run_tool(tool_name, tool_input)
        print(f"  → 工具结果：{tool_output}")

        # 关键：把工具调用和结果都追加到 messages
        messages = add_tool_result(messages, tool_name, tool_input, tool_output)

    print()

    # 第二轮：模型看到工具结果后给出最终回答
    response = mock_llm(messages)
    print(f"[第二轮] 模型输出类型：{response['type']}")
    print(f"助手：{response['content']}")

    print()
    print("── messages 完整内容 ──")
    for i, msg in enumerate(messages):
        print(f"  [{i}] role={msg['role']}  content={msg['content']}")


chat("1024 乘以 1024 等于多少？")
