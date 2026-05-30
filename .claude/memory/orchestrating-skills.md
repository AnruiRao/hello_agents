---
name: orchestrating-skills
description: 一个元技能，负责协调和指挥所有其他技能的使用
metadata:
  type: reference
---

**orchestrating-skills** 是一个元技能（meta-skill），它的作用是：

1. **自动识别任务类型** - 分析用户任务的性质（新功能、Bug 修复、重构等）
2. **智能分派子技能** - 根据任务类型调用最合适的子技能
3. **协调多步骤工作流** - 确保各个技能按正确的顺序和组合执行

## 使用方式

每次遇到复杂任务时，只需调用：
```
Skill orchestrating-skills
```

它会：
- 分析任务需要什么能力
- 自动调用相关的子技能（如 brainstorming、TDD、code-review 等）
- 协调多个子智能体并行工作（如果需要）
- 在最后进行验证

## 与 superpowers-zh 的关系

这是 superpowers-zh 技能集的**协调层**，让原本独立的 20+ 个技能能够协同工作。

## 典型应用场景

| 任务类型 | 调用的子技能序列 |
|---------|-----------------|
| 新功能实现 | brainstorming → TDD → 实现 → code-review → verification |
| Bug 修复 | systematic-debugging → TDD → 修复 → verification |
| 大规模重构 | subagent-driven-development + workflow-runner |
| 调试问题 | systematic-debugging |
| 设置配置 | update-config |

**核心价值：** 无需手动记住每个任务应该用什么技能——只需调用 orchestrating-skills，它会自动处理。
