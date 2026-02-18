# Perplexity Dev Controller 🚀

**AI-Powered Full-Stack Development Assistant**

A complete development environment powered by Perplexity AI - similar to Gemini CLI or Warp AI. Build complete applications, fix bugs, plan features, manage projects, and deploy with AI assistance.

## 🎯 Features

### 🏗️ Project Management
- **Create Projects** - AI generates complete project structures from descriptions
- **Smart Templates** - Python, Node.js, FastAPI, React, and custom templates
- **Auto-scaffolding** - Intelligent directory structure and starter files

### 💻 Code Generation
- **Generate Code** - Describe what you need, AI writes production-ready code
- **Fix Bugs** - AI analyzes errors and provides fixes
- **Refactor Code** - Automated code improvements and optimization
- **Code Review** - AI reviews code for quality, security, and performance

### 🧪 Testing & Quality
- **Auto-generate Tests** - Unit, integration, and E2E tests
- **Code Coverage** - Analysis and suggestions
- **Linting & Formatting** - Automated code style enforcement

### 📋 Planning & Architecture
- **Feature Planning** - Detailed implementation plans
- **Architecture Design** - System design and component breakdown
- **Task Breakdown** - Step-by-step development tasks

### 🚀 Deployment & DevOps
- **Dockerfile Generation** - Optimized container configurations
- **CI/CD Pipelines** - GitHub Actions, GitLab CI, etc.
- **Kubernetes Manifests** - Complete K8s deployment configs
- **Docker Compose** - Multi-service orchestration

### 📚 Documentation
- **Auto-generate READMEs** - Comprehensive project documentation
- **API Docs** - Automated API documentation
- **Code Comments** - Intelligent inline documentation

### 🔧 Tool Integrations
- **Git** - Version control operations
- **Docker** - Container management
- **Package Managers** - npm, pip, cargo, go modules
- **Code Formatters** - Black, Prettier, ESLint

## 🚀 Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python dev_controller.py setup
```

### 2. Create Your First Project

```bash
# Interactive mode (recommended)
python dev_controller.py interactive

# Or create directly
python dev_controller.py create my-app --template "fastapi REST API"
```

### 3. Start Building

```bash
# Load your project
python dev_controller.py load my-app

# Generate code
python dev_controller.py generate "create user authentication endpoint" --file app/auth.py

# Fix bugs
python dev_controller.py fix app/main.py --error "NameError: name 'user' is not defined"

# Plan features
python dev_controller.py plan "add payment integration with Stripe"
```

## 📖 Complete Usage Guide

### Interactive Mode (Best for Development)

```bash
python dev_controller.py interactive
```

Interactive commands:
- `create <name>` - Create new project
- `load <name>` - Load existing project
- `gen <description>` - Generate code
- `fix <file>` - Fix code errors
- `plan <feature>` - Plan feature implementation
- `ask <question>` - Ask anything
- `exit` - Quit

### Project Creation

```bash
# Predefined templates
python dev_controller.py create my-api --template "fastapi microservice"
python dev_controller.py create my-web --template "react frontend"
python dev_controller.py create my-cli --template "python CLI tool"

# Custom projects
python dev_controller.py create my-project
# AI will ask for details and generate custom structure
```

### Code Generation

```bash
# Generate specific files
python dev_controller.py generate "create database models for users and posts" --file models.py

# Generate features
python dev_controller.py generate "implement JWT authentication"

# Generate tests
python dev_controller.py generate "write tests for the auth module" --file tests/test_auth.py
```

### Bug Fixing

```bash
# Fix with error message
python dev_controller.py fix app/main.py --error "TypeError: object of type 'NoneType' has no len()"

# General code review and fix
python dev_controller.py fix app/main.py
```

### Feature Planning

```bash
# Get detailed implementation plan
python dev_controller.py plan "add real-time chat functionality"

# Plan outputs:
# - Architecture overview
# - Files to create/modify
# - Step-by-step tasks
# - Dependencies needed
# - Testing strategy
# - Potential challenges
```

### Testing

```bash
# Run all tests
python dev_controller.py test

