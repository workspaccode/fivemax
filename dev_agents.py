#!/usr/bin/env python3
"""
Advanced Development Agents
Specialized AI agents for complex development tasks
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

load_dotenv()


class DevAgent:
    """Base development agent"""
    
    def __init__(self, api_key: str, role: str):
        self.api_key = api_key
        self.role = role
        self.model = "sonar"
        self.context = []
    
    def _call_ai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Perplexity API"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(self.context[-5:])  # Last 5 messages
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            self.context.append({"role": "user", "content": prompt})
            self.context.append({"role": "assistant", "content": content})
            return content
        else:
            raise Exception(f"API Error: {response.status_code}")


class ArchitectAgent(DevAgent):
    """Software architecture and design agent"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "architect")
        self.system_prompt = """You are a senior software architect with expertise in:
- System design and architecture patterns
- Database design and optimization
- API design (REST, GraphQL, gRPC)
- Microservices and distributed systems
- Security best practices
- Scalability and performance
- Cloud architecture (AWS, GCP, Azure)"""
    
    def design_architecture(self, requirements: str) -> Dict:
        """Design system architecture"""
        
        prompt = f"""Design a comprehensive software architecture for:

{requirements}

Provide a detailed architecture document with:
1. System overview and components
2. Technology stack recommendations
3. Database schema design
4. API endpoints design
5. Security considerations
6. Scalability strategy
7. Deployment architecture
8. Monitoring and logging

Format as JSON with these sections."""
        
        response = self._call_ai(prompt, self.system_prompt)
        return self._parse_json(response)
    
    def review_architecture(self, architecture_doc: str) -> Dict:
        """Review existing architecture"""
        
        prompt = f"""Review this architecture and provide:
1. Strengths
2. Weaknesses and potential issues
3. Improvement recommendations
4. Security concerns
5. Scalability concerns

Architecture:
{architecture_doc}

Respond in JSON format."""
        
        response = self._call_ai(prompt, self.system_prompt)
        return self._parse_json(response)
    
    def _parse_json(self, response: str) -> Dict:
        """Extract JSON from response"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"raw_response": response}


class CodeReviewAgent(DevAgent):
    """Code review and quality assurance agent"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "code_reviewer")
        self.system_prompt = """You are an expert code reviewer focusing on:
- Code quality and best practices
- Performance optimization
- Security vulnerabilities
- Design patterns
- SOLID principles
- Testing and maintainability
- Documentation quality"""
    
    def review_code(self, code: str, language: str, filepath: str = "") -> Dict:
        """Perform comprehensive code review"""
        
        prompt = f"""Review this {language} code and provide detailed feedback:

File: {filepath}
```{language}
{code}
```

Analyze:
1. Code Quality (1-10)
2. Security Issues
3. Performance Issues
4. Best Practices Violations
5. Suggested Improvements
6. Refactoring Opportunities

Respond in JSON format with:
{{
  "score": <1-10>,
  "security_issues": [],
  "performance_issues": [],
  "code_smells": [],
  "suggestions": [],
  "refactoring": []
}}"""
        
        response = self._call_ai(prompt, self.system_prompt)
        return self._parse_json(response)
    
    def suggest_refactoring(self, code: str, language: str) -> str:
        """Suggest code refactoring"""
        
        prompt = f"""Refactor this {language} code following best practices:

```{language}
{code}
```

Provide:
1. Refactored code
2. Explanation of changes
3. Benefits of refactoring

Format:
REFACTORED:
```{language}
<code>
```

CHANGES:
- Change 1
- Change 2

BENEFITS:
- Benefit 1"""
        
        return self._call_ai(prompt, self.system_prompt)
    
    def _parse_json(self, response: str) -> Dict:
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"raw_response": response}


class TestingAgent(DevAgent):
    """Testing and QA automation agent"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "tester")
        self.system_prompt = """You are a testing expert specializing in:
- Unit testing
- Integration testing
- End-to-end testing
- Test-driven development (TDD)
- Testing frameworks (pytest, jest, junit)
- Mocking and fixtures
- Code coverage"""
    
    def generate_tests(self, code: str, language: str, framework: str = "auto") -> str:
        """Generate comprehensive tests"""
        
        if framework == "auto":
            framework = self._detect_framework(language)
        
        prompt = f"""Generate comprehensive tests for this {language} code using {framework}:

```{language}
{code}
```

Include:
1. Unit tests for all functions/methods
2. Edge case tests
3. Error handling tests
4. Mocking where appropriate
5. Test fixtures/setup

