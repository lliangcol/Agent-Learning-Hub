# task3_tools.py — Task 3: 定义工具函数

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ── 1. 工具函数（程序执行） ──────────────────────────────────────

def calculator(expression):
    """计算一个数学表达式，例如 '2 + 3 * 4'"""
    try:
        result = eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


def get_weather(city):
    """返回城市天气（mock 数据）"""
    mock_data = {
        "北京": {"temperature": 28, "condition": "晴"},
        "上海": {"temperature": 25, "condition": "多云"},
    }
    if city in mock_data:
        return mock_data[city]
    return {"error": f"没有 {city} 的天气数据"}


# ── 2. 工具描述 schema（模型读取） ────────────────────────────────
# 格式遵循 OpenAI function calling 规范，Claude / Gemini 结构类似。

TOOLS = [
    {
        "name": "calculator",
        "description": "计算数学表达式，支持加减乘除和括号",
        "parameters": {
            "expression": {
                "type": "string",
                "description": "要计算的表达式，例如 '(2 + 3) * 4'",
            }
        },
        "required": ["expression"],
    },
    {
        "name": "get_weather",
        "description": "查询某个城市的当前天气",
        "parameters": {
            "city": {
                "type": "string",
                "description": "城市名称，例如 '北京'",
            }
        },
        "required": ["city"],
    },
]


# ── 3. 工具注册表（名字 → 函数） ──────────────────────────────────
# agent loop 里通过名字找到对应函数来执行

TOOL_REGISTRY = {
    "calculator": calculator,
    "get_weather": get_weather,
}


# ── 4. 手动测试 ───────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== 测试 calculator ===")
    print(calculator("(2 + 3) * 4"))
    print(calculator("10 / 0"))

    print()
    print("=== 测试 get_weather ===")
    print(get_weather("北京"))
    print(get_weather("广州"))

    print()
    print("=== 通过注册表调用 ===")
    tool_name = "calculator"
    tool_args = {"expression": "100 - 37"}
    result = TOOL_REGISTRY[tool_name](**tool_args)
    print(f"调用 {tool_name}({tool_args}) => {result}")
