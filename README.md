# MCP Teaching Repository

## Branch: v3-goal-agent

This is **Lab 3 - From Chatbot to Agent**: Adding goals and a basic task loop so the assistant works step-by-step instead of responding once.

### Learning Objectives
- Explain the difference between reactive and goal-driven AI systems
- Implement a task-oriented agent loop
- Describe how agent behavior emerges from context and goals

### Key Changes from v2
- Added `agent.py` with Goal and Agent classes
- Agent can decompose goals into steps
- Step-by-step execution with progress tracking

### New Files
- `agent.py` - Goal-oriented agent with planning and execution

### Setup

```bash
pip install -r requirements.txt
python main.py
```

### Try These Experiments

1. Set a goal:
   ```
   goal: Create a Python function to validate email addresses
   ```

2. View the generated plan:
   ```
   status
   ```

3. Execute step by step:
   ```
   next
   next
   next
   ```

4. Or run all steps automatically:
   ```
   goal: Build a simple calculator class
   run all
   ```

### Key Concepts

**Reactive Chatbot (v1-v2):**
```
User: "How do I validate emails?"
Bot: [Answers question]
User: "Now add error handling"
Bot: [Doesn't remember previous context]
```

**Goal-Driven Agent (v3):**
```
User: "goal: Create email validation with error handling"
Agent: [Plans steps]
  1. Create base validation function
  2. Add regex pattern matching
  3. Add error handling
  4. Write tests
Agent: [Executes each step, maintaining context]
```

The assistant now **acts** towards goals, not just **responds** to questions!

---

## Branch Navigation

| Branch | Lab | Description |
|--------|-----|-------------|
| `v1-prompt-baseline` | Lab 1 | Naive prompt-based assistant |
| `v2-structured-context` | Lab 2 | Externalizing context |
| `v3-goal-agent` | Lab 3 | Goal-oriented agent (current) |
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
