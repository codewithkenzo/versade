"""
Core models for dependency checking with unwavering precision.
Provides deterministic data structures with strategic type safety.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class ErrorCode(str, Enum):
    """MCP protocol error codes with deterministic values."""
    INTERNAL_ERROR = "internal_error"
    INVALID_REQUEST = "invalid_request"
    INVALID_PARAMS = "invalid_params"
    TOOL_NOT_FOUND = "tool_not_found"
    TOOL_EXECUTION_ERROR = "tool_execution_error"


class McpError(Exception):
    """Strategic error handling for MCP protocol."""
    def __init__(self, code: ErrorCode, message: str) -> None:
        self.code: ErrorCode = code
        self.message: str = message
        super().__init__(message)


@dataclass
class PackageInfo:
    """Package information with complete version and documentation details."""
    name: str
    current_version: str
    latest_version: str
    is_outdated: bool
    homepage: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[str] = None
    security_issues: List[Dict[str, Any]] = field(default_factory=list)
    documentation_url: Optional[str] = None
    api_docs_url: Optional[str] = None
    mypy_stub_url: Optional[str] = None
    github_url: Optional[str] = None


@dataclass
class MypyIssue:
    """Type checking issue with strategic precision."""
    file: str
    line: int
    column: int
    level: str
    message: str
    error_code: str


@dataclass
class MypyResult:
    """Result of mypy type checking with unwavering precision."""
    success: bool
    issues: List[MypyIssue]
    exit_code: int


@dataclass
class NpmAuditVulnerability:
    """npm audit vulnerability with deterministic structure."""
    severity: str
    name: str
    version: str
    url: Optional[str] = None
    title: Optional[str] = None
    recommendation: Optional[str] = None


@dataclass
class NpmAuditResult:
    """Result of npm audit with strategic precision."""
    success: bool
    vulnerabilities: Dict[str, Any]
    metadata: Dict[str, Any]
    exit_code: int


@dataclass
class McpRequest:
    """Core data models for Versa package version and documentation info."""
    id: str
    name: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class McpResponse:
    """MCP response with strategic type safety."""
    id: str
    result: Union[
        PackageInfo, 
        List[PackageInfo], 
        MypyResult, 
        NpmAuditResult, 
        Dict[str, Any], 
        List[Dict[str, Any]]
    ]
    error: Optional[Dict[str, Any]] = None
