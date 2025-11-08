"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {"key": "value"}

