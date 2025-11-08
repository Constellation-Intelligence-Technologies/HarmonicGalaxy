"""Example unit tests."""

import pytest


@pytest.mark.unit
def test_example():
    """Example test to verify test setup."""
    assert True


@pytest.mark.unit
class TestExample:
    """Example test class."""

    def test_method(self):
        """Example test method."""
        assert 1 + 1 == 2

