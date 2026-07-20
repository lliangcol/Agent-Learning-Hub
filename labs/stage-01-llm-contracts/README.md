# Stage 01 Lab：LLM 契约

## 目标

用严格 JSON decoder 和字段契约解析离线 Provider 输出，区分成功、拒答和格式错误。

## 前置条件

完成 S01 概念任务；执行 `uv sync --all-extras --dev --locked`，无需 API key。

## 运行命令

`uv run pytest labs/stage-01-llm-contracts/tests`

## 预期输出

合法的单一 JSON 对象解析为 `StructuredAnswer`；错误输入返回稳定错误类别。

## 失败场景

无 JSON、多 JSON、缺字段、错类型、超长输出、越界置信度和布尔值伪装数字。

## 安全限制

不执行模型文本，不贪婪截取 JSON，不读取环境变量或调用真实 Provider。

## 完成标准

全部契约测试通过，并能解释为什么每个失败样例被拒绝。

## 扩展任务

在可选 Provider 层使用结构化输出，并保留相同的本地 schema 验证。
