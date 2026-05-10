from dotenv import load_dotenv
from agents.react_agent import ReActAgent 
from core.llm import HelloAgentsLLM
from tools.executor import ToolExecutor

load_dotenv()

llm_client = HelloAgentsLLM()

tool_executer=ToolExecutor()

agent = ReActAgent(llm_client=llm_client, tool_executer=tool_executer)

if __name__ == '__main__':
    
    question = "2026年华为最新的手机是哪一款？它的主要卖点是什么？"
    result = agent.run(question=question)
    print("\n--- 最终结果 ---")
    print(result)