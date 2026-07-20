# Agent Learning Hub V2 完整执行计划

> - 文档状态：待执行计划（本文件只定义未来工作，不代表任何整改项已经执行）
> - 计划版本：1.3
> - Review 状态：R7 通过；本轮无新增问题
> - 编制日期：2026-07-20
> - 基线分支：`main`
> - 基线提交：`842d45f`
> 适用仓库：`D:\Repositories\Agent-Learning-Hub`

## 1. 计划目标与硬边界

### 1.1 总目标

将当前“README 学习路线、个人学习笔记、零散 Python 示例、单文件静态网站”混合形态，升级为一个边界清晰、内容可维护、实验可验证、进度有证据、站点可自动发布的 **Agent Learning Lab**。

目标产品由四个相互解耦的部分组成：

1. **公共课程（Curriculum）**：定义阶段、任务、前置条件、产出与验收标准。
2. **可运行实验（Labs）**：提供离线默认、真实 API 可选、跨平台验证的实践代码。
3. **个人工作簿（Workbook）**：保存学习进度、回答、修正和证据，不污染公共课程状态。
4. **静态学习站点（Site）**：从课程唯一数据源构建，提供导航、搜索、进度和笔记能力。

### 1.2 本计划编制任务的硬边界

- 当前任务只允许新增和修订本执行计划文件。
- 当前任务不得修改现有源码、README、学习笔记、网站、配置、依赖、测试或 Git 状态。
- 当前任务不得执行本计划中的安装、迁移、构建、测试、发布、同步、提交或推送操作。
- 本文中的命令、路径和文件清单均为未来执行说明，不表示已经运行或创建。
- 若未来执行期间发现范围外问题，先记录到变更控制区，不得静默扩大整改范围。

### 1.3 目标范围

本计划覆盖：

- 项目定位与上下游关系
- 信息架构与唯一事实源
- 课程体系与学习完成规则
- Python 实验架构与安全整改
- RAG、工具、记忆实现升级
- 静态网站、安全、移动端和无障碍
- 个人进度迁移与隐私边界
- 测试、CI、发布、依赖和链接治理
- 贡献流程、版本化、回滚和长期维护

### 1.4 非目标

以下内容不纳入 V2 首次整改：

- 用户账号、登录、服务端数据库或云同步
- 付费、排行榜、社区、评论或课程运营后台
- 自建模型网关、生产级多租户 Agent 平台
- 默认执行任意用户代码的在线沙箱服务
- 一次性实现 Stage 0-9 的所有扩展项目
- 为追求形式完整而引入微服务、消息队列或复杂前端框架

## 2. 基线事实与问题登记

### 2.1 当前基线

| 项目 | 当前状态 |
| --- | --- |
| Git | `main` 与 `origin/main` 对齐，基线提交 `842d45f` |
| 跟踪文件 | 21 个 |
| 主要内容 | 9 个 Markdown、9 个 Python、1 个 HTML |
| 公共路线 | README 中 Stage 0-8，共 50 个课程项 |
| README 进度 | 11/50 已勾选 |
| Stage 2 笔记进度 | 3 项另行标为完成 |
| 网站进度 | localStorage 独立状态，课程 50 项与项目阶梯 11 项混算为 61 项 |
| 自动化 | 无测试、无 CI、无构建、无链接检查 |
| 运行验证 | 8 个示例可启动，`stage-2/tools_safety.py` 在 Windows 因 `resource` 模块缺失失败 |

### 2.2 已知问题分级

#### P0：执行前必须消除

1. 教学示例使用 `eval()`，可形成任意代码执行风险。
2. `tools_safety.py` 把普通子进程称为沙箱，但没有文件、网络、凭据和权限隔离。
3. `tools_safety.py` 当前无法在 Windows 运行。
4. 网站将搜索词和 Markdown 结果写入 `innerHTML`，存在 HTML/XSS 注入面。
5. 使用未固定版本、无完整性保护的远程 Markdown 依赖。
6. “真实 LLM API”“长期记忆”等完成状态与实际 mock/进程内实现不一致。
7. `CLAUDE.md` 仍把仓库描述成无可运行代码的文档仓库。

#### P1：V2 基础能力

1. README、HTML、学习笔记和 localStorage 形成多套事实源。
2. 没有稳定的 stage/task ID，无法可靠迁移进度。
3. 没有 Python 项目元数据、版本声明、依赖锁定或运行入口。
4. 没有自动化测试、跨平台验证和质量门禁。
5. 工具 schema、错误模型、调用超时、重试、幂等和引用校验不完整。
6. RAG 中文检索策略不一致；长期记忆不持久化。
7. 个人学习状态污染公共课程勾选状态。
8. 没有明确的上游同步与差异审计机制。

#### P2：体验与运营质量

1. 移动端隐藏主标签栏，功能入口不完整。
2. 清单、卡片和标签页缺少键盘及 ARIA 语义。
3. 网站无深链接、状态迁移、导入导出和隐私说明。
4. 资源无最后验证时间、失效状态或替代链接。
5. 贡献流程只覆盖 README，未覆盖代码、课程、网站和测试。
6. 无站点预览、发布、回滚、版本和变更日志。

### 2.3 必须保护的现有资产

- README 中的 Stage 0-8 路线和资源说明。
- `learning-notes/` 下现有回答、修正、续接锚点和阶段证据。
- `stage-1/` 与 `stage-2/` 中体现学习演进的示例代码。
- `index.html` 中已有的资源数据、样式偏好和交互意图。
- Git 历史、上游归属、维护者署名和许可证信息。
- 当前 localStorage 中可能存在的用户进度和 Markdown 笔记。

任何迁移必须先复制、映射、验证，再删除或替换旧入口；不得先删后补。

## 3. 已确定的架构决策

### 3.1 产品定位

- 仓库从“链接清单”升级为“可验证学习实验室”。
- 公共课程与个人学习状态严格分层。
- 保留对 Datawhale 上游的署名和来源说明，但本地 V2 允许形成独立的信息架构。

### 3.2 技术选择

| 领域 | 决策 | 原因 |
| --- | --- | --- |
| Python | Python 3.11+，`pyproject.toml` 管理 | 与现有实验一致，支持现代类型与工具链 |
| 环境 | 标准 `venv` 文档 + `uv` 推荐路径 | 保持通用性，同时提供快速可重复安装 |
| Python 质量 | pytest、ruff、mypy | 覆盖测试、格式/lint、类型边界 |
| 课程事实源 | YAML 元数据 + Markdown 正文 | 兼顾结构化校验与可读内容 |
| 静态站点 | MkDocs Material，版本在执行时固定到受审查的锁文件 | 适合文档型项目、搜索和 GitHub Pages，消除实现选型歧义 |
| 前端交互 | 少量模块化 JavaScript，不建设 SPA | 保持静态、低复杂度 |
| Markdown 笔记 | 固定版本解析器 + DOMPurify；或安全纯文本降级 | 消除当前 XSS 面 |
| 进度 | 带 schema version 的 JSON/localStorage | 无需后端，可迁移、可导入导出 |
| 长期记忆实验 | SQLite | 标准库可用、跨平台、真实持久化 |
| 任意代码执行 | 默认不提供；可选 Docker/WSL 隔离实验 | 普通子进程不能宣称沙箱 |
| 托管 | GitHub Pages + GitHub Actions | 静态项目足够，无需服务器 |

### 3.3 需要在执行开始时落盘的 ADR

