# S08 Multi-Agent 协调

先建立单 Agent 基线，再引入 Supervisor、Worker 和 Reviewer。角色输入输出使用 schema，并设置总预算、最大轮次、无进展检测和停止条件。

评测成功率、成本、延迟与错误放大；如果没有收益，正确结论可以是“不应使用 Multi-Agent”。
