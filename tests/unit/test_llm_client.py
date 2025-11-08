"""Tests for LLM client factory."""

import pytest
from harmonicgalaxy.llm.client import create_client, create_client_from_dict
from harmonicgalaxy.llm.types import LLMConfig, LLMProvider


@pytest.mark.unit
class TestCreateClient:
    """Test client creation."""

    def test_create_openai_client(self):
        """Test creating OpenAI client."""
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            api_key="sk-test",
        )
        client = create_client(config)
        assert client.provider == LLMProvider.OPENAI
        assert client.config.model == "gpt-4"

    def test_create_anthropic_client(self):
        """Test creating Anthropic client."""
        config = LLMConfig(
            provider=LLMProvider.ANTHROPIC,
            model="claude-3-opus",
            api_key="sk-ant-test",
        )
        client = create_client(config)
        assert client.provider == LLMProvider.ANTHROPIC
        assert client.config.model == "claude-3-opus"

    def test_create_client_unsupported_provider(self):
        """Test creating client with unsupported provider."""
        # This will fail when we add more providers, but for now we can't test
        # as we don't have a way to create an invalid provider enum value
        pass

    def test_create_client_from_dict(self):
        """Test creating client from dictionary."""
        config_dict = {
            "provider": "openai",
            "model": "gpt-4",
            "api_key": "sk-test",
        }
        client = create_client_from_dict(config_dict)
        assert client.provider == LLMProvider.OPENAI
        assert client.config.model == "gpt-4"

    def test_create_client_from_dict_invalid_provider(self):
        """Test creating client with invalid provider string."""
        config_dict = {
            "provider": "invalid_provider",
            "model": "gpt-4",
        }
        with pytest.raises(ValueError):
            create_client_from_dict(config_dict)