未来执行时首先创建：

- `decisions/ADR-0001-product-boundary.md`
- `decisions/ADR-0002-curriculum-single-source.md`
- `decisions/ADR-0003-progress-and-privacy.md`
- `decisions/ADR-0004-static-site-stack.md`
- `decisions/ADR-0005-code-execution-boundary.md`
- `decisions/ADR-0006-upstream-sync-policy.md`

ADR 只能记录已确认决策，不得用来掩盖未解决问题。

## 4. 目标目录结构

以下为完成 V2 基础整改后的目标结构；迁移期间允许新旧结构短暂并存：

```text
Agent-Learning-Hub/
├─ README.md
├─ EXECUTION_PLAN.md
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ CLAUDE.md
├─ SECURITY.md
├─ LICENSE
├─ pyproject.toml
├─ uv.lock
├─ package.json
├─ package-lock.json
├─ mkdocs.yml
├─ .python-version
├─ .node-version
├─ .env.example
├─ .editorconfig
├─ .gitattributes
├─ curriculum/
│  ├─ index.md
│  ├─ roadmap.yaml
│  ├─ projects.yaml
│  ├─ resources.yaml
│  ├─ schemas/
│  │  ├─ roadmap.schema.json
│  │  ├─ projects.schema.json
│  │  ├─ resources.schema.json
│  │  └─ progress.schema.json
│  └─ stages/
│     ├─ stage-00-foundations.md
│     ├─ stage-01-llm-contracts.md
│     ├─ stage-02-agent-loop.md
│     ├─ stage-03-rag-and-memory.md
│     ├─ stage-04-reliability-and-safety.md
│     ├─ stage-05-harness-and-evals.md
│     ├─ stage-06-skills-and-protocols.md
│     ├─ stage-07-browser-and-computer-use.md
│     ├─ stage-08-multi-agent.md
│     └─ stage-09-capstone.md
├─ labs/
│  ├─ README.md
│  ├─ stage-01-llm-contracts/
│  ├─ stage-02-agent-loop/
│  ├─ stage-03-rag-and-memory/
│  └─ stage-04-reliability-and-safety/
├─ src/agent_learning_hub/
│  ├─ core/
│  ├─ providers/
│  ├─ tools/
│  ├─ retrieval/
│  ├─ memory/
│  ├─ policies/
│  └─ tracing/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ security/
│  └─ content/
├─ workbook/
│  ├─ README.md
│  ├─ template/
│  ├─ examples/
│  └─ archive/legacy-v1/
├─ site/
│  ├─ assets/
│  ├─ overrides/
│  └─ src/
├─ tools/
│  ├─ build_readme.py
│  ├─ validate_content.py
│  ├─ migrate_progress.py
│  ├─ check_resource_catalog.py
│  └─ audit_upstream.py
├─ decisions/
└─ .github/
   ├─ workflows/
   │  ├─ quality.yml
   │  ├─ pages.yml
   │  ├─ links.yml
   │  └─ upstream-audit.yml
   ├─ ISSUE_TEMPLATE/
   ├─ pull_request_template.md
   └─ dependabot.yml
```

## 5. 课程 V2 设计

### 5.1 阶段结构

| ID | 阶段 | 核心产出 | 完成证据 |
| --- | --- | --- | --- |
| S00 | Agent 适用性与边界 | Agent/Workflow 决策说明 | 检查题、场景分析、review 记录 |
| S01 | LLM API 与结构化契约 | 离线 mock + 可选真实 Provider | schema 测试、错误样例、可选真实调用证据 |
| S02 | Agent Loop 与工具调用 | 安全计算器 Agent + trace | 单元测试、循环退出、超时和未知响应测试 |
| S03 | RAG、上下文与记忆 | 带来源研究助手 + SQLite 记忆 | 检索评测、引用校验、跨进程持久化测试 |
| S04 | 可靠性、权限与安全 | 工具策略层 | 重试、幂等、审批、脱敏、安全回归测试 |
| S05 | Harness、Trace 与 Evals | 裸 loop/harness 对照实验 | 固定数据集、指标、失败分类和报告 |
| S06 | Skills 与协议 | 可复用 Skill 或 MCP 工具 | smoke test、触发条件、版本和验收结果 |
| S07 | Browser/Computer Use | 受控公开网站 Agent | DOM/截图/动作日志、失败恢复和权限证明 |
| S08 | Multi-Agent 协调 | 有监督者和停止条件的协作流 | 与单 Agent 基线对比、循环检测和成本指标 |
| S09 | Capstone | 可 clone、测试、部署的完整项目 | README、CI、评测、限制、发布和复盘 |

### 5.2 每个课程任务的强制字段

`roadmap.yaml` 中每个任务至少包含：

- `id`：永久稳定，例如 `S02-T03`
- `title`
- `status`：课程条目状态，不是个人完成状态
- `prerequisites`
- `learning_outcomes`
- `concepts`
- `lab_path`：可为 `null`；仅概念/决策类任务可为空，其余任务必须指向存在的 Lab
- `artifact`
- `rubric`
- `validation_commands`
- `failure_cases`
- `safety_notes`
- `resources`
- `estimated_effort`
- `introduced_in`
- `last_reviewed_at`

Project Ladder 使用独立 `projects.yaml`，不作为课程完成度的必修任务集合。

### 5.3 个人学习状态模型

个人进度不得继续使用单一布尔值。统一状态：

```text
not_started
  -> learning
  -> concept_verified
  -> lab_verified_offline
  -> lab_verified_live（仅任务要求真实服务时）
  -> complete
```

另设非进度状态：

- `blocked`
- `needs_revalidation`
- `validation_failed`

每次状态变化必须记录：

- task ID
- 状态
- 更新时间
- 证据路径
- review 结论
- 使用环境
- 下一步锚点

### 5.4 完成规则

任务只有同时满足以下条件才可标为 `complete`：

1. 必需概念检查已经回答并 review。
2. 必需 Lab 已完成，不只是阅读代码。
3. 自动化验证命令通过。
4. 失败场景至少验证一个。
5. 修正后理解已写入工作簿。
6. 证据路径存在且与 task ID 对应。
7. 当前进度已迁移到下一个明确锚点。

真实 API 是可选扩展时，离线 mock 可以完成核心任务；任务文字若明确要求“会调用真实 API”，则没有真实调用证据不得标为 `complete`。

## 6.0 Phase 0：执行准备与基线冻结

### P0-01 创建执行分支和基线标记

- **目标**：为后续整改建立可回退边界。
- **计划动作**：
  - 确认工作区干净、`HEAD` 和远端关系。
  - 创建 `feature/agent-learning-hub-v2`。
  - 记录基线提交 `842d45f`。
  - 是否创建 `v1-baseline` tag 必须单独获得确认；无确认时只记录 commit，不创建 tag。
- **验证**：分支基点等于基线提交，无遗失或隐式纳入的改动。
- **回滚**：删除未推送的执行分支即可；禁止 `reset --hard`。

### P0-02 生成资产清单与状态快照

- **目标**：保证迁移可审计。
- **计划文件**：`workbook/archive/legacy-v1/manifest.md`。
- **记录内容**：
  - 所有跟踪文件及摘要哈希
  - README 50 个任务及 11 个勾选状态
  - Stage 2 的 3 个完成记录
  - `PROGRESS.md` 当前锚点
  - 当前可运行命令和输出摘要
  - 已知 Windows 失败和编码问题
