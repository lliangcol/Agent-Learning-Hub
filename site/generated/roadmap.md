---
title: 课程路线
description: Stage 0-9 课程任务、前置条件与验收入口
---

# 课程路线

<p data-progress-summary role="status" aria-live="polite">课程进度正在加载…</p>

课程任务与可选项目分别统计。复选框只记录本地学习状态；勾选只表示 `concept_verified`，`complete` 仍需工作簿证据和 review。

## S00 Agent 适用性与边界 { #s00 }

通过可复查证据学习 Agent 适用性与边界。

<ul class="task-list">
<li class="progress-item" id="s00-t01">
<input type="checkbox" id="check-S00-T01" data-task-id="S00-T01" disabled>
<label for="check-S00-T01"><code>S00-T01</code> 区分 chatbot、workflow、agent、multi-agent</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：区分 chatbot、workflow、agent、multi-agent。</li></ul></dd>
<dt>Lab</dt><dd>无</dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S00-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run python tools/validate_content.py</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r001"><code>R001</code></a>, <a href="../resources/#r002"><code>R002</code></a>, <a href="../resources/#r004"><code>R004</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s00-t02">
<input type="checkbox" id="check-S00-T02" data-task-id="S00-T02" disabled>
<label for="check-S00-T02"><code>S00-T02</code> 理解 agent 的基本循环：observe -&gt; think -&gt; act -&gt; observe</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S00-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：理解 agent 的基本循环：observe -&gt; think -&gt; act -&gt; observe。</li></ul></dd>
<dt>Lab</dt><dd>无</dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S00-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run python tools/validate_content.py</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r001"><code>R001</code></a>, <a href="../resources/#r002"><code>R002</code></a>, <a href="../resources/#r004"><code>R004</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s00-t03">
<input type="checkbox" id="check-S00-T03" data-task-id="S00-T03" disabled>
<label for="check-S00-T03"><code>S00-T03</code> 明白什么时候不该用 agent：任务可预测、流程稳定、普通脚本能解决时，agent 反而增加不确定性</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S00-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：明白什么时候不该用 agent：任务可预测、流程稳定、普通脚本能解决时，agent 反而增加不确定性。</li></ul></dd>
<dt>Lab</dt><dd>无</dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S00-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run python tools/validate_content.py</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r001"><code>R001</code></a>, <a href="../resources/#r002"><code>R002</code></a>, <a href="../resources/#r004"><code>R004</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s00-t04">
<input type="checkbox" id="check-S00-T04" data-task-id="S00-T04" disabled>
<label for="check-S00-T04"><code>S00-T04</code> 读完 <a href="https://www.anthropic.com/engineering/building-effective-agents">Anthropic: Building effective agents</a></label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S00-T03</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：读完 [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)。</li></ul></dd>
<dt>Lab</dt><dd>无</dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S00-T04.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run python tools/validate_content.py</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r001"><code>R001</code></a>, <a href="../resources/#r002"><code>R002</code></a>, <a href="../resources/#r004"><code>R004</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s00-t05">
<input type="checkbox" id="check-S00-T05" data-task-id="S00-T05" disabled>
<label for="check-S00-T05"><code>S00-T05</code> 读完 <a href="https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/">OpenAI: A practical guide to building agents</a></label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S00-T04</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：读完 [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)。</li></ul></dd>
<dt>Lab</dt><dd>无</dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S00-T05.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run python tools/validate_content.py</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r001"><code>R001</code></a>, <a href="../resources/#r002"><code>R002</code></a>, <a href="../resources/#r004"><code>R004</code></a></dd>
</dl>
</details>
</li>
</ul>

## S01 LLM API 与结构化契约 { #s01 }

通过可复查证据学习 LLM API 与结构化契约。

