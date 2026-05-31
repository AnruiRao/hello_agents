from __future__ import annotations
from core.llm import HelloAgentsLLM
# from tools.executor import ToolExecutor
import re
from typing import TYPE_CHECKING, List
from core.agent import Agent
from core.config import Config
from core.message import Message

REACT_PROMPT_TEMPLATE = """
你是一个具备推理和行动能力的AI助手。你可以通过思考分析问题，然后调用合适的工具来获取信息，最终给出准确的答案。

## 可用工具
{tools}

## 工作流程
请严格按照以下格式进行回应，每次只能执行一个步骤:

Thought: 分析当前问题，思考需要什么信息或采取什么行动。
Action: 选择一个行动，格式必须是以下之一:
- `{{tool_name}}[{{tool_input}}]` - 调用指定工具
- `Finish[最终答案]` - 当你有足够信息给出最终答案时

## 重要提醒
1. 每次回应必须包含Thought和Action两部分
2. 工具调用的格式必须严格遵循:工具名[参数]
3. 只有当你确信有足够信息回答问题时，才使用Finish
4. 如果工具返回的信息不够，继续使用其他工具或相同工具的不同参数

## 当前任务
**Question:** {question}

## 执行历史
{history}

现在开始你的推理和行动:
"""

if TYPE_CHECKING:
    from tools.registry import ToolRegistry

class ReActAgent(Agent):
    def __init__(
        self, 
        name: str,
        llm: HelloAgentsLLM,
        tool_registry: ToolRegistry | None = None,
        system_prompt: str | None = None,
        config: Config | None = None,
        max_steps: int = 5,
        custom_prompt: str | None = None
    ):
        super().__init__(name, llm, system_prompt, config)
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.current_history:List[str] = []
        self.prompt_template = custom_prompt if custom_prompt else REACT_PROMPT_TEMPLATE 
    
    def run(self, input_text: str, **kwargs) -> str:
        """
        运行ReAct智能体来回答一个问题。
        """
        self.current_history = []
        current_step = 0    

        while current_step < self.max_steps:
            current_step += 1

            print(f"--- 第 {current_step} 步 ---")

            tools_desc = self.tool_registry.get_tools_description()
            history_str = "\n".join(self.current_history)
            prompt = self.prompt_template.format(
                tools = tools_desc,
                question = input_text,
                history = history_str
            )

            messages = [{"role":"user","content":prompt}]
            response_text = self.llm.invoke(messages, **kwargs)

            if not response_text:
                print("错误:LLM未能返回有效响应。")
                break

            thought, action = self._parse_output(response_text)

            if thought:
                print(f"思考: {thought}")

            if not action:
                print("警告:未能解析出有效的Action，流程终止。")
                break
            else:
                if  action.startswith("Finish"):
                    final_answer = re.match(r"Finish\[(.*?)\]", action, re.DOTALL).group(1)
                    print(f"🎉 最终答案: {final_answer}")
                    self.add_message(Message(input_text, "user"))
                    self.add_message(Message(final_answer, "assistant"))
                    return final_answer
    
                tool_name, tool_input = self._parse_action(action)
                if not tool_name or not tool_input:
                    # ... 处理无效Action格式 ...
                    continue

                print(f"🎬 行动: {tool_name}[{tool_input}]")

                observation = self.tool_registry.execute_tool(tool_name,tool_input)
                self.current_history.append(f'Action: {action}')
                self.current_history.append(f'Observation: {observation}')

                print(f"👀 观察: {observation}")

        final_answer = "抱歉，我无法在限定步数内完成这个任务。"

        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_answer, 'assistant'))
        return final_answer
    
    def _parse_output(self, text: str):
        """
        解析LLM的输出，提取Thought和Action。
        """
        thought_match = re.search(r"Thought:\s(.*?)(?=\nAction:|$)", text, re.DOTALL)
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)

        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None

        return thought, action
    
    def _parse_action(self, action_text: str):
        """
        解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*?)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