- **验证**：清单数量与 `git ls-files` 一致。
- **回滚**：该清单是新增文档，可单独撤销。

### P0-03 浏览器本地状态保护

- **目标**：网站重构前避免 localStorage 进度和笔记丢失。
- **计划动作**：
  - 先登记旧站点实际使用过的 origin，例如 `file://`、本地 HTTP 地址和 GitHub Pages；不同 origin 的 localStorage 互不共享，必须分别处理。
  - 先在旧页面增加只读导出能力，再切换新状态模型。
  - 导出旧键 `agent-learning-hub-state`、`note-${stageId}` 和主题值。
  - 输出带版本和导出时间的 JSON。
  - 在迁移测试通过前不删除或覆盖旧键。
- **用户协作边界**：仓库脚本和 CI 不得读取用户浏览器存储；每个实际使用过的 origin 需要用户打开旧页面并主动触发导出。
- **隐私边界**：导出文件只保存在用户明确选择的位置；不得提交个人笔记。
- **验证**：每个已登记 origin 都有“无数据”或“已导出”的明确记录；旧状态导出后可在隔离测试环境还原。

### P0-04 个人笔记隐私审计门

- **目标**：决定现有 `learning-notes/` 的公开去向。
- **默认决策**：未来个人工作簿默认本地私有并被 `.gitignore` 排除。
- **执行门**：
  - 逐文件检查账号、公司、内部项目、路径、凭据和个人敏感信息。
  - 无敏感内容时，原文件通过 `git mv` 进入 `workbook/archive/legacy-v1/`。
  - 有敏感内容时，停止迁移并请求用户决定“脱敏保留”或“历史清理”。
  - Git 历史重写不属于自动整改范围，必须获得单独授权。
- **验证**：隐私审计结果有记录，未把新个人状态加入版本控制。

### Phase 0 退出条件

- 基线和资产清单可复查。
- 旧进度、旧笔记和 localStorage 均有恢复路径。
- 个人内容公开边界已确认。
- 未开始任何不可逆迁移。

## 6.1 Phase 1：P0 安全与真实性整改

### P1-01 消除 `eval()` 教学风险

- **影响文件**：现有 Stage 1 计算器示例及迁移后的对应 Lab。
- **实现要求**：
  - 使用 `ast.parse(..., mode="eval")`。
  - 只允许数字、括号和明确列出的算术运算符。
  - 禁止名称、属性、调用、下标、容器、推导式和导入。
  - 设置表达式长度和 AST 节点数量上限。
  - 错误返回结构化、安全、可教学的结果。
- **必测场景**：
  - 正常四则运算
  - 除零
  - 超长表达式
  - `__import__`
  - 属性访问
  - 函数调用
  - 极大幂运算或资源消耗输入
- **验收**：仓库模型输入路径的残余搜索不存在危险 `eval/exec`。

### P1-02 纠正“沙箱”定义和跨平台实现

- **影响文件**：`stage-2/tools_safety.py`、课程说明、对应测试。
- **实现要求**：
  - 普通子进程示例改名为 `run_code_with_timeout_demo`，明确“不是安全沙箱”。
  - `resource` 条件导入，只在支持的平台启用。
  - Windows/Linux 都可运行教学主流程。
  - 默认实验不接受任意不可信代码。
  - 真正任意代码执行只进入可选容器实验：禁网络、只读根文件系统、临时工作区、非 root、CPU/内存/进程/时间/输出限制。
  - Docker/WSL 不可用时明确跳过，不能假装已验证。
- **验收**：Windows/Linux 主 Lab 通过；文档不再把普通子进程称为沙箱。

### P1-03 修复网站注入面

- **影响范围**：旧 `index.html` 紧急补丁与新站点实现。
- **实现要求**：
  - 搜索词只通过 `textContent` 输出。
  - 用户笔记经过固定版本解析器和 DOMPurify 清洗。
  - 解析器不可用时回退为转义纯文本，不允许原始 HTML。
  - 移除内联事件处理器，采用事件监听。
  - 添加 CSP meta，限制脚本、样式、图片和连接来源。
  - 外部新窗口链接增加 `rel="noopener noreferrer"`。
  - 依赖固定版本并通过锁文件安装，不运行“latest” CDN。
- **必测攻击样例**：`<script>`、事件属性、`javascript:`、SVG、Markdown 原始 HTML、恶意搜索词。
- **验收**：安全回归测试全部通过，页面无未经净化的用户输入 `innerHTML`。

### P1-04 校正完成状态和项目描述

- **影响文件**：README、Stage 1/2 笔记、PROGRESS、CLAUDE、课程迁移数据。
- **迁移原则**：不删除学习成果，只降低不满足证据的状态。
- **初始建议映射**：
  - Stage 0：保留 `complete`，前提是对应回答与 review 证据完整。
  - Stage 1 Task 1：`concept_verified` 或 `lab_verified_offline`，不得声称真实 API 已验证。
  - Stage 1 Task 2-6：按现有回答和离线代码映射为 `lab_verified_offline`；P1-01 安全整改完成后再复核。
  - Stage 2 Task 1：`needs_revalidation`，因为中文检索与引用完整性仍需补测。
  - Stage 2 Task 2：`validation_failed`，因为 Windows 当前不能运行且沙箱表述不准确。
  - Stage 2 Task 3：`lab_verified_offline`，但不得称为跨进程长期持久化。
  - Stage 2 Task 4：`learning`。
  - Stage 2 Task 5：`not_started`。
- **验收**：每个完成状态都能追溯到实际证据和环境。

### P1-05 建立威胁模型与安全响应入口

- **计划文件**：`SECURITY.md`、`decisions/ADR-0005-code-execution-boundary.md`、安全测试清单。
- **威胁范围**：
  - 模型生成的工具名、参数、路径和代码
  - 搜索结果、网页正文、Markdown 和导入进度文件
  - API key、日志、错误堆栈和工作簿隐私
  - CDN、Python/npm 依赖和 GitHub Actions
  - Pages 静态站点的 XSS、恶意链接和供应链风险
- **要求**：
  - 为每类威胁记录资产、信任边界、攻击路径、预防、检测和恢复。
  - `SECURITY.md` 提供私下报告安全问题的方式；未配置安全邮箱时使用 GitHub Private Vulnerability Reporting，并在执行前确认仓库能力。
  - 安全声明不得超出真实隔离和测试能力。
- **验收**：每个 P0 安全整改项都能映射到威胁模型和回归测试。

### Phase 1 退出条件

- P0 安全问题有回归测试。
- Windows 上的 Stage 2 工具示例不再导入失败。
- 站点用户输入路径完成净化。
- 项目描述与真实能力一致。
- 威胁模型覆盖代码执行、工具、站点、数据和供应链边界。
- 第一轮安全 re-review 不再产生新的 P0 问题。

## 6.2 Phase 2：工程基础与质量门禁

### P2-01 建立 Python 与 Node 项目元数据

