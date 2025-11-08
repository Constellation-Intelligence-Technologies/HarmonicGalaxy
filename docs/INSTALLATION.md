# HarmonicGalaxy 安装指南

本文档介绍如何在其他项目中引入和使用 HarmonicGalaxy 框架。

## 安装方式

### 方式 1: 从 GitHub 安装（推荐用于开发）

如果项目还未发布到 PyPI，可以从 GitHub 直接安装：

```bash
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git
```

安装特定分支：

```bash
# 安装 dev 分支
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev

# 安装 master 分支
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@master
```

安装特定版本（当有 tag 时）：

```bash
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@v0.1.0
```

### 方式 2: 从 PyPI 安装（发布后）

当项目发布到 PyPI 后：

```bash
pip install harmonicgalaxy
```

安装特定版本：

```bash
pip install harmonicgalaxy==0.1.0
```

### 方式 3: 本地开发模式安装

如果你在本地开发 HarmonicGalaxy，可以使用开发模式安装：

```bash
# 克隆仓库
git clone https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git
cd HarmonicGalaxy

# 安装开发模式（代码变更会立即生效）
pip install -e .
```

### 方式 4: 使用 requirements.txt

在你的项目 `requirements.txt` 中添加：

```
# 从 GitHub 安装
harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev

# 或发布后从 PyPI 安装
harmonicgalaxy>=0.1.0
```

然后安装：

```bash
pip install -r requirements.txt
```

### 方式 5: 使用 pyproject.toml（现代 Python 项目）

在你的项目的 `pyproject.toml` 中添加：

```toml
[project]
dependencies = [
    "harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev",
]
```

或使用可选依赖：

```toml
[project.optional-dependencies]
harmonicgalaxy = [
    "harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev",
]
```

## 快速开始

### 1. 安装依赖

```bash
pip install harmonicgalaxy
```

### 2. 基本使用

#### 使用 LLM 客户端

```python
import asyncio
from harmonicgalaxy import create_client, LLMConfig, LLMMessage, LLMProvider

async def main():
    # 创建 OpenAI 客户端
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key="your-api-key",
    )
    
    client = create_client(config)
    
    # 发送消息
    messages = [
        LLMMessage(role="user", content="Hello!")
    ]
    
    response = await client.chat(messages)
    print(response.content)

asyncio.run(main())
```

#### 使用日志系统

```python
from harmonicgalaxy import get_logger, setup_logging
from harmonicgalaxy.utils.logging import LoggingConfig

# 配置日志（可选，有默认配置）
config = LoggingConfig(theme="galaxy", level="INFO")
setup_logging(config)

# 使用日志
logger = get_logger(__name__)
logger.info("⭐ 使用 HarmonicGalaxy 日志系统")
logger.mission_start("my_mission", target="test")
```

## 在你的项目中集成

### 示例：创建一个使用 HarmonicGalaxy 的简单应用

```python
# my_app.py
import asyncio
from harmonicgalaxy import (
    create_client,
    LLMConfig,
    LLMMessage,
    LLMProvider,
    get_logger,
    setup_logging,
)

# 配置日志
setup_logging()

logger = get_logger(__name__)

async def process_with_llm(text: str, provider: str = "openai"):
    """使用 LLM 处理文本"""
    logger.info(f"Processing text with {provider}")
    
    # 创建客户端
    config = LLMConfig(
        provider=LLMProvider(provider),
        model="gpt-4" if provider == "openai" else "claude-3-opus-20240229",
        api_key="your-api-key",
    )
    
    client = create_client(config)
    
    # 发送请求
    messages = [
        LLMMessage(role="user", content=text)
    ]
    
    response = await client.chat(messages)
    logger.info("Processing completed")
    
    return response.content

if __name__ == "__main__":
    result = asyncio.run(process_with_llm("What is Python?"))
    print(result)
```

### 示例：在 requirements.txt 中指定

```txt
# requirements.txt
harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev
```

### 示例：在 pyproject.toml 中指定

```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev",
]
```

## 依赖说明

HarmonicGalaxy 会自动安装以下依赖：

- `openai >= 1.0.0` - OpenAI API 支持
- `anthropic >= 0.18.0` - Anthropic API 支持
- `dashscope >= 1.17.0` - Qwen/DashScope API 支持

**注意**: 即使你只使用其中一个提供商，所有依赖都会被安装。如果希望减少依赖，可以考虑：

1. 只安装需要的提供商 SDK
2. 使用可选依赖（未来版本可能支持）

## 环境变量配置

### LLM API Keys

```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DASHSCOPE_API_KEY="your-dashscope-key"
```

### 日志配置

```bash
export HARMONICGALAXY_LOG_LEVEL=INFO
export HARMONICGALAXY_LOG_THEME=galaxy
export HARMONICGALAXY_LOG_DIR=./logs
```

## 验证安装

安装后可以验证：

```python
import harmonicgalaxy

print(f"HarmonicGalaxy version: {harmonicgalaxy.__version__}")

# 测试导入
from harmonicgalaxy import create_client, LLMProvider, get_logger
print("✓ All imports successful")
```

## 更新 HarmonicGalaxy

### 从 GitHub 更新

```bash
pip install --upgrade git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev
```

### 从 PyPI 更新

```bash
pip install --upgrade harmonicgalaxy
```

## 常见问题

### Q: 安装时提示找不到包？

确保：
1. 网络连接正常（GitHub 可访问）
2. 已安装 git
3. 使用正确的 URL 和分支名

### Q: 如何只安装特定功能？

目前所有功能都包含在一个包中。未来可能会支持可选依赖：

```bash
# 未来可能的用法
pip install harmonicgalaxy[llm]
pip install harmonicgalaxy[logging]
```

### Q: 在虚拟环境中安装

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev
```

### Q: 与现有项目冲突？

HarmonicGalaxy 使用独立的命名空间，不会与其他项目冲突。如果遇到依赖冲突：

1. 检查 Python 版本（需要 3.10+）
2. 使用虚拟环境隔离
3. 检查依赖版本兼容性

## 下一步

安装完成后，可以：

1. 查看 [LLM 客户端文档](LLM_CLIENT.md) 了解如何使用 LLM 功能
2. 查看 [日志系统文档](LOGGING.md) 了解日志配置
3. 查看 [开发指南](DEVELOPMENT.md) 了解如何贡献代码
4. 查看 `examples/` 目录中的示例代码

## 支持

如有问题，请：
- 查看 [GitHub Issues](https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy/issues)
- 阅读 [文档](https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy#readme)
