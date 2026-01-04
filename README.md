# 🤖 CrewAI CLI Agent

A general-purpose command-line AI agent powered by **CrewAI** and **Ollama**.

## Features

- 🤖 **CrewAI Framework** - Built on the powerful CrewAI agent framework
- 🏠 **100% Local** - Runs with Ollama, no API keys needed
- 🎨 **Beautiful Terminal UI** - Rich formatting with colors and markdown
- ⚡ **Extensible** - Easy to add more agents and tools

## Prerequisites

### Install Ollama

Download and install from [ollama.com](https://ollama.com)

```bash
# Pull a model
ollama pull llama3.2
```

## Setup

### 1. Create Virtual Environment & Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. (Optional) Configure

Create a `.env` file:

```bash
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
```

### 3. Run

```bash
source venv/bin/activate
python agent.py
```

## Extending the Agent

### Add New Agents

```python
researcher = Agent(
    role="Researcher",
    goal="Find accurate information",
    backstory="Expert at research and fact-finding",
    llm=llm,
)
```

### Add Tools

```python
from crewai_tools import SerperDevTool, WebsiteSearchTool

search_tool = SerperDevTool()
agent = Agent(..., tools=[search_tool])
```

## License

MIT
