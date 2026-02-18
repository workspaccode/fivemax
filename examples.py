#!/usr/bin/env python3
"""
Perplexity Agent Examples
Practical examples of using the agent system
"""

import os
from dotenv import load_dotenv
from multi_agent_system import AgentOrchestrator, ResearchAgent, CodingAgent
from perplexity_agent import PerplexityAgent

load_dotenv()


def example_1_simple_chat():
    """Example 1: Simple chat interaction"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Chat Interaction")
    print("="*60)
    
    agent = PerplexityAgent()
    
    # Single turn conversation
    print("\nQuery: What is machine learning?")
    response = agent.chat("What is machine learning?", stream=False)
    print(f"\nResponse: {response[:300]}...")
    
    # Follow-up question (uses conversation history)
    print("\n\nFollow-up: Give me a practical example")
    response = agent.chat("Give me a practical example", stream=False)
    print(f"\nResponse: {response[:300]}...")


def example_2_research_task():
    """Example 2: Using specialized research agent"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Research Task with Specialized Agent")
    print("="*60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    research_agent = ResearchAgent(api_key)
    
    task = "What are the latest breakthroughs in renewable energy in 2026?"
    print(f"\nResearch Task: {task}")
    
    result = research_agent.process(task)
    print(f"\nResearch Results:\n{result[:400]}...")


def example_3_coding_assistant():
    """Example 3: Using coding agent for technical tasks"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Coding Assistant")
    print("="*60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    coding_agent = CodingAgent(api_key)
    
    tasks = [
        "Write a Python function to validate email addresses using regex",
        "Add error handling to the previous function",
        "Write unit tests for this function"
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n\nTask {i}: {task}")
        result = coding_agent.process(task)
        print(f"\nCode:\n{result[:300]}...")


def example_4_multi_agent_workflow():
    """Example 4: Multi-agent workflow for complex task"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Multi-Agent Workflow")
    print("="*60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    orchestrator = AgentOrchestrator(api_key)
    
    # Complex task requiring multiple agents
    task = "Create content about the impact of AI on healthcare"
    
    print(f"\nTask: {task}")
    print("\nWorkflow: Research → Analysis → Writing")
    
    results = orchestrator.multi_agent_workflow(
        task,
        workflow=['research', 'analyst', 'writer']
    )
    
    for i, result in enumerate(results, 1):
        print(f"\n\n--- Step {i}: {result['agent'].upper()} ---")
        print(result['response'][:250] + "...")


def example_5_auto_routing():
    """Example 5: Automatic task routing"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Automatic Task Routing")
    print("="*60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    orchestrator = AgentOrchestrator(api_key)
    
    tasks = [
        "Write a Python function to calculate prime numbers",
        "What are the current trends in artificial intelligence?",
        "Analyze the data: [1, 5, 3, 8, 2, 9, 4]",
        "Write a blog post introduction about space exploration"
    ]
    
    for task in tasks:
        result = orchestrator.execute(task)
        print(f"\nTask: {task}")
        print(f"Routed to: {result['agent'].upper()}")
        print(f"Response: {result['response'][:150]}...")


def example_6_web_search():
    """Example 6: Web search functionality"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Web Search")
    print("="*60)
    
    agent = PerplexityAgent()
    
    query = "latest developments in quantum computing 2026"
    print(f"\nSearch Query: {query}")
    
    results = agent.search(query, max_results=3)
    
    if 'results' in results:
        print("\n\nSearch Results:")
        for i, result in enumerate(results['results'], 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
    else:
        print(f"\n\nAnswer: {results.get('answer', '')[:300]}...")


def example_7_agent_memory():
    """Example 7: Using agent memory for context"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Agent Memory and Context")
    print("="*60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    research_agent = ResearchAgent(api_key)
    
    # First task
    print("\nTask 1: Initial research")
    result1 = research_agent.process("What is blockchain technology?")
    print(f"Response: {result1[:200]}...")
    
    # Second task - agent remembers previous context
    print("\n\nTask 2: Follow-up question (using memory)")
    result2 = research_agent.process("What are its main use cases?")
    print(f"Response: {result2[:200]}...")
    
    # Save memory to file
    research_agent.save_memory('agent_memory.json')
    print("\n\nMemory saved to agent_memory.json")
    
    # Load memory in new instance
    new_agent = ResearchAgent(api_key)
    new_agent.load_memory('agent_memory.json')
    print(f"Memory loaded: {len(new_agent.memory)} items")


def example_8_different_models():
    """Example 8: Using different models"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Different Models Comparison")
    print("="*60)
    
    models = ['sonar', 'sonar-small-online']
    query = "Explain neural networks briefly"
    
    for model in models:
        print(f"\n\n--- Using {model} ---")
        agent = PerplexityAgent(model=model)
        response = agent.chat(query, stream=False)
        print(f"Response: {response[:250]}...")


