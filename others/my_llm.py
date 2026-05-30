import os
from openai import OpenAI
# from typing import Optional
from core.llm import HelloAgentsLLM
from dotenv import load_dotenv

load_dotenv()

class MyLLM(HelloAgentsLLM):
    
    def __init__(self, 
                model: str | None = None,
                apiKey: str | None = None, 
                baseUrl: str | None = None, 
                provider: str | None = "auto",
                **kwargs
    ):
        if provider == "qwen":
            print("正在使用自定义的 Qwen Provider")
            self.provider = "qwen"

            self.apiKey = apiKey or os.getenv("QWEN_API_KEY")
            self.baseUrl = baseUrl or "https://dashscope.aliyuncs.com/compatible-mode/v1"

            if not self.apiKey:
                raise ValueError("QWEN API key not found. Please set QWEN_API_KEY environment variable.")
             
            self.model = model or os.getenv("QWEN_MODEL_ID")
            self.temperature = kwargs.get("temperature", 0.7)
            self.maxTokens = kwargs.get("maxTokens")
            self.timeout = kwargs.get("timeout",60)

            print(self.apiKey)
            print(self.baseUrl)
            self.client = OpenAI(api_key=self.apiKey, base_url=self.baseUrl, timeout=self.timeout)

        else:
            super().__init__(model=model, apiKey=apiKey, baseUrl=baseUrl, timeout=kwargs.get("timeout",60))
             
