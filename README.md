# MCP Teaching Repository

## Branch: v5-memory-guardrails

This is **Lab 5 - State, Memory, and Guardrails**: Introducing persistent memory and safety constraints to control what the assistant can and cannot do.

### Learning Objectives
- Implement capability boundaries for AI systems
- Design persistent memory for stateful behavior
- Explain why guardrails are essential in AI tooling

### Key Changes from v4
- Added `memory/` package with persistent storage
- Added `guardrails/` package with safety rules
- Memory survives across sessions
- Actions are checked against guardrails

### New Files
```
memory/
├── __init__.py
└── store.py        # JSON-based persistent storage

guardrails/
├── __init__.py
└── rules.py        # Safety rules and constraints
```

### Setup

```bash
pip install -r requirements.txt
python main.py
```

### Try These Experiments

1. Test persistent memory:
   ```
   remember name Alice
   remember project MyApp
   quit
   ```
   Then restart and:
   ```
   memory
   recall name
   ```
   Your data persists!

2. View guardrails:
   ```
   guardrails
   ```

3. Test guardrails (try storing a very large value):
   ```
   remember bigdata [paste 10000+ characters]
   ```
   It will be blocked by the memory size limit!

### Key Concepts

**Persistent vs Ephemeral State:**
```
Session Memory (v4):    Persistent Memory (v5):
┌─────────────────┐     ┌─────────────────┐
│  Lost on exit   │     │  Saved to disk  │
│                 │     │                 │
│  Fast, simple   │     │  Survives       │
│                 │     │  restarts       │
└─────────────────┘     └─────────────────┘
```

**Why Guardrails?**
- Prevent accidental data loss (no silent deletes)
- Block dangerous operations (no shell execution)
- Warn about sensitive data access
- Enforce resource limits

**Default Guardrails:**
| Rule | Severity | Description |
|------|----------|-------------|
| no_silent_delete | HIGH | Requires confirmation for deletions |
| no_shell_exec | CRITICAL | Blocks shell command execution |
| sensitive_file_warning | MEDIUM | Warns on .env, password, etc. |
| no_system_modification | CRITICAL | Blocks system file writes |
| memory_size_limit | LOW | Limits stored value size |

The assistant is now **safe and controllable**!

---

## Branch Navigation

| Branch | Lab | Description |
|--------|-----|-------------|
| `v1-prompt-baseline` | Lab 1 | Naive prompt-based assistant |
| `v2-structured-context` | Lab 2 | Externalizing context |
| `v3-goal-agent` | Lab 3 | Goal-oriented agent |
| `v4-mcp-roles` | Lab 4 | MCP role architecture |
| `v5-memory-guardrails` | Lab 5 | Persistent memory + safety (current) |
| `v6-context-hierarchy` | Lab 6 | Context blocks and hierarchy |
| `v7-execution-flow` | Lab 7 | Full MCP execution loop |
| `v8-feedback-loop` | Lab 8 | Self-reflecting assistant |
| `v9-prompt-vs-mcp` | Lab 9 | Prompt reduction experiment |
| `v10-file-docking` | Lab 10 | Editor and file dock |
| `v11-codebase-aware` | Lab 11 | Codebase-aware assistant |
| `v12-final-mcp` | Lab 12 | Final MCP docked system |
| `main` | Final | Complete MCP implementation |
