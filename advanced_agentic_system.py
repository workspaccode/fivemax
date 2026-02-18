#!/usr/bin/env python3
"""
Advanced Agentic AI Framework
Deep thinking, multi-agent collaboration, and advanced reasoning capabilities
"""

import os
import sys
import json
import asyncio
from typing import List, Dict, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import time
import uuid
from datetime import datetime

from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

console = Console()


class ThoughtType(Enum):
    ANALYSIS = "analysis"
    PLANNING = "planning"
    REASONING = "reasoning"
    REFLECTION = "reflection"
    HYPOTHESIS = "hypothesis"
    VERIFICATION = "verification"
    EXECUTION = "execution"
    MONITORING = "monitoring"


class AgentRole(Enum):
    COORDINATOR = "coordinator"
    ANALYST = "analyst"
    PLANNER = "planner"
    EXECUTOR = "executor"
    CRITIC = "critic"
    RESEARCHER = "researcher"
    SYNTHESIZER = "synthesizer"


@dataclass
class Thought:
    """Represents a single thought in the reasoning chain"""
    id: str
    type: ThoughtType
    content: str
    confidence: float
    evidence: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    parent: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Agent:
    """Represents an AI agent with specific capabilities"""
    id: str
    name: str
    role: AgentRole
    capabilities: List[str]
    model: str = "sonar"
    status: str = "idle"
    current_task: Optional[str] = None
    performance_history: List[Dict] = field(default_factory=list)


@dataclass
class Task:
    """Represents a task to be executed by agents"""
    id: str
    description: str
    priority: int
    complexity: int
    required_agents: List[AgentRole]
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"
    assigned_to: List[str] = field(default_factory=list)
    result: Optional[Dict] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Memory:
    """Represents a memory entry for the agent"""
    id: str
    content: str
    type: str
    importance: float
    tags: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    associations: List[str] = field(default_factory=list)


