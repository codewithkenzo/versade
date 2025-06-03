#!/usr/bin/env python3
"""
Versade Installation Script
Automatically detects and uses the best installation method.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Tuple

def run_command(cmd: List[str], capture_output: bool = True) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(
            cmd, 
            capture_output=capture_output, 
            text=True, 
            check=False
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def check_command_exists(command: str) -> bool:
    """Check if a command exists in PATH."""
    return shutil.which(command) is not None

def detect_package_manager() -> Optional[str]:
    """Detect the best available package manager."""
    managers = [
        ("uvx", "uvx"),
        ("pipx", "pipx"), 
        ("pip", "pip"),
        ("pip3", "pip3")
    ]
    
    for name, cmd in managers:
        if check_command_exists(cmd):
            return name
    
    return None

def install_with_uvx() -> bool:
    """Install using uvx."""
    print("🚀 Installing with uvx...")
    
    # For local development, uvx doesn't work well with local packages
    # Recommend using uv run instead
    if Path("pyproject.toml").exists():
        print("❌ uvx doesn't support local development installs well.")
        print("💡 For development, use: uv sync && uv run versade --help")
        print("💡 Or try option 4 (Development) from the menu.")
        return False
    
    # Try installing from PyPI (when published)
    print("Trying to install from PyPI...")
    success, output = run_command(["uvx", "install", "versade"])
    if success:
        print("✅ Successfully installed Versade from PyPI!")
        return True
    else:
        print(f"❌ uvx install from PyPI failed: {output}")
        print("Note: Package may not be published to PyPI yet.")
        print("💡 For local development, use option 4 (Development) instead.")
    
    return False

def install_with_pipx() -> bool:
    """Install using pipx."""
    print("📦 Installing with pipx...")
    
    if Path("pyproject.toml").exists():
        print("Installing from local project directory...")
        success, output = run_command(["pipx", "install", "-e", "."])
        if success:
            print("✅ Successfully installed Versade with pipx!")
            return True
        else:
            print(f"❌ pipx editable install failed: {output}")
            
            # Try non-editable install
            print("Trying non-editable install...")
            success, output = run_command(["pipx", "install", "."])
            if success:
                print("✅ Successfully installed Versade with pipx!")
                return True
            else:
                print(f"❌ pipx install failed: {output}")
    
    # Try installing from PyPI
    print("Trying to install from PyPI...")
    success, output = run_command(["pipx", "install", "versade"])
    if success:
        print("✅ Successfully installed Versade from PyPI!")
        return True
    else:
        print(f"❌ pipx install from PyPI failed: {output}")
        print("Note: Package may not be published to PyPI yet.")
    
    return False

def install_with_pip() -> bool:
    """Install using pip."""
    print("🐍 Installing with pip...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("⚠️  Warning: Not in a virtual environment.")
        response = input("Continue with system-wide installation? (y/N): ")
        if response.lower() != 'y':
            print("Installation cancelled. Consider using uvx or pipx instead.")
            return False
    
    pip_cmd = "pip3" if check_command_exists("pip3") else "pip"
    
    if Path("pyproject.toml").exists():
        success, output = run_command([pip_cmd, "install", "-e", "."])
        if success:
            print("✅ Successfully installed Versade with pip (editable)!")
            return True
        else:
            print(f"❌ pip install failed: {output}")
    
    # Try installing from PyPI
    success, output = run_command([pip_cmd, "install", "versade"])
    if success:
        print("✅ Successfully installed Versade from PyPI!")
        return True
    else:
        print(f"❌ pip install from PyPI failed: {output}")
    
    return False

def install_development() -> bool:
    """Install for development."""
    print("🔧 Setting up development environment...")
    
    if not Path("pyproject.toml").exists():
        print("❌ Not in Versade project directory!")
        return False
    
    # Check for uv first (preferred for development)
    if check_command_exists("uv"):
        print("Using uv for development setup...")
        success, output = run_command(["uv", "sync"])
        if success:
            print("✅ Development environment set up with uv!")
            print("\n🎯 Usage:")
            print("  uv run versade --help           # Show help")
            print("  uv run versade check requests   # Check packages")
            print("  uv run versade serve            # Start API server")
            print("  uv run versade mcp              # Start MCP server")
            print("  uv run versade setup            # Interactive setup")
            return True
        else:
            print(f"❌ uv sync failed: {output}")
    
    # Fallback to pip
    pip_cmd = "pip3" if check_command_exists("pip3") else "pip"
    success, output = run_command([pip_cmd, "install", "-e", "."])
    if success:
        print("✅ Development environment set up with pip!")
        print("\n🎯 Usage:")
        print("  versade --help           # Show help")
        print("  versade check requests   # Check packages")
        print("  versade serve            # Start API server")
        print("  versade mcp              # Start MCP server")
        print("  versade setup            # Interactive setup")
        return True
    else:
        print(f"❌ Development install failed: {output}")
    
    return False

def test_installation() -> bool:
    """Test if installation was successful."""
    print("🧪 Testing installation...")
    
    # Try different ways to run versade
    test_commands = [
        ["versade", "--version"],
        ["uv", "run", "versade", "--version"],
        ["python", "-m", "versade.cli", "--version"]
    ]
    
    for cmd in test_commands:
        if check_command_exists(cmd[0]):
            success, output = run_command(cmd)
            if success and "versade" in output.lower():
                print(f"✅ Installation test passed: {' '.join(cmd)}")
                return True
    
    print("❌ Installation test failed")
    print("💡 For development mode, try: uv run versade --help")
    return False

def show_post_install_info():
    """Show post-installation information."""
    print("\n🎉 Versade Installation Complete!")
    print("\n📚 Quick Start:")
    print("  versade check requests numpy        # Check Python packages")
    print("  versade check --npm express react   # Check npm packages")
    print("  versade serve                       # Start HTTP API")
    print("  versade mcp                         # Start MCP server")
    print("  versade setup                       # Interactive setup")
    print("  versade history list                # View query history")
    print("\n🔧 Configuration:")
    print("  Run 'versade setup' for interactive configuration")
    print("  Or set PERPLEXITY_API_KEY environment variable")
    print("\n📖 Documentation:")
    print("  versade --help                      # Show help")
    print("  versade <command> --help            # Command-specific help")

def main():
    """Main installation function."""
    print("🔧 Versade Installation Script")
    print("=" * 40)
    
    # Show available options
    print("\nAvailable installation methods:")
    print("1. uvx - Isolated global install (PyPI only)")
    print("2. pipx - Isolated global install") 
    print("3. pip - System/venv install")
    print("4. Development - Local development setup (recommended)")
    print("5. Auto-detect - Let script choose best method")
    
    choice = input("\nChoose installation method (1-5) or press Enter for auto-detect: ").strip()
    
    success = False
    
    if choice == "1":
        if check_command_exists("uvx"):
            success = install_with_uvx()
        else:
            print("❌ uvx not found. Install with: pip install uvx")
    
    elif choice == "2":
        if check_command_exists("pipx"):
            success = install_with_pipx()
        else:
            print("❌ pipx not found. Install with: pip install pipx")
    
    elif choice == "3":
        success = install_with_pip()
    
    elif choice == "4":
        success = install_development()
    
    else:  # Auto-detect
        print("🔍 Auto-detecting best installation method...")
        
        manager = detect_package_manager()
        if not manager:
            print("❌ No suitable package manager found!")
            print("Please install pip, pipx, or uvx first.")
            sys.exit(1)
        
        print(f"Found: {manager}")
        
        if manager == "uvx":
            success = install_with_uvx()
        elif manager == "pipx":
            success = install_with_pipx()
        else:
            success = install_with_pip()
    
    if success:
        if test_installation():
            show_post_install_info()
        else:
            print("\n⚠️  Installation completed but test failed.")
            print("Try running 'versade --help' manually.")
    else:
        print("\n❌ Installation failed!")
        print("\nTroubleshooting:")
        print("1. Make sure you have Python 3.8+ installed")
        print("2. Try installing uvx: pip install uvx")
        print("3. For development: git clone && cd versade && uv sync")
        sys.exit(1)

if __name__ == "__main__":
    main() 