#!/usr/bin/env python3
"""
FastAPI Backend Development Examples
Demonstrating the circular review system in action
"""

import asyncio
from fastapi_developer import FastAPIBackendDeveloper

async def example_1_user_management_api():
    """Example 1: User Management API"""
    print("=" * 60)
    print("EXAMPLE 1: User Management API Development")
    print("=" * 60)
    
    # Initialize developer
    developer = FastAPIBackendDeveloper(
        api_key="your-api-key-here",
        project_path="./examples/user_management_api"
    )
    
    # Develop the feature
    feature = "Complete user management system with registration, login, profile management, and admin controls"
    
    result = await developer.develop_backend_feature(feature)
    
    print(f"\n🎯 Feature: {result['feature']}")
    print(f"🔄 Development Cycle: {result['cycle']}")
    print(f"✅ Success: {result['success']}")
    
    # Show project status
    status = developer.get_project_status()
    print(f"\n📊 Project Status:")
    print(f"  Python Files: {status['python_files']}")
    print(f"  Test Files: {status['test_files']}")
    print(f"  Test Status: {status['test_status']}")
    
    return result

async def example_2_ecommerce_products():
    """Example 2: E-commerce Products API"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: E-commerce Products API")
    print("=" * 60)
    
    developer = FastAPIBackendDeveloper(
        api_key="your-api-key-here",
        project_path="./examples/ecommerce_products"
    )
    
    feature = """
    E-commerce product management system with:
    - Product catalog with categories and tags
    - Inventory management and stock tracking
    - Product search and filtering
    - Price management with discounts
    - Product reviews and ratings
    - Admin product management interface
    """
    
    result = await developer.develop_backend_feature(feature)
    
    print(f"\n🎯 Feature: {result['feature']}")
    print(f"🔄 Development Cycle: {result['cycle']}")
    print(f"✅ Success: {result['success']}")
    
    return result

async def example_3_blog_system():
    """Example 3: Blog System API"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Blog System API")
    print("=" * 60)
    
    developer = FastAPIBackendDeveloper(
        api_key="your-api-key-here",
        project_path="./examples/blog_system"
    )
    
    feature = """
    Complete blog system with:
    - User authentication and author profiles
    - Blog post creation, editing, and deletion
    - Category and tag management
    - Comment system with moderation
    - Search functionality
    - Draft and publish workflow
    - SEO optimization features
    """
    
    result = await developer.develop_backend_feature(feature)
    
    print(f"\n🎯 Feature: {result['feature']}")
    print(f"🔄 Development Cycle: {result['cycle']}")
    print(f"✅ Success: {result['success']}")
    
    return result

async def example_4_real_time_chat():
    """Example 4: Real-time Chat API"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Real-time Chat API")
    print("=" * 60)
    
    developer = FastAPIBackendDeveloper(
        api_key="your-api-key-here",
        project_path="./examples/realtime_chat"
    )
    
    feature = """
    Real-time chat application with:
    - WebSocket connections for live messaging
    - User presence and online status
    - Chat rooms and private messages
    - Message history and search
    - File sharing capabilities
    - Push notifications
    - Message encryption and security
    """
    
    result = await developer.develop_backend_feature(feature)
    
    print(f"\n🎯 Feature: {result['feature']}")
    print(f"🔄 Development Cycle: {result['cycle']}")
    print(f"✅ Success: {result['success']}")
    
    return result

async def example_5_task_management():
    """Example 5: Task Management API"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Task Management API")
    print("=" * 60)
    
    developer = FastAPIBackendDeveloper(
        api_key="your-api-key-here",
        project_path="./examples/task_management"
    )
    
    feature = """
    Project task management system with:
    - User teams and project organization
    - Task creation, assignment, and tracking
    - Kanban board with drag-and-drop
    - Task dependencies and milestones
    - Time tracking and reporting
    - File attachments and comments
    - Notifications and reminders
    """
    
    result = await developer.develop_backend_feature(feature)
    
    print(f"\n🎯 Feature: {result['feature']}")
    print(f"🔄 Development Cycle: {result['cycle']}")
    print(f"✅ Success: {result['success']}")
    
    return result

async def demonstrate_circular_review():
    """Demonstrate the circular review process"""
    print("\n" + "=" * 60)
    print("CIRCULAR REVIEW PROCESS DEMONSTRATION")
    print("=" * 60)
    
    print("""
    🔄 The Circular Review Process:
    
    1. 🏗️  DESIGN & ARCHITECTURE
       - System Architect designs the API structure
       - Defines endpoints, models, and requirements
       - Creates technical specifications
    
    2. 💻 CODE IMPLEMENTATION
       - Backend Developer writes the actual code
       - Implements FastAPI routes and logic
       - Follows design specifications
    
    3. 🧪 TESTING
       - QA Engineer creates comprehensive tests
       - Writes unit and integration tests
       - Ensures code quality and functionality
    
    4. 🔍 CODE REVIEW
       - Code Reviewer analyzes implementation
       - Checks for security, performance, and best practices
       - Provides feedback and improvement suggestions
    
    5. 🔧 REFACTORING (if needed)
       - Refactoring Specialist improves the code
       - Addresses all review feedback
       - Optimizes performance and maintainability
    
    6. 📚 DOCUMENTATION
       - Technical Writer creates documentation
       - Generates API docs and user guides
       - Provides deployment instructions
    
    ⚡ The cycle repeats until approval is achieved!
    """)

async def run_all_examples():
    """Run all examples"""
    print("🚀 FastAPI Backend Development Examples")
    print("=" * 60)
    
    try:
        print("📝 NOTE: These examples require a valid Perplexity API key")
        print("Set your API key to run the full examples")
        print()
        
        # Demonstrate the process
        await demonstrate_circular_review()
        
        print("\n" + "=" * 60)
        print("AVAILABLE EXAMPLES:")
        print("=" * 60)
        
        examples = [
            "1. User Management API",
            "2. E-commerce Products API", 
            "3. Blog System API",
            "4. Real-time Chat API",
            "5. Task Management API"
        ]
        
        for example in examples:
            print(f"  {example}")
        
        print(f"\n🔧 CLI Usage:")
        print(f"  python fastapi_developer.py develop 'user management system'")
        print(f"  python fastapi_developer.py test")
        print(f"  python fastapi_developer.py serve --port 8000")
        print(f"  python fastapi_developer.py status")
        
        print(f"\n✅ Examples demonstration complete!")
        print("🔑 Set PERPLEXITY_API_KEY in .env to run full examples")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    asyncio.run(run_all_examples())