- **计划文件**：`pyproject.toml`、`.python-version`、`uv.lock`、`package.json`、`package-lock.json`、`.node-version`、`.gitignore`、`.env.example`。
- **要求**：
  - `requires-python = ">=3.11"`。
  - `.python-version` 固定本地推荐版本；CI 同时验证最低支持版本和执行时核实的 Python 最新稳定版本。
  - `.node-version` 固定执行时的 Active LTS 主版本，并与 CI、开发文档一致。
  - 核心尽量使用标准库。
  - Provider、站点、开发工具使用 extras 分组。
  - Python/npm 依赖锁文件由受信任环境生成并 review。
  - README 同时提供 `venv + pip` 与 `uv` 两条路径。
  - `.gitignore` 明确排除 `.env`、`workbook/local/**`、导出的个人进度、构建产物、覆盖率和工具缓存；不得排除 `workbook/template/**`、`workbook/examples/**`、`workbook/archive/legacy-v1/**` 和测试 fixture。
  - `.env.example` 只提供变量名和安全说明，不包含真实密钥或可工作的示例凭据。
- **验证**：全新 Windows、Ubuntu 环境均能安装离线核心依赖。

### P2-02 建立编码和跨平台规范

- **计划文件**：`.editorconfig`、`.gitattributes`。
- **要求**：
  - 文本统一 UTF-8。
  - 明确 LF 策略，Windows 脚本例外需说明。
  - Python 不再替换 `sys.stdout`；由入口和文档统一处理终端编码。
  - 所有文件读写显式使用 UTF-8。
- **验证**：Windows/Ubuntu 输出中文一致，无乱码快照差异。

### P2-03 重构可测试的核心包

- **计划目录**：`src/agent_learning_hub/`。
- **模块边界**：
  - `core`：消息、Agent 状态、停止原因
  - `providers`：`LLMClient` 协议、Mock Provider、可选真实 Provider
  - `tools`：schema、注册表、执行结果、安全计算器
  - `policies`：权限、重试、幂等、预算、审批
  - `retrieval`：chunk、index、retrieve、citation
  - `memory`：session、SQLite、TTL、删除
  - `tracing`：step、tool call、latency、error、cost 占位
- **约束**：Lab 可以展示渐进代码，但最终参考实现不得复制多份核心逻辑。

### P2-04 建立测试层级

- **单元测试**：纯函数、schema、策略、分词、引用、TTL。
- **集成测试**：Agent loop + Mock Provider + 工具注册表。
- **安全测试**：计算器逃逸、路径穿越、SQL 注入、XSS、错误脱敏。
- **内容测试**：ID 唯一性、引用完整性、文件路径、任务关系。
- **覆盖率目标**：
  - 核心整体行覆盖率不低于 85%。
  - 安全计算器、权限策略、引用校验要求分支覆盖率 100%。
  - 覆盖率不得通过排除失败路径来达标。

### P2-05 建立 CI

- **`quality.yml`**：
  - Ubuntu + Windows
  - Python 最低支持版本、当前本机推荐版本、执行时核实的最新稳定版本；重复版本去重后生成矩阵
  - Node Active LTS，与 `.node-version` 一致
  - ruff format check
  - ruff lint
  - mypy
  - pytest + coverage
  - 内容 schema 校验
  - README 生成差异校验
  - Markdown lint 和内部链接检查
  - `npm ci`、前端单元测试和前端构建
  - Ubuntu 上的 Playwright/axe 核心路径；Windows 保留 Python 和内容矩阵，浏览器矩阵按稳定性单独扩展
  - 前端静态资产先构建，再执行 MkDocs strict build
- **真实 API 测试**：默认不在 PR CI 执行；只允许手动、受限 secrets 和预算上限。
- **验收**：全新 checkout 可以只按 CI 文件复现质量门禁。

### Phase 2 退出条件

- 项目具备确定的安装、测试和构建入口。
- Windows/Ubuntu CI 通过。
- 核心模块可导入而不产生演示输出或副作用。
- P0 回归测试进入永久门禁。

## 6.3 Phase 3：课程唯一事实源与进度迁移

### P3-01 定义 schema

- 创建 roadmap、projects、resources、progress 四个 JSON Schema。
- 定义版本升级规则：新增可选字段为 minor，删除/改义为 major。
- 所有 stage/task/project/resource ID 永久稳定；标题变化不得改变 ID。
- 课程条目 `status` 只允许 `draft`、`active`、`deprecated`、`archived`；它描述课程生命周期，不代表个人进度。
- `roadmap_version` 使用语义化版本，并在进度迁移和生成物中保留。
- 校验所有前置 task ID、项目 prerequisite、资源 replacement 和课程引用都指向存在且类型正确的 ID。
- task 前置关系必须是有向无环图；replacement 链不得成环，也不得指向自身。
- 验证器必须报告具体文件、字段和 ID。

### P3-02 迁移 Stage 0-9 课程结构

- 将 README 中现有 Stage 0-8 内容迁移到 `curriculum/`。
- 按 V2 结构拆分原 Stage 1/2，并新增 Stage 9 Capstone。
- 把安全、评测和可观测性前移为跨阶段要求。
- 每个任务补齐产出、rubric、失败案例和验证命令。
- 保留旧编号到新 task ID 的映射表。
- 迁移完成前保留旧 README 内容作为对照，不直接覆盖。

### P3-03 资源目录结构化

每条资源至少包含：

- `id`
- `title`
- `url`
- `source_type`
- `publisher`
- `stage_ids`
- `why_it_matters`
- `trust_level`
- `last_verified_at`
- `status`
- `replacement_id`
- `license_or_access_note`

规则：官方资料优先；同类资源控制数量；失效资源先归档，不直接丢失历史。

资源 `status` 只允许：

- `active`
- `suspect`
- `archived`
- `replaced`

### P3-04 README 和站点生成

- README 从模板与课程数据生成。
- 生成结果包含清晰项目定位、快速开始、课程摘要、贡献入口和上游归属。
- CI 执行生成器后必须保持 `git diff --exit-code`。
- 禁止同时手工维护 README 和 HTML 中的课程列表。

### P3-05 迁移个人进度

- 创建旧任务到 V2 ID 的显式映射。
- 迁移器支持 dry-run、报告、执行、校验四个阶段。
- 无法判断的状态使用 `needs_revalidation`，不得猜测 `complete`。
- 迁移后保留旧文件和旧 localStorage 键一个发布周期。
- 导入导出均验证 schema version 和 task ID。
- 导入前生成带时间、origin、schema version 和内容摘要的本地备份。
- 导入采用“解析 -> schema 校验 -> task ID 映射 -> 冲突预览 -> 用户确认 -> 单次替换”的原子流程。
- 错误导入不得部分覆盖现有状态；失败后自动恢复导入前备份并显示原因。
- 迁移报告分别列出成功、降级、未映射、冲突和拒绝项，数量总和必须等于输入项数。

### P3-06 课程与资源语义审计

- 对全部课程目标检查前置关系、难度递进、概念重复和安全内容是否过晚。
- 对“当前、现代、推荐、官方、生产级”等时效性描述重新核实，并记录核实日期。
- 技术事实只使用官方文档、标准、原始论文或项目仓库作为首选证据。
- 检查中英文术语是否一致；同一概念不得在不同页面使用冲突定义。
- 语言策略固定为：简体中文是课程叙述主语言，技术专有名词首次出现时给出英文；文件 slug、代码标识和协议正式名称保留英文；不再混用英文标题与中文正文而没有翻译规则。
- 删除“按 star 数推荐”等不可复现判断，改为与具体学习目标和验收能力绑定。
- 对上游新增内容逐项分类，不能因为本地结构变化而停止吸收高质量更新。
- 语义审计结果写入任务/资源的 `last_reviewed_at` 或 `last_verified_at`，并生成未解决清单。
- **验收**：没有未经核实的时效性断言；每个推荐项都能说明适用阶段和具体学习价值。

