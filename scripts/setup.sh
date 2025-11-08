#!/bin/bash
# Setup script for HarmonicGalaxy development environment

set -e

echo "🚀 Setting up HarmonicGalaxy development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📌 Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install package in development mode
echo "📥 Installing HarmonicGalaxy in development mode..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
pytest tests/unit/test_example.py -v

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  make test"
echo ""
echo "To format code:"
echo "  make format"
echo ""

