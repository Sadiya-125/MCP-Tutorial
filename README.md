# MCP Teaching Repository

## Branch: v4-mcp-roles

This is **Lab 4 - MCP Role Architecture**: Refactoring the system into clear MCP roles (orchestrator, reasoner, tool handler, memory manager).

### Learning Objectives
- Identify key MCP roles and responsibilities
- Design a modular AI system architecture
- Justify role separation in MCP-based systems

### Key Changes from v3
- Created `mcp/` package with modular components
- Separated concerns into distinct roles
- Clean interfaces between components

### New Files
```
mcp/
├── __init__.py       # Package exports
├── orchestrator.py   # Coordinates execution flow
├── reasoner.py       # All LLM interactions
├── tool_handler.py   # Tool registration and execution
└── memory_manager.py # State and persistence
```

### MCP Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                        │
│              (Coordinates everything)                   │
├─────────────┬─────────────────┬────────────────────────┤
│   REASONER  │  TOOL HANDLER   │    MEMORY MANAGER      │
│   (LLM AI)  │   (Actions)     │      (State)           │
└─────────────┴─────────────────┴────────────────────────┘
```

**Why this separation?**
- **Orchestrator**: Single point of control, easy to modify flow
- **Reasoner**: All AI calls in one place, easy to swap models
- **Tool Handler**: Actions are controlled and auditable
- **Memory Manager**: State is centralized and persistent

### Setup

```bash
pip install -r requirements.txt
python main.py
```

### Try These Experiments

1. Check system status:
   ```
   status
   ```

2. List available tools:
   ```
   tools
   ```

3. Use memory:
   ```
   remember project MyAwesomeApp
   recall project
   memory
   ```

4. Set a goal:
   ```
   goal: Create a function to parse JSON
   next
   next
   ```

### Key Concepts

**Before (v3) - Monolithic:**
```python
class Agent:
    def process(self, input):
        # Everything mixed together:
        # - LLM calls
        # - Tool execution
        # - State management
        # - Flow control
```

**After (v4) - Modular MCP:**
```python
class Orchestrator:
    def __init__(self):
        self.reasoner = Reasoner()      # AI reasoning
        self.tools = ToolHandler()       # Actions
        self.memory = MemoryManager()    # State

    def process(self, input):
        # Clear flow with role separation
        intent = self.reasoner.interpret(input)
        result = self.tools.invoke(...)
        self.memory.store(...)
```

This is the **MCP "dock" structure** - modular and extensible!

---

## Branch Navigation

| Branch | Lab | Description |
|--------|-----|-------------|
| `v1-prompt-baseline` | Lab 1 | Naive prompt-based assistant |
| `v2-structured-context` | Lab 2 | Externalizing context |
| `v3-goal-agent` | Lab 3 | Goal-oriented agent |
| `v4-mcp-roles` | Lab 4 | MCP role architecture (current) |
| `v5-memory-guardrails` | Lab 5 | Persistent memory and safety |
| `v6-context-hierarchy` | Lab 6 | Context blocks and hierarchy |
| `v7-execution-flow` | Lab 7 | Full MCP execution loop |
| `v8-feedback-loop` | Lab 8 | Self-reflecting assistant |
| `v9-prompt-vs-mcp` | Lab 9 | Prompt reduction experiment |
| `v10-file-docking` | Lab 10 | Editor and file dock |
| `v11-codebase-aware` | Lab 11 | Codebase-aware assistant |
| `v12-final-mcp` | Lab 12 | Final MCP docked system |
| `main` | Final | Complete MCP implementation |
