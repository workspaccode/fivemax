#!/usr/bin/env python3
"""
CLI Interface for Advanced Agentic System
Command-line interface for interacting with the agentic AI framework
"""

import os
import sys
import json
import asyncio
import click
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

from advanced_agentic_system import AdvancedAgenticSystem
from tool_executor import ToolExecutor, ToolType

# Load environment variables
load_dotenv()

console = Console()


class AgenticCLI:
    """Main CLI interface for the agentic system"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            console.print("[red]Error: PERPLEXITY_API_KEY not found in environment variables[/red]")
            console.print("Please set it in your .env file or pass it with --api-key")
            sys.exit(1)
        
        self.system = AdvancedAgenticSystem(self.api_key)
        self.tool_executor = ToolExecutor()
        self.session_history: List[Dict] = []
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    async def solve_problem(self, problem: str, context_file: Optional[str] = None):
        """Solve a complex problem using the agentic system"""
        
        # Load context if provided
        context = {}
        if context_file and Path(context_file).exists():
            try:
                with open(context_file, 'r') as f:
                    context = json.load(f)
                console.print(f"[green]Loaded context from {context_file}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load context file: {e}[/yellow]")
        
        # Display problem
        console.print(Panel.fit(
            f"[bold cyan]Problem to Solve:[/bold cyan]\n{problem}",
            border_style="cyan"
        ))
        
        # Solve the problem
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Initializing agentic system...", total=None)
            
            try:
                result = await self.system.solve_complex_problem(problem, context)
                
                progress.update(task, description="Solution complete!", completed=True)
                
                # Store in session history
                self.session_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "problem": problem,
                    "result": result,
                    "session_id": self.current_session_id
                })
                
                # Display results
                self._display_solution(result)
                
            except Exception as e:
                progress.update(task, description=f"Error: {str(e)}", completed=True)
                console.print(f"[red]Error solving problem: {e}[/red]")
    
    def _display_solution(self, result: Dict):
        """Display the solution in a formatted way"""
        
        # Performance metrics
        metrics = result["performance"]
        console.print("\n[bold]Performance Metrics:[/bold]")
        metrics_table = Table()
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="green")
        
        metrics_table.add_row("Total Agents", str(metrics["total_agents"]))
        metrics_table.add_row("Busy Agents", str(metrics["busy_agents"]))
        metrics_table.add_row("Completed Tasks", str(metrics["completed_tasks"]))
        metrics_table.add_row("Total Memories", str(metrics["total_memories"]))
        metrics_table.add_row("System Health", metrics["system_health"])
        
        console.print(metrics_table)
        
        # Thinking process
        console.print("\n[bold]Thinking Process:[/bold]")
        thinking_tree = Tree("🧠 Deep Thinking Process")
        
        for thought in result["thoughts"]:
            icon = {
                "analysis": "🔍",
                "planning": "📋",
                "hypothesis": "💡",
                "verification": "✅",
                "synthesis": "🎯"
            }.get(thought["type"], "📝")
            
            branch = thinking_tree.add(f"{icon} {thought['type'].title()}")
            branch.add(f"[dim]{thought['content']}[/dim]")
        
        console.print(thinking_tree)
        
        # Task result synthesis
        if "synthesis" in result["task_result"]:
            console.print("\n[bold]Solution Synthesis:[/bold]")
            console.print(Panel(
                Markdown(result["task_result"]["synthesis"]),
                border_style="green"
            ))
    
    def interactive_mode(self):
        """Start interactive mode"""
        console.print(Panel.fit(
            "[bold cyan]Advanced Agentic AI - Interactive Mode[/bold cyan]\n"
            "Type your problems and let the AI solve them\n"
            "Type 'exit' to quit, 'help' for commands, 'tools' to see available tools",
            border_style="cyan"
        ))
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if user_input.lower() in ['exit', 'quit']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'tools':
                    self.tool_executor.display_tools()
                    continue
                elif user_input.lower() == 'history':
                    self._show_history()
                    continue
                elif user_input.lower().startswith('tool '):
                    self._execute_tool_command(user_input[5:])
                    continue
                elif user_input.lower().startswith('save '):
                    self._save_session(user_input[5:])
                    continue
                elif user_input.lower().startswith('load '):
                    self._load_session(user_input[5:])
                    continue
                elif not user_input.strip():
                    continue
                
                # Solve the problem
                asyncio.run(self.solve_problem(user_input))
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
                continue
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue
    
    def _show_help(self):
        """Show help information"""
        help_text = """
