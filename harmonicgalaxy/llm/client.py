"""Base LLM client interface and factory."""

from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from harmonicgalaxy.llm.types import LLMMessage, LLMResponse, LLMConfig, LLMProvider

from harmonicgalaxy.llm.types import LLMMessage, LLMResponse, LLMConfig, LLMProvider
from harmonicgalaxy.utils.logging import get_logger

logger = get_logger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, config: LLMConfig):
        """Initialize LLM client with configuration.

        Args:
            config: LLM configuration
        """
        self.config = config
        self.provider = config.provider
        logger.debug(f"Initializing {self.__class__.__name__} with model={config.model}")

    @abstractmethod
    async def chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> LLMResponse:
        """Send a chat completion request.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters specific to the provider

        Returns:
            LLMResponse object containing the response

        Raises:
            Exception: If the request fails
        """
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ):
        """Send a streaming chat completion request.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters specific to the provider

        Yields:
            Chunks of the response as they arrive
        """
        pass

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(provider={self.provider.value}, model={self.config.model})"


def create_client(config: LLMConfig) -> "LLMClient":
    """Create an LLM client for the specified provider.

    Args:
        config: LLM configuration

    Returns:
        LLMClient instance for the specified provider

    Raises:
        ValueError: If the provider is not supported
    """
    # Lazy import to avoid circular dependencies
    from harmonicgalaxy.llm.providers.openai_client import OpenAIClient
    from harmonicgalaxy.llm.providers.anthropic_client import AnthropicClient
    from harmonicgalaxy.llm.providers.qwen_client import QwenClient

    provider = config.provider
    logger.info(f"Creating LLM client: provider={provider.value}, model={config.model}")

    if provider == LLMProvider.OPENAI:
        client = OpenAIClient(config)
    elif provider == LLMProvider.ANTHROPIC:
        client = AnthropicClient(config)
    elif provider == LLMProvider.QWEN:
        client = QwenClient(config)
    else:
        logger.error(f"Unsupported provider: {provider}")
        raise ValueError(f"Unsupported provider: {provider}")

    logger.debug(f"LLM client created successfully: {client}")
    return client


def create_client_from_dict(config_dict: dict) -> "LLMClient":
    """Create an LLM client from a dictionary configuration.

    Args:
        config_dict: Dictionary containing configuration

    Returns:
        LLMClient instance

    Example:
        >>> config = {
        ...     "provider": "openai",
        ...     "model": "gpt-4",
        ...     "api_key": "sk-...",
        ... }
        >>> client = create_client_from_dict(config)
    """
    provider_str = config_dict.get("provider")
    if isinstance(provider_str, str):
        provider = LLMProvider(provider_str)
    elif isinstance(provider_str, LLMProvider):
        provider = provider_str
    else:
        raise ValueError(f"Invalid provider type: {type(provider_str)}")

    config = LLMConfig(
        provider=provider,
        model=config_dict["model"],
        api_key=config_dict.get("api_key"),
        base_url=config_dict.get("base_url"),
        timeout=config_dict.get("timeout"),
        max_retries=config_dict.get("max_retries", 3),
        temperature=config_dict.get("temperature", 1.0),
        max_tokens=config_dict.get("max_tokens"),
        top_p=config_dict.get("top_p"),
        frequency_penalty=config_dict.get("frequency_penalty"),
        presence_penalty=config_dict.get("presence_penalty"),
        stop=config_dict.get("stop"),
        extra_params=config_dict.get("extra_params"),
    )

    return create_client(config)

