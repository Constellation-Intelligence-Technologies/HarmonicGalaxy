# Architecture Overview

## 项目结构

```
HarmonicGalaxy/
├── harmonicgalaxy/          # 主包
│   ├── __init__.py
│   ├── core/                # 核心组件
│   │   ├── __init__.py
│   │   └── mission.py       # 任务/使命模型
│   ├── agents/              # Agent 注册和能力描述
│   │   ├── __init__.py
│   │   ├── registry.py     # Agent 注册表
│   │   └── base.py         # Agent 基类
│   ├── orchestrator/        # 编排器
│   │   ├── __init__.py
│   │   └── engine.py        # 编排引擎
│   ├── state/               # 状态管理
│   │   ├── __init__.py
│   │   └── manager.py       # 状态管理器
│   └── events/              # 事件流
│       ├── __init__.py
│       └── stream.py        # 事件流处理
├── tests/                   # 测试
│   ├── __init__.py
│   ├── conftest.py          # pytest 配置
│   ├── unit/                # 单元测试
│   └── integration/         # 集成测试
├── docs/                    # 文档
│   ├── ARCHITECTURE.md      # 架构文档（本文件）
│   └── DEVELOPMENT.md       # 开发指南
├── scripts/                 # 脚本工具
├── .github/                 # GitHub 配置
│   └── workflows/           # CI/CD 工作流
├── pyproject.toml           # 项目配置
├── Makefile                # 开发命令
├── README.md               # 项目说明
├── CONTRIBUTING.md         # 贡献指南
└── CHANGELOG.md            # 变更日志
```

## 核心概念

### Mission（任务/使命）

Mission 是多步骤、多智能体工作流的基本单元。它包含：
- 任务上下文
- 执行状态
- 历史记录

### Agent（智能体）

每个 Agent 是一个独立的能力节点，具有：
- 能力描述
- 输入/输出接口
- 执行逻辑

### Orchestrator（编排器）

负责决定下一步执行哪个 Agent，考虑因素：
- Agent 能力匹配
- 当前任务状态
- 负载均衡

### State Manager（状态管理器）

维护任务的状态和上下文，支持：
- 状态持久化
- 状态查询
- 状态恢复

### Event Stream（事件流）

提供可观测性，记录：
- Agent 执行事件
- 状态变更事件
- 错误和警告

## 设计原则

1. **每个智能体都是一颗行星**：独立且有价值
2. **编排优先**：业务语义的流程编排
3. **天然有状态**：跨多轮、多阶段执行
4. **可扩展的银河系**：易于接入新组件

## 扩展点

- 新增 Agent：实现 Agent 接口并注册
- 自定义编排策略：实现 Orchestrator 接口
- 状态存储后端：实现 State Manager 接口
- 事件处理：实现 Event Handler 接口

