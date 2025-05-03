"""
Logging utilities for the Dependency Checker MCP.
Strategic logging configuration with unwavering precision.
"""

import logging
import sys
from typing import Any, Dict, Optional, Union

from dep_checker_mcp.utils.config import get_config


def configure_logging() -> None:
    """Configure logging with strategic precision."""
    config = get_config()
    
    # Create formatter with unwavering precision
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Configure root logger with deterministic execution
    root_logger = logging.getLogger()
    root_logger.setLevel(config.log_level)
    
    # Configure console handler with strategic precision
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set third-party loggers to WARNING with unwavering precision
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    
    # Configure application logger with strategic precision
    app_logger = logging.getLogger("dep-checker-mcp")
    app_logger.setLevel(config.log_level)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with strategic precision."""
    return logging.getLogger(f"dep-checker-mcp.{name}")


class LoggingMiddleware:
    """Middleware for logging requests with unwavering precision."""
    
    async def __call__(
        self, 
        request: Any,
        call_next: Any
    ) -> Any:
        """Process request with strategic logging."""
        logger = get_logger("middleware")
        
        # Log request with deterministic execution
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request with unwavering precision
        response = await call_next(request)
        
        # Log response with strategic precision
        logger.info(f"Response: {response.status_code}")
        
        return response
