# HarmonicGalaxy 开发上下文

本文档记录 HarmonicGalaxy 项目的开发上下文、关键决策和技术细节，便于后续开发参考。

## 项目概述

**HarmonicGalaxy** 是 CINT（Constellation Intelligence & Technologies）体系下的第一个基石项目，定位是一套**分布式多智能体编排框架**。

### 核心理念

- **每个智能体都是一颗行星**：都有自己的能力和接口，都是一等公民
- **编排优先**：不是把模型"调用一下"这么简单，而是把多个智能体排成有业务语义的流程
- **天然有状态**：一次任务可以跨多轮、多阶段执行，状态在系统里被维护下来
- **可扩展的银河系**：后续新增的场景、Agent、工具，都能接入同一套框架，不需要推翻重来

## 项目结构

```
HarmonicGalaxy/
├── harmonicgalaxy/          # 主包
│   ├── __init__.py          # 导出主要接口
│   ├── llm/                 # LLM 客户端模块 ✅
│   │   ├── types.py         # 类型定义
│   │   ├── client.py        # 抽象基类和工厂
│   │   └── providers/       # 提供商实现
│   │       ├── openai_client.py
│   │       ├── anthropic_client.py
│   │       └── qwen_client.py
│   ├── utils/               # 工具模块 ✅
│   │   ├── logging.py       # 日志系统
│   │   └── decorators.py    # 装饰器
│   ├── core/                # 核心组件（待开发）
│   ├── agents/              # Agent 模块（待开发）
│   ├── orchestrator/        # 编排器（待开发）
│   ├── state/               # 状态管理（待开发）
│   └── events/              # 事件流（待开发）
├── tests/                   # 测试
├── examples/                # 示例代码
├── docs/                    # 文档
└── .github/                 # GitHub 配置
```

## 技术栈

- **Python**: 3.10+ (支持 3.10, 3.11, 3.12, 3.13)
- **构建系统**: hatchling (PEP 621)
- **依赖管理**: pyproject.toml
- **LLM SDKs**:
  - `openai >= 1.0.0` - OpenAI API
  - `anthropic >= 0.18.0` - Anthropic API
  - `dashscope >= 1.17.0` - Qwen/DashScope API
- **开发工具**:
  - `black >= 23.7.0` - 代码格式化
  - `ruff >= 0.1.0` - 代码检查
  - `mypy >= 1.5.0` - 类型检查
  - `isort >= 5.12.0` - 导入排序
  - `pre-commit >= 3.4.0` - Git hooks
  - `pytest >= 7.4.0` - 测试框架

## Git 分支策略

