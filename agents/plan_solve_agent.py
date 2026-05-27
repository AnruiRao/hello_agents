from core.llm import HelloAgentsLLM
from typing import List
import ast

PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划,```python与```作为前后缀是必要的:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

EXECUTOR_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""

class Planner:
    def __init__(self, llm_client: HelloAgentsLLM | None = None):
        self.llm_client = llm_client or HelloAgentsLLM()


    def plan(self, question: str) -> List[str]:
        """
        根据用户问题生成一个行动计划。
        """
        prompt = PLANNER_PROMPT_TEMPLATE.format(question=question)

        messages = [{"role":"user","content":prompt}]

        print("--- 正在生成计划 ---")
        response_text = self.llm_client.invoke(messages=messages) or ""
        print(f"✅ 计划已生成:\n{response_text}")

        try:
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan,list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_text}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []

class Executor:
    def __init__(self, llm_client: HelloAgentsLLM | None = None):
        self.llm_client = llm_client or HelloAgentsLLM()

    def execute(self, question: str, plan: List[str]) -> str:
        """
        根据计划，逐步执行并解决问题。
        """
        history = ""

        print("\n--- 正在执行计划 ---")

        for i, step in enumerate(plan):
            print(f"\n-> 正在执行步骤 {i+1}/{len(plan)}：{step}")

            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=question, 
                plan=plan,
                history=history if history else "无",
                current_step=step
            )

            messages = [{"role":"user", "content":prompt}]

            response_text = self.llm_client.invoke(messages=messages) or ""
            history += f"步骤 {i+1}： {step}\n结果： {response_text}\n\n" 
            print(f"✅ 步骤 {i+1} 已完成，结果: {response_text}")

        final_answer = response_text
        return final_answer

class PlanAndSolveAgent:
    def __init__(self, llm_client: HelloAgentsLLM | None = None):
        """
        初始化智能体，同时创建规划器和执行器实例。
        """
        self.llm_client = llm_client or HelloAgentsLLM()
        self.planner = Planner(self.llm_client)
        self.executor = Executor(self.llm_client)

    def run(self, question: str):
        """
        运行智能体的完整流程:先规划，后执行。
        """
        print(f"\n--- 开始处理问题 ---\n问题: {question}")

        plan = self.planner.plan(question=question)

        if not plan:
            print("\n--- 任务终止 --- \n无法生成有效的行动计划。")
            return
        
        final_answer = self.executor.execute(question=question, plan=plan)

        print(f"\n--- 👾任务完成 ---\n最终答案: {final_answer}")