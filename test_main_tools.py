import os
from dotenv import load_dotenv
# from llm.my_llm import MyLLM
from tools.executor import ToolExecutor
from tools.search import search

load_dotenv()

if __name__ == '__main__':
    toolExecutot = ToolExecutor()

    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutot.registerTool("Search",description=search_description,func=search)

    print("\n--- 可用的工具 ---")
    print(toolExecutot.getAvailableTools())

    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutot.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")