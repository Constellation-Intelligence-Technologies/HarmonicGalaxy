# HarmonicGalaxy

**HarmonicGalaxy** is the first foundational project of **CINT (Constellation Intelligence & Technologies)**.

It is a **distributed, multi-agent orchestration framework** designed to make many intelligent components work together in harmony — just like planets in a well-arranged galaxy.

> [中文版 / Chinese Version](README_zh.md)

---

## Key Ideas

- **Every agent matters**: each agent is a first-class capability node.
- **Harmonic orchestration**: tasks are not just passed around — they are arranged in a controllable, observable flow.
- **Stateful by design**: missions keep context across multiple agents and phases.
- **Extensible universe**: new agents, new scenarios, and new toolchains can be plugged into the same galaxy.

---

## What HarmonicGalaxy provides

- Mission / task model for multi-step AI workflows
- Orchestrator to decide which agent runs next
- Agent registry and capability description
- Context & state management
- Event / log stream for observability
- A naming / metaphor system that matches the CINT "constellation" universe

This project is intended to be the **gravitational core** of future CINT products: nebula-level solutions, agent bundles, and console/observatory tools will all orbit around HarmonicGalaxy.

---

## Quick Start

### Installation

**For using HarmonicGalaxy in your project:**

```bash
# Install from GitHub (recommended for now)
pip install git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev

# Or add to your requirements.txt:
# harmonicgalaxy @ git+https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git@dev
```

**For developing HarmonicGalaxy:**

```bash
# Clone the repository
git clone https://github.com/Constellation-Intelligence-Technologies/HarmonicGalaxy.git
cd HarmonicGalaxy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

See [Installation Guide](docs/INSTALLATION.md) for more details.

### Development

```bash
# Run tests
make test

# Format code
make format

# Run linting
make lint

# Type checking
make type-check
```

For more development guidelines, see [Development Guide](docs/DEVELOPMENT.md).

---

## Documentation

- [Development Guide](docs/DEVELOPMENT.md) - Development guidelines
- [Architecture](docs/ARCHITECTURE.md) - Architecture documentation
- [Contributing Guide](CONTRIBUTING.md) - Contributing guidelines
- [Changelog](CHANGELOG.md) - Changelog

---

## Contributing

We welcome all forms of contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

This project is licensed under the [Apache-2.0](LICENSE) License.
