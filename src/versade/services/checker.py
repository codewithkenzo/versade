"""
Versade dependency checker service for both Python and npm packages.
Handles version comparison and documentation retrieval.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import httpx
import orjson

from versade.models.core import (
    ErrorCode,
    McpError,
    MypyIssue,
    MypyResult,
    NpmAuditResult,
    PackageInfo,
)

# Configure logging
logger = logging.getLogger("dep-checker-mcp")


class DependencyChecker:
    """
    Dependency checker for Python and npm packages.
    Handles package validation and documentation retrieval.
    """
    def __init__(self) -> None:
        self.http_client: httpx.AsyncClient = httpx.AsyncClient(timeout=30.0)
    
    async def check_python_package(self, package_name: str, version: Optional[str] = None) -> PackageInfo:
        """Check Python package for version information and documentation."""
        try:
            # Get package info from PyPI
            response = await self.http_client.get(
                f"https://pypi.org/pypi/{package_name}/json",
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            pypi_data = cast(Dict[str, Any], response.json())
            
            # Extract relevant info
            latest_version = str(pypi_data["info"]["version"])
            homepage = str(pypi_data["info"]["home_page"] or pypi_data["info"]["project_url"] or f"https://pypi.org/project/{package_name}/")
            description = str(pypi_data["info"]["summary"] or "")
            
            # Extract documentation URLs
            project_urls = pypi_data["info"].get("project_urls", {})
            documentation_url = None
            api_docs_url = None
            github_url = None
            
            # Look for documentation links
            for label, url in project_urls.items():
                label_lower = label.lower()
                if "documentation" in label_lower or "docs" in label_lower:
                    documentation_url = url
                elif "api" in label_lower:
                    api_docs_url = url
                elif "github" in label_lower or "source" in label_lower or "repository" in label_lower:
                    github_url = url
            
            # Set documentation URL fallbacks if not found
            if not documentation_url:
                documentation_url = project_urls.get("Documentation") or project_urls.get("Homepage") or homepage
            
            # Try to find mypy stubs URL
            mypy_stub_url = f"https://github.com/python/typeshed/tree/master/stubs/{package_name}" if package_name else None
            
            # Check if the package has typing info on PyPI
            has_py_typed = False
            for file_info in pypi_data.get("urls", []):
                if file_info.get("packagetype") == "sdist":
                    # Package likely has typing information
                    has_py_typed = True
                    break
            
            # If no mypy stub found and package has typing, use its documentation
            if not mypy_stub_url and has_py_typed and documentation_url:
                mypy_stub_url = documentation_url
            
            # Extract release date
            release_date: Optional[str] = None
            release_info = pypi_data["releases"].get(latest_version, [])
            if release_info and isinstance(release_info, list) and len(release_info) > 0:
                release_date = str(release_info[0].get("upload_time", ""))
            
            current_version = version or latest_version
            is_outdated = self._compare_versions(current_version, latest_version)
            
            # Check for security issues
            security_issues: List[Dict[str, Any]] = []
            try:
                safety_response = await self.http_client.get(
                    f"https://pyup.io/api/v1/safety/{package_name}/{current_version}",
                    headers={"Accept": "application/json"}
                )
                if safety_response.status_code == 200:
                    safety_data = cast(Dict[str, Any], safety_response.json())
                    security_issues = cast(List[Dict[str, Any]], safety_data.get("vulnerabilities", []))
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
                security_issues=security_issues,
                documentation_url=documentation_url,
                api_docs_url=api_docs_url,
                mypy_stub_url=mypy_stub_url,
                github_url=github_url
            )
        except Exception as e:
            logger.error(f"Error checking Python package {package_name}: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error checking Python package {package_name}: {str(e)}"
            )
    
    async def check_npm_package(self, package_name: str, version: Optional[str] = None) -> PackageInfo:
        """Check npm package for version information and documentation."""
        try:
            # Get the latest version from npm registry
            response = await self.http_client.get(
                f"https://registry.npmjs.org/{package_name}",
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            npm_data = cast(Dict[str, Any], response.json())
            
            # Extract relevant info
            latest_version = str(npm_data.get("dist-tags", {}).get("latest", ""))
            description = str(npm_data.get("description", ""))
            
            # Extract homepage and documentation URLs
            homepage = str(npm_data.get("homepage", f"https://www.npmjs.com/package/{package_name}"))
            documentation_url = npm_data.get("documentation") or homepage
            repository = npm_data.get("repository", {})
            github_url = None
            
            # Extract GitHub URL if available
            if isinstance(repository, dict):
                repo_url = repository.get("url", "")
                if "github.com" in repo_url:
                    github_url = repo_url.replace("git+", "").replace(".git", "")
            elif isinstance(repository, str) and "github.com" in repository:
                github_url = repository.replace("git+", "").replace(".git", "")
            
            # Try to find API docs
            api_docs_url = None
            if github_url:
                api_docs_url = f"{github_url}/blob/main/API.md"
            
            # Extract release date
            release_date = None
            if latest_version and "time" in npm_data:
                release_date = npm_data["time"].get(latest_version)
            
            # Check current version
            current_version = version or latest_version
            is_outdated = self._compare_versions(current_version, latest_version)
            
            # Check for security issues
            security_issues: List[Dict[str, Any]] = []
            
            return PackageInfo(
                name=package_name,
                current_version=current_version,
                latest_version=latest_version,
                is_outdated=is_outdated,
                homepage=homepage,
                description=description,
                release_date=release_date,
                security_issues=security_issues,
                documentation_url=documentation_url,
                api_docs_url=api_docs_url,
                mypy_stub_url=None,
                github_url=github_url
            )
        except Exception as e:
            logger.error(f"Error checking npm package {package_name}: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error checking npm package {package_name}: {str(e)}"
            )
    
    async def check_python_file(self, file_path: str) -> List[PackageInfo]:
        """Check Python requirements file for package updates."""
        try:
            if not os.path.exists(file_path):
                raise McpError(
                    ErrorCode.TOOL_EXECUTION_ERROR,
                    f"File not found: {file_path}"
                )
            
            # Determine file type and parse accordingly
            packages: List[Tuple[str, Optional[str]]] = []
            
            if file_path.endswith(".txt"):
                # Parse requirements.txt
                with open(file_path, "r") as f:
                    for line in f.readlines():
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        
                        # Handle different requirements formats
                        if "==" in line:
                            # Exact version: package==1.0.0
                            parts = line.split("==")
                            package_name = parts[0].strip()
                            version = parts[1].strip() if len(parts) > 1 else None
                            packages.append((package_name, version))
                        elif ">=" in line:
                            # Minimum version: package>=1.0.0
                            parts = line.split(">=")
                            package_name = parts[0].strip()
                            version = parts[1].strip() if len(parts) > 1 else None
                            packages.append((package_name, version))
                        elif "~=" in line:
                            # Compatible release: package~=1.0.0
                            parts = line.split("~=")
                            package_name = parts[0].strip()
                            version = parts[1].strip() if len(parts) > 1 else None
                            packages.append((package_name, version))
                        else:
                            # No version specified
                            package_name = line.split("[")[0].strip() if "[" in line else line
                            packages.append((package_name, None))
            
            elif file_path.endswith(".toml"):
                # Parse pyproject.toml
                try:
                    import tomllib
                except ImportError:
                    import tomli as tomllib
                
                with open(file_path, "rb") as f:
                    toml_data = tomllib.load(f)
                
                # Check various potential locations for dependencies
                dependencies = []
                
                # Poetry style
                if "tool" in toml_data and "poetry" in toml_data["tool"]:
                    poetry_deps = toml_data["tool"]["poetry"].get("dependencies", {})
                    if isinstance(poetry_deps, dict):
                        for package, version in poetry_deps.items():
                            if package != "python":
                                if isinstance(version, str):
                                    dependencies.append((package, version))
                                else:
                                    dependencies.append((package, None))
                
                # PEP 621 style
                elif "project" in toml_data:
                    project_deps = toml_data["project"].get("dependencies", [])
                    for dep in project_deps:
                        if isinstance(dep, str):
                            if "==" in dep:
                                parts = dep.split("==")
                                package_name = parts[0].strip()
                                version = parts[1].strip() if len(parts) > 1 else None
                                dependencies.append((package_name, version))
                            else:
                                package_name = dep.split("[")[0].strip() if "[" in dep else dep
                                dependencies.append((package_name, None))
                
                # Add dependencies from various locations
                for dep in dependencies:
                    packages.append(dep)
            
            # Check each package
            results: List[PackageInfo] = []
            for package_name, version in packages:
                try:
                    package_info = await self.check_python_package(package_name, version)
                    results.append(package_info)
                except Exception as e:
                    logger.warning(f"Error checking {package_name}: {str(e)}")
            
            return results
        
        except Exception as e:
            logger.error(f"Error checking Python file {file_path}: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error checking Python file {file_path}: {str(e)}"
            )
    
    async def check_npm_file(self, file_path: str) -> List[PackageInfo]:
        """Check npm package.json file for package updates."""
        try:
            if not os.path.exists(file_path):
                raise McpError(
                    ErrorCode.TOOL_EXECUTION_ERROR,
                    f"File not found: {file_path}"
                )
            
            # Parse package.json
            with open(file_path, "r") as f:
                pkg_data = json.load(f)
            
            # Extract dependencies
            dependencies = {}
            dependencies.update(pkg_data.get("dependencies", {}))
            dependencies.update(pkg_data.get("devDependencies", {}))
            
            # Check each package
            results: List[PackageInfo] = []
            for package_name, version_str in dependencies.items():
                try:
                    # Extract version without range specifiers
                    version = None
                    if version_str:
                        version_match = re.search(r'[\d.]+', version_str)
                        if version_match:
                            version = version_match.group(0)
                    
                    package_info = await self.check_npm_package(package_name, version)
                    results.append(package_info)
                except Exception as e:
                    logger.warning(f"Error checking {package_name}: {str(e)}")
            
            return results
        
        except Exception as e:
            logger.error(f"Error checking npm file {file_path}: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error checking npm file {file_path}: {str(e)}"
            )
    
    async def run_mypy(self, file_path: str) -> MypyResult:
        """Run mypy type checker on a Python file or directory."""
        try:
            if not os.path.exists(file_path):
                raise McpError(
                    ErrorCode.TOOL_EXECUTION_ERROR,
                    f"File or directory not found: {file_path}"
                )
            
            # Run mypy command
            cmd = ["mypy", "--no-color-output", file_path]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout_bytes, stderr_bytes = await proc.communicate()
            stdout = stdout_bytes.decode("utf-8") if stdout_bytes else ""
            stderr = stderr_bytes.decode("utf-8") if stderr_bytes else ""
            
            # Process mypy output
            issues: List[MypyIssue] = []
            
            if stdout:
                for line in stdout.splitlines():
                    # Match pattern: file:line: error: message
                    issue_match = re.match(r'(.+?):(\d+):(?:\d+:)?\s+(\w+):\s+(.+)', line)
                    if issue_match:
                        file, line_num, issue_type, message = issue_match.groups()
                        issues.append(MypyIssue(
                            file=file,
                            line=int(line_num),
                            type=issue_type,
                            message=message
                        ))
            
            return MypyResult(
                success=proc.returncode == 0,
                issues=issues,
                exit_code=proc.returncode or 0
            )
            
        except Exception as e:
            logger.error(f"Error running mypy: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error running mypy: {str(e)}"
            )
    
    async def run_npm_audit(self, file_path: str) -> NpmAuditResult:
        """Run npm audit on a package.json file."""
        try:
            if not os.path.exists(file_path):
                raise McpError(
                    ErrorCode.TOOL_EXECUTION_ERROR,
                    f"File not found: {file_path}"
                )
            
            # Get project directory
            project_dir = os.path.dirname(os.path.abspath(file_path))
            
            # Run npm audit
            cmd = ["npm", "audit", "--json"]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout_bytes, stderr_bytes = await proc.communicate()
            stdout = stdout_bytes.decode("utf-8") if stdout_bytes else ""
            
            if stdout:
                # Parse npm audit output
                audit_data = json.loads(stdout)
                return NpmAuditResult(
                    success=proc.returncode == 0,
                    vulnerabilities=audit_data.get("vulnerabilities", {}),
                    metadata=audit_data.get("metadata", {}),
                    exit_code=proc.returncode or 0
                )
            else:
                raise McpError(
                    ErrorCode.TOOL_EXECUTION_ERROR,
                    f"No output from npm audit: {stderr_bytes.decode('utf-8') if stderr_bytes else 'unknown error'}"
                )
        except Exception as e:
            logger.error(f"Error running npm audit: {str(e)}")
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error running npm audit: {str(e)}"
            )
    
    def _compare_versions(self, current: str, latest: str) -> bool:
        """Compare versions to determine if outdated."""
        if current == latest:
            return False
        
        # Split into release and prerelease parts
        current_release, current_prerelease = self._split_version(current)
        latest_release, latest_prerelease = self._split_version(latest)
        
        # Compare release versions first
        release_comparison = self._compare_release_versions(current_release, latest_release)
        
        # If release versions are equal, compare prerelease designations
        if release_comparison == 0:
            # If current has a prerelease but latest doesn't, current is outdated
            if current_prerelease and not latest_prerelease:
                return True
            # If current doesn't have a prerelease but latest does, current is NOT outdated
            elif not current_prerelease and latest_prerelease:
                return False
            # If both have prereleases, compare them alphabetically
            elif current_prerelease and latest_prerelease:
                return current_prerelease < latest_prerelease
            # If neither has a prerelease, they are equal (not outdated)
            else:
                return False
        
        # Return based on release version comparison
        return release_comparison < 0
        
    def _split_version(self, version: str) -> tuple[str, str]:
        """Split version into release and prerelease parts."""
        # Check for prerelease designation patterns
        match = re.match(r'^([0-9.]+)[-.]?(.+)?$', version)
        if match:
            release, prerelease = match.groups()
            return release, prerelease or ""
        return version, ""

    def _compare_release_versions(self, current: str, latest: str) -> int:
        """Compare release versions and return -1 (outdated), 0 (equal), 1 (newer)."""
        # Parse versions for comparison
        current_parts = [int(part) for part in re.findall(r'\d+', current)]
        latest_parts = [int(part) for part in re.findall(r'\d+', latest)]
        
        # Pad shorter list
        while len(current_parts) < len(latest_parts):
            current_parts.append(0)
        while len(latest_parts) < len(current_parts):
            latest_parts.append(0)
        
        # Compare parts
        for c, l in zip(current_parts, latest_parts):
            if c < l:
                return -1
            elif c > l:
                return 1
        
        return 0
    
    async def close(self) -> None:
        """Close resources."""
        await self.http_client.aclose()
