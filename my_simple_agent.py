from .core.llm import HelloAgentsLLM
from .agents.simple_agent import SimpleAgent
from .core.config import Config
from typing import TYPE_CHECKING

import re

if TYPE_CHECKING:
    from .tools.registry import ToolRegistry

class MysimpleAgent(SimpleAgent):

    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: str | None = None,
            config: Config | None = None,
            tool_registry: 'ToolRegistry' | None = None,
            enable_tool_calling: bool = True
    ):
        super().__init__(name, llm, system_prompt, config)
        self.tool_registry = tool_registry
        self.enable_tool_calling = enable_tool_calling and tool_registry is not None

        print(f"✅ {name} 初始化完成，工具调用: {'启用' if self.enable_tool_calling else '禁用'}")
        

    def run(self, input_text: str, **kwargs) -> str:
        
        print(f"🤖 {self.name} 正在处理: {input_text}")
        
        messages = []

        enhanced_system_prompt = self._get_enhanced_system_prompt()
        messages.append({"role": "system", "content": enhanced_system_prompt})

        for msg in self._history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": input_text})

        if not self.enable_tool_calling:
            response = self.llm.invoke(messages, **kwargs)



    def _get_enhanced_system_prompt(self) -> str:
        """构建增强的系统提示词，包含工具信息"""
        base_prompt = self.system_prompt or "你是一个有用的AI助手。"

        if not self.enable_tool_calling or not self.tool_registry:
            return base_prompt
