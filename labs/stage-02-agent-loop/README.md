# Stage 02 Lab：Agent Loop

## 目标

运行带状态、停止原因、工具预算、重复检测、超时和结构化工具结果的离线 Agent。

## 前置条件

完成 Stage 01 Lab；执行 `uv sync --all-extras --dev --locked`。

## 运行命令

`uv run pytest labs/stage-02-agent-loop/tests`

## 预期输出

计算器返回真实数值，Mock Provider 从工具消息生成最终回答，并记录 trace。

## 失败场景

未知响应、Provider 错误、工具超时、重复调用、最大步骤和工具预算耗尽。

## 安全限制

只使用注册的安全计算器；Mock 是离线证据，不表示真实 API 已验证。

## 完成标准

改变计算表达式会改变最终回答，且每条停止路径都有自动化测试。

## 扩展任务

增加一个只读工具，并比较不同 deadline、步骤和重复阈值。
