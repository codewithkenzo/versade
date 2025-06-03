"""
Versade CLI - Modern command-line interface with subcommands.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

import uvicorn
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

from versade.server import check_python_package, check_npm_package
from versade.api.app import app
from versade.services.research import research_service
from versade.services.history import history_service, HistoryEntry
from versade.utils.error_handling import error_handler, input_validator

console = Console()


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="versade",
        description="Versatile dependency analysis and MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  versade check requests numpy                    # Check Python packages
  versade check --npm express react              # Check npm packages
  versade serve --port 8000                      # Start HTTP API server
  versade mcp                                     # Start MCP server (stdio)
  versade setup                                   # Interactive setup
  versade research "security issues with flask"  # Research query
  versade research "npm vulnerabilities" --model sonar-reasoning-pro
        """
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 1.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Check command
    check_parser = subparsers.add_parser(
        "check", 
        help="Check package versions and security"
    )
    check_parser.add_argument(
        "packages", 
        nargs="+", 
        help="Package names to check"
    )
    check_parser.add_argument(
        "--npm", 
        action="store_true", 
        help="Check npm packages (default: pip)"
    )
    check_parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output results as JSON"
    )
    
    # Serve command
    serve_parser = subparsers.add_parser(
        "serve", 
        help="Start HTTP API server"
    )
    serve_parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind to (default: 0.0.0.0)"
    )
    serve_parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind to (default: 8000)"
    )
    serve_parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    
    # MCP command
    mcp_parser = subparsers.add_parser(
        "mcp", 
        help="Start MCP server (stdio mode)"
    )
    mcp_parser.add_argument(
        "--transport", 
        choices=["stdio", "sse"], 
        default="stdio", 
        help="Transport mode (default: stdio)"
    )
    
    # Setup command
    setup_parser = subparsers.add_parser(
        "setup", 
        help="Interactive setup and configuration"
    )
    setup_parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force reconfiguration"
    )
    
    # Research command
    research_parser = subparsers.add_parser(
        "research", 
        help="Research packages and security issues"
    )
    research_parser.add_argument(
        "query", 
        help="Research query"
    )
    research_parser.add_argument(
        "--api-key", 
        help="Perplexity API key (optional if set in env)"
    )
    research_parser.add_argument(
        "--model",
        choices=[
            "sonar-deep-research",
            "sonar-reasoning-pro", 
            "sonar-reasoning",
            "sonar-pro",
            "sonar",
            "r1-1776"
        ],
        default="sonar-deep-research",
        help="Perplexity model to use (default: sonar-deep-research)"
    )
    
    # History command
    history_parser = subparsers.add_parser(
        "history", 
        help="Manage query history"
    )
    history_subparsers = history_parser.add_subparsers(dest="history_command", help="History commands")
    
    # History list
    list_parser = history_subparsers.add_parser("list", help="List recent queries")
    list_parser.add_argument("--limit", type=int, default=20, help="Number of entries to show")
    list_parser.add_argument("--type", choices=["research", "check", "analyze"], help="Filter by query type")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # History search
    search_parser = history_subparsers.add_parser("search", help="Search query history")
    search_parser.add_argument("term", help="Search term")
    search_parser.add_argument("--limit", type=int, default=20, help="Number of results")
    search_parser.add_argument("--type", choices=["research", "check", "analyze"], help="Filter by query type")
    
    # History view
    view_parser = history_subparsers.add_parser("view", help="View specific query")
    view_parser.add_argument("id", type=int, help="Query ID to view")
    
    # History clear
    clear_parser = history_subparsers.add_parser("clear", help="Clear history")
    clear_parser.add_argument("--older-than", help="Clear entries older than date (YYYY-MM-DD)")
    clear_parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
    
    # History stats
    stats_parser = history_subparsers.add_parser("stats", help="Show history statistics")
    
    # History export
    export_parser = history_subparsers.add_parser("export", help="Export history")
    export_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format")
    export_parser.add_argument("--output", help="Output file (default: stdout)")
    
    # Test command
    test_parser = subparsers.add_parser(
        "test", 
        help="Test all Perplexity models"
    )
    test_parser.add_argument(
        "--api-key", 
        help="Perplexity API key (optional if set in env)"
    )
    test_parser.add_argument(
        "--query",
        default="What are Python security best practices?",
        help="Test query to use (default: Python security question)"
    )
    test_parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick test with shorter responses"
    )
    
    return parser


