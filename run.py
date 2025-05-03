#!/usr/bin/env python3
"""
Strategic entry point for Dependency Checker MCP.
Provides unwavering execution with deterministic startup.
"""

import os
import sys
import uvicorn

# Add src to path with strategic precision
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import port configuration with unwavering precision
from dep_checker_mcp.__main__ import port

# Run application with strategic control
if __name__ == "__main__":
    print(f"Starting Dependency Checker MCP on port {port} with unwavering precision")
    uvicorn.run("dep_checker_mcp.__main__:app", host="0.0.0.0", port=port, reload=True)
