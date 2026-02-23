# MCP Teaching Repository

## Branch: v7-execution-flow

This is **Lab 7 - MCP Execution Flow**: Implementing a deterministic execution pipeline that initializes context, decides actions, and updates state.

### Learning Objectives
- Describe the MCP execution lifecycle
- Implement deterministic execution pipelines
- Trace how context flows through an AI system

### Key Changes from v6
- Added `execution/` package with pipeline
- 5-step deterministic execution flow
- Traceable execution history

### Pipeline Steps

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                           │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  1. INITIALIZE CONTEXT                                  │
│     Load context from all sources                       │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  2. INTERPRET INSTRUCTION                               │
│     Parse and understand user intent                    │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  3. DECIDE ACTION                                       │
│     Choose: command, goal, or question                  │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  4. INVOKE ACTION                                       │
│     Execute tool or generate response                   │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│  5. UPDATE STATE                                        │
│     Save results and update context                     │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│                     OUTPUT                              │
└─────────────────────────────────────────────────────────┘
```

### Setup

```bash
pip install -r requirements.txt
python main.py
```

### Try These Experiments

1. View pipeline status:
   ```
   pipeline
   ```

2. Run with trace to see execution flow:
   ```
   trace What is Python?
   trace goal: Build a REST API
   ```

3. See execution history after multiple queries

### Key Concepts

**Why Deterministic Pipelines?**
- **Predictability**: Same input → same flow
- **Debuggability**: Trace exactly what happened
- **Testability**: Test each step independently
- **Control**: Modify specific steps without breaking others

This is the **core MCP runtime**!

---

## Branch Navigation

| Branch | Lab | Description |
|--------|-----|-------------|
| `v1-prompt-baseline` | Lab 1 | Naive prompt-based assistant |
| `v2-structured-context` | Lab 2 | Externalizing context |
| `v3-goal-agent` | Lab 3 | Goal-oriented agent |
| `v4-mcp-roles` | Lab 4 | MCP role architecture |
| `v5-memory-guardrails` | Lab 5 | Persistent memory + safety |
| `v6-context-hierarchy` | Lab 6 | Context hierarchy |
| `v7-execution-flow` | Lab 7 | Execution pipeline (current) |
| `v8-feedback-loop` | Lab 8 | Self-reflecting assistant |
| `v9-prompt-vs-mcp` | Lab 9 | Prompt reduction experiment |
| `v10-file-docking` | Lab 10 | Editor and file dock |
| `v11-codebase-aware` | Lab 11 | Codebase-aware assistant |
| `v12-final-mcp` | Lab 12 | Final MCP docked system |
| `main` | Final | Complete MCP implementation |
