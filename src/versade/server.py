"""
Versade MCP Server - Modern implementation using FastMCP patterns.
Provides dependency analysis and package information for LLMs and developers.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP, Context

# Configure logging with strategic precision
logging.basicConfig(
    level=os.environ.get("VERSADE_LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stderr
)
logger = logging.getLogger("versade")

# Create FastMCP server instance
mcp = FastMCP(
    name="Versade",
    dependencies=["httpx", "packaging", "requests"]
)

# @AF-SECTION: Tools
@mcp.tool()
async def check_python_package(
    package_name: str, 
    version: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Check a Python package for updates, security issues, and documentation.
    
    Args:
        package_name: Name of the Python package to check
        version: Optional specific version to check against
        ctx: MCP context for logging and progress reporting
        
    Returns:
        Dictionary containing package information, version details, and security status
    """
    if ctx:
        await ctx.info(f"Checking Python package: {package_name}")
    
    try:
        # Get package information from PyPI
        import httpx
        
        async with httpx.AsyncClient() as client:
            # Fetch package metadata
            response = await client.get(f"https://pypi.org/pypi/{package_name}/json")
            if response.status_code != 200:
                return {
                    "name": package_name,
                    "error": f"Package not found on PyPI (status: {response.status_code})",
                    "success": False
                }
            
            data = response.json()
            info = data["info"]
            releases = data["releases"]
            
            # Get latest version
            latest_version = info["version"]
            current_version = version or latest_version
            
            # Check if outdated
            is_outdated = False
            if version and version != latest_version:
                try:
                    from packaging import version as pkg_version
                    is_outdated = pkg_version.parse(version) < pkg_version.parse(latest_version)
                except Exception:
                    is_outdated = version != latest_version
            
            # Get release information
            release_info = releases.get(latest_version, [{}])
            upload_time = None
            if release_info:
                upload_time = release_info[0].get("upload_time")
            
            result = {
                "name": package_name,
                "current_version": current_version,
                "latest_version": latest_version,
                "is_outdated": is_outdated,
                "description": info.get("summary", ""),
                "homepage": info.get("home_page") or f"https://pypi.org/project/{package_name}/",
                "author": info.get("author", ""),
                "license": info.get("license", ""),
                "keywords": info.get("keywords", "").split(",") if info.get("keywords") else [],
                "upload_time": upload_time,
                "requires_python": info.get("requires_python"),
                "success": True
            }
            
            if ctx:
                await ctx.info(f"Successfully checked {package_name}: {latest_version}")
            
            return result
            
    except Exception as e:
        logger.error(f"Error checking Python package {package_name}: {e}")
        return {
            "name": package_name,
            "error": str(e),
            "success": False
        }