[bold]Available Commands:[/bold]

• [cyan]help[/cyan] - Show this help message
• [cyan]tools[/cyan] - List available tools
• [cyan]history[/cyan] - Show session history
• [cyan]tool <tool_id> <params>[/cyan] - Execute a tool directly
• [cyan]save <filename>[/cyan] - Save current session
• [cyan]load <filename>[/cyan] - Load a previous session
• [cyan]exit/quit[/cyan] - Exit the program

[bold]Examples:[/bold]
• "Design a microservices architecture for e-commerce"
• "Write a Python script to analyze data from CSV files"
• "Create a REST API for user management"
• "Debug this error: TypeError in my Flask app"
        """
        console.print(Panel(help_text, border_style="blue"))
    
    def _show_history(self):
        """Show session history"""
        if not self.session_history:
            console.print("[yellow]No history yet[/yellow]")
            return
        
        console.print("\n[bold]Session History:[/bold]")
        history_table = Table()
        history_table.add_column("Time", style="cyan")
        history_table.add_column("Problem", style="green")
        history_table.add_column("Session ID", style="yellow")
        
        for entry in self.session_history[-10:]:  # Show last 10
            problem_preview = entry["problem"][:50] + "..." if len(entry["problem"]) > 50 else entry["problem"]
            history_table.add_row(
                entry["timestamp"][:19],
                problem_preview,
                entry["session_id"]
            )
        
        console.print(history_table)
    
    def _execute_tool_command(self, command: str):
        """Execute a tool command"""
        try:
            parts = command.split()
            if len(parts) < 1:
                console.print("[red]Usage: tool <tool_id> <param1=value1 param2=value2>[/red]")
                return
            
            tool_id = parts[0]
            params = {}
            
            for part in parts[1:]:
                if '=' in part:
                    key, value = part.split('=', 1)
                    # Try to parse as JSON, fallback to string
                    try:
                        params[key] = json.loads(value)
                    except:
                        params[key] = value
            
            # Execute tool with basic permissions
            result = self.tool_executor.execute_tool(
                tool_id, params, 
                user_permissions=["file_read", "file_write", "web_access"]
            )
            
            console.print(f"\n[bold]Tool Execution Result:[/bold]")
            console.print(f"Tool: {tool_id}")
            console.print(f"Success: {result.success}")
            console.print(f"Execution Time: {result.execution_time:.2f}s")
            
            if result.success:
                console.print(f"Result: {json.dumps(result.result, indent=2)}")
            else:
                console.print(f"Error: {result.error}")
                
        except Exception as e:
            console.print(f"[red]Error executing tool: {e}[/red]")
    
    def _save_session(self, filename: str):
        """Save current session to file"""
        try:
            session_data = {
                "session_id": self.current_session_id,
                "timestamp": datetime.now().isoformat(),
                "history": self.session_history
            }
            
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            console.print(f"[green]Session saved to {filename}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving session: {e}[/red]")
    
    def _load_session(self, filename: str):
        """Load session from file"""
        try:
            with open(filename, 'r') as f:
                session_data = json.load(f)
            
            self.session_history = session_data.get("history", [])
            self.current_session_id = session_data.get("session_id", self.current_session_id)
            
            console.print(f"[green]Session loaded from {filename}[/green]")
            console.print(f"Session ID: {self.current_session_id}")
            console.print(f"History entries: {len(self.session_history)}")
        except Exception as e:
            console.print(f"[red]Error loading session: {e}[/red]")


# CLI Commands
@click.group()
@click.option('--api-key', envvar='PERPLEXITY_API_KEY', help='Perplexity API key')
@click.pass_context
def cli(ctx, api_key):
    """Advanced Agentic AI CLI - Deep thinking and multi-agent collaboration"""
    ctx.ensure_object(dict)
    ctx.obj['cli'] = AgenticCLI(api_key)


@cli.command()
@click.argument('problem')
@click.option('--context', '-c', help='Context file (JSON)')
@click.pass_context
def solve(ctx, problem, context):
    """Solve a complex problem using the agentic system"""
    cli_instance = ctx.obj['cli']
    asyncio.run(cli_instance.solve_problem(problem, context))


@cli.command()
@click.pass_context
def interactive(ctx):
    """Start interactive mode"""
    cli_instance = ctx.obj['cli']
    cli_instance.interactive_mode()


@cli.command()
@click.pass_context
def tools(ctx):
    """List available tools"""
    cli_instance = ctx.obj['cli']
    cli_instance.tool_executor.display_tools()


@cli.command()
@click.argument('tool_id')
@click.argument('params', nargs=-1)
@click.pass_context
def tool(ctx, tool_id, params):
    """Execute a tool directly"""
    cli_instance = ctx.obj['cli']
    
    # Parse parameters
    param_dict = {}
    for param in params:
        if '=' in param:
            key, value = param.split('=', 1)
            try:
                param_dict[key] = json.loads(value)
            except:
                param_dict[key] = value
    
    # Execute tool
    result = cli_instance.tool_executor.execute_tool(
        tool_id, param_dict,
        user_permissions=["file_read", "file_write", "web_access", "code_execution"]
    )
    
    console.print(f"\n[bold]Tool: {tool_id}[/bold]")
    console.print(f"Success: {result.success}")
    console.print(f"Execution Time: {result.execution_time:.2f}s")
    
    if result.success:
        console.print(f"Result: {json.dumps(result.result, indent=2)}")
    else:
        console.print(f"Error: {result.error}")


@cli.command()
@click.option('--limit', '-l', default=10, help='Number of recent executions')
@click.pass_context
def history(ctx, limit):
    """Show tool execution history"""
    cli_instance = ctx.obj['cli']
    history = cli_instance.tool_executor.get_execution_history(limit)
    
    if not history:
        console.print("[yellow]No execution history[/yellow]")
        return
    
    console.print(f"\n[bold]Recent Tool Executions (last {limit}):[/bold]")
    history_table = Table()
    history_table.add_column("Time", style="cyan")
    history_table.add_column("Tool", style="green")
    history_table.add_column("Success", style="yellow")
    history_table.add_column("Duration", style="magenta")
    
    for execution in history:
        history_table.add_row(
            execution.timestamp.strftime("%H:%M:%S"),
            execution.tool_id,
            "✓" if execution.success else "✗",
            f"{execution.execution_time:.2f}s"
        )
    
    console.print(history_table)


@cli.command()
@click.argument('filename')
@click.pass_context
def save(ctx, filename):
    """Save current session"""
    cli_instance = ctx.obj['cli']
    cli_instance._save_session(filename)


@cli.command()
@click.argument('filename')
@click.pass_context
def load(ctx, filename):
    """Load a session"""
    cli_instance = ctx.obj['cli']
    cli_instance._load_session(filename)


@cli.command()
@click.pass_context
def status(ctx):
    """Show system status"""
    cli_instance = ctx.obj['cli']
    
    # System metrics
    metrics = cli_instance.system._get_performance_metrics()
    
    console.print("\n[bold]System Status:[/bold]")
    status_table = Table()
    status_table.add_column("Metric", style="cyan")
    status_table.add_column("Value", style="green")
    
    status_table.add_row("Total Agents", str(metrics["total_agents"]))
    status_table.add_row("Busy Agents", str(metrics["busy_agents"]))
    status_table.add_row("Completed Tasks", str(metrics["completed_tasks"]))
    status_table.add_row("Total Memories", str(metrics["total_memories"]))
    status_table.add_row("System Health", metrics["system_health"])
    status_table.add_row("Session ID", cli_instance.current_session_id)
    status_table.add_row("Session History", f"{len(cli_instance.session_history)} entries")
    
    console.print(status_table)
    
    # Agent details
    console.print("\n[bold]Available Agents:[/bold]")
    agent_table = Table()
    agent_table.add_column("Name", style="cyan")
    agent_table.add_column("Role", style="green")
    agent_table.add_column("Status", style="yellow")
    agent_table.add_column("Capabilities", style="magenta")
    
    for agent in cli_instance.system.orchestrator.agents.values():
        agent_table.add_row(
            agent.name,
            agent.role.value,
            agent.status,
            ", ".join(agent.capabilities[:3]) + ("..." if len(agent.capabilities) > 3 else "")
        )
    
    console.print(agent_table)


if __name__ == "__main__":
    cli()
