from typing import Dict, List, Any
from .base import Tool
from typing import Callable

class ToolRegistry:
    """
    HelloAgents工具注册表

    提供工具的注册、管理和执行功能。
    支持两种工具注册方式：
    1. Tool对象注册（推荐）
    2. 函数直接注册（简便）
    """
    def __init__(self):
        self._tools:Dict[str, Tool] = {}
        self._tool_functions: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, tool: Tool):
        """注册Tool对象"""
        if tool.name in self._tools:
            print(f"⚠️ 警告:工具 '{tool.name}' 已存在，将被覆盖。")
        self._tools[tool.name] = tool
        print(f"✅ 工具 '{tool.name}' 已注册。")

    def register_function(self, name: str, description: str, func: Callable[[str], str]):
        """
        直接注册函数作为工具（简便方式）

        Args:
            name: 工具名称
            description: 工具描述
            func: 工具函数，接受字符串参数，返回字符串结果
        """
        if name in self._tool_functions:
            print(f"⚠️ 警告:工具 '{name}' 已存在，将被覆盖。")
        self._tool_functions[name] = {
            "description": description,
            "func": func
        }
        print(f"✅ 工具 '{name}' 已注册。")

    def unregister(self, name: str):
        """注销工具"""
        if name in self._tools:
            del self._tools[name]
            print(f"🗑️ 工具 '{name}' 已注销。")
        elif name in self._tool_functions:
            del self._tool_functions[name]
            print(f"🗑️ 工具 '{name}' 已注销。")
        else:
            print(f"⚠️ 工具 '{name}' 不存在。")

    def clear(self):
        """清空所有工具"""
        self._tools.clear(),
        self._tool_functions.clear()
        print("🧹 所有工具已清空。")

    def get_tool(self, name: str) -> Tool | None:
        """获取Tool对象"""
        return self._tools.get(name)
    
    def get_function(self, name: str) -> Callable | None:
        """获取工具函数"""
        func_info = self._tool_functions.get(name)
        return func_info["func"] if func_info else None

    def get_tools_description(self) -> str:
        """获取所有可用工具的格式化描述字符串"""
        descriptions = []

        for tool in self._tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")

        for name, info in self._tool_functions:
            descriptions.append(f"- {name}: {info['description']}")

        return "\n".join(descriptions) if descriptions else "暂无可用工具"
    
    def list_tools(self) -> list[str]:
        """列出所有工具名称"""
        return list(self._tools.keys()) + list(self._tool_functions.keys())
    
    def get_all_tools(self) -> list[Tool]:
        """获取所有Tool对象"""
        return list(self._tools.values())

    def execute_tool(self, name: str, input_text: str) ->str:
        """
        执行工具

        Args:
            name: 工具名称
            input_text: 输入参数

        Returns:
            工具执行结果
        """
        if name in self._tools:
            tool = self._tools[name]
            try:
                return tool.run({"input": input_text})
            except Exception as e:
                return f"错误：执行工具 '{name}' 时发生异常: {str(e)}"

        elif name in self._tool_functions:
            func = self._tool_functions[name]["func"]
            try:
                return func(input_text)
            except Exception as e:
                return f"错误：执行工具 '{name}' 时发生异常: {str(e)}"
        
        else:
            return f"错误：未找到名为 '{name}' 的工具。"

global_registry = ToolRegistry()




    # def to_openai_schema(self) -> Dict[str, Any]:
    #     """转换为 OpenAI function calling schema 格式

    #     用于 FunctionCallAgent，使工具能够被 OpenAI 原生 function calling 使用

    #     Returns:
    #         符合 OpenAI function calling 标准的 schema
    #     """
    #     parameters = self.get_parameters()

    #     properties = {}
    #     required = []

    #     for param in parameters:
    #         prop = {
    #             "type": param.type,
    #             "description": param.description
    #         }