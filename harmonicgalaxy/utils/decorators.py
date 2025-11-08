"""Decorators for HarmonicGalaxy."""

import functools
from typing import Callable, Any
from harmonicgalaxy.utils.logging import get_logger


def log_function_call(logger_name: str = None):
    """Decorator to log function calls with galaxy theme.

    Args:
        logger_name: Optional logger name. If None, uses function's module.

    Example:
        >>> @log_function_call()
        >>> def my_function(x, y):
        ...     return x + y
    """

    def decorator(func: Callable) -> Callable:
        logger = get_logger(logger_name or func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"🔭 Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"✨ {func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"💥 {func.__name__} failed: {e}", exc_info=True)
                raise

        return wrapper

    return decorator


def log_async_function_call(logger_name: str = None):
    """Decorator to log async function calls with galaxy theme.

    Args:
        logger_name: Optional logger name. If None, uses function's module.

    Example:
        >>> @log_async_function_call()
        >>> async def my_async_function(x, y):
        ...     return x + y
    """

    def decorator(func: Callable) -> Callable:
        logger = get_logger(logger_name or func.__module__)

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.debug(f"🔭 Calling async {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = await func(*args, **kwargs)
                logger.debug(f"✨ Async {func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"💥 Async {func.__name__} failed: {e}", exc_info=True)
                raise

        return wrapper

    return decorator

