from ..core.agent import Agent
from ..core.llm import HelloAgentsLLM
from ..core.config import Config
from typing import List, Dict

class SimpleAgent(Agent):
    
    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: str | None = None,
            config: Config | None= None
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self._history = []

    def run(self, input_text: str) -> str:
        
        messages = self._build_messages(input_text)
        response = self.llm.think(messages)

        self._history.append(("user", input_text))
        self._history.append(("assistant", response))

        return response


    def _build_messages(self, input_text: str) -> List[Dict[str, str]]:
        messages = []

        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        if self._history:
            for role, content in self._history:
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": input_text})
        return messages