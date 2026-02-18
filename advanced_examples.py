#!/usr/bin/env python3
"""
Advanced Examples and demonstrations of the Advanced Agentic AI Framework
"""

import asyncio
import json
from pathlib import Path

from advanced_agentic_system import AdvancedAgenticSystem, AgentRole
from tool_executor import ToolExecutor


async def example_1_software_architecture():
    """Example 1: Design software architecture"""
    print("=" * 60)
    print("EXAMPLE 1: Software Architecture Design")
    print("=" * 60)
    
    # Initialize system
    system = AdvancedAgenticSystem("your-api-key-here")
    
    # Complex architecture problem
    problem = """
    Design a scalable microservices architecture for a global e-commerce platform
    that needs to handle:
    - 1M+ concurrent users
    - Real-time inventory management
    - Personalized recommendations
    - Multi-region deployment
    - Payment processing
    - Order tracking
    """
    
    # Solve the problem
    result = await system.solve_complex_problem(problem)
    
    # Display key results
    print("\n🎯 SOLUTION SYNTHESIS:")
    print("-" * 40)
    print(result["task_result"]["synthesis"][:500] + "...")
    
    print("\n📊 PERFORMANCE METRICS:")
    print("-" * 40)
    for key, value in result["performance"].items():
        print(f"{key}: {value}")


async def example_2_code_debugging():
    """Example 2: Debug code issues"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Code Debugging")
    print("=" * 60)
    
    system = AdvancedAgenticSystem("your-api-key-here")
    
    # Debugging problem
    problem = """
    I'm getting a 500 Internal Server Error in my Flask application.
    The error occurs when users try to upload large files.
    Here's the error log:
    - MemoryError: Unable to allocate memory
    - Request timeout after 30 seconds
    - Only happens with files > 50MB
    
    The application uses:
    - Flask with uWSGI
    - PostgreSQL database
    - Redis for caching
    - Nginx as reverse proxy
    """
    
    result = await system.solve_complex_problem(problem)
    
    print("\n🔍 DEBUGGING ANALYSIS:")
    print("-" * 40)
    print(result["task_result"]["synthesis"][:500] + "...")


async def example_4_tool_execution():
    """Example 4: Tool execution demonstration"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Tool Execution")
    print("=" * 60)
    
    executor = ToolExecutor()
    
    # Example tool executions
    print("\n📁 FILE SYSTEM OPERATIONS:")
    print("-" * 40)
    
    # Create a test file
    result = executor.execute_tool(
        "write_file",
        {"file_path": "test_advanced_example.txt", "content": "Hello from Advanced Agentic AI!"},
        user_permissions=["file_write"]
    )
    print(f"Write file: {result.success}")
    
    # Read the file
    result = executor.execute_tool(
        "read_file",
        {"file_path": "test_advanced_example.txt"},
        user_permissions=["file_read"]
    )
    print(f"Read file: {result.success}")
    if result.success:
        print(f"Content: {result.result['content']}")
    
    # List directory
    result = executor.execute_tool(
        "list_directory",
        {"dir_path": ".", "recursive": False},
        user_permissions=["file_read"]
    )
    print(f"List directory: {result.success}")
    if result.success:
        files = [item["name"] for item in result.result["items"] if item["type"] == "file"]
        print(f"Files found: {len(files)}")
    
    print("\n💻 CODE EXECUTION:")
    print("-" * 40)
    
    # Execute Python code
    code = """
import json
data = {"message": "Hello from advanced executed code!", "timestamp": "2024-01-01"}
print(json.dumps(data, indent=2))
"""
    
    result = executor.execute_tool(
        "execute_python",
        {"code": code, "timeout": 10},
        user_permissions=["code_execution"]
    )
    print(f"Python execution: {result.success}")
    if result.success:
        print(f"Output: {result.result['output']}")


