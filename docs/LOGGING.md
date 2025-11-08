# HarmonicGalaxy 日志系统

HarmonicGalaxy 提供了一个带有"星系"主题的统一日志系统，日志级别用天体表示，具有明确的项目印记。

## 快速开始

### 基本使用

```python
from harmonicgalaxy import get_logger

logger = get_logger(__name__)

logger.debug("🌌 调试信息（星云）")
logger.info("⭐ 正常信息（恒星）")
logger.warning("☄️ 警告信息（彗星）")
logger.error("💥 错误信息（流星）")
logger.critical("💫 严重错误（超新星）")
```

### 输出示例

```
2025-01-08 10:30:45 [HarmonicGalaxy] 🌌 DEBUG [module_name] 调试信息（星云）
2025-01-08 10:30:45 [HarmonicGalaxy] ⭐ INFO [module_name] 正常信息（恒星）
2025-01-08 10:30:45 [HarmonicGalaxy] ☄️ WARNING [module_name] 警告信息（彗星）
2025-01-08 10:30:45 [HarmonicGalaxy] 💥 ERROR [module_name] 错误信息（流星）
2025-01-08 10:30:45 [HarmonicGalaxy] 💫 CRITICAL [module_name] 严重错误（超新星）
```

## 日志级别（天体主题）

| 级别 | 天体 | 含义 | 使用场景 |
|------|------|------|----------|
| DEBUG | 🌌 星云 | 详细的调试信息 | 开发调试、详细追踪 |
| INFO | ⭐ 恒星 | 正常的操作信息 | 一般信息、状态更新 |
| WARNING | ☄️ 彗星 | 警告但不影响运行 | 异常但可恢复的情况 |
| ERROR | 💥 流星 | 错误发生 | 功能失败、异常情况 |
| CRITICAL | 💫 超新星 | 严重错误 | 系统崩溃、致命错误 |

## 星系主题方法

HarmonicGalaxy 提供了专门的方法来记录多智能体系统的操作：

### 任务（Mission）日志

```python
logger.mission_start("explore_galaxy", target="Andromeda", distance="2.5M light-years")
logger.mission_complete("explore_galaxy", duration="5.2s", discoveries=3)
```

### 智能体（Agent）日志

```python
logger.agent_activated("data_processor", capability="text_analysis")
logger.agent_deactivated("data_processor")
```

### 编排（Orchestration）日志

```python
logger.orchestration_step(1, "Selecting next agent")
logger.orchestration_step(2, "Executing agent task")
```

### 状态（State）日志

```python
logger.state_update("mission_status", "pending", "in_progress")
logger.state_update("agent_count", 0, 5)
```

### 事件（Event）日志

```python
logger.event_emitted("agent_ready", {"agent_id": "agent_001", "status": "ready"})
```

## 主题模式

HarmonicGalaxy 支持两种日志主题：

### 1. 星系主题（Galaxy Theme）- 默认

带有表情符号和星系主题的日志格式：

```
2025-01-08 10:30:45 [HarmonicGalaxy] ⭐ INFO [module_name] 正常信息
2025-01-08 10:30:45 [HarmonicGalaxy] ☄️ WARNING [module_name] 警告信息
```

### 2. 标准主题（Standard Theme）

简洁的标准日志格式：

```
2025-01-08 10:30:45 [HarmonicGalaxy] INFO     [module_name] 正常信息
2025-01-08 10:30:45 [HarmonicGalaxy] WARNING  [module_name] 警告信息
```

## 配置

### 方式 1: 代码配置

```python
from harmonicgalaxy import setup_logging
from harmonicgalaxy.utils.logging import LoggingConfig

# 星系主题（默认）
config_galaxy = LoggingConfig(
    theme="galaxy",             # 或 "standard"
    level="DEBUG",              # 日志级别
    enabled=True,               # 是否启用日志
    use_colors=True,            # 是否使用颜色（终端）
    show_emoji=True,            # 是否显示表情符号（仅星系主题）
    show_constellation=True,    # 是否显示 [HarmonicGalaxy] 前缀
    log_file="./logs/app.log",  # 日志文件路径（可选）
    log_dir="./logs",           # 日志目录（可选）
    file_level="DEBUG",         # 文件日志级别（可选）
)

# 标准主题
config_standard = LoggingConfig(
    theme="standard",
    level="INFO",
    use_colors=True,
    show_constellation=True,
)

setup_logging(config_galaxy)  # 或 config_standard
```

