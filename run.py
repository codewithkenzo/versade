#!/usr/bin/env python3
"""
Entry point for Versade package version and documentation finder.
Provides simple server startup for the MCP interface.
"""

import os
import sys
import uvicorn

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import port configuration
from versade.__main__ import port

# Run application
if __name__ == "__main__":
    print(f"Starting Versade on port {port}")
    uvicorn.run("versade.__main__:app", host="0.0.0.0", port=port, reload=True)