def example_9_batch_processing():
    """Example 9: Batch processing multiple queries"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Batch Processing")
    print("="*60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    orchestrator = AgentOrchestrator(api_key)
    
    queries = [
        "What is Python's GIL?",
        "How does async/await work?",
        "What is a context manager?",
        "Explain decorators"
    ]
    
    print("\nProcessing multiple Python concept queries...")
    
    for i, query in enumerate(queries, 1):
        result = orchestrator.execute(query, agent_name='coding')
        print(f"\n{i}. {query}")
        print(f"   Answer: {result['response'][:150]}...")
    
    # Save all results
    orchestrator.save_workflow('batch_results.json')
    print("\n\nResults saved to batch_results.json")


def example_10_custom_workflow():
    """Example 10: Custom workflow with specific agents"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Custom Workflow")
    print("="*60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    orchestrator = AgentOrchestrator(api_key)
    
    # Create a complete technical document
    task = "Python best practices for error handling"
    
    print(f"\nCreating technical document: {task}")
    print("\nWorkflow: Research → Code Examples → Analysis → Documentation")
    
    # Custom workflow
    workflow_steps = [
        ('research', 'Research Python error handling best practices'),
        ('coding', 'Provide code examples of proper error handling'),
        ('analyst', 'Analyze common mistakes and anti-patterns'),
        ('writer', 'Create a comprehensive guide document')
    ]
    
    results = []
    for agent_name, step_task in workflow_steps:
        print(f"\n\n--- {agent_name.upper()}: {step_task} ---")
        result = orchestrator.execute(step_task, agent_name=agent_name)
        results.append(result)
        print(f"{result['response'][:200]}...")
    
    # Combine all results
    print("\n\n--- FINAL DOCUMENT ---")
    final_doc = "\n\n".join([
        f"## {r['agent'].upper()}\n{r['response']}"
        for r in results
    ])
    
    # Save final document
    with open('technical_guide.md', 'w') as f:
        f.write(f"# {task}\n\n{final_doc}")
    
    print("Complete guide saved to technical_guide.md")


def main():
    """Run all examples"""
    
    # Check if API key is set
    if not os.getenv("PERPLEXITY_API_KEY"):
        print("Error: PERPLEXITY_API_KEY not found!")
        print("Please set up your .env file first.")
        return
    
    print("\n" + "="*60)
    print("PERPLEXITY AI AGENT SYSTEM - EXAMPLES")
    print("="*60)
    
    examples = [
        ("Simple Chat", example_1_simple_chat),
        ("Research Task", example_2_research_task),
        ("Coding Assistant", example_3_coding_assistant),
        ("Multi-Agent Workflow", example_4_multi_agent_workflow),
        ("Auto Routing", example_5_auto_routing),
        ("Web Search", example_6_web_search),
        ("Agent Memory", example_7_agent_memory),
        ("Different Models", example_8_different_models),
        ("Batch Processing", example_9_batch_processing),
        ("Custom Workflow", example_10_custom_workflow),
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\n0. Run all examples")
    print("q. Quit")
    
    choice = input("\nSelect an example (0-10): ").strip()
    
    if choice == 'q':
        return
    elif choice == '0':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\nError in {name}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        try:
            examples[int(choice)-1][1]()
        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
