"""
Configuration utilities for the Dependency Checker MCP.
Strategic configuration management with unwavering precision.
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AppConfig:
    """Strategic application configuration with deterministic values."""
    port: int
    log_level: str
    cors_origins: list[str]
    max_request_size: int
    rate_limit_requests: int
    rate_limit_window: int
    timeout: float
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment with strategic precision."""
        return cls(
            port=int(os.environ.get("DEP_CHECKER_MCP_PORT", "9373")),
            log_level=os.environ.get("DEP_CHECKER_MCP_LOG_LEVEL", "INFO"),
            cors_origins=os.environ.get("DEP_CHECKER_MCP_CORS_ORIGINS", "*").split(","),
            max_request_size=int(os.environ.get("DEP_CHECKER_MCP_MAX_REQUEST_SIZE", "1048576")),
            rate_limit_requests=int(os.environ.get("DEP_CHECKER_MCP_RATE_LIMIT_REQUESTS", "5")),
            rate_limit_window=int(os.environ.get("DEP_CHECKER_MCP_RATE_LIMIT_WINDOW", "1")),
            timeout=float(os.environ.get("DEP_CHECKER_MCP_TIMEOUT", "30.0")),
        )


def get_config() -> AppConfig:
    """Get application configuration with unwavering precision."""
    return AppConfig.from_env()


def get_version() -> str:
    """Get application version with strategic precision."""
    from dep_checker_mcp import __version__
    return __version__
