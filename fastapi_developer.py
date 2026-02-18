#!/usr/bin/env python3
"""
FastAPI Backend Development with Circular Review System
Code → Test → Review → Improve cycle
"""

import os
import sys
import json
import asyncio
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pytest
from openai import OpenAI

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class DevelopmentPhase(Enum):
    DESIGN = "design"
    CODING = "coding"
    TESTING = "testing"
    REVIEW = "review"
    REFACTOR = "refactor"
    DEPLOY = "deploy"


@dataclass
class CodeModule:
    """Represents a code module being developed"""
    id: str
    name: str
    description: str
    code: str = ""
    tests: str = ""
    documentation: str = ""
    status: str = "pending"
    version: int = 1
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class DevelopmentTask:
    """Represents a development task in the cycle"""
    id: str
    module_id: str
    phase: DevelopmentPhase
    description: str
    assignee: str  # AI agent role
    requirements: Dict[str, Any]
    result: Optional[Dict] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CodeReview:
    """Represents a code review result"""
    id: str
    module_id: str
    reviewer: str
    score: float  # 0-10
    issues: List[str]
    suggestions: List[str]
    approval: bool
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class FastAPIBackendDeveloper:
    """Main system for FastAPI backend development with circular review"""
    
    def __init__(self, api_key: str, project_path: str = "./fastapi_project"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        self.project_path = Path(project_path)
        self.project_path.mkdir(exist_ok=True)
        
        self.modules: Dict[str, CodeModule] = {}
        self.tasks: List[DevelopmentTask] = []
        self.reviews: Dict[str, List[CodeReview]] = {}
        self.current_cycle = 1
        
        # AI agents for different phases
        self.agents = {
            "architect": "System Architect",
            "developer": "Backend Developer", 
            "tester": "QA Engineer",
            "reviewer": "Code Reviewer",
            "refactorer": "Refactoring Specialist"
        }
        
        self._initialize_project_structure()
    
    def _initialize_project_structure(self):
        """Initialize FastAPI project structure"""
        directories = [
            "app",
            "app/api",
            "app/models",
            "app/schemas",
            "app/core",
            "app/services",
            "tests",
            "tests/unit",
            "tests/integration",
            "docs",
            "scripts"
        ]
        
        for dir_path in directories:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)
        
        # Create initial files
        initial_files = {
            "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
""",
            "app/__init__.py": "",
            "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Generated Backend API",
    description="Auto-generated FastAPI backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
""",
            "app/core/__init__.py": "",
            "app/core/config.py": """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
""",
            "tests/__init__.py": "",
            "tests/conftest.py": """import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
""",
            "pytest.ini": """[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
"""
        }
        
        for file_path, content in initial_files.items():
            full_path = self.project_path / file_path
            full_path.write_text(content)
    
    async def develop_backend_feature(self, feature_description: str) -> Dict:
        """Develop a complete backend feature with circular review process"""
        
        console.print(Panel.fit(
            f"[bold cyan]FastAPI Backend Development[/bold cyan]\n"
            f"Feature: {feature_description}\n"
            f"Cycle: {self.current_cycle}",
            border_style="cyan"
        ))
        
        # Phase 1: Design and Architecture
        console.print("\n[bold]🏗️ Phase 1: Design & Architecture[/bold]")
        design_result = await self._design_feature(feature_description)
        
        # Phase 2: Code Implementation
        console.print("\n[bold]💻 Phase 2: Code Implementation[/bold]")
        code_result = await self._implement_feature(design_result)
        
        # Phase 3: Testing
        console.print("\n[bold]🧪 Phase 3: Testing[/bold]")
        test_result = await self._test_feature(code_result)
        
        # Phase 4: Code Review
        console.print("\n[bold]🔍 Phase 4: Code Review[/bold]")
        review_result = await self._review_code(code_result, test_result)
        
        # Phase 5: Refactoring (if needed)
        if not review_result.get("approval", False):
            console.print("\n[bold]🔧 Phase 5: Refactoring[/bold]")
            refactor_result = await self._refactor_feature(code_result, review_result)
            # Repeat testing and review
            test_result = await self._test_feature(refactor_result)
            review_result = await self._review_code(refactor_result, test_result)
        
        # Phase 6: Documentation
        console.print("\n[bold]📚 Phase 6: Documentation[/bold]")
        docs_result = await self._generate_documentation(code_result, design_result)
        
        # Save everything
        await self._save_development_results(code_result, test_result, review_result, docs_result)
        
        # Increment cycle
        self.current_cycle += 1
        
        return {
            "feature": feature_description,
            "cycle": self.current_cycle - 1,
            "design": design_result,
            "code": code_result,
            "tests": test_result,
            "review": review_result,
            "documentation": docs_result,
            "success": review_result.get("approval", False)
        }
    
    async def _design_feature(self, description: str) -> Dict:
        """Design the feature architecture"""
        
        prompt = f"""
        Design a FastAPI backend feature for: {description}
        
        Provide:
        1. API endpoints (HTTP methods, paths, request/response schemas)
        2. Database models (SQLAlchemy models)
        3. Business logic requirements
        4. Dependencies and integrations
        5. Security considerations
        6. Performance requirements
        
        Be specific and provide complete design specifications.
        """
        
        response = await self._call_llm(prompt, temperature=0.3)
        
        return {
            "description": description,
            "design": response,
            "agent": self.agents["architect"],
            "timestamp": datetime.now()
        }
    
    async def _implement_feature(self, design: Dict) -> Dict:
        """Implement the feature code"""
        
        prompt = f"""
        Based on this design, implement the complete FastAPI code:
        
        {design['design']}
        
        Provide:
        1. FastAPI route implementations
        2. Pydantic schemas for request/response
        3. SQLAlchemy models
        4. Service layer functions
        5. Error handling
        6. Input validation
        
        Write production-ready, clean, and well-documented Python code.
        Follow FastAPI best practices and type hints.
        """
        
        response = await self._call_llm(prompt, temperature=0.1)
        
        # Parse the response to extract different code components
        code_components = self._parse_code_response(response)
        
        return {
            "design": design,
            "code": response,
            "components": code_components,
            "agent": self.agents["developer"],
            "timestamp": datetime.now()
        }
    
    async def _test_feature(self, code_result: Dict) -> Dict:
        """Generate comprehensive tests"""
        
        prompt = f"""
        Create comprehensive tests for this FastAPI implementation:
        
        {code_result['code']}
        
        Provide:
        1. Unit tests for all functions
        2. Integration tests for API endpoints
        3. Test data fixtures
        4. Edge case testing
        5. Error scenario testing
        6. Performance tests if applicable
        
        Use pytest and pytest-asyncio. Include proper assertions and test coverage.
        """
        
        response = await self._call_llm(prompt, temperature=0.2)
        
        return {
            "code": code_result,
            "tests": response,
            "agent": self.agents["tester"],
            "timestamp": datetime.now()
        }
    
    async def _review_code(self, code_result: Dict, test_result: Dict) -> Dict:
        """Review code and tests for quality"""
        
        prompt = f"""
        Review this FastAPI code and tests for production readiness:
        
        CODE:
        {code_result['code']}
        
        TESTS:
        {test_result['tests']}
        
        Evaluate:
        1. Code quality and readability (0-10)
        2. Security vulnerabilities
        3. Performance issues
        4. Best practices compliance
        5. Test coverage and quality
        6. Documentation completeness
        7. Error handling
        
        Provide specific issues found and suggestions for improvement.
        Give an overall approval/rejection decision.
        """
        
        response = await self._call_llm(prompt, temperature=0.1)
        
        # Parse review results
        review_data = self._parse_review_response(response)
        
        return {
            "code": code_result,
            "tests": test_result,
            "review": response,
            "analysis": review_data,
            "agent": self.agents["reviewer"],
            "timestamp": datetime.now()
        }
    
    async def _refactor_feature(self, code_result: Dict, review_result: Dict) -> Dict:
        """Refactor code based on review feedback"""
        
        prompt = f"""
        Refactor this FastAPI code based on the review feedback:
        
        ORIGINAL CODE:
        {code_result['code']}
        
        REVIEW FEEDBACK:
        {review_result['review']}
        
        Address all issues mentioned in the review:
        1. Fix security vulnerabilities
        2. Improve performance
        3. Enhance code quality
        4. Add missing error handling
        5. Improve test coverage
        6. Add better documentation
        
        Provide the refactored, production-ready code.
        """
        
        response = await self._call_llm(prompt, temperature=0.1)
        
        return {
            "original": code_result,
            "review": review_result,
            "refactored": response,
            "agent": self.agents["refactorer"],
            "timestamp": datetime.now()
        }
    
    async def _generate_documentation(self, code_result: Dict, design: Dict) -> Dict:
        """Generate comprehensive documentation"""
        
        prompt = f"""
        Generate comprehensive documentation for this FastAPI feature:
        
        DESIGN:
        {design['design']}
        
        CODE:
        {code_result['code']}
        
        Provide:
        1. API documentation (endpoint descriptions, parameters, responses)
        2. Developer guide
        3. Deployment instructions
        4. Configuration guide
        5. Troubleshooting guide
        6. Example usage
        
        Format as clear, professional documentation.
        """
        
        response = await self._call_llm(prompt, temperature=0.2)
        
        return {
            "design": design,
            "code": code_result,
            "documentation": response,
            "timestamp": datetime.now()
        }
    
    async def _save_development_results(self, code_result: Dict, test_result: Dict, 
                                       review_result: Dict, docs_result: Dict):
        """Save all development results to files"""
        
        # Save code files
        if "components" in code_result:
            for component_name, component_code in code_result["components"].items():
                file_path = self._get_component_path(component_name)
                if file_path:
                    (self.project_path / file_path).write_text(component_code)
        
        # Save tests
        test_file = self.project_path / "tests" / "test_feature.py"
        test_file.write_text(test_result["tests"])
        
        # Save documentation
        docs_file = self.project_path / "docs" / "feature_documentation.md"
        docs_file.write_text(docs_result["documentation"])
        
        # Save review results
        review_file = self.project_path / "docs" / "code_review.json"
        review_data = {
            "review": review_result["review"],
            "analysis": review_result.get("analysis", {}),
            "timestamp": review_result["timestamp"].isoformat()
        }
        review_file.write_text(json.dumps(review_data, indent=2))
    
    def _get_component_path(self, component_name: str) -> Optional[str]:
        """Get file path for a code component"""
        component_paths = {
            "main": "app/main.py",
            "models": "app/models/models.py",
            "schemas": "app/schemas/schemas.py",
            "routes": "app/api/routes.py",
            "services": "app/services/services.py",
            "config": "app/core/config.py"
        }
        return component_paths.get(component_name.lower())
    
    def _parse_code_response(self, response: str) -> Dict[str, str]:
        """Parse code response into components"""
        components = {}
        
        # Simple parsing - look for common patterns
        if "```python" in response:
            code_blocks = response.split("```python")
            for i, block in enumerate(code_blocks[1:], 1):
                if "```" in block:
                    code = block.split("```")[0].strip()
                    # Try to identify component type
                    if "class" in code and "Model" in code:
                        components["models"] = code
                    elif "class" in code and "Schema" in code:
                        components["schemas"] = code
                    elif "@app." in code or "router" in code:
                        components["routes"] = code
                    elif "def " in code and "service" in code.lower():
                        components["services"] = code
                    else:
                        components[f"component_{i}"] = code
        
        return components
    
    def _parse_review_response(self, response: str) -> Dict:
        """Parse review response for structured data"""
        # Simple parsing - look for score and approval
        analysis = {
            "score": 7.0,  # Default score
            "approval": False,
            "issues": [],
            "suggestions": []
        }
        
        lines = response.split('\n')
        for line in lines:
            if "score" in line.lower() or "/" in line:
                try:
                    # Extract score like "7/10" or "Score: 7"
                    if "/" in line:
                        score_part = line.split("/")[0].split()[-1]
                        analysis["score"] = float(score_part)
                    elif ":" in line:
                        score_part = line.split(":")[1].strip().split()[0]
                        analysis["score"] = float(score_part)
                except:
                    pass
            elif "approve" in line.lower():
                analysis["approval"] = "approved" in line.lower() or "yes" in line.lower()
        
        return analysis
    
    async def _call_llm(self, prompt: str, temperature: float = 0.3) -> str:
        """Call the language model"""
        try:
            response = self.client.chat.completions.create(
                model="sonar",
                messages=[
                    {"role": "system", "content": "You are an expert FastAPI backend developer and architect."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]LLM call failed: {e}[/red]")
            return f"Error: {str(e)}"
    
    def run_tests(self) -> Dict:
        """Run the test suite"""
        try:
            result = subprocess.run(
                ["pytest", "tests/", "-v"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Tests timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def start_server(self, port: int = 8000) -> Dict:
        """Start the FastAPI development server"""
        try:
            # This would normally run in background
            console.print(f"[green]Starting FastAPI server on port {port}[/green]")
            console.print(f"[yellow]Run this command to start:[/yellow]")
            console.print(f"cd {self.project_path} && uvicorn app.main:app --reload --port {port}")
            
            return {
                "success": True,
                "port": port,
                "command": f"uvicorn app.main:app --reload --port {port}",
                "cwd": str(self.project_path)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_project_status(self) -> Dict:
        """Get current project status"""
        
        # Count files
        python_files = list(self.project_path.rglob("*.py"))
        test_files = list(self.project_path.glob("tests/**/*.py"))
        
        # Run tests
        test_results = self.run_tests()
        
        return {
            "project_path": str(self.project_path),
            "python_files": len(python_files),
            "test_files": len(test_files),
            "development_cycles": self.current_cycle - 1,
            "test_status": "passed" if test_results["success"] else "failed",
            "last_test_output": test_results.get("output", "")[:500]
        }


# CLI Interface
import click

@click.group()
@click.option('--api-key', envvar='PERPLEXITY_API_KEY', help='Perplexity API key')
@click.option('--project-path', default='./fastapi_project', help='Project directory')
@click.pass_context
def cli(ctx, api_key, project_path):
    """FastAPI Backend Development with Circular Review System"""
    ctx.ensure_object(dict)
    ctx.obj['developer'] = FastAPIBackendDeveloper(api_key, project_path)

@cli.command()
@click.argument('feature')
@click.pass_context
def develop(ctx, feature):
    """Develop a backend feature with circular review"""
    developer = ctx.obj['developer']
    
    async def run_development():
        result = await developer.develop_backend_feature(feature)
        
        console.print("\n[bold green]🎉 Development Complete![/bold green]")
        console.print(f"Feature: {result['feature']}")
        console.print(f"Cycle: {result['cycle']}")
        console.print(f"Success: {result['success']}")
        
        if result['success']:
            console.print("\n[bold]✅ Approved for deployment![/bold]")
        else:
            console.print("\n[bold]⚠️  Needs more work[/bold]")
    
    asyncio.run(run_development())

@cli.command()
@click.pass_context
def test(ctx):
    """Run the test suite"""
    developer = ctx.obj['developer']
    results = developer.run_tests()
    
    if results["success"]:
        console.print("[bold green]✅ All tests passed![/bold]")
    else:
        console.print("[bold red]❌ Tests failed![/bold]")
    
    console.print(results["output"])

@cli.command()
@click.option('--port', default=8000, help='Port to run server on')
@click.pass_context
def serve(ctx, port):
    """Start the FastAPI development server"""
    developer = ctx.obj['developer']
    result = developer.start_server(port)
    
    if result["success"]:
        console.print(f"[green]Server command ready:[/green]")
        console.print(f"cd {result['cwd']} && {result['command']}")
    else:
        console.print(f"[red]Error: {result['error']}[/red]")

@cli.command()
@click.pass_context
def status(ctx):
    """Show project status"""
    developer = ctx.obj['developer']
    status = developer.get_project_status()
    
    console.print("\n[bold]📊 Project Status:[/bold]")
    console.print(f"Path: {status['project_path']}")
    console.print(f"Python Files: {status['python_files']}")
    console.print(f"Test Files: {status['test_files']}")
    console.print(f"Development Cycles: {status['development_cycles']}")
    console.print(f"Test Status: {status['test_status']}")

if __name__ == "__main__":
    cli()
