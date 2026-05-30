# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目架构

这是一个多智能体系统框架，采用分层架构设计：

### 核心层 (core/)
- **agent.py**: 抽象基类 `Agent`，定义了所有智能体的通用接口和历史记录管理
- **llm.py**: `HelloAgentsLLM` 类，封装了与大语言模型的交互，支持自动检测和配置不同的 LLM 提供商（如 SiliconFlow、DashScope 等）
- **config.py**: 配置管理
- **message.py**: 消息数据结构

### 智能体层 (agents/)
实现了多种智能体模式：
- **simple_agent.py**: 基础对话智能体，维护对话历史
- **react_agent.py**: ReAct（Reasoning + Action）智能体，支持工具调用和多步推理
- **plan_solve_agent.py**: Plan-and-Solve 智能体，先规划后执行的两阶段推理
- **reflection_agent.py**: Reflection 智能体，包含自我反思和改进机制

### 工具层 (tools/)
- **executor.py**: `ToolExecutor` 类，管理可用工具的注册和执行，当前集成了 SerpApi 搜索引擎

### 其他组件
- **others/**: 示例和参考实现
  - `autogen.py`: 基于 AutoGen 框架的多智能体协作示例
  - `hello_agents.py`, `my_llm.py`, `my_simple_agent.py`: 简化的示例实现

## 开发命令

### 虚拟环境
项目使用名为 `.hello_agents` 的 Python 虚拟环境。在运行任何命令前，请先激活虚拟环境：

```bash
# 激活虚拟环境（macOS/Linux）
source .hello_agents/bin/activate

# 激活虚拟环境（Windows）
.hello_agents\Scripts\activate
```

### 环境设置
1. 复制 `.env.example` 到 `.env` 并配置 API 密钥（确保在激活的虚拟环境中操作）：
   - `LLM_API_KEY`, `LLM_MODEL_ID`, `LLM_BASE_URL` - 主要 LLM 提供商配置
   - `SILICON_API_KEY`, `SILICON_MODEL_ID`, `SILICON_BASE_URL` - SiliconFlow 提供商配置  
   - `SERPAPI_API_KEY` - 搜索引擎 API 密钥

### 运行测试
```bash
# 确保已激活 .hello_agents 虚拟环境
# 运行 Simple Agent 测试
python test_main_tools.py

# 运行 ReAct Agent 测试  
python test_main_react.py

# 运行 Plan-and-Solve Agent 测试
python test_main_planSolve.py

# 运行 Reflection Agent 测试
python test_main_reflection.py

# 运行基础 LLM 测试
python others/hello_agents.py

# 运行 SimpleAgent 单元测试
python test_simple_agent.py
```

### 运行 AutoGen 多智能体示例
```bash
python others/autogen.py
```

## 依赖管理
项目使用 Python 标准库和以下主要依赖：
- `openai` - OpenAI 兼容的 API 客户端
- `python-dotenv` - 环境变量加载
- `serpapi` - 搜索引擎 API 客户端
- `autogen-agentchat`, `autogen-ext` - AutoGen 多智能体框架（可选）

**重要：确保在激活 `.hello_agents` 虚拟环境后安装依赖：**

```bash
# 激活虚拟环境后安装依赖
pip install openai python-dotenv serpapi
# AutoGen 相关依赖（按需安装）
pip install autogen-agentchat autogen-ext
```

## 智能体开发指南

### 添加新智能体
1. 在 `agents/` 目录下创建新的智能体类
2. 继承 `core.agent.Agent` 抽象基类
3. 实现 `run()` 方法的核心逻辑
4. 创建对应的测试文件（如 `test_main_<agent_name>.py`）

### 添加新工具
1. 在 `tools/executor.py` 中定义工具函数
2. 在 `ToolExecutor.__init__()` 中注册新工具
3. 确保工具描述清晰说明其用途和适用场景

### LLM 提供商支持
`HelloAgentsLLM` 支持自动检测和配置不同的 LLM 提供商。添加新提供商支持需要：
1. 在 `_auto_detect_provider()` 方法中添加检测逻辑
2. 在 `_resolve_credentials()` 方法中添加凭证解析逻辑

<!-- superpowers-zh:begin (do not edit between these markers) -->
# Superpowers-ZH 中文增强版

本项目已安装 superpowers-zh 技能框架（20 个 skills）。

## 核心规则

1. **收到任务时，先检查是否有匹配的 skill** — 哪怕只有 1% 的可能性也要检查
2. **设计先于编码** — 收到功能需求时，先用 brainstorming skill 做需求分析
3. **测试先于实现** — 写代码前先写测试（TDD）
4. **验证先于完成** — 声称完成前必须运行验证命令

## 可用 Skills

Skills 位于 `.claude/skills/` 目录，每个 skill 有独立的 `SKILL.md` 文件。

- **brainstorming**: 在任何创造性工作之前必须使用此技能——创建功能、构建组件、添加功能或修改行为。在实现之前先探索用户意图、需求和设计。
- **chinese-code-review**: 中文 review 沟通参考——话术模板、分级标注（必须修复/建议修改/仅供参考）、国内团队常见反模式应对。仅在用户显式 /chinese-code-review 时调用，不要根据上下文自动触发。
- **chinese-commit-conventions**: 中文 commit 与 changelog 配置参考——Conventional Commits 中文适配、commitlint/husky/commitizen 中文模板、conventional-changelog 中文配置。仅在用户显式 /chinese-commit-conventions 时调用，不要根据上下文自动触发。
- **chinese-documentation**: 中文文档排版参考——中英文空格、全半角标点、术语保留、链接格式、中文文案排版指北约定。仅在用户显式 /chinese-documentation 时调用，不要根据上下文自动触发。
- **chinese-git-workflow**: 国内 Git 平台配置参考——Gitee、Coding.net、极狐 GitLab、CNB 的 SSH/HTTPS/凭据/CI 接入差异与镜像同步配置。仅在用户显式 /chinese-git-workflow 时调用，不要根据上下文自动触发。
- **dispatching-parallel-agents**: 当面对 2 个以上可以独立进行、无共享状态或顺序依赖的任务时使用
- **executing-plans**: 当你有一份书面实现计划需要在单独的会话中执行，并设有审查检查点时使用
- **finishing-a-development-branch**: 当实现完成、所有测试通过、需要决定如何集成工作时使用——通过提供合并、PR 或清理等结构化选项来引导开发工作的收尾
- **mcp-builder**: MCP 服务器构建方法论 — 系统化构建生产级 MCP 工具，让 AI 助手连接外部能力
- **receiving-code-review**: 收到代码审查反馈后、实施建议之前使用，尤其当反馈不明确或技术上有疑问时——需要技术严谨性和验证，而非敷衍附和或盲目执行
- **requesting-code-review**: 完成任务、实现重要功能或合并前使用，用于验证工作成果是否符合要求
- **subagent-driven-development**: 当在当前会话中执行包含独立任务的实现计划时使用
- **systematic-debugging**: 遇到任何 bug、测试失败或异常行为时使用，在提出修复方案之前执行
- **test-driven-development**: 在实现任何功能或修复 bug 时使用，在编写实现代码之前
- **using-git-worktrees**: 当需要开始与当前工作区隔离的功能开发，或在执行实现计划之前使用——通过原生工具或 git worktree 回退机制确保隔离工作区存在
- **using-superpowers**: 在开始任何对话时使用——确立如何查找和使用技能，要求在任何响应（包括澄清性问题）之前调用 Skill 工具
- **verification-before-completion**: 在宣称工作完成、已修复或测试通过之前使用，在提交或创建 PR 之前——必须运行验证命令并确认输出后才能声称成功；始终用证据支撑断言
- **workflow-runner**: 在 Claude Code / OpenClaw / Cursor 中直接运行 agency-orchestrator YAML 工作流——无需 API key，使用当前会话的 LLM 作为执行引擎。当用户提供 .yaml 工作流文件或要求多角色协作完成任务时触发。
- **writing-plans**: 当你有规格说明或需求用于多步骤任务时使用，在动手写代码之前
- **writing-skills**: 当创建新技能、编辑现有技能或在部署前验证技能是否有效时使用

**元技能（协调层）：**
- **orchestrating-skills**: 技能指挥器——面对复杂任务或多步骤工作流时调用此技能即可，它会自动识别任务类型并分派最合适的子技能组合

## 如何使用

当任务匹配某个 skill 时，使用 `Skill` 工具加载对应 skill 并严格遵循其流程。绝不要用 Read 工具读取 SKILL.md 文件。

如果你认为哪怕只有 1% 的可能性某个 skill 适用于你正在做的事情，你必须调用该 skill 检查。
<!-- superpowers-zh:end -->
