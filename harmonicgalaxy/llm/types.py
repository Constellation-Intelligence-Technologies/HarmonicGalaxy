"""Type definitions for LLM client."""

from typing import Optional, List, Dict, Any, Literal
from dataclasses import dataclass
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    QWEN = "qwen"
    # Add more providers as needed
    # GOOGLE = "google"
    # COHERE = "cohere"


@dataclass
class LLMMessage:
    """Represents a message in a conversation."""

    role: Literal["system", "user", "assistant"]
    content: str
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format."""
        result: Dict[str, Any] = {
            "role": self.role,
            "content": self.content,
        }
        if self.name:
            result["name"] = self.name
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMMessage":
        """Create message from dictionary."""
        return cls(
            role=data["role"],
            content=data["content"],
            name=data.get("name"),
            metadata=data.get("metadata"),
        )


@dataclass
class LLMResponse:
    """Represents a response from an LLM."""

    content: str
    model: str
    provider: str
    usage: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary format."""
        result: Dict[str, Any] = {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
        }
        if self.usage:
            result["usage"] = self.usage
        if self.finish_reason:
            result["finish_reason"] = self.finish_reason
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class LLMConfig:
    """Configuration for LLM client."""

    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: Optional[float] = None
    max_retries: int = 3
    temperature: float = 1.0
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[List[str]] = None
    extra_params: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary format."""
        result: Dict[str, Any] = {
            "provider": self.provider.value,
            "model": self.model,
        }
        if self.api_key:
            result["api_key"] = self.api_key
        if self.base_url:
            result["base_url"] = self.base_url
        if self.timeout:
            result["timeout"] = self.timeout
        result["max_retries"] = self.max_retries
        result["temperature"] = self.temperature
        if self.max_tokens:
            result["max_tokens"] = self.max_tokens
        if self.top_p:
            result["top_p"] = self.top_p
        if self.frequency_penalty:
            result["frequency_penalty"] = self.frequency_penalty
        if self.presence_penalty:
            result["presence_penalty"] = self.presence_penalty
        if self.stop:
            result["stop"] = self.stop
        if self.extra_params:
            result["extra_params"] = self.extra_params
        return result

