from agents.reflection_agent import ReflectionAgent

reflection_agent = ReflectionAgent()

if __name__ == '__main__':
    input = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)"
    reflection_agent.run(task=input)