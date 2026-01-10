"""
Structured logging configuration for Epiphany Engine.

Provides JSON-formatted logging with context tracking.
"""

import contextvars
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional

request_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "request_id",
    default=None,
)
user_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("user", default=None)


def get_request_id() -> Optional[str]:
    """Return the current request id from contextvars."""
    return request_id_var.get()


def get_user() -> Optional[str]:
    """Return the current user from contextvars."""
    return user_var.get()


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.

    Outputs log records as JSON objects with consistent structure.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        # Add request context if available
        request_id = getattr(record, "request_id", None)
        if request_id is None:
            request_id = request_id_var.get()
        if request_id is not None:
            log_data["request_id"] = request_id

        user = getattr(record, "user", None)
        if user is None:
            user = user_var.get()
        if user is not None:
            log_data["user"] = user

        return json.dumps(log_data)


def setup_logging(log_level: str = None) -> logging.Logger:
    """
    Configure structured logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured root logger
    """
    # Get log level from environment or parameter
    level_name = log_level or os.getenv("LOG_LEVEL", "INFO")
    level = getattr(logging, level_name.upper(), logging.INFO)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Use JSON formatter in production, simple formatter in development
    use_json = os.getenv("LOG_FORMAT", "json").lower() == "json"

    if use_json:
        console_handler.setFormatter(JSONFormatter())
    else:
        # Simple formatter for development
        simple_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        console_handler.setFormatter(logging.Formatter(simple_format))

    logger.addHandler(console_handler)

    # Log initial configuration
    logger.info(
        "Logging configured",
        extra={
            "extra_fields": {
                "log_level": level_name,
                "format": "json" if use_json else "simple",
            }
        },
    )

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


class LogContext:
    """
    Context manager for adding extra fields to log records.

    Usage:
        with LogContext(request_id="123", user="alice"):
            logger.info("Processing request")
    """

    def __init__(self, request_id: Optional[str] = None, user: Optional[str] = None):
        """Initialize with extra fields to add to logs."""
        self.request_id = request_id
        self.user = user
        self.tokens: Dict[str, contextvars.Token] = {}

    def __enter__(self):
        """Add extra fields to log records."""
        if self.request_id is not None:
            self.tokens["request_id"] = request_id_var.set(self.request_id)
        if self.user is not None:
            self.tokens["user"] = user_var.set(self.user)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Reset context variables."""
        if "request_id" in self.tokens:
            request_id_var.reset(self.tokens["request_id"])
        if "user" in self.tokens:
            user_var.reset(self.tokens["user"])
