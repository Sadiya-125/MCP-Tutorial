# MCP Teaching Repository

## Branch: v1-prompt-baseline

This is **Lab 1 - Prompt-Only Baseline**: A simple prompt-based coding assistant to observe how AI fails without structure, memory, or context.

### Learning Objectives
- Understand what "context" means in AI systems
- Identify limitations of prompt-only chatbots
- Observe why naive prompting fails for coding tasks

### Key Observations
- **No memory**: Each interaction starts fresh
- **No structure**: Everything embedded in prompts
- **No predictability**: Responses vary wildly

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key in .env
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the assistant
python main.py
```

### Try These Experiments

1. Ask: "Remember that my name is Alice"
2. Then ask: "What is my name?"
3. Observe: It doesn't remember!

4. Ask: "I'm working on a Python web app using Flask"
5. Then ask: "What framework am I using?"
6. Observe: Context is lost!

### What's Missing?
- Persistent memory
- Structured context
- State management
- Predictable behavior

This establishes the **baseline failure case** that MCP will fix in subsequent lessons.

---

## Branch Navigation

| Branch | Lab | Description |
|--------|-----|-------------|
| `v1-prompt-baseline` | Lab 1 | Naive prompt-based assistant (current) |
| `v2-structured-context` | Lab 2 | Externalizing context into structured data |
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

```bash
# Switch between versions
git checkout v1-prompt-baseline
git checkout v2-structured-context
# ... etc
```
