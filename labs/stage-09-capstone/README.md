# Stage 09 Lab：Capstone

## 目标

从研究助手、代码审查助手、个人知识助手中选择一个，形成可安装、可测试的发布基线。

## 前置条件

完成前序核心 Lab，并明确用户、任务、成功标准、权限和固定 eval 数据集。

## 运行命令

`uv run pytest labs/stage-09-capstone/tests`

`uv run python labs/stage-09-capstone/solution/demo.py`

## 预期输出

本地 CLI 对五类固定场景输出脱敏状态、停止原因和引用，不产生外部副作用。

## 失败场景

无来源、外部访问请求、敏感输入、错误格式、manifest 缺字段和路径越界。

## 安全限制

默认只读本地 fixture；不发布、不发消息、不访问生产数据，也不保存 secrets。

## 完成标准

三个方向共享发布清单；选择的方向具备 manifest、eval、日志、部署、限制和回滚。

## 扩展任务

完成另一个方向的本地 CLI，但保持相同发布门和无外部副作用策略。