async def example_5_custom_agent():
    """Example 5: Custom agent creation"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Custom Agent Creation")
    print("=" * 60)
    
    system = AdvancedAgenticSystem("your-api-key-here")
    
    # Create custom security agent
    security_agent = system.orchestrator.create_agent(
        "Security Expert",
        AgentRole.CRITIC,
        ["security_analysis", "penetration_testing", "compliance", "vulnerability_assessment"]
    )
    
    # Create custom DevOps agent
    devops_agent = system.orchestrator.create_agent(
        "DevOps Specialist",
        AgentRole.EXECUTOR,
        ["docker", "kubernetes", "ci_cd", "monitoring", "infrastructure"]
    )
    
    print(f"Created custom agents: {security_agent.name}, {devops_agent.name}")
    print(f"Total agents in system: {len(system.orchestrator.agents)}")
    
    # Show agent details
    print("\n🤖 AVAILABLE AGENTS:")
    print("-" * 40)
    for agent in system.orchestrator.agents.values():
        print(f"• {agent.name} ({agent.role.value})")
        print(f"  Capabilities: {', '.join(agent.capabilities[:3])}...")


async def example_6_memory_management():
    """Example 6: Memory management demonstration"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Memory Management")
    print("=" * 60)
    
    system = AdvancedAgenticSystem("your-api-key-here")
    
    # Store various types of memories
    memories = []
    
    # Store user preference
    memory_id1 = system.memory_manager.store_memory(
        content="User prefers microservices architecture over monolithic for scalability",
        memory_type="preference",
        importance=0.9,
        tags=["architecture", "preference", "scalability"]
    )
    memories.append(memory_id1)
    
    # Store technical knowledge
    memory_id2 = system.memory_manager.store_memory(
        content="Redis is excellent for caching session data due to its in-memory nature",
        memory_type="knowledge",
        importance=0.8,
        tags=["redis", "caching", "database", "performance"]
    )
    memories.append(memory_id2)
    
    # Store project context
    memory_id3 = system.memory_manager.store_memory(
        content="Current project is a fintech application requiring PCI compliance",
        memory_type="context",
        importance=0.95,
        tags=["fintech", "compliance", "pci", "project"]
    )
    memories.append(memory_id3)
    
    print(f"Stored {len(memories)} memories")
    
    # Retrieve memories by tags
    architecture_memories = system.memory_manager.retrieve_memories(
        query="architecture",
        tags=["architecture"],
        limit=5
    )
    
    print(f"\n📚 Retrieved {len(architecture_memories)} architecture-related memories:")
    print("-" * 40)
    for memory in architecture_memories:
        print(f"Type: {memory.type}, Importance: {memory.importance}")
        print(f"Content: {memory.content[:100]}...")
        print()


async def run_all_examples():
    """Run all examples"""
    print("🚀 ADVANCED AGENTIC AI FRAMEWORK - EXAMPLES")
    print("=" * 60)
    
    try:
        # Note: These examples require a valid API key
        # For demonstration, we'll show the structure
        
        print("📝 NOTE: These examples require a valid Perplexity API key")
        print("Set your API key in the .env file to run the examples")
        print()
        
        # Run tool execution example (doesn't need API key)
        await example_4_tool_execution()
        
        # Show agent creation (doesn't need API key)
        await example_5_custom_agent()
        
        # Show memory management (doesn't need API key)
        await example_6_memory_management()
        
        print("\n" + "=" * 60)
        print("ADDITIONAL EXAMPLES (API key required):")
        print("=" * 60)
        
        examples = [
            "1. Software Architecture Design",
            "2. Code Debugging", 
            "3. Data Pipeline Design",
            "4. Tool Execution ✓",
            "5. Custom Agent Creation ✓",
            "6. Memory Management ✓",
            "7. Interactive Session Simulation"
        ]
        
        for example in examples:
            print(f"  {example}")
        
        print(f"\n✅ Example demonstration complete!")
        print("🔑 Set PERPLEXITY_API_KEY in .env to run full examples")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    asyncio.run(run_all_examples())
