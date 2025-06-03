#!/usr/bin/env python3
"""
Test script for Versade MCP tools
"""

import asyncio
import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from versade.server import check_python_package, check_npm_package

async def test_tools():
    """Test the MCP tools directly"""
    print("🧪 Testing Versade MCP Tools")
    print("=" * 50)
    
    # Test Python package checking
    print("\n📦 Testing Python package check (requests)...")
    result = await check_python_package("requests")
    if result.get("success"):
        print(f"✅ Success: {result['name']} v{result['latest_version']}")
        print(f"   Description: {result.get('description', 'N/A')}")
        print(f"   Homepage: {result.get('homepage', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    # Test npm package checking
    print("\n📦 Testing npm package check (express)...")
    result = await check_npm_package("express")
    if result.get("success"):
        print(f"✅ Success: {result['name']} v{result['latest_version']}")
        print(f"   Description: {result.get('description', 'N/A')}")
        print(f"   Homepage: {result.get('homepage', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    # Test with a non-existent package
    print("\n📦 Testing non-existent package...")
    result = await check_python_package("this-package-definitely-does-not-exist-12345")
    if not result.get("success"):
        print(f"✅ Correctly handled error: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ Unexpected success for non-existent package")
    
    print("\n🎉 Tool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_tools()) 