<ul class="task-list">
<li class="progress-item" id="s01-t01">
<input type="checkbox" id="check-S01-T01" data-task-id="S01-T01" disabled>
<label for="check-S01-T01"><code>S01-T01</code> 会用一个 LLM API 完成普通对话</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会用一个 LLM API 完成普通对话。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-01-llm-contracts</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S01-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-01-llm-contracts/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s01-t02">
<input type="checkbox" id="check-S01-T02" data-task-id="S01-T02" disabled>
<label for="check-S01-T02"><code>S01-T02</code> 会让模型输出结构化 JSON</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S01-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会让模型输出结构化 JSON。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-01-llm-contracts</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S01-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-01-llm-contracts/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s01-t03">
<input type="checkbox" id="check-S01-T03" data-task-id="S01-T03" disabled>
<label for="check-S01-T03"><code>S01-T03</code> 会定义一个工具函数，例如 search、calculator、read_file</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S01-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会定义一个工具函数，例如 search、calculator、read_file。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-01-llm-contracts</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S01-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-01-llm-contracts/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
</ul>

## S02 Agent Loop 与工具调用 { #s02 }

通过可复查证据学习 Agent Loop 与工具调用。

<ul class="task-list">
<li class="progress-item" id="s02-t01">
<input type="checkbox" id="check-S02-T01" data-task-id="S02-T01" disabled>
<label for="check-S02-T01"><code>S02-T01</code> 会解析模型的 tool call / function call</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会解析模型的 tool call / function call。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-02-agent-loop</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S02-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-02-agent-loop/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s02-t02">
<input type="checkbox" id="check-S02-T02" data-task-id="S02-T02" disabled>
<label for="check-S02-T02"><code>S02-T02</code> 会执行工具，并把工具结果喂回模型</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S02-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会执行工具，并把工具结果喂回模型。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-02-agent-loop</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S02-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-02-agent-loop/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s02-t03">
<input type="checkbox" id="check-S02-T03" data-task-id="S02-T03" disabled>
<label for="check-S02-T03"><code>S02-T03</code> 会给 agent loop 加最大步数、超时和错误处理</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S02-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会给 agent loop 加最大步数、超时和错误处理。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-02-agent-loop</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S02-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-02-agent-loop/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
</ul>

## S03 RAG、上下文与记忆 { #s03 }

通过可复查证据学习 RAG、上下文与记忆。

<ul class="task-list">
<li class="progress-item" id="s03-t01">
<input type="checkbox" id="check-S03-T01" data-task-id="S03-T01" disabled>
<label for="check-S03-T01"><code>S03-T01</code> 会做检索增强生成：chunk、embed、retrieve、answer with citations</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会做检索增强生成：chunk、embed、retrieve、answer with citations。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-03-rag-and-memory</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S03-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-03-rag-and-memory/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r019"><code>R019</code></a>, <a href="../resources/#r020"><code>R020</code></a>, <a href="../resources/#r021"><code>R021</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s03-t02">
<input type="checkbox" id="check-S03-T02" data-task-id="S03-T02" disabled>
<label for="check-S03-T02"><code>S03-T02</code> 会区分短期上下文、会话记忆、长期记忆</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S03-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会区分短期上下文、会话记忆、长期记忆。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-03-rag-and-memory</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S03-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-03-rag-and-memory/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r019"><code>R019</code></a>, <a href="../resources/#r020"><code>R020</code></a>, <a href="../resources/#r021"><code>R021</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s03-t03">
<input type="checkbox" id="check-S03-T03" data-task-id="S03-T03" disabled>
<label for="check-S03-T03"><code>S03-T03</code> 会让 agent 在回答里给出来源或证据</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S03-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会让 agent 在回答里给出来源或证据。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-03-rag-and-memory</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S03-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-03-rag-and-memory/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r019"><code>R019</code></a>, <a href="../resources/#r020"><code>R020</code></a>, <a href="../resources/#r021"><code>R021</code></a></dd>
</dl>
</details>
</li>
</ul>

## S04 可靠性、权限与安全 { #s04 }

通过可复查证据学习 可靠性、权限与安全。

