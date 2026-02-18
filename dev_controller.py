#!/usr/bin/env python3
"""
Perplexity Dev Controller - AI-Powered Development Assistant
Full-stack development agent for building, fixing, and managing applications
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from dotenv import load_dotenv
import requests

load_dotenv()
console = Console()


class PerplexityDevController:
    """Main development controller using Perplexity AI"""
    
    def __init__(self, api_key: str, model: str = "sonar", workspace: str = "./workspace"):
        self.api_key = api_key
        self.model = model
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True)
        self.conversation_history = []
        self.current_project = None
        self.project_context = {}
        
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send message to Perplexity AI"""
        
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add project context
        if self.project_context:
            context_msg = self._build_context_message()
            messages.append({"role": "system", "content": context_msg})
        
        # Add conversation history
        messages.extend(self.conversation_history[-10:])  # Last 10 messages
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Make API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,  # More deterministic for code
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": content})
            
            return content
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    def _build_context_message(self) -> str:
        """Build context message from project information"""
        context_parts = []
        
        if self.current_project:
            context_parts.append(f"Current Project: {self.current_project}")
        
        if self.project_context.get('tech_stack'):
            context_parts.append(f"Tech Stack: {', '.join(self.project_context['tech_stack'])}")
        
        if self.project_context.get('files'):
            context_parts.append(f"Project Files: {', '.join(self.project_context['files'][:10])}")
        
        return "Project Context:\n" + "\n".join(context_parts)
    
    def create_project(self, name: str, template: str = "custom") -> Dict:
        """Create a new project from template or custom spec"""
        
        project_path = self.workspace / name
        
        if project_path.exists():
            console.print(f"[red]Project {name} already exists![/red]")
            return {"success": False, "error": "Project exists"}
        
        console.print(f"\n[cyan]Creating project: {name}[/cyan]")
        
        # Get project requirements from AI
        prompt = f"""You are a project scaffolding expert. Create a detailed project structure for a {template} project named '{name}'.

Provide a JSON response with:
1. "structure": nested dict of directories and files
2. "tech_stack": list of technologies
3. "dependencies": dict of package managers and their packages
4. "initial_files": dict of filename: content for starter files

Example format:
{{
  "structure": {{
    "src": {{"main.py": null, "utils": {{}}}},
    "tests": {{}},
    "README.md": null
  }},
  "tech_stack": ["python", "fastapi"],
  "dependencies": {{
    "pip": ["fastapi", "uvicorn"]
  }},
  "initial_files": {{
    "README.md": "# {name}\\n\\nProject description...",
    "src/main.py": "from fastapi import FastAPI\\n\\napp = FastAPI()\\n"
  }}
}}

Respond ONLY with valid JSON, no markdown formatting."""

        response = self.chat(prompt)
        
        # Extract JSON from response
        try:
            # Try to find JSON in response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                project_spec = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            console.print(f"[red]Failed to parse AI response: {e}[/red]")
            console.print(f"[yellow]Response was: {response[:200]}...[/yellow]")
            return {"success": False, "error": str(e)}
        
        # Create project structure
        self._create_structure(project_path, project_spec['structure'])
        
        # Write initial files
        for filepath, content in project_spec.get('initial_files', {}).items():
            file_path = project_path / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        
        # Create project metadata
        metadata = {
            "name": name,
            "template": template,
            "tech_stack": project_spec.get('tech_stack', []),
            "dependencies": project_spec.get('dependencies', {}),
            "created": str(Path.cwd())
        }
        
        (project_path / ".perplexity.json").write_text(json.dumps(metadata, indent=2))
        
        self.current_project = name
        self.project_context = metadata
        
        console.print(f"\n[green]✓ Project created: {project_path}[/green]")
        
        return {"success": True, "path": str(project_path), "spec": project_spec}
    
    def _create_structure(self, base_path: Path, structure: Dict):
        """Recursively create directory structure"""
        for name, content in structure.items():
            path = base_path / name
            
            if content is None:
                # It's a file
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    path.touch()
            elif isinstance(content, dict):
                # It's a directory
                path.mkdir(parents=True, exist_ok=True)
                self._create_structure(path, content)
    
    def load_project(self, name: str) -> bool:
        """Load an existing project"""
        project_path = self.workspace / name
        metadata_path = project_path / ".perplexity.json"
        
        if not metadata_path.exists():
            console.print(f"[red]Project {name} not found or not initialized![/red]")
            return False
        
        metadata = json.loads(metadata_path.read_text())
        self.current_project = name
        self.project_context = metadata
        
        # Scan files
        files = []
        for path in project_path.rglob("*"):
            if path.is_file() and not path.name.startswith('.'):
                files.append(str(path.relative_to(project_path)))
        
        self.project_context['files'] = files
        
        console.print(f"[green]✓ Loaded project: {name}[/green]")
        return True
    
    def generate_code(self, description: str, filepath: Optional[str] = None) -> Dict:
        """Generate code based on description"""
        
        if not self.current_project:
            console.print("[red]No project loaded! Use 'load' or 'create' first.[/red]")
            return {"success": False}
        
        console.print(f"\n[cyan]Generating code: {description}[/cyan]")
        
        prompt = f"""You are an expert software developer. Generate production-ready code for:

Task: {description}

Project Context:
- Tech Stack: {', '.join(self.project_context.get('tech_stack', []))}
- Existing Files: {', '.join(self.project_context.get('files', [])[:5])}

Requirements:
1. Write clean, well-documented code
2. Include error handling
3. Follow best practices
4. Add type hints (if applicable)
5. Include docstrings

If a filename is specified, write code for that file.
Otherwise, suggest an appropriate filename.

Respond with:
FILE: <filename>
```language
<code>
```
EXPLANATION: <brief explanation>"""

        if filepath:
            prompt += f"\n\nTarget file: {filepath}"
        
        response = self.chat(prompt)
        
        # Parse response
        result = self._parse_code_response(response)
        
        if result['success'] and result.get('filename'):
            # Save to file
            project_path = self.workspace / self.current_project
            file_path = project_path / result['filename']
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(result['code'])
            
            console.print(f"\n[green]✓ Code generated: {result['filename']}[/green]")
            
            # Show the code
            syntax = Syntax(result['code'], result.get('language', 'python'), theme="monokai")
            console.print("\n")
            console.print(syntax)
            
            if result.get('explanation'):
                console.print(f"\n[cyan]{result['explanation']}[/cyan]")
        
        return result
    
    def fix_code(self, filepath: str, error: Optional[str] = None) -> Dict:
        """Fix code errors in a file"""
        
        if not self.current_project:
            console.print("[red]No project loaded![/red]")
            return {"success": False}
        
        project_path = self.workspace / self.current_project
        file_path = project_path / filepath
        
        if not file_path.exists():
            console.print(f"[red]File not found: {filepath}[/red]")
            return {"success": False}
        
        # Read current code
        current_code = file_path.read_text()
        
        console.print(f"\n[cyan]Analyzing and fixing: {filepath}[/cyan]")
        
        prompt = f"""You are a debugging expert. Fix the following code:

File: {filepath}
Current Code:
```
{current_code}
```
"""
        
        if error:
            prompt += f"\n\nError Message:\n{error}"
        else:
            prompt += "\n\nTask: Review code for bugs, errors, and improvements."
        
        prompt += """

Provide:
1. Fixed code
2. Explanation of issues found
3. Suggestions for improvement

Format:
FIXED CODE:
```language
<code>
```

ISSUES FOUND:
- Issue 1
- Issue 2

IMPROVEMENTS:
- Suggestion 1
- Suggestion 2
"""
        
        response = self.chat(prompt)
        
        # Parse and save
        result = self._parse_code_response(response)
        
        if result['success'] and result.get('code'):
            # Backup original
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            backup_path.write_text(current_code)
            
            # Write fixed code
            file_path.write_text(result['code'])
            
            console.print(f"\n[green]✓ Code fixed: {filepath}[/green]")
            console.print(f"[yellow]Original backed up to: {backup_path.name}[/yellow]")
            
            # Show diff
            console.print("\n[bold]Changes:[/bold]")
            console.print(result.get('explanation', 'Code has been fixed'))
        
        return result
    
    def plan_feature(self, description: str) -> Dict:
        """Plan implementation of a new feature"""
        
        console.print(f"\n[cyan]Planning feature: {description}[/cyan]")
        
        prompt = f"""You are a software architect. Create a detailed implementation plan for:

Feature: {description}

Project Context:
{json.dumps(self.project_context, indent=2)}

Provide a comprehensive plan with:
1. Architecture overview
2. Files to create/modify
3. Step-by-step implementation tasks
4. Dependencies needed
5. Testing strategy
6. Potential challenges

Format as JSON:
{{
  "overview": "Brief description",
  "files": [
    {{"path": "file.py", "action": "create/modify", "purpose": "..."}}
  ],
  "tasks": [
    {{"step": 1, "description": "...", "estimated_time": "..."}}
  ],
  "dependencies": ["package1", "package2"],
  "tests": ["test1.py", "test2.py"],
  "challenges": ["challenge1", "challenge2"]
}}

Respond with ONLY valid JSON."""
        
        response = self.chat(prompt)
        
        # Parse JSON
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            plan = json.loads(response[json_start:json_end])
            
            # Display plan
            self._display_plan(plan)
            
            # Save plan
            if self.current_project:
                plan_file = self.workspace / self.current_project / f"plan_{description.replace(' ', '_')[:30]}.json"
                plan_file.write_text(json.dumps(plan, indent=2))
                console.print(f"\n[green]Plan saved to: {plan_file.name}[/green]")
            
            return {"success": True, "plan": plan}
            
        except Exception as e:
            console.print(f"[red]Failed to parse plan: {e}[/red]")
            console.print(response)
            return {"success": False, "error": str(e)}
    
    def _display_plan(self, plan: Dict):
        """Display implementation plan in a nice format"""
        
        console.print("\n" + "="*60)
        console.print("[bold cyan]FEATURE IMPLEMENTATION PLAN[/bold cyan]")
        console.print("="*60)
        
        # Overview
        console.print(f"\n[bold]Overview:[/bold]")
        console.print(plan.get('overview', 'N/A'))
        
        # Files
        if plan.get('files'):
            console.print(f"\n[bold]Files to Change:[/bold]")
            table = Table()
            table.add_column("File", style="cyan")
            table.add_column("Action", style="yellow")
            table.add_column("Purpose", style="white")
            
            for file_info in plan['files']:
                table.add_row(
                    file_info['path'],
                    file_info['action'],
                    file_info['purpose']
                )
            
            console.print(table)
        
        # Tasks
        if plan.get('tasks'):
            console.print(f"\n[bold]Implementation Steps:[/bold]")
            for task in plan['tasks']:
                console.print(f"  {task['step']}. {task['description']} ({task.get('estimated_time', 'N/A')})")
        
        # Dependencies
        if plan.get('dependencies'):
            console.print(f"\n[bold]Dependencies:[/bold] {', '.join(plan['dependencies'])}")
        
        # Challenges
        if plan.get('challenges'):
            console.print(f"\n[bold]Potential Challenges:[/bold]")
            for challenge in plan['challenges']:
                console.print(f"  ⚠ {challenge}")
    
    def _parse_code_response(self, response: str) -> Dict:
        """Parse code from AI response"""
        
        result = {"success": False}
        
        # Extract filename
        if "FILE:" in response:
            filename_line = [l for l in response.split('\n') if 'FILE:' in l][0]
            result['filename'] = filename_line.split('FILE:')[1].strip()
        
        # Extract code block
        if '```' in response:
            parts = response.split('```')
            if len(parts) >= 3:
                code_block = parts[1]
                # Remove language identifier
                lines = code_block.split('\n')
                if lines[0].strip() in ['python', 'javascript', 'typescript', 'java', 'go', 'rust', 'cpp', 'c']:
                    result['language'] = lines[0].strip()
                    code_block = '\n'.join(lines[1:])
                
                result['code'] = code_block.strip()
                result['success'] = True
        
        # Extract explanation
        if "EXPLANATION:" in response:
            expl_part = response.split("EXPLANATION:")[1].strip()
            result['explanation'] = expl_part.split('```')[0].strip()
        
        return result
    
    def list_projects(self):
        """List all projects in workspace"""
        
        projects = []
        for path in self.workspace.iterdir():
            if path.is_dir() and (path / ".perplexity.json").exists():
                metadata = json.loads((path / ".perplexity.json").read_text())
                projects.append({
                    "name": path.name,
                    "tech_stack": metadata.get('tech_stack', []),
                    "template": metadata.get('template', 'custom')
                })
        
        if projects:
            console.print("\n[bold cyan]Projects:[/bold cyan]")
            table = Table()
            table.add_column("Name", style="cyan")
            table.add_column("Tech Stack", style="yellow")
            table.add_column("Template", style="white")
            
            for proj in projects:
                table.add_row(
                    proj['name'],
                    ', '.join(proj['tech_stack'][:3]),
                    proj['template']
                )
            
            console.print(table)
        else:
            console.print("[yellow]No projects found. Create one with 'create'![/yellow]")
    
    def run_tests(self, test_file: Optional[str] = None):
        """Run tests in the project"""
        
        if not self.current_project:
            console.print("[red]No project loaded![/red]")
            return
        
        project_path = self.workspace / self.current_project
        
        # Detect test framework
        if (project_path / "package.json").exists():
            # JavaScript/TypeScript project
            cmd = ["npm", "test"]
        elif any((project_path / "tests").rglob("test_*.py")):
            # Python project with pytest
            cmd = ["pytest"]
            if test_file:
                cmd.append(test_file)
        else:
            console.print("[yellow]No tests found or framework not detected[/yellow]")
            return
        
        console.print(f"\n[cyan]Running tests...[/cyan]")
        
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True
        )
        
        console.print(result.stdout)
        if result.stderr:
            console.print(f"[red]{result.stderr}[/red]")