class SequentialThinkingEngine:
    """Core engine for sequential thinking and reasoning"""
    
    def __init__(self, client: OpenAI):
        self.client = client
        self.thoughts: Dict[str, Thought] = {}
        self.current_chain: List[str] = []
        self.max_chain_length = 50
        
    async def think(self, problem: str, context: Dict = None) -> List[Thought]:
        """Perform deep sequential thinking on a problem"""
        context = context or {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Initializing thinking process...", total=None)
            
            # Initial problem analysis
            initial_thought = await self._analyze_problem(problem, context)
            self.thoughts[initial_thought.id] = initial_thought
            self.current_chain.append(initial_thought.id)
            
            progress.update(task, description="Decomposing problem...")
            
            # Problem decomposition
            sub_thoughts = await self._decompose_problem(initial_thought, context)
            for thought in sub_thoughts:
                self.thoughts[thought.id] = thought
                thought.parent = initial_thought.id
                initial_thought.children.append(thought.id)
                self.current_chain.append(thought.id)
            
            progress.update(task, description="Generating hypotheses...")
            
            # Generate hypotheses for each sub-problem
            for sub_thought in sub_thoughts:
                hypotheses = await self._generate_hypotheses(sub_thought, context)
                for hypothesis in hypotheses:
                    self.thoughts[hypothesis.id] = hypothesis
                    hypothesis.parent = sub_thought.id
                    sub_thought.children.append(hypothesis.id)
                    self.current_chain.append(hypothesis.id)
            
            progress.update(task, description="Reasoning and verification...")
            
            # Reasoning and verification
            for thought_id in self.current_chain:
                thought = self.thoughts[thought_id]
                if thought.type in [ThoughtType.HYPOTHESIS, ThoughtType.ANALYSIS]:
                    verified = await self._verify_thought(thought, context)
                    if verified:
                        self.thoughts[verified.id] = verified
                        verified.parent = thought.id
                        thought.children.append(verified.id)
            
            progress.update(task, description="Synthesizing solution...")
            
            # Final synthesis
            synthesis = await self._synthesize_solution(self.current_chain, context)
            self.thoughts[synthesis.id] = synthesis
            
            progress.update(task, description="Thinking complete!", completed=True)
        
        return [self.thoughts[tid] for tid in self.current_chain + [synthesis.id]]
    
    async def _analyze_problem(self, problem: str, context: Dict) -> Thought:
        """Initial problem analysis"""
        response = await self._call_llm(
            f"""Analyze this problem deeply: {problem}
            
            Context: {json.dumps(context, indent=2)}
            
            Provide:
            1. Problem classification
            2. Key components and constraints
            3. Success criteria
            4. Potential challenges
            5. Required knowledge domains
            
            Be thorough and structured in your analysis.""",
            temperature=0.3
        )
        
        return Thought(
            id=str(uuid.uuid4()),
            type=ThoughtType.ANALYSIS,
            content=response,
            confidence=0.8,
            metadata={"stage": "initial_analysis"}
        )
    
    async def _decompose_problem(self, problem_thought: Thought, context: Dict) -> List[Thought]:
        """Decompose problem into sub-problems"""
        response = await self._call_llm(
            f"""Based on this analysis: {problem_thought.content}
            
            Decompose the problem into 3-5 manageable sub-problems.
            For each sub-problem:
            1. Clear description
            2. Dependencies on other sub-problems
            3. Estimated complexity (1-10)
            4. Required approach/method
            
            Format as a structured list.""",
            temperature=0.2
        )
        
        sub_problems = []
        lines = response.split('\n')
        current_problem = ""
        
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                if current_problem:
                    sub_problems.append(current_problem.strip())
                current_problem = line
            else:
                current_problem += "\n" + line
        
        if current_problem:
            sub_problems.append(current_problem.strip())
        
        return [
            Thought(
                id=str(uuid.uuid4()),
                type=ThoughtType.PLANNING,
                content=problem,
                confidence=0.7,
                metadata={"sub_problem_index": i, "complexity": 5}
            )
            for i, problem in enumerate(sub_problems)
        ]
    
    async def _generate_hypotheses(self, problem_thought: Thought, context: Dict) -> List[Thought]:
        """Generate hypotheses for solving the sub-problem"""
        response = await self._call_llm(
            f"""For this sub-problem: {problem_thought.content}
            
            Generate 2-3 plausible solution hypotheses.
            For each hypothesis:
            1. Clear approach description
            2. Expected outcome
            3. Potential risks
            4. Resource requirements
            5. Confidence level (1-10)
            
            Be creative but realistic.""",
            temperature=0.4
        )
        
        hypotheses = []
        sections = response.split('\n\n')
        
        for section in sections:
            if section.strip():
                hypotheses.append(
                    Thought(
                        id=str(uuid.uuid4()),
                        type=ThoughtType.HYPOTHESIS,
                        content=section.strip(),
                        confidence=0.6,
                        metadata={"parent_problem": problem_thought.id}
                    )
                )
        
        return hypotheses
    
    async def _verify_thought(self, thought: Thought, context: Dict) -> Optional[Thought]:
        """Verify a hypothesis or analysis"""
        response = await self._call_llm(
            f"""Verify this hypothesis/analysis: {thought.content}
            
            Evaluate:
            1. Logical consistency
            2. Evidence support
            3. Feasibility
            4. Potential flaws
            5. Confidence adjustment (1-10)
            
            Provide a verification report with confidence score.""",
            temperature=0.1
        )
        
        return Thought(
            id=str(uuid.uuid4()),
            type=ThoughtType.VERIFICATION,
            content=response,
            confidence=0.7,
            metadata={"verified_thought": thought.id}
        )
    
    async def _synthesize_solution(self, thought_chain: List[str], context: Dict) -> Thought:
        """Synthesize final solution from thought chain"""
        chain_content = "\n\n".join([
            self.thoughts[tid].content for tid in thought_chain
        ])
        
        response = await self._call_llm(
            f"""Based on this reasoning chain: {chain_content}
            
            Synthesize a comprehensive solution:
            1. Executive summary
            2. Step-by-step implementation plan
            3. Resource requirements
            4. Risk mitigation strategies
            5. Success metrics
            6. Alternative approaches
            
            Be specific and actionable.""",
            temperature=0.2
        )
        
        return Thought(
            id=str(uuid.uuid4()),
            type=ThoughtType.SYNTHESIS,
            content=response,
            confidence=0.9,
            metadata={"final_solution": True}
        )
    
    async def _call_llm(self, prompt: str, temperature: float = 0.3) -> str:
        """Call the language model"""
        try:
            response = self.client.chat.completions.create(
                model="sonar",
                messages=[
                    {"role": "system", "content": "You are an advanced reasoning AI that thinks deeply and systematically."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]LLM call failed: {e}[/red]")
            return f"Error: {str(e)}"


class MultiAgentOrchestrator:
    """Orchestrates multiple specialized agents"""
    
    def __init__(self, client: OpenAI):
        self.client = client
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
        self.completed_tasks: List[str] = []
        
    def create_agent(self, name: str, role: AgentRole, capabilities: List[str]) -> Agent:
        """Create a new agent"""
        agent = Agent(
            id=str(uuid.uuid4()),
            name=name,
            role=role,
            capabilities=capabilities
        )
        self.agents[agent.id] = agent
        return agent
    
    def create_task(self, description: str, priority: int, complexity: int, 
                   required_agents: List[AgentRole]) -> Task:
        """Create a new task"""
        task = Task(
            id=str(uuid.uuid4()),
            description=description,
            priority=priority,
            complexity=complexity,
            required_agents=required_agents
        )
        self.tasks[task.id] = task
        self.task_queue.append(task.id)
        return task
    
    async def execute_task(self, task_id: str) -> Dict:
        """Execute a task using appropriate agents"""
        task = self.tasks[task_id]
        task.status = "executing"
        
        # Find suitable agents
        suitable_agents = [
            agent for agent in self.agents.values()
            if agent.role in task.required_agents and agent.status == "idle"
        ]
        
        if not suitable_agents:
            return {"error": "No suitable agents available"}
        
        # Assign task to agents
        assigned_agents = suitable_agents[:len(task.required_agents)]
        for agent in assigned_agents:
            agent.status = "busy"
            agent.current_task = task_id
            task.assigned_to.append(agent.id)
        
        try:
            # Execute task with assigned agents
            result = await self._collaborative_execution(task, assigned_agents)
            task.result = result
            task.status = "completed"
            self.completed_tasks.append(task_id)
            
            # Update agent performance
            for agent in assigned_agents:
                agent.status = "idle"
                agent.current_task = None
                agent.performance_history.append({
                    "task_id": task_id,
                    "success": True,
                    "timestamp": datetime.now()
                })
            
            return result
            
        except Exception as e:
            task.status = "failed"
            for agent in assigned_agents:
                agent.status = "idle"
                agent.current_task = None
                agent.performance_history.append({
                    "task_id": task_id,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now()
                })
            return {"error": str(e)}
    
    async def _collaborative_execution(self, task: Task, agents: List[Agent]) -> Dict:
        """Execute task collaboratively with multiple agents"""
        results = {}
        
        # Phase 1: Individual analysis
        for agent in agents:
            console.print(f"[cyan]{agent.name}[/cyan] analyzing task...")
            
            analysis = await self._agent_analyze(task, agent)
            results[f"{agent.role}_analysis"] = analysis
        
        # Phase 2: Collaborative planning
        console.print("[yellow]Agents collaborating on plan...[/yellow]")
        plan = await self._collaborative_planning(task, agents, results)
        results["collaborative_plan"] = plan
        
        # Phase 3: Execution
        console.print("[green]Executing plan...[/green]")
        execution_result = await self._execute_plan(task, agents, plan)
        results["execution"] = execution_result
        
        # Phase 4: Review and synthesis
        console.print("[blue]Reviewing and synthesizing results...[/blue]")
        synthesis = await self._synthesize_results(task, agents, results)
        results["synthesis"] = synthesis
        
        return results
    
    async def _agent_analyze(self, task: Task, agent: Agent) -> str:
        """Agent performs individual analysis"""
        role_prompt = {
            AgentRole.ANALYST: "Analyze the problem requirements, constraints, and success criteria.",
            AgentRole.PLANNER: "Break down the task into actionable steps and estimate timelines.",
            AgentRole.EXECUTOR: "Identify technical requirements and implementation approaches.",
            AgentRole.CRITIC: "Identify potential risks, edge cases, and failure modes.",
            AgentRole.RESEARCHER: "Research best practices, similar solutions, and relevant technologies.",
            AgentRole.SYNTHESIZER: "Consider how different components will integrate and communicate."
        }
        
        prompt = f"""As a {agent.role}, analyze this task: {task.description}
        
        Your role: {role_prompt.get(agent.role, "Provide your expert analysis.")}
        
        Capabilities: {', '.join(agent.capabilities)}
        
        Provide detailed analysis from your perspective."""
        
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": f"You are an AI agent specialized as a {agent.role}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def _collaborative_planning(self, task: Task, agents: List[Agent], 
                                   analyses: Dict) -> str:
        """Agents collaborate on planning"""
        analyses_text = "\n\n".join([f"{role}: {content}" for role, content in analyses.items()])
        
        prompt = f"""Task: {task.description}
        
        Individual Analyses:
        {analyses_text}
        
        As a team, create a comprehensive execution plan that:
        1. Integrates insights from all agents
        2. Assigns responsibilities based on agent capabilities
        3. Defines clear milestones and deliverables
        4. Includes coordination mechanisms
        5. Addresses identified risks and constraints
        
        Provide a structured collaborative plan."""
        
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": "You are coordinating a team of AI agents to create an optimal plan."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    async def _execute_plan(self, task: Task, agents: List[Agent], plan: str) -> str:
        """Execute the collaborative plan"""
        # Simulate execution with different agent contributions
        execution_steps = []
        
        for agent in agents:
            if agent.role == AgentRole.EXECUTOR:
                step = await self._execute_implementation(task, agent, plan)
            elif agent.role == AgentRole.RESEARCHER:
                step = await self._execute_research(task, agent, plan)
            elif agent.role == AgentRole.ANALYST:
                step = await self._execute_validation(task, agent, plan)
            else:
                step = await self._execute_coordination(task, agent, plan)
            
            execution_steps.append(f"{agent.name}: {step}")
        
        return "\n\n".join(execution_steps)
    
    async def _execute_implementation(self, task: Task, agent: Agent, plan: str) -> str:
        """Execute implementation tasks"""
        prompt = f"""As an executor, implement the core components for: {task.description}
        
        Plan: {plan}
        
        Provide:
        1. Implementation approach
        2. Key components built
        3. Technical decisions made
        4. Code/architecture details
        5. Integration points"""
        
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": "You are a technical implementation specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1200
        )
        
        return response.choices[0].message.content
    
    async def _execute_research(self, task: Task, agent: Agent, plan: str) -> str:
        """Execute research tasks"""
        prompt = f"""As a researcher, investigate best practices for: {task.description}
        
        Plan: {plan}
        
        Provide:
        1. Research findings
        2. Best practices identified
        3. Technology recommendations
        4. Industry standards
        5. Case studies or examples"""
        
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": "You are a research specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def _execute_validation(self, task: Task, agent: Agent, plan: str) -> str:
        """Execute validation tasks"""
        prompt = f"""As an analyst, validate the approach for: {task.description}
        
        Plan: {plan}
        
        Provide:
        1. Requirements validation
        2. Risk assessment
        3. Quality criteria
        4. Testing strategy
        5. Success metrics"""
        
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": "You are a quality assurance analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def _execute_coordination(self, task: Task, agent: Agent, plan: str) -> str:
        """Execute coordination tasks"""
        prompt = f"""As a coordinator/synthesizer, ensure alignment for: {task.description}
        
        Plan: {plan}
        
        Provide:
        1. Coordination strategy
        2. Communication protocols
        3. Integration approach
        4. Conflict resolution
        5. Progress tracking"""
        
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": "You are a project coordination specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def _synthesize_results(self, task: Task, agents: List[Agent], 
                                results: Dict) -> str:
        """Synthesize all results into final output"""
        results_text = json.dumps(results, indent=2)
        
        prompt = f"""Task: {task.description}
        
        Execution Results:
        {results_text}
        
        Synthesize a comprehensive final result that:
        1. Integrates all agent contributions
        2. Addresses the original task requirements
        3. Provides clear deliverables
        4. Documents decisions made
        5. Outlines next steps
        
        Provide a polished final output."""
        
        response = self.client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": "You are synthesizing team results into a final deliverable."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1500
        )
        
        return response.choices[0].message.content


class MemoryManager:
    """Manages agent memory and learning"""
    
    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.associations: Dict[str, List[str]] = {}
        
    def store_memory(self, content: str, memory_type: str, importance: float, 
                    tags: List[str]) -> str:
        """Store a new memory"""
        memory = Memory(
            id=str(uuid.uuid4()),
            content=content,
            type=memory_type,
            importance=importance,
            tags=tags
        )
        self.memories[memory.id] = memory
        
        # Create associations based on tags
        for tag in tags:
            if tag not in self.associations:
                self.associations[tag] = []
            self.associations[tag].append(memory.id)
        
        return memory.id
    
    def retrieve_memories(self, query: str, tags: List[str] = None, 
                         limit: int = 10) -> List[Memory]:
        """Retrieve relevant memories"""
        relevant_memories = []
        
        for memory in self.memories.values():
            # Simple relevance check
            if tags:
                if any(tag in memory.tags for tag in tags):
                    relevant_memories.append(memory)
            else:
                # Keyword matching
                query_words = query.lower().split()
                content_words = memory.content.lower().split()
                if any(word in content_words for word in query_words):
                    relevant_memories.append(memory)
        
        # Sort by importance and recency
        relevant_memories.sort(
            key=lambda m: (m.importance, m.timestamp),
            reverse=True
        )
        
        return relevant_memories[:limit]
    
    def update_memory(self, memory_id: str, new_content: str, 
                     importance_adjustment: float = 0):
        """Update an existing memory"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.content = new_content
            memory.importance += importance_adjustment
            memory.timestamp = datetime.now()


class AdvancedAgenticSystem:
    """Main agentic system combining all capabilities"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        self.thinking_engine = SequentialThinkingEngine(self.client)
        self.orchestrator = MultiAgentOrchestrator(self.client)
        self.memory_manager = MemoryManager()
        
        # Initialize default agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize default set of specialized agents"""
        self.orchestrator.create_agent(
            "Analyst", AgentRole.ANALYST, 
            ["requirements_analysis", "data_analysis", "validation"]
        )
        self.orchestrator.create_agent(
            "Planner", AgentRole.PLANNER,
            ["project_planning", "task_decomposition", "scheduling"]
        )
        self.orchestrator.create_agent(
            "Executor", AgentRole.EXECUTOR,
            ["implementation", "coding", "testing"]
        )
        self.orchestrator.create_agent(
            "Critic", AgentRole.CRITIC,
            ["risk_assessment", "quality_assurance", "review"]
        )
        self.orchestrator.create_agent(
            "Researcher", AgentRole.RESEARCHER,
            ["research", "analysis", "best_practices"]
        )
        self.orchestrator.create_agent(
            "Synthesizer", AgentRole.SYNTHESIZER,
            ["integration", "coordination", "synthesis"]
        )
    
    async def solve_complex_problem(self, problem: str, context: Dict = None) -> Dict:
        """Solve a complex problem using the full agentic system"""
        console.print(Panel.fit(
            "[bold cyan]Advanced Agentic System[/bold cyan]\n"
            "Initializing deep thinking and multi-agent collaboration...",
            border_style="cyan"
        ))
        
        context = context or {}
        
        # Phase 1: Deep sequential thinking
        console.print("\n[bold]Phase 1:[/bold] Deep Sequential Thinking")
        thoughts = await self.thinking_engine.think(problem, context)
        
        # Store thinking process in memory
        for thought in thoughts:
            self.memory_manager.store_memory(
                thought.content,
                f"thought_{thought.type.value}",
                thought.confidence,
                [thought.type.value, "reasoning"]
            )
        
        # Phase 2: Create and execute tasks
        console.print("\n[bold]Phase 2:[/bold] Multi-Agent Collaboration")
        
        # Create tasks based on thinking
        task_id = self.orchestrator.create_task(
            problem,
            priority=1,
            complexity=len(thoughts),
            required_agents=[
                AgentRole.ANALYST,
                AgentRole.PLANNER,
                AgentRole.EXECUTOR,
                AgentRole.CRITIC
            ]
        )
        
        # Execute task
        result = await self.orchestrator.execute_task(task_id)
        
        # Phase 3: Store results and learn
        console.print("\n[bold]Phase 3:[/bold] Learning and Memory Integration")
        
        # Store results in memory
        self.memory_manager.store_memory(
            json.dumps(result, indent=2),
            "task_result",
            0.9,
            ["execution", "collaboration", problem[:50]]
        )
        
        return {
            "problem": problem,
            "thoughts": [{"id": t.id, "type": t.type.value, "content": t.content[:200] + "..."} 
                        for t in thoughts],
            "task_result": result,
            "performance": self._get_performance_metrics()
        }
    
    def _get_performance_metrics(self) -> Dict:
        """Get system performance metrics"""
        total_agents = len(self.orchestrator.agents)
        busy_agents = sum(1 for a in self.orchestrator.agents.values() if a.status == "busy")
        completed_tasks = len(self.orchestrator.completed_tasks)
        total_memories = len(self.memory_manager.memories)
        
        return {
            "total_agents": total_agents,
            "busy_agents": busy_agents,
            "completed_tasks": completed_tasks,
            "total_memories": total_memories,
            "system_health": "optimal" if busy_agents < total_agents else "under_load"
        }
    
    def display_thinking_tree(self, thoughts: List[Thought]):
        """Display the thinking process as a tree"""
        tree = Tree("[bold cyan]Thinking Process[/bold cyan]")
        
        for thought in thoughts:
            if thought.type == ThoughtType.ANALYSIS:
                branch = tree.add(f"[green]🧠 Analysis[/green]")
                branch.add(f"[dim]{thought.content[:100]}...[/dim]")
            elif thought.type == ThoughtType.PLANNING:
                branch = tree.add(f"[blue]📋 Planning[/blue]")
                branch.add(f"[dim]{thought.content[:100]}...[/dim]")
            elif thought.type == ThoughtType.HYPOTHESIS:
                branch = tree.add(f"[yellow]💡 Hypothesis[/yellow]")
                branch.add(f"[dim]{thought.content[:100]}...[/dim]")
            elif thought.type == ThoughtType.VERIFICATION:
                branch = tree.add(f"[magenta]✅ Verification[/magenta]")
                branch.add(f"[dim]{thought.content[:100]}...[/dim]")
            elif thought.type == ThoughtType.SYNTHESIS:
                branch = tree.add(f"[red]🎯 Solution[/red]")
                branch.add(f"[dim]{thought.content[:100]}...[/dim]")
        
        console.print(tree)


if __name__ == "__main__":
    # Example usage
    import asyncio
    
    async def main():
        # Initialize system
        system = AdvancedAgenticSystem("your-api-key-here")
        
        # Solve a complex problem
        problem = "Design and implement a scalable microservices architecture for an e-commerce platform"
        
        result = await system.solve_complex_problem(problem)
        
        # Display results
        console.print("\n[bold green]Problem Solved![/bold green]")
        console.print(Markdown(result["task_result"]["synthesis"]))
    
    asyncio.run(main())
