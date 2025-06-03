# Versade

**Versatile dependency analysis and MCP server** - A modern tool for package version checking, security analysis, and dependency research with LLM integration.

## Features

- 🔍 **Package Analysis**: Check Python (pip) and npm package versions and security
- 🚀 **FastAPI Server**: HTTP/SSE endpoints for real-time dependency analysis
- 🧠 **Research Integration**: Deep package research using Perplexity API
- 🔌 **MCP Server**: Model Context Protocol server for LLM integration
- 📊 **Batch Processing**: Queue and process large dependency lists
- 🎨 **Rich CLI**: Beautiful command-line interface with subcommands
- ⚡ **Multiple Transports**: stdio and SSE transport modes
- 🔧 **Interactive Setup**: Plug-and-play configuration

## Quick Start

### Installation

#### Option 1: Quick Development Setup (Recommended)
```bash
# Clone and setup for development
git clone https://github.com/versade/versade
cd versade

# Quick setup with script
./dev-setup.sh

# Or manual setup
uv sync
uv run versade --help
```

#### Option 2: Automated Installation
```bash
# Use the installation script
python install.py

# Choose from:
# 1. uvx - Global install (PyPI only)
# 2. pipx - Global install 
# 3. pip - System/venv install
# 4. Development - Local setup (recommended)
# 5. Auto-detect - Best method
```

#### Option 3: Manual Methods

**pipx (Global install)**:
```bash
# From source
git clone https://github.com/versade/versade
cd versade
pipx install -e .

# From PyPI (when published)
pipx install versade
```

**pip (System/venv install)**:
```bash
# From source
git clone https://github.com/versade/versade
cd versade
pip install -e .

# From PyPI (when published)
pip install versade
```

**uvx (Global install from PyPI)**:
```bash
# Only works when published to PyPI
uvx install versade

# Or run directly without installing
uvx --from versade versade check requests numpy
```

### Basic Usage

```bash
# Interactive setup (optional)
versade setup

# Check Python packages
versade check requests numpy flask

# Check npm packages
versade check --npm express react lodash

# Start HTTP API server
versade serve --port 8000

# Start MCP server for LLM integration
versade mcp

# Research package security
versade research "security vulnerabilities in flask 2.3.0"
```

## CLI Commands

### Package Analysis
```bash
# Check Python packages
versade check requests numpy pandas
versade check --json requests  # JSON output

# Check npm packages  
versade check --npm express react vue
```

### HTTP API Server
```bash
# Start development server
versade serve --reload

# Production server
versade serve --host 0.0.0.0 --port 8000
```

### MCP Server
```bash
# Start MCP server (stdio mode)
versade mcp

# Start with SSE transport
versade mcp --transport sse
```

### Research
```bash
# Research package security (uses sonar-deep-research by default)
versade research "is requests library secure?"

# Research with custom API key
versade research "npm express vulnerabilities" --api-key YOUR_KEY

# Research with specific model
versade research "security analysis" --model sonar-reasoning-pro

# Available models:
# - sonar-deep-research (128k) - Best for comprehensive research (default)
# - sonar-reasoning-pro (128k) - Advanced reasoning capabilities
# - sonar-reasoning (128k) - Standard reasoning
# - sonar-pro (200k) - High-quality with large context
# - sonar (128k) - Standard model
# - r1-1776 (128k) - Specialized model
```

### Setup
```bash
# Interactive configuration
versade setup

# Force reconfiguration
versade setup --force
```

## HTTP API Endpoints

### Real-time Analysis (SSE)
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "dependencies": ["requests", "numpy", "flask"],
    "package_manager": "pip"
  }'
```

### Batch Processing
```bash
# Queue a job
curl -X POST "http://localhost:8000/queue" \
  -H "Content-Type: application/json" \
  -d '{
    "dependencies": ["express", "react", "lodash"],
    "package_manager": "npm"
  }'

# Check job status
curl "http://localhost:8000/queue/{job_id}"
```

### Research
```bash
# Single research query
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "security issues with flask framework",
    "model": "sonar-pro"
  }'

# Batch research (uses sonar-deep-research by default)
curl -X POST "http://localhost:8000/research/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "security vulnerabilities in requests library",
      "best practices for flask security",
      "npm package security scanning"
    ],
    "model": "sonar-deep-research"
  }'
```

## MCP Integration

### Cursor/Windsurf Integration

1. **Install with uvx**:
   ```bash
   uvx install versade
   ```

2. **Add to MCP config** (`mcp-config.json`):
   ```json
   {
     "mcpServers": {
       "versade": {
         "command": "uvx",
         "args": ["--from", "versade", "versade", "mcp"],
         "env": {
           "VERSADE_LOG_LEVEL": "INFO",
           "VERSADE_TRANSPORT_MODE": "stdio"
         }
       }
     }
   }
   ```

3. **Restart Cursor/Windsurf** and use Versade tools in your LLM conversations.

### Available MCP Tools

- `check_python_package`: Analyze Python package versions and security
- `check_npm_package`: Analyze npm package versions and security  
- `analyze_dependencies`: Batch analyze multiple packages

## Configuration

### Environment Variables

```bash
# Perplexity API key for research features
PERPLEXITY_API_KEY=your_api_key_here

# Log level
VERSADE_LOG_LEVEL=INFO

# Default transport mode
VERSADE_TRANSPORT_MODE=stdio
```

### Config File

Run `versade setup` for interactive configuration, or create `~/.versade/config.env`:

```env
PERPLEXITY_API_KEY=your_key_here
VERSADE_LOG_LEVEL=INFO
VERSADE_TRANSPORT_MODE=stdio
```

## API Documentation

When running the HTTP server, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Setup
```bash
git clone https://github.com/versade/versade
cd versade
uv sync
```

### Run Tests
```bash
uv run pytest
```

### Type Checking
```bash
uv run mypy src/
```

### Development Server
```bash
# CLI development
uv run python -m versade.cli check requests

# API development  
uv run python -m versade.api.app

# MCP development
uv run python -m versade.server
```

## Architecture

```
src/versade/
├── api/           # FastAPI HTTP/SSE endpoints
├── models/        # Pydantic data models
├── services/      # Business logic (research, analysis)
├── utils/         # Utility functions
├── cli.py         # Command-line interface
├── config.py      # Configuration management
└── server.py      # MCP server implementation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run type checking and tests
6. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/versade/versade/issues)
- **Discussions**: [GitHub Discussions](https://github.com/versade/versade/discussions)
- **Documentation**: [Wiki](https://github.com/versade/versade/wiki)
