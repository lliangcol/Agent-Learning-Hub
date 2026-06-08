# Stage 0: Agent 基础概念

来源：`README.md` 的 `Learning Todo List -> Stage 0: Understand What An Agent Is`

## 当前进度

- [x] 区分 chatbot、workflow、agent、multi-agent。
- [x] 理解 agent 的基本循环：observe -> think -> act -> observe。
- [x] 明白什么时候不该用 agent：任务可预测、流程稳定、普通脚本能解决时，agent 反而增加不确定性。
- [x] 读完 Anthropic: Building effective agents。
- [ ] 读完 OpenAI: A practical guide to building agents。

## 核心概念

### Chatbot

Chatbot 主要负责对话。典型模式是用户输入问题，模型直接生成回答。它可以很有帮助，但通常不会主动规划多步行动，也不会在外部环境里执行操作。

### Workflow

Workflow 是预先定义好的固定流程。每一步通常由开发者提前写清楚，例如：

1. 读取文件。
2. 调用模型生成摘要。
3. 写入目标文档。

当任务流程稳定、规则明确、异常可预测时，workflow 通常比 agent 更合适。

### Agent

Agent 会在受约束的环境里循环执行：

```text
observe -> think -> act -> observe
```

也就是：

1. 观察当前状态和已有信息。
2. 判断下一步需要做什么。
3. 必要时调用工具或执行操作。
4. 读取反馈结果，再决定是否继续。

工程里的 agent 不是“无限自主”。它应该被工具、权限、停止条件、上下文、成本和超时约束住。

### Multi-Agent

Multi-agent 是多个 agent 分工协作。重点不是让多个模型随便聊天，而是明确每个 agent 的职责、输入输出、停止条件和协调机制。

## 本次回答与修正

### 1. Agent 和普通 chatbot 的最大区别

自己的回答：

> agent 可以自主观察、判断、思考，必要时调用集成的外部工具，执行操作获取反馈，获取缺失信息，帮助自己进行下一步的决策。

修正后理解：

Agent 的关键不只是回答问题，而是能在任务执行过程中根据观察结果决定下一步动作。它可以调用工具、读取反馈、补齐缺失信息，并继续迭代。但这种自主性必须受到工具权限、预算、最大步数、超时和停止条件约束。

### 2. 什么时候应该用 workflow，而不是 agent

自己的回答：

> 当流程固定，中间不会产生不可预测的变量，不需要实时判断时使用 workflow。

修正后理解：

如果任务可以用确定规则、脚本、状态机、SQL 或固定 API 编排稳定完成，就优先使用 workflow。agent 会引入不确定性、成本和调试难度，不应该为了“智能”而替代简单可靠的流程。

### 3. 资料整理助手为什么可能需要 agent

自己的回答：

> 资料整理助手需要分析每一份资料，判断归档类别，生成各种关联关系，方便后续查找，可能会涉及内容处理等工作，而要完成以上列举的任务，就需要使用 agent，由它进行分析判断、调用工具整理、生成复杂的关联关系，处理各种不同的内容。

修正后理解：

资料整理助手在以下情况下更适合用 agent：

- 资料来源不固定，需要动态判断下一步去哪里找。
- 内容类型不同，需要选择不同处理方式。
- 需要识别缺失信息并继续查找。
- 需要根据资料内容决定分类、关联和后续动作。
- 需要保留引用、证据和处理过程，方便复查。

如果只是对固定文件夹里的文档做批量摘要或固定分类，workflow + LLM 调用可能已经足够。

## 判断是否该使用 Agent 的简单标准

优先使用 agent：

- 任务目标明确，但路径不固定。
- 中间结果会影响下一步动作。
- 需要调用工具获取外部信息。
- 需要处理失败、空结果、歧义或缺失信息。
- 需要多轮观察和调整。

优先使用 workflow：

- 步骤固定。
- 输入输出结构稳定。
- 错误情况可预测。
- 普通脚本、规则或 API 编排能可靠完成。
- 成本、稳定性和可测试性比灵活性更重要。

## 阅读笔记：Anthropic - Building effective agents

阅读时间：2026-06-05

原文链接：https://www.anthropic.com/engineering/building-effective-agents

### 文章主线

这篇文章把 agentic systems 分成两类：

- Workflows：LLM 和工具沿着开发者预定义的代码路径执行。
- Agents：LLM 动态决定流程和工具使用方式，并控制如何完成任务。

这个区分很重要：workflow 里，LLM 更像流程中的处理节点；agent 里，LLM 更像受约束的决策中枢。

### 常见模式

文章总结的常见 agentic system 模式：

- Prompt chaining：把任务拆成串行步骤，逐步精化。
- Routing：先分类，再派发到不同处理路径。
- Parallelization：并行处理后聚合结果，包括 sectioning 和 voting。
- Orchestrator-workers：由编排者动态拆分任务，再交给 worker 处理。
- Evaluator-optimizer：生成者和评估者循环迭代改进结果。
- Agents：在开放路径中根据环境反馈持续决定下一步行动。

### 本次理解

