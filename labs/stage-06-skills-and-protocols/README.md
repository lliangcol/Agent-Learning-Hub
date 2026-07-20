# Stage 06 Lab：Skills 与协议

## 目标

构建可发现、可版本化、带脚本/模板的 Skill，并实现无外部副作用的只读 MCP 工具。

## 前置条件

理解 Skill、Tool、Prompt 和 MCP 的边界；依赖锁定的官方 MCP Python SDK 1.28.1。

## 运行命令

`uv run pytest labs/stage-06-skills-and-protocols/tests`

## 预期输出

Skill smoke 显示来源遗漏下降；MCP client 能列出并调用 `read_course_note`。

## 失败场景

缺少 Skill 元数据、非 Markdown 输入、未知 note ID、越界路径和 MCP 契约漂移。

## 安全限制

Skill 只读显式本地 Markdown；MCP 只暴露合成内存数据，不连接外部系统。

## 完成标准

脚本、模板、触发条件和验收标准齐全，官方 in-memory transport 的 list/call 测试通过。

## 扩展任务

阅读 A2A/ACP 契约并比较协议职责，不接入生产系统。
