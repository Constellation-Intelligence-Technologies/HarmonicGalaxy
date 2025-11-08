"""Logging utilities for HarmonicGalaxy with constellation theme.

This module provides a unified logging system with a "galaxy" theme,
where log levels are represented as celestial bodies and events flow
like stars in a constellation.
"""

import logging
import sys
from enum import Enum
from typing import Optional, Dict, Any
from pathlib import Path
import os
from datetime import datetime


class LogLevel(str, Enum):
    """Log levels represented as celestial bodies."""

    DEBUG = "DEBUG"  # Nebula - faint, detailed information
    INFO = "INFO"  # Star - normal operational messages
    WARNING = "WARNING"  # Comet - unusual but not error
    ERROR = "ERROR"  # Meteor - error occurred
    CRITICAL = "CRITICAL"  # Supernova - critical failure


# Celestial body emojis for log levels
CELESTIAL_EMOJIS = {
    "DEBUG": "🌌",  # Nebula
    "INFO": "⭐",  # Star
    "WARNING": "☄️",  # Comet
    "ERROR": "💥",  # Meteor
    "CRITICAL": "💫",  # Supernova
}

# Constellation names for different modules (project identity)
CONSTELLATION_PREFIX = "HarmonicGalaxy"


class StandardFormatter(logging.Formatter):
    """Standard formatter without galaxy theme."""

    # Color codes for terminal
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",
    }

    def __init__(
        self,
        use_colors: bool = True,
        show_project_prefix: bool = True,
    ):
        """Initialize standard formatter.

        Args:
            use_colors: Whether to use colors in output
            show_project_prefix: Whether to show [HarmonicGalaxy] prefix
        """
        super().__init__()
        self.use_colors = use_colors and sys.stdout.isatty()
        self.show_project_prefix = show_project_prefix

    def format(self, record: logging.LogRecord) -> str:
        """Format log record in standard format."""
        # Get color
        color = self.COLORS.get(record.levelname, "")
        reset = self.COLORS["RESET"] if self.use_colors else ""

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        # Project prefix
        prefix = f"[{CONSTELLATION_PREFIX}]" if self.show_project_prefix else ""

        # Module/component name
        component = f"[{record.name}]" if record.name != "root" else ""

        # Format message
        if self.use_colors:
            level_name = f"{color}{record.levelname:8s}{reset}"
        else:
            level_name = f"{record.levelname:8s}"

        # Build log line
        log_parts = [
            timestamp,
            prefix,
            level_name,
            component,
            record.getMessage(),
        ]

        # Add exception info if present
        if record.exc_info:
            log_parts.append(self.formatException(record.exc_info))

        return " ".join(filter(None, log_parts))


