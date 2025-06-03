#!/usr/bin/env python3
"""
Versade MCP Server Entry Point
Simple script to run the Versade MCP server in various modes.
"""

import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from versade.server import mcp

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
