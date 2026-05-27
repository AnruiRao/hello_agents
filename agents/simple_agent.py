from ..core.agent import Agent
from ..core.llm import HelloAgentsLLM
from ..core.config import Config
from typing import List, Dict ,TYPE_CHECKING

import re

from ..core.message import Message

if TYPE_CHECKING:
    from ..tools.registry import ToolRegistry

class SimpleAgent(Agent):
    
    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: str | None = None,
            config: Config | None= None,
            tool_registry: 'ToolRegistry' | None = None,
            enable_tool_calling: bool = True,
            max_tool_iterations: int = 3
    ):
        super().__init__(name, llm, system_prompt, config, tool_registry)
        self.enable_tool_calling = enable_tool_calling and tool_registry is not None
        self.max_tool_iterations = max_tool_iterations

    def run(self, input_text: str, **kwargs) -> str:

        messages = self._build_messages(input_text)
        response = self.llm.invoke(messages, **kwargs)

        self.add_message(Message(input_text, "user"))
        self.add_message(Message(response, "assistant"))

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