# HarmonicGalaxy 安装和使用指南

本文档说明如何在其他项目中引入和使用 HarmonicGalaxy 框架。

## 安装方式

### 方式 1: 从 GitHub 安装（推荐用于开发）

如果项目还未发布到 PyPI，可以从 GitHub 直接安装：

```bash
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev
```

或者安装特定分支/标签：

```bash
# 安装 dev 分支
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev

# 安装 master 分支
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@master

# 安装特定版本（发布后）
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@v0.1.0
```

### 方式 2: 从本地路径安装（开发阶段）

如果你在本地开发 HarmonicGalaxy，可以在其他项目中直接安装本地版本：

```bash
# 安装本地开发版本（可编辑模式）
pip install -e /path/to/HarmonicGalaxy

# 或者使用相对路径
pip install -e ../HarmonicGalaxy
```

### 方式 3: 添加到 requirements.txt

在你的项目 `requirements.txt` 中添加：

```txt
# 从 GitHub 安装
harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev

# 或者安装本地版本
# harmonicgalaxy @ file:///path/to/HarmonicGalaxy
```

然后安装：

```bash
pip install -r requirements.txt
```

### 方式 4: 添加到 pyproject.toml（推荐）

如果你的项目使用 `pyproject.toml`：

```toml
[project]
dependencies = [
    "harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev",
]
```

或者使用可选依赖：

```toml
[project.optional-dependencies]
harmonicgalaxy = [
    "harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev",
]
```

### 方式 5: 从 PyPI 安装（发布后）

当 HarmonicGalaxy 发布到 PyPI 后：

```bash
pip install harmonicgalaxy
```

## 基本使用

### 1. 使用 LLM 客户端

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

### 2. 使用日志系统

```python
from harmonicgalaxy import get_logger, setup_logging
from harmonicgalaxy.utils.logging import LoggingConfig

# 配置日志（可选，有默认配置）
config = LoggingConfig(theme="galaxy", level="INFO")
setup_logging(config)

# 获取 logger
logger = get_logger(__name__)

# 使用日志
logger.info("⭐ 项目启动")
logger.mission_start("process_data", dataset="large.csv")
```

### 3. 完整示例

```python
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

async def process_with_llm():
    logger.mission_start("data_analysis")
    
    # 创建 LLM 客户端
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key="your-api-key",
    )
    client = create_client(config)
    
    # 处理数据
    messages = [
        LLMMessage(role="system", content="You are a data analyst."),
        LLMMessage(role="user", content="Analyze this data: ..."),
    ]
    
    response = await client.chat(messages)
    logger.info(f"分析结果: {response.content}")
    
    logger.mission_complete("data_analysis")

asyncio.run(process_with_llm())
```

## 配置环境变量

可以通过环境变量配置，避免在代码中硬编码：

```bash
# LLM API Keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export DASHSCOPE_API_KEY="your-dashscope-key"

# 日志配置
export HARMONICGALAXY_LOG_LEVEL=INFO
export HARMONICGALAXY_LOG_THEME=galaxy
```

然后在代码中可以不指定 `api_key`（如果 SDK 支持从环境变量读取）。

## 依赖说明

安装 HarmonicGalaxy 会自动安装以下依赖：

- `openai >= 1.0.0` - OpenAI SDK
- `anthropic >= 0.18.0` - Anthropic SDK
- `dashscope >= 1.17.0` - DashScope/Qwen SDK

## 版本兼容性

- **Python**: 3.10, 3.11, 3.12, 3.13
- **操作系统**: Linux, macOS, Windows

## 常见问题

### Q: 如何只使用特定功能？

HarmonicGalaxy 的模块是独立的，你可以只导入需要的部分：

```python
# 只使用 LLM 客户端
from harmonicgalaxy.llm import create_client, LLMConfig, LLMProvider

# 只使用日志系统
from harmonicgalaxy.utils.logging import get_logger, setup_logging
```

### Q: 如何避免安装不需要的 LLM SDK？

目前所有 LLM SDK 都是核心依赖。如果未来版本支持可选依赖，可以这样安装：

```bash
# 只安装基础功能（未来版本）
pip install harmonicgalaxy[core]

# 安装特定提供商（未来版本）
pip install harmonicgalaxy[openai]
pip install harmonicgalaxy[anthropic]
pip install harmonicgalaxy[qwen]
```

### Q: 如何在 Docker 中使用？

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装 HarmonicGalaxy
RUN pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev

# 复制你的代码
COPY . .

# 运行
CMD ["python", "app.py"]
```

### Q: 如何更新到最新版本？

```bash
# 从 GitHub 更新
pip install --upgrade git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev

# 从 PyPI 更新（发布后）
pip install --upgrade harmonicgalaxy
```

## 开发模式安装

如果你想修改 HarmonicGalaxy 的源码：

```bash
# 克隆仓库
git clone https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git
cd HarmonicGalaxy

# 安装开发依赖
pip install -e ".[dev]"

# 在你的项目中安装本地版本
cd /path/to/your/project
pip install -e /path/to/HarmonicGalaxy
```

这样修改 HarmonicGalaxy 源码后，你的项目会自动使用最新版本。

## 下一步

- 查看 [LLM 客户端文档](LLM_CLIENT.md) 了解详细用法
- 查看 [日志系统文档](LOGGING.md) 了解日志配置
- 查看 [开发指南](DEVELOPMENT.md) 了解如何贡献代码