### 方式 2: 环境变量配置

```bash
export HARMONICGALAXY_LOG_LEVEL=DEBUG
export HARMONICGALAXY_LOG_ENABLED=true
export HARMONICGALAXY_LOG_COLORS=true
export HARMONICGALAXY_LOG_EMOJI=true
export HARMONICGALAXY_LOG_FILE=./logs/app.log
export HARMONICGALAXY_LOG_DIR=./logs
```

然后在代码中：

```python
from harmonicgalaxy.utils.logging import LoggingConfig, setup_logging

config = LoggingConfig.from_env()
setup_logging(config)
```

### 环境变量说明

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `HARMONICGALAXY_LOG_LEVEL` | `INFO` | 日志级别 |
| `HARMONICGALAXY_LOG_ENABLED` | `true` | 是否启用日志 |
| `HARMONICGALAXY_LOG_THEME` | `galaxy` | 日志主题：`galaxy` 或 `standard` |
| `HARMONICGALAXY_LOG_COLORS` | `true` | 是否使用颜色 |
| `HARMONICGALAXY_LOG_EMOJI` | `true` | 是否显示表情符号（仅星系主题） |
| `HARMONICGALAXY_LOG_FILE` | - | 日志文件路径 |
| `HARMONICGALAXY_LOG_DIR` | - | 日志目录 |

### 主题切换示例

```bash
# 使用星系主题（默认）
export HARMONICGALAXY_LOG_THEME=galaxy

# 使用标准主题
export HARMONICGALAXY_LOG_THEME=standard
```

## 装饰器

### 函数调用日志

```python
from harmonicgalaxy.utils.decorators import log_function_call

@log_function_call()
def my_function(x, y):
    return x + y

result = my_function(5, 3)  # 自动记录函数调用和结果
```

### 异步函数调用日志

```python
from harmonicgalaxy.utils.decorators import log_async_function_call

@log_async_function_call()
async def my_async_function(name):
    await asyncio.sleep(1)
    return f"Hello {name}"

result = await my_async_function("World")  # 自动记录异步函数调用
```

## 日志格式

### 控制台输出格式

```
{timestamp} [HarmonicGalaxy] {emoji} {level} [{module}] {message}
```

示例：
```
2025-01-08 10:30:45 [HarmonicGalaxy] ⭐ INFO [harmonicgalaxy.llm.client] Creating LLM client
```

### 文件输出格式

文件日志格式与控制台相同，但不使用颜色。

## 最佳实践

### 1. 在模块中使用

```python
from harmonicgalaxy import get_logger

logger = get_logger(__name__)

class MyClass:
    def __init__(self):
        logger.info("Initializing MyClass")
    
    def process(self, data):
        logger.debug(f"Processing data: {data}")
        # ... 处理逻辑
        logger.info("Processing completed")
```

### 2. 记录关键操作

```python
logger.mission_start("data_analysis", dataset="large_dataset.csv")
try:
    result = analyze_data()
    logger.mission_complete("data_analysis", records_processed=1000)
except Exception as e:
    logger.error(f"Mission failed: {e}", exc_info=True)
```

### 3. 使用装饰器简化日志

```python
from harmonicgalaxy.utils.decorators import log_function_call

@log_function_call()
def critical_operation():
    # 自动记录调用和异常
    pass
```

### 4. 配置不同环境的日志级别

```python
import os

# 开发环境
if os.getenv("ENV") == "development":
    setup_logging(LoggingConfig(level="DEBUG"))
# 生产环境
else:
    setup_logging(LoggingConfig(level="INFO", log_dir="./logs"))
```

## 项目印记

所有日志都包含 `[HarmonicGalaxy]` 前缀，确保：
- 明确标识日志来源
- 便于日志过滤和分析
- 体现项目特色

## 示例

完整示例请查看 `examples/logging_example.py`。