<ul class="task-list">
<li class="progress-item" id="s04-t01">
<input type="checkbox" id="check-S04-T01" data-task-id="S04-T01" disabled>
<label for="check-S04-T01"><code>S04-T01</code> 会把搜索、数据库、文件、浏览器、代码执行接成工具</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会把搜索、数据库、文件、浏览器、代码执行接成工具。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s04-t02">
<input type="checkbox" id="check-S04-T02" data-task-id="S04-T02" disabled>
<label for="check-S04-T02"><code>S04-T02</code> 会处理工具失败、空结果、重复调用、幻觉引用</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S04-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会处理工具失败、空结果、重复调用、幻觉引用。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s04-t03">
<input type="checkbox" id="check-S04-T03" data-task-id="S04-T03" disabled>
<label for="check-S04-T03"><code>S04-T03</code> 为 agent 准备固定测试集，而不是只看 demo</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S04-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：为 agent 准备固定测试集，而不是只看 demo。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s04-t04">
<input type="checkbox" id="check-S04-T04" data-task-id="S04-T04" disabled>
<label for="check-S04-T04"><code>S04-T04</code> 记录成功率、失败原因、工具调用次数、成本、延迟</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S04-T03</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：记录成功率、失败原因、工具调用次数、成本、延迟。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T04.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s04-t05">
<input type="checkbox" id="check-S04-T05" data-task-id="S04-T05" disabled>
<label for="check-S04-T05"><code>S04-T05</code> 会看 trace，知道失败发生在 prompt、工具、检索、模型还是状态管理</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S04-T04</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会看 trace，知道失败发生在 prompt、工具、检索、模型还是状态管理。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T05.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s04-t06">
<input type="checkbox" id="check-S04-T06" data-task-id="S04-T06" disabled>
<label for="check-S04-T06"><code>S04-T06</code> 给危险工具加人工确认，例如发邮件、删文件、付款、发布内容</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S04-T05</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：给危险工具加人工确认，例如发邮件、删文件、付款、发布内容。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T06.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s04-t07">
<input type="checkbox" id="check-S04-T07" data-task-id="S04-T07" disabled>
<label for="check-S04-T07"><code>S04-T07</code> 了解 prompt injection、data exfiltration、tool abuse 等风险</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S04-T06</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：了解 prompt injection、data exfiltration、tool abuse 等风险。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T07.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s04-t08">
<input type="checkbox" id="check-S04-T08" data-task-id="S04-T08" disabled>
<label for="check-S04-T08"><code>S04-T08</code> 会用回归测试防止 prompt 或工具改动后能力退化</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S04-T07</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会用回归测试防止 prompt 或工具改动后能力退化。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-04-reliability-and-safety</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S04-T08.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-04-reliability-and-safety/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r010"><code>R010</code></a>, <a href="../resources/#r012"><code>R012</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
</ul>

## S05 Harness、Trace 与 Evals { #s05 }

通过可复查证据学习 Harness、Trace 与 Evals。

<ul class="task-list">
<li class="progress-item" id="s05-t01">
<input type="checkbox" id="check-S05-T01" data-task-id="S05-T01" disabled>
<label for="check-S05-T01"><code>S05-T01</code> 读懂一个 agent harness 的目录结构</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：读懂一个 agent harness 的目录结构。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-05-harness-and-evals</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S05-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-05-harness-and-evals/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r016"><code>R016</code></a>, <a href="../resources/#r017"><code>R017</code></a>, <a href="../resources/#r018"><code>R018</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s05-t02">
<input type="checkbox" id="check-S05-T02" data-task-id="S05-T02" disabled>
<label for="check-S05-T02"><code>S05-T02</code> 找出它的 agent loop、tool registry、permission gate、session store、context compaction</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S05-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：找出它的 agent loop、tool registry、permission gate、session store、context compaction。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-05-harness-and-evals</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S05-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-05-harness-and-evals/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r016"><code>R016</code></a>, <a href="../resources/#r017"><code>R017</code></a>, <a href="../resources/#r018"><code>R018</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s05-t03">
<input type="checkbox" id="check-S05-T03" data-task-id="S05-T03" disabled>
<label for="check-S05-T03"><code>S05-T03</code> 跑通它的最小示例，并加一个你自己的工具</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S05-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：跑通它的最小示例，并加一个你自己的工具。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-05-harness-and-evals</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S05-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-05-harness-and-evals/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r016"><code>R016</code></a>, <a href="../resources/#r017"><code>R017</code></a>, <a href="../resources/#r018"><code>R018</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s05-t04">
<input type="checkbox" id="check-S05-T04" data-task-id="S05-T04" disabled>
<label for="check-S05-T04"><code>S05-T04</code> 观察一次完整 trace，解释每一步为什么发生</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S05-T03</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：观察一次完整 trace，解释每一步为什么发生。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-05-harness-and-evals</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S05-T04.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-05-harness-and-evals/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r016"><code>R016</code></a>, <a href="../resources/#r017"><code>R017</code></a>, <a href="../resources/#r018"><code>R018</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s05-t05">
<input type="checkbox" id="check-S05-T05" data-task-id="S05-T05" disabled>
<label for="check-S05-T05"><code>S05-T05</code> 把同一个任务分别用「裸 agent loop」和「harness」实现，对比差异</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S05-T04</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：把同一个任务分别用「裸 agent loop」和「harness」实现，对比差异。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-05-harness-and-evals</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S05-T05.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-05-harness-and-evals/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r016"><code>R016</code></a>, <a href="../resources/#r017"><code>R017</code></a>, <a href="../resources/#r018"><code>R018</code></a></dd>
</dl>
</details>
</li>
</ul>

