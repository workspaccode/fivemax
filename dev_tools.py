#!/usr/bin/env python3
"""
Development Tools Integration
Git, Docker, NPM, pip, and other development tool integrations
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Dict
import json


class GitIntegration:
    """Git version control integration"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
    
    def init(self, initial_branch: str = "main") -> bool:
        """Initialize git repository"""
        try:
            subprocess.run(["git", "init"], cwd=self.project_path, check=True)
            subprocess.run(["git", "branch", "-M", initial_branch], cwd=self.project_path, check=True)
            
            # Create .gitignore
            gitignore_content = self._generate_gitignore()
            (self.project_path / ".gitignore").write_text(gitignore_content)
            
            return True
        except subprocess.CalledProcessError:
            return False
    
    def commit(self, message: str, add_all: bool = True) -> bool:
        """Commit changes"""
        try:
            if add_all:
                subprocess.run(["git", "add", "."], cwd=self.project_path, check=True)
            
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def create_branch(self, branch_name: str) -> bool:
        """Create and checkout new branch"""
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.project_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def status(self) -> str:
        """Get git status"""
        try:
            result = subprocess.run(
                ["git", "status"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
    
    def diff(self, file: Optional[str] = None) -> str:
        """Get git diff"""
        try:
            cmd = ["git", "diff"]
            if file:
                cmd.append(file)
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
    
    def push(self, remote: str = "origin", branch: str = "main") -> bool:
        """Push to remote"""
        try:
            subprocess.run(
                ["git", "push", remote, branch],
                cwd=self.project_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _generate_gitignore(self) -> str:
        """Generate .gitignore content"""
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log
yarn-error.log
.npm
.yarn

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Logs
*.log
logs/

# Testing
.coverage
htmlcov/
.pytest_cache/

# Build
dist/
build/
*.egg-info/
"""


class DockerIntegration:
    """Docker containerization integration"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
    
    def build(self, tag: str, dockerfile: str = "Dockerfile") -> Dict:
        """Build Docker image"""
        try:
            result = subprocess.run(
                ["docker", "build", "-t", tag, "-f", dockerfile, "."],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
    
    def run(self, image: str, ports: Optional[Dict[int, int]] = None, env: Optional[Dict] = None) -> Dict:
        """Run Docker container"""
        try:
            cmd = ["docker", "run", "-d"]
            
            # Add port mappings
            if ports:
                for host_port, container_port in ports.items():
                    cmd.extend(["-p", f"{host_port}:{container_port}"])
            
            # Add environment variables
            if env:
                for key, value in env.items():
                    cmd.extend(["-e", f"{key}={value}"])
            
            cmd.append(image)
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {"success": True, "container_id": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
    
    def compose_up(self, file: str = "docker-compose.yml") -> Dict:
        """Start docker-compose services"""
        try:
            result = subprocess.run(
                ["docker-compose", "-f", file, "up", "-d"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
    
    def compose_down(self, file: str = "docker-compose.yml") -> Dict:
        """Stop docker-compose services"""
        try:
            result = subprocess.run(
                ["docker-compose", "-f", file, "down"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}


class PackageManagerIntegration:
    """Package manager integration (npm, pip, etc.)"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.manager = self._detect_manager()
    
    def _detect_manager(self) -> str:
        """Detect package manager"""
        if (self.project_path / "package.json").exists():
            return "npm"
        elif (self.project_path / "requirements.txt").exists():
            return "pip"
        elif (self.project_path / "Cargo.toml").exists():
            return "cargo"
        elif (self.project_path / "go.mod").exists():
            return "go"
        else:
            return "unknown"
    
    def install(self, package: Optional[str] = None) -> Dict:
        """Install package or all dependencies"""
        try:
            if self.manager == "npm":
                cmd = ["npm", "install"]
                if package:
                    cmd.append(package)
            elif self.manager == "pip":
                if package:
                    cmd = ["pip", "install", package, "--break-system-packages"]
                else:
                    cmd = ["pip", "install", "-r", "requirements.txt", "--break-system-packages"]
            elif self.manager == "cargo":
                cmd = ["cargo", "build"]
            elif self.manager == "go":
                cmd = ["go", "mod", "download"]
            else:
                return {"success": False, "error": "Unknown package manager"}
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
    
    def run_script(self, script: str) -> Dict:
        """Run package manager script"""
        try:
            if self.manager == "npm":
                cmd = ["npm", "run", script]
            elif self.manager == "cargo":
                cmd = ["cargo", "run"]
            elif self.manager == "go":
                cmd = ["go", "run", "."]
            else:
                return {"success": False, "error": "Scripts not supported for this manager"}
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
    
    def test(self) -> Dict:
        """Run tests"""
        try:
            if self.manager == "npm":
                cmd = ["npm", "test"]
            elif self.manager == "pip":
                cmd = ["pytest"]
            elif self.manager == "cargo":
                cmd = ["cargo", "test"]
            elif self.manager == "go":
                cmd = ["go", "test", "./..."]
            else:
                return {"success": False, "error": "Testing not configured"}
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}


class CodeFormatter:
    """Code formatting and linting integration"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
    
    def format_python(self, file: Optional[str] = None) -> Dict:
        """Format Python code with black"""
        try:
            cmd = ["black"]
            if file:
                cmd.append(file)
            else:
                cmd.append(".")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
        except FileNotFoundError:
            return {"success": False, "error": "black not installed"}
    
    def lint_python(self, file: Optional[str] = None) -> Dict:
        """Lint Python code with flake8"""
        try:
            cmd = ["flake8"]
            if file:
                cmd.append(file)
            else:
                cmd.append(".")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "issues": result.stdout.split('\n') if result.returncode != 0 else []
            }
        except FileNotFoundError:
            return {"success": False, "error": "flake8 not installed"}
    
    def format_javascript(self, file: Optional[str] = None) -> Dict:
        """Format JavaScript/TypeScript with prettier"""
        try:
            cmd = ["npx", "prettier", "--write"]
            if file:
                cmd.append(file)
            else:
                cmd.append(".")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
    
    def lint_javascript(self, file: Optional[str] = None) -> Dict:
        """Lint JavaScript with eslint"""
        try:
            cmd = ["npx", "eslint"]
            if file:
                cmd.append(file)
            else:
                cmd.append(".")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "issues": result.stdout.split('\n') if result.returncode != 0 else []
            }
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}


class ProjectScaffold:
    """Project scaffolding utilities"""
    
    @staticmethod
    def create_python_project(path: Path, name: str) -> Dict:
        """Create Python project structure"""
        
        # Create directories
        dirs = [
            path / name,
            path / "tests",
            path / "docs",
        ]
        
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)
        
        # Create files
        files = {
            "README.md": f"# {name}\n\nProject description here.",
            "requirements.txt": "# Add your dependencies here\n",
            "setup.py": f"""from setuptools import setup, find_packages

setup(
    name="{name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
)
""",
            f"{name}/__init__.py": f'"""{ name} package"""',
            f"{name}/main.py": """def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""",
            "tests/__init__.py": "",
            "tests/test_main.py": f"""import pytest
from {name}.main import main

def test_main():
    # Add your tests here
    pass
""",
            ".gitignore": GitIntegration(path)._generate_gitignore()
        }
        
        for filepath, content in files.items():
            file_path = path / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        
        return {"success": True, "structure": list(files.keys())}
    
    @staticmethod
    def create_nodejs_project(path: Path, name: str) -> Dict:
        """Create Node.js project structure"""
        
        # Create directories
        dirs = [
            path / "src",
            path / "tests",
            path / "docs",
        ]
        
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)
        
        # Create package.json
        package_json = {
            "name": name,
            "version": "1.0.0",
            "description": "",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "test": "jest",
                "dev": "nodemon src/index.js"
            },
            "keywords": [],
            "author": "",
            "license": "MIT",
            "dependencies": {},
            "devDependencies": {
                "jest": "^29.0.0",
                "nodemon": "^3.0.0"
            }
        }
        
        files = {
            "package.json": json.dumps(package_json, indent=2),
            "README.md": f"# {name}\n\nProject description here.",
            "src/index.js": """console.log('Hello, World!');

module.exports = {};
""",
            "tests/index.test.js": """describe('Example Test', () => {
  test('should pass', () => {
    expect(true).toBe(true);
  });
});
""",
            ".gitignore": "node_modules/\n.env\n*.log\n"
        }
        
        for filepath, content in files.items():
            file_path = path / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        
        return {"success": True, "structure": list(files.keys())}
    
    @staticmethod
    def create_fastapi_project(path: Path, name: str) -> Dict:
        """Create FastAPI project structure"""
        
        dirs = [
            path / "app",
            path / "app" / "api",
            path / "app" / "models",
            path / "app" / "schemas",
            path / "tests",
        ]
        
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)
        
        files = {
            "README.md": f"# {name}\n\nFastAPI application",
            "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
""",
            "app/__init__.py": "",
            "app/main.py": """from fastapi import FastAPI

app = FastAPI(title="$name")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
""",
            "app/api/__init__.py": "",
            "app/models/__init__.py": "",
            "app/schemas/__init__.py": "",
            "tests/__init__.py": "",
            "tests/test_main.py": """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
""",
            ".gitignore": GitIntegration(path)._generate_gitignore()
        }
        
        for filepath, content in files.items():
            file_path = path / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content.replace("$name", name))
        
        return {"success": True, "structure": list(files.keys())}


if __name__ == "__main__":
    # Example usage
    project_path = Path("./test_project")
    project_path.mkdir(exist_ok=True)
    
    # Initialize git
    git = GitIntegration(project_path)
    git.init()
    print("Git initialized")
    
    # Create Python project
    scaffold = ProjectScaffold()
    scaffold.create_python_project(project_path, "myapp")
    print("Project created")
