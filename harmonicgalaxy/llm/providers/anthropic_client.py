"""Anthropic (Claude) client implementation."""

from typing import List, Optional, Dict, Any, AsyncIterator
from harmonicgalaxy.llm.client import LLMClient
from harmonicgalaxy.llm.types import LLMMessage, LLMResponse, LLMConfig, LLMProvider


class AnthropicClient(LLMClient):
    """Anthropic API client implementation."""

    def __init__(self, config: LLMConfig):
        """Initialize Anthropic client.

        Args:
            config: LLM configuration
        """
        super().__init__(config)
        if config.provider != LLMProvider.ANTHROPIC:
            raise ValueError(f"Provider mismatch: expected ANTHROPIC, got {config.provider}")

        # Lazy import to avoid requiring anthropic package if not used
        try:
            from anthropic import AsyncAnthropic
        except ImportError:
            raise ImportError(
                "anthropic package is required for AnthropicClient. "
                "Install it with: pip install anthropic"
            )

        self._client = AsyncAnthropic(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
        )

    def _convert_messages(self, messages: List[LLMMessage]) -> List[Dict[str, Any]]:
        """Convert LLMMessage format to Anthropic format.

        Args:
            messages: List of LLMMessage objects

        Returns:
            List of messages in Anthropic format
        """
        anthropic_messages = []
        system_message = None

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                # Anthropic uses "user" and "assistant" roles
                anthropic_messages.append(
                    {
                        "role": msg.role if msg.role != "assistant" else "assistant",
                        "content": msg.content,
                    }
                )

        return anthropic_messages, system_message

    async def chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> LLMResponse:
        """Send a chat completion request to Anthropic.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            LLMResponse object containing the response
        """
        anthropic_messages, system_message = self._convert_messages(messages)

        # Merge config parameters with kwargs
        params: Dict[str, Any] = {
            "model": self.config.model,
            "messages": anthropic_messages,
            "temperature": kwargs.get("temperature", self.config.temperature),
        }

        if system_message:
            params["system"] = system_message

        if self.config.max_tokens:
            params["max_tokens"] = kwargs.get("max_tokens", self.config.max_tokens)
        if self.config.top_p:
            params["top_p"] = kwargs.get("top_p", self.config.top_p)
        if self.config.stop:
            params["stop_sequences"] = kwargs.get("stop", self.config.stop)

        # Add extra params
        if self.config.extra_params:
            params.update(self.config.extra_params)

        # Override with kwargs
        params.update(kwargs)

        response = await self._client.messages.create(**params)

        # Extract response data
        content_text = ""
        for content_block in response.content:
            if content_block.type == "text":
                content_text += content_block.text

        return LLMResponse(
            content=content_text,
            model=response.model,
            provider=LLMProvider.ANTHROPIC.value,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
            if response.usage
            else None,
            finish_reason=response.stop_reason,
            metadata={"id": response.id},
        )

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> AsyncIterator[str]:
        """Send a streaming chat completion request to Anthropic.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters

        Yields:
            Chunks of the response content as they arrive
        """
        anthropic_messages, system_message = self._convert_messages(messages)

        # Merge config parameters with kwargs
        params: Dict[str, Any] = {
            "model": self.config.model,
            "messages": anthropic_messages,
            "stream": True,
            "temperature": kwargs.get("temperature", self.config.temperature),
        }

        if system_message:
            params["system"] = system_message

        if self.config.max_tokens:
            params["max_tokens"] = kwargs.get("max_tokens", self.config.max_tokens)
        if self.config.top_p:
            params["top_p"] = kwargs.get("top_p", self.config.top_p)
        if self.config.stop:
            params["stop_sequences"] = kwargs.get("stop", self.config.stop)

        # Add extra params
        if self.config.extra_params:
            params.update(self.config.extra_params)

        # Override with kwargs
        params.update(kwargs)

        async with self._client.messages.stream(**params) as stream:
            async for event in stream:
                if event.type == "content_block_delta":
                    if event.delta.type == "text":
                        yield event.delta.text

