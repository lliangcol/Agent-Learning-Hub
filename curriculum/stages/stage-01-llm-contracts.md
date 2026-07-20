# S01 LLM API 与结构化契约

默认使用 `SequenceProvider` 离线完成消息与结构化输出练习。可选 OpenAI Provider 只从环境变量读取密钥，并使用 Responses API；没有真实调用证据时不得标为 live verified。

重点检查无 JSON、多 JSON、缺字段、错类型、超长输出和拒答。正则贪婪截取不是推荐协议解析方式。
