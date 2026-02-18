# 🚀 Dev Controller Quick Start

Get up and running in 5 minutes!

## Step 1: Install (1 minute)

```bash
pip install -r requirements.txt
```

## Step 2: Setup API Key (1 minute)

```bash
python dev_controller.py setup
```

Or manually create `.env`:
```bash
PERPLEXITY_API_KEY=pplx-your-key-here
```

Get your API key: https://www.perplexity.ai/settings → API tab

## Step 3: Start Interactive Mode (30 seconds)

```bash
python dev_controller.py interactive
```

## Step 4: Create Your First Project (2 minutes)

```bash
dev> create my-first-app
```

Describe what you want to build when prompted!

## Common Commands Cheat Sheet

### In Interactive Mode

```bash
create <name>           # Create new project
load <name>             # Load existing project  
gen <what>              # Generate code
fix <file>              # Fix bugs
plan <feature>          # Plan implementation
ask <question>          # Ask anything
exit                    # Quit
```

### Direct Commands

```bash
# Create project
python dev_controller.py create my-api --template "fastapi REST API"

# Generate code
python dev_controller.py generate "create user authentication"

# Fix bugs
python dev_controller.py fix app.py --error "NameError"

# Plan feature
python dev_controller.py plan "add payment system"

# Run tests
python dev_controller.py test

# List projects
python dev_controller.py projects
```

## Example: Build a REST API in 2 Minutes

```bash
# 1. Create project
python dev_controller.py create todo-api --template "fastapi REST API"

# 2. Load it
python dev_controller.py load todo-api

# 3. Generate endpoints
python dev_controller.py generate "create CRUD endpoints for Todo items"

# 4. Generate tests
python dev_controller.py generate "write pytest tests for all endpoints"

# 5. Done! Your API is ready
cd workspace/todo-api
uvicorn app.main:app --reload
```

## Next Steps

- Read [DEV_CONTROLLER_README.md](DEV_CONTROLLER_README.md) for full documentation
- Try the advanced agents: `python dev_agents.py`
- Explore tool integrations: `python dev_tools.py`
- Check out examples in the README

## Tips for Best Results

✅ **Be specific** in descriptions
- ❌ "add API"
- ✅ "create FastAPI endpoint GET /users returning list of users from database"

✅ **Plan before building**
```bash
python dev_controller.py plan "add real-time notifications"
# Review the plan, then implement step by step
```

✅ **Use the right model**
- `sonar` - General coding (default, cheaper)
- `sonar-pro` - Complex architecture/planning

✅ **Review before committing**
```bash
python dev_controller.py generate "review all code for security issues"
```

## Troubleshooting

**"API key not found"**
```bash
python dev_controller.py setup
```

**"Project not found"**
```bash
python dev_controller.py projects  # See all projects
```

**Want to start over?**
```bash
rm -rf workspace/my-project
python dev_controller.py create my-project
```

---

🎉 **You're ready to build!**

Start with: `python dev_controller.py interactive`
