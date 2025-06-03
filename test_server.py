#!/usr/bin/env python3
"""
Test script for Versade MCP Server
"""

import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from versade.server import mcp

def test_server_info():
    """Test basic server information"""
    print("🚀 Versade MCP Server Test")
    print(f"Server name: {mcp.name}")
    print(f"Dependencies: {mcp.dependencies}")
    
    print("✅ Server basic info test completed successfully!")
    print("\n📋 Available functionality:")
    print("  🔧 Tools:")
    print("    - check_python_package: Check Python packages for updates and info")
    print("    - check_npm_package: Check npm packages for updates and info") 
    print("    - analyze_dependencies: Analyze dependency files")
    print("  📄 Resources:")
    print("    - package://python/{package_name}: Python package info")
    print("    - package://npm/{package_name}: npm package info")
    print("    - config://versade: Versade configuration")
    print("  💬 Prompts:")
    print("    - analyze_package_security: Security analysis prompt")
    print("    - dependency_update_strategy: Update strategy prompt")

if __name__ == "__main__":
    test_server_info() 