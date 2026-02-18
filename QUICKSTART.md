# Quick Start Guide

## Setup (5 minutes)

1. **Get your API key:**
   - Go to: https://www.perplexity.ai/settings
   - Click "API" tab
   - Generate new API key

2. **Install:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure:**
   ```bash
   # Copy template
   cp .env.template .env
   
   # Edit and add your API key
   nano .env
   ```

## Try It Now

### Interactive Chat
```bash
python perplexity_agent.py chat
```

### Quick Question
```bash
python perplexity_agent.py ask "What are the latest AI trends?"
```

### Run Examples
```bash
python examples.py
```

### Multi-Agent System
```bash
python multi_agent_system.py
```

## Common Commands

```bash
# Setup wizard
python perplexity_agent.py setup

# List models
python perplexity_agent.py models

# Web search
python perplexity_agent.py search "quantum computing news"

# Help
python perplexity_agent.py --help
```

## Files Included

- `perplexity_agent.py` - Main CLI tool
- `multi_agent_system.py` - Multi-agent orchestration
- `examples.py` - 10 practical examples
- `requirements.txt` - Dependencies
- `.env.template` - Configuration template
- `README.md` - Complete documentation

## Next Steps

1. Try the interactive chat mode
2. Run the examples to see what's possible
3. Check README.md for full documentation
4. Customize agents for your use case

Happy coding! 🚀
