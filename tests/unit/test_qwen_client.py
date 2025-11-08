"""Tests for Qwen client."""

import pytest
from harmonicgalaxy.llm.client import create_client
from harmonicgalaxy.llm.types import LLMConfig, LLMProvider


@pytest.mark.unit
class TestQwenClient:
    """Test Qwen client creation."""

    def test_create_qwen_client(self):
        """Test creating Qwen client."""
        config = LLMConfig(
            provider=LLMProvider.QWEN,
            model="qwen-max",
            api_key="sk-test",
        )
        client = create_client(config)
        assert client.provider == LLMProvider.QWEN
        assert client.config.model == "qwen-max"

    def test_create_qwen_client_from_dict(self):
        """Test creating Qwen client from dictionary."""
        from harmonicgalaxy.llm.client import create_client_from_dict

        config_dict = {
            "provider": "qwen",
            "model": "qwen-turbo",
            "api_key": "sk-test",
        }
        client = create_client_from_dict(config_dict)
        assert client.provider == LLMProvider.QWEN
        assert client.config.model == "qwen-turbo"

