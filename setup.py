"""
Strategic setup script for Versade MCP server.
Enables standardized deployment with uwx/npx integration.
"""

from setuptools import setup, find_packages

setup(
    name="versade-mcp",
    version="1.0.0",
    description="Versade MCP Server for package dependency analysis",
    author="Versade Team",
    author_email="info@versade.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "fastapi>=0.115.0,<0.116.0",
        "uvicorn>=0.28.0,<0.29.0",
        "orjson>=3.10.0,<3.11.0",
        "httpx>=0.27.0,<0.28.0",
        "sse-starlette>=1.6.0",
        "anyio>=4.0.0",
        "pydantic>=2.7.0"
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "versade-mcp=versade.standard_mcp:main",
            "versade=versade.server:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
