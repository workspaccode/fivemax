# Advanced Agentic AI Framework

A sophisticated deep thinking and multi-agent collaboration system inspired by Claude AI's capabilities. This framework provides sequential thinking, multi-agent orchestration, tool execution, and advanced reasoning capabilities.

## Features

### 🧠 Deep Sequential Thinking
- **Problem Analysis**: Deep decomposition and understanding of complex problems
- **Hypothesis Generation**: Multiple solution approaches with confidence scoring
- **Verification**: Logical consistency and evidence validation
- **Synthesis**: Comprehensive solution generation from reasoning chains

### 👥 Multi-Agent Collaboration
- **Specialized Agents**: Analyst, Planner, Executor, Critic, Researcher, Synthesizer
- **Collaborative Planning**: Agents work together to create optimal solutions
- **Role-Based Execution**: Each agent contributes based on their expertise
- **Performance Tracking**: Monitor agent effectiveness and learning

### 🛠️ Tool Execution Framework
- **File System**: Read, write, list, and manage files and directories
- **Web Access**: Search the web and fetch URLs
- **Code Execution**: Execute Python code and shell commands
- **Git Integration**: Version control operations
- **Extensible**: Easy to add new tools

### 💾 Memory Management
- **Persistent Memory**: Store and retrieve important information
- **Associative Learning**: Connect related concepts and experiences
- **Context Awareness**: Maintain conversation and problem-solving context

## Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up API Key**:
```bash
# Copy the template
cp .env.template .env

# Edit .env with your Perplexity API key
# Get your key from: https://www.perplexity.ai/settings
PERPLEXITY_API_KEY=your_api_key_here
```

## Quick Start

### Command Line Interface

1. **Interactive Mode**:
```bash
python agentic_cli.py interactive
```

2. **Solve a Single Problem**:
```bash
python agentic_cli.py solve "Design a scalable microservices architecture for e-commerce"
```

3. **With Context File**:
```bash
python agentic_cli.py solve "Optimize this database schema" --context database_context.json
```

### Python API

```python
import asyncio
from advanced_agentic_system import AdvancedAgenticSystem

async def main():
    # Initialize the system
    system = AdvancedAgenticSystem("your-api-key-here")
    
    # Solve a complex problem
    problem = "Create a REST API for user management with authentication"
    result = await system.solve_complex_problem(problem)
    
    # Access the solution
    print(result["task_result"]["synthesis"])

asyncio.run(main())
```

## Core Components

### 1. Sequential Thinking Engine

The thinking engine performs deep, structured reasoning:

```python
from advanced_agentic_system import SequentialThinkingEngine
from openai import OpenAI

engine = SequentialThinkingEngine(OpenAI(api_key="your-key"))
thoughts = await engine.think("How to optimize database queries?")
```

**Thinking Process**:
1. **Analysis**: Break down the problem into components
2. **Planning**: Create structured approach
3. **Hypothesis**: Generate potential solutions
4. **Verification**: Test and validate approaches
5. **Synthesis**: Create comprehensive solution

### 2. Multi-Agent Orchestrator

Coordinate multiple specialized agents:

```python
from advanced_agentic_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator(client)

# Create custom agents
orchestrator.create_agent(
    "Security Expert", 
    AgentRole.CRITIC,
    ["security_analysis", "penetration_testing", "compliance"]
)

# Execute complex tasks
task = orchestrator.create_task(
    "Secure the web application",
    priority=1,
    complexity=8,
    required_agents=[AgentRole.EXECUTOR, AgentRole.CRITIC]
)
result = await orchestrator.execute_task(task.id)
```

### 3. Tool Executor

Execute real-world operations:

```python
from tool_executor import ToolExecutor

executor = ToolExecutor()

# Read a file
result = executor.execute_tool(
    "read_file",
    {"file_path": "config.json"},
    user_permissions=["file_read"]
)

# Web search
result = executor.execute_tool(
    "web_search",
    {"query": "Python async best practices", "max_results": 5},
    user_permissions=["web_access"]
)
```

## Available Tools

| Tool ID | Name | Description | Permissions |
|---------|------|-------------|-------------|
| `read_file` | Read File | Read contents of a file | `file_read` |
| `write_file` | Write File | Write content to a file | `file_write` |
| `list_directory` | List Directory | List directory contents | `file_read` |
| `web_search` | Web Search | Search the web | `web_access` |
| `fetch_url` | Fetch URL | Fetch content from URL | `web_access` |
| `execute_python` | Execute Python | Run Python code | `code_execution` |
| `execute_shell` | Execute Shell | Run shell commands | `shell_access` |
| `git_status` | Git Status | Get repository status | `git_access` |
| `git_commit` | Git Commit | Commit changes | `git_write` |

## CLI Commands

