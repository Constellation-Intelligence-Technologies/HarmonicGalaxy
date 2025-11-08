# LLM Client 使用指南

HarmonicGalaxy 提供了一个统一的接口来连接和使用各种 LLM 提供商的模型，包括 OpenAI、Anthropic 等。

## 快速开始

### 安装依赖

```bash
pip install harmonicgalaxy
```

或者安装开发版本：

```bash
pip install -e ".[dev]"
```

### 基本使用

#### 1. 使用 OpenAI

```python
import asyncio
from harmonicgalaxy.llm import create_client, LLMConfig, LLMMessage, LLMProvider

async def main():
    # 创建配置
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key="your-api-key",
        temperature=0.7,
        max_tokens=1000,
    )
    
    # 创建客户端
    client = create_client(config)
    
    # 准备消息
    messages = [
        LLMMessage(role="system", content="You are a helpful assistant."),
        LLMMessage(role="user", content="What is Python?"),
    ]
    
    # 发送请求
    response = await client.chat(messages)
    print(response.content)

asyncio.run(main())
```

#### 2. 使用 Anthropic (Claude)

```python
import asyncio
from harmonicgalaxy.llm import create_client, LLMConfig, LLMMessage, LLMProvider

async def main():
    config = LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        model="claude-3-opus-20240229",
        api_key="your-api-key",
        temperature=0.7,
        max_tokens=1000,
    )
    
    client = create_client(config)
    
    messages = [
        LLMMessage(role="system", content="You are a helpful assistant."),
        LLMMessage(role="user", content="Explain quantum computing."),
    ]
    
    response = await client.chat(messages)
    print(response.content)

asyncio.run(main())
```

#### 3. 使用 Qwen (通义千问)

```python
import asyncio
from harmonicgalaxy.llm import create_client, LLMConfig, LLMMessage, LLMProvider

async def main():
    config = LLMConfig(
        provider=LLMProvider.QWEN,
        model="qwen-max",
        api_key="your-dashscope-api-key",  # DashScope API Key
        temperature=0.7,
        max_tokens=1000,
    )
    
    client = create_client(config)
    
    messages = [
        LLMMessage(role="system", content="你是一个有用的助手。"),
        LLMMessage(role="user", content="什么是人工智能？"),
    ]
    
    response = await client.chat(messages)
    print(response.content)

asyncio.run(main())
```

#### 4. 使用字典配置

```python
from harmonicgalaxy.llm.client import create_client_from_dict

config_dict = {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "api_key": "your-api-key",
    "temperature": 0.5,
}

client = create_client_from_dict(config_dict)
```

#### 5. 流式响应

```python
async def stream_example():
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key="your-api-key",
    )
    
    client = create_client(config)
    
    messages = [
        LLMMessage(role="user", content="Tell me a story."),
    ]
    
    async for chunk in client.stream_chat(messages):
        print(chunk, end="", flush=True)
```

## API 参考

### LLMConfig

配置类，用于设置 LLM 客户端的参数。

```python
LLMConfig(
    provider: LLMProvider,      # 提供商 (OPENAI, ANTHROPIC)
    model: str,                  # 模型名称
    api_key: Optional[str],      # API 密钥
    base_url: Optional[str],     # 自定义 API 基础 URL
    timeout: Optional[float],    # 超时时间（秒）
    max_retries: int = 3,       # 最大重试次数
    temperature: float = 1.0,   # 温度参数
    max_tokens: Optional[int],   # 最大 token 数
    top_p: Optional[float],     # Top-p 采样
    frequency_penalty: Optional[float],  # 频率惩罚
    presence_penalty: Optional[float],   # 存在惩罚
    stop: Optional[List[str]],   # 停止序列
    extra_params: Optional[Dict[str, Any]],  # 额外参数
)
```

### LLMMessage

消息类，表示对话中的一条消息。

```python
LLMMessage(
    role: Literal["system", "user", "assistant"],
    content: str,
    name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
)
```

### LLMResponse

响应类，包含 LLM 的回复信息。

```python
LLMResponse(
    content: str,                # 回复内容
    model: str,                  # 使用的模型
    provider: str,              # 提供商名称
    usage: Optional[Dict[str, Any]],  # Token 使用情况
    finish_reason: Optional[str],      # 完成原因
    metadata: Optional[Dict[str, Any]],  # 元数据
)
```

### LLMClient 方法

#### `chat(messages: List[LLMMessage], **kwargs) -> LLMResponse`

发送聊天完成请求。

**参数：**
- `messages`: 消息列表
- `**kwargs`: 额外的提供商特定参数

**返回：**
- `LLMResponse`: 包含回复的对象

#### `stream_chat(messages: List[LLMMessage], **kwargs) -> AsyncIterator[str]`

发送流式聊天完成请求。

**参数：**
- `messages`: 消息列表
- `**kwargs`: 额外的提供商特定参数

**返回：**
- `AsyncIterator[str]`: 异步迭代器，产生回复的文本块

## 支持的提供商

### OpenAI

- **Provider**: `LLMProvider.OPENAI`
- **模型示例**: `gpt-4`, `gpt-3.5-turbo`, `gpt-4-turbo-preview`
- **要求**: 需要安装 `openai` 包

### Anthropic

- **Provider**: `LLMProvider.ANTHROPIC`
- **模型示例**: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`
- **要求**: 需要安装 `anthropic` 包

### Qwen (通义千问)

- **Provider**: `LLMProvider.QWEN`
- **模型示例**: `qwen-turbo`, `qwen-plus`, `qwen-max`, `qwen-max-longcontext`
- **要求**: 需要安装 `dashscope` 包
- **API 密钥**: 需要在阿里云 DashScope 平台获取

## 环境变量

你可以通过环境变量设置 API 密钥：

```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

然后在代码中可以不指定 `api_key`，客户端会自动从环境变量读取。

## 错误处理

```python
try:
    response = await client.chat(messages)
except Exception as e:
    print(f"Error: {e}")
    # 处理错误
```

## 扩展支持新的提供商

要添加新的 LLM 提供商支持：

1. 在 `harmonicgalaxy/llm/types.py` 中添加新的 `LLMProvider` 枚举值
2. 在 `harmonicgalaxy/llm/providers/` 目录下创建新的客户端实现
3. 实现 `LLMClient` 抽象基类的 `chat` 和 `stream_chat` 方法
4. 在 `harmonicgalaxy/llm/client.py` 的 `create_client` 函数中添加新提供商的创建逻辑

## 示例

更多示例请查看 `examples/llm_client_example.py`。

