# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目架构

这是一个多智能体系统框架，采用分层架构设计：

### 核心层 (core/)
- **agent.py**: 抽象基类 `Agent`，定义了所有智能体的通用接口和历史记录管理
- **llm.py**: `HelloAgentsLLM` 类，封装了与大语言模型的交互，支持自动检测和配置不同的LLM提供商（如SiliconFlow、DashScope等）
- **config.py**: 配置管理
- **message.py**: 消息数据结构

### 智能体层 (agents/)
实现了多种智能体模式：
- **simple_agent.py**: 基础对话智能体，维护对话历史
- **react_agent.py**: ReAct（Reasoning + Action）智能体，支持工具调用和多步推理
- **plan_solve_agent.py**: Plan-and-Solve 智能体，先规划后执行的两阶段推理
- **reflection_agent.py**: Reflection 智能体，包含自我反思和改进机制

### 工具层 (tools/)
- **executor.py**: `ToolExecutor` 类，管理可用工具的注册和执行，当前集成了SerpApi搜索引擎

### 其他组件
- **autogen.py**: 基于AutoGen框架的多智能体协作示例，包含产品经理、工程师、代码审查员和用户代理
- **hello_agents.py**: 主模块入口，包含 `HelloAgentsLLM` 的完整实现
- **my_llm.py**, **my_simple_agent.py**: 简化的示例实现

## 开发命令

### 虚拟环境
项目使用名为 `.hello_agents` 的Python虚拟环境。在运行任何命令前，请先激活虚拟环境：

```bash
# 激活虚拟环境（macOS/Linux）
source .hello_agents/bin/activate

# 激活虚拟环境（Windows）
.hello_agents\Scripts\activate
```

### 环境设置
1. 复制 `.env.example` 到 `.env` 并配置API密钥（确保在激活的虚拟环境中操作）：
   - `LLM_API_KEY`, `LLM_MODEL_ID`, `LLM_BASE_URL` - 主要LLM提供商配置
   - `SILICON_API_KEY`, `SILICON_MODEL_ID`, `SILICON_BASE_URL` - SiliconFlow提供商配置  
   - `SERPAPI_API_KEY` - 搜索引擎API密钥

### 运行测试
```bash
# 确保已激活 .hello_agents 虚拟环境
# 运行Simple Agent测试
python test_main_tools.py

# 运行ReAct Agent测试  
python test_main_react.py

# 运行Plan-and-Solve Agent测试
python test_main_planSolve.py

# 运行Reflection Agent测试
python test_main_reflection.py

# 运行基础LLM测试
python hello_agents.py
```

### 运行AutoGen多智能体示例
```bash
python autogen.py
```

## 依赖管理
项目使用Python标准库和以下主要依赖：
- `openai` - OpenAI兼容的API客户端
- `python-dotenv` - 环境变量加载
- `serpapi` - 搜索引擎API客户端
- `autogen-agentchat`, `autogen-ext` - AutoGen多智能体框架（可选）

**重要：确保在激活 `.hello_agents` 虚拟环境后安装依赖：**

```bash
# 激活虚拟环境后安装依赖
pip install openai python-dotenv serpapi
# AutoGen相关依赖（按需安装）
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

### LLM提供商支持
`HelloAgentsLLM` 支持自动检测和配置不同的LLM提供商。添加新提供商支持需要：
1. 在 `_auto_detect_provider()` 方法中添加检测逻辑
2. 在 `_resolve_credentials()` 方法中添加凭证解析逻辑