class GalaxyFormatter(logging.Formatter):
    """Custom formatter with galaxy theme."""

    # Color codes for terminal
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan for nebula
        "INFO": "\033[32m",  # Green for star
        "WARNING": "\033[33m",  # Yellow for comet
        "ERROR": "\033[31m",  # Red for meteor
        "CRITICAL": "\033[35m",  # Magenta for supernova
        "RESET": "\033[0m",
    }

    def __init__(
        self,
        use_colors: bool = True,
        show_emoji: bool = True,
        show_constellation: bool = True,
    ):
        """Initialize galaxy formatter.

        Args:
            use_colors: Whether to use colors in output
            show_emoji: Whether to show celestial emojis
            show_constellation: Whether to show constellation prefix
        """
        super().__init__()
        self.use_colors = use_colors and sys.stdout.isatty()
        self.show_emoji = show_emoji
        self.show_constellation = show_constellation

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with galaxy theme."""
        # Get celestial emoji
        emoji = CELESTIAL_EMOJIS.get(record.levelname, "⭐")
        if not self.show_emoji:
            emoji = ""

        # Get color
        color = self.COLORS.get(record.levelname, "")
        reset = self.COLORS["RESET"] if self.use_colors else ""

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        # Constellation prefix
        constellation = f"[{CONSTELLATION_PREFIX}]" if self.show_constellation else ""

        # Module/component name (like a planet in the galaxy)
        component = f"[{record.name}]" if record.name != "root" else ""

        # Format message
        if self.use_colors:
            level_name = f"{color}{record.levelname}{reset}"
        else:
            level_name = record.levelname

        # Build log line
        log_parts = [
            timestamp,
            constellation,
            emoji,
            level_name,
            component,
            record.getMessage(),
        ]

        # Add exception info if present
        if record.exc_info:
            log_parts.append(self.formatException(record.exc_info))

        return " ".join(filter(None, log_parts))


class GalaxyLogger(logging.Logger):
    """Extended logger with galaxy-themed methods."""

    def mission_start(self, mission_name: str, **kwargs):
        """Log mission start (like a new constellation formation)."""
        details = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.info(f"🚀 Mission '{mission_name}' initiated {details}".strip())

    def mission_complete(self, mission_name: str, **kwargs):
        """Log mission completion."""
        details = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.info(f"✅ Mission '{mission_name}' completed {details}".strip())

    def agent_activated(self, agent_name: str, capability: Optional[str] = None):
        """Log agent activation (like a planet coming online)."""
        cap_info = f" (capability: {capability})" if capability else ""
        self.info(f"🪐 Agent '{agent_name}' activated{cap_info}")

    def agent_deactivated(self, agent_name: str):
        """Log agent deactivation."""
        self.info(f"🌑 Agent '{agent_name}' deactivated")

    def orchestration_step(self, step: int, description: str):
        """Log orchestration step."""
        self.debug(f"🎼 Orchestration step {step}: {description}")

    def state_update(self, state_key: str, old_value: Any, new_value: Any):
        """Log state update."""
        self.debug(f"🔄 State '{state_key}' updated: {old_value} → {new_value}")

    def event_emitted(self, event_type: str, event_data: Optional[Dict[str, Any]] = None):
        """Log event emission."""
        data_str = f" {event_data}" if event_data else ""
        self.debug(f"📡 Event '{event_type}' emitted{data_str}")


# Register custom logger class
logging.setLoggerClass(GalaxyLogger)


class LoggingConfig:
    """Configuration for HarmonicGalaxy logging."""

    def __init__(
        self,
        level: str = "INFO",
        enabled: bool = True,
        theme: str = "galaxy",  # "galaxy" or "standard"
        use_colors: bool = True,
        show_emoji: bool = True,
        show_constellation: bool = True,
        log_file: Optional[str] = None,
        log_dir: Optional[str] = None,
        file_level: Optional[str] = None,
    ):
        """Initialize logging configuration.

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            enabled: Whether logging is enabled
            theme: Log theme - "galaxy" (with emojis and galaxy theme) or "standard" (plain format)
            use_colors: Whether to use colors in console output
            show_emoji: Whether to show celestial emojis (only for galaxy theme)
            show_constellation: Whether to show constellation prefix
            log_file: Optional log file path
            log_dir: Optional log directory (log_file will be created here)
            file_level: Optional different log level for file (defaults to level)
        """
        self.level = level.upper()
        self.enabled = enabled
        self.theme = theme.lower()
        if self.theme not in ["galaxy", "standard"]:
            raise ValueError(f"Invalid theme: {theme}. Must be 'galaxy' or 'standard'")
        self.use_colors = use_colors
        self.show_emoji = show_emoji
        self.show_constellation = show_constellation
        self.log_file = log_file
        self.log_dir = log_dir
        self.file_level = (file_level or level).upper()

    @classmethod
    def from_env(cls) -> "LoggingConfig":
        """Create config from environment variables.

        Environment variables:
            HARMONICGALAXY_LOG_LEVEL: Log level (default: INFO)
            HARMONICGALAXY_LOG_ENABLED: Enable/disable logging (default: true)
            HARMONICGALAXY_LOG_THEME: Log theme - "galaxy" or "standard" (default: galaxy)
            HARMONICGALAXY_LOG_COLORS: Enable/disable colors (default: true)
            HARMONICGALAXY_LOG_EMOJI: Enable/disable emojis (default: true, only for galaxy theme)
            HARMONICGALAXY_LOG_FILE: Log file path
            HARMONICGALAXY_LOG_DIR: Log directory
        """
        level = os.getenv("HARMONICGALAXY_LOG_LEVEL", "INFO").upper()
        enabled = os.getenv("HARMONICGALAXY_LOG_ENABLED", "true").lower() == "true"
        theme = os.getenv("HARMONICGALAXY_LOG_THEME", "galaxy").lower()
        use_colors = os.getenv("HARMONICGALAXY_LOG_COLORS", "true").lower() == "true"
        show_emoji = os.getenv("HARMONICGALAXY_LOG_EMOJI", "true").lower() == "true"
        log_file = os.getenv("HARMONICGALAXY_LOG_FILE")
        log_dir = os.getenv("HARMONICGALAXY_LOG_DIR")

        return cls(
            level=level,
            enabled=enabled,
            theme=theme,
            use_colors=use_colors,
            show_emoji=show_emoji,
            log_file=log_file,
            log_dir=log_dir,
        )


def setup_logging(config: Optional[LoggingConfig] = None) -> None:
    """Setup HarmonicGalaxy logging system.

    Args:
        config: Logging configuration. If None, loads from environment.
    """
    if config is None:
        config = LoggingConfig.from_env()

    if not config.enabled:
        logging.disable(logging.CRITICAL + 1)
        return

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.level, logging.INFO))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config.level, logging.INFO))

    # Choose formatter based on theme
    if config.theme == "galaxy":
        console_formatter = GalaxyFormatter(
            use_colors=config.use_colors,
            show_emoji=config.show_emoji,
            show_constellation=config.show_constellation,
        )
    else:  # standard theme
        console_formatter = StandardFormatter(
            use_colors=config.use_colors,
            show_project_prefix=config.show_constellation,
        )

    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (if configured)
    if config.log_file or config.log_dir:
        if config.log_dir:
            log_dir_path = Path(config.log_dir)
            log_dir_path.mkdir(parents=True, exist_ok=True)
            log_file_path = log_dir_path / f"harmonicgalaxy_{datetime.now().strftime('%Y%m%d')}.log"
        else:
            log_file_path = Path(config.log_file)

        # Ensure log file directory exists
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, config.file_level, logging.DEBUG))

        # Choose formatter based on theme for file
        if config.theme == "galaxy":
            file_formatter = GalaxyFormatter(
                use_colors=False,
                show_emoji=config.show_emoji,
                show_constellation=config.show_constellation,
            )
        else:  # standard theme
            file_formatter = StandardFormatter(
                use_colors=False,
                show_project_prefix=config.show_constellation,
            )

        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: Optional[str] = None) -> GalaxyLogger:
    """Get a logger instance with galaxy theme.

    Args:
        name: Logger name (typically module name). If None, uses caller's module.

    Returns:
        GalaxyLogger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Star is shining")
        >>> logger.mission_start("explore_galaxy", target="Andromeda")
    """
    if name is None:
        import inspect

        frame = inspect.currentframe().f_back
        name = frame.f_globals.get("__name__", "harmonicgalaxy")

    logger = logging.getLogger(name)
    return logger  # type: ignore


# Initialize logging on module import
setup_logging()

