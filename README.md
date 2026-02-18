# Perplexity AI Agent System

A powerful Python-based agent system for using your Perplexity AI Pro account via CLI and programmatically.

## Features

✨ **Interactive CLI Interface** - Chat with AI directly from your terminal
🔍 **Web Search Integration** - Access real-time web search capabilities
🤖 **Multi-Agent System** - Specialized agents for different tasks (Research, Coding, Analysis, Writing)
💾 **Memory & Context** - Agents remember conversation history
🔄 **Streaming Responses** - Real-time response streaming
📝 **Workflow Automation** - Chain multiple agents for complex tasks

## Prerequisites

- Python 3.9 or higher
- Perplexity AI Pro account
- Perplexity API key

## Getting Your API Key

1. Go to https://www.perplexity.ai/settings
2. Click on the **"</> API"** tab
3. Add a payment method (required for API access)
4. Generate a new API key
5. Copy the key (you'll need it for setup)

**Note:** Pro subscribers get $5/month in API credits. Additional usage is pay-as-you-go.

## Installation

### Option 1: Quick Setup

```bash
# Clone or download this repository
cd perplexity-agent

# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python perplexity_agent.py setup
```

### Option 2: Manual Setup

```bash
# Install dependencies
pip install perplexity-python python-dotenv requests rich click

# Create .env file
cp .env.template .env

# Edit .env and add your API key
nano .env
```

## Usage

### 1. Interactive Chat Mode

Start an interactive chat session:

```bash
python perplexity_agent.py chat
```

Options:
```bash
# Use a specific model
python perplexity_agent.py chat --model sonar-pro

# Commands during chat:
# - Type your message and press Enter
# - Type 'exit' or 'quit' to end session
# - Type 'clear' to clear conversation history
# - Type 'help' for more commands
```

### 2. Single Question Mode

Ask a single question without starting a chat session:

```bash
python perplexity_agent.py ask "What are the latest AI developments?"

# With specific model
python perplexity_agent.py ask "Explain quantum computing" --model sonar-pro
```

### 3. Web Search Mode

Search the web directly:

```bash
python perplexity_agent.py search "latest tech news 2026"

# Limit number of results
python perplexity_agent.py search "Python best practices" --max-results 10
```

### 4. List Available Models

```bash
python perplexity_agent.py models
```

### 5. Multi-Agent System

Use specialized agents for different tasks:

```bash
# Run the multi-agent demo
python multi_agent_system.py
```

Example in Python:

```python
from multi_agent_system import AgentOrchestrator
import os

# Initialize orchestrator
api_key = os.getenv("PERPLEXITY_API_KEY")
orchestrator = AgentOrchestrator(api_key)

# Auto-route to appropriate agent
result = orchestrator.execute("What are the latest AI trends?")
print(result['response'])

# Use specific agent
result = orchestrator.execute(
    "Write a Python function to sort a list",
    agent_name='coding'
)
print(result['response'])

# Multi-agent workflow
results = orchestrator.multi_agent_workflow(
    "Research quantum computing, analyze trends, write summary",
    workflow=['research', 'analyst', 'writer']
)

# Save workflow history
orchestrator.save_workflow('my_workflow.json')
```

## Available Agents

The multi-agent system includes:

- **ResearchAgent** - Specialized in research and fact-finding
- **CodingAgent** - Expert in coding and technical tasks
- **AnalystAgent** - Data analysis and insights
- **WriterAgent** - Content creation and writing

## Advanced Usage

### Using as a Python Library

```python
from perplexity_agent import PerplexityAgent

# Initialize agent
agent = PerplexityAgent(api_key="your_key", model="sonar")

# Chat with streaming
response = agent.chat("Tell me about AI", stream=True)

# Chat without streaming
response = agent.chat("What is Python?", stream=False)

# Web search
results = agent.search("latest news", max_results=5)

# Clear conversation history
agent.clear_history()

# Access conversation history
print(agent.conversation_history)
```

### Custom Integration

```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("PERPLEXITY_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "sonar",
    "messages": [
        {"role": "user", "content": "What is the weather today?"}
    ]
}

response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers=headers,
    json=payload
)

print(response.json()['choices'][0]['message']['content'])
```

## Available Models

- **sonar** - Fast and efficient model for general queries
- **sonar-pro** - Advanced model with enhanced capabilities
- **sonar-reasoning** - Specialized for complex reasoning tasks
- **sonar-small-online** - Small model with web search
- **sonar-medium-online** - Medium model with web search
- **sonar-large-online** - Large model with web search

## API Pricing

- Pro subscribers: $5/month in credits included
- Search API: $5 per 1,000 requests
- Chat API: Token-based pricing
  - Sonar models: $1 per million tokens (input and output)

## Project Structure

```
perplexity-agent/
├── perplexity_agent.py      # Main CLI interface
├── multi_agent_system.py    # Multi-agent orchestration system
├── requirements.txt         # Python dependencies
├── .env.template           # Environment variables template
├── .env                    # Your API key (create this)
└── README.md               # This file
```

## Troubleshooting

### Issue: "API key not found"
- Make sure you've created a `.env` file
- Verify your API key is correct
- Run `python perplexity_agent.py setup` to reconfigure

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "SDK not available" warning
```bash
# Install the official SDK
pip install perplexity-python
```

### Issue: API rate limits or quota exceeded
- Check your API credit balance at https://www.perplexity.ai/settings
- Add more credits or wait for monthly refresh ($5 for Pro users)

## Examples

### Example 1: Research Assistant

```bash
python perplexity_agent.py chat

You: Research the history of artificial intelligence
Assistant: [Provides detailed research with sources]

You: What are the key milestones?
Assistant: [Lists major AI milestones with context]
```

### Example 2: Code Helper

```python
from multi_agent_system import AgentOrchestrator

orchestrator = AgentOrchestrator(api_key)

# Get coding help
result = orchestrator.execute(
    "Write a Python web scraper with error handling",
    agent_name='coding'
)

print(result['response'])
```

### Example 3: Content Creation Workflow

```python
# Research → Analyze → Write workflow
results = orchestrator.multi_agent_workflow(
    "Create a blog post about sustainable energy",
    workflow=['research', 'analyst', 'writer']
)

for result in results:
    print(f"\n--- {result['agent']} ---")
    print(result['response'])
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this for any purpose

## Support

- Perplexity API Docs: https://docs.perplexity.ai
- Perplexity Help: https://www.perplexity.ai/help-center
- API Settings: https://www.perplexity.ai/settings

## Tips for Best Results

1. **Be specific** in your queries for better responses
2. **Use appropriate models** - online models for current info, chat models for general queries
3. **Leverage conversation history** - the agent remembers context
4. **Try multi-agent workflows** for complex tasks requiring different expertise
5. **Monitor your API usage** to avoid unexpected charges

---

**Happy researching! 🚀**