### Interactive Mode
```bash
python agentic_cli.py interactive
```
- Type problems directly
- Use `help` for commands
- Use `tools` to see available tools
- Use `history` to see past interactions

### Tool Execution
```bash
# Execute a tool directly
python agentic_cli.py tool read_file file_path=config.json

# Web search
python agentic_cli.py tool web_search query="machine learning tutorials"

# Execute Python code
python agentic_cli.py tool execute_python code="print('Hello World')"
```

### Session Management
```bash
# Save session
python agentic_cli.py save my_session.json

# Load session
python agentic_cli.py load my_session.json

# View history
python agentic_cli.py history --limit 20
```

### System Status
```bash
# Check system status
python agentic_cli.py status

# View available tools
python agentic_cli.py tools
```

## Examples

### Example 1: Software Architecture Design

```bash
python agentic_cli.py solve "Design a microservices architecture for a food delivery platform"
```

**Expected Output**:
- Deep analysis of requirements
- Multiple architectural approaches
- Risk assessment and mitigation
- Detailed implementation plan
- Technology recommendations

### Example 2: Code Debugging

```bash
python agentic_cli.py solve "Debug this Flask app error: 500 Internal Server Error"
```

**Expected Output**:
- Systematic error analysis
- Potential root causes
- Debugging steps
- Code fixes
- Prevention strategies

### Example 3: Data Analysis Pipeline

```bash
python agentic_cli.py solve "Create a data pipeline for processing user analytics"
```

**Expected Output**:
- Data flow architecture
- Technology stack recommendations
- Implementation steps
- Quality assurance measures
- Monitoring and alerting

## Configuration

### Environment Variables

```bash
# Required
PERPLEXITY_API_KEY=your_api_key_here

# Optional
DEFAULT_MODEL=sonar
MAX_THINKING_STEPS=50
TOOL_TIMEOUT=30
MEMORY_LIMIT=1000
```

### Custom Configuration

Create a `config.json` file:

```json
{
  "thinking": {
    "max_chain_length": 50,
    "confidence_threshold": 0.7,
    "verification_enabled": true
  },
  "agents": {
    "default_model": "sonar",
    "max_concurrent_tasks": 5,
    "performance_tracking": true
  },
  "tools": {
    "default_timeout": 30,
    "safe_mode": true,
    "allowed_domains": ["api.github.com", "stackoverflow.com"]
  },
  "memory": {
    "max_memories": 1000,
    "importance_threshold": 0.5,
    "auto_cleanup": true
  }
}
```

## Advanced Usage

### Custom Agent Creation

```python
from advanced_agentic_system import Agent, AgentRole

# Create specialized agent
security_agent = Agent(
    id="security_expert",
    name="Security Expert",
    role=AgentRole.CRITIC,
    capabilities=[
        "security_analysis",
        "penetration_testing",
        "compliance_checking",
        "vulnerability_assessment"
    ]
)

system.orchestrator.agents[security_agent.id] = security_agent
```

### Custom Tool Development

```python
from tool_executor import Tool, ToolType

# Create custom tool
database_tool = Tool(
    id="query_database",
    name="Query Database",
    type=ToolType.DATABASE,
    description="Execute SQL queries",
    parameters={
        "query": {"type": "string", "required": True},
        "database": {"type": "string", "required": True}
    },
    required_permissions=["database_access"]
)

executor.register_tool(database_tool)
```

### Memory Management

```python
# Store important information
memory_id = system.memory_manager.store_memory(
    content="User prefers microservices over monolithic architecture",
    memory_type="preference",
    importance=0.8,
    tags=["architecture", "preference", "user"]
)

# Retrieve relevant memories
memories = system.memory_manager.retrieve_memories(
    query="architecture preferences",
    tags=["preference"],
    limit=5
)
```

## Performance Optimization

### Thinking Optimization
- Adjust `max_chain_length` for complex problems
- Set appropriate `confidence_threshold`
- Enable/disable verification based on requirements

### Agent Optimization
- Monitor agent performance metrics
- Adjust agent specializations
- Balance workload across agents

### Tool Optimization
- Set appropriate timeouts
- Use caching for repeated operations
- Monitor tool execution history

## Troubleshooting

### Common Issues

1. **API Key Not Found**:
   - Ensure `.env` file exists with `PERPLEXITY_API_KEY`
   - Check file permissions
   - Verify API key validity

2. **Tool Execution Failures**:
   - Check required permissions
   - Verify tool parameters
   - Review error messages

3. **Memory Issues**:
   - Monitor memory usage
   - Adjust `max_memories` limit
   - Enable auto-cleanup

4. **Performance Issues**:
   - Reduce concurrent tasks
   - Optimize thinking chain length
   - Monitor system resources

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section
- Review the examples
- Open an issue on GitHub

---

**Built with ❤️ using advanced AI principles and multi-agent collaboration**