1. Workflow 的流程是固定的，代码决定下一步做什么。LLM 通常只是某个处理节点。
2. Agent 的流程是动态的，LLM 会根据观察和反馈决定下一步调用什么工具、是否继续循环、什么时候停止。
3. 不应该一开始就追求复杂 agent。复杂性会带来延迟、成本、调试难度和错误累积，只有当收益能被验证时才值得引入。
4. 工具接口设计非常重要。工具是 agent 与外部世界交互的接口，接口是否清楚会直接影响 agent 的行动质量。
5. 生产环境中的 agent 需要透明、可测试、可观察、有人机协作检查点，并且必须有停止条件。

### 修正与补充

你的笔记里 “从 HCI 到 ACI 的设计思维迁移” 抓得很好。需要继续强化的一点是：ACI 不是抽象口号，它落到工程里就是工具名称、参数、描述、示例、边界、错误信息和测试样例。

“信任是隐含约束” 也判断准确。工程上对应的是：

- 沙盒测试。
- 明确展示规划步骤。
- 保留 trace 和工具调用记录。
- 危险动作前设置人工确认。
- 设置最大步数、超时和成本上限。

### 可以打勾的内容

- [x] 读完 Anthropic: Building effective agents。
- [x] 能解释 workflow 和 agent 的区别。
- [x] 能说出常见 workflow / agentic patterns。
- [x] 理解为什么先从简单方案开始。

## 学习卡片：OpenAI - A practical guide to building agents

开始时间：2026-06-08

原文链接：https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/

状态：阅读中，等待完成检查题后整理为正式笔记。

### 先抓主线

OpenAI 这篇 guide 更偏产品和工程落地。它的重点不是“agent 很智能”，而是：

1. 什么任务值得做成 agent。
2. agent 最小组成是什么。
3. 单 agent 和多 agent 该如何取舍。
4. 如何用 guardrails、人工介入和 evals 让 agent 可控。

### OpenAI 对 Agent 的定义

OpenAI 把 agent 描述为能代表用户独立完成任务的系统。和普通 LLM 应用相比，关键差异是：LLM 不只是生成一句回答，而是参与控制 workflow 的执行过程，能判断任务是否完成、选择工具、处理失败，并在必要时把控制权交还给用户。

这和 Anthropic 的文章可以对上：

- Anthropic 强调 workflow 和 agent 的边界。
- OpenAI 进一步把 agent 拆成可落地的工程组件。

### Agent 的三个基础组件

OpenAI guide 里的最小 agent 可以先记成：

1. Model：负责推理和决策。
2. Tools：连接外部系统，读取信息或执行动作。
3. Instructions：约束行为、说明流程、定义边界和 guardrails。

初学时不要先纠结框架名字，先确认这三个部分是否清楚：模型为什么能判断下一步、工具具体能做什么、指令如何限制它不能乱做。

### 什么时候值得构建 Agent

更适合 agent 的任务通常有这些特征：

- 需要复杂判断，而不是简单 if/else。
- 规则很多、维护困难，传统规则系统容易变脆。
- 大量依赖非结构化数据，例如自然语言、文档、用户对话。

反过来，如果规则稳定、输入输出固定、普通脚本或 workflow 能可靠完成，就不应该为了使用 agent 而使用 agent。

### Orchestration 的取舍

OpenAI 的建议和 Stage 0 的主线一致：先最大化单 agent 的能力，再考虑多 agent。

单 agent 更容易评估、调试和维护。只有当提示词条件分支过多、工具相似度太高、模型经常选错工具或职责需要明确拆分时，才考虑多 agent。

多 agent 也不是“多个角色聊天”，常见模式是：

- Manager pattern：中心 manager 把任务委派给专门 agent，最终仍由 manager 控制和汇总。
- Decentralized handoff：一个 agent 根据任务类型把控制权移交给另一个 agent。

### Guardrails / Human Oversight / Evals

Guardrails 解决的是安全和边界问题，例如防止越权、跑题、泄露隐私、执行高风险工具或输出不合规内容。它应该是多层防线，而不是单个提示词。

Human oversight 解决的是“系统信心不够或风险过高时怎么办”。常见触发条件包括失败次数过多、高风险动作、不可逆操作、付款、退款、删除或发布等。

Evals 解决的是“它到底有没有稳定做好”。先用强模型做基线，再用测试集观察准确率、失败类型、成本和延迟，之后才考虑换小模型或加复杂架构。

### 等待你回答的检查题

1. 用你自己的话说，OpenAI 为什么认为 agent 不等于普通 chatbot 或单次 LLM 调用？
2. 如果要做一个“资料整理助手”，它的 model、tools、instructions 分别应该包含什么？
3. 对这个资料整理助手，你会设计哪 3 条 guardrails？哪些动作必须 human oversight？
4. 你会怎么设计一个最小 eval，证明这个 agent 比普通 workflow 更值得做？

## 下一步

完成上一节 `等待你回答的检查题`。回答不用长，先用自己的话写 5-10 句话。回答后需要先 review 和修正，再把 OpenAI 阅读项标记为完成。