# CLI Commands

@click.group()
@click.pass_context
def cli(ctx):
    """Perplexity Dev Controller - AI-Powered Development Assistant"""
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        console.print("[red]PERPLEXITY_API_KEY not found![/red]")
        console.print("Run: python dev_controller.py setup")
        sys.exit(1)
    
    ctx.obj = PerplexityDevController(api_key)


@cli.command()
@click.argument('name')
@click.option('--template', default='custom', help='Project template (web, api, cli, ml, custom)')
@click.pass_obj
def create(controller, name, template):
    """Create a new project"""
    
    if template == 'custom':
        description = Prompt.ask("\n[bold]Describe your project[/bold]")
        template = description
    
    result = controller.create_project(name, template)
    
    if result['success']:
        console.print("\n[green]Project created successfully![/green]")
        console.print(f"[cyan]Location: {result['path']}[/cyan]")


@cli.command()
@click.argument('name')
@click.pass_obj
def load(controller, name):
    """Load an existing project"""
    controller.load_project(name)


@cli.command()
@click.pass_obj
def projects(controller):
    """List all projects"""
    controller.list_projects()


@cli.command()
@click.argument('description')
@click.option('--file', help='Target filename')
@click.pass_obj
def generate(controller, description, file):
    """Generate code from description"""
    
    if not controller.current_project:
        console.print("[red]Load a project first: dev_controller.py load <name>[/red]")
        return
    
    controller.generate_code(description, file)