## S06 Skills 与协议 { #s06 }

通过可复查证据学习 Skills 与协议。

<ul class="task-list">
<li class="progress-item" id="s06-t01">
<input type="checkbox" id="check-S06-T01" data-task-id="S06-T01" disabled>
<label for="check-S06-T01"><code>S06-T01</code> 理解 Skill 和 Tool 的区别：tool 是可调用接口，skill 是可复用流程知识</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：理解 Skill 和 Tool 的区别：tool 是可调用接口，skill 是可复用流程知识。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s06-t02">
<input type="checkbox" id="check-S06-T02" data-task-id="S06-T02" disabled>
<label for="check-S06-T02"><code>S06-T02</code> 理解 Skill 和 Prompt 的区别：prompt 通常是一次性指令，skill 是可发现、可版本化、可分发的能力包</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S06-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：理解 Skill 和 Prompt 的区别：prompt 通常是一次性指令，skill 是可发现、可版本化、可分发的能力包。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s06-t03">
<input type="checkbox" id="check-S06-T03" data-task-id="S06-T03" disabled>
<label for="check-S06-T03"><code>S06-T03</code> 理解 Skill 和 MCP 的区别：MCP 接入外部工具/数据源，skill 告诉 agent 如何完成一类任务</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S06-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：理解 Skill 和 MCP 的区别：MCP 接入外部工具/数据源，skill 告诉 agent 如何完成一类任务。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s06-t04">
<input type="checkbox" id="check-S06-T04" data-task-id="S06-T04" disabled>
<label for="check-S06-T04"><code>S06-T04</code> 阅读 Claude Code Skills 的文件结构和触发机制</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S06-T03</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：阅读 Claude Code Skills 的文件结构和触发机制。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T04.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s06-t05">
<input type="checkbox" id="check-S06-T05" data-task-id="S06-T05" disabled>
<label for="check-S06-T05"><code>S06-T05</code> 阅读 OpenClaw Skills 的加载、作用域和安全边界</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S06-T04</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：阅读 OpenClaw Skills 的加载、作用域和安全边界。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T05.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s06-t06">
<input type="checkbox" id="check-S06-T06" data-task-id="S06-T06" disabled>
<label for="check-S06-T06"><code>S06-T06</code> 写一个最小 `SKILL.md`，包含 name、description、何时使用、步骤、验收标准</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S06-T05</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：写一个最小 `SKILL.md`，包含 name、description、何时使用、步骤、验收标准。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T06.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s06-t07">
<input type="checkbox" id="check-S06-T07" data-task-id="S06-T07" disabled>
<label for="check-S06-T07"><code>S06-T07</code> 给 skill 加一个脚本或模板文件，并说明 agent 什么时候才需要加载它</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S06-T06</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：给 skill 加一个脚本或模板文件，并说明 agent 什么时候才需要加载它。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T07.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s06-t08">
<input type="checkbox" id="check-S06-T08" data-task-id="S06-T08" disabled>
<label for="check-S06-T08"><code>S06-T08</code> 给 skill 写一个 smoke test，验证它是否真的提升任务成功率</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S06-T07</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：给 skill 写一个 smoke test，验证它是否真的提升任务成功率。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-06-skills-and-protocols</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S06-T08.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-06-skills-and-protocols/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r015"><code>R015</code></a>, <a href="../resources/#r019"><code>R019</code></a></dd>
</dl>
</details>
</li>
</ul>

