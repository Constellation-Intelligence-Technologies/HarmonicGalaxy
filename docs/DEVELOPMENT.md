# Development Guide

## 开发环境

### 系统要求

- Python 3.10+
- Git
- Make (可选，但推荐)

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git
cd HarmonicGalaxy

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装开发依赖
make install-dev
# 或
pip install -e ".[dev]"
pre-commit install

# 4. 验证安装
make test
```

## 常用命令

### 使用 Makefile

```bash
make help          # 查看所有可用命令
make install-dev   # 安装开发依赖
make test          # 运行测试
make lint          # 代码检查
make format        # 格式化代码
make type-check    # 类型检查
make clean         # 清理构建产物
```

### 直接使用工具

```bash
# 测试
pytest
pytest tests/unit/          # 只运行单元测试
pytest tests/integration/  # 只运行集成测试
pytest -m slow             # 运行标记为 slow 的测试

# 代码格式化
black harmonicgalaxy tests
isort harmonicgalaxy tests

# 代码检查
ruff check harmonicgalaxy tests
ruff check --fix harmonicgalaxy tests  # 自动修复

# 类型检查
mypy harmonicgalaxy

# Pre-commit
pre-commit run --all-files
```

## 代码规范

### 格式化

项目使用 Black 进行代码格式化，配置在 `pyproject.toml` 中：

- 行长度：100 字符
- 目标 Python 版本：3.10+

### 导入排序

使用 isort，配置为与 Black 兼容：

```python
# 标准库
import os
import sys

# 第三方库
import requests
import numpy as np

# 本地库
from harmonicgalaxy.core import Mission
from harmonicgalaxy.agents import Agent
```

### 类型注解

推荐为新代码添加类型注解：

```python
from typing import List, Optional, Dict

def process_agents(agents: List[Agent]) -> Dict[str, Optional[str]]:
    """处理智能体列表并返回结果字典。"""
    ...
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def create_mission(name: str, description: str) -> Mission:
    """创建新任务。
    
    Args:
        name: 任务名称
        description: 任务描述
        
    Returns:
        创建的 Mission 对象
        
    Raises:
        ValueError: 当名称或描述为空时
    """
    ...
```

## 测试

### 编写测试

测试文件命名：`test_*.py` 或 `*_test.py`

```python
import pytest
from harmonicgalaxy.core import Mission

@pytest.mark.unit
def test_mission_creation():
    """测试任务创建。"""
    mission = Mission(name="test", description="test mission")
    assert mission.name == "test"
    assert mission.description == "test mission"
```

### 测试标记

- `@pytest.mark.unit`: 单元测试
- `@pytest.mark.integration`: 集成测试
- `@pytest.mark.slow`: 慢速测试

### 运行特定测试

```bash
pytest tests/unit/test_core.py          # 运行特定文件
pytest tests/unit/test_core.py::test_mission_creation  # 运行特定测试
pytest -m unit                          # 运行标记为 unit 的测试
pytest -k "mission"                     # 运行名称包含 mission 的测试
```

### 覆盖率

```bash
pytest --cov=harmonicgalaxy --cov-report=html
# 查看 htmlcov/index.html
```

## Git 工作流

### 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档
- `style`: 格式（不影响代码运行）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(orchestrator): add agent selection strategy

Implement a new strategy for selecting the next agent based on
capability matching and load balancing.

Closes #123
```

### 分支命名

- `feature/feature-name`: 新功能
- `fix/bug-description`: Bug 修复
- `docs/documentation-update`: 文档更新
- `refactor/refactoring-description`: 重构

## 调试

### 使用 pytest 调试

```bash
pytest --pdb              # 失败时进入调试器
pytest --pdb-trace        # 每个测试前进入调试器
pytest -s                  # 显示 print 输出
pytest -v                  # 详细输出
```

### 日志

使用 Python 标准 logging：

```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
```

## 发布流程

1. 更新版本号（`pyproject.toml`）
2. 更新 `CHANGELOG.md`
3. 创建 release tag
4. 构建和发布包

## 常见问题

### Pre-commit hooks 失败

```bash
# 手动运行所有 hooks
pre-commit run --all-files

# 跳过 hooks（不推荐）
git commit --no-verify
```

### 类型检查错误

如果 mypy 报告错误但代码是正确的，可以使用类型忽略：

```python
result = some_function()  # type: ignore[assignment]
```

### 测试失败

1. 检查 Python 版本
2. 确保所有依赖已安装
3. 清理缓存：`make clean`
4. 重新安装：`pip install -e ".[dev]"`

