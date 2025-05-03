#!/usr/bin/env python3
"""
Dependency Checker MCP Server
------------------------------
Strategic MCP server for validating both Python and npm dependencies with unwavering precision.
Provides deterministic dependency checking, version comparison, and security reporting.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import anyio
import httpx
import orjson
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

# Configure logging with strategic precision
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("dep-checker-mcp")


class ErrorCode(str, Enum):
    """MCP protocol error codes with deterministic values."""
    INTERNAL_ERROR = "internal_error"
    INVALID_REQUEST = "invalid_request"
    INVALID_PARAMS = "invalid_params"
    TOOL_NOT_FOUND = "tool_not_found"
    TOOL_EXECUTION_ERROR = "tool_execution_error"


class McpError(Exception):
    """Strategic error handling for MCP protocol."""
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass
class PackageInfo:
    """Package information with deterministic structure."""
    name: str
    current_version: str
    latest_version: str
    is_outdated: bool
    homepage: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[str] = None
    security_issues: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.security_issues is None:
            self.security_issues = []


class DependencyChecker:
    """
    Strategic dependency checker with unwavering precision.
    Handles both Python and npm package validation.
    """
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def check_python_package(self, package_name: str, version: Optional[str] = None) -> PackageInfo:
        """Check Python package with strategic precision."""
        try:
            # Get the latest version from PyPI
            response = await self.http_client.get(
                f"https://pypi.org/pypi/{package_name}/json",
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            pypi_data = response.json()
            
            latest_version = pypi_data["info"]["version"]
            homepage = pypi_data["info"]["home_page"] or pypi_data["info"]["project_url"]
            description = pypi_data["info"]["summary"]
            release_date = next(
                (release_date for ver, release_info in pypi_data["releases"].items() 
                 if ver == latest_version and release_info for release_date in [release_info[0].get("upload_time", None)]),
                None
            )
            
            current_version = version or latest_version
            is_outdated = self._compare_versions(current_version, latest_version)
            
            # Check for security issues with strategic precision
            security_issues = []
            try:
                safety_response = await self.http_client.get(
                    f"https://pyup.io/api/v1/safety/{package_name}/{current_version}",
                    headers={"Accept": "application/json"}
                )
                if safety_response.status_code == 200:
                    safety_data = safety_response.json()
                    security_issues = safety_data.get("vulnerabilities", [])
            except Exception as e:
                logger.warning(f"Could not check security for {package_name}: {str(e)}")
            
            return PackageInfo(
                name=package_name,
                current_version=current_version,
                latest_version=latest_version,
                is_outdated=is_outdated,
                homepage=homepage,
                description=description,
                release_date=release_date,
                security_issues=security_issues
            )
        except Exception as e:
            logger.error(f"Error checking Python package {package_name}: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error checking Python package {package_name}: {str(e)}"
            )
    
    async def check_npm_package(self, package_name: str, version: Optional[str] = None) -> PackageInfo:
        """Check npm package with unwavering precision."""
        try:
            # Get the latest version from npm registry
            response = await self.http_client.get(
                f"https://registry.npmjs.org/{package_name}",
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            npm_data = response.json()
            
            latest_version = npm_data["dist-tags"]["latest"]
            homepage = npm_data["homepage"]
            description = npm_data["description"]
            release_date = npm_data["time"].get(latest_version)
            
            current_version = version or latest_version
            is_outdated = self._compare_versions(current_version, latest_version)
            
            # Check for security issues with strategic precision
            security_issues = []
            try:
                # Check npm audit API with deterministic execution
                audit_response = await self.http_client.post(
                    "https://registry.npmjs.org/-/npm/v1/security/advisories/bulk",
                    json={"packages": [{package_name: current_version}]},
                    headers={"Accept": "application/json"}
                )
                if audit_response.status_code == 200:
                    audit_data = audit_response.json()
                    security_issues = list(audit_data.get("advisories", {}).values())
            except Exception as e:
                logger.warning(f"Could not check security for {package_name}: {str(e)}")
            
            return PackageInfo(
                name=package_name,
                current_version=current_version,
                latest_version=latest_version,
                is_outdated=is_outdated,
                homepage=homepage,
                description=description,
                release_date=release_date,
                security_issues=security_issues
            )
        except Exception as e:
            logger.error(f"Error checking npm package {package_name}: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error checking npm package {package_name}: {str(e)}"
            )
    
    async def check_python_file(self, file_path: str) -> List[PackageInfo]:
        """Check Python requirements file with strategic precision."""
        if not os.path.exists(file_path):
            raise McpError(
                ErrorCode.INVALID_PARAMS,
                f"File not found: {file_path}"
            )
        
        with open(file_path, "r") as f:
            content = f.read()
        
        # Parse requirements with unwavering precision
        packages = []
        
        # Strategy 1: Parse requirements.txt format
        if file_path.endswith(".txt"):
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Extract package name and version with deterministic regex
                match = re.match(r"([a-zA-Z0-9_.-]+)\s*([=<>!~]+.*)?", line)
                if match:
                    package_name = match.group(1)
                    version_spec = match.group(2)
                    
                    # Extract exact version from specification with strategic precision
                    version = None
                    if version_spec:
                        exact_match = re.match(r"==\s*([a-zA-Z0-9_.-]+)", version_spec)
                        if exact_match:
                            version = exact_match.group(1)
                    
                    packages.append((package_name, version))
        
        # Strategy 2: Parse pyproject.toml format
        elif file_path.endswith(".toml"):
            # Use a simplified TOML parser for unwavering precision
            dependencies_section = False
            for line in content.splitlines():
                line = line.strip()
                
                if line == "[tool.poetry.dependencies]" or line == "dependencies = [":
                    dependencies_section = True
                    continue
                elif line.startswith("[") or line == "]":
                    dependencies_section = False
                
                if dependencies_section and "=" in line:
                    # Extract package with deterministic logic
                    line = line.strip('"\',[]()')
                    match = re.match(r'["\']*([a-zA-Z0-9_.-]+)["\']*\s*[=]+\s*["\']*([^"\'#,]+)', line)
                    if match:
                        package_name = match.group(1)
                        version_spec = match.group(2).strip()
                        
                        # Clean version spec with strategic precision
                        version = version_spec.strip('"\'>=^~')
                        packages.append((package_name, version))
        
        # Check each package with unwavering precision
        results = []
        for package_name, version in packages:
            try:
                package_info = await self.check_python_package(package_name, version)
                results.append(package_info)
            except Exception as e:
                logger.error(f"Error checking {package_name}: {str(e)}")
                # Include error record with deterministic structure
                results.append(PackageInfo(
                    name=package_name,
                    current_version=version or "unknown",
                    latest_version="error",
                    is_outdated=False,
                    description=f"Error: {str(e)}"
                ))
        
        return results
    
    async def check_npm_file(self, file_path: str) -> List[PackageInfo]:
        """Check npm package.json file with strategic precision."""
        if not os.path.exists(file_path):
            raise McpError(
                ErrorCode.INVALID_PARAMS,
                f"File not found: {file_path}"
            )
        
        with open(file_path, "r") as f:
            content = f.read()
        
        try:
            # Parse package.json with deterministic execution
            data = json.loads(content)
            
            # Extract dependencies with strategic precision
            dependencies = {}
            for dep_type in ["dependencies", "devDependencies"]:
                if dep_type in data:
                    for name, version in data[dep_type].items():
                        # Clean version spec for deterministic comparison
                        clean_version = version.strip('"\'>=^~')
                        dependencies[name] = clean_version
            
            # Check each package with unwavering precision
            results = []
            for package_name, version in dependencies.items():
                try:
                    package_info = await self.check_npm_package(package_name, version)
                    results.append(package_info)
                except Exception as e:
                    logger.error(f"Error checking {package_name}: {str(e)}")
                    # Include error record with deterministic structure
                    results.append(PackageInfo(
                        name=package_name,
                        current_version=version or "unknown",
                        latest_version="error",
                        is_outdated=False,
                        description=f"Error: {str(e)}"
                    ))
            
            return results
        except Exception as e:
            logger.error(f"Error parsing package.json: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error parsing package.json: {str(e)}"
            )
    
    async def run_mypy(self, file_path: str) -> Dict[str, Any]:
        """Run mypy with unwavering precision."""
        if not os.path.exists(file_path):
            raise McpError(
                ErrorCode.INVALID_PARAMS,
                f"File not found: {file_path}"
            )
        
        try:
            # Use asyncio.subprocess for deterministic execution
            proc = await asyncio.create_subprocess_exec(
                "mypy", 
                "--show-column-numbers",
                "--show-error-codes",
                file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
            
            # Parse mypy output with strategic precision
            issues = []
            if stdout:
                for line in stdout.decode().splitlines():
                    # Parse mypy output with deterministic regex
                    match = re.match(r"([^:]+):(\d+):(\d+): (\w+): (.+) \[(\w+)\]", line)
                    if match:
                        file, line_num, col, level, message, error_code = match.groups()
                        issues.append({
                            "file": file,
                            "line": int(line_num),
                            "column": int(col),
                            "level": level,
                            "message": message,
                            "error_code": error_code
                        })
            
            return {
                "success": proc.returncode == 0,
                "issues": issues,
                "exit_code": proc.returncode
            }
        except Exception as e:
            logger.error(f"Error running mypy: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error running mypy: {str(e)}"
            )
    
    async def run_npm_audit(self, file_path: str) -> Dict[str, Any]:
        """Run npm audit with unwavering precision."""
        if not os.path.exists(file_path):
            raise McpError(
                ErrorCode.INVALID_PARAMS,
                f"File not found: {file_path}"
            )
        
        project_dir = os.path.dirname(file_path)
        
        try:
            # Use asyncio.subprocess for deterministic execution
            proc = await asyncio.create_subprocess_exec(
                "npm", 
                "audit", 
                "--json",
                cwd=project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
            
            if stdout:
                # Parse npm audit output with strategic precision
                audit_data = json.loads(stdout.decode())
                return {
                    "success": proc.returncode == 0,
                    "vulnerabilities": audit_data.get("vulnerabilities", {}),
                    "metadata": audit_data.get("metadata", {}),
                    "exit_code": proc.returncode
                }
            else:
                return {
                    "success": False,
                    "error": stderr.decode() if stderr else "No output from npm audit",
                    "exit_code": proc.returncode
                }
        except Exception as e:
            logger.error(f"Error running npm audit: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error running npm audit: {str(e)}"
            )
    
    def _compare_versions(self, current: str, latest: str) -> bool:
        """Compare versions with strategic precision to determine if outdated."""
        if current == latest:
            return False
        
        # Parse versions for deterministic comparison
        current_parts = re.findall(r'\d+', current)
        latest_parts = re.findall(r'\d+', latest)
        
        # Convert to integers with unwavering precision
        current_parts = [int(part) for part in current_parts]
        latest_parts = [int(part) for part in latest_parts]
        
        # Pad shorter list with strategic precision
        while len(current_parts) < len(latest_parts):
            current_parts.append(0)
        while len(latest_parts) < len(current_parts):
            latest_parts.append(0)
        
        # Compare parts with deterministic logic
        for c, l in zip(current_parts, latest_parts):
            if c < l:
                return True
            elif c > l:
                return False
        
        return False


# FastAPI application with strategic configuration
app = FastAPI(
    title="Dependency Checker MCP", 
    version="1.0.0"
)

# Add CORS middleware with unwavering precision
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize checker with strategic timing
dependency_checker = DependencyChecker()


@app.exception_handler(McpError)
async def mcp_error_handler(request: Request, exc: McpError):
    """Handle MCP errors with strategic precision."""
    return JSONResponse(
        status_code=400,
        content={"error": {"code": exc.code, "message": exc.message}}
    )


@app.get("/mcp/meta")
async def get_meta():
    """Get MCP server metadata with strategic values."""
    return {
        "metadata": {
            "name": "dependency-checker-mcp",
            "version": "1.0.0"
        },
        "capabilities": {
            "tools": {}
        }
    }


@app.post("/mcp/list_tools")
async def list_tools(request: Request):
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
                        "description": "Path to the Python requirements file",
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


@app.post("/mcp/call_tool")
async def call_tool(request: Request):
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
        result = None
        
        # Route tool call with deterministic precision
        if tool_name == "mcp_check_python_package":
            package_name = parameters.get("package_name")
            if not package_name:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing package_name parameter")
            
            version = parameters.get("version")
            result = await dependency_checker.check_python_package(package_name, version)
            
            # Convert dataclass to dict with strategic serialization
            result = {
                "name": result.name,
                "current_version": result.current_version,
                "latest_version": result.latest_version,
                "is_outdated": result.is_outdated,
                "homepage": result.homepage,
                "description": result.description,
                "release_date": result.release_date,
                "security_issues": result.security_issues
            }
        
        elif tool_name == "mcp_check_npm_package":
            package_name = parameters.get("package_name")
            if not package_name:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing package_name parameter")
            
            version = parameters.get("version")
            result = await dependency_checker.check_npm_package(package_name, version)
            
            # Convert dataclass to dict with strategic serialization
            result = {
                "name": result.name,
                "current_version": result.current_version,
                "latest_version": result.latest_version,
                "is_outdated": result.is_outdated,
                "homepage": result.homepage,
                "description": result.description,
                "release_date": result.release_date,
                "security_issues": result.security_issues
            }
        
        elif tool_name == "mcp_check_python_file":
            file_path = parameters.get("file_path")
            if not file_path:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing file_path parameter")
            
            results = await dependency_checker.check_python_file(file_path)
            
            # Convert dataclasses to dicts with unwavering precision
            result = {
                "file": file_path,
                "packages": [
                    {
                        "name": pkg.name,
                        "current_version": pkg.current_version,
                        "latest_version": pkg.latest_version,
                        "is_outdated": pkg.is_outdated,
                        "homepage": pkg.homepage,
                        "description": pkg.description,
                        "release_date": pkg.release_date,
                        "security_issues": pkg.security_issues
                    }
                    for pkg in results
                ]
            }
        
        elif tool_name == "mcp_check_npm_file":
            file_path = parameters.get("file_path")
            if not file_path:
                raise McpError(ErrorCode.INVALID_PARAMS, "Missing file_path parameter")
            
            results = await dependency_checker.check_npm_file(file_path)
            
            # Convert dataclasses to dicts with unwavering precision
            result = {
                "file": file_path,
                "packages": [
                    {
                        "name": pkg.name,
                        "current_version": pkg.current_version,
                        "latest_version": pkg.latest_version,
                        "is_outdated": pkg.is_outdated,
                        "homepage": pkg.homepage,
                        "description": pkg.description,
                        "release_date": pkg.release_date,
                        "security_issues": pkg.security_issues
                    }
                    for pkg in results
                ]
            }
        
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
                f"Unknown tool: {tool_name}"
            )
        
        return {
            "id": request_id,
            "content": result
        }
    except McpError as e:
        raise e
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        raise McpError(
            ErrorCode.TOOL_EXECUTION_ERROR,
            f"Error executing tool {tool_name}: {str(e)}"
        )


@app.get("/mcp/stream")
async def stream(request: Request):
    """
    Establish SSE stream for deterministic real-time communication.
    This is the strategic endpoint for agent connections.
    """
    async def event_generator():
        """Generate events with unwavering precision."""
        while True:
            # Keep connection alive with strategic timing
            yield {
                "event": "ping",
                "data": json.dumps({"timestamp": time.time()})
            }
            await anyio.sleep(30)
    
    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn
    
    # Strategic port selection with deterministic fallback
    port = int(os.environ.get("DEP_CHECKER_MCP_PORT", "9373"))
    
    # Execute with unwavering precision
    uvicorn.run(app, host="0.0.0.0", port=port)