# Run specific test file
python dev_controller.py test --file tests/test_auth.py
```

### Project Management

```bash
# List all projects
python dev_controller.py projects

# Load existing project
python dev_controller.py load my-project
```

## 🤖 Advanced Development Agents

The system includes specialized AI agents for different tasks:

### Using Individual Agents

```python
from dev_agents import DevAgentManager

api_key = "your_perplexity_api_key"
manager = DevAgentManager(api_key)

# Architecture design
architect = manager.get_agent('architect')
design = architect.design_architecture("e-commerce platform with microservices")

# Code review
reviewer = manager.get_agent('reviewer')
review = reviewer.review_code(code, "python", "main.py")

# Generate tests
tester = manager.get_agent('tester')
tests = tester.generate_tests(code, "python")

# Deployment setup
devops = manager.get_agent('devops')
dockerfile = devops.generate_dockerfile(project_info)
ci_pipeline = devops.generate_ci_pipeline('github-actions', project_info)

# Documentation
documenter = manager.get_agent('documenter')
readme = documenter.generate_readme(project_path)
api_docs = documenter.generate_api_docs(code, "python")

# Debugging
debugger = manager.get_agent('debugger')
analysis = debugger.analyze_error(error_message, code, "python")
```

### Available Agents

| Agent | Purpose | Capabilities |
|-------|---------|--------------|
| **Architect** | System design | Architecture patterns, database design, API design, scalability |
| **Code Reviewer** | Quality assurance | Code quality, security, performance, best practices |
| **Tester** | Testing | Unit tests, integration tests, coverage analysis |
| **DevOps** | Deployment | Docker, K8s, CI/CD, infrastructure as code |
| **Documenter** | Documentation | READMEs, API docs, code comments |
| **Debugger** | Troubleshooting | Error analysis, performance debugging, profiling |

## 🛠️ Development Tools Integration

### Git Integration

```python
from dev_tools import GitIntegration

git = GitIntegration(project_path)

# Initialize repository
git.init(initial_branch="main")

# Commit changes
git.commit("Initial commit", add_all=True)

# Create branch
git.create_branch("feature/user-auth")

# Check status
status = git.status()

# View diff
diff = git.diff("app/main.py")

# Push to remote
git.push("origin", "main")
```

### Docker Integration

```python
from dev_tools import DockerIntegration

docker = DockerIntegration(project_path)

# Build image
docker.build("my-app:latest")

# Run container
docker.run("my-app:latest", ports={8000: 8000})

# Docker Compose
docker.compose_up("docker-compose.yml")
docker.compose_down()
```

### Package Management

```python
from dev_tools import PackageManagerIntegration

pkg_manager = PackageManagerIntegration(project_path)

# Install dependencies
pkg_manager.install()

# Install specific package
pkg_manager.install("fastapi")

# Run scripts
pkg_manager.run_script("dev")

# Run tests
pkg_manager.test()
```

### Code Formatting

```python
from dev_tools import CodeFormatter

formatter = CodeFormatter(project_path)

# Format Python
formatter.format_python()

# Lint Python
formatter.lint_python("app/main.py")

# Format JavaScript
formatter.format_javascript()

# Lint JavaScript
formatter.lint_javascript()
```

## 📦 Project Templates

### Built-in Templates

1. **Python CLI Tool**
   - Click/argparse based CLI
   - Tests with pytest
   - Package structure

2. **FastAPI Microservice**
   - REST API structure
   - Database models
   - Authentication
   - Docker ready

3. **React Frontend**
   - Modern React with hooks
   - TypeScript support
   - Testing setup
   - Build configuration

4. **Node.js Backend**
   - Express.js API
   - JWT authentication
   - MongoDB integration
   - Testing with Jest

5. **Machine Learning Project**
   - Jupyter notebooks
   - Data processing pipeline
   - Model training structure
   - MLflow integration

### Custom Templates

Describe your project and AI will create a custom template:

```bash
python dev_controller.py create my-project

# AI asks:
# "Describe your project"

