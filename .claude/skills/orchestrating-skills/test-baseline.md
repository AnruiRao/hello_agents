# 基线压力场景

## 场景 1：多阶段功能实现

**任务：** "帮我实现一个带用户认证的 REST API"

**预期智能体应该做的事：**
1. 先用 brainstorming 探索需求和设计
2. 用 test-driven-development 写测试
3. 实现代码
4. 用 code-review 检查
5. 最后用 verification-before-completion 验证

**记录基线行为（不使用指挥技能时）：**
- 智能体会跳过多步骤？
- 智能体会直接写代码不写测试？
- 智能体会忘记审查和验证？

---

## 场景 2：问题调试

**任务：** "这个测试总是失败，帮我修复"

**预期智能体应该做的事：**
1. 用 systematic-debugging 系统诊断
2. 可能用到 root-cause-tracing
3. 修改后用 verification-before-completion 验证

**记录基线行为：**
- 智能体会跳过调试直接猜测？
- 智能体会修复但不验证？

---

## 场景 3：大规模重构

**任务：** "把整个项目从 Python 迁移到 TypeScript"

**预期智能体应该做的事：**
1. 用 workflow-runner 或 subagent-driven-development 分派任务
2. 每个模块用 plan-solve-agent 式的规划
3. 每部分完成后审查

**记录基线行为：**
- 智能体会试图一次处理太多？
- 智能体会失去组织性？