@cli.command()
@click.argument('filepath')
@click.option('--error', help='Error message to fix')
@click.pass_obj
def fix(controller, filepath, error):
    """Fix code errors in a file"""
    controller.fix_code(filepath, error)


@cli.command()
@click.argument('description')
@click.pass_obj
def plan(controller, description):
    """Plan a new feature implementation"""
    controller.plan_feature(description)


@cli.command()
@click.option('--file', help='Specific test file to run')
@click.pass_obj
def test(controller, file):
    """Run project tests"""
    controller.run_tests(file)


@cli.command()
@click.pass_obj
def interactive(controller):
    """Start interactive development session"""
    
    console.print(Panel.fit(
        "[bold cyan]Perplexity Dev Controller - Interactive Mode[/bold cyan]\n\n"
        "Commands:\n"
        "  create <name> - Create new project\n"
        "  load <name> - Load project\n"
        "  gen <description> - Generate code\n"
        "  fix <file> - Fix code\n"
        "  plan <feature> - Plan feature\n"
        "  ask <question> - Ask anything\n"
        "  exit - Quit\n",
        border_style="cyan"
    ))
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold green]dev>[/bold green]")
            
            if user_input.lower() in ['exit', 'quit']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            parts = user_input.split(' ', 1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""
            
            if cmd == 'create':
                controller.create_project(arg, 'custom')
            elif cmd == 'load':
                controller.load_project(arg)
            elif cmd == 'gen':
                controller.generate_code(arg)
            elif cmd == 'fix':
                controller.fix_code(arg)
            elif cmd == 'plan':
                controller.plan_feature(arg)
            elif cmd == 'ask':
                response = controller.chat(arg)
                console.print(f"\n[cyan]{response}[/cyan]")
            else:
                console.print("[yellow]Unknown command. Try: create, load, gen, fix, plan, ask[/yellow]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted[/yellow]")
            continue
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


@cli.command()
def setup():
    """Setup wizard"""
    
    console.print(Panel.fit(
        "[bold cyan]Perplexity Dev Controller Setup[/bold cyan]",
        border_style="cyan"
    ))
    
    api_key = Prompt.ask("\n[bold]Enter your Perplexity API key[/bold]", password=True)
    
    with open('.env', 'w') as f:
        f.write(f"PERPLEXITY_API_KEY={api_key}\n")
    
    console.print("\n[green]✓ Setup complete![/green]")
    console.print("\nTry: python dev_controller.py interactive")


if __name__ == "__main__":
    cli()
