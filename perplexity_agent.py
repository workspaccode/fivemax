#!/usr/bin/env python3
"""
Perplexity AI Agent CLI
A powerful command-line interface for interacting with Perplexity AI
"""

import os
import sys
from typing import Optional, List, Dict
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv

# Use OpenAI client for Perplexity API compatibility
from openai import OpenAI
PERPLEXITY_AVAILABLE = True

# Load environment variables
load_dotenv()

console = Console()


class PerplexityAgent:
    """Main agent class for interacting with Perplexity API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "sonar"):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Set PERPLEXITY_API_KEY environment variable or pass it directly.")
        
        self.model = model
        self.conversation_history: List[Dict] = []
        
        if PERPLEXITY_AVAILABLE:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.perplexity.ai"
            )
        else:
            self.client = None
            self.base_url = "https://api.perplexity.ai"
    
    def chat(self, message: str, stream: bool = True, return_sources: bool = True) -> str:
        """Send a chat message and get response"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        if PERPLEXITY_AVAILABLE:
            # Use OpenAI client with Perplexity API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                stream=stream
            )
            
            if stream:
                full_response = ""
                console.print("\n[bold cyan]Assistant:[/bold cyan]")
                for chunk in response:
                    if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        console.print(content, end="")
                console.print("\n")
                
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                return full_response
            else:
                content = response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": content
                })
                return content
        else:
            # Fallback to direct API calls
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "stream": stream
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                stream=stream
            )
            
            if stream:
                full_response = ""
                console.print("\n[bold cyan]Assistant:[/bold cyan]")
                for line in response.iter_lines():
                    if line:
                        try:
                            import json
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                line_str = line_str[6:]
                            if line_str.strip() == '[DONE]':
                                break
                            data = json.loads(line_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    content = delta['content']
                                    full_response += content
                                    console.print(content, end="")
                        except:
                            pass
                console.print("\n")
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })
                return full_response
            else:
                data = response.json()
                content = data['choices'][0]['message']['content']
                self.conversation_history.append({
                    "role": "assistant",
                    "content": content
                })
                return content
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        """Perform a web search using Perplexity Search API"""
        
        if PERPLEXITY_AVAILABLE and hasattr(self.client, 'search'):
            try:
                response = self.client.search.create(
                    query=query,
                    max_results=max_results
                )
                return {
                    'results': [
                        {
                            'title': r.title,
                            'url': r.url,
                            'snippet': getattr(r, 'snippet', '')
                        }
                        for r in response.results
                    ]
                }
            except Exception as e:
                console.print(f"[red]Search API error: {e}[/red]")
                return {'results': []}
        else:
            # Fallback: use chat with search-focused prompt
            search_prompt = f"Search the web for: {query}\n\nProvide a concise summary with sources."
            response = self.chat(search_prompt, stream=False)
            return {'answer': response}
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        console.print("[yellow]Conversation history cleared.[/yellow]")


@click.group()
def cli():
    """Perplexity AI Agent - Your AI-powered research assistant"""
    pass


@cli.command()
@click.option('--model', default='sonar', help='Model to use (sonar, sonar-pro, etc.)')
@click.option('--api-key', envvar='PERPLEXITY_API_KEY', help='Perplexity API key')
def chat(model, api_key):
    """Start an interactive chat session"""
    
    console.print(Panel.fit(
        "[bold cyan]Perplexity AI Agent - Chat Mode[/bold cyan]\n"
        "Type 'exit' or 'quit' to end the session\n"
        "Type 'clear' to clear conversation history\n"
        "Type 'help' for more commands",
        border_style="cyan"
    ))
    
    try:
        agent = PerplexityAgent(api_key=api_key, model=model)
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if user_input.lower() in ['exit', 'quit']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                elif user_input.lower() == 'clear':
                    agent.clear_history()
                    continue
                elif user_input.lower() == 'help':
                    console.print("""
[bold]Available Commands:[/bold]
- exit/quit: End the session
- clear: Clear conversation history
- help: Show this help message
                    """)
                    continue
                
                # Send message and get response
                agent.chat(user_input, stream=True)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
                continue
                
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--model', default='sonar', help='Model to use')
@click.option('--api-key', envvar='PERPLEXITY_API_KEY', help='Perplexity API key')
def ask(query, model, api_key):
    """Ask a single question"""
    
    try:
        agent = PerplexityAgent(api_key=api_key, model=model)
        
        console.print(f"\n[bold green]Query:[/bold green] {query}\n")
        response = agent.chat(query, stream=True)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--max-results', default=5, help='Maximum number of results')
@click.option('--api-key', envvar='PERPLEXITY_API_KEY', help='Perplexity API key')
def search(query, max_results, api_key):
    """Search the web"""
    
    try:
        agent = PerplexityAgent(api_key=api_key)
        
        console.print(f"\n[bold green]Searching for:[/bold green] {query}\n")
        results = agent.search(query, max_results=max_results)
        
        if 'results' in results:
            for i, result in enumerate(results['results'], 1):
                console.print(f"\n[bold cyan]{i}. {result['title']}[/bold cyan]")
                console.print(f"   {result['url']}")
                if result.get('snippet'):
                    console.print(f"   {result['snippet']}")
        elif 'answer' in results:
            console.print(results['answer'])
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def setup():
    """Setup wizard for API key configuration"""
    
    console.print(Panel.fit(
        "[bold cyan]Perplexity AI Agent Setup[/bold cyan]\n"
        "Let's configure your API key",
        border_style="cyan"
    ))
    
    console.print("\n[bold]Step 1:[/bold] Get your API key")
    console.print("1. Go to https://www.perplexity.ai/settings")
    console.print("2. Click on the '</> API' tab")
    console.print("3. Generate a new API key\n")
    
    api_key = Prompt.ask("[bold]Enter your API key[/bold]", password=True)
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"PERPLEXITY_API_KEY={api_key}\n")
    
    console.print("\n[bold green]✓[/bold green] API key saved to .env file")
    console.print("\n[bold]You're all set![/bold] Try:")
    console.print("  python perplexity_agent.py chat")
    console.print("  python perplexity_agent.py ask 'What are the latest AI developments?'")


@cli.command()
def models():
    """List available models"""
    
    console.print("\n[bold cyan]Available Models:[/bold cyan]\n")
    
    models_info = [
        ("sonar", "Fast and efficient model for general queries"),
        ("sonar-pro", "Advanced model with enhanced capabilities"),
        ("sonar-reasoning", "Specialized for complex reasoning tasks"),
        ("sonar-small-online", "Small model with web search"),
        ("sonar-medium-online", "Medium model with web search"),
        ("sonar-large-online", "Large model with web search"),
    ]
    
    for model_name, description in models_info:
        console.print(f"[bold]{model_name}[/bold]")
        console.print(f"  {description}\n")


if __name__ == "__main__":
    cli()