Provide complete, runnable test code."""
        
        return self._call_ai(prompt, self.system_prompt)
    
    def analyze_coverage(self, code: str, tests: str, language: str) -> Dict:
        """Analyze test coverage"""
        
        prompt = f"""Analyze test coverage for:

Code:
```{language}
{code}
```

Tests:
```{language}
{tests}
```

Provide:
1. Estimated coverage percentage
2. Uncovered code paths
3. Missing test cases
4. Improvement suggestions

Respond in JSON."""
        
        response = self._call_ai(prompt, self.system_prompt)
        return self._parse_json(response)
    
    def _detect_framework(self, language: str) -> str:
        """Detect appropriate testing framework"""
        frameworks = {
            "python": "pytest",
            "javascript": "jest",
            "typescript": "jest",
            "java": "junit",
            "go": "testing",
            "rust": "cargo test"
        }
        return frameworks.get(language.lower(), "unittest")
    
    def _parse_json(self, response: str) -> Dict:
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"raw_response": response}


class DeploymentAgent(DevAgent):
    """Deployment and DevOps agent"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "devops")
        self.system_prompt = """You are a DevOps expert specializing in:
- CI/CD pipelines
- Docker and containerization
- Kubernetes orchestration
- Cloud platforms (AWS, GCP, Azure)
- Infrastructure as Code (Terraform, CloudFormation)
- Monitoring and logging
- Security and compliance"""
    
    def generate_dockerfile(self, project_info: Dict) -> str:
        """Generate optimized Dockerfile"""
        
        prompt = f"""Generate an optimized Dockerfile for:

Project: {project_info.get('name')}
Language: {project_info.get('language')}
Framework: {project_info.get('framework')}
Dependencies: {project_info.get('dependencies', [])}

Include:
1. Multi-stage build
2. Security best practices
3. Minimal image size
4. Health checks
5. Non-root user

Provide complete Dockerfile with comments."""
        
        return self._call_ai(prompt, self.system_prompt)
    
    def generate_ci_pipeline(self, platform: str, project_info: Dict) -> str:
        """Generate CI/CD pipeline configuration"""
        
        prompt = f"""Generate a {platform} CI/CD pipeline for:

{json.dumps(project_info, indent=2)}

Include:
1. Build stage
2. Test stage
3. Security scanning
4. Docker image building
5. Deployment stage
6. Rollback strategy

Provide complete pipeline configuration file."""
        
        return self._call_ai(prompt, self.system_prompt)
    
    def generate_k8s_manifests(self, app_info: Dict) -> Dict:
        """Generate Kubernetes manifests"""
        
        prompt = f"""Generate Kubernetes manifests for:

{json.dumps(app_info, indent=2)}

Create:
1. Deployment
2. Service
3. ConfigMap
4. Secret (template)
5. Ingress
6. HorizontalPodAutoscaler

Respond with JSON: {{"filename": "content"}}"""
        
        response = self._call_ai(prompt, self.system_prompt)
        return self._parse_json(response)
    
    def _parse_json(self, response: str) -> Dict:
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"raw_response": response}


class DocumentationAgent(DevAgent):
    """Documentation generation agent"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "documenter")
        self.system_prompt = """You are a technical documentation expert focusing on:
- API documentation
- User guides
- Developer documentation
- README files
- Code comments
- Architecture documentation
- Tutorials and examples"""
    
    def generate_readme(self, project_path: Path) -> str:
        """Generate comprehensive README"""
        
        # Analyze project
        project_info = self._analyze_project(project_path)
        
        prompt = f"""Generate a comprehensive README.md for:

{json.dumps(project_info, indent=2)}

Include:
1. Project title and description
2. Features
3. Installation instructions
4. Usage examples
5. API documentation (if applicable)
6. Configuration
7. Contributing guidelines
8. License

Use proper markdown formatting."""
        
        return self._call_ai(prompt, self.system_prompt)
    
    def generate_api_docs(self, code: str, language: str) -> str:
        """Generate API documentation"""
        
        prompt = f"""Generate comprehensive API documentation for this {language} code:

```{language}
{code}
```

Include:
1. Endpoints/Functions overview
2. Request/Response formats
3. Parameters description
4. Examples
5. Error codes
6. Authentication (if applicable)

Use markdown format."""
        
        return self._call_ai(prompt, self.system_prompt)
    
    def document_code(self, code: str, language: str) -> str:
        """Add documentation to code"""
        
        prompt = f"""Add comprehensive documentation to this {language} code:

