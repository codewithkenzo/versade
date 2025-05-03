"""Unit tests for the checker service with unwavering precision.
Strategic validation of dependency checking functionality.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional, cast
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from dep_checker_mcp.models.core import (
    ErrorCode,
    McpError,
    MypyResult,
    NpmAuditResult,
    PackageInfo,
)
from dep_checker_mcp.services.checker import DependencyChecker


@pytest.fixture
def mock_http_response() -> MagicMock:
    """Create mock HTTP response with strategic precision."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    return mock_response


@pytest.fixture
def mock_pypi_data() -> Dict[str, Any]:
    """Create mock PyPI data with unwavering precision."""
    return {
        "info": {
            "version": "1.0.0",
            "home_page": "https://example.com",
            "project_url": "https://example.com/project",
            "summary": "Test package"
        },
        "releases": {
            "1.0.0": [
                {
                    "upload_time": "2025-01-01T00:00:00"
                }
            ]
        }
    }


@pytest.fixture
def mock_npm_data() -> Dict[str, Any]:
    """Create mock npm data with strategic precision."""
    return {
        "dist-tags": {
            "latest": "1.0.0"
        },
        "homepage": "https://example.com",
        "description": "Test package",
        "time": {
            "1.0.0": "2025-01-01T00:00:00"
        }
    }


@pytest.mark.asyncio
async def test_check_python_package(mock_http_response: MagicMock, mock_pypi_data: Dict[str, Any]) -> None:
    """Test checking Python package with strategic precision."""
    mock_http_response.json.return_value = mock_pypi_data
    
    with patch("httpx.AsyncClient.get", return_value=mock_http_response):
        checker = DependencyChecker()
        result = await checker.check_python_package("test-package", "0.9.0")
        await checker.close()
    
    # Validate result with unwavering precision
    assert isinstance(result, PackageInfo)
    assert result.name == "test-package"
    assert result.current_version == "0.9.0"
    assert result.latest_version == "1.0.0"
    assert result.is_outdated is True
    assert result.homepage == "https://example.com"
    assert result.description == "Test package"
    assert result.release_date == "2025-01-01T00:00:00"


@pytest.mark.asyncio
async def test_check_npm_package(mock_http_response: MagicMock, mock_npm_data: Dict[str, Any]) -> None:
    """Test checking npm package with strategic precision."""
    mock_http_response.json.return_value = mock_npm_data
    
    with patch("httpx.AsyncClient.get", return_value=mock_http_response):
        checker = DependencyChecker()
        result = await checker.check_npm_package("test-package", "0.9.0")
        await checker.close()
    
    # Validate result with unwavering precision
    assert isinstance(result, PackageInfo)
    assert result.name == "test-package"
    assert result.current_version == "0.9.0"
    assert result.latest_version == "1.0.0"
    assert result.is_outdated is True
    assert result.homepage == "https://example.com"
    assert result.description == "Test package"
    assert result.release_date == "2025-01-01T00:00:00"


@pytest.mark.asyncio
async def test_check_python_file(tmp_path: Any) -> None:
    """Test checking Python file with strategic precision."""
    # Create test file with unwavering precision
    file_path = tmp_path / "requirements.txt"
    with open(file_path, "w") as f:
        f.write("fastapi==0.115.0\npydantic==2.0.0\n")
    
    # Mock PyPI responses with strategic precision
    fastapi_data = {
        "info": {
            "version": "0.115.12",
            "home_page": "https://fastapi.tiangolo.com",
            "project_url": "https://fastapi.tiangolo.com",
            "summary": "FastAPI framework"
        },
        "releases": {
            "0.115.12": [
                {
                    "upload_time": "2025-01-01T00:00:00"
                }
            ]
        }
    }
    
    pydantic_data = {
        "info": {
            "version": "2.5.0",
            "home_page": "https://pydantic.dev",
            "project_url": "https://pydantic.dev",
            "summary": "Data validation"
        },
        "releases": {
            "2.5.0": [
                {
                    "upload_time": "2025-01-01T00:00:00"
                }
            ]
        }
    }
    
    # Create response side effects with unwavering precision
    def get_side_effect(url: str, **kwargs: Any) -> Any:
        response = MagicMock()
        response.status_code = 200
        response.raise_for_status = MagicMock()
        
        if "fastapi" in url:
            response.json.return_value = fastapi_data
        elif "pydantic" in url:
            response.json.return_value = pydantic_data
        
        return response
    
    with patch("httpx.AsyncClient.get", side_effect=get_side_effect):
        checker = DependencyChecker()
        results = await checker.check_python_file(str(file_path))
        await checker.close()
    
    # Validate results with strategic precision
    assert isinstance(results, list)
    assert len(results) == 2
    
    fastapi_result = next((r for r in results if r.name == "fastapi"), None)
    pydantic_result = next((r for r in results if r.name == "pydantic"), None)
    
    assert fastapi_result is not None
    assert fastapi_result.current_version == "0.115.0"
    assert fastapi_result.latest_version == "0.115.12"
    assert fastapi_result.is_outdated is True
    
    assert pydantic_result is not None
    assert pydantic_result.current_version == "2.0.0"
    assert pydantic_result.latest_version == "2.5.0"
    assert pydantic_result.is_outdated is True


