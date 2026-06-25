# Stage 1: Build A Minimal Agent Loop

来源：`README.md` -> `Learning Todo List` -> `Stage 1: Build A Minimal Agent Loop`

## 学习目标

这个阶段的目标是从“理解 agent 是什么”进入“能写出最小可运行 agent”。先不要追求复杂框架，重点是把一次模型调用、结构化输出、工具定义、工具执行、结果回填、停止条件和错误处理串起来。

## 当前进度

- [x] 会用一个 LLM API 完成普通对话。
- [x] 会让模型输出结构化 JSON。
- [x] 会定义一个工具函数，例如 `search`、`calculator`、`read_file`。
- [x] 会解析模型的 tool call / function call。
- [x] 会执行工具，并把工具结果喂回模型。
- [x] 会给 agent loop 加最大步数、超时和错误处理。

## 核心概念

最小 agent loop 可以先理解成：

```text
user task -> model decides -> optional tool call -> run tool -> send observation back -> model answers or continues
```

Stage 1 的重点不是“模型有多聪明”，而是工程闭环是否清楚：

- 模型输入是什么。
- 模型输出是否能被程序稳定解析。
- 工具是否有明确名称、参数和返回值。
- 工具失败时是否有错误信息。
- loop 是否有最大步数、超时和停止条件。

## 已完成任务

### Task 1：普通 LLM API 对话

完成时间：2026-06-25

方式：Python + mock（环境无真实 API key）。

代码：`stage-1/chat.py`

结构：
- `messages` 列表，每条含 `role` 和 `content`。
- `mock_llm(messages)` 模拟模型返回，之后只需替换这一个函数即可接入真实 API。

Windows 终端中文乱码：在文件开头加 `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")` 解决。

### Task 2：让模型输出结构化 JSON

完成时间：2026-06-25

代码：`stage-1/task2_json.py`

关键点：
- `json.loads()`：JSON 字符串 → Python 字典。
- `json.dumps()`：Python 对象 → JSON 字符串（方向相反）。
- 真实 LLM 常在 JSON 前后加多余文字，用 `re.search(r'\{.*\}', text, re.DOTALL)` 提取。
- 找不到 JSON 时主动 `raise ValueError`，不静默失败 — 方便调试。

检查题修正：
- 用户回答第 2 题时只说了"容错处理"，未说清楚"找不到时抛出 ValueError"。修正后理解：`re.search()` 返回 `None`，`if not match` 触发，程序明确报错并打印原始输出。

### Task 3：定义工具函数

完成时间：2026-06-25

代码：`stage-1/task3_tools.py`

工具由三部分组成：
- **Python 函数**：实际执行逻辑，统一返回字典（成功或错误），用 `try/except` 防止崩溃。
- **schema（`TOOLS`）**：给模型读的描述，含 name、description、parameters、required。
- **注册表（`TOOL_REGISTRY`）**：名字 → 函数的映射，agent loop 通过 `TOOL_REGISTRY[name](**args)` 执行工具。

关键语法：
- `**tool_args`：将字典解包为关键字参数。去掉 `**` 后函数收到的是整个字典对象，类型不对，eval() 抛 TypeError。
- `try/except Exception as e`：捕获所有异常，返回 `{"error": str(e)}`，工具失败不崩溃。

检查题修正：
- 第 2 题用户说"返回错误信息"方向正确，但原因需补全：去掉 `**` 是参数类型传错（整个字典当 expression），而不是语法错误。

### Task 4：解析模型的 tool call

完成时间：2026-06-25

代码：`stage-1/task4_tool_call.py`

模型输出两种类型：
- `type == "text"`：直接展示给用户。
- `type == "tool_use"`：提取 `name` + `input`，交给注册表执行。

`parse_response()` 返回元组，用解包读取：`_, tool_name, tool_input = parsed`，`_` 表示该位置存在但不需要使用。

为什么 `raise ValueError` 而不是 `return None`：`None` 静默传递，错误会在下游才暴露；`raise` 在源头立即报错，带有具体原因，调试更快。

解包数量不匹配时抛 `ValueError: not enough values to unpack`。

各 API tool call 字段差异：Claude 用 `input`，OpenAI 用 `function.arguments`（JSON 字符串需再次 `json.loads()`）。

### Task 5：执行工具，把结果喂回模型

完成时间：2026-06-25

代码：`stage-1/task5_execute.py`

完整单轮工具调用流程：
1. messages = [system, user]
2. 第一轮调模型 → type=tool_use → 执行工具
3. 追加 role=assistant（tool_use 记录）+ role=tool（执行结果）到 messages
4. 第二轮调模型 → type=text → 最终回答

关键：`role=assistant` 和 `role=tool` 必须成对追加。只追加 tool 结果会让消息结构损坏，API 会拒绝或模型无法理解凭空出现的工具结果。

模型没有记忆，每次调用看到的就是完整 messages 列表，工具结果必须显式追加进去模型才能"知道"。

检查题修正：
- 第 2 题用户说"有可能 len 为 1"，方向对但原因需补全：真实 loop 里模型可能连续调用多次工具，messages 长度一直变，固定数字判断轮次完全不可靠。正确做法是检查响应 type，用 while 循环（Task 6）。

### Task 6：agent loop + 最大步数 + 超时 + 错误处理

完成时间：2026-06-25

代码：`stage-1/task6_agent_loop.py`

loop 结构：`for step in range(1, MAX_STEPS + 1)` 替代写死轮次，检查 response type 决定继续还是退出。

三道保险：
1. 超时：每步检查 `time.time() - start_time > TIMEOUT_SECONDS`。
2. 工具错误：`try/except` 包裹 `run_tool()`，错误作为观察结果追加进 messages，loop 不中断。
3. 最大步数：for 循环走完仍无 text 回复，循环后返回超出步数提示。

关键设计原则：工具错误是**观察结果**，不是终止信号。模型看到错误后自行决定下一步（解释、重试或放弃）。如果工具错误直接终止 loop，agent 会过于脆弱。

loop 只有一个正常出口（`type == "text"` 时 return），其余出口均为异常保护。

检查题修正：
- 第 1 题用户说"输出错误信息便于查看"方向对，但核心原因需补全：工具错误是观察结果，设计上不应终止 loop，让模型决定如何响应。

## 阶段产出

- 预期产出：一个 50-150 行的最小 agent，可以选择工具、执行工具、返回最终答案。
- 实际产出：`stage-1/task6_agent_loop.py`，包含完整 agent loop、工具注册表、三道保险，覆盖正常/无限循环/工具错误三种场景。
- 全部代码文件：
  - `stage-1/chat.py` — Task 1 普通对话
  - `stage-1/task2_json.py` — Task 2 结构化 JSON
  - `stage-1/task3_tools.py` — Task 3 工具定义与注册表
  - `stage-1/task4_tool_call.py` — Task 4 解析 tool call
  - `stage-1/task5_execute.py` — Task 5 执行工具并回填
  - `stage-1/task6_agent_loop.py` — Task 6 完整 agent loop

## 下一步

Stage 1 全部完成。进入 Stage 2：Learn Tool Use, RAG, And Memory。

## 续接记录

2026-06-25：Stage 1 全部完成（Task 1-6）。用 Python + mock 跑通了完整 agent loop。所有代码在 `stage-1/` 目录。下次从 Stage 2 开始，先选择 Stage 2 的第一个任务。
