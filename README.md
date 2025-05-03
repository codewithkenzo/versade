# Versade

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/codewithkenzo/versade)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![AUR](https://img.shields.io/badge/AUR-versade-blue)](https://aur.archlinux.org/packages/versade)

**Versade** is your no-nonsense dependency and docs checker, built for LLMs, devs, and automation. Instantly find the latest package versions, compatibility, and docs-no more mismatches or guesswork.

---

## 🚀 Features

- **Python & npm version checks**  
- **Security & type safety audits**  
- **Docs, API, and repo links-auto-discovered**  
- **File-based analysis**: requirements.txt, pyproject.toml, package.json  
- **FastAPI backend, async, 100% type-annotated**  
- **MCP server: plug into Smithery or your LLM stack**  
- **AUR & pip install ready**

---

## ⚡ Quick Start

```bash
# Install with pip
pip install versade

# Run the server
versade # runs at http://localhost:9373 (auto-picks port if busy)
```

Or use Docker:

```bash
docker run -d -p 9373:9373 ghcr.io/codewithkenzo/versade:latest
```

---

## 🛠️ MCP Tools

- `mcp_check_python_package`  
- `mcp_check_npm_package`  
- `mcp_check_python_file`  
- `mcp_check_npm_file`  
- `mcp_run_mypy`  
- `mcp_run_npm_audit`

---

## 📖 Docs & Integration

- [Full Documentation](https://github.com/codewithkenzo/versade/wiki)
- [Smithery MCP Registry](https://smithery.app/registry/versade)
- [AUR Package](https://aur.archlinux.org/packages/versade)

---

## 🤝 Contributing

PRs, issues, and ideas welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

**Versade: Dependency clarity for humans and AIs. Built by Smithery, powered by the community.**
