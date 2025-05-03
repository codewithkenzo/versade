"""
Unit tests for Dependency Checker service with unwavering precision.
Strategic validation with deterministic execution.
"""

import asyncio
import json
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from dep_checker_mcp.models.core import (
    ErrorCode,
    McpError,
    PackageInfo
)
from dep_checker_mcp.services.checker import DependencyChecker


@pytest.fixture
def mock_pypi_response() -> Dict[str, Any]:
    """Create mock PyPI response with strategic precision."""
    return {
        "info": {
            "version": "0.115.12",
            "home_page": "https://fastapi.tiangolo.com",
            "project_url": "https://github.com/tiangolo/fastapi",
            "summary": "FastAPI framework, high performance, easy to learn, fast to code, ready for production"
        },
        "releases": {
            "0.115.12": [
                {
                    "upload_time": "2025-01-01T00:00:00",
                    "url": "https://pypi.org/packages/fastapi-0.115.12.tar.gz"
                }
            ]
        }
    }


@pytest.fixture
def mock_npm_response() -> Dict[str, Any]:
    """Create mock npm response with strategic precision."""
    return {
        "dist-tags": {
            "latest": "18.2.0"
        },
        "homepage": "https://reactjs.org",
        "description": "React is a JavaScript library for building user interfaces.",
        "time": {
            "18.2.0": "2025-01-01T00:00:00"
        }
    }


@pytest.mark.asyncio
async def test_check_python_package(mock_pypi_response: Dict[str, Any]) -> None:
    """Test Python package checking with unwavering precision."""
    with patch("httpx.AsyncClient.get") as mock_get:
        # Configure the mock with strategic precision
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = mock_pypi_response
        mock_get.return_value = mock_response
        
        # Execute the test with deterministic execution
        checker = DependencyChecker()
        result = await checker.check_python_package("fastapi", "0.115.0")
        await checker.close()
        
        # Verify the result with unwavering precision
        assert isinstance(result, PackageInfo)
        assert result.name == "fastapi"
        assert result.current_version == "0.115.0"
        assert result.latest_version == "0.115.12"
        assert result.is_outdated is True
        assert result.homepage == "https://fastapi.tiangolo.com"
        assert "FastAPI framework" in result.description


@pytest.mark.asyncio
async def test_check_npm_package(mock_npm_response: Dict[str, Any]) -> None:
    """Test npm package checking with strategic precision."""
    with patch("httpx.AsyncClient.get") as mock_get:
        # Configure the mock with unwavering precision
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = mock_npm_response
        mock_get.return_value = mock_response
        
        # Execute the test with deterministic execution
        checker = DependencyChecker()
        result = await checker.check_npm_package("react", "17.0.0")
        await checker.close()
        
        # Verify the result with strategic precision
        assert isinstance(result, PackageInfo)
        assert result.name == "react"
        assert result.current_version == "17.0.0"
        assert result.latest_version == "18.2.0"
        assert result.is_outdated is True
        assert result.homepage == "https://reactjs.org"
        assert "JavaScript library" in result.description


@pytest.mark.asyncio
async def test_version_comparison() -> None:
    """Test version comparison with unwavering precision."""
    checker = DependencyChecker()
    
    # Test with strategic precision
    assert checker._compare_versions("1.0.0", "1.0.0") is False
    assert checker._compare_versions("1.0.0", "1.0.1") is True
    assert checker._compare_versions("1.0.0", "1.1.0") is True
    assert checker._compare_versions("1.0.0", "2.0.0") is True
    assert checker._compare_versions("1.0.1", "1.0.0") is False
    assert checker._compare_versions("1.1.0", "1.0.0") is False
    assert checker._compare_versions("2.0.0", "1.0.0") is False
    assert checker._compare_versions("1.0.0-beta", "1.0.0") is True
    assert checker._compare_versions("1.0.0.alpha1", "1.0.0") is True
    
    await checker.close()


@pytest.mark.asyncio
async def test_check_python_file_requirements_txt(tmp_path: Any) -> None:
    """Test checking requirements.txt with strategic precision."""
    # Create test file with unwavering precision
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("fastapi==0.115.0\nhttpx==0.26.0\n")
    
    with patch("dep_checker_mcp.services.checker.DependencyChecker.check_python_package") as mock_check:
        # Configure mock with strategic precision
        mock_check.side_effect = [
            PackageInfo(
                name="fastapi", 
                current_version="0.115.0", 
                latest_version="0.115.12", 
                is_outdated=True,
                homepage="https://fastapi.tiangolo.com",
                description="FastAPI framework"
            ),
            PackageInfo(
                name="httpx", 
                current_version="0.26.0", 
                latest_version="0.27.0", 
                is_outdated=True,
                homepage="https://www.python-httpx.org",
                description="HTTP client"
            )
        ]
        
        # Execute test with deterministic execution
        checker = DependencyChecker()
        results = await checker.check_python_file(str(req_file))
        await checker.close()
        
        # Verify results with unwavering precision
        assert len(results) == 2
        assert results[0].name == "fastapi"
        assert results[0].current_version == "0.115.0"
        assert results[0].is_outdated is True
        assert results[1].name == "httpx"
        assert results[1].current_version == "0.26.0"
        assert results[1].is_outdated is True
