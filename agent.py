#!/usr/bin/env python3
"""
A general-purpose CLI agent powered by CrewAI and Ollama.
"""

import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme

# Load environment variables
load_dotenv()

# Custom theme for beautiful output
custom_theme = Theme({
    "user": "bold cyan",
    "agent": "bold green",
    "error": "bold red",
    "info": "dim white",
})

console = Console(theme=custom_theme)

# Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Set environment variable for CrewAI to use Ollama
os.environ["OPENAI_API_BASE"] = OLLAMA_HOST
os.environ["OPENAI_MODEL_NAME"] = f"ollama/{OLLAMA_MODEL}"
os.environ["OPENAI_API_KEY"] = "NA"  # Not needed for Ollama but required by CrewAI


def create_assistant_agent() -> Agent:
    """Create the main assistant agent."""
    return Agent(
        role="General Assistant",
        goal="Help users with any questions or tasks they have",
        backstory="""You are a helpful, friendly, and knowledgeable AI assistant.
        You provide clear, accurate, and well-structured responses.
        You can help with coding, writing, analysis, research, and general questions.
        When appropriate, use markdown formatting for better readability.""",
        verbose=False,
        llm=f"ollama/{OLLAMA_MODEL}",
    )


def display_welcome():
    """Display welcome message."""
    welcome_text = f"""
# 🤖 CrewAI CLI Agent

Welcome! I'm your AI assistant powered by **CrewAI** + **Ollama**.

**Model:** `{OLLAMA_MODEL}`

**Commands:**
- Type your message to chat
- Type `exit` or `quit` to exit

Let's get started!
    """
    console.print(Panel(Markdown(welcome_text), border_style="cyan"))


def run_task(agent: Agent, user_input: str) -> str:
    """Run a task with the agent and return the response."""
    task = Task(
        description=f"Respond to the user's message: {user_input}",
        expected_output="A helpful and informative response to the user's query",
        agent=agent,
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )
    
    result = crew.kickoff()
    return str(result)


def main():
    """Main function to run the CLI agent."""
    display_welcome()
    
    # Setup CrewAI with Ollama
    console.print("[info]Initializing CrewAI with Ollama...[/info]")
    
    try:
        agent = create_assistant_agent()
        console.print("[info]Ready![/info]\n")
    except Exception as e:
        console.print(f"[error]Failed to initialize: {e}[/error]")
        console.print("[info]Make sure Ollama is running: ollama serve[/info]")
        sys.exit(1)
    
    while True:
        try:
            # Get user input
            console.print("[user]You:[/user] ", end="")
            user_input = input().strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ["exit", "quit"]:
                console.print("\n[info]Goodbye! 👋[/info]")
                break
            
            # Run the task
            console.print()
            with console.status("[info]Thinking...[/info]", spinner="dots"):
                response = run_task(agent, user_input)
            
            # Display response
            console.print("[agent]Agent:[/agent]")
            console.print(Panel(Markdown(response), border_style="green"))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n\n[info]Goodbye! 👋[/info]")
            break
        except Exception as e:
            console.print(f"[error]Error: {e}[/error]\n")


if __name__ == "__main__":
    main()