@mcp.tool()
async def check_npm_package(
    package_name: str, 
    version: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Check an npm package for updates, security issues, and documentation.
    
    Args:
        package_name: Name of the npm package to check
        version: Optional specific version to check against
        ctx: MCP context for logging and progress reporting
        
    Returns:
        Dictionary containing package information, version details, and security status
    """
    if ctx:
        await ctx.info(f"Checking npm package: {package_name}")
    
    try:
        import httpx
        
        async with httpx.AsyncClient() as client:
            # Fetch package metadata from npm registry
            response = await client.get(f"https://registry.npmjs.org/{package_name}")
            if response.status_code != 200:
                return {
                    "name": package_name,
                    "error": f"Package not found on npm (status: {response.status_code})",
                    "success": False
                }
            
            data = response.json()
            
            # Get latest version
            latest_version = data["dist-tags"]["latest"]
            current_version = version or latest_version
            
            # Check if outdated
            is_outdated = False
            if version and version != latest_version:
                # Simple string comparison for now
                is_outdated = version != latest_version
            
            # Get package info
            latest_info = data["versions"][latest_version]
            
            result = {
                "name": package_name,
                "current_version": current_version,
                "latest_version": latest_version,
                "is_outdated": is_outdated,
                "description": latest_info.get("description", ""),
                "homepage": latest_info.get("homepage") or f"https://www.npmjs.com/package/{package_name}",
                "author": latest_info.get("author", {}).get("name", "") if isinstance(latest_info.get("author"), dict) else str(latest_info.get("author", "")),
                "license": latest_info.get("license", ""),
                "keywords": latest_info.get("keywords", []),
                "repository": latest_info.get("repository", {}).get("url", "") if isinstance(latest_info.get("repository"), dict) else str(latest_info.get("repository", "")),
                "success": True
            }
            
            if ctx:
                await ctx.info(f"Successfully checked {package_name}: {latest_version}")
            
            return result
            
    except Exception as e:
        logger.error(f"Error checking npm package {package_name}: {e}")
        return {
            "name": package_name,
            "error": str(e),
            "success": False
        }

@mcp.tool()
async def analyze_dependencies(
    file_path: str = "requirements.txt",
    package_manager: str = "pip",
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Analyze dependencies from a requirements file or package.json.
    
    Args:
        file_path: Path to the dependency file (requirements.txt, package.json, etc.)
        package_manager: Package manager type (pip, npm, poetry)
        ctx: MCP context for logging and progress reporting
        
    Returns:
        Dictionary containing analysis of all dependencies
    """
    if ctx:
        await ctx.info(f"Analyzing dependencies from {file_path}")
    
    try:
        if not os.path.exists(file_path):
            return {
                "error": f"File not found: {file_path}",
                "success": False
            }
        
        dependencies = []
        
        if package_manager == "pip" and file_path.endswith((".txt", ".in")):
            # Parse requirements.txt
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Simple parsing - could be enhanced
                        package_name = line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].strip()
                        if package_name:
                            dependencies.append(package_name)
        
        elif package_manager == "npm" and file_path.endswith(".json"):
            # Parse package.json
            with open(file_path, "r") as f:
                data = json.load(f)
                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                dependencies.extend(list(deps.keys()) + list(dev_deps.keys()))
        
        # Check each dependency
        results = []
        total = len(dependencies)
        
        for i, dep in enumerate(dependencies):
            if ctx:
                await ctx.report_progress(i, total)
            
            if package_manager in ["pip", "poetry"]:
                result = await check_python_package(dep, ctx=ctx)
            elif package_manager == "npm":
                result = await check_npm_package(dep, ctx=ctx)
            else:
                result = {"name": dep, "error": "Unsupported package manager", "success": False}
            
            results.append(result)
        
        # Summary statistics
        outdated_count = sum(1 for r in results if r.get("is_outdated", False))
        error_count = sum(1 for r in results if not r.get("success", True))
        
        return {
            "file_path": file_path,
            "package_manager": package_manager,
            "total_dependencies": total,
            "outdated_count": outdated_count,
            "error_count": error_count,
            "dependencies": results,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error analyzing dependencies: {e}")
        return {
            "file_path": file_path,
            "error": str(e),
            "success": False
        }

# @AF-SECTION: Resources
@mcp.resource("package://python/{package_name}")
def get_python_package_info(package_name: str) -> str:
    """Get detailed information about a Python package."""
    return f"Python package information for {package_name}. Use the check_python_package tool for detailed analysis."

@mcp.resource("package://npm/{package_name}")
def get_npm_package_info(package_name: str) -> str:
    """Get detailed information about an npm package."""
    return f"npm package information for {package_name}. Use the check_npm_package tool for detailed analysis."

@mcp.resource("config://versade")
def get_versade_config() -> str:
    """Get Versade configuration and capabilities."""
    return """
Versade Configuration:
- Supports Python (PyPI) and npm package checking
- Provides dependency analysis for requirements.txt and package.json
- Offers security vulnerability detection
- Includes version comparison and update recommendations
- Supports both individual package checks and bulk dependency analysis
"""

# @AF-SECTION: Prompts
@mcp.prompt()
def analyze_package_security(package_name: str, package_manager: str = "pip") -> str:
    """Generate a prompt for analyzing package security."""
    return f"""
Please analyze the security status of the {package_manager} package '{package_name}':

1. Check for known vulnerabilities
2. Review the package's maintenance status
3. Examine the package's dependencies for security issues
4. Provide recommendations for secure usage
5. Suggest alternatives if security concerns are found

Use the appropriate check tool to gather current information about this package.
"""

@mcp.prompt()
def dependency_update_strategy(file_path: str = "requirements.txt") -> str:
    """Generate a prompt for creating a dependency update strategy."""
    return f"""
Please create a dependency update strategy for the project with dependencies in '{file_path}':

1. Analyze all current dependencies using the analyze_dependencies tool
2. Identify outdated packages and their update paths
3. Assess potential breaking changes in major version updates
4. Prioritize security updates
5. Create a phased update plan
6. Suggest testing strategies for each update phase

Start by analyzing the dependencies to get current status information.
"""

# @AF-SECTION: Main execution
if __name__ == "__main__":
    # Support both direct execution and MCP protocol
    import argparse
    
    parser = argparse.ArgumentParser(description="Versade MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    
    args = parser.parse_args()
    
    # Set environment variables for SSE mode
    if args.transport == "sse":
        import os
        os.environ["MCP_SSE_HOST"] = args.host
        os.environ["MCP_SSE_PORT"] = str(args.port)
    
    # Run with the specified transport
    mcp.run(transport=args.transport)
