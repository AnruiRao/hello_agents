from dotenv import load_dotenv
from agents.react_agent import ReActAgent 
from core.llm import HelloAgentsLLM
from tools.registry import ToolRegistry
from tools.builtin import SearchTool, search_serpapi

load_dotenv()

llm_client = HelloAgentsLLM()

tool_registry = ToolRegistry()

search_tool = SearchTool()

tool_name = search_tool.name
tool_description = search_tool.description

tool_registry.register_function(name=tool_name, description=tool_description, func=search_serpapi)

agent = ReActAgent(name="循环助手", llm=llm_client, tool_registry=tool_registry)

if __name__ == '__main__':
    
    question = "今年苹果最新的手机是哪一款？它的主要卖点是什么？"
    result = agent.run(input_text=question)
    print("\n--- 最终结果 ---")
    print(result)