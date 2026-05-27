import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Iterator
from .exceptions import HelloAgentsException

load_dotenv()

class HelloAgentsLLM:
    def __init__(
            self, 
            model:str=None, 
            apiKey:str=None, 
            baseUrl:str=None, 
            timeout:int=None, 
            provider:str ="auto", 
            temperature: float = 0.7,
            max_tokens:int | None = None, 
            **kwargs
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT") or 60)
        self.kwargs = kwargs

        self.provider = provider
        if self.provider == "auto":
            self.provider = self._auto_detect_provider(apiKey, baseUrl)
        print(f"🔍 检测到 provider: {self.provider}")

        self.apiKey, self.baseUrl = self._resolve_credentials(apiKey, baseUrl)

        if not all([self.model,self.apiKey,self.baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
        
        self.client = self._create_client()

    def think(self, messages:List[Dict[str, str]], temperature:float |None = None) -> Iterator[str]:
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            print("✅ 大语言模型响应成功:")
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                if content:
                    print(content, end="",flush=True)
            print()
        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            raise HelloAgentsException(f"LLM调用失败: {str(e)}")

        
    def _auto_detect_provider(self,apiKey:str | None, baseUrl:str | None) -> str:
        actual_apiKey = apiKey or os.getenv("LLM_API_KEY")
        actual_baseUrl = baseUrl or os.getenv("LLM_BASE_URL")

        if actual_baseUrl and "api.siliconflow.cn/v1" in actual_baseUrl.lower():
            return "silicon"
        elif os.getenv("SILICON_API_KEY") and not os.getenv("LLM_API_KEY"):
            return "silicon"
        else:
            return "auto"

    def _resolve_credentials(self, apiKey:str | None, baseUrl:str | None) -> tuple[str, str]:
        if self.provider == "silicon":
            resolve_apiKey = apiKey or os.getenv("SILICON_API_KEY") or os.getenv("LLM_API_KEY")
            resolve_baseUrl = baseUrl or os.getenv("SILICON_BASE_URL") or "https://api.siliconflow.cn/v1"
            self.model = self.model or os.getenv("SILICON_MODEL_ID")
            return resolve_apiKey, resolve_baseUrl
        else:
            resolve_apiKey = apiKey or os.getenv("LLM_API_KEY")
            resolve_baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
            self.model = self.model or os.getenv("LLM_MODEL_ID")
            return resolve_apiKey, resolve_baseUrl

    def _create_client(self) -> OpenAI:
        return OpenAI(self.apiKey,
                      self.baseUrl,
                      self.timeout
        )
    
    def invoke(self, messages:List[Dict[str, str]], **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                **{k: v for k, v in self.kwargs.items() if k not in ['temperature', 'max_tokens']}
            )
            return response.choices[0].message.content
        except Exception as e:
            raise HelloAgentsException(f"LLM调用失败: {str(e)}")
