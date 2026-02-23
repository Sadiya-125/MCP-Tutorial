# MCP Teaching Repository

## Branch: v8-feedback-loop

This is **Lab 8 - Feedback Loops & Iterative Refinement**: Adding self-reflection so the assistant can improve during execution.

### Key Changes from v7
- Added `feedback/` package with reviewer and error tracker
- Output quality review
- Error tracking for learning

### New Files
```
feedback/
├── __init__.py
├── reviewer.py      # Output quality review
└── error_tracker.py # Error tracking
```

### Commands
- `review` - Review last output quality
- `errors` - View tracked errors
- `quality` - View average quality score

The assistant now **improves during execution**!

---

## Branch Navigation

| Branch | Description |
|--------|-------------|
| `v1-prompt-baseline` | Naive prompt-based assistant |
| `v2-structured-context` | Externalizing context |
| `v3-goal-agent` | Goal-oriented agent |
| `v4-mcp-roles` | MCP role architecture |
| `v5-memory-guardrails` | Persistent memory + safety |
| `v6-context-hierarchy` | Context hierarchy |
| `v7-execution-flow` | Execution pipeline |
| `v8-feedback-loop` | Self-reflecting assistant (current) |
| `v9-prompt-vs-mcp` | Prompt reduction experiment |
| `v10-file-docking` | Editor and file dock |
| `v11-codebase-aware` | Codebase-aware assistant |
| `v12-final-mcp` | Final MCP docked system |
