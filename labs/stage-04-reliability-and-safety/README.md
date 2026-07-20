# Stage 04 Lab：可靠性与安全

## 目标

练习权限、幂等、缓存、重试、文件边界，以及可选容器代码执行的真实边界。

## 前置条件

完成 Agent Loop；核心测试不要求 Docker，容器 smoke 需要维护者另行批准。

## 运行命令

`uv run pytest labs/stage-04-reliability-and-safety/tests tests/unit/test_registry_and_policies.py`

## 预期输出

只读调用可缓存；副作用调用需要批准和幂等 key；路径穿越与隐式覆盖被拒绝。

## 失败场景

临时错误、致命错误、越权调用、幂等冲突、路径穿越、Docker 不可用和超时。

## 安全限制

普通子进程不是沙箱。可选容器禁网络、只读根、非 root，并限制 CPU、内存、进程和时间。

## 完成标准

权限、重试、文件和容器命令测试通过；容器 smoke 未获明确 opt-in 时报告 skip；
没有任意不可信代码进入默认实验。

## 扩展任务

在获得批准后运行一次容器 smoke，并记录镜像 digest、环境和清理结果。