# You respond:
# "GraphQL API for social media platform with PostgreSQL, Redis caching, 
#  and real-time subscriptions"

# AI generates complete custom structure
```

## 🎯 Example Workflows

### Workflow 1: Create Full-Stack App

```bash
# 1. Create backend
python dev_controller.py create backend --template "fastapi microservice"
python dev_controller.py load backend

# 2. Generate authentication
python dev_controller.py generate "implement JWT authentication with refresh tokens"

# 3. Generate database models
python dev_controller.py generate "create SQLAlchemy models for User, Post, Comment"

# 4. Generate tests
python dev_controller.py generate "write comprehensive tests for auth endpoints"

# 5. Plan frontend integration
python dev_controller.py plan "integrate with React frontend"

# 6. Generate deployment
python dev_controller.py generate "create Dockerfile and docker-compose for development"
```

### Workflow 2: Debug and Fix

```bash
# 1. Load project
python dev_controller.py load my-app

# 2. Run tests and capture error
python dev_controller.py test
# Error: "KeyError: 'user_id' in auth.py line 45"

# 3. Fix the error
python dev_controller.py fix auth.py --error "KeyError: 'user_id' in auth.py line 45"

# 4. Review fixed code
python dev_controller.py generate "review auth.py for similar issues"

# 5. Re-run tests
python dev_controller.py test
```

### Workflow 3: Feature Development

```bash
# 1. Plan feature
python dev_controller.py plan "add payment processing with Stripe"
# Saves detailed plan to project

# 2. Implement step by step
python dev_controller.py generate "create Stripe payment service class"
python dev_controller.py generate "add payment endpoint to API"
python dev_controller.py generate "create payment webhook handler"

# 3. Generate tests
python dev_controller.py generate "write tests for payment integration"

# 4. Update documentation
python dev_controller.py generate "update README with payment setup instructions"
```

## ⚙️ Configuration

### Environment Variables

Create `.env` file:

```bash
# Required
PERPLEXITY_API_KEY=your_api_key_here

# Optional
DEFAULT_MODEL=sonar  # or sonar-pro, sonar-reasoning
WORKSPACE_DIR=./workspace  # Default project directory
```

### Project Metadata

Each project includes `.perplexity.json`:

```json
{
  "name": "my-project",
  "template": "custom",
  "tech_stack": ["python", "fastapi", "postgresql"],
  "dependencies": {
    "pip": ["fastapi", "uvicorn", "sqlalchemy"]
  },
  "created": "2026-02-15T10:30:00"
}
```

## 🔐 Best Practices

1. **Version Control** - Always initialize git for your projects
2. **Test Early** - Generate tests alongside code
3. **Plan First** - Use the plan command for complex features
4. **Review Code** - Use AI code review before committing
5. **Document** - Auto-generate docs as you build
6. **Backup** - Keep backups of original code (`.backup` files created automatically)

## 🚨 Troubleshooting

### Common Issues

**Issue: API rate limits**
```bash
# Solution: Use caching, batch operations, or upgrade plan
```

**Issue: Project not found**
```bash
# Solution: Make sure you're in the right directory
python dev_controller.py projects  # List all projects
```

**Issue: Code generation incomplete**
```bash
# Solution: Be more specific in descriptions
# Instead of: "add API"
# Use: "create FastAPI router with GET /users endpoint returning JSON"
```

## 💰 Cost Optimization

- Use **sonar** model for general tasks (cheaper)
- Use **sonar-pro** for complex architecture/planning
- Batch similar operations
- Cache frequently used responses
- Monitor API usage in Perplexity dashboard

## 🔄 Updates

Check for updates and new features:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📚 Additional Resources

- **Perplexity API Docs**: https://docs.perplexity.ai
- **API Dashboard**: https://www.perplexity.ai/settings
- **Support**: Create an issue in the repository

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional project templates
- More language support
- Enhanced tool integrations
- Custom agent implementations

## 📄 License

MIT License - use freely for any purpose

---

**Built with ❤️ using Perplexity AI**

*Transform your development workflow with AI assistance*
