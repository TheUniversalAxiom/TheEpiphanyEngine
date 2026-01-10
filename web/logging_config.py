"""
Structured logging configuration for Epiphany Engine.

Provides JSON-formatted logging with context tracking.
"""

import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional


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
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if hasattr(record, "user"):
            log_data["user"] = record.user

        return json.dumps(log_data)


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Configure structured logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured root logger
    """
    # Get log level from environment or parameter
    level_name: str = log_level or os.getenv("LOG_LEVEL", "INFO") or "INFO"
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

    def __init__(self, **kwargs):
        """Initialize with extra fields to add to logs."""
        self.extra_fields = kwargs
        self.old_factory = None

    def __enter__(self):
        """Add extra fields to log records."""
        old_factory = logging.getLogRecordFactory()
        self.old_factory = old_factory

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            for key, value in self.extra_fields.items():
                setattr(record, key, value)
            return record

        logging.setLogRecordFactory(record_factory)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original log record factory."""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)
