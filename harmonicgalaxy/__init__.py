"""
HarmonicGalaxy - A distributed, multi-agent orchestration framework.

HarmonicGalaxy is designed to make many intelligent components work together
in harmony — just like planets in a well-arranged galaxy.
"""

__version__ = "0.1.0"
__author__ = "Constellation Intelligence & Technologies"

# Export LLM client functionality
from harmonicgalaxy.llm import (
    LLMClient,
    create_client,
    LLMMessage,
    LLMResponse,
    LLMConfig,
    LLMProvider,
)

# Export logging utilities
from harmonicgalaxy.utils.logging import get_logger, setup_logging, LogLevel

__all__ = [
    "__version__",
    "__author__",
    "LLMClient",
    "create_client",
    "LLMMessage",
    "LLMResponse",
    "LLMConfig",
    "LLMProvider",
    "get_logger",
    "setup_logging",
    "LogLevel",
]
