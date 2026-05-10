from .core.llm import HelloAgentsLLM
from .agents.simple_agent import SimpleAgent
from .core.config import Config

class MysimpleAgent(SimpleAgent):

    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: str | None = None,
            config: Config | None = None,
            # tool_registry: 'ToolRegistry' | None = None,
            enable_tool_calling: bool = True
    ):
        super().__init__(name, llm, system_prompt, config)
        