- **master**: 主分支，用于生产环境
- **dev**: 开发分支，用于集成新功能
- **feature/***: 功能分支，从 `dev` 创建
- **fix/***: 修复分支

## 已实现功能

### 1. LLM 客户端统一接口

**设计目标**: 提供统一的接口连接所有 LLM 提供商，简化多模型切换。

**实现方式**:
- 抽象基类 `LLMClient` 定义统一接口
- 工厂模式 `create_client()` 创建不同提供商的客户端
- 每个提供商实现独立的适配器类

**支持的提供商**:
- OpenAI (GPT-4, GPT-3.5-turbo 等)
- Anthropic (Claude 3 系列)
- Qwen (通义千问，通过 DashScope API)

**关键设计决策**:
- 使用异步接口（`async def chat()`）以支持高并发
- 支持流式响应（`async def stream_chat()`）
- 延迟导入避免循环依赖
- 统一的类型定义（`LLMMessage`, `LLMResponse`, `LLMConfig`）

**使用示例**:
```python
from harmonicgalaxy import create_client, LLMConfig, LLMMessage, LLMProvider

config = LLMConfig(
    provider=LLMProvider.OPENAI,
    model="gpt-4",
    api_key="your-key",
)
client = create_client(config)

messages = [LLMMessage(role="user", content="Hello")]
response = await client.chat(messages)
```

### 2. 日志系统

**设计目标**: 提供带有项目特色的日志系统，支持灵活配置。

**核心特性**:
- **星系主题**: 日志级别用天体表示（🌌 ⭐ ☄️ 💥 💫）
- **主题切换**: 支持 `galaxy`（默认）和 `standard` 两种主题
- **项目印记**: 所有日志都带有 `[HarmonicGalaxy]` 前缀
- **专用方法**: 提供 `mission_start()`, `agent_activated()` 等星系主题方法

**配置方式**:
- 代码配置：`LoggingConfig(theme="galaxy", level="INFO")`
- 环境变量：`HARMONICGALAXY_LOG_THEME=galaxy`

**关键设计决策**:
- 默认使用星系主题，体现项目特色
- 支持标准主题，满足不同场景需求
- 文件日志和控制台日志可独立配置
- 提供装饰器简化函数日志记录

**日志级别映射**:
- DEBUG → 🌌 星云（详细调试信息）
- INFO → ⭐ 恒星（正常操作信息）
- WARNING → ☄️ 彗星（警告信息）
- ERROR → 💥 流星（错误信息）
- CRITICAL → 💫 超新星（严重错误）

## 开发规范

### 代码风格

- **行长度**: 100 字符
- **格式化**: Black
- **检查**: Ruff（包含 pycodestyle, pyflakes, isort 等）
- **类型**: MyPy（渐进式类型检查）

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 测试要求

- 单元测试放在 `tests/unit/`
- 集成测试放在 `tests/integration/`
- 使用 pytest markers (`@pytest.mark.unit`, `@pytest.mark.integration`)
- 目标覆盖率：80%+

## 环境配置

### 开发环境设置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"

# 安装 pre-commit hooks
pre-commit install
```

### 环境变量

**日志配置**:
- `HARMONICGALAXY_LOG_LEVEL`: 日志级别（默认: INFO）
- `HARMONICGALAXY_LOG_THEME`: 主题（galaxy/standard，默认: galaxy）
- `HARMONICGALAXY_LOG_ENABLED`: 是否启用（默认: true）
- `HARMONICGALAXY_LOG_COLORS`: 是否使用颜色（默认: true）
- `HARMONICGALAXY_LOG_EMOJI`: 是否显示表情符号（默认: true）
- `HARMONICGALAXY_LOG_DIR`: 日志目录

**LLM API Keys**:
- `OPENAI_API_KEY`: OpenAI API 密钥
- `ANTHROPIC_API_KEY`: Anthropic API 密钥
- `DASHSCOPE_API_KEY`: DashScope/Qwen API 密钥

## 关键实现细节

### LLM 客户端

**循环依赖处理**:
- 在 `client.py` 中使用延迟导入（lazy import）
- 使用 `TYPE_CHECKING` 避免运行时导入

**异步处理**:
- Qwen/DashScope API 是同步的，使用 `asyncio.run_in_executor()` 包装为异步
- OpenAI 和 Anthropic 原生支持异步

**消息格式转换**:
- 统一的 `LLMMessage` 格式
- 各提供商适配器负责转换为各自的格式
- Anthropic 和 Qwen 需要特殊处理 system message

### 日志系统

**Formatter 选择**:
- `GalaxyFormatter`: 星系主题，带表情符号
- `StandardFormatter`: 标准主题，简洁格式
- 根据 `config.theme` 动态选择

**自定义 Logger**:
- `GalaxyLogger` 继承 `logging.Logger`
- 添加星系主题专用方法
- 通过 `logging.setLoggerClass()` 注册

**初始化时机**:
- 模块导入时自动调用 `setup_logging()`
- 使用环境变量默认配置
- 可在运行时重新配置

## 待开发功能

### 核心模块

1. **Mission（任务/使命）**
   - 多步骤、多智能体工作流的基本单元
   - 包含任务上下文、执行状态、历史记录

2. **Agent（智能体）**
   - 独立的能力节点
   - 能力描述、输入/输出接口、执行逻辑
   - Agent 注册表

3. **Orchestrator（编排器）**
   - 决定下一步执行哪个 Agent
   - 考虑能力匹配、当前状态、负载均衡

4. **State Manager（状态管理器）**
   - 维护任务的状态和上下文
   - 支持状态持久化、查询、恢复

5. **Event Stream（事件流）**
   - 提供可观测性
   - 记录 Agent 执行事件、状态变更事件

### 扩展计划

- 更多 LLM 提供商（Google, Cohere 等）
- 向量数据库集成
- 配置管理优化
- 性能监控和指标
- Web UI / 控制台

## 常见问题

### Q: 如何添加新的 LLM 提供商？

1. 在 `harmonicgalaxy/llm/types.py` 的 `LLMProvider` 枚举中添加新值
2. 在 `harmonicgalaxy/llm/providers/` 创建新的客户端实现
3. 实现 `LLMClient` 的 `chat()` 和 `stream_chat()` 方法
4. 在 `harmonicgalaxy/llm/client.py` 的 `create_client()` 中添加创建逻辑
5. 更新 `pyproject.toml` 添加依赖

### Q: 如何切换日志主题？

```python
from harmonicgalaxy import setup_logging
from harmonicgalaxy.utils.logging import LoggingConfig

# 切换到标准主题
config = LoggingConfig(theme="standard")
setup_logging(config)
```

或使用环境变量：
```bash
export HARMONICGALAXY_LOG_THEME=standard
```

### Q: 如何处理 LLM API 错误？

所有 LLM 客户端在 API 调用失败时会抛出异常，建议使用 try-except：

```python
try:
    response = await client.chat(messages)
except Exception as e:
    logger.error(f"LLM API error: {e}")
    # 处理错误
```

## 开发注意事项

1. **导入顺序**: 避免循环依赖，使用延迟导入
2. **异步函数**: 所有 LLM 相关操作都是异步的
3. **类型注解**: 推荐为新代码添加类型注解
4. **日志使用**: 使用 `get_logger(__name__)` 获取 logger
5. **测试**: 新功能必须包含测试

## 参考文档

- [开发指南](docs/DEVELOPMENT.md)
- [架构文档](docs/ARCHITECTURE.md)
- [日志系统文档](docs/LOGGING.md)
- [LLM 客户端文档](docs/LLM_CLIENT.md)
- [贡献指南](CONTRIBUTING.md)

## 更新记录

- **2025-01-08**: 项目初始化，实现 LLM 客户端和日志系统