```{language}
{code}
```

Add:
1. Function/class docstrings
2. Parameter descriptions
3. Return value descriptions
4. Example usage
5. Inline comments for complex logic

Return the documented code."""
        
        return self._call_ai(prompt, self.system_prompt)
    
    def _analyze_project(self, project_path: Path) -> Dict:
        """Analyze project structure"""
        
        info = {
            "name": project_path.name,
            "files": [],
            "dependencies": []
        }
        
        # Check for common files
        for file in ['package.json', 'requirements.txt', 'go.mod', 'Cargo.toml']:
            if (project_path / file).exists():
                info['dependency_file'] = file
        
        # List main files
        for path in project_path.rglob("*"):
            if path.is_file() and not path.name.startswith('.'):
                info['files'].append(str(path.relative_to(project_path)))
        
        return info


class DebugAgent(DevAgent):
    """Debugging and troubleshooting agent"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "debugger")
        self.system_prompt = """You are a debugging expert specializing in:
- Error analysis and resolution
- Performance debugging
- Memory leaks
- Race conditions
- Stack trace analysis
- Logging and monitoring
- Profiling"""
    
    def analyze_error(self, error_message: str, code: str, language: str) -> Dict:
        """Analyze error and suggest fixes"""
        
        prompt = f"""Analyze this error in {language} code:

Error:
{error_message}

Code:
```{language}
{code}
```

Provide:
1. Root cause analysis
2. Step-by-step fix
3. Prevention strategies
4. Related issues to check

Respond in JSON:
{{
  "root_cause": "...",
  "fix_steps": [],
  "prevention": [],
  "related_checks": []
}}"""
        
        response = self._call_ai(prompt, self.system_prompt)
        return self._parse_json(response)
    
    def debug_performance(self, code: str, language: str, issue: str = "") -> Dict:
        """Debug performance issues"""
        
        prompt = f"""Analyze performance issues in this {language} code:

{f'Issue: {issue}' if issue else ''}

Code:
```{language}
{code}
```

Identify:
1. Performance bottlenecks
2. Time complexity issues
3. Memory usage problems
4. Optimization opportunities
5. Profiling suggestions

Respond in JSON."""
        
        response = self._call_ai(prompt, self.system_prompt)
        return self._parse_json(response)
    
    def _parse_json(self, response: str) -> Dict:
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"raw_response": response}


# Agent Manager

class DevAgentManager:
    """Manages and coordinates multiple development agents"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agents = {
            'architect': ArchitectAgent(api_key),
            'reviewer': CodeReviewAgent(api_key),
            'tester': TestingAgent(api_key),
            'devops': DeploymentAgent(api_key),
            'documenter': DocumentationAgent(api_key),
            'debugger': DebugAgent(api_key)
        }
    
    def get_agent(self, role: str) -> DevAgent:
        """Get agent by role"""
        return self.agents.get(role)
    
    def full_project_setup(self, requirements: str, project_path: Path) -> Dict:
        """Complete project setup with all agents"""
        
        results = {}
        
        # 1. Architecture design
        print("📐 Designing architecture...")
        results['architecture'] = self.agents['architect'].design_architecture(requirements)
        
        # 2. Generate documentation
        print("📝 Generating documentation...")
        results['readme'] = self.agents['documenter'].generate_readme(project_path)
        
        # 3. Setup deployment
        print("🚀 Setting up deployment...")
        project_info = {
            "name": project_path.name,
            "language": "python",  # Auto-detect in production
            "framework": "fastapi"
        }
        results['dockerfile'] = self.agents['devops'].generate_dockerfile(project_info)
        results['ci_pipeline'] = self.agents['devops'].generate_ci_pipeline('github-actions', project_info)
        
        return results
    
    def review_and_test_code(self, code: str, language: str, filepath: str = "") -> Dict:
        """Review code and generate tests"""
        
        results = {}
        
        # Code review
        print("🔍 Reviewing code...")
        results['review'] = self.agents['reviewer'].review_code(code, language, filepath)
        
        # Generate tests
        print("🧪 Generating tests...")
        results['tests'] = self.agents['tester'].generate_tests(code, language)
        
        return results


if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("PERPLEXITY_API_KEY")
    manager = DevAgentManager(api_key)
    
    # Example: Review code
    sample_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price']
    return total
"""
    
    results = manager.review_and_test_code(sample_code, "python", "calculator.py")
    print(json.dumps(results, indent=2))