### P3-07 重构 Project Ladder

- 把当前 11 个项目迁移到 `projects.yaml`，为每个项目分配稳定 ID。
- 每个项目至少定义：
  - `id`
  - `title`
  - `track`
  - `difficulty`
  - `prerequisite_task_ids`
  - `artifact`
  - `rubric`
  - `validation_commands`
  - `safety_notes`
  - `estimated_effort`
  - `status`
- 项目轨道至少区分：基础工具、研究/RAG、Coding Agent、Browser/Computer Use、Skills/协议、Multi-Agent、Personal Agent、Production Harness。
- “等级”表示建议难度，不表示所有学习者必须线性完成；每个项目明确必修或可选属性。
- 个人项目进度使用独立 `project_progress` 命名空间，不计入课程任务总完成率。
- 当前 11 个项目全部建立旧序号到新项目 ID 的迁移映射。
- **验收**：项目列表只从 `projects.yaml` 生成；每个项目都有可检查产出和完成 rubric。

### Phase 3 退出条件

- README、站点输入和课程定义只有一个事实源。
- 50 个旧任务均有明确映射、合并或弃用说明。
- 11 个旧项目均有稳定 ID、独立进度和迁移映射。
- 个人进度迁移有 dry-run 报告和回滚路径。
- 课程、资源和进度 schema 校验全部通过。

## 6.4 Phase 4：Labs 和参考实现升级

### P4-01 Stage 1：LLM 契约

- Mock Provider 为默认路径，离线可运行。
- 提供一个可选 OpenAI Provider 适配示例；执行时依据官方文档核对当前 API，固定 SDK 版本，密钥只从环境变量读取。
- Provider 协议保持厂商中立，Anthropic/Gemini 作为后续扩展，不进入 V2 核心依赖。
- 不使用正则贪婪截取 JSON 作为推荐实现。
- 优先使用 Provider 结构化输出；否则使用严格 JSON decoder + schema 校验。
- 覆盖无 JSON、多 JSON、缺字段、错类型、超长输出和拒答。

### P4-02 Stage 2：Agent Loop

- 使用明确的 `AgentState` 和 `StopReason`。
- 识别 text、tool call、未知响应和 Provider 错误。
- 模型调用、工具调用分别配置超时。
- 最大步骤、总 deadline、工具预算、重复调用检测相互独立。
- 工具结果保持结构化，不用 `str(dict)` 冒充协议消息。
- Mock 最终回答必须基于真实工具结果生成，不能硬编码与结果无关的答案。

### P4-03 Stage 3：RAG

- 离线检索支持中文，算法可选字符 n-gram/BM25，但必须有固定评测集。
- chunk 保存文档 ID、标题、URI、偏移和正文。
- 检索返回结构化 score 和原因。
- 引用验证同时检查：
  - 引用 ID 真实存在
  - 必须引用的结论没有漏引
  - 引用内容确实支持对应结论
  - 无检索结果时不得生成来源型事实
- “支持对应结论”采用两层验收：离线核心答案使用可追踪的 claim-to-chunk 映射和确定性规则；自由生成答案使用固定人工标注集抽查，不把未经验证的 LLM-as-judge 结果作为唯一门禁。
- 真实 embedding 作为可选扩展，不成为离线核心门槛。

### P4-04 Stage 3：记忆

- Session memory 使用滑动窗口 + 累积摘要，避免每次无限重复摘要全部历史。
- 原始审计日志和模型上下文分开存储。
- Long-term memory 使用 SQLite 跨进程持久化。
- SQLite 使用独立 `schema_version`，每次结构变化提供向前迁移、迁移前备份和不兼容版本拒绝策略。
- 记录 key、内容、来源、创建/更新时间、TTL、记录版本和敏感级别。
- 支持覆盖、冲突、过期、删除和导出测试。
- 不将用户内容伪装为 system message。
- 长期写入必须经过显式策略：只保存未来会复用且允许持久化的信息；秘密、验证码、凭据、完整隐私文本默认拒绝。
- 提供查看、纠正、删除和清空记忆的接口，验证删除后不会继续被检索。
- 教学示例使用合成数据，不把真实个人信息写入 fixture、快照或日志。

### P4-05 Stage 4：工具可靠性和权限

- 统一 `ToolResult` 状态：`ok`、`empty`、`retryable_error`、`fatal_error`、`denied`。
- 重试只作用于明确可重试错误，使用最大次数、退避和抖动。
- 相同只读调用可以缓存；有副作用工具必须使用幂等 key。
- 连续无进展调用触发 loop guard。
- 文件读写分工具、分权限；写入前有路径和覆盖策略。
- 外部错误先脱敏，再进入模型上下文和用户输出。

### P4-06 Lab 统一结构

每个 Lab 包含：

```text
README.md
starter/
solution/
tests/
fixtures/
expected/
```

Lab README 必须说明：目标、前置条件、运行命令、预期输出、失败场景、安全限制、完成标准和扩展任务。

### P4-07 Stage 5：Harness、Trace 与 Evals 基线 Lab

- 用同一固定任务分别运行裸 Agent loop 和一个经 ADR 确认的现代 harness。
- 统一采集步骤、工具调用、停止原因、延迟、错误和可选成本字段。
- 建立不少于 20 条的离线固定评测集，包含成功、空结果、错误、重复调用和越权请求。
- 输出对比报告，不以 demo 是否“看起来聪明”作为完成标准。
- harness 版本必须锁定；若 API 漂移，先更新适配和回归测试。

### P4-08 Stage 6：Skills 与协议基线 Lab

- 创建一个最小可复用 Skill，包含触发条件、步骤、脚本/模板和验收标准。
- 创建一个只读、无外部副作用的最小 MCP 工具示例。
- 用固定任务对比“无 Skill”和“有 Skill”的成功率、步骤数和失败原因。
- A2A/ACP 在 V2 核心课程中以协议阅读和契约练习为主，不强制接入外部生产系统。

### P4-09 Stage 7：Browser/Computer Use 基线 Lab

- 只操作仓库提供的本地受控测试页或明确允许的公开测试站点。
- 不登录敏感账号、不处理验证码、不绕过权限或平台规则。
- 记录 DOM/截图、动作、观察、失败和停止原因。
- 覆盖页面变化、元素缺失、加载失败、弹窗和最大步骤。
- 浏览器测试环境、版本和允许域名必须固定并进入配置。

### P4-10 Stage 8：Multi-Agent 基线 Lab

- 先建立同一任务的单 Agent 基线。
- 多 Agent 只实现明确的 supervisor、worker、reviewer 边界。
- 输入输出使用 schema，设置总预算、最大轮次、无进展检测和停止条件。
- 评测成功率、成本、延迟和错误放大；若没有收益，结论允许为“不应使用多 Agent”。

### P4-11 Stage 9：Capstone 基线

- 提供三个可选方向：研究助手、代码审查助手、个人知识助手。
- 每个方向共享发布清单，但只要求学习者完成一个。
- 必须包含明确用户、任务、成功标准、固定评测集、权限边界、日志、部署和限制。
- 默认提供本地 CLI 或静态演示；外部发布、消息发送和生产数据访问不属于自动执行范围。
- Capstone 模板和示例必须可 clone、可安装、可测试、可移除 secrets。

### Phase 4 退出条件