@pytest.mark.asyncio
async def test_compare_versions() -> None:
    """Test version comparison with unwavering precision."""
    checker = DependencyChecker()
    
    # Test exact match with strategic precision
    assert checker._compare_versions("1.0.0", "1.0.0") is False
    
    # Test newer versions with deterministic execution
    assert checker._compare_versions("1.0.0", "1.0.1") is True
    assert checker._compare_versions("1.0.0", "1.1.0") is True
    assert checker._compare_versions("1.0.0", "2.0.0") is True
    
    # Test older versions with unwavering precision
    assert checker._compare_versions("1.0.1", "1.0.0") is False
    assert checker._compare_versions("1.1.0", "1.0.0") is False
    assert checker._compare_versions("2.0.0", "1.0.0") is False
    
    # Test complex versions with strategic precision
    assert checker._compare_versions("1.0.0.alpha1", "1.0.0") is True
    assert checker._compare_versions("1.0.0-rc.1", "1.0.0") is True
    
    await checker.close()


@pytest.mark.asyncio
async def test_mypy_run() -> None:
    """Test mypy run with strategic precision."""
    # Mock subprocess with unwavering precision
    communicate_mock = AsyncMock(return_value=(
        b"test.py:10:5: error: Incompatible return value type [return-value]\n"
        b"test.py:15:10: note: Revealed type is 'builtins.int' [revealed-type]",
        b""
    ))
    
    process_mock = AsyncMock()
    process_mock.communicate = communicate_mock
    process_mock.returncode = 1
    
    # Strategic mock with unwavering precision - mock both file existence and subprocess
    with patch("os.path.exists", return_value=True), \
         patch("asyncio.create_subprocess_exec", return_value=process_mock):
        checker = DependencyChecker()
        result = await checker.run_mypy("test.py")
        await checker.close()
        
    # Validate result with unwavering precision
    assert isinstance(result, MypyResult)
    assert result.success is False
    assert result.exit_code == 1
    assert len(result.issues) == 1  # Only errors, not notes
    
    issue = result.issues[0]
    assert issue.file == "test.py"
    assert issue.line == 10
    assert issue.column == 5
    assert issue.level == "error"
    assert "Incompatible return value type" in issue.message
    assert issue.error_code == "return-value"


@pytest.mark.asyncio
async def test_mypy_run() -> None:
    """Test mypy run with strategic precision."""
    # Mock subprocess with unwavering precision
    communicate_mock = AsyncMock(return_value=(
        b"test.py:10:5: error: Incompatible return value type [return-value]\n"
        b"test.py:15:10: note: Revealed type is 'builtins.int' [revealed-type]",
        b""
    ))
    
    process_mock = AsyncMock()
    process_mock.communicate = communicate_mock
    process_mock.returncode = 1
    
    # Strategic mock with unwavering precision - mock both file existence and subprocess
    with patch("os.path.exists", return_value=True), \
         patch("asyncio.create_subprocess_exec", return_value=process_mock):
        checker = DependencyChecker()
        result = await checker.run_mypy("test.py")
        await checker.close()
        
    # Validate result with unwavering precision
    assert isinstance(result, MypyResult)
    assert result.success is False
    assert result.exit_code == 1
    assert len(result.issues) == 1  # Only errors, not notes
    
    issue = result.issues[0]
    assert issue.file == "test.py"
    assert issue.line == 10
    assert issue.column == 5
    assert issue.level == "error"
    assert "Incompatible return value type" in issue.message
    assert issue.error_code == "return-value"