## S07 Browser 与 Computer Use { #s07 }

通过可复查证据学习 Browser 与 Computer Use。

<ul class="task-list">
<li class="progress-item" id="s07-t01">
<input type="checkbox" id="check-S07-T01" data-task-id="S07-T01" disabled>
<label for="check-S07-T01"><code>S07-T01</code> 理解 browser agent 和普通 API tool 的区别</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：理解 browser agent 和普通 API tool 的区别。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-07-browser-and-computer-use</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S07-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-07-browser-and-computer-use/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r011"><code>R011</code></a>, <a href="../resources/#r032"><code>R032</code></a>, <a href="../resources/#r033"><code>R033</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s07-t02">
<input type="checkbox" id="check-S07-T02" data-task-id="S07-T02" disabled>
<label for="check-S07-T02"><code>S07-T02</code> 会用 Playwright 或 browser-use 做网页观察和点击</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S07-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会用 Playwright 或 browser-use 做网页观察和点击。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-07-browser-and-computer-use</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S07-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-07-browser-and-computer-use/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r011"><code>R011</code></a>, <a href="../resources/#r032"><code>R032</code></a>, <a href="../resources/#r033"><code>R033</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s07-t03">
<input type="checkbox" id="check-S07-T03" data-task-id="S07-T03" disabled>
<label for="check-S07-T03"><code>S07-T03</code> 会给浏览器操作加安全限制：不登录敏感账号、不越权、不绕过平台规则</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S07-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会给浏览器操作加安全限制：不登录敏感账号、不越权、不绕过平台规则。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-07-browser-and-computer-use</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S07-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-07-browser-and-computer-use/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r011"><code>R011</code></a>, <a href="../resources/#r032"><code>R032</code></a>, <a href="../resources/#r033"><code>R033</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s07-t04">
<input type="checkbox" id="check-S07-T04" data-task-id="S07-T04" disabled>
<label for="check-S07-T04"><code>S07-T04</code> 会处理页面变化、弹窗、加载失败、元素定位失败</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S07-T03</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会处理页面变化、弹窗、加载失败、元素定位失败。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-07-browser-and-computer-use</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S07-T04.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-07-browser-and-computer-use/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r011"><code>R011</code></a>, <a href="../resources/#r032"><code>R032</code></a>, <a href="../resources/#r033"><code>R033</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s07-t05">
<input type="checkbox" id="check-S07-T05" data-task-id="S07-T05" disabled>
<label for="check-S07-T05"><code>S07-T05</code> 会记录截图、DOM、动作日志，方便复盘</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S07-T04</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会记录截图、DOM、动作日志，方便复盘。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-07-browser-and-computer-use</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S07-T05.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-07-browser-and-computer-use/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r011"><code>R011</code></a>, <a href="../resources/#r032"><code>R032</code></a>, <a href="../resources/#r033"><code>R033</code></a></dd>
</dl>
</details>
</li>
</ul>

## S08 Multi-Agent 协调 { #s08 }

通过可复查证据学习 Multi-Agent 协调。

