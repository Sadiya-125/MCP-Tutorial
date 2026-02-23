# MCP Teaching Repository

## Branch: v6-context-hierarchy

This is **Lab 6 - Context Design & Hierarchy**: Organizing context into reusable layers (global, project, task) to support scalability.

### Learning Objectives
- Design reusable context blocks
- Differentiate between global and task-level context
- Identify failure modes caused by poor context design

### Key Changes from v5
- Added `context/` package with hierarchical context
- Four context levels: Global, Project, Task, Session
- Modular and scalable context management

### New Files
```
context/
├── __init__.py
├── global_context.py    # System-wide settings
├── project_context.py   # Project-specific context
├── task_context.py      # Current task context
├── session_context.py   # Session state
└── hierarchy.py         # Context hierarchy manager
```

### Context Hierarchy

```
┌─────────────────────────────────────┐
│           GLOBAL CONTEXT            │  ← System-wide
│   (model, settings, constraints)    │
├─────────────────────────────────────┤
│          PROJECT CONTEXT            │  ← Project-specific
│   (name, language, framework)       │
├─────────────────────────────────────┤
│           TASK CONTEXT              │  ← Current task
│   (title, goal, steps, files)       │
├─────────────────────────────────────┤
│          SESSION CONTEXT            │  ← Current session
│   (user, topics, temp data)         │
└─────────────────────────────────────┘
```

### Setup

```bash
pip install -r requirements.txt
python main.py
```

### Try These Experiments

1. Set up project context:
   ```
   project MyWebApp
   project lang Python
   project framework FastAPI
   ```

2. View the hierarchy:
   ```
   hierarchy
   ```

3. Set a task in context:
   ```
   task: Implement user authentication
   ```

4. See how context flows into prompts - the AI now knows your project!

### Key Concepts

**Why Hierarchy?**
- **Separation of concerns**: Different scopes, different contexts
- **Reusability**: Project context persists, task context changes
- **Scalability**: Add new context levels without breaking existing ones

**Context Inheritance:**
```
Global: safe_mode=True
  └─ Project: language=Python, framework=FastAPI
       └─ Task: Implement authentication
            └─ Session: User=Alice, Messages=5
```

---

## Branch Navigation

| Branch | Lab | Description |
|--------|-----|-------------|
| `v1-prompt-baseline` | Lab 1 | Naive prompt-based assistant |
| `v2-structured-context` | Lab 2 | Externalizing context |
| `v3-goal-agent` | Lab 3 | Goal-oriented agent |
| `v4-mcp-roles` | Lab 4 | MCP role architecture |
| `v5-memory-guardrails` | Lab 5 | Persistent memory + safety |
| `v6-context-hierarchy` | Lab 6 | Context hierarchy (current) |
| `v7-execution-flow` | Lab 7 | Full MCP execution loop |
| `v8-feedback-loop` | Lab 8 | Self-reflecting assistant |
| `v9-prompt-vs-mcp` | Lab 9 | Prompt reduction experiment |
| `v10-file-docking` | Lab 10 | Editor and file dock |
| `v11-codebase-aware` | Lab 11 | Codebase-aware assistant |
| `v12-final-mcp` | Lab 12 | Final MCP docked system |
| `main` | Final | Complete MCP implementation |
