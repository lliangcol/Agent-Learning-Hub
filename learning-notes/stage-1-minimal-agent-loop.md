# Stage 1: Build A Minimal Agent Loop

来源：`README.md` -> `Learning Todo List` -> `Stage 1: Build A Minimal Agent Loop`

## 学习目标

这个阶段的目标是从“理解 agent 是什么”进入“能写出最小可运行 agent”。先不要追求复杂框架，重点是把一次模型调用、结构化输出、工具定义、工具执行、结果回填、停止条件和错误处理串起来。

## 当前进度

- [ ] 会用一个 LLM API 完成普通对话。
- [ ] 会让模型输出结构化 JSON。
- [ ] 会定义一个工具函数，例如 `search`、`calculator`、`read_file`。
- [ ] 会解析模型的 tool call / function call。
- [ ] 会执行工具，并把工具结果喂回模型。
- [ ] 会给 agent loop 加最大步数、超时和错误处理。

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

## 待实践任务

### 任务 1：普通 LLM API 对话

目标：先完成一次最小的普通对话调用，不引入工具。

验收标准：

- 能通过命令运行示例。
- 输入一条用户消息后，模型返回一段回答。
- 记录使用的模型/API、运行命令、示例输入和示例输出。
- 如果当前环境没有 API key，也要记录缺失项，并给出下一步配置方式。

当前检查结果：

- 检查时间：2026-06-12
- 已检查环境变量：`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`GEMINI_API_KEY`、`GOOGLE_API_KEY`、`GOOGLE_GENERATIVE_AI_API_KEY`
- 结果：均未配置。
- 仓库内未发现 `.env`、`package.json`、`pyproject.toml`、`requirements*.txt` 或现成 Python/JS/TS 示例。
- 结论：任务 1 暂不能完成真实 API 调用；下一步需要先选择 provider 并配置 key，或先用本地 mock 练习程序结构。

## 阶段产出

- 预期产出：一个 50-150 行的最小 agent，可以选择工具、执行工具、返回最终答案。
- 当前产出：尚未开始。
- 保存位置：尚未创建代码产物；完成普通 LLM API 对话后再记录具体文件。

## 验证方式

每完成一个小任务后，都要记录：

- 运行命令。
- 关键输出。
- 是否通过。
- 如果失败，失败原因和下一步修正。

## 下一步

开始任务 1：会用一个 LLM API 完成普通对话。

当前没有可用 API key。下一步先选择一种方案：

1. 配置真实 API：OpenAI、Claude 或 Gemini。
2. 先用本地 mock 练习普通对话程序结构，之后再替换成真实 API。

## 续接记录

2026-06-12：Stage 0 已完成，进入 Stage 1。已检查常见 API key，当前均未配置。下一步先配置 provider，或用本地 mock 练习普通对话结构；不急着加入 tool call。
