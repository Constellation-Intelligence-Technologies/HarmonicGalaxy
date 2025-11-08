"""Example usage of HarmonicGalaxy logging system.

This example demonstrates the galaxy-themed logging system with
various configuration options and logging methods.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from harmonicgalaxy import get_logger, setup_logging, LogLevel
from harmonicgalaxy.utils.logging import LoggingConfig


def basic_logging_example():
    """Basic logging example."""
    print("\n" + "=" * 60)
    print("Basic Logging Example")
    print("=" * 60)

    logger = get_logger(__name__)

    logger.debug("🌌 This is a debug message (Nebula - detailed info)")
    logger.info("⭐ This is an info message (Star - normal operation)")
    logger.warning("☄️ This is a warning message (Comet - unusual but not error)")
    logger.error("💥 This is an error message (Meteor - error occurred)")
    logger.critical("💫 This is a critical message (Supernova - critical failure)")


def galaxy_themed_methods_example():
    """Example of galaxy-themed logging methods."""
    print("\n" + "=" * 60)
    print("Galaxy-Themed Methods Example")
    print("=" * 60)

    logger = get_logger(__name__)

    # Mission logging
    logger.mission_start("explore_galaxy", target="Andromeda", distance="2.5M light-years")
    logger.mission_complete("explore_galaxy", duration="5.2s", discoveries=3)

    # Agent logging
    logger.agent_activated("data_processor", capability="text_analysis")
    logger.agent_deactivated("data_processor")

    # Orchestration logging
    logger.orchestration_step(1, "Selecting next agent")
    logger.orchestration_step(2, "Executing agent task")

    # State logging
    logger.state_update("mission_status", "pending", "in_progress")
    logger.state_update("agent_count", 0, 5)

    # Event logging
    logger.event_emitted("agent_ready", {"agent_id": "agent_001", "status": "ready"})


def configuration_example():
    """Example of different logging configurations."""
    print("\n" + "=" * 60)
    print("Configuration Examples")
    print("=" * 60)

    # Example 1: Galaxy theme (default)
    print("\n--- Galaxy Theme (Default) ---")
    config_galaxy = LoggingConfig(theme="galaxy", level="INFO", show_emoji=True, use_colors=True)
    setup_logging(config_galaxy)
    logger = get_logger("galaxy_example")
    logger.info("⭐ Galaxy theme message with emoji")
    logger.warning("☄️ Warning message")

    # Example 2: Standard theme
    print("\n--- Standard Theme ---")
    config_standard = LoggingConfig(theme="standard", level="INFO", use_colors=True)
    setup_logging(config_standard)
    logger = get_logger("standard_example")
    logger.info("Standard theme message without emoji")
    logger.warning("Warning message in standard format")

    # Example 3: Debug level
    print("\n--- Debug Level (Galaxy Theme) ---")
    config_debug = LoggingConfig(theme="galaxy", level="DEBUG", show_emoji=True, use_colors=True)
    setup_logging(config_debug)
    logger = get_logger("debug_example")
    logger.debug("Debug message visible")
    logger.info("Info message visible")

    # Example 4: Standard theme without colors
    print("\n--- Standard Theme (No Colors) ---")
    config_standard_no_color = LoggingConfig(theme="standard", level="INFO", use_colors=False)
    setup_logging(config_standard_no_color)
    logger = get_logger("standard_no_color_example")
    logger.info("Standard message without colors")

    # Example 5: File logging with galaxy theme
    print("\n--- File Logging (Galaxy Theme) ---")
    config_file = LoggingConfig(
        theme="galaxy",
        level="DEBUG",
        log_dir="./logs",
        file_level="DEBUG",
    )
    setup_logging(config_file)
    logger = get_logger("file_example")
    logger.info("This message will be written to log file with galaxy theme")
    print("Check ./logs/ directory for log files")


def decorator_example():
    """Example of using logging decorators."""
    print("\n" + "=" * 60)
    print("Decorator Example")
    print("=" * 60)

    from harmonicgalaxy.utils.decorators import log_function_call, log_async_function_call
    import asyncio

    @log_function_call()
    def calculate_sum(a: int, b: int) -> int:
        """Calculate sum of two numbers."""
        return a + b

    @log_async_function_call()
    async def async_task(name: str) -> str:
        """Async task example."""
        await asyncio.sleep(0.1)
        return f"Task {name} completed"

    # Sync function
    result = calculate_sum(5, 3)
    print(f"Result: {result}")

    # Async function
    async def run_async():
        result = await async_task("test")
        print(f"Result: {result}")

    asyncio.run(run_async())


def theme_comparison_example():
    """Compare galaxy theme vs standard theme."""
    print("\n" + "=" * 60)
    print("Theme Comparison")
    print("=" * 60)

    print("\n--- Galaxy Theme ---")
    config_galaxy = LoggingConfig(theme="galaxy", level="INFO")
    setup_logging(config_galaxy)
    logger = get_logger("comparison")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

    print("\n--- Standard Theme ---")
    config_standard = LoggingConfig(theme="standard", level="INFO")
    setup_logging(config_standard)
    logger = get_logger("comparison")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")


def environment_config_example():
    """Example of using environment variables for configuration."""
    print("\n" + "=" * 60)
    print("Environment Configuration Example")
    print("=" * 60)
    print("""
To configure logging via environment variables, set:

export HARMONICGALAXY_LOG_LEVEL=DEBUG
export HARMONICGALAXY_LOG_ENABLED=true
export HARMONICGALAXY_LOG_THEME=galaxy  # or "standard"
export HARMONICGALAXY_LOG_COLORS=true
export HARMONICGALAXY_LOG_EMOJI=true
export HARMONICGALAXY_LOG_FILE=./logs/app.log
export HARMONICGALAXY_LOG_DIR=./logs

Then use:
    from harmonicgalaxy.utils.logging import LoggingConfig
    config = LoggingConfig.from_env()
    setup_logging(config)
    """)


if __name__ == "__main__":
    # Setup default logging
    setup_logging()

    # Run examples
    basic_logging_example()
    galaxy_themed_methods_example()
    configuration_example()
    theme_comparison_example()
    decorator_example()
    environment_config_example()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)

