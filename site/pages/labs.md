---
title: 实验室
description: Stage 1-9 离线核心实验
---

# 实验室

| Stage | Lab | 默认路径 | 验证 |
| --- | --- | --- | --- |
| S01 | LLM 契约 | Mock Provider | `uv run pytest labs/stage-01-llm-contracts/tests` |
| S02 | Agent Loop | 安全计算器 | `uv run pytest labs/stage-02-agent-loop/tests` |
| S03 | RAG 与 Memory | n-gram + SQLite | `uv run pytest labs/stage-03-rag-and-memory/tests` |
| S04 | 可靠性与安全 | deny-by-default | `uv run pytest labs/stage-04-reliability-and-safety/tests` |
| S05 | Harness 与 Evals | 20 条固定集 | `uv run pytest labs/stage-05-harness-and-evals/tests` |
| S06 | Skills 与协议 | 本地只读 | `uv run pytest labs/stage-06-skills-and-protocols/tests` |
| S07 | Browser | 受控 localhost | `npx playwright test` |
| S08 | Multi-Agent | 确定性模拟 | `uv run pytest labs/stage-08-multi-agent/tests` |
| S09 | Capstone | 本地模板 | `uv run pytest labs/stage-09-capstone/tests` |

每个 Lab 都包含 Starter、Solution、Tests、Fixtures 和 Expected。可选真实 Provider 或容器实验在依赖不可用时必须明确跳过。
