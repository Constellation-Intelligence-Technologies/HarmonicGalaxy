"""Example usage of LLM client.

This example demonstrates how to use the unified LLM client interface
to interact with different LLM providers.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
from harmonicgalaxy.llm import create_client, LLMConfig, LLMMessage, LLMProvider


async def main():
    """Example usage of LLM client."""

    # Example 1: Using OpenAI
    print("=== Example 1: OpenAI ===")
    openai_config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key="your-openai-api-key",  # Replace with your actual API key
        temperature=0.7,
        max_tokens=1000,
    )

    openai_client = create_client(openai_config)

    messages = [
        LLMMessage(role="system", content="You are a helpful assistant."),
        LLMMessage(role="user", content="What is the capital of France?"),
    ]

    try:
        response = await openai_client.chat(messages)
        print(f"Response: {response.content}")
        print(f"Model: {response.model}")
        print(f"Usage: {response.usage}")
    except Exception as e:
        print(f"Error: {e}")

    # Example 2: Using Anthropic
    print("\n=== Example 2: Anthropic ===")
    anthropic_config = LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        model="claude-3-opus-20240229",
        api_key="your-anthropic-api-key",  # Replace with your actual API key
        temperature=0.7,
        max_tokens=1000,
    )

    anthropic_client = create_client(anthropic_config)

    messages = [
        LLMMessage(role="system", content="You are a helpful assistant."),
        LLMMessage(role="user", content="Explain quantum computing in simple terms."),
    ]

    try:
        response = await anthropic_client.chat(messages)
        print(f"Response: {response.content}")
        print(f"Model: {response.model}")
        print(f"Usage: {response.usage}")
    except Exception as e:
        print(f"Error: {e}")

    # Example 3: Using Qwen
    print("\n=== Example 3: Qwen (通义千问) ===")
    qwen_config = LLMConfig(
        provider=LLMProvider.QWEN,
        model="qwen-max",
        api_key="your-dashscope-api-key",  # Replace with your actual DashScope API key
        temperature=0.7,
        max_tokens=1000,
    )

    qwen_client = create_client(qwen_config)

    messages = [
        LLMMessage(role="system", content="你是一个有用的助手。"),
        LLMMessage(role="user", content="用中文解释一下什么是机器学习。"),
    ]

    try:
        response = await qwen_client.chat(messages)
        print(f"Response: {response.content}")
        print(f"Model: {response.model}")
        print(f"Usage: {response.usage}")
    except Exception as e:
        print(f"Error: {e}")

    # Example 4: Streaming response
    print("\n=== Example 4: Streaming (OpenAI) ===")
    messages = [
        LLMMessage(role="user", content="Count from 1 to 5, one number per line."),
    ]

    try:
        print("Streaming response:")
        async for chunk in openai_client.stream_chat(messages):
            print(chunk, end="", flush=True)
        print()  # New line after streaming
    except Exception as e:
        print(f"Error: {e}")

    # Example 5: Using dictionary configuration
    print("\n=== Example 5: Dictionary Configuration ===")
    from harmonicgalaxy.llm.client import create_client_from_dict

    config_dict = {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": "your-openai-api-key",
        "temperature": 0.5,
    }

    client = create_client_from_dict(config_dict)
    print(f"Created client: {client}")


if __name__ == "__main__":
    asyncio.run(main())

