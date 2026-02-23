# MCP Teaching Repository

## Branch: v2-structured-context

This is **Lab 2 - Externalizing Context**: Separating prompts from context by moving task details and state into a structured context object.

### Learning Objectives
- Distinguish between prompts, context, and memory
- Externalize context from prompts into structured data
- Reduce prompt length without losing behavior

### Key Changes from v1
- Added `context.py` with structured context objects
- Prompts are now minimal - context is injected separately
- The assistant can "remember" within a session

### New Files
- `context.py` - Structured context with TaskInfo, FileInfo, and Context classes

### Setup

```bash
pip install -r requirements.txt
python main.py
```

### Try These Experiments

1. Set your context:
   ```
   my name is Alice
   task: Build a REST API
   working on api.py
   using FastAPI
   ```

2. Ask questions that reference context:
   ```
   What am I working on?
   What's my current task?
   ```

3. View the structured context:
   ```
   context
   ```

### Key Concepts

**Before (v1):**
```python
# Everything in the prompt
prompt = "I'm Alice, working on api.py using FastAPI, building a REST API..."
```

**After (v2):**
```python
# Structured context object
context = Context(
    user_name="Alice",
    task=TaskInfo(description="Build a REST API"),
    file_info=FileInfo(current_file="api.py", framework="FastAPI")
)
# Prompt is minimal - context injected separately
```

This is the **first MCP-style separation** - prompts become minimal!

---

## Branch Navigation

| Branch | Lab | Description |
|--------|-----|-------------|
| `v1-prompt-baseline` | Lab 1 | Naive prompt-based assistant |
| `v2-structured-context` | Lab 2 | Externalizing context (current) |
| `v3-goal-agent` | Lab 3 | Goal-oriented assistant with task loops |
| `v4-mcp-roles` | Lab 4 | MCP role architecture skeleton |
| `v5-memory-guardrails` | Lab 5 | Persistent memory and safety constraints |
| `v6-context-hierarchy` | Lab 6 | Context blocks and hierarchy |
| `v7-execution-flow` | Lab 7 | Full MCP execution loop |
| `v8-feedback-loop` | Lab 8 | Self-reflecting assistant |
| `v9-prompt-vs-mcp` | Lab 9 | Prompt reduction experiment |
| `v10-file-docking` | Lab 10 | Editor and file dock |
| `v11-codebase-aware` | Lab 11 | Codebase-aware assistant |
| `v12-final-mcp` | Lab 12 | Final MCP docked system |
| `main` | Final | Complete MCP implementation |