- Stage 1-9 核心 Lab/模板全部可定位；Stage 1-6 离线核心路径跨平台通过，Stage 7-9 按其环境矩阵通过或给出明确、经验证的跳过条件。
- 课程声明与代码能力一致。
- 安全和失败路径具备自动化回归。
- 初学者不需要 API key 即可完成核心路径。

## 6.5 Phase 5：静态网站重建

### P5-01 站点信息架构

一级导航固定为：

1. 开始学习
2. 课程路线
3. 实验室
4. 项目阶梯
5. 资源目录
6. 我的工作簿
7. 贡献指南

课程、可选项目和个人进度分别统计，不再合并为一个总数。

站点基础元数据同时包含页面标题、描述、canonical URL、Open Graph、sitemap 和自定义 404；不添加用户追踪脚本。

### P5-02 进度与笔记

- 使用稳定 task ID，不用数组下标作为 key。
- 课程任务和项目分别使用 `task_progress`、`project_progress`，各自显示分母和完成率。
- localStorage 包含 `schema_version`、`roadmap_version` 和更新时间。
- 支持 JSON 导入、导出、预览和冲突策略。
- 导入失败保持原数据不变。
- 笔记默认只在本地浏览器保存，并显示隐私说明。
- 不实现账号或远端同步。

### P5-03 移动端和无障碍

- 360px 宽度能访问全部一级导航。
- 使用原生 button、checkbox、nav、main、heading。
- 标签页提供 `role=tab`、`aria-selected` 和键盘切换。
- 清单提供可见焦点、空格/回车操作和 `aria-checked`。
- 增加 skip link、H1、状态播报和错误提示关联。
- 颜色不作为唯一状态表达。
- 目标为 WCAG 2.2 AA；自动检查不能替代手工键盘和屏幕阅读器抽查。

### P5-04 搜索和路由

- 每阶段、任务、资源拥有稳定 URL。
- 搜索索引由构建生成，不直接搜索带 HTML 的字符串。
- 搜索高亮基于文本节点，不能破坏链接属性或标签结构。
- 刷新页面后保持当前路由，不依赖内存变量。

### P5-05 前端验证

- 单元测试：状态迁移、导入导出、搜索、净化。
- Playwright：桌面、768px、360px 核心路径。
- axe：阻断 critical/serious 问题。
- 安全测试：笔记和搜索恶意输入。
- 构建测试：断网条件下核心页面仍可加载，不依赖 latest CDN。

### P5-06 URL 与旧入口兼容

- 建立旧 README 锚点、旧 `index.html` 入口与 V2 页面之间的映射表。
- 保留可行的稳定锚点；无法直接重定向时提供迁移页和明确新链接。
- 增加 `404.html`，指导用户返回课程入口或搜索。
- 外部已分享链接抽样验证，避免站点升级后全部失效。
- legacy 入口保留到 `v2.1.0` 发布或 V2 正式发布满 30 天，以较晚者为准。

### P5-07 性能与离线退化

- 记录 V1 页面体积和核心交互基线。
- 设置站点构建产物和自定义 JavaScript 体积预算；预算值由 ADR 根据首次构建基线确定，后续增长必须解释。
- 核心课程正文在 JavaScript 失败时仍可阅读。
- 搜索、进度和笔记失败时提供明确降级提示，不影响静态课程访问。
- 对首页和课程页执行 Lighthouse 或等价检查，并把显著回归纳入 review。

### Phase 5 退出条件

- 移动端、键盘和主要屏幕阅读器语义通过检查。
- 旧进度和笔记可导入新站点。
- 用户输入不能执行脚本或破坏 DOM。
- 所有页面由课程事实源构建。
- 旧入口有兼容映射，JavaScript 失败时核心课程仍可阅读。

## 6.6 Phase 6：资源、上游和贡献治理

### P6-01 链接巡检

- PR 中检查新增/修改链接。
- 每周执行完整外链检查。
- 对 429、5xx 和超时重试，不因一次瞬时失败直接删除资源。
- 连续失败进入 `suspect`，人工确认后转 `archived`。
- 内部链接和资源 ID 失败必须阻断 PR。

### P6-02 上游同步

- 文档记录 `upstream` remote 配置方法。
- `audit_upstream.py` 只生成差异报告，不自动合并或创建外部 Issue。
- 差异分类：可直接吸收、需映射到 V2、仅上游适用、与本地冲突。
- 每次同步保持上游署名和链接。
- 上游合并必须经过课程 schema 和内容 review。

### P6-03 贡献治理

更新 `CONTRIBUTING.md`，分别定义：

- 课程修改
- 资源新增/归档
- Lab 代码
- 网站交互
- 个人示例工作簿
- 安全问题

PR 模板必须要求：范围、动机、影响 ID、验证命令、截图/输出、风险、迁移和回滚。

### P6-04 依赖与供应链

- 使用 Dependabot 检查 Python、npm 和 Actions。
- GitHub Actions 固定到审核后的版本；关键发布 action 可固定 commit SHA。
- 禁止未锁定的远程脚本。
- CI 增加 secrets 扫描和依赖审计。
- 依赖升级必须运行完整回归，不以“版本更新”豁免 review。

### P6-05 许可证、署名与内容来源审计

- 核对仓库 LICENSE 是否覆盖新增代码、课程文本、模板和站点资源。
- 保留 Datawhale 上游、原维护者和外部贡献者署名。
- 不复制超出合理引用范围的文章、课程或代码；引用外部内容时记录链接和许可证/访问说明。
- 对图片、字体、图标、测试页面和示例数据逐项确认再分发权利。
- 个人笔记转为公开示例前同时完成隐私和版权检查。
- 验收结果记录在资源目录和发布清单中。

### P6-06 版本、弃用和兼容策略

- 当前仓库无既有正式版本基线，不预设 `v1.1.0` 等历史语义版本。
- 首次版本化前在 ADR 中确认：课程版本、站点版本和代码包版本是统一还是分别管理。
- V2 路线使用 `roadmap_version`；仓库发布使用 Git tag；二者在 CHANGELOG 中建立映射。
- `deprecated` 内容必须给出替代项和最早删除版本。
- 破坏性 schema 变更必须提供迁移器、dry-run、回滚和兼容窗口。
- 未获得显式确认时，只生成发布候选说明，不创建 tag 或 release。

### Phase 6 退出条件

- 外链、上游和依赖均有周期性审计。
- 贡献者能根据变更类型找到明确流程。
- 自动化不会未经确认合并上游或创建外部副作用。
- 新增内容和资产的许可证、署名与来源可追溯。

## 6.7 Phase 7：发布与稳定化

### P7-01 Pages 构建和预览

- PR 只构建并上传预览 artifact，不部署正式站点。
- `main` 通过全部门禁后才部署 GitHub Pages。
- Pages workflow 使用最小权限和 `github-pages` environment。
- 构建产物不手工提交到主分支，除非 ADR 明确改变决策。
- 每次正式部署记录源 commit、workflow run 和 artifact 标识。
- 回滚通过从最后一个已验证的源 commit 重新构建并部署新 artifact 完成，不强推、不直接修改 Pages 产物。
- 回滚演练必须在 RC 阶段完成一次，并验证站点版本和源 commit 对应。

### P7-02 发布候选

- 创建 `v2.0.0-rc.1` 前必须获得显式发布确认。
- 执行全新 Windows/Ubuntu checkout 验证。
- 验证旧进度迁移、回滚、链接、移动端和安全场景。
- 收集 RC 问题并回到对应 Phase 修复，不能在发布阶段打临时补丁绕过门禁。

