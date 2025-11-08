"""OpenAI client implementation."""

from typing import List, Optional, Dict, Any, AsyncIterator
from harmonicgalaxy.llm.client import LLMClient
from harmonicgalaxy.llm.types import LLMMessage, LLMResponse, LLMConfig, LLMProvider


class OpenAIClient(LLMClient):
    """OpenAI API client implementation."""

    def __init__(self, config: LLMConfig):
        """Initialize OpenAI client.

        Args:
            config: LLM configuration
        """
        super().__init__(config)
        if config.provider != LLMProvider.OPENAI:
            raise ValueError(f"Provider mismatch: expected OPENAI, got {config.provider}")

        # Lazy import to avoid requiring openai package if not used
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError(
                "openai package is required for OpenAIClient. "
                "Install it with: pip install openai"
            )

        self._client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
        )

    async def chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> LLMResponse:
        """Send a chat completion request to OpenAI.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            LLMResponse object containing the response
        """
        # Merge config parameters with kwargs
        params: Dict[str, Any] = {
            "model": self.config.model,
            "messages": [msg.to_dict() for msg in messages],
            "temperature": kwargs.get("temperature", self.config.temperature),
        }

        if self.config.max_tokens:
            params["max_tokens"] = kwargs.get("max_tokens", self.config.max_tokens)
        if self.config.top_p:
            params["top_p"] = kwargs.get("top_p", self.config.top_p)
        if self.config.frequency_penalty:
            params["frequency_penalty"] = kwargs.get(
                "frequency_penalty", self.config.frequency_penalty
            )
        if self.config.presence_penalty:
            params["presence_penalty"] = kwargs.get(
                "presence_penalty", self.config.presence_penalty
            )
        if self.config.stop:
            params["stop"] = kwargs.get("stop", self.config.stop)

        # Add extra params
        if self.config.extra_params:
            params.update(self.config.extra_params)

        # Override with kwargs
        params.update(kwargs)

        response = await self._client.chat.completions.create(**params)

        # Extract response data
        choice = response.choices[0]
        message = choice.message

        return LLMResponse(
            content=message.content or "",
            model=response.model,
            provider=LLMProvider.OPENAI.value,
            usage={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            }
            if response.usage
            else None,
            finish_reason=choice.finish_reason,
            metadata={"id": response.id, "created": response.created},
        )

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> AsyncIterator[str]:
        """Send a streaming chat completion request to OpenAI.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters

        Yields:
            Chunks of the response content as they arrive
        """
        # Merge config parameters with kwargs
        params: Dict[str, Any] = {
            "model": self.config.model,
            "messages": [msg.to_dict() for msg in messages],
            "stream": True,
            "temperature": kwargs.get("temperature", self.config.temperature),
        }

        if self.config.max_tokens:
            params["max_tokens"] = kwargs.get("max_tokens", self.config.max_tokens)
        if self.config.top_p:
            params["top_p"] = kwargs.get("top_p", self.config.top_p)
        if self.config.stop:
            params["stop"] = kwargs.get("stop", self.config.stop)

        # Add extra params
        if self.config.extra_params:
            params.update(self.config.extra_params)

        # Override with kwargs
        params.update(kwargs)

        stream = await self._client.chat.completions.create(**params)

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

