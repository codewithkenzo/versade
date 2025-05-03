text
# Versade

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/codewithkenzo/versade)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![Type Hints](https://img.shields.io/badge/type%20hints-100%25-brightgreen)](https://mypy.readthedocs.io/)
[![AUR](https://img.shields.io/badge/AUR-versade-blue)](https://aur.archlinux.org/packages/versade)

**Versade** is your all-in-one dependency version checker and documentation finder-built for LLMs, devs, and anyone who wants instant, precise answers about package versions, compatibility, and docs.

---

## 🚀 Why Versade?

- **Find the latest package versions and docs** for Python and npm in seconds.
- **Validate dependencies**: Check for updates, security issues, and type hint support.
- **Instant docs**: Get direct links to docs, API references, and GitHub repos.
- **Production-grade**: Async FastAPI backend, blazing orjson, 100% type-annotated, and tested.
- **Smithery MCP-ready**: Plug-and-play with your LLM or automation stack.

---

## 🛠️ Quick Start

pip install versade # or: uv pip install versade
versade # runs server on http://localhost:9373 (auto-picks port if busy)

text

Or spin up with Docker:

docker pull ghcr.io/codewithkenzo/versade:latest
docker run -d -p 9373:9373 --name versade-container versade:latest

text

---

## 🧩 Features

- **Python & npm version checks** (PyPI, npm registry)
- **Security vulnerability detection** (Python & npm)
- **Smart docs discovery**: Docs, API, GitHub, type stubs
- **File-based analysis**: requirements.txt, pyproject.toml, package.json
- **MCP tools**: Built-in endpoints for LLM automation
- **Arch Linux & AUR support**

---

## 🔎 Example Usage

**Python:**

versade mcp_check_python_package fastapi

text

**npm:**

versade mcp_check_npm_package react

text

**File analysis:**

versade mcp_check_python_file requirements.txt
versade mcp_check_npm_file package.json

text

---

## 🏗️ Architecture

versade/
├── api/ # FastAPI endpoints
├── models/ # Typed data models
├── services/ # Dependency & docs logic
├── utils/ # Utilities & config

text

---

## 📦 Installation

**PyPI:**

pip install versade

text

**AUR:**

yay -S versade

text

**From source:**

git clone https://github.com/codewithkenzo/versade.git
cd versade
pip install -e .

text

---

## 📝 Docs & MCP Integration

- [Full Documentation](https://github.com/codewithkenzo/versade/wiki)
- [Smithery MCP Registry](https://smithery.app/registry/versade)
- [Linear Project Board](https://linear.app/versade)

---

## 🤝 Contributing

Pull requests, issues, and feedback welcome!  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT

---

<p align="center"><b>Versade: Dependency clarity for humans and AIs. Built by Smithery, powered by the community.</b></p>
