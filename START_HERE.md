# 🚀 Complete Perplexity AI Development System

**Two Complete Systems Included!**

## 📦 What You Have

### System 1: Basic Agent System ✨
Perfect for learning and simple tasks

### System 2: Dev Controller 🏗️
**Full development environment** (like Gemini CLI / Warp)

---

## 🎯 Quick Decision Guide

### Want to Chat & Research?
→ **Use Basic Agent System**
```bash
python perplexity_agent.py chat
```

### Want to Build Complete Applications?
→ **Use Dev Controller**
```bash
python dev_controller.py interactive
```

---

## 📁 File Structure

### Basic Agent System Files

| File | Purpose |
|------|---------|
| `perplexity_agent.py` | Main CLI - chat, ask, search |
| `multi_agent_system.py` | Specialized agents (Research, Coding, Analysis, Writing) |
| `examples.py` | 10 practical examples |
| `README.md` | Complete basic system documentation |
| `QUICKSTART.md` | 5-minute quick start guide |

**Use for:**
- Interactive conversations
- Web search with AI
- Simple code help
- Research tasks
- Content writing

**Start with:**
```bash
pip install -r requirements.txt
python perplexity_agent.py setup
python perplexity_agent.py chat
```

---

### Dev Controller System Files

| File | Purpose |
|------|---------|
| `dev_controller.py` | **Main development controller** |
| `dev_agents.py` | **6 specialized dev agents** |
| `dev_tools.py` | Git, Docker, package manager integration |
| `DEV_CONTROLLER_README.md` | **Complete dev system docs** |
| `DEV_QUICKSTART.md` | **5-minute start guide** |
| `COMPARISON.md` | vs Gemini CLI / Warp |

**Use for:**
- Creating complete projects
- Generating production code
- Planning features
- Fixing bugs
- Code review
- Testing
- Documentation
- Deployment (Docker, K8s, CI/CD)

**Start with:**
```bash
pip install -r requirements.txt
python dev_controller.py setup
python dev_controller.py interactive
```

---

## 🚀 Quick Start Paths

### Path 1: Just Want to Chat with AI
```bash
# 1. Setup
pip install -r requirements.txt
python perplexity_agent.py setup

# 2. Start chatting
python perplexity_agent.py chat
```

### Path 2: Build Complete Applications
```bash
# 1. Setup  
pip install -r requirements.txt
python dev_controller.py setup

# 2. Create your first app
python dev_controller.py interactive
> create my-first-app
> gen "create user authentication"
```

### Path 3: Explore Everything
```bash
# 1. Setup
pip install -r requirements.txt
python perplexity_agent.py setup

# 2. Try basic examples
python examples.py

# 3. Try dev controller
python dev_controller.py interactive
```

---

## 📚 Documentation Guide

### Read First
1. **DEV_QUICKSTART.md** or **QUICKSTART.md** (choose based on your need)
2. Start using the system
3. Refer to full README when needed

### Complete Documentation
- **README.md** - Basic agent system
- **DEV_CONTROLLER_README.md** - Development controller
- **COMPARISON.md** - How it compares to other tools

---

## 🎯 What Each System Does Best

### Basic Agent System
```bash
✅ Chat conversations
✅ Web search + AI answers
✅ Research tasks
✅ Content writing
✅ Simple coding help
✅ Learning about topics
```

**Example:**
```bash
python perplexity_agent.py chat

You: Research quantum computing developments
AI: [Searches web and provides comprehensive answer]

You: Write a blog post about it
AI: [Creates engaging content]
```

### Dev Controller System
```bash
✅ Create complete projects
✅ Generate production code
✅ Plan features & architecture
✅ Fix bugs automatically
✅ Generate tests
✅ Code review
✅ Documentation generation
✅ Docker/K8s deployment
✅ CI/CD pipeline setup
```

**Example:**
```bash
python dev_controller.py interactive

> create todo-api --template "fastapi REST API"
→ Complete project created with structure, code, tests, docs

> gen "add user authentication with JWT"
→ Auth system generated with security best practices

> plan "add real-time notifications"  
→ Detailed implementation plan with architecture, tasks, challenges

> fix auth.py --error "NameError: user"
→ Bug analyzed and fixed automatically
```

