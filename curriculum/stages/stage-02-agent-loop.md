# S02 Agent Loop 与工具调用

Agent Loop 使用明确的 `AgentState` 与 `StopReason`，区分文字、工具调用、未知响应和 Provider 错误。模型调用、工具调用、总 deadline、最大步骤、工具预算和重复调用检测分别生效。

工具结果保持结构化。最终回答必须基于真实工具结果，不能用与结果无关的硬编码答案冒充成功。
