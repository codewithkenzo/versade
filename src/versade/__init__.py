"""
Versade: Versatile dependency analysis and MCP server with strategic precision.

A modern MCP server for dependency analysis, package checking, and security monitoring.
Supports Python (PyPI) and npm packages with comprehensive analysis capabilities.
"""

__version__ = "1.0.0"
__author__ = "Versade Team"
__description__ = "Versatile dependency analysis and MCP server with strategic precision"

# Export main server for MCP integration
from versade.server import mcp

# Export key components for programmatic use
from versade.server import (
    check_python_package,
    check_npm_package,
    analyze_dependencies,
)

__all__ = [
    "mcp",
    "check_python_package", 
    "check_npm_package",
    "analyze_dependencies",
    "__version__",
    "__author__",
    "__description__",
]