### P7-03 正式发布

- 发布 `v2.0.0` 前再次确认变更范围和提交历史。
- CHANGELOG 说明破坏性变化、迁移、已知限制和回滚方法。
- 旧入口至少保留到 `v2.1.0` 发布或 V2 正式发布满 30 天，以较晚者为准。
- 发布后不自动删除 legacy 资产。

### P7-04 稳定观察

- 发布后检查 Pages 构建、浏览器错误、链接和迁移反馈。
- 只记录匿名构建/错误信息；不引入用户追踪分析。
- P0/P1 问题立即进入修复循环；P2 进入后续版本。

### Phase 7 退出条件

- 正式站点可用且可回滚。
- 安装、学习、迁移、贡献和发布文档完整。
- 连续一轮全量 re-review 无新增 P0/P1 问题。

## 7. 依赖关系与关键路径

```text
Phase 0 基线与保护
  -> Phase 1 安全与真实性
  -> Phase 2 工程基础
  -> Phase 3 唯一事实源与迁移
      -> Phase 4 Labs
      -> Phase 5 Site
  -> Phase 6 治理
  -> Phase 7 发布
```

约束：

- Phase 4 与 Phase 5 可在 Phase 3 schema 稳定后并行，但合并前必须共同验证 task ID 和进度契约。
- Phase 6 的链接、依赖检查可提前建设，但正式门禁要等 Phase 2 CI 稳定。
- Phase 7 不得绕过任一上游退出条件。
- 任何 P0 发现都中断当前阶段并回到 Phase 1。

### 7.1 执行角色

| 角色 | 责任 | 不可替代的确认 |
| --- | --- | --- |
| Maintainer/用户 | 产品边界、个人数据、上游关系、发布和 Git 外部动作 | 隐私处理、commit/push/tag、Pages 正式发布 |
| Implementer | 按当前 Phase 实现、测试、记录证据和修复问题 | 不得自行扩大范围或降低门禁 |
| Reviewer | 从新状态检查安全、语义、迁移、UX 和治理 | 不以实现者自证代替独立 review 视角 |
| Learner acceptance | 验证任务说明、运行路径和完成规则是否可理解 | 课程“可学会”不能只靠代码测试证明 |

同一人可以承担多个角色，但 review 必须使用独立检查清单和新鲜验证结果，不能把实现过程中的判断直接当作 re-review。

### 7.2 相对工作量和发布切片

| Phase | 相对规模 | 主要产物 | 发布切片 |
| --- | --- | --- | --- |
| 0 | S | 快照、隐私/状态保护、ADR 输入 | 不发布 |
| 1 | M | P0 安全修复和真实性校正 | 安全修复里程碑；版本策略确认前不创建版本号 |
| 2 | M | 工程配置、核心包、测试、CI | 内部里程碑 |
| 3 | L | schema、课程、资源、进度迁移 | `v2.0.0-alpha` |
| 4 | XL | Stage 1-9 核心 Lab/模板 | `v2.0.0-beta` |
| 5 | L | 新站点、迁移、无障碍、兼容 | `v2.0.0-rc.1` |
| 6 | M | 上游、资源、贡献、供应链治理 | 合入 RC |
| 7 | M | 发布、迁移观察、稳定化 | `v2.0.0` |

规模只用于排序和拆分，不是承诺工期。每个 L/XL 阶段必须继续拆成可单独验证的 PR，禁止一次性交付。

V2.0 要求 Stage 1-9 都有核心 Lab 或可执行模板，但不要求完成每阶段所有扩展项目；扩展项目进入 V2.x backlog。

### 7.3 变更控制与状态报告

每次执行更新至少报告：

- 当前 Phase、任务 ID 和允许修改路径
- 本轮实际变更
- 新发现问题及优先级
- 已执行验证及结果时间
- 未解决风险、阻塞和需要用户确认的动作
- 下一步和退出条件完成度

范围变化分三类：

1. **范围内修正**：为满足当前任务验收所必需，可直接纳入并记录。
2. **相邻优化**：不阻断当前验收，进入 backlog，不顺手实现。
3. **范围扩张**：改变产品边界、技术栈、个人数据处理或外部动作，必须暂停并请求确认。

## 8. 计划变更清单

### 8.1 计划新增

- Python 工程配置与锁文件
- 课程、资源、进度 schema 和数据文件
- Stage 0-9 课程正文
- `src/` 参考实现和 `labs/` 渐进实验
- 单元、集成、安全、内容和前端测试
- 静态站点源文件
- 构建、迁移、校验、上游审计工具
- ADR、CHANGELOG、PR/Issue 模板和 CI workflows

### 8.2 计划迁移

- `learning-notes/` -> 经隐私审计后的 `workbook/archive/legacy-v1/`
- `stage-1/`、`stage-2/` -> 对应 `labs/`，保留旧文件到迁移验收完成
- README 课程正文 -> `curriculum/`
- HTML 内嵌课程和资源数据 -> 构建期数据
- localStorage 数组下标 key -> 稳定 task ID

### 8.3 计划删除或停用

只有在迁移验收、回滚验证，并达到 `v2.1.0` 发布或 V2 正式发布满 30 天（以较晚者为准）后，才允许删除：

- 手工维护的旧课程数据副本
- 旧 localStorage key 的写入逻辑
- 无测试、含危险 `eval()` 的旧运行入口
- 未固定版本的 CDN 依赖
- 重复或失效且已有归档记录的资源入口

删除必须独立提交，便于审查和回退。

## 9. 验证命令矩阵（未来执行）

以下命令仅作为未来门禁定义，当前计划编制任务不得执行：

```powershell
uv sync --all-extras --dev
uv run ruff format --check .
uv run ruff check .
uv run mypy src tools
uv run pytest --cov=agent_learning_hub --cov-report=term-missing
uv run python tools/validate_content.py
uv run python tools/build_readme.py --check
uv run python tools/check_resource_catalog.py --internal
npm ci
npm test
npm run build
uv run mkdocs build --strict
npx playwright test
```

补充检查：

- `git diff --check`
- 生成后 `git diff --exit-code`
- 危险模式残余搜索
- 内部链接和 ID 完整性检查
- 每周/手动执行资源外链检查；PR 默认只检查内部引用和本次变更链接
- Windows/Ubuntu 双平台矩阵
- 全新 checkout smoke test
- 旧进度 dry-run 与回滚测试

Playwright 配置必须通过受控的 localhost web server 打开构建产物；不能直接使用 `file://` 作为正式浏览器测试基线。

## 10. Review-Fix-Re-review 执行协议

每个 Phase 必须执行以下循环：

1. **Scope review**：确认只修改当前阶段授权的路径和能力。
2. **Evidence review**：对照基线、需求、代码、测试和生成物核实声明。
3. **Safety review**：检查权限、注入、数据损失、隐私、外部副作用和回滚。
4. **Semantic review**：检查课程概念、示例行为、rubric 与完成状态是否一致。
5. **UX review**：对网站或文档检查桌面、移动端、键盘和错误路径。
6. **Fresh validation**：修复后重新运行当前阶段全部门禁，不复用修复前结果。
7. **Fresh re-review**：从新状态重新审查，不只确认旧问题是否关闭。

循环退出条件：

- 当前轮没有发现新的 P0/P1 问题。
- 之前问题均有修复证据或明确接受记录。
- 自动化验证结果来自最后一次修复后的状态。
- 变更路径和计划一致。
- 仍存在的 P2/P3 项均进入 backlog，且不影响当前里程碑目标。

