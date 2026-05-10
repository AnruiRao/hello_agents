import os
from pydantic import BaseModel
from typing import Dict, Any

class Config(BaseModel):

    default_model: str = "qwen3.5-plus-2026-02-15"
    default_provider: str = "qwen"
    temperature: float = 0.7
    max_tokens: int | None = None


    debug: bool = False
    log_level: str = "INFO"

    max_history_length: int = 100

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            debug=os.getenv("DEBUG","false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            temperature=float(os.getenv("TEMPERATURE", 0.7)),
            max_tokens=int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()