"""
 * flask_captcha2 OSS
 * author: github.com/alisharify7
 * email: alisharifyofficial@gmail.com
 * license: see LICENSE for more details.
 * Copyright (c) 2023 - ali sharifi
 * https://github.com/alisharify7/flask_captcha2
"""
import sys
import logging
from typing import Optional


def get_logger(
        log_level: Optional[int] = None,
        logger_name: str = "Flask-Captcha",
        log_format: Optional[str] = None,
        handlers: Optional[list[logging.Handler]] = None
) -> logging.Logger:
    """Create and configure a custom Logger with given level, name, and formatting.

    Args:
        log_level: Logging level (e.g., logging.DEBUG, logging.INFO). Defaults to logging.DEBUG.
        logger_name: Name of the logger. Defaults to "Flask-Captcha".
        log_format: Custom log format string. If None, uses a default format.
        handlers: List of custom handlers to add. If None, adds a stdout StreamHandler.

    Returns:
        Configured Logger instance.

    Example:
        >>> logger = get_logger(logging.INFO)
        >>> logger.info("Test message")
    """
    log_level = logging.DEBUG if log_level is None else log_level

    # Create default format if none provided
    if log_format is None:
        log_format = (
            f"[{logger_name} - %(levelname)s] "
            "[%(asctime)s] [%(filename)s:%(lineno)d] - %(message)s"
        )

    formatter = logging.Formatter(log_format)

    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        if handlers is None:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(log_level)
            handler.setFormatter(formatter)
            handlers = [handler]

        for handler in handlers:
            logger.addHandler(handler)

    logger.setLevel(log_level)
    logger.propagate = False
    return logger