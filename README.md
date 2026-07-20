# Agent Learning Hub

> 一个离线优先、可验证、可迁移的 AI Agent 学习实验室。

## 快速开始

Python 3.11+；推荐使用 uv。核心路径不需要 API key。

```powershell
uv sync --all-extras --dev --locked
uv run pytest
uv run python tools/validate_content.py
npm ci
npm run build
uv run mkdocs serve
```

使用标准 venv：

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev,site,protocol]"
.venv\Scripts\python -m pytest
```

真实 OpenAI Provider 是可选扩展。复制 `.env.example` 的变量名到本地环境；不要提交密钥。

## 课程路线

Roadmap version: `2.0.0`。个人进度不写回本列表。

| 阶段 | 主题 | 任务数 | 正文 |
| --- | --- | ---: | --- |
| `S00` | Agent 适用性与边界 | 5 | [stage-00-foundations](curriculum/stages/stage-00-foundations.md) |
| `S01` | LLM API 与结构化契约 | 3 | [stage-01-llm-contracts](curriculum/stages/stage-01-llm-contracts.md) |
| `S02` | Agent Loop 与工具调用 | 3 | [stage-02-agent-loop](curriculum/stages/stage-02-agent-loop.md) |
| `S03` | RAG、上下文与记忆 | 3 | [stage-03-rag-and-memory](curriculum/stages/stage-03-rag-and-memory.md) |
| `S04` | 可靠性、权限与安全 | 8 | [stage-04-reliability-and-safety](curriculum/stages/stage-04-reliability-and-safety.md) |
| `S05` | Harness、Trace 与 Evals | 5 | [stage-05-harness-and-evals](curriculum/stages/stage-05-harness-and-evals.md) |
| `S06` | Skills 与协议 | 8 | [stage-06-skills-and-protocols](curriculum/stages/stage-06-skills-and-protocols.md) |
| `S07` | Browser 与 Computer Use | 5 | [stage-07-browser-and-computer-use](curriculum/stages/stage-07-browser-and-computer-use.md) |
| `S08` | Multi-Agent 协调 | 5 | [stage-08-multi-agent](curriculum/stages/stage-08-multi-agent.md) |
| `S09` | Capstone | 5 | [stage-09-capstone](curriculum/stages/stage-09-capstone.md) |

## Project Ladder

项目进度与课程进度分开统计；所有项目均为可选。

| ID | 项目 | 轨道 | 难度 |
| --- | --- | --- | --- |
| `P01` | Calculator Agent | 基础工具 | beginner |
| `P02` | Web Research Agent | 研究与 RAG | beginner |
| `P03` | PDF QA Agent | 研究与 RAG | beginner |
| `P04` | Coding Review Agent | Coding Agent | intermediate |
| `P05` | Browser Agent | Browser 与 Computer Use | intermediate |
| `P06` | Claude Code-like Nano Agent | Coding Agent | intermediate |
| `P07` | OpenClaw-like Gateway | Personal Agent | intermediate |
| `P08` | Reusable Skill Pack | Skills 与协议 | intermediate |
| `P09` | Multi-Agent Writer | Multi-Agent | advanced |
| `P10` | Personal Agent | Personal Agent | advanced |
| `P11` | Production Harness | Production Harness | advanced |

## 事实源与个人数据

- `curriculum/roadmap.yaml`、`projects.yaml`、`resources.yaml` 是唯一结构化事实源。
- `workbook/local/`、浏览器笔记、导出进度和 SQLite 记忆默认不进入 Git。
- V1 资产与迁移证据保存在 `workbook/archive/legacy-v1/`。
- 资源目录当前有 57 个 active、23 个待外链复核项；状态不会被隐藏。

## 质量与安全

- 默认 Labs 离线运行，不执行任意不可信代码。
- 普通子进程不被称为沙箱；详见 `SECURITY.md` 与 ADR-0005。
- CI 验证 Python、内容、前端、MkDocs、链接与浏览器核心路径。

## 贡献与上游

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。项目保留 Datawhale 上游、原维护者及
外部贡献者署名；上游同步只生成差异报告，不自动合并。

## Maintainer

Curated by [陈思州](https://github.com/jjyaoao), Datawhale member。

## License

MIT。外部链接内容仍受各自许可证和访问条款约束。
