# Stage 03 Lab：RAG 与记忆

## 目标

验证中文离线检索、人工标注的 claim-to-chunk 支持关系和 SQLite 长期记忆。

## 前置条件

理解 chunk、citation、session memory 和持久化同意；无需 embedding 服务。

## 运行命令

`uv run pytest labs/stage-03-rag-and-memory/tests`

## 预期输出

固定中文查询命中预期 chunk；错误支持关系被拒绝；跨进程记忆可删除且不再检索。

## 失败场景

无检索结果、未知引用、漏引、不支持结论、TTL 过期、不兼容 schema 和秘密写入。

## 安全限制

只使用合成数据；长期写入需要显式许可，秘密和验证码默认拒绝。

## 完成标准

检索与引用固定集、持久化、迁移备份、纠正、删除、清空和导出测试通过。

## 扩展任务

在独立人工标注集上抽查自由生成答案，不把 LLM-as-judge 作为唯一门禁。
