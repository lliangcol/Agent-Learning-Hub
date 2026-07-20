# S03 RAG、上下文与记忆

离线检索采用中文字符 n-gram，并用固定数据集验证。Chunk 保存文档 ID、标题、URI、偏移与正文；引用验证检查存在性、完整性和支持关系。

Session Memory 使用滑动窗口与累积摘要。Long-term Memory 使用 SQLite、显式持久化许可、TTL、版本、敏感级别及查看/纠正/删除/清空接口。
