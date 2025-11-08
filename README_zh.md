# HarmonicGalaxy（和弦星系）

**HarmonicGalaxy** 是 **CINT（Constellation Intelligence & Technologies）** 体系下的第一个基石项目，定位是一套 **分布式多智能体编排框架**。  
它要解决的问题是：当你有很多能力各不相同的智能体（Agent）时，如何在同一套引力场中让它们有序运行，而不是一团乱麻。

> [English Version](README.md)

---

## 核心理念

- **每个智能体都是一颗行星**：都有自己的能力和接口，都是一等公民。
- **编排优先**：不是把模型"调用一下"这么简单，而是把多个智能体排成有业务语义的流程。
- **天然有状态**：一次任务可以跨多轮、多阶段执行，状态在系统里被维护下来。
- **可扩展的银河系**：后续新增的场景、Agent、工具，都能接入同一套框架，不需要推翻重来。

---

## HarmonicGalaxy 提供什么？

- 一套适合多步骤、多智能体的任务/使命模型
- 一个负责"下一步该谁出场"的编排器
- 智能体的注册与能力描述机制
- 任务上下文与状态的管理
- 执行过程的事件流与日志，方便观测、排错和可视化
- 与 CINT 宇宙统一的命名与世界观（星系、星云、行星…）

我们希望以 **HarmonicGalaxy** 为"引力核心"，后续的智能客服、文档/政策智能、工具集成、可视化控制台等都能像星体一样围绕它生长，最终构成一套自己的智能星座体系。

---

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git
cd HarmonicGalaxy

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 以开发模式安装
pip install -e ".[dev]"

# 安装 pre-commit hooks
pre-commit install
```

### 开发

```bash
# 运行测试
make test

# 格式化代码
make format

# 代码检查
make lint

# 类型检查
make type-check
```

更多开发指南请查看 [开发指南](docs/DEVELOPMENT.md)。

---

## 文档

- [开发指南](docs/DEVELOPMENT.md) - 开发指南
- [架构文档](docs/ARCHITECTURE.md) - 架构文档
- [贡献指南](CONTRIBUTING.md) - 贡献指南
- [变更日志](CHANGELOG.md) - 变更日志

---

## 贡献

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

---

## 许可证

本项目采用 [Apache-2.0](LICENSE) 许可证。

