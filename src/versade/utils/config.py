"""
Configuration utilities for the Versade package.
Strategic configuration management with unwavering precision.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, Field, validator
from pydantic.env_settings import SettingsSourceCallable


class LogLevel(str, Enum):
    """Log levels with strategic precision."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class TransportMode(str, Enum):
    """Transport modes with unwavering precision."""
    HTTP = "http"
    SSE = "sse"
    STDIO = "stdio"


class AppConfig(BaseSettings):
    """Strategic application configuration with deterministic values."""
    
    # Server configuration
    port: int = Field(default=9373, description="Server port")
    host: str = Field(default="0.0.0.0", description="Server host")
    
    # Logging configuration
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    log_format: str = Field(
        default="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        description="Log format string"
    )
    log_date_format: str = Field(default="%Y-%m-%d %H:%M:%S", description="Log date format")
    
    # CORS configuration
    cors_origins: List[str] = Field(default=["*"], description="CORS allowed origins")
    cors_credentials: bool = Field(default=True, description="CORS allow credentials")
    cors_methods: List[str] = Field(default=["*"], description="CORS allowed methods")
    cors_headers: List[str] = Field(default=["*"], description="CORS allowed headers")
    
    # Request configuration
    max_request_size: int = Field(default=1048576, description="Maximum request size in bytes")
    timeout: float = Field(default=30.0, description="Request timeout in seconds")
    
    # Rate limiting
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per window")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")
    
    # Transport configuration
    transport_mode: TransportMode = Field(default=TransportMode.HTTP, description="Transport mode")
    
    # Security configuration
    enable_security_checks: bool = Field(default=True, description="Enable security vulnerability checks")
    security_timeout: float = Field(default=10.0, description="Security check timeout")
    
    # Cache configuration
    enable_cache: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    
    # Development configuration
    debug: bool = Field(default=False, description="Enable debug mode")
    reload: bool = Field(default=False, description="Enable auto-reload")
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("cors_methods", pre=True)
    def parse_cors_methods(cls, v):
        """Parse CORS methods from string or list."""
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        return v
    
    @validator("cors_headers", pre=True)
    def parse_cors_headers(cls, v):
        """Parse CORS headers from string or list."""
        if isinstance(v, str):
            return [header.strip() for header in v.split(",")]
        return v
    
    class Config:
        """Pydantic configuration."""
        env_prefix = "VERSADE_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            """Customize settings sources priority."""
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get application configuration with unwavering precision."""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config


def reload_config() -> AppConfig:
    """Reload configuration from environment with strategic precision."""
    global _config
    _config = AppConfig()
    return _config


def get_version() -> str:
    """Get application version with strategic precision."""
    from versade import __version__
    return __version__


def get_project_root() -> Path:
    """Get project root directory with strategic precision."""
    return Path(__file__).parent.parent.parent.parent


def get_env_file_path() -> Path:
    """Get .env file path with strategic precision."""
    return get_project_root() / ".env"


def create_default_env_file() -> None:
    """Create default .env file with strategic precision."""
    env_file = get_env_file_path()
    if not env_file.exists():
        default_content = """# Versade Configuration
# Server Configuration
VERSADE_PORT=9373
VERSADE_HOST=0.0.0.0

# Logging Configuration
VERSADE_LOG_LEVEL=INFO

# CORS Configuration
VERSADE_CORS_ORIGINS=*

# Request Configuration
VERSADE_MAX_REQUEST_SIZE=1048576
VERSADE_TIMEOUT=30.0

# Rate Limiting
VERSADE_RATE_LIMIT_REQUESTS=100
VERSADE_RATE_LIMIT_WINDOW=60

# Transport Configuration
VERSADE_TRANSPORT_MODE=http

# Security Configuration
VERSADE_ENABLE_SECURITY_CHECKS=true
VERSADE_SECURITY_TIMEOUT=10.0

# Cache Configuration
VERSADE_ENABLE_CACHE=true
VERSADE_CACHE_TTL=300

# Development Configuration
VERSADE_DEBUG=false
VERSADE_RELOAD=false
"""
        env_file.write_text(default_content)