async def cmd_check(args) -> None:
    """Handle the check command."""
    package_manager = "npm" if args.npm else "pip"
    results = []
    
    # Validate package names
    for package in args.packages:
        if not error_handler.validate_package_name(package):
            error_handler.handle_package_error(package)
            return
    
    console.print(f"[bold blue]Checking {len(args.packages)} {package_manager} packages...[/bold blue]")
    
    # Save query to history
    query_text = f"check {' '.join(args.packages)} --{package_manager}"
    query_id = history_service.save_query(
        query=query_text,
        query_type="check",
        metadata={"package_manager": package_manager, "packages": args.packages}
    )
    
    for package in args.packages:
        try:
            if package_manager == "npm":
                result = await check_npm_package(package)
            else:
                result = await check_python_package(package)
            results.append(result)
            
            if not args.json:
                status = "✅" if result.get("success") else "❌"
                console.print(f"{status} {package}: {result.get('version', 'N/A')}")
                
        except Exception as e:
            error_handler.handle_network_error(e)
            error_result = {"name": package, "error": str(e), "success": False}
            results.append(error_result)
            
            if not args.json:
                console.print(f"❌ {package}: Error - {e}")
    
    # Save results to history
    history_service.save_query(
        query=query_text,
        query_type="check",
        response=json.dumps(results),
        success=all(r.get("success", False) for r in results),
        metadata={"package_manager": package_manager, "packages": args.packages, "results_count": len(results)}
    )
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Create a summary table
        table = Table(title=f"{package_manager.upper()} Package Analysis")
        table.add_column("Package", style="cyan")
        table.add_column("Version", style="green")
        table.add_column("Status", style="bold")
        
        for result in results:
            status = "✅ OK" if result.get("success") else "❌ Error"
            table.add_row(
                result.get("name", "Unknown"),
                result.get("version", "N/A"),
                status
            )
        
        console.print(table)
        console.print(f"[dim]💾 Saved to history (ID: {query_id})[/dim]")


