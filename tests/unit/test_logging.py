"""Tests for logging utilities."""

import pytest
import logging
import os
from harmonicgalaxy.utils.logging import (
    get_logger,
    setup_logging,
    LoggingConfig,
    LogLevel,
    GalaxyLogger,
)


@pytest.mark.unit
class TestLoggingConfig:
    """Test LoggingConfig class."""

    def test_create_config(self):
        """Test creating a logging config."""
        config = LoggingConfig(level="DEBUG", enabled=True)
        assert config.level == "DEBUG"
        assert config.enabled is True
        assert config.theme == "galaxy"  # Default theme

    def test_create_config_standard_theme(self):
        """Test creating config with standard theme."""
        config = LoggingConfig(theme="standard", level="INFO")
        assert config.theme == "standard"
        assert config.level == "INFO"

    def test_create_config_invalid_theme(self):
        """Test creating config with invalid theme."""
        with pytest.raises(ValueError):
            LoggingConfig(theme="invalid")

    def test_from_env(self):
        """Test creating config from environment."""
        os.environ["HARMONICGALAXY_LOG_LEVEL"] = "WARNING"
        os.environ["HARMONICGALAXY_LOG_ENABLED"] = "false"
        os.environ["HARMONICGALAXY_LOG_THEME"] = "standard"

        config = LoggingConfig.from_env()
        assert config.level == "WARNING"
        assert config.enabled is False
        assert config.theme == "standard"

        # Cleanup
        del os.environ["HARMONICGALAXY_LOG_LEVEL"]
        del os.environ["HARMONICGALAXY_LOG_ENABLED"]
        del os.environ["HARMONICGALAXY_LOG_THEME"]


@pytest.mark.unit
class TestGetLogger:
    """Test get_logger function."""

    def test_get_logger(self):
        """Test getting a logger."""
        logger = get_logger("test_module")
        assert isinstance(logger, GalaxyLogger)
        assert logger.name == "test_module"

    def test_get_logger_default_name(self):
        """Test getting logger with default name."""
        logger = get_logger()
        assert isinstance(logger, GalaxyLogger)


@pytest.mark.unit
class TestGalaxyLogger:
    """Test GalaxyLogger custom methods."""

    def test_mission_start(self, caplog):
        """Test mission_start method."""
        logger = get_logger("test")
        with caplog.at_level(logging.INFO):
            logger.mission_start("test_mission", target="test_target")
            assert "Mission 'test_mission' initiated" in caplog.text

    def test_mission_complete(self, caplog):
        """Test mission_complete method."""
        logger = get_logger("test")
        with caplog.at_level(logging.INFO):
            logger.mission_complete("test_mission", duration="1s")
            assert "Mission 'test_mission' completed" in caplog.text

    def test_agent_activated(self, caplog):
        """Test agent_activated method."""
        logger = get_logger("test")
        with caplog.at_level(logging.INFO):
            logger.agent_activated("test_agent", capability="test_capability")
            assert "Agent 'test_agent' activated" in caplog.text

    def test_agent_deactivated(self, caplog):
        """Test agent_deactivated method."""
        logger = get_logger("test")
        with caplog.at_level(logging.INFO):
            logger.agent_deactivated("test_agent")
            assert "Agent 'test_agent' deactivated" in caplog.text

    def test_orchestration_step(self, caplog):
        """Test orchestration_step method."""
        logger = get_logger("test")
        with caplog.at_level(logging.DEBUG):
            logger.orchestration_step(1, "test step")
            assert "Orchestration step 1" in caplog.text

    def test_state_update(self, caplog):
        """Test state_update method."""
        logger = get_logger("test")
        with caplog.at_level(logging.DEBUG):
            logger.state_update("test_key", "old", "new")
            assert "State 'test_key' updated" in caplog.text

    def test_event_emitted(self, caplog):
        """Test event_emitted method."""
        logger = get_logger("test")
        with caplog.at_level(logging.DEBUG):
            logger.event_emitted("test_event", {"key": "value"})
            assert "Event 'test_event' emitted" in caplog.text


@pytest.mark.unit
class TestSetupLogging:
    """Test setup_logging function."""

    def test_setup_logging_enabled(self):
        """Test setting up logging when enabled."""
        config = LoggingConfig(level="INFO", enabled=True)
        setup_logging(config)
        logger = get_logger("test")
        assert logger.level <= logging.INFO

    def test_setup_logging_disabled(self):
        """Test setting up logging when disabled."""
        config = LoggingConfig(level="INFO", enabled=False)
        setup_logging(config)
        # When disabled, logging should be at CRITICAL+1
        assert logging.getLogger().disabled is True

    def test_setup_logging_standard_theme(self):
        """Test setting up logging with standard theme."""
        config = LoggingConfig(theme="standard", level="INFO", enabled=True)
        setup_logging(config)
        logger = get_logger("test")
        assert logger.level <= logging.INFO

    def test_setup_logging_galaxy_theme(self):
        """Test setting up logging with galaxy theme."""
        config = LoggingConfig(theme="galaxy", level="INFO", enabled=True)
        setup_logging(config)
        logger = get_logger("test")
        assert logger.level <= logging.INFO

