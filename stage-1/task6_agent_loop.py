# task6_agent_loop.py — Task 6: agent loop + 最大步数 + 超时 + 错误处理

import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MAX_STEPS = 5
TIMEOUT_SECONDS = 10


# ── 工具 ────────────────────────────────────────────────────────────

def calculator(expression):
    try:
        return {"result": eval(expression)}
    except Exception as e:
        return {"error": str(e)}

TOOL_REGISTRY = {"calculator": calculator}


def run_tool(tool_name, tool_input):
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"未知工具：{tool_name}"}
    return TOOL_REGISTRY[tool_name](**tool_input)


def add_tool_result(messages, tool_name, tool_input, tool_output):
    messages.append({
        "role": "assistant",
        "content": {"type": "tool_use", "name": tool_name, "input": tool_input},
    })
    messages.append({
        "role": "tool",
        "name": tool_name,
        "content": str(tool_output),
    })


# ── mock LLM（三种场景） ────────────────────────────────────────────

def mock_normal(messages):
    """场景 1：正常，一次工具调用后给出答案"""
    if len(messages) == 2:
        return {"type": "tool_use", "name": "calculator", "input": {"expression": "99 * 99"}}
    return {"type": "text", "content": "99 × 99 = 9801。"}


def mock_infinite(messages):
    """场景 2：模型一直调工具，不给最终答案（无限循环）"""
    return {"type": "tool_use", "name": "calculator", "input": {"expression": "1 + 1"}}


def mock_tool_error(messages):
    """场景 3：工具调用出错"""
    if len(messages) == 2:
        return {"type": "tool_use", "name": "calculator", "input": {"expression": "1 / 0"}}
    return {"type": "text", "content": "计算失败了，请检查表达式。"}


# ── agent loop ──────────────────────────────────────────────────────

def agent_loop(user_input, mock_llm):
    messages = [
        {"role": "system", "content": "你是一个助手，可以使用 calculator 工具。"},
        {"role": "user",   "content": user_input},
    ]

    start_time = time.time()

    for step in range(1, MAX_STEPS + 1):

        # 保险 1：超时检查
        elapsed = time.time() - start_time
        if elapsed > TIMEOUT_SECONDS:
            return f"[超时] 已运行 {elapsed:.1f}s，超过 {TIMEOUT_SECONDS}s 上限"

        response = mock_llm(messages)
        print(f"  step {step}：type={response['type']}")

        # 模型给出最终答案，正常退出循环
        if response["type"] == "text":
            return response["content"]

        if response["type"] == "tool_use":
            tool_name  = response["name"]
            tool_input = response["input"]

            # 保险 2：工具执行错误不崩溃
            try:
                tool_output = run_tool(tool_name, tool_input)
            except Exception as e:
                tool_output = {"error": str(e)}

            print(f"         调用 {tool_name}{tool_input} => {tool_output}")
            add_tool_result(messages, tool_name, tool_input, tool_output)

    # 保险 3：超过最大步数
    return f"[超出步数] 已执行 {MAX_STEPS} 步，仍未得到最终答案"


# ── 测试三种场景 ────────────────────────────────────────────────────

print("=== 场景 1：正常流程 ===")
result = agent_loop("99 乘以 99 等于多少？", mock_normal)
print(f"最终答案：{result}\n")

print("=== 场景 2：模型无限调工具（最大步数保护） ===")
result = agent_loop("帮我算点东西", mock_infinite)
print(f"最终答案：{result}\n")

print("=== 场景 3：工具执行出错（错误处理） ===")
result = agent_loop("计算 1/0", mock_tool_error)
print(f"最终答案：{result}\n")
