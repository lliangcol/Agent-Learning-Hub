# Upstream audit report

- Generated: `2026-07-20T08:18:46+00:00`
- Local source commit: `842d45fc1ebac4ca03f280f973d0bdcdab5bd3e6`
- Upstream: [Datawhale Agent Learning Hub](https://github.com/datawhalechina/Agent-Learning-Hub)
- Upstream commit: `dddf777dde6788228136862f270203424a28efbc`
- Policy: report-only; this audit never merges, pushes, or opens issues.

| Path | Upstream vs baseline | Line delta | V2 action |
| --- | --- | ---: | --- |
| `README.md` | changed | +22/-16 | map semantic changes into curriculum sources |
| `CONTRIBUTING.md` | unchanged | +0/-0 | none |
| `LICENSE` | unchanged | +0/-0 | none |
| `.gitignore` | unchanged | +0/-0 | none |
| `index.html` | changed | +11/-5 | map semantic changes into curriculum sources |

## Upstream changes since local baseline

```text
Local baseline is not present in upstream history.
```

```text
A history-based diff is unavailable; file hashes were compared.
```

## Content delta requiring review

### `README.md`

```diff
--- baseline/README.md
+++ upstream/README.md
@@ -35,7 +35,7 @@

-- [x] 区分 chatbot、workflow、agent、multi-agent。
-- [x] 理解 agent 的基本循环：observe -> think -> act -> observe。
-- [x] 明白什么时候不该用 agent：任务可预测、流程稳定、普通脚本能解决时，agent 反而增加不确定性。
-- [x] 读完 [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)。
-- [x] 读完 [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)。
+- [ ] 区分 chatbot、workflow、agent、multi-agent。
+- [ ] 理解 agent 的基本循环：observe -> think -> act -> observe。
+- [ ] 明白什么时候不该用 agent：任务可预测、流程稳定、普通脚本能解决时，agent 反而增加不确定性。
+- [ ] 读完 [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)。
+- [ ] 读完 [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)。

@@ -45,8 +45,8 @@

-- [x] 会用一个 LLM API 完成普通对话。
-- [x] 会让模型输出结构化 JSON。
-- [x] 会定义一个工具函数，例如 search、calculator、read_file。
-- [x] 会解析模型的 tool call / function call。
-- [x] 会执行工具，并把工具结果喂回模型。
-- [x] 会给 agent loop 加最大步数、超时和错误处理。
+- [ ] 会用一个 LLM API 完成普通对话。
+- [ ] 会让模型输出结构化 JSON。
+- [ ] 会定义一个工具函数，例如 search、calculator、read_file。
+- [ ] 会解析模型的 tool call / function call。
+- [ ] 会执行工具，并把工具结果喂回模型。
+- [ ] 会给 agent loop 加最大步数、超时和错误处理。

@@ -250,3 +250,4 @@
 | Coding Agents | [Claude Code](https://code.claude.com/docs/en/overview), [OpenAI Codex](https://github.com/openai/codex), [OpenCode](https://github.com/opencode-ai/opencode), [OpenHands](https://github.com/All-Hands-AI/OpenHands), [SWE-agent](https://github.com/SWE-agent/SWE-agent), [pi](https://github.com/earendil-works/pi) | 真实代码库编辑、shell、测试、sandbox、PR 工作流。 |
-| Deep Research / RAG Agents | [DeerFlow](https://github.com/bytedance/deer-flow), [LlamaIndex](https://docs.llamaindex.ai/) | 搜索、抓取、检索、rerank、引用、报告生成。 |
+| Agent Harness / SuperAgent Runtime | [DeerFlow](https://github.com/bytedance/deer-flow), [LangGraph](https://langchain-ai.github.io/langgraph/) | 长任务执行、sandbox、memory、skills、subagents、message gateway、trace。 |
+| Deep Research / RAG Agents | [GPT Researcher](https://github.com/assafelovic/gpt-researcher), [Open Deep Research](https://github.com/langchain-ai/open_deep_research), [LlamaIndex](https://docs.llamaindex.ai/) | 搜索、抓取、检索、rerank、引用、报告生成。 |
 | Tutorial Encyclopedias | [GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents), [hello-agents](https://github.com/datawhalechina/hello-agents), [smolagents](https://github.com/huggingface/smolagents), [agents-towards-production](https://github.com/NirDiamant/agents-towards-production) | 横向看 ReAct、Plan-and-Execute、Multi-Agent、production patterns。 |
@@ -259,6 +260,6 @@
 | Skills | [Claude Code Skills](https://code.claude.com/docs/en/skills), [OpenClaw Skills](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md) | 把一类任务的流程知识、脚本、模板和验收标准打包成可复用能力。 |
-| MCP | [Model Context Protocol](https://modelcontextprotocol.io/) | 让 agent 标准化连接外部工具、数据源和服务。 |
+| MCP | [Model Context Protocol](https://modelcontextprotocol.io/), [官方 MCP Servers 合集](https://github.com/modelcontextprotocol/servers) | 让 agent 标准化连接外部工具、数据源和服务；官方 servers 合集涵盖文件系统、数据库、搜索、浏览器等常见场景，是学 MCP 接入最直接的参考。 |
 | A2A | [Agent2Agent Protocol](https://a2a-protocol.org/latest/specification/) | 让不同 agent 之间发现、通信和协作。 |
 | ACP | [Agent Client Protocol](https://agentclientprotocol.com/) | 让编辑器、终端、IDE、宿主应用和 agent 之间形成统一接口。 |
-| Skill Quality | [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401), [Agent Skills analysis](https://arxiv.org/abs/2602.08004) | 评估 skills 是否真的提升成功率，而不是制造新的 prompt 噪声。 |
+| Skill Quality | [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401), [Agent Skills analysis](https://arxiv.org/abs/2602.08004), [SkillOpt](https://github.com/microsoft/SkillOpt) | 评估、优化和验证 skills 是否真的提升成功率，而不是制造新的 prompt 噪声。 |

@@ -275,3 +276,3 @@
 | [CyberClaw](https://github.com/ttguy0707/CyberClaw) | 透明可控 agent 架构，适合研究审计、两段式执行和安全边界。 |
-| [DeerFlow](https://github.com/bytedance/deer-flow) | 字节开源 long-horizon SuperAgent harness，适合研究 Deep Research、报告、slides、网页、图像和视频生成。 |
+| [DeerFlow](https://github.com/bytedance/deer-flow) | 字节开源 long-horizon SuperAgent harness。2.0 主分支是从头重写的通用 agent runtime，适合研究 sandbox、memory、skills、subagents、message gateway 和长任务执行；原 Deep Research 框架在 1.x 分支。 |
 | [smolagents](https://github.com/huggingface/smolagents) | Hugging Face 轻量 agent 框架，CodeAgent 思路值得研究。 |
@@ -305,2 +306,5 @@
 | [SWE-bench](https://arxiv.org/abs/2310.06770) | 真实 GitHub issue 修复评测。 |
+| [GAIA](https://arxiv.org/abs/2311.12983) | 通用 AI 助手基准，测推理、多模态、工具使用；人类 92% vs GPT-4 15%，差距揭示 agent 能力上限。 |
+| [OSWorld](https://arxiv.org/abs/2404.07972) | 真实操作系统环境下的多模态 agent benchmark，覆盖 Ubuntu / Windows / macOS；适合 Stage 6 计算机操作 agent 学习。 |
+| [τ-bench](https://arxiv.org/abs/2406.12045) | 测量 tool-agent-user 三方动态交互；GPT-4o 在真实场景成功率不足 50%，pass^8 不足 25%，是评估 agent 可靠性的重要参照。 |
 | [SWE-agent](https://arxiv.org/abs/2405.15793) | 软件工程 agent 的 agent-computer interface。 |
@@ -321,3 +325,3 @@
 | [ttguy0707/CyberClaw](https://github.com/ttguy0707/CyberClaw) | 研究透明 agent、安全审计、两段式执行、双水位记忆和心跳任务。 |
-| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | Deep Research / long-horizon agent，适合学习搜索、报告生成、沙箱、memory、skills、subagents、message gateway。 |
+| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 2.0 是通用 long-horizon SuperAgent harness，适合学习沙箱、memory、skills、subagents、message gateway 和产物生成；Deep Research 代码看 1.x 分支。 |
 | [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) | 综合教程库，适合横向比较 ReAct、Plan-and-Execute、Multi-Agent 等实现方式。 |
@@ -327,2 +331,4 @@
 | [opencode-ai/opencode](https://github.com/opencode-ai/opencode) | 终端优先的开源 coding agent，适合对照 Claude Code / Codex。 |
+| [Aider-AI/aider](https://github.com/Aider-AI/aider) | 终端 AI pair programming 工具，支持多模型，与 git 深度集成；是最早期也最活跃的 coding agent 之一，对照 Claude Code 视角学习价值高。 |
+| [block/goose](https://github.com/block/goose) | Block 出品的开源可扩展 AI agent，支持安装、执行、编辑、测试，不限于代码建议；架构和 skills 设计值得研究。 |
 | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 状态图和可控 agent 编排。 |
```

### `index.html`

```diff
--- baseline/index.html
+++ upstream/index.html
@@ -518,3 +518,4 @@
       ['Coding Agents','<a href="https://code.claude.com/docs/en/overview" target="_blank">Claude Code</a>, <a href="https://github.com/openai/codex" target="_blank">OpenAI Codex</a>, <a href="https://github.com/opencode-ai/opencode" target="_blank">OpenCode</a>, <a href="https://github.com/All-Hands-AI/OpenHands" target="_blank">OpenHands</a>, <a href="https://github.com/SWE-agent/SWE-agent" target="_blank">SWE-agent</a>, <a href="https://github.com/earendil-works/pi" target="_blank">pi</a>','真实代码库编辑、shell、测试、sandbox、PR 工作流。'],
-      ['Deep Research / RAG Agents','<a href="https://github.com/bytedance/deer-flow" target="_blank">DeerFlow</a>, <a href="https://docs.llamaindex.ai/" target="_blank">LlamaIndex</a>','搜索、抓取、检索、rerank、引用、报告生成。'],
+      ['Agent Harness / SuperAgent Runtime','<a href="https://github.com/bytedance/deer-flow" target="_blank">DeerFlow</a>, <a href="https://langchain-ai.github.io/langgraph/" target="_blank">LangGraph</a>','长任务执行、sandbox、memory、skills、subagents、message gateway、trace。'],
+      ['Deep Research / RAG Agents','<a href="https://github.com/assafelovic/gpt-researcher" target="_blank">GPT Researcher</a>, <a href="https://github.com/langchain-ai/open_deep_research" target="_blank">Open Deep Research</a>, <a href="https://docs.llamaindex.ai/" target="_blank">LlamaIndex</a>','搜索、抓取、检索、rerank、引用、报告生成。'],
       ['Tutorial Encyclopedias','<a href="https://github.com/NirDiamant/GenAI_Agents" target="_blank">GenAI_Agents</a>, <a href="https://github.com/datawhalechina/hello-agents" target="_blank">hello-agents</a>, <a href="https://github.com/huggingface/smolagents" target="_blank">smolagents</a>, <a href="https://github.com/NirDiamant/agents-towards-production" target="_blank">agents-towards-production</a>','横向看 ReAct、Plan-and-Execute、Multi-Agent、production patterns。'],
@@ -527,6 +528,6 @@
       ['Skills','<a href="https://code.claude.com/docs/en/skills" target="_blank">Claude Code Skills</a>, <a href="https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md" target="_blank">OpenClaw Skills</a>','把一类任务的流程知识、脚本、模板和验收标准打包成可复用能力。'],
-      ['MCP','<a href="https://modelcontextprotocol.io/" target="_blank">Model Context Protocol</a>','让 agent 标准化连接外部工具、数据源和服务。'],
+      ['MCP','<a href="https://modelcontextprotocol.io/" target="_blank">Model Context Protocol</a>, <a href="https://github.com/modelcontextprotocol/servers" target="_blank">官方 MCP Servers 合集</a>','让 agent 标准化连接外部工具、数据源和服务；官方 servers 合集涵盖文件系统、数据库、搜索、浏览器等常见场景，是学 MCP 接入最直接的参考。'],
       ['A2A','<a href="https://a2a-protocol.org/latest/specification/" target="_blank">Agent2Agent Protocol</a>','让不同 agent 之间发现、通信和协作。'],
       ['ACP','<a href="https://agentclientprotocol.com/" target="_blank">Agent Client Protocol</a>','让编辑器、终端、IDE、宿主应用和 agent 之间形成统一接口。'],
-      ['Skill Quality','<a href="https://arxiv.org/abs/2603.15401" target="_blank">SWE-Skills-Bench</a>, <a href="https://arxiv.org/abs/2602.08004" target="_blank">Agent Skills analysis</a>','评估 skills 是否真的提升成功率，而不是制造新的 prompt 噪声。']
+      ['Skill Quality','<a href="https://arxiv.org/abs/2603.15401" target="_blank">SWE-Skills-Bench</a>, <a href="https://arxiv.org/abs/2602.08004" target="_blank">Agent Skills analysis</a>, <a href="https://github.com/microsoft/SkillOpt" target="_blank">SkillOpt</a>','评估、优化和验证 skills 是否真的提升成功率，而不是制造新的 prompt 噪声。']
     ]
@@ -543,3 +544,3 @@
       ['<a href="https://github.com/ttguy0707/CyberClaw" target="_blank">CyberClaw</a>','透明可控 agent 架构，适合研究审计、两段式执行和安全边界。'],
-      ['<a href="https://github.com/bytedance/deer-flow" target="_blank">DeerFlow</a>','字节开源 long-horizon SuperAgent harness，适合研究 Deep Research、报告、slides、网页、图像和视频生成。'],
+      ['<a href="https://github.com/bytedance/deer-flow" target="_blank">DeerFlow</a>','字节开源 long-horizon SuperAgent harness。2.0 主分支是从头重写的通用 agent runtime，适合研究 sandbox、memory、skills、subagents、message gateway 和长任务执行；原 Deep Research 框架在 1.x 分支。'],
       ['<a href="https://github.com/huggingface/smolagents" target="_blank">smolagents</a>','Hugging Face 轻量 agent 框架，CodeAgent 思路值得研究。'],
@@ -571,2 +572,5 @@
       ['<a href="https://arxiv.org/abs/2310.06770" target="_blank">SWE-bench</a>','真实 GitHub issue 修复评测。'],
+      ['<a href="https://arxiv.org/abs/2311.12983" target="_blank">GAIA</a>','通用 AI 助手基准，测推理、多模态、工具使用；人类 92% vs GPT-4 15%，差距揭示 agent 能力上限。'],
+      ['<a href="https://arxiv.org/abs/2404.07972" target="_blank">OSWorld</a>','真实操作系统环境下的多模态 agent benchmark，覆盖 Ubuntu / Windows / macOS；适合 Stage 6 计算机操作 agent 学习。'],
+      ['<a href="https://arxiv.org/abs/2406.12045" target="_blank">τ-bench</a>','测量 tool-agent-user 三方动态交互；GPT-4o 在真实场景成功率不足 50%，pass^8 不足 25%，是评估 agent 可靠性的重要参照。'],
       ['<a href="https://arxiv.org/abs/2405.15793" target="_blank">SWE-agent</a>','软件工程 agent 的 agent-computer interface。'],
@@ -587,3 +591,3 @@
       ['<a href="https://github.com/ttguy0707/CyberClaw" target="_blank">ttguy0707/CyberClaw</a>','研究透明 agent、安全审计、两段式执行、双水位记忆和心跳任务。'],
-      ['<a href="https://github.com/bytedance/deer-flow" target="_blank">bytedance/deer-flow</a>','Deep Research / long-horizon agent，适合学习搜索、报告生成、沙箱、memory、skills、subagents、message gateway。'],
+      ['<a href="https://github.com/bytedance/deer-flow" target="_blank">bytedance/deer-flow</a>','2.0 是通用 long-horizon SuperAgent harness，适合学习沙箱、memory、skills、subagents、message gateway 和产物生成；Deep Research 代码看 1.x 分支。'],
       ['<a href="https://github.com/NirDiamant/GenAI_Agents" target="_blank">NirDiamant/GenAI_Agents</a>','综合教程库，适合横向比较 ReAct、Plan-and-Execute、Multi-Agent 等实现方式。'],
@@ -593,2 +597,4 @@
       ['<a href="https://github.com/opencode-ai/opencode" target="_blank">opencode-ai/opencode</a>','终端优先的开源 coding agent，适合对照 Claude Code / Codex。'],
+      ['<a href="https://github.com/Aider-AI/aider" target="_blank">Aider-AI/aider</a>','终端 AI pair programming 工具，支持多模型，与 git 深度集成；是最早期也最活跃的 coding agent 之一，对照 Claude Code 视角学习价值高。'],
+      ['<a href="https://github.com/block/goose" target="_blank">block/goose</a>','Block 出品的开源可扩展 AI agent，支持安装、执行、编辑、测试，不限于代码建议；架构和 skills 设计值得研究。'],
       ['<a href="https://github.com/langchain-ai/langgraph" target="_blank">langchain-ai/langgraph</a>','状态图和可控 agent 编排。'],
```

## Review boundary

Absorbing content requires schema validation, attribution and license review.
A maintainer must approve the PR. Add the remote only for interactive comparison:

```powershell
git remote add upstream https://github.com/datawhalechina/Agent-Learning-Hub.git
git fetch --no-tags upstream main
```

The audit command itself does not change Git remotes or the working tree.
