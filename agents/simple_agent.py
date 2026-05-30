from __future__ import annotations
from core.agent import Agent
from core.llm import HelloAgentsLLM
from core.config import Config
from typing import List, Dict, TYPE_CHECKING, Iterator
from tools.base import Tool


import re

from core.message import Message

if TYPE_CHECKING:
    from tools.registry import ToolRegistry

class SimpleAgent(Agent):
    
    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: str | None = None,
            config: Config | None = None,
            tool_registry: ToolRegistry | None = None,
            enable_tool_calling: bool = True,
            max_tool_iterations: int = 3
    ):
        super().__init__(name, llm, system_prompt, config, tool_registry)
        self.enable_tool_calling = enable_tool_calling and tool_registry is not None
        self.max_tool_iterations = max_tool_iterations

    def run(self, input_text: str, **kwargs) -> str:

        messages = self._build_messages(input_text)

        if not self.enable_tool_calling or not self.tool_registry:
            response = self.llm.invoke(messages, **kwargs)

            self.add_message(Message(input_text, "user"))
            self.add_message(Message(response, "assistant"))

            return response

        response = ""

        return response


    def _build_messages(self, input_text: str) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages = []

        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        for msg in self._history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": input_text})
        return messages
    
    def stream_run(self, input_text: str, **kwargs) -> Iterator[str]:
        """
        流式运行Agent
        
        Args:
            input_text: 用户输入
            **kwargs: 其他参数
            
        Yields:
            Agent响应片段
        """
        messages = self._build_messages(input_text)
        
        full_response = ""
        for chunk in self.llm.stream_invoke(messages, **kwargs):
            full_response += chunk
            yield chunk

        self.add_message(Message(input_text, "user"))
        self.add_message(Message(full_response, "assistant"))

    def add_tool(self, tool: Tool) -> None:
        """添加工具到Agent（便利方法）"""
        if not self.tool_registry:
            from tools.registry import ToolRegistry
            self.tool_registry = ToolRegistry()
            self.enable_tool_calling = True

        self.tool_registry.register_tool(tool)

    def has_tools(self) -> bool:
        """检查是否有可用工具"""
        return self.enable_tool_calling and self.tool_registry is not None
    
    def remove_tool(self, tool_name: str) -> bool:
        """移除工具"""
        if self.tool_registry:
            self.tool_registry.unregister(tool_name)
            return True
        return False
    
    def list_tools(self) -> list:
        """列出所有可用工具"""
        if self.tool_registry:
            return self.tool_registry.list_tools()
        return []
            