def cmd_serve(args) -> None:
    """Handle the serve command."""
    console.print(f"[bold green]Starting Versade API server on {args.host}:{args.port}[/bold green]")
    
    uvicorn.run(
        "versade.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


def cmd_mcp(args) -> None:
    """Handle the MCP command."""
    from versade.server import main as mcp_main
    
    console.print(f"[bold green]Starting MCP server in {args.transport} mode[/bold green]")
    
    # Set transport mode in environment
    os.environ["VERSADE_TRANSPORT_MODE"] = args.transport
    
    # Run the MCP server
    mcp_main()


def cmd_setup(args) -> None:
    """Handle the setup command."""
    config_path = Path.home() / ".versade" / "config.env"
    
    if config_path.exists() and not args.force:
        if not Confirm.ask(f"Configuration already exists at {config_path}. Overwrite?"):
            return
    
    console.print(Panel.fit(
        "[bold blue]Versade Interactive Setup[/bold blue]\n"
        "Configure your Versade installation with API keys and preferences.",
        title="Setup"
    ))
    
    # Create config directory
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Collect configuration
    config_data = {}
    
    # Perplexity API key
    perplexity_key = Prompt.ask(
        "Perplexity API key (optional, for research features)",
        default="",
        show_default=False
    )
    if perplexity_key:
        config_data["PERPLEXITY_API_KEY"] = perplexity_key
    
    # Log level
    log_level = Prompt.ask(
        "Log level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO"
    )
    config_data["VERSADE_LOG_LEVEL"] = log_level
    
    # Default transport mode
    transport_mode = Prompt.ask(
        "Default MCP transport mode",
        choices=["stdio", "sse"],
        default="stdio"
    )
    config_data["VERSADE_TRANSPORT_MODE"] = transport_mode
    
    # Write configuration
    with open(config_path, "w") as f:
        for key, value in config_data.items():
            f.write(f"{key}={value}\n")
    
    console.print(f"[bold green]✅ Configuration saved to {config_path}[/bold green]")
    
    # Show next steps
    console.print(Panel.fit(
        "[bold]Next Steps:[/bold]\n"
        "• Test package checking: [cyan]versade check requests[/cyan]\n"
        "• Start API server: [cyan]versade serve[/cyan]\n"
        "• Start MCP server: [cyan]versade mcp[/cyan]\n"
        "• Research packages: [cyan]versade research 'security issues with flask'[/cyan]",
        title="Getting Started"
    ))


async def cmd_research(args) -> None:
    """Handle the research command."""
    # Validate API key if provided
    if args.api_key and not error_handler.validate_api_key(args.api_key):
        error_handler.handle_api_key_error(args.api_key)
        return
    
    if args.api_key:
        research_service.api_key = args.api_key
    
    # Save query to history
    query_id = history_service.save_query(
        query=args.query,
        query_type="research",
        metadata={"model": args.model, "api_key_provided": bool(args.api_key)}
    )
    
    try:
        console.print(f"[bold blue]Researching: {args.query}[/bold blue]")
        console.print(f"[dim]Using model: {args.model}[/dim]")
        
        # Show loading indicator for slower models
        if args.model in ["sonar-reasoning-pro", "sonar-deep-research"]:
            console.print("[yellow]⏳ This model may take 1-3 minutes to respond...[/yellow]")
        
        console.print("[dim]🔄 Sending request...[/dim]")
        
        # Add timeout based on model
        import asyncio
        timeout = 300 if args.model == "sonar-deep-research" else 120
        
        result = await asyncio.wait_for(
            research_service.research(args.query, model=args.model),
            timeout=timeout
        )
        
        # Save successful result to history
        history_service.save_query(
            query=args.query,
            query_type="research",
            response=result["response"],
            success=True,
            metadata={
                "model": args.model,
                "citations": result.get("citations", []),
                "related_questions": result.get("related_questions", [])
            }
        )
        
        console.print(Panel.fit(
            result["response"],
            title="Research Results"
        ))
        
        if result.get("citations"):
            console.print("\n[bold]Sources:[/bold]")
            for i, citation in enumerate(result["citations"], 1):
                console.print(f"{i}. {citation}")
        
        if result.get("related_questions"):
            console.print("\n[bold]Related Questions:[/bold]")
            for question in result["related_questions"]:
                console.print(f"• {question}")
        
        console.print(f"[dim]💾 Saved to history (ID: {query_id})[/dim]")
    
    except asyncio.TimeoutError:
        error_message = f"Request timed out after {timeout} seconds"
        history_service.save_query(
            query=args.query,
            query_type="research",
            success=False,
            error_message=error_message,
            metadata={"model": args.model, "error_type": "timeout"}
        )
        console.print(f"[red]❌ Request timed out after {timeout} seconds[/red]")
        console.print("[yellow]💡 Try using a faster model like 'sonar' or 'sonar-pro'[/yellow]")
                
    except ValueError as e:
        error_message = str(e)
        history_service.save_query(
            query=args.query,
            query_type="research",
            success=False,
            error_message=error_message,
            metadata={"model": args.model}
        )
        console.print(f"[bold red]Error: {e}[/bold red]")
        console.print("Set PERPLEXITY_API_KEY environment variable or use --api-key option")
    except Exception as e:
        error_message = str(e)
        history_service.save_query(
            query=args.query,
            query_type="research",
            success=False,
            error_message=error_message,
            metadata={"model": args.model}
        )
        error_handler.handle_network_error(e)
        console.print(f"[bold red]Research failed: {e}[/bold red]")


async def cmd_history(args) -> None:
    """Handle the history command."""
    if not args.history_command:
        console.print("[yellow]Please specify a history subcommand. Use --help for options.[/yellow]")
        return
    
    try:
        if args.history_command == "list":
            await cmd_history_list(args)
        elif args.history_command == "search":
            await cmd_history_search(args)
        elif args.history_command == "view":
            await cmd_history_view(args)
        elif args.history_command == "clear":
            await cmd_history_clear(args)
        elif args.history_command == "stats":
            await cmd_history_stats(args)
        elif args.history_command == "export":
            await cmd_history_export(args)
    except Exception as e:
        error_handler.handle_file_error("history database", e)


async def cmd_history_list(args) -> None:
    """List recent queries."""
    limit = input_validator.validate_limit(str(args.limit))
    entries = history_service.get_history(limit=limit, query_type=args.type)
    
    if args.json:
        data = []
        for entry in entries:
            data.append({
                "id": entry.id,
                "query": entry.query,
                "type": entry.query_type,
                "timestamp": entry.timestamp.isoformat(),
                "success": entry.success,
                "metadata": entry.metadata
            })
        print(json.dumps(data, indent=2))
        return
    
    if not entries:
        console.print("[yellow]No history entries found.[/yellow]")
        return
    
    table = Table(title="Query History")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Query", style="white", width=50)
    table.add_column("Type", style="green", width=10)
    table.add_column("Status", style="bold", width=8)
    table.add_column("Time", style="dim", width=16)
    
    for entry in entries:
        query_preview = entry.query[:47] + "..." if len(entry.query) > 50 else entry.query
        status = "✅ OK" if entry.success else "❌ Error"
        time_str = entry.timestamp.strftime("%m-%d %H:%M")
        
        table.add_row(
            str(entry.id),
            query_preview,
            entry.query_type,
            status,
            time_str
        )
    
    console.print(table)
    console.print(f"[dim]Showing {len(entries)} entries. Use 'versade history view <id>' to see details.[/dim]")


async def cmd_history_search(args) -> None:
    """Search query history."""
    search_term = input_validator.sanitize_search_term(args.term)
    limit = input_validator.validate_limit(str(args.limit))
    entries = history_service.search_history(search_term, limit=limit, query_type=args.type)
    
    if not entries:
        console.print(f"[yellow]No entries found matching '{args.term}'.[/yellow]")
        return
    
    table = Table(title=f"Search Results for '{args.term}'")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Query", style="white", width=50)
    table.add_column("Type", style="green", width=10)
    table.add_column("Status", style="bold", width=8)
    table.add_column("Time", style="dim", width=16)
    
    for entry in entries:
        query_preview = entry.query[:47] + "..." if len(entry.query) > 50 else entry.query
        status = "✅ OK" if entry.success else "❌ Error"
        time_str = entry.timestamp.strftime("%m-%d %H:%M")
        
        # Highlight search term
        if search_term.lower() in query_preview.lower():
            query_preview = query_preview.replace(
                search_term, f"[bold yellow]{search_term}[/bold yellow]"
            )
        
        table.add_row(
            str(entry.id),
            query_preview,
            entry.query_type,
            status,
            time_str
        )
    
    console.print(table)
    console.print(f"[dim]Found {len(entries)} matching entries.[/dim]")


async def cmd_history_view(args) -> None:
    """View a specific query."""
    entry = history_service.get_entry_by_id(args.id)
    
    if not entry:
        console.print(f"[red]❌ No entry found with ID {args.id}[/red]")
        return
    
    # Create detailed view
    console.print(Panel.fit(
        f"[bold]Query:[/bold] {entry.query}\n"
        f"[bold]Type:[/bold] {entry.query_type}\n"
        f"[bold]Time:[/bold] {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"[bold]Status:[/bold] {'✅ Success' if entry.success else '❌ Error'}",
        title=f"Query Details (ID: {entry.id})"
    ))
    
    if entry.response:
        console.print(Panel.fit(
            entry.response[:1000] + ("..." if len(entry.response) > 1000 else ""),
            title="Response"
        ))
    
    if entry.error_message:
        console.print(Panel.fit(
            entry.error_message,
            title="Error",
            border_style="red"
        ))
    
    if entry.metadata:
        console.print(Panel.fit(
            json.dumps(entry.metadata, indent=2),
            title="Metadata"
        ))


async def cmd_history_clear(args) -> None:
    """Clear history entries."""
    if args.older_than:
        try:
            from datetime import datetime
            older_than = datetime.strptime(args.older_than, "%Y-%m-%d")
        except ValueError:
            console.print("[red]❌ Invalid date format. Use YYYY-MM-DD[/red]")
            return
    else:
        older_than = None
    
    if not args.confirm:
        if older_than:
            message = f"Clear all entries older than {args.older_than}?"
        else:
            message = "Clear ALL history entries?"
        
        if not Confirm.ask(message):
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
    
    deleted_count = history_service.clear_history(older_than)
    console.print(f"[green]✅ Cleared {deleted_count} history entries.[/green]")


async def cmd_history_stats(args) -> None:
    """Show history statistics."""
    stats = history_service.get_stats()
    
    console.print(Panel.fit(
        f"[bold]Total Queries:[/bold] {stats['total_queries']}\n"
        f"[bold]Successful Responses:[/bold] {stats['successful_responses']}\n"
        f"[bold]Database Size:[/bold] {stats['database_size']:,} bytes\n\n"
        f"[bold]By Type:[/bold]\n" +
        "\n".join([f"  • {type_name}: {count}" for type_name, count in stats['by_type'].items()]) +
        f"\n\n[bold]Date Range:[/bold] {stats['date_range'][0] or 'N/A'} to {stats['date_range'][1] or 'N/A'}",
        title="History Statistics"
    ))


async def cmd_history_export(args) -> None:
    """Export history to file."""
    entries = history_service.get_history(limit=10000)  # Export all
    
    if args.format == "json":
        data = []
        for entry in entries:
            data.append({
                "id": entry.id,
                "query": entry.query,
                "query_type": entry.query_type,
                "timestamp": entry.timestamp.isoformat(),
                "response": entry.response,
                "success": entry.success,
                "error_message": entry.error_message,
                "metadata": entry.metadata
            })
        output = json.dumps(data, indent=2)
    
    elif args.format == "csv":
        import csv
        import io
        output_buffer = io.StringIO()
        writer = csv.writer(output_buffer)
        writer.writerow(["ID", "Query", "Type", "Timestamp", "Success", "Response", "Error"])
        
        for entry in entries:
            writer.writerow([
                entry.id,
                entry.query,
                entry.query_type,
                entry.timestamp.isoformat(),
                entry.success,
                entry.response or "",
                entry.error_message or ""
            ])
        output = output_buffer.getvalue()
    
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            console.print(f"[green]✅ Exported {len(entries)} entries to {args.output}[/green]")
        except Exception as e:
            error_handler.handle_file_error(args.output, e)
    else:
        print(output)


async def cmd_test(args) -> None:
    """Test all Perplexity models."""
    # Validate API key if provided
    if args.api_key and not error_handler.validate_api_key(args.api_key):
        error_handler.handle_api_key_error(args.api_key)
        return
    
    if args.api_key:
        research_service.api_key = args.api_key
    
    # Order models by speed (fastest first)
    models = [
        "sonar",           # Fastest
        "sonar-pro",       # Fast
        "sonar-reasoning", # Medium
        "r1-1776",         # Medium-slow
        "sonar-reasoning-pro",  # Slow
        "sonar-deep-research"   # Slowest (can take minutes)
    ]
    
    query = args.query
    if args.quick:
        query = "Is Flask secure? (brief answer)"
    
    console.print(f"[bold blue]🧪 Testing all Perplexity models[/bold blue]")
    console.print(f"[dim]Query: {query}[/dim]")
    console.print("=" * 60)
    
    results = []
    
    for i, model in enumerate(models, 1):
        # Show model info with expected speed
        speed_info = {
            "sonar": "⚡ Very Fast",
            "sonar-pro": "🚀 Fast", 
            "sonar-reasoning": "⏱️ Medium",
            "r1-1776": "⏳ Medium-Slow",
            "sonar-reasoning-pro": "🐌 Slow",
            "sonar-deep-research": "🕰️ Very Slow (1-3 min)"
        }
        
        console.print(f"\n[bold cyan]{i}/{len(models)} Testing model: {model}[/bold cyan] [dim]({speed_info.get(model, 'Unknown speed')})[/dim]")
        
        # Show loading indicator for slower models
        if model in ["sonar-reasoning-pro", "sonar-deep-research"]:
            console.print("[yellow]⏳ This model may take 1-3 minutes to respond...[/yellow]")
        
        try:
            # Add timeout for very slow models
            import asyncio
            timeout = 300 if model == "sonar-deep-research" else 120  # 5 min for deep-research, 2 min for others
            
            console.print("[dim]🔄 Sending request...[/dim]")
            result = await asyncio.wait_for(
                research_service.research(query, model=model),
                timeout=timeout
            )
            
            # Save to history
            history_service.save_query(
                query=f"test: {query}",
                query_type="test",
                response=result["response"],
                success=True,
                metadata={"model": model, "test_run": True, "response_time": "completed"}
            )
            
            # Show preview
            preview = result["response"][:200] + "..." if len(result["response"]) > 200 else result["response"]
            console.print(f"[green]✅ {model}: SUCCESS[/green]")
            console.print(f"[dim]{preview}[/dim]")
            
            results.append({
                "model": model,
                "success": True,
                "response_length": len(result["response"]),
                "preview": preview
            })
            
        except asyncio.TimeoutError:
            error_msg = f"Request timed out after {timeout} seconds"
            console.print(f"[red]❌ {model}: TIMEOUT - {error_msg}[/red]")
            
            # Save timeout error to history
            history_service.save_query(
                query=f"test: {query}",
                query_type="test",
                success=False,
                error_message=error_msg,
                metadata={"model": model, "test_run": True, "error_type": "timeout"}
            )
            
            results.append({
                "model": model,
                "success": False,
                "error": error_msg
            })
            
        except Exception as e:
            error_msg = str(e)
            console.print(f"[red]❌ {model}: FAILED - {error_msg}[/red]")
            
            # Save error to history
            history_service.save_query(
                query=f"test: {query}",
                query_type="test",
                success=False,
                error_message=error_msg,
                metadata={"model": model, "test_run": True, "error_type": "api_error"}
            )
            
            results.append({
                "model": model,
                "success": False,
                "error": error_msg
            })
        
        # Rate limiting with progress indicator
        if i < len(models):
            console.print("[dim]⏸️ Waiting 2 seconds (rate limiting)...[/dim]")
            import asyncio
            await asyncio.sleep(2)
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold blue]🎉 Test Summary[/bold blue]")
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    console.print(f"[green]✅ Successful: {len(successful)}/{len(models)}[/green]")
    console.print(f"[red]❌ Failed: {len(failed)}/{len(models)}[/red]")
    
    if successful:
        console.print("\n[bold green]Working models:[/bold green]")
        for result in successful:
            console.print(f"  • {result['model']} ({result['response_length']} chars)")
    
    if failed:
        console.print("\n[bold red]Failed models:[/bold red]")
        for result in failed:
            console.print(f"  • {result['model']}: {result['error']}")
    
    console.print(f"\n[dim]💾 All results saved to history[/dim]")


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    
    # Handle case where no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Check for invalid commands before parsing
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command not in ["check", "serve", "mcp", "setup", "research", "history", "test", "--version", "--help", "-h"]:
            error_handler.handle_command_error(command)
            return
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "check":
            asyncio.run(cmd_check(args))
        elif args.command == "serve":
            cmd_serve(args)
        elif args.command == "mcp":
            cmd_mcp(args)
        elif args.command == "setup":
            cmd_setup(args)
        elif args.command == "research":
            asyncio.run(cmd_research(args))
        elif args.command == "history":
            asyncio.run(cmd_history(args))
        elif args.command == "test":
            asyncio.run(cmd_test(args))
        else:
            error_handler.handle_command_error(args.command)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")
        console.print("[dim]If this persists, please report it as a bug.[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main() 