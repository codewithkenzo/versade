"""
Main entry point for the Versade MCP server.
Provides deterministic startup and shutdown for LLM and developer dependency checking.
"""

import asyncio
import logging
import os
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from versade.api.routes import router
from versade.models.core import ErrorCode, McpError
from versade.services.checker import DependencyChecker

# Configure logging with strategic precision
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("versade")

# Global dependency checker instance for strategic reuse
dependency_checker: Optional[DependencyChecker] = None

# Environment variable for port with unwavering precision
DEFAULT_PORT = 9373
port = int(os.environ.get("VERSADE_PORT", DEFAULT_PORT))

# FastAPI application with strategic configuration
app = FastAPI(
    title="Versade", 
    version="1.0.0",
    description="Versatile dependency version checker and documentation finder for LLM and developer assistance."
)

# Add CORS middleware with unwavering precision
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes with strategic precision
app.include_router(router)


@app.exception_handler(McpError)
async def mcp_error_handler(request: Request, exc: McpError) -> JSONResponse:
    """Handle MCP errors with strategic precision."""
    return JSONResponse(
        status_code=400,
        content={"error": {"code": exc.code, "message": exc.message}}
    )


@app.on_event("startup")
async def startup_event() -> None:
    """
    Strategic startup event with unwavering precision.
    Initialize resources with deterministic execution.
    """
    global dependency_checker
    logger.info("Starting Versade with unwavering precision")
    dependency_checker = DependencyChecker()
    logger.info(f"Versade running on port {port}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Strategic shutdown event with unwavering precision.
    Clean up resources with deterministic execution.
    """
    global dependency_checker
    logger.info("Shutting down Versade with strategic precision")
    if dependency_checker:
        await dependency_checker.close()
    logger.info("Versade has been shut down with unwavering precision")


def main() -> None:
    """Strategic entry point with unwavering precision for LLM and developer assistance."""
    import argparse
    import socket
    from contextlib import closing
    
    # Create command line parser with strategic precision
    parser = argparse.ArgumentParser(
        description="Versade: Versatile dependency version checker and documentation finder for LLM and developer assistance"
    )
    parser.add_argument(
        "-p", "--port", 
        type=int,
        default=port,
        help=f"Port to run the server on (default: {port})"
    )
    parser.add_argument(
        "--host", 
        type=str,
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--check", 
        action="store_true",
        help="Check dependencies in current directory without starting server"
    )
    
    args = parser.parse_args()
    
    # Handle check argument with unwavering precision
    if args.check:
        logger.info("Checking dependencies in current directory with strategic precision")
        # TODO: Implement checking dependencies in current directory
        return
    
    # Find available port with strategic fallback
    def is_port_available(port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex((args.host, port)) != 0
    
    # If specified port is not available, find the next available port
    if not is_port_available(args.port):
        logger.warning(f"Port {args.port} is already in use. Finding available port with strategic precision...")
        for port_attempt in range(args.port + 1, args.port + 100):
            if is_port_available(port_attempt):
                logger.info(f"Found available port: {port_attempt}")
                args.port = port_attempt
                break
        else:
            logger.error("Could not find an available port. Please specify an available port with --port")
            return
    
    # Run server with strategic precision
    logger.info(f"Starting Versade server on {args.host}:{args.port} with unwavering precision")
    uvicorn.run("versade.__main__:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
