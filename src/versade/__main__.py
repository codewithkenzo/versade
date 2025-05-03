"""
Main entry point for the Dependency Checker MCP server.
Provides deterministic startup and shutdown with strategic precision.
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
logger = logging.getLogger("dep-checker-mcp")

# Global dependency checker instance for strategic reuse
dependency_checker: Optional[DependencyChecker] = None

# Environment variable for port with unwavering precision
DEFAULT_PORT = 9373
port = int(os.environ.get("DEP_CHECKER_MCP_PORT", DEFAULT_PORT))

# FastAPI application with strategic configuration
app = FastAPI(
    title="Dependency Checker MCP", 
    version="1.0.0",
    description="Strategic MCP server for validating both Python and npm dependencies with unwavering precision."
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
    logger.info("Starting Dependency Checker MCP with unwavering precision")
    dependency_checker = DependencyChecker()
    logger.info(f"Dependency Checker MCP running on port {port}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Strategic shutdown event with unwavering precision.
    Clean up resources with deterministic execution.
    """
    global dependency_checker
    logger.info("Shutting down Dependency Checker MCP with strategic precision")
    if dependency_checker:
        await dependency_checker.close()
    logger.info("Dependency Checker MCP has been shut down with unwavering precision")


def main() -> None:
    """Strategic entry point with unwavering precision."""
    uvicorn.run("dep_checker_mcp.__main__:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
