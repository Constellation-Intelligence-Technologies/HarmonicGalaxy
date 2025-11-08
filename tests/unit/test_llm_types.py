"""Tests for LLM types."""

import pytest
from harmonicgalaxy.llm.types import (
    LLMMessage,
    LLMResponse,
    LLMConfig,
    LLMProvider,
)


@pytest.mark.unit
class TestLLMMessage:
    """Test LLMMessage class."""

    def test_create_message(self):
        """Test creating a message."""
        msg = LLMMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.name is None
        assert msg.metadata is None

    def test_message_to_dict(self):
        """Test converting message to dictionary."""
        msg = LLMMessage(role="assistant", content="Hi", name="bot")
        data = msg.to_dict()
        assert data["role"] == "assistant"
        assert data["content"] == "Hi"
        assert data["name"] == "bot"

    def test_message_from_dict(self):
        """Test creating message from dictionary."""
        data = {"role": "user", "content": "Hello"}
        msg = LLMMessage.from_dict(data)
        assert msg.role == "user"
        assert msg.content == "Hello"


@pytest.mark.unit
class TestLLMResponse:
    """Test LLMResponse class."""

    def test_create_response(self):
        """Test creating a response."""
        response = LLMResponse(
            content="Hello",
            model="gpt-4",
            provider="openai",
        )
        assert response.content == "Hello"
        assert response.model == "gpt-4"
        assert response.provider == "openai"

    def test_response_to_dict(self):
        """Test converting response to dictionary."""
        response = LLMResponse(
            content="Hello",
            model="gpt-4",
            provider="openai",
            usage={"total_tokens": 100},
        )
        data = response.to_dict()
        assert data["content"] == "Hello"
        assert data["model"] == "gpt-4"
        assert data["usage"]["total_tokens"] == 100


@pytest.mark.unit
class TestLLMConfig:
    """Test LLMConfig class."""

    def test_create_config(self):
        """Test creating a config."""
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            api_key="sk-test",
        )
        assert config.provider == LLMProvider.OPENAI
        assert config.model == "gpt-4"
        assert config.api_key == "sk-test"
        assert config.temperature == 1.0
        assert config.max_retries == 3

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = LLMConfig(
            provider=LLMProvider.ANTHROPIC,
            model="claude-3-opus",
            api_key="sk-ant-test",
            temperature=0.7,
        )
        data = config.to_dict()
        assert data["provider"] == "anthropic"
        assert data["model"] == "claude-3-opus"
        assert data["temperature"] == 0.7


@pytest.mark.unit
class TestLLMProvider:
    """Test LLMProvider enum."""

    def test_provider_values(self):
        """Test provider enum values."""
        assert LLMProvider.OPENAI.value == "openai"
        assert LLMProvider.ANTHROPIC.value == "anthropic"

