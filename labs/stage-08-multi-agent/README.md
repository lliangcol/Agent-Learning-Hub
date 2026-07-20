# Stage 08 Lab：Multi-Agent

## 目标

比较单 Agent 与 Supervisor/Worker/Reviewer，并允许结论为“不应使用多 Agent”。

## 前置条件

理解输入输出 schema、预算、停止条件和基线评测；实验完全离线。

## 运行命令

`uv run pytest labs/stage-08-multi-agent/tests`

## 预期输出

报告成功率、轮次、消息、成本单位、延迟和错误放大，并给出可解释推荐。

## 失败场景

预算不足、最大轮次不足、Worker 无进展、Reviewer 拒绝和错误放大。

## 安全限制

角色边界固定，不让 Agent 自由聊天；总预算和停止条件不可由 Worker 覆盖。

## 完成标准

相同任务的单 Agent 基线与多 Agent 流程都执行；更高成本且无收益时推荐单 Agent。

## 扩展任务

增加一个多 Agent 确有收益的合成任务，并预先定义收益阈值。
