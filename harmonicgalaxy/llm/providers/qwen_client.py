"""Qwen (通义千问) client implementation via DashScope API."""

from typing import List, Optional, Dict, Any, AsyncIterator
from harmonicgalaxy.llm.client import LLMClient
from harmonicgalaxy.llm.types import LLMMessage, LLMResponse, LLMConfig, LLMProvider


class QwenClient(LLMClient):
    """Qwen API client implementation via DashScope."""

    def __init__(self, config: LLMConfig):
        """Initialize Qwen client.

        Args:
            config: LLM configuration
        """
        super().__init__(config)
        if config.provider != LLMProvider.QWEN:
            raise ValueError(f"Provider mismatch: expected QWEN, got {config.provider}")

        # Lazy import to avoid requiring dashscope package if not used
        try:
            import dashscope
        except ImportError:
            raise ImportError(
                "dashscope package is required for QwenClient. "
                "Install it with: pip install dashscope"
            )

        # Set API key if provided
        if config.api_key:
            dashscope.api_key = config.api_key

        self._dashscope = dashscope
        self._base_url = config.base_url

    def _convert_messages(self, messages: List[LLMMessage]) -> List[Dict[str, Any]]:
        """Convert LLMMessage format to DashScope format.

        Args:
            messages: List of LLMMessage objects

        Returns:
            List of messages in DashScope format
        """
        dashscope_messages = []
        system_message = None

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                # DashScope uses "user" and "assistant" roles
                dashscope_messages.append(
                    {
                        "role": msg.role if msg.role != "assistant" else "assistant",
                        "content": msg.content,
                    }
                )

        return dashscope_messages, system_message

    async def chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> LLMResponse:
        """Send a chat completion request to Qwen.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            LLMResponse object containing the response
        """
        dashscope_messages, system_message = self._convert_messages(messages)

        # Merge config parameters with kwargs
        params: Dict[str, Any] = {
            "model": self.config.model,
            "messages": dashscope_messages,
            "temperature": kwargs.get("temperature", self.config.temperature),
        }

        if system_message:
            params["system"] = system_message

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

        # Use DashScope API
        # Note: DashScope Generation.call is synchronous, but we wrap it in async
        import asyncio
        from dashscope import Generation

        # Run synchronous call in executor to make it async-friendly
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, Generation.call, **params)

        if response.status_code != 200:
            raise RuntimeError(
                f"Qwen API error: {response.status_code} - {response.message}"
            )

        # Extract response data
        output = response.output
        if not output or not output.choices:
            raise RuntimeError("No response from Qwen API")

        choice = output.choices[0]
        content = choice.message.content if choice.message else ""

        return LLMResponse(
            content=content,
            model=output.model or self.config.model,
            provider=LLMProvider.QWEN.value,
            usage={
                "input_tokens": output.usage.input_tokens if output.usage else 0,
                "output_tokens": output.usage.output_tokens if output.usage else 0,
                "total_tokens": (
                    output.usage.input_tokens + output.usage.output_tokens
                    if output.usage
                    else None
                ),
            }
            if output.usage
            else None,
            finish_reason=getattr(choice, "finish_reason", None),
            metadata={
                "request_id": response.request_id,
                "status_code": response.status_code,
            },
        )

    async def stream_chat(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> AsyncIterator[str]:
        """Send a streaming chat completion request to Qwen.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters

        Yields:
            Chunks of the response content as they arrive
        """
        dashscope_messages, system_message = self._convert_messages(messages)

        # Merge config parameters with kwargs
        params: Dict[str, Any] = {
            "model": self.config.model,
            "messages": dashscope_messages,
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
            params["stop"] = kwargs.get("stop", self.config.stop)

        # Add extra params
        if self.config.extra_params:
            params.update(self.config.extra_params)

        # Override with kwargs
        params.update(kwargs)

        # Use DashScope API with streaming
        import asyncio
        from dashscope import Generation

        # DashScope streaming: Generation.call returns an iterator when stream=True
        # We need to run it in executor since it's synchronous
        loop = asyncio.get_event_loop()

        def _get_stream():
            """Get the stream iterator."""
            response_stream = Generation.call(**params)
            return response_stream

        # Get the stream iterator in executor
        response_stream = await loop.run_in_executor(None, _get_stream)

        # Process chunks asynchronously
        def _process_chunk(chunk):
            """Process a single chunk."""
            if hasattr(chunk, "output") and chunk.output:
                if chunk.output.choices:
                    choice = chunk.output.choices[0]
                    if choice.message and hasattr(choice.message, "content"):
                        return choice.message.content
            return None

        # Iterate through stream chunks
        while True:
            try:
                # Get next chunk in executor
                chunk = await loop.run_in_executor(
                    None, lambda: next(response_stream, None)
                )
                if chunk is None:
                    break

                content = _process_chunk(chunk)
                if content:
                    yield content

                # Check if stream is done
                if hasattr(chunk, "output") and chunk.output:
                    if hasattr(chunk.output, "finish_reason"):
                        if chunk.output.finish_reason:
                            break
            except StopIteration:
                break
            except Exception as e:
                # Handle errors
                if hasattr(e, "status_code") and e.status_code != 200:
                    raise RuntimeError(f"Qwen API error: {e.status_code} - {e.message}")
                raise

