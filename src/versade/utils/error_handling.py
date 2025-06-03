"""
Versade Error Handling and Prediction Service.
"""

import difflib
import re
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel

console = Console()

# Valid commands and subcommands
VALID_COMMANDS = {
    "check": ["packages", "--npm", "--json"],
    "serve": ["--host", "--port", "--reload"],
    "mcp": ["--transport"],
    "setup": ["--force"],
    "research": ["query", "--api-key", "--model"],
    "history": ["list", "search", "view", "clear", "stats", "export"],
    "test": ["--api-key", "--query", "--quick"]
}

# Valid models
VALID_MODELS = [
    "sonar-deep-research",
    "sonar-reasoning-pro", 
    "sonar-reasoning",
    "sonar-pro",
    "sonar",
    "r1-1776"
]

# Valid package managers
VALID_PACKAGE_MANAGERS = ["pip", "npm", "poetry", "yarn"]


class ErrorHandler:
    """Handles errors and provides intelligent suggestions."""
    
    def __init__(self):
        self.console = Console()
    
    def suggest_command(self, invalid_command: str, threshold: float = 0.6) -> Optional[str]:
        """Suggest a similar valid command."""
        all_commands = list(VALID_COMMANDS.keys())
        matches = difflib.get_close_matches(
            invalid_command, 
            all_commands, 
            n=1, 
            cutoff=threshold
        )
        return matches[0] if matches else None
    
    def suggest_subcommand(self, command: str, invalid_subcommand: str, threshold: float = 0.6) -> Optional[str]:
        """Suggest a similar valid subcommand for a given command."""
        if command not in VALID_COMMANDS:
            return None
        
        valid_subcommands = VALID_COMMANDS[command]
        matches = difflib.get_close_matches(
            invalid_subcommand,
            valid_subcommands,
            n=1,
            cutoff=threshold
        )
        return matches[0] if matches else None
    
    def suggest_model(self, invalid_model: str, threshold: float = 0.6) -> Optional[str]:
        """Suggest a similar valid model."""
        matches = difflib.get_close_matches(
            invalid_model,
            VALID_MODELS,
            n=1,
            cutoff=threshold
        )
        return matches[0] if matches else None
    
    def validate_package_name(self, package_name: str) -> bool:
        """Validate package name format."""
        # Basic validation - alphanumeric, hyphens, underscores, dots
        pattern = r'^[a-zA-Z0-9._-]+$'
        return bool(re.match(pattern, package_name)) and len(package_name) > 0
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate API key format."""
        # Basic validation for Perplexity API keys
        if api_key.startswith('pplx-') and len(api_key) > 10:
            return True
        return False
    
    def handle_command_error(self, command: str, error_type: str = "invalid") -> None:
        """Handle command errors with suggestions."""
        if error_type == "invalid":
            suggestion = self.suggest_command(command)
            if suggestion:
                self.console.print(f"[red]❌ Unknown command: '{command}'[/red]")
                self.console.print(f"[yellow]💡 Did you mean: [bold]versade {suggestion}[/bold]?[/yellow]")
                self.log_prediction(f"Suggested '{suggestion}' for invalid command '{command}'")
            else:
                self.console.print(f"[red]❌ Unknown command: '{command}'[/red]")
                self.console.print("[yellow]💡 Available commands: check, serve, mcp, setup, research, history, test[/yellow]")
    
    def handle_model_error(self, model: str) -> None:
        """Handle invalid model errors with suggestions."""
        suggestion = self.suggest_model(model)
        if suggestion:
            self.console.print(f"[red]❌ Invalid model: '{model}'[/red]")
            self.console.print(f"[yellow]💡 Did you mean: [bold]{suggestion}[/bold]?[/yellow]")
            self.log_prediction(f"Suggested '{suggestion}' for invalid model '{model}'")
        else:
            self.console.print(f"[red]❌ Invalid model: '{model}'[/red]")
            self.console.print("[yellow]💡 Available models:[/yellow]")
            for valid_model in VALID_MODELS:
                self.console.print(f"  • {valid_model}")
    
    def handle_package_error(self, package: str) -> None:
        """Handle invalid package name errors."""
        if not self.validate_package_name(package):
            self.console.print(f"[red]❌ Invalid package name: '{package}'[/red]")
            self.console.print("[yellow]💡 Package names should contain only letters, numbers, hyphens, underscores, and dots[/yellow]")
    
    def handle_api_key_error(self, api_key: str) -> None:
        """Handle invalid API key errors."""
        if not self.validate_api_key(api_key):
            self.console.print(f"[red]❌ Invalid API key format[/red]")
            self.console.print("[yellow]💡 Perplexity API keys should start with 'pplx-' followed by the key[/yellow]")
    
    def handle_network_error(self, error: Exception, retry_suggestion: bool = True) -> None:
        """Handle network-related errors."""
        self.console.print(f"[red]❌ Network error: {error}[/red]")
        if retry_suggestion:
            self.console.print("[yellow]💡 Try again in a moment or check your internet connection[/yellow]")
    
    def handle_file_error(self, filepath: str, error: Exception) -> None:
        """Handle file-related errors."""
        self.console.print(f"[red]❌ File error with '{filepath}': {error}[/red]")
        self.console.print("[yellow]💡 Check file permissions and path[/yellow]")
    
    def log_prediction(self, prediction: str) -> None:
        """Log prediction to user output."""
        self.console.print(f"[dim]🔮 Prediction logged: {prediction}[/dim]")
    
    def create_error_panel(self, title: str, message: str, suggestions: List[str] = None) -> Panel:
        """Create a rich error panel with suggestions."""
        content = f"[red]{message}[/red]"
        
        if suggestions:
            content += "\n\n[yellow]💡 Suggestions:[/yellow]"
            for suggestion in suggestions:
                content += f"\n  • {suggestion}"
        
        return Panel(
            content,
            title=f"[red]❌ {title}[/red]",
            border_style="red"
        )
    
    def validate_input(self, input_type: str, value: str) -> Dict[str, Any]:
        """Validate input and return validation result."""
        result = {
            "valid": False,
            "error": None,
            "suggestion": None
        }
        
        if input_type == "package":
            result["valid"] = self.validate_package_name(value)
            if not result["valid"]:
                result["error"] = "Invalid package name format"
        
        elif input_type == "model":
            result["valid"] = value in VALID_MODELS
            if not result["valid"]:
                result["error"] = f"Invalid model: {value}"
                result["suggestion"] = self.suggest_model(value)
        
        elif input_type == "api_key":
            result["valid"] = self.validate_api_key(value)
            if not result["valid"]:
                result["error"] = "Invalid API key format"
        
        elif input_type == "command":
            result["valid"] = value in VALID_COMMANDS
            if not result["valid"]:
                result["error"] = f"Unknown command: {value}"
                result["suggestion"] = self.suggest_command(value)
        
        return result


class InputValidator:
    """Validates and sanitizes user inputs."""
    
    @staticmethod
    def sanitize_package_name(package: str) -> str:
        """Sanitize package name by removing invalid characters."""
        # Remove invalid characters, keep only alphanumeric, hyphens, underscores, dots
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', package.strip())
        return sanitized
    
    @staticmethod
    def sanitize_search_term(search_term: str) -> str:
        """Sanitize search term for SQL queries."""
        # Basic sanitization - remove SQL injection attempts
        sanitized = search_term.replace("'", "''").replace(";", "").strip()
        return sanitized[:500]  # Limit length
    
    @staticmethod
    def validate_limit(limit: str) -> int:
        """Validate and convert limit parameter."""
        try:
            limit_int = int(limit)
            return max(1, min(limit_int, 1000))  # Clamp between 1 and 1000
        except ValueError:
            return 50  # Default


# Global error handler instance
error_handler = ErrorHandler()
input_validator = InputValidator() 