<ul class="task-list">
<li class="progress-item" id="s08-t01">
<input type="checkbox" id="check-S08-T01" data-task-id="S08-T01" disabled>
<label for="check-S08-T01"><code>S08-T01</code> 理解 planner / executor / reviewer / critic / router 等常见角色</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：理解 planner / executor / reviewer / critic / router 等常见角色。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-08-multi-agent</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S08-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-08-multi-agent/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r003"><code>R003</code></a>, <a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r016"><code>R016</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s08-t02">
<input type="checkbox" id="check-S08-T02" data-task-id="S08-T02" disabled>
<label for="check-S08-T02"><code>S08-T02</code> 学会用 supervisor 或 graph 管理多 agent，而不是让 agent 随便聊天</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S08-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：学会用 supervisor 或 graph 管理多 agent，而不是让 agent 随便聊天。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-08-multi-agent</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S08-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-08-multi-agent/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r003"><code>R003</code></a>, <a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r016"><code>R016</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s08-t03">
<input type="checkbox" id="check-S08-T03" data-task-id="S08-T03" disabled>
<label for="check-S08-T03"><code>S08-T03</code> 会定义每个 agent 的职责边界、输入输出 schema、停止条件</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S08-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会定义每个 agent 的职责边界、输入输出 schema、停止条件。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-08-multi-agent</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S08-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-08-multi-agent/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r003"><code>R003</code></a>, <a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r016"><code>R016</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s08-t04">
<input type="checkbox" id="check-S08-T04" data-task-id="S08-T04" disabled>
<label for="check-S08-T04"><code>S08-T04</code> 会处理循环、争论、任务漂移、上下文膨胀</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S08-T03</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会处理循环、争论、任务漂移、上下文膨胀。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-08-multi-agent</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S08-T04.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-08-multi-agent/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r003"><code>R003</code></a>, <a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r016"><code>R016</code></a></dd>
</dl>
</details>
</li>
<li class="progress-item" id="s08-t05">
<input type="checkbox" id="check-S08-T05" data-task-id="S08-T05" disabled>
<label for="check-S08-T05"><code>S08-T05</code> 会判断什么时候单 agent 更好</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S08-T04</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：会判断什么时候单 agent 更好。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-08-multi-agent</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S08-T05.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-08-multi-agent/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd><a href="../resources/#r003"><code>R003</code></a>, <a href="../resources/#r006"><code>R006</code></a>, <a href="../resources/#r016"><code>R016</code></a></dd>
</dl>
</details>
</li>
</ul>

## S09 Capstone { #s09 }

通过可复查证据学习 Capstone。

<ul class="task-list">
<li class="progress-item" id="s09-t01">
<input type="checkbox" id="check-S09-T01" data-task-id="S09-T01" disabled>
<label for="check-S09-T01"><code>S09-T01</code> 有明确用户、明确任务、明确成功标准</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd>无</dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：有明确用户、明确任务、明确成功标准。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-09-capstone</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S09-T01.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-09-capstone/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s09-t02">
<input type="checkbox" id="check-S09-T02" data-task-id="S09-T02" disabled>
<label for="check-S09-T02"><code>S09-T02</code> 有日志、trace、错误重试、超时、成本上限</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S09-T01</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：有日志、trace、错误重试、超时、成本上限。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-09-capstone</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S09-T02.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-09-capstone/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s09-t03">
<input type="checkbox" id="check-S09-T03" data-task-id="S09-T03" disabled>
<label for="check-S09-T03"><code>S09-T03</code> 有权限边界和人工确认机制</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S09-T02</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：有权限边界和人工确认机制。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-09-capstone</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S09-T03.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-09-capstone/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s09-t04">
<input type="checkbox" id="check-S09-T04" data-task-id="S09-T04" disabled>
<label for="check-S09-T04"><code>S09-T04</code> 有部署方式：CLI、Web app、Slack bot、GitHub Action 或后台任务</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S09-T03</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：有部署方式：CLI、Web app、Slack bot、GitHub Action 或后台任务。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-09-capstone</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S09-T04.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-09-capstone/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
<li class="progress-item" id="s09-t05">
<input type="checkbox" id="check-S09-T05" data-task-id="S09-T05" disabled>
<label for="check-S09-T05"><code>S09-T05</code> 有 README：怎么运行、怎么配置 key、怎么扩展工具、有哪些限制</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>前置任务</dt><dd><code>S09-T04</code></dd>
<dt>学习成果</dt><dd><ul><li>能够解释并验证：有 README：怎么运行、怎么配置 key、怎么扩展工具、有哪些限制。</li></ul></dd>
<dt>Lab</dt><dd><code>labs/stage-09-capstone</code></dd>
<dt>产出</dt><dd><code>workbook/local/evidence/S09-T05.md</code></dd>
<dt>Rubric</dt><dd><ul><li>概念说明准确且边界清晰。</li><li>验证命令通过，并记录至少一个失败场景。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest labs/stage-09-capstone/tests</code></dd>
<dt>失败场景</dt><dd><ul><li>输入为空、无效或依赖不可用时给出可解释结果。</li></ul></dd>
<dt>安全说明</dt><dd><ul><li>使用最小权限；不把 mock、普通子进程或未验证输出描述成真实安全能力。</li></ul></dd>
<dt>资源</dt><dd>无</dd>
</dl>
</details>
</li>
</ul>
