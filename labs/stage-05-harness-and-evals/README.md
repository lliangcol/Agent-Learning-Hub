# Stage 05 Lab：Harness、Trace 与 Evals

## 目标

在同一 20 条固定数据集上比较裸循环与 ADR-0007 选定的类型化 `AgentRunner`。

## 前置条件

完成 Stage 02 和 Stage 04；使用锁定的本仓库 Harness，不需要外部服务。

## 运行命令

`uv run pytest labs/stage-05-harness-and-evals/tests`

## 预期输出

逐条保存成功、停止原因、步骤、工具调用、延迟、错误和可选成本字段，再汇总对比。

## 失败场景

空结果、工具错误、重复调用、越权、未知响应、Provider 错误、deadline 和工具预算。

## 安全限制

数据集完全离线；成本未知时保持 `null`，不得伪造；不能按 runner 名称直接判成功。

## 完成标准

20 条场景实际执行，Harness 的每个“通过”都由观察结果与期望停止条件比较得出。

## 扩展任务

锁定一个外部 Harness 版本，在同一数据集上运行并解释 API 漂移和结果差异。
