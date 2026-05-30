"""
Core package for the Hello Agents framework.

This package contains the fundamental building blocks for the multi-agent system:
- Agent base class and implementations
- LLM interface and provider management
- Configuration management
- Message structures
"""

from .agent import Agent
from .llm import HelloAgentsLLM
from .message import Message
from .config import Config
from .exceptions import HelloAgentsException

__all__ = [
    "Agent",
    "HelloAgentsLLM",
    "Message",
    "Config",
    "HelloAgentsException"
]