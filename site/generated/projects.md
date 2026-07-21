---
title: 项目阶梯
description: 可选项目与独立进度
---

# 项目阶梯

<p data-progress-summary role="status" aria-live="polite">项目进度正在加载…</p>

<ul class="project-list">
<li class="progress-item" id="p01">
<input type="checkbox" id="check-P01" data-project-id="P01" disabled>
<label for="check-P01"><code>P01</code> Calculator Agent · 基础工具</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>beginner</dd>
<dt>前置任务</dt><dd><code>S02-T03</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P01/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 最小 tool call loop。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>2-4h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p02">
<input type="checkbox" id="check-P02" data-project-id="P02" disabled>
<label for="check-P02"><code>P02</code> Web Research Agent · 研究与 RAG</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>beginner</dd>
<dt>前置任务</dt><dd><code>S02-T03</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P02/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 搜索、筛选、引用、总结。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>4-6h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p03">
<input type="checkbox" id="check-P03" data-project-id="P03" disabled>
<label for="check-P03"><code>P03</code> PDF QA Agent · 研究与 RAG</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>beginner</dd>
<dt>前置任务</dt><dd><code>S02-T03</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P03/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 RAG、chunk、retrieval、citation。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>6-9h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p04">
<input type="checkbox" id="check-P04" data-project-id="P04" disabled>
<label for="check-P04"><code>P04</code> Coding Review Agent · Coding Agent</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>intermediate</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P04/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 读取 diff、风险排序、测试建议。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>8-12h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p05">
<input type="checkbox" id="check-P05" data-project-id="P05" disabled>
<label for="check-P05"><code>P05</code> Browser Agent · Browser 与 Computer Use</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>intermediate</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P05/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 页面观察、点击、提取、失败恢复。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>10-15h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p06">
<input type="checkbox" id="check-P06" data-project-id="P06" disabled>
<label for="check-P06"><code>P06</code> Claude Code-like Nano Agent · Coding Agent</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>intermediate</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P06/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 shell、文件编辑、权限、session、compact。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>12-18h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p07">
<input type="checkbox" id="check-P07" data-project-id="P07" disabled>
<label for="check-P07"><code>P07</code> OpenClaw-like Gateway · Personal Agent</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>intermediate</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P07/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 channel、routing、session、memory、heartbeat、delivery。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>14-21h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p08">
<input type="checkbox" id="check-P08" data-project-id="P08" disabled>
<label for="check-P08"><code>P08</code> Reusable Skill Pack · Skills 与协议</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>intermediate</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P08/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 SKILL.md、脚本、模板、触发条件、smoke test。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>16-24h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p09">
<input type="checkbox" id="check-P09" data-project-id="P09" disabled>
<label for="check-P09"><code>P09</code> Multi-Agent Writer · Multi-Agent</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>advanced</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P09/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 planner、writer、reviewer 协作。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>18-27h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p10">
<input type="checkbox" id="check-P10" data-project-id="P10" disabled>
<label for="check-P10"><code>P10</code> Personal Agent · Personal Agent</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>advanced</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P10/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 OpenClaw/Hermes-style 记忆、skills、消息入口。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>20-30h</dd>
</dl>
</details>
</li>
<li class="progress-item" id="p11">
<input type="checkbox" id="check-P11" data-project-id="P11" disabled>
<label for="check-P11"><code>P11</code> Production Harness · Production Harness</label>
<details class="acceptance-details">
<summary>查看前置条件与验收</summary>
<dl>
<dt>难度</dt><dd>advanced</dd>
<dt>前置任务</dt><dd><code>S04-T08</code></dd>
<dt>产出</dt><dd><code>workbook/local/projects/P11/README.md</code></dd>
<dt>Rubric</dt><dd><ul><li>产物展示 evals、trace、权限、CI、runner、回放。</li><li>验证命令、限制与回滚方式完整。</li></ul></dd>
<dt>验证命令</dt><dd><code>uv run pytest</code></dd>
<dt>安全说明</dt><dd><ul><li>只使用合成数据；外部发布或高风险动作需要用户批准。</li></ul></dd>
<dt>预计投入</dt><dd>22-33h</dd>
</dl>
</details>
</li>
</ul>

项目全部可选，不计入课程任务总完成率。