对本执行计划自身的 review 使用更严格标准：只有当前轮没有发现任何新的可操作缺陷、歧义、遗漏或矛盾时才可结束；不能把计划问题转入 backlog 后宣称“无新问题”。

若 re-review 发现新问题，必须回到修复步骤；不得以 review 次数、时间或“问题较小”为理由提前退出。

## 11. 风险、触发条件与应对

| 风险 | 触发条件 | 应对 |
| --- | --- | --- |
| 过度工程化 | 新增服务端、账号或复杂框架 | 回到非目标，优先静态方案 |
| 学习证据丢失 | 迁移后状态或笔记数量不一致 | 停止迁移，使用快照恢复，修复映射器 |
| 完成状态虚高 | mock 被当作真实服务证据 | 降级为离线验证状态，补真实证据或改任务定义 |
| 上游同步冲突 | README-first 上游与结构化本地冲突 | 生成差异报告，人工映射，不自动合并 |
| Windows 不兼容 | Unix-only 模块、路径或编码 | CI 矩阵阻断，提供条件实现或明确跳过 |
| 安全示例误导 | 子进程被称为沙箱、错误直接泄露 | 修正文案和 API，增加安全回归 |
| 外链波动 | 429、5xx、站点迁移 | 重试、suspect 状态、人工归档与替代链接 |
| 供应链风险 | latest CDN、未锁定依赖 | 固定版本、锁文件、CSP、依赖审计 |
| 发布破坏旧用户状态 | schema/key 改变 | 版本化迁移、旧键保留、导入导出和回滚 |
| 私人信息公开 | 工作簿进入 Git | 默认 ignore、提交前扫描、显式公开决策 |

## 12. 发布级验收标准

V2 只有同时满足以下条件才可宣告完成：

### 架构与内容

- README、站点、课程元数据不存在手工维护的重复课程列表。
- 100% stage/task/project/resource ID 唯一且通过 schema。
- 旧 50 个任务均有迁移映射或弃用理由。
- 每个 V2 任务具有产出、rubric、验证命令和安全说明。

### 代码与安全

- 模型控制的输入路径不存在危险 `eval/exec`。
- 普通子进程不再被称为安全沙箱。
- Windows/Ubuntu 核心实验全部通过。
- 用户输入无法通过搜索或笔记执行脚本。
- Provider、工具和文件错误经过结构化与脱敏。

### 学习完整性

- 完成状态都有证据路径和 review 记录。
- 离线验证与真实服务验证明确区分。
- 长期记忆通过跨进程持久化测试。
- RAG 通过固定中文检索集与引用完整性测试。

### 网站与数据

- 360px、768px、桌面端核心流程通过。
- 键盘可完成导航、清单、搜索、进度和笔记操作。
- axe 无 critical/serious 问题。
- 旧 localStorage 状态可 dry-run、迁移、回滚。
- 课程进度与可选项目进度分离。

### 工程与发布

- CI 在 Windows/Ubuntu 全绿。
- 全新 checkout 能按 README 在 10 分钟内运行第一个离线 Lab。
- Pages 构建可复现、可预览、可回滚。
- 链接、依赖和上游有定期审计。
- 发布前最后一轮全量 re-review 无新增 P0/P1 问题。

## 13. 提交与回滚策略

未来执行时建议按里程碑拆分提交：

1. `chore: capture v1 baseline and decisions`
2. `fix: remove unsafe teaching patterns and correct status`
3. `build: add project metadata tests and ci`
4. `feat: add curriculum schemas and migration tooling`
5. `feat: rebuild stage 1-4 labs`
6. `feat: build generated learning site`
7. `docs: add governance upstream and release guides`
8. `release: prepare agent learning hub v2`

规则：

- 不把全部整改压成一个提交。
- 不修改或压缩已有历史。
- 不使用 `reset --hard` 或强推作为常规回滚。
- 迁移和删除分开提交。
- 每个提交都必须在自身范围内可验证。
- commit、push、tag、Pages 发布均需遵守未来任务的明确授权。

## 14. 执行前最终检查表

- [ ] 用户已确认开始执行，而不只是继续修订计划。
- [ ] 工作区干净，基线提交仍可定位。
- [ ] 执行分支、范围和允许修改路径已确认。
- [ ] 个人笔记公开策略已确认。
- [ ] localStorage 已具备导出和恢复方案。
- [ ] P0 问题的回归测试设计已先于实现确认。
- [ ] Python、站点、进度和上游 ADR 已批准。
- [ ] CI 和依赖下载权限已确认。
- [ ] commit、push、tag、Pages 发布权限分别确认。
- [ ] 退出、回滚和停止条件清晰。

任一检查项未满足时，只能继续准备或请求确认，不得进入对应执行动作。

## 15. 本计划自身 Review 记录

本节只记录对 `EXECUTION_PLAN.md` 的 review-fix-re-review，不记录未来实现状态。

### Review 轮次

- R1：发现并修复以下计划问题：技术栈选择含糊；Stage 5-9 缺少核心 Lab；localStorage 未区分 origin；缺少威胁模型、安全响应、许可证审计；legacy 保留周期不精确；缺少角色、相对工作量和变更控制；缺少 URL 兼容与性能门禁；纯概念任务的 `lab_path` 约束过严。
- R2：发现并修复以下计划问题：Phase 标题层级错误；CI 未纳入前端/Markdown/浏览器门禁；记忆实验缺少持久化同意、数据最小化和删除验证；引用支持性验收不可操作；缺少课程与资源语义时效审计；课程/资源状态枚举未定义；`.gitignore` 和 `.env.example` 未落到任务；仓库无版本基线却预设 `v1.1.0`。
- R3：发现并修复以下计划问题：未固定 Node 运行时且 Python 矩阵未覆盖最新稳定版本；进度导入缺少原子备份与数量对账；SQLite 记忆缺少 schema 迁移策略；Pages 回滚没有可执行动作；`.gitignore` 的工作簿范围可能误伤公开模板和 legacy 档案。
- R4：发现并修复以下计划问题：现有 11 项 Project Ladder 缺少独立事实源、稳定 ID、rubric、进度和迁移模型；中英文混排策略未定义；站点基础元数据未纳入建设范围。
- R5：发现并修复以下计划问题：部分 ID 唯一性验收漏写 project；schema 未明确验证前置关系和 replacement 链的引用完整性与无环性；验证命令顺序与“先构建前端资产、再构建 MkDocs”矛盾，且缺少资源目录检查和受控 localhost 浏览器基线。
- R6：完成语义层 final fresh re-review；覆盖范围边界、49 个任务 ID、8 个 Phase 及退出条件、依赖闭环、迁移可逆性、安全与隐私、课程/项目/资源模型、跨平台 CI、站点兼容、发布和回滚，未发现新的语义缺陷。随后格式门禁发现元数据区 6 行 Markdown 硬换行属于 Git 尾随空白，因此进入 R7 修复。
- R7：将元数据改为无尾随空白的引用列表，并重新执行结构、重复 ID、Phase/退出条件、占位词、尾随空白、差异范围和 Git 状态检查；本轮未发现新问题。

### 当前结论

- R1-R6 发现的问题均已修复；R7 未发现新问题，满足本计划 review-fix-re-review 循环退出条件。计划已达到“可在获得用户明确执行授权后使用”的状态，但当前任务没有执行任何计划项。
