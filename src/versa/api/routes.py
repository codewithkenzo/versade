"""
API routes for the Dependency Checker MCP.
Strategic FastAPI endpoints with unwavering precision.
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

import orjson
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, Response

from dep_checker_mcp.models.core import (
    ErrorCode,
    McpError,
    McpRequest,
    MypyResult,
    NpmAuditResult,
    PackageInfo,
)
from dep_checker_mcp.services.checker import DependencyChecker

# Configure logging with strategic precision
logger = logging.getLogger("dep-checker-mcp")

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


def get_dependency_checker() -> DependencyChecker:
    """Dependency injection with strategic precision."""
    return DependencyChecker()


@router.get("/mcp/meta", response_class=OrjsonResponse)
async def get_meta() -> Dict[str, Any]:
    """Get MCP server metadata with strategic values."""
    return {
        "metadata": {
            "name": "dependency-checker-mcp",
            "version": "1.0.0",
            "description": "Strategic MCP server for validating both Python and npm dependencies with unwavering precision"
        },
        "capabilities": {
            "tools": {}
        }
    }


@router.post("/mcp/list_tools", response_class=OrjsonResponse)
async def list_tools(request: Request) -> Dict[str, Any]:
    """List available tools with deterministic execution."""
    data = await request.json()
    request_id = data.get("id", str(uuid.uuid4()))
    
    tools = [
        {
            "name": "mcp_check_python_package",
            "description": "Check a Python package for updates and security issues",
            "parameters": {
                "properties": {
                    "package_name": {
                        "description": "Name of the Python package to check",
                        "type": "string"
                    },
                    "version": {
                        "description": "Current version (optional)",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        },
        {
            "name": "mcp_check_npm_package",
            "description": "Check an npm package for updates and security issues",
            "parameters": {
                "properties": {
                    "package_name": {
                        "description": "Name of the npm package to check",
                        "type": "string"
                    },
                    "version": {
                        "description": "Current version (optional)",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        },
        {
            "name": "mcp_check_python_file",
            "description": "Check a Python requirements.txt or pyproject.toml file",
            "parameters": {
                "properties": {
                    "file_path": {
                        "description": "Path to the requirements file",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        },
        {
            "name": "mcp_check_npm_file",
            "description": "Check a package.json file",
            "parameters": {
                "properties": {
                    "file_path": {
                        "description": "Path to the package.json file",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        },
        {
            "name": "mcp_run_mypy",
            "description": "Run mypy type checker on a Python file or directory",
            "parameters": {
                "properties": {
                    "file_path": {
                        "description": "Path to the Python file or directory",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        },
        {
            "name": "mcp_run_npm_audit",
            "description": "Run npm audit on a package.json file",
            "parameters": {
                "properties": {
                    "file_path": {
                        "description": "Path to the package.json file",
                        "type": "string"
                    }
                },
                "type": "object"
            }
        }
    ]
    
    return {
        "id": request_id,
        "tools": tools
    }


@router.post("/mcp/call_tool", response_class=OrjsonResponse)
async def call_tool(
    request: Request, 
    dependency_checker: DependencyChecker = Depends(get_dependency_checker)
) -> Dict[str, Any]:
    """Call a tool with strategic precision."""
    data = await request.json()
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
            
            result = await dependency_checker.check_python_package(package_name, version)
        
        elif tool_name == "mcp_check_npm_package":
            package_name = parameters.get("package_name")
            version = parameters.get("version")
            
            if not package_name:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing package_name parameter")
            
            result = await dependency_checker.check_npm_package(package_name, version)
        
        elif tool_name == "mcp_check_python_file":
            file_path = parameters.get("file_path")
            if not file_path:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing file_path parameter")
            
            result = await dependency_checker.check_python_file(file_path)
        
        elif tool_name == "mcp_check_npm_file":
            file_path = parameters.get("file_path")
            if not file_path:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing file_path parameter")
            
            result = await dependency_checker.check_npm_file(file_path)
        
        elif tool_name == "mcp_run_mypy":
            file_path = parameters.get("file_path")
            if not file_path:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing file_path parameter")
            
            result = await dependency_checker.run_mypy(file_path)
        
        elif tool_name == "mcp_run_npm_audit":
            file_path = parameters.get("file_path")
            if not file_path:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing file_path parameter")
            
            result = await dependency_checker.run_npm_audit(file_path)
        
        else:
            raise McpError(
                ErrorCode.TOOL_NOT_FOUND,
                f"Tool not found: {tool_name}"
            )
        
        return {
            "id": request_id,
            "result": result
        }
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
