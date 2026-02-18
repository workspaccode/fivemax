#!/usr/bin/env python3
"""
Tool Execution Framework for Advanced Agentic System
Provides real-world tool integrations and execution capabilities
"""

import os
import sys
import json
import subprocess
import requests
import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
import uuid
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class ToolType(Enum):
    FILE_SYSTEM = "file_system"
    WEB_SEARCH = "web_search"
    API_CALL = "api_call"
    CODE_EXECUTION = "code_execution"
    DATABASE = "database"
    SHELL = "shell"
    GIT = "git"
    DOCKER = "docker"


@dataclass
class Tool:
    """Represents a tool that agents can use"""
    id: str
    name: str
    type: ToolType
    description: str
    parameters: Dict[str, Any]
    required_permissions: List[str]
    safe_execution: bool = True


@dataclass
class ToolExecution:
    """Represents a tool execution result"""
    id: str
    tool_id: str
    parameters: Dict[str, Any]
    result: Any
    success: bool
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class FileSystemTools:
    """File system manipulation tools"""
    
    @staticmethod
    def read_file(file_path: str) -> Dict:
        """Read file contents"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"success": False, "error": f"File not found: {file_path}"}
            
            content = path.read_text(encoding='utf-8')
            return {
                "success": True,
                "content": content,
                "size": len(content),
                "lines": len(content.split('\n'))
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def write_file(file_path: str, content: str) -> Dict:
        """Write content to file"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            return {
                "success": True,
                "bytes_written": len(content.encode('utf-8'))
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def list_directory(dir_path: str, recursive: bool = False) -> Dict:
        """List directory contents"""
        try:
            path = Path(dir_path)
            if not path.exists():
                return {"success": False, "error": f"Directory not found: {dir_path}"}
            
            if recursive:
                items = list(path.rglob('*'))
            else:
                items = list(path.iterdir())
            
            file_list = []
            for item in items:
                file_list.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
                })
            
            return {"success": True, "items": file_list}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def create_directory(dir_path: str) -> Dict:
        """Create directory"""
        try:
            path = Path(dir_path)
            path.mkdir(parents=True, exist_ok=True)
            return {"success": True, "path": str(path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_path(path_str: str, recursive: bool = False) -> Dict:
        """Delete file or directory"""
        try:
            path = Path(path_str)
            if not path.exists():
                return {"success": False, "error": f"Path not found: {path_str}"}
            
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                if recursive:
                    import shutil
                    shutil.rmtree(path)
                else:
                    path.rmdir()
            
            return {"success": True, "deleted": str(path)}
        except Exception as e:
            return {"success": False, "error": str(e)}


class WebTools:
    """Web interaction tools"""
    
    @staticmethod
    def web_search(query: str, max_results: int = 10) -> Dict:
        """Perform web search (using a free search API)"""
        try:
            # Using DuckDuckGo instant answer API as example
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "query": query,
                    "results": data.get("RelatedTopics", [])[:max_results],
                    "abstract": data.get("Abstract", ""),
                    "answer": data.get("Answer", "")
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def fetch_url(url: str, method: str = "GET", headers: Dict = None, 
                  data: Dict = None) -> Dict:
        """Fetch content from URL"""
        try:
            headers = headers or {}
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}
            
            return {
                "success": True,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text[:10000],  # Limit content size
                "content_type": response.headers.get("content-type", "")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class CodeExecutionTools:
    """Code execution tools"""
    
    @staticmethod
    def execute_python(code: str, timeout: int = 30) -> Dict:
        """Execute Python code safely"""
        try:
            import tempfile
            import sys
            from io import StringIO
            import contextlib
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Capture output
                old_stdout = sys.stdout
                sys.stdout = captured_output = StringIO()
                
                # Execute with timeout
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Code execution timed out")
                
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout)
                
                # Execute the code
                exec_globals = {}
                with open(temp_file, 'r') as f:
                    exec(f.read(), exec_globals)
                
                signal.alarm(0)  # Cancel timeout
                
                # Get output
                output = captured_output.getvalue()
                
                return {
                    "success": True,
                    "output": output,
                    "execution_time": timeout
                }
                
            finally:
                sys.stdout = old_stdout
                os.unlink(temp_file)
                
        except TimeoutError:
            return {"success": False, "error": "Code execution timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def execute_shell(command: str, timeout: int = 30, cwd: str = None) -> Dict:
        """Execute shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "execution_time": timeout
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command execution timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GitTools:
    """Git version control tools"""
    
    @staticmethod
    def git_status(repo_path: str = ".") -> Dict:
        """Get git status"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n')
            modified_files = []
            untracked_files = []
            
            for line in lines:
                if line.startswith(' M'):
                    modified_files.append(line[3:])
                elif line.startswith('??'):
                    untracked_files.append(line[3:])
            
            return {
                "success": True,
                "modified": modified_files,
                "untracked": untracked_files,
                "clean": len(modified_files) == 0 and len(untracked_files) == 0
            }
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def git_commit(message: str, files: List[str] = None, repo_path: str = ".") -> Dict:
        """Commit changes"""
        try:
            # Add files
            if files:
                subprocess.run(
                    ["git", "add"] + files,
                    cwd=repo_path,
                    check=True
                )
            else:
                subprocess.run(
                    ["git", "add", "."],
                    cwd=repo_path,
                    check=True
                )
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {"success": True, "message": message, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ToolExecutor:
    """Main tool execution engine"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.execution_history: List[ToolExecution] = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default set of tools"""
        
        # File system tools
        self.register_tool(Tool(
            id="read_file",
            name="Read File",
            type=ToolType.FILE_SYSTEM,
            description="Read contents of a file",
            parameters={"file_path": {"type": "string", "required": True}},
            required_permissions=["file_read"]
        ))
        
        self.register_tool(Tool(
            id="write_file",
            name="Write File",
            type=ToolType.FILE_SYSTEM,
            description="Write content to a file",
            parameters={
                "file_path": {"type": "string", "required": True},
                "content": {"type": "string", "required": True}
            },
            required_permissions=["file_write"]
        ))
        
        self.register_tool(Tool(
            id="list_directory",
            name="List Directory",
            type=ToolType.FILE_SYSTEM,
            description="List contents of a directory",
            parameters={
                "dir_path": {"type": "string", "required": True},
                "recursive": {"type": "boolean", "default": False}
            },
            required_permissions=["file_read"]
        ))
        
        # Web tools
        self.register_tool(Tool(
            id="web_search",
            name="Web Search",
            type=ToolType.WEB_SEARCH,
            description="Search the web for information",
            parameters={
                "query": {"type": "string", "required": True},
                "max_results": {"type": "integer", "default": 10}
            },
            required_permissions=["web_access"]
        ))
        
        self.register_tool(Tool(
            id="fetch_url",
            name="Fetch URL",
            type=ToolType.WEB_SEARCH,
            description="Fetch content from a URL",
            parameters={
                "url": {"type": "string", "required": True},
                "method": {"type": "string", "default": "GET"},
                "headers": {"type": "object", "default": {}},
                "data": {"type": "object", "default": {}}
            },
            required_permissions=["web_access"]
        ))
        
        # Code execution tools
        self.register_tool(Tool(
            id="execute_python",
            name="Execute Python",
            type=ToolType.CODE_EXECUTION,
            description="Execute Python code",
            parameters={
                "code": {"type": "string", "required": True},
                "timeout": {"type": "integer", "default": 30}
            },
            required_permissions=["code_execution"],
            safe_execution=False  # Potentially dangerous
        ))
        
        self.register_tool(Tool(
            id="execute_shell",
            name="Execute Shell",
            type=ToolType.SHELL,
            description="Execute shell command",
            parameters={
                "command": {"type": "string", "required": True},
                "timeout": {"type": "integer", "default": 30},
                "cwd": {"type": "string", "default": None}
            },
            required_permissions=["shell_access"],
            safe_execution=False  # Potentially dangerous
        ))
        
        # Git tools
        self.register_tool(Tool(
            id="git_status",
            name="Git Status",
            type=ToolType.GIT,
            description="Get git repository status",
            parameters={"repo_path": {"type": "string", "default": "."}},
            required_permissions=["git_access"]
        ))
        
        self.register_tool(Tool(
            id="git_commit",
            name="Git Commit",
            type=ToolType.GIT,
            description="Commit changes to git",
            parameters={
                "message": {"type": "string", "required": True},
                "files": {"type": "array", "default": None},
                "repo_path": {"type": "string", "default": "."}
            },
            required_permissions=["git_write"]
        ))
    
    def register_tool(self, tool: Tool):
        """Register a new tool"""
        self.tools[tool.id] = tool
    
    def execute_tool(self, tool_id: str, parameters: Dict, 
                    user_permissions: List[str] = None) -> ToolExecution:
        """Execute a tool with given parameters"""
        
        if tool_id not in self.tools:
            return ToolExecution(
                id=str(uuid.uuid4()),
                tool_id=tool_id,
                parameters=parameters,
                result=None,
                success=False,
                error=f"Tool not found: {tool_id}"
            )
        
        tool = self.tools[tool_id]
        
        # Check permissions
        user_permissions = user_permissions or []
        missing_perms = [p for p in tool.required_permissions 
                        if p not in user_permissions]
        if missing_perms:
            return ToolExecution(
                id=str(uuid.uuid4()),
                tool_id=tool_id,
                parameters=parameters,
                result=None,
                success=False,
                error=f"Missing permissions: {missing_perms}"
            )
        
        # Validate parameters
        missing_params = [p for p, spec in tool.parameters.items() 
                         if spec.get("required", False) and p not in parameters]
        if missing_params:
            return ToolExecution(
                id=str(uuid.uuid4()),
                tool_id=tool_id,
                parameters=parameters,
                result=None,
                success=False,
                error=f"Missing required parameters: {missing_params}"
            )
        
        # Execute tool
        start_time = datetime.now()
        
        try:
            if tool_id == "read_file":
                result = FileSystemTools.read_file(parameters["file_path"])
            elif tool_id == "write_file":
                result = FileSystemTools.write_file(
                    parameters["file_path"], parameters["content"]
                )
            elif tool_id == "list_directory":
                result = FileSystemTools.list_directory(
                    parameters["dir_path"], parameters.get("recursive", False)
                )
            elif tool_id == "web_search":
                result = WebTools.web_search(
                    parameters["query"], parameters.get("max_results", 10)
                )
            elif tool_id == "fetch_url":
                result = WebTools.fetch_url(
                    parameters["url"],
                    parameters.get("method", "GET"),
                    parameters.get("headers", {}),
                    parameters.get("data", {})
                )
            elif tool_id == "execute_python":
                result = CodeExecutionTools.execute_python(
                    parameters["code"], parameters.get("timeout", 30)
                )
            elif tool_id == "execute_shell":
                result = CodeExecutionTools.execute_shell(
                    parameters["command"],
                    parameters.get("timeout", 30),
                    parameters.get("cwd")
                )
            elif tool_id == "git_status":
                result = GitTools.git_status(parameters.get("repo_path", "."))
            elif tool_id == "git_commit":
                result = GitTools.git_commit(
                    parameters["message"],
                    parameters.get("files"),
                    parameters.get("repo_path", ".")
                )
            else:
                result = {"success": False, "error": f"Unknown tool: {tool_id}"}
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            execution = ToolExecution(
                id=str(uuid.uuid4()),
                tool_id=tool_id,
                parameters=parameters,
                result=result,
                success=result.get("success", False),
                error=result.get("error") if not result.get("success", False) else None,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            execution = ToolExecution(
                id=str(uuid.uuid4()),
                tool_id=tool_id,
                parameters=parameters,
                result=None,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
        
        self.execution_history.append(execution)
        return execution
    
    def list_tools(self) -> List[Tool]:
        """List all available tools"""
        return list(self.tools.values())
    
    def get_execution_history(self, limit: int = 50) -> List[ToolExecution]:
        """Get recent execution history"""
        return self.execution_history[-limit:]
    
    def display_tools(self):
        """Display available tools in a table"""
        table = Table(title="Available Tools")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Description", style="white")
        table.add_column("Safe", style="red")
        
        for tool in self.tools.values():
            table.add_row(
                tool.id,
                tool.name,
                tool.type.value,
                tool.description[:50] + "..." if len(tool.description) > 50 else tool.description,
                "✓" if tool.safe_execution else "⚠"
            )
        
        console.print(table)


if __name__ == "__main__":
    # Example usage
    executor = ToolExecutor()
    
    # Display available tools
    executor.display_tools()
    
    # Example tool execution
    result = executor.execute_tool(
        "read_file",
        {"file_path": __file__},
        user_permissions=["file_read"]
    )
    
    console.print(f"\n[bold]Execution Result:[/bold]")
    console.print(f"Success: {result.success}")
    if result.success:
        console.print(f"Content length: {len(result.result['content'])}")
    else:
        console.print(f"Error: {result.error}")
