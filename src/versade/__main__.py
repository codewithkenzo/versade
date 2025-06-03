#!/usr/bin/env python3
"""
Versade MCP Server - Main entry point
Supports multiple transport modes for maximum compatibility.
"""

import argparse
import sys
from typing import Optional

from versade.server import mcp


def main() -> None:
    """Main entry point for Versade MCP Server."""
    parser = argparse.ArgumentParser(
        description="Versade MCP Server - Dependency analysis with strategic precision",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  versade                           # Run with stdio transport (default)
  versade --transport sse           # Run with SSE transport on localhost:8000
  versade --transport sse --port 9373  # Run with SSE on custom port
  versade --host 0.0.0.0 --port 8080   # Run with SSE on all interfaces
  
Transport modes:
  stdio: Standard input/output (for MCP clients like Claude Desktop)
  sse: Server-Sent Events over HTTP (for web clients)
        """
    )
    
    parser.add_argument(
        "--transport", 
        choices=["stdio", "sse"], 
        default="stdio",
        help="Transport mode (default: stdio)"
    )
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Log level (default: INFO)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Versade 1.0.0"
    )
    parser.add_argument(
        "--check-package",
        metavar="PACKAGE",
        help="Quick check of a package (for testing)"
    )
    
    args = parser.parse_args()
    
    # Handle quick package check
    if args.check_package:
        import asyncio
        from versade.server import check_python_package
        
        async def quick_check():
            print(f"🔍 Checking package: {args.check_package}")
            result = await check_python_package(args.check_package)
            if result.get("success"):
                print(f"✅ {result['name']} v{result['latest_version']}")
                print(f"   Description: {result.get('description', 'N/A')}")
                print(f"   Homepage: {result.get('homepage', 'N/A')}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        asyncio.run(quick_check())
        return
    
    # Set log level
    import logging
    import os
    os.environ["VERSADE_LOG_LEVEL"] = args.log_level
    
    # Print startup info for non-stdio modes
    if args.transport != "stdio":
        print(f"🚀 Starting Versade MCP Server")
        print(f"   Transport: {args.transport}")
        print(f"   Address: {args.host}:{args.port}")
        print(f"   Log level: {args.log_level}")
        print(f"   Available at: http://{args.host}:{args.port}")
        print()
    
    # Run the server
    try:
        # Set environment variables for SSE mode
        if args.transport == "sse":
            os.environ["MCP_SSE_HOST"] = args.host
            os.environ["MCP_SSE_PORT"] = str(args.port)
        
        # Run with the specified transport
        mcp.run(transport=args.transport)
    except KeyboardInterrupt:
        print("\n👋 Versade MCP Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
