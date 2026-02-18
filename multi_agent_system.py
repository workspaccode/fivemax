#!/usr/bin/env python3
"""
Advanced Perplexity Multi-Agent System
Specialized AI agents for different tasks
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class BaseAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, api_key: str, model: str = "sonar"):
        self.api_key = api_key
        self.model = model
        self.name = "BaseAgent"
        self.system_prompt = ""
        self.memory: List[Dict] = []
    
    def _make_request(self, messages: List[Dict], stream: bool = False) -> str:
        """Make API request to Perplexity"""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Add system prompt if exists
        full_messages = []
        if self.system_prompt:
            full_messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        full_messages.extend(messages)
        
        payload = {
            "model": self.model,
            "messages": full_messages,
            "stream": False
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    def process(self, task: str) -> str:
        """Process a task"""
        messages = [{"role": "user", "content": task}]
        
        # Add relevant memory
        if self.memory:
            context = self._get_relevant_memory(task)
            if context:
                messages.insert(0, {
                    "role": "system",
                    "content": f"Previous context: {context}"
                })
        
        response = self._make_request(messages)
        
        # Store in memory
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "response": response
        })
        
        return response
    
    def _get_relevant_memory(self, task: str, max_items: int = 3) -> str:
        """Get relevant items from memory"""
        if not self.memory:
            return ""
        
        # Simple approach: return last N items
        recent = self.memory[-max_items:]
        return "\n".join([
            f"Previous task: {m['task']}\nResponse: {m['response'][:200]}..."
            for m in recent
        ])
    
    def save_memory(self, filepath: str):
        """Save memory to file"""
        with open(filepath, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def load_memory(self, filepath: str):
        """Load memory from file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.memory = json.load(f)


class ResearchAgent(BaseAgent):
    """Agent specialized in research and fact-finding"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, model="sonar")
        self.name = "ResearchAgent"
        self.system_prompt = """You are a research specialist AI agent. Your role is to:
- Conduct thorough research on topics
- Provide accurate, well-sourced information
- Cite sources and verify facts
- Present information in a clear, organized manner
- Identify knowledge gaps and suggest further research areas"""


class CodingAgent(BaseAgent):
    """Agent specialized in coding and technical tasks"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, model="sonar")
        self.name = "CodingAgent"
        self.system_prompt = """You are a coding specialist AI agent. Your role is to:
- Write clean, efficient, well-documented code
- Debug and optimize existing code
- Explain technical concepts clearly
- Suggest best practices and design patterns
- Provide code examples and implementations"""


class AnalystAgent(BaseAgent):
    """Agent specialized in data analysis and insights"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, model="sonar")
        self.name = "AnalystAgent"
        self.system_prompt = """You are a data analyst AI agent. Your role is to:
- Analyze data and identify patterns
- Generate insights and recommendations
- Create clear summaries of complex information
- Identify trends and correlations
- Provide actionable conclusions"""


class WriterAgent(BaseAgent):
    """Agent specialized in content creation and writing"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, model="sonar")
        self.name = "WriterAgent"
        self.system_prompt = """You are a content writer AI agent. Your role is to:
- Create engaging, well-structured content
- Adapt tone and style to the audience
- Ensure clarity and readability
- Generate creative ideas
- Edit and refine text"""


class AgentOrchestrator:
    """Orchestrates multiple agents for complex tasks"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.agents = {
            'research': ResearchAgent(api_key),
            'coding': CodingAgent(api_key),
            'analyst': AnalystAgent(api_key),
            'writer': WriterAgent(api_key)
        }
        self.workflow_history: List[Dict] = []
    
    def route_task(self, task: str) -> str:
        """Automatically route task to appropriate agent"""
        
        # Simple keyword-based routing
        task_lower = task.lower()
        
        if any(word in task_lower for word in ['code', 'program', 'script', 'debug', 'function']):
            return 'coding'
        elif any(word in task_lower for word in ['analyze', 'data', 'trend', 'pattern', 'insight']):
            return 'analyst'
        elif any(word in task_lower for word in ['write', 'article', 'blog', 'content', 'story']):
            return 'writer'
        else:
            return 'research'
    
    def execute(self, task: str, agent_name: Optional[str] = None) -> Dict:
        """Execute task with specified or auto-selected agent"""
        
        if agent_name is None:
            agent_name = self.route_task(task)
        
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        agent = self.agents[agent_name]
        
        print(f"\n[{agent.name}] Processing task...")
        response = agent.process(task)
        
        result = {
            'agent': agent_name,
            'task': task,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        
        self.workflow_history.append(result)
        
        return result
    
    def multi_agent_workflow(self, task: str, workflow: List[str]) -> List[Dict]:
        """Execute task through multiple agents in sequence"""
        
        results = []
        current_task = task
        
        for agent_name in workflow:
            result = self.execute(current_task, agent_name)
            results.append(result)
            
            # Use previous response as context for next agent
            current_task = f"Based on this previous work:\n{result['response']}\n\nNow: {task}"
        
        return results
    
    def save_workflow(self, filepath: str):
        """Save workflow history"""
        with open(filepath, 'w') as f:
            json.dump(self.workflow_history, f, indent=2)


def main():
    """Example usage of the multi-agent system"""
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        print("Error: PERPLEXITY_API_KEY not found in environment")
        return
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(api_key)
    
    print("=== Perplexity Multi-Agent System ===\n")
    
    # Example 1: Auto-routing
    print("Example 1: Auto-routing a research task")
    result = orchestrator.execute("What are the latest developments in quantum computing?")
    print(f"\nAgent used: {result['agent']}")
    print(f"Response:\n{result['response'][:300]}...\n")
    
    # Example 2: Specific agent
    print("\nExample 2: Using coding agent specifically")
    result = orchestrator.execute(
        "Write a Python function to calculate Fibonacci numbers",
        agent_name='coding'
    )
    print(f"\nResponse:\n{result['response'][:300]}...\n")
    
    # Example 3: Multi-agent workflow
    print("\nExample 3: Multi-agent workflow")
    print("Task: Research AI trends, analyze them, then write a summary")
    
    workflow_results = orchestrator.multi_agent_workflow(
        "Research the top 3 AI trends in 2026",
        workflow=['research', 'analyst', 'writer']
    )
    
    for i, result in enumerate(workflow_results, 1):
        print(f"\nStep {i} - {result['agent']}:")
        print(result['response'][:200] + "...")
    
    # Save workflow
    orchestrator.save_workflow('workflow_history.json')
    print("\n\nWorkflow saved to workflow_history.json")


if __name__ == "__main__":
    main()
