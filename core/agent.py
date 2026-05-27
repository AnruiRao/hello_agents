from abc import ABC, abstractmethod
from typing import List
from .message import Message
from .llm import HelloAgentsLLM
from .config import Config
from ..tools.registry import ToolRegistry

class Agent(ABC):

    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: str | None = None,
            config: Config | None = None,
            tool_registry: 'ToolRegistry' | None = None
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config or Config()
        self._history = list[Message] = []

        self.tool_registry = tool_registry

    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        """运行Agent"""
        pass

    def add_message(self, message: Message):
        """添加消息到历史记录"""
        self._history.append(message)

    def clean_history(self):
        """清空历史记录"""
        self._history.clear()

    def get_history(self) -> List[Message]:
        """获取历史记录"""
        return self._history.copy()
    
    def __str__(self) -> str:
        return f"Agent(name={self.name}, provider={self.llm.provider})"
    