---

## 🔧 System Requirements

```bash
# Python 3.9+
python --version

# Install dependencies
pip install -r requirements.txt

# Get API key
# Visit: https://www.perplexity.ai/settings → API tab
```

---

## 💡 Usage Examples

### Example 1: Research Assistant
```bash
# Use: Basic Agent System
python perplexity_agent.py chat

You: What are the latest AI developments?
You: Compare GPT-4 vs Claude
You: Write a summary of AI trends
```

### Example 2: Build a Web App
```bash
# Use: Dev Controller
python dev_controller.py interactive

> create my-blog --template "react + fastapi"
> gen "create blog post CRUD API"
> gen "add user authentication"
> gen "write tests for all endpoints"
> gen "create Dockerfile for production"
```

### Example 3: Debug Existing Code
```bash
# Use: Dev Controller
python dev_controller.py load my-project
python dev_controller.py fix app.py --error "TypeError: ..."
```

### Example 4: Multi-Agent Research
```bash
# Use: Basic Agent System
python examples.py
# Select: Multi-Agent Workflow
# Agents collaborate: Research → Analyze → Write
```

---

## 🎓 Learning Path

### Beginner
1. Start with basic agent chat
2. Try examples.py
3. Read QUICKSTART.md

### Intermediate  
4. Try dev_controller interactive mode
5. Create a simple project
6. Generate some code

### Advanced
7. Use specialized dev agents
8. Create custom workflows
9. Integrate with git/docker
10. Build production apps

---

## 🔥 Power User Tips

### Tip 1: Combine Both Systems
```bash
# Use basic agent for research
python perplexity_agent.py ask "best practices for FastAPI auth"

# Then use dev controller to implement
python dev_controller.py generate "implement FastAPI JWT auth with those best practices"
```

### Tip 2: Use Right Model for Task
```bash
# Cheap model for simple tasks
DEFAULT_MODEL=sonar python perplexity_agent.py chat

# Expensive model for complex architecture
python dev_controller.py plan --model sonar-pro "microservices architecture"
```

### Tip 3: Batch Operations
```bash
# Instead of 3 separate commands
python dev_controller.py generate "create user model + API endpoints + tests all at once"
```

---

## 🆘 Getting Help

### Quick Reference
```bash
# Basic Agent
python perplexity_agent.py --help
python perplexity_agent.py chat --help

# Dev Controller
python dev_controller.py --help
python dev_controller.py create --help
```

### Common Issues

**"API key not found"**
```bash
python perplexity_agent.py setup  # or dev_controller.py setup
```

**"Which system should I use?"**
- Chatting/Research → Basic Agent
- Building Apps → Dev Controller
- Not sure? → Try both!

**"Can I use both?"**
Yes! They're complementary. Use basic agent for research, dev controller for building.

---

## 📊 Feature Matrix

| Feature | Basic Agent | Dev Controller |
|---------|-------------|----------------|
| Chat | ✅ | ✅ |
| Web Search | ✅ | ✅ |
| Code Snippets | ✅ | ✅ |
| **Complete Projects** | ❌ | ✅ |
| **Architecture Design** | ❌ | ✅ |
| **Auto Testing** | ❌ | ✅ |
| **Docker/K8s** | ❌ | ✅ |
| **CI/CD** | ❌ | ✅ |
| **Git Integration** | ❌ | ✅ |
| **Code Review** | ⚠️ Basic | ✅ Advanced |
| **Bug Fixing** | ⚠️ Suggestions | ✅ Automatic |

---

## 🎯 Next Steps

1. **Read the appropriate quickstart:**
   - Chat/Research: `QUICKSTART.md`
   - Development: `DEV_QUICKSTART.md`

2. **Set up your API key:**
   ```bash
   python perplexity_agent.py setup
   ```

3. **Start building:**
   ```bash
   python dev_controller.py interactive
   ```

---

## 🚀 Ready to Start?

### For Research & Chat:
```bash
python perplexity_agent.py chat
```

### For Development:
```bash
python dev_controller.py interactive
```

### To Explore:
```bash
python examples.py
```

---

**You now have a complete AI-powered development environment!** 🎉

Choose your path and start building amazing things! 🚀
