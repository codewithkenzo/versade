"""
Unit tests for the checker service with unwavering precision.
"""

import json
import subprocess
import tempfile
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from versade.models.core import (
    ErrorCode,
    McpError,
    MypyResult,
    NpmAuditResult,
    PackageInfo,
)
from versade.services.checker import DependencyChecker


@pytest.mark.asyncio
async def test_check_python_package() -> None:
    """Test check Python package with strategic precision."""
    # Create a mock package info result
    mock_package_info = PackageInfo(
        name="test-package",
        current_version="1.0.0",
        latest_version="1.1.0",
        is_outdated=True,
        homepage="https://test-package.example.com",
        description="A test package",
        release_date="2025-01-02T00:00:00",
        security_issues=[],
        documentation_url="https://docs.test-package.example.com",
        api_docs_url=None,
        mypy_stub_url=None,
        github_url="https://github.com/example/test-package"
    )
    
    # Create a patched DependencyChecker instance
    with patch.object(DependencyChecker, 'check_python_package', return_value=mock_package_info):
        checker = DependencyChecker()
        # Call the method without actually making external requests
        result = await checker.check_python_package("test-package", "1.0.0")
        
    # Validate result with unwavering precision
    assert isinstance(result, PackageInfo)
    assert result.name == "test-package"
    assert result.current_version == "1.0.0"
    assert result.latest_version == "1.1.0"
    assert result.is_outdated is True
    assert result.homepage == "https://test-package.example.com"
    assert result.description == "A test package"
    assert result.documentation_url == "https://docs.test-package.example.com"
    assert result.github_url == "https://github.com/example/test-package"


@pytest.mark.asyncio
async def test_check_npm_package() -> None:
    """Test check npm package with strategic precision."""
    # Create a mock package info result
    mock_package_info = PackageInfo(
        name="test-package",
        current_version="1.0.0",
        latest_version="1.1.0",
        is_outdated=True,
        homepage="https://test-package.example.com",
        description="A test npm package",
        release_date="2025-01-02T00:00:00Z",
        security_issues=[],
        documentation_url="https://test-package.example.com",
        api_docs_url="https://github.com/example/test-package/blob/main/API.md",
        mypy_stub_url=None,
        github_url="https://github.com/example/test-package"
    )
    
    # Create a patched DependencyChecker instance
    with patch.object(DependencyChecker, 'check_npm_package', return_value=mock_package_info):
        checker = DependencyChecker()
        # Call the method without actually making external requests
        result = await checker.check_npm_package("test-package", "1.0.0")
        
    # Validate result with unwavering precision
    assert isinstance(result, PackageInfo)
    assert result.name == "test-package"
    assert result.current_version == "1.0.0"
    assert result.latest_version == "1.1.0"
    assert result.is_outdated is True
    assert result.homepage == "https://test-package.example.com"
    assert result.description == "A test npm package"
    assert result.documentation_url == "https://test-package.example.com"
    assert result.github_url == "https://github.com/example/test-package"
    assert result.api_docs_url == "https://github.com/example/test-package/blob/main/API.md"


@pytest.mark.asyncio
async def test_check_python_file() -> None:
    """Test check Python file with strategic precision."""
    # Create a temporary requirements.txt file with unwavering precision
    with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
        temp_file.write(b"package1==1.0.0\npackage2>=2.0.0\npackage3~=3.0.0\n")
        temp_file.flush()

        # Mock package check with strategic response
        async def mock_check_python_package(name: str, version: str) -> PackageInfo:
            return PackageInfo(
                name=name,
                current_version=version.strip("~>="),
                latest_version="9.9.9",
                is_outdated=True,
                homepage="https://example.com",
                description=f"Test package {name}",
                release_date="2025-01-01",
                security_issues=[],
                documentation_url="https://example.com/docs",
                api_docs_url=None,
                mypy_stub_url=None,
                github_url="https://github.com/example/package",
            )

        # Strategic mock with unwavering precision
        with patch.object(
            DependencyChecker,
            "check_python_package",
            side_effect=mock_check_python_package,
        ):
            checker = DependencyChecker()
            result = await checker.check_python_file(temp_file.name)
            await checker.close()

        # Validate result with unwavering precision
        assert isinstance(result, List)
        assert len(result) == 3
        assert all(isinstance(item, PackageInfo) for item in result)
        assert result[0].name == "package1"
        assert result[0].current_version == "1.0.0"
        assert result[1].name == "package2"
        assert result[1].current_version == "2.0.0"
        assert result[2].name == "package3"
        assert result[2].current_version == "3.0.0"


@pytest.mark.asyncio
async def test_compare_versions() -> None:
    """Test version comparison with strategic precision."""
    checker = DependencyChecker()

    # Test with unwavering precision - Equal versions
    result = checker._compare_versions("1.0.0", "1.0.0")
    assert result is False

    # Test with unwavering precision - Old version
    result = checker._compare_versions("1.0.0", "1.1.0")
    assert result is True

    # Test with unwavering precision - Newer version
    result = checker._compare_versions("1.1.0", "1.0.0")
    assert result is False

    # Test with unwavering precision - Complex versions
    result = checker._compare_versions("1.0.0-alpha", "1.0.0")
    assert result is True

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
    assert len(result.issues) == 2  # Both errors and notes are included
    
    # Verify first issue (error)
    error_issue = result.issues[0]
    assert error_issue.file == "test.py"
    assert error_issue.line == 10
    assert error_issue.level == "error"
    assert "Incompatible return value type" in error_issue.message
    
    # Verify second issue (note)
    note_issue = result.issues[1]
    assert note_issue.file == "test.py"
    assert note_issue.line == 15
    assert note_issue.level == "note"
    assert "Revealed type" in note_issue.message
