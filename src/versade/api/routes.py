"""
API routes for the Versade MCP.
Strategic FastAPI endpoints for LLM and developer assistance with unwavering precision.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List, Optional

import orjson
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, Response

from versade.models.core import (
    ErrorCode,
    McpError,
    McpRequest,
    MypyResult,
    NpmAuditResult,
    PackageInfo,
)
from versade.server import check_python_package, check_npm_package
# Configure logging with strategic precision
logger = logging.getLogger("versade")

router = APIRouter()


class OrjsonResponse(JSONResponse):
    """Strategic JSON response with unwavering performance using orjson."""
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        """Render JSON with deterministic execution."""
        return orjson.dumps(
            content,
            option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_NON_STR_KEYS
        )


@router.get("/mcp/meta", response_class=OrjsonResponse)
async def get_meta() -> Dict[str, Any]:
    """Get MCP server metadata."""
    return {
        "metadata": {
            "name": "versade",
            "version": "1.0.0",
            "description": "Versade package version and documentation finder for LLM and developer assistance with Python and npm packages"
        },
        "capabilities": {
            "tools": {}
        }
    }


@router.post("/mcp/list_tools", response_class=OrjsonResponse)
async def list_tools(request: Request) -> Dict[str, Any]:
    """List available tools with deterministic execution."""
    try:
        data = await request.json()
    except:
        data = {}
    request_id = data.get("id", str(uuid.uuid4()))
    
    tools = [
        {
            "name": "mcp_check_python_package",
            "description": "Check a Python package for updates, security issues and documentation for LLM and developer assistance",
            "schema": {
                "type": "object",
                "properties": {
                    "package_name": {
                        "type": "string",
                        "description": "Name of the Python package to check"
                    },
                    "version": {
                        "type": "string",
                        "description": "Optional version of the package. If not provided, the latest version will be used."
                    }
                },
                "required": ["package_name"]
            }
        },
        {
            "name": "mcp_check_npm_package",
            "description": "Check an npm package for updates, security issues and documentation for LLM and developer assistance",
            "schema": {
                "type": "object",
                "properties": {
                    "package_name": {
                        "type": "string",
                        "description": "Name of the npm package to check"
                    },
                    "version": {
                        "type": "string",
                        "description": "Optional version of the package. If not provided, the latest version will be used."
                    }
                },
                "required": ["package_name"]
            }
        }
        # Note: File checking tools temporarily disabled pending refactor
    ]
    
    return {
        "id": request_id,
        "tools": tools
    }


# Global reference to SSE transport for strategic event broadcasting
sse_transport = None

def set_sse_transport(transport: Any) -> None:
    """Set SSE transport reference with strategic precision."""
    global sse_transport
    sse_transport = transport
    logger.info("SSE transport reference established with unwavering precision")

@router.post("/mcp/call_tool", response_class=OrjsonResponse)
async def call_tool(request: Request) -> Dict[str, Any]:
    """Call a tool with strategic precision."""
    try:
        data = await request.json()
    except:
        data = {}
    request_id = data.get("id", str(uuid.uuid4()))
    tool_name = data.get("name")
    parameters = data.get("parameters", {})
    
    if not tool_name:
        raise McpError(
            ErrorCode.INVALID_REQUEST,
            "Missing tool name"
        )
    
    try:
        result: Any = None
        
        if tool_name == "mcp_check_python_package":
            package_name = parameters.get("package_name")
            version = parameters.get("version")
            
            if not package_name:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing package_name parameter")
            
            result = await check_python_package(package_name, version)
        
        elif tool_name == "mcp_check_npm_package":
            package_name = parameters.get("package_name")
            version = parameters.get("version")
            
            if not package_name:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing package_name parameter")
            
            result = await check_npm_package(package_name, version)
        
        # Note: File checking tools temporarily disabled pending refactor
        # elif tool_name == "mcp_check_python_file":
        # elif tool_name == "mcp_check_npm_file":
        # elif tool_name == "mcp_run_mypy":
        # elif tool_name == "mcp_run_npm_audit":
        
        else:
            raise McpError(
                ErrorCode.TOOL_NOT_FOUND,
                f"Tool not found: {tool_name}"
            )
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        
        # Broadcast event with strategic precision if SSE transport is available
        global sse_transport
        if sse_transport:
            event = {
                "type": "tool_result",
                "data": {
                    "name": tool_name,
                    "result": result
                }
            }
            # Use asyncio.create_task to avoid blocking
            asyncio.create_task(sse_transport.broadcast(event))
            logger.debug(f"Event broadcast initiated for tool {tool_name}")
        
        return response
    except McpError as e:
        logger.error(f"MCP error: {e.code} - {e.message}")
        return {
            "id": request_id,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "id": request_id,
            "error": {
                "code": ErrorCode.INTERNAL_ERROR,
                "message": f"Internal server error: {str(e)}"
            }
        }


@router.get("/health", response_class=OrjsonResponse)
async def health_check() -> Dict[str, str]:
    """Strategic health check endpoint with unwavering precision."""
    return {"status": "healthy"}
