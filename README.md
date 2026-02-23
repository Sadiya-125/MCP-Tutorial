# MCP Teaching Repository

A progressive tutorial for understanding the **Modular Context Protocol (MCP)**!

## Branch: v12-final-mcp (also `main`)

This is the **complete MCP implementation** with server, client, and all components integrated.

## What is MCP?

The Modular Context Protocol separates AI assistant concerns into:
- **Context Management** - Structured, hierarchical context
- **Memory** - Persistent state across sessions
- **Guardrails** - Safety constraints and rules
- **Execution** - Deterministic pipelines
- **Feedback** - Self-reflection and correction
- **Tools** - File, editor, git, and codebase integration

## Quick Start

```bash
# Clone and checkout
git clone https://github.com/Sadiya-125/MCP-Tutorial.git
cd MCP-Tutorial

# Install dependencies
pip install -r requirements.txt

# Create .env with your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the assistant
python main.py

# Or run server/client separately
python server.py  # MCP Server (JSON-RPC)
python client.py  # MCP Client demo
```

## Branch Progression

Learn MCP concepts progressively:

| Branch | Topic | Key Learning |
|--------|-------|--------------|
| `v1-prompt-baseline` | Prompt-only | Limitations of simple prompting |
| `v2-structured-context` | Context objects | Separate context from prompts |
| `v3-goal-agent` | Goal-driven agent | Agent behavior from context + goals |
| `v4-mcp-roles` | MCP architecture | Orchestrator, Reasoner, Tools, Memory |
| `v5-memory-guardrails` | Persistence + safety | Memory across sessions, constraints |
| `v6-context-hierarchy` | Context layers | Global, project, task, session context |
| `v7-execution-flow` | Pipelines | Deterministic execution steps |
| `v8-feedback-loop` | Self-reflection | Review and error tracking |
| `v9-prompt-vs-mcp` | Comparison | Empirical MCP benefits |
| `v10-file-docking` | File access | Read files and editor state |
| `v11-codebase-aware` | Multi-file | Project-wide reasoning |
| `v12-final-mcp` | Complete system | Full MCP server + client |

## Architecture (v12)

```
mcp-teaching-repo/
├── main.py              # Entry point
├── server.py            # MCP Server (JSON-RPC)
├── client.py            # MCP Client
├── mcp/                 # Core MCP components
│   ├── orchestrator.py  # Coordinates execution
│   ├── reasoner.py      # LLM reasoning layer
│   ├── tool_handler.py  # Executes actions
│   └── memory_manager.py# Manages state
├── context/             # Context hierarchy
│   ├── global_context.py
│   ├── project_context.py
│   ├── task_context.py
│   └── session_context.py
├── memory/              # Persistent storage
│   └── store.py
├── guardrails/          # Safety rules
│   └── rules.py
├── execution/           # Execution pipeline
│   └── pipeline.py
├── feedback/            # Self-reflection
│   ├── reviewer.py
│   └── error_tracker.py
├── tools/               # Tool implementations
│   ├── file_reader.py
│   ├── editor_context.py
│   ├── git_tools.py
│   └── todo_tools.py
├── analysis/            # Codebase analysis
│   └── codebase_analyzer.py
└── experiments/         # Comparison experiments
    └── comparison.py
```

## MCP Server Resources & Tools

### Resources (read-only)
- `git://status` - Current git status
- `git://commits` - Recent commit history
- `todo://list` - TODO.md contents

### Tools (actions)
- `add_todo` - Add item to TODO.md
- `read_file` - Read file contents
- `analyze_codebase` - Analyze project structure

## Learning Path

1. **Start with v1**: See how simple prompts fail at complex tasks
2. **Progress through branches**: Each branch adds one MCP concept
3. **Compare approaches**: v9 shows empirical benefits
4. **Build understanding**: By v12, you understand the full MCP system

```bash
# Example: checkout v1 and see limitations
git checkout v1-prompt-baseline
python main.py

# Then progress to v4 and see MCP roles
git checkout v4-mcp-roles
python main.py
```

## Key Concepts

### Context Separation
MCP separates what the AI knows (context) from how it reasons (model).

### Role Boundaries
- **Orchestrator**: Manages workflow
- **Reasoner**: LLM calls only
- **ToolHandler**: Executes actions
- **MemoryManager**: State persistence

### Deterministic Execution
Pipelines ensure consistent, predictable behavior.

### Guardrails
Safety constraints prevent harmful actions.
