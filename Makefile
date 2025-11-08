.PHONY: help install install-dev test lint format type-check clean run

help:
	@echo "HarmonicGalaxy Development Commands"
	@echo "===================================="
	@echo "install      - Install package in development mode"
	@echo "install-dev  - Install package with development dependencies"
	@echo "test         - Run tests"
	@echo "lint         - Run linting checks"
	@echo "format       - Format code with black and isort"
	@echo "type-check   - Run type checking with mypy"
	@echo "clean        - Clean build artifacts"
	@echo "pre-commit   - Install pre-commit hooks"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=harmonicgalaxy --cov-report=html --cov-report=term

lint:
	ruff check harmonicgalaxy tests
	black --check harmonicgalaxy tests
	isort --check-only harmonicgalaxy tests

format:
	black harmonicgalaxy tests
	isort harmonicgalaxy tests
	ruff check --fix harmonicgalaxy tests

type-check:
	mypy harmonicgalaxy

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

pre-commit:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

