"""
Lab 3: From Chatbot to Agent
============================
Building on Lab 2, we transform the reactive chatbot into a goal-driven agent.

Key Changes from Lab 2:
- Added agent.py with goal-oriented behavior
- Agent works step-by-step towards goals
- Plans are generated and executed automatically

Key Learning Points:
- Reactive vs goal-driven systems
- What makes an "agent"
- Agent behavior emerges from context and goals
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from context import Context, create_context
from agent import Agent

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt
SYSTEM_PROMPT = """You are a helpful coding assistant with goal-oriented capabilities.
You can work step-by-step towards goals, not just answer questions reactively.
Use the context to maintain state and track progress."""


def get_response(user_message: str, context: Context) -> str:
    """Get a response for general questions (non-goal tasks)."""
    context_str = context.to_prompt_context()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Current Context:\n{context_str}"},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def parse_commands(user_input: str, context: Context, agent: Agent) -> tuple[bool, str]:
    """Parse commands including agent commands."""
    lower_input = user_input.lower()

    # Context commands (from Lab 2)
    if lower_input.startswith("my name is "):
        name = user_input[11:].strip()
        context.user_name = name
        context.add_note(f"User introduced themselves as {name}")
        return True, f"Nice to meet you, {name}!"

    if lower_input.startswith("working on "):
        filename = user_input[11:].strip()
        context.set_file_context(filename)
        return True, f"Noted! Working on {filename}."

    if lower_input.startswith("using "):
        framework = user_input[6:].strip()
        context.file_info.framework = framework
        return True, f"Got it! Using {framework}."

    if lower_input in ["context", "show context"]:
        return True, f"Context:\n{context.to_prompt_context()}"

    # NEW: Agent commands
    if lower_input.startswith("goal:"):
        goal_desc = user_input[5:].strip()
        goal = agent.set_goal(goal_desc)
        context.add_note(f"Set goal: {goal_desc}")
        return True, f"Goal set! Here's the plan:\n\n{agent.get_status()}"

    if lower_input in ["status", "plan", "progress"]:
        return True, agent.get_status()

    if lower_input in ["next", "step", "continue"]:
        result = agent.execute_current_step()
        return True, f"Step result:\n\n{result}\n\n{agent.get_status()}"

    if lower_input in ["run", "run all", "auto"]:
        results = agent.run_all()
        output = "\n\n---\n\n".join(results)
        return True, f"Executed all steps:\n\n{output}\n\n{agent.get_status()}"

    return False, ""


def main():
    """
    Main interaction loop with goal-oriented agent.

    Improvements over Lab 2:
    1. Can set goals and generate plans
    2. Executes steps towards goals
    3. Agent acts, not just responds
    """
    print("=" * 60)
    print("Lab 3: From Chatbot to Agent")
    print("=" * 60)
    print("\nThis assistant is now GOAL-ORIENTED - it acts, not just responds.")
    print("\nAgent commands:")
    print("  'goal: <description>' - Set a goal (generates a plan)")
    print("  'status' - View current goal and progress")
    print("  'next' - Execute the next step")
    print("  'run all' - Execute all remaining steps")
    print("\nContext commands (from Lab 2):")
    print("  'my name is <name>', 'working on <file>', 'using <framework>'")
    print("  'context' - Show current context")
    print("\nType 'quit' to exit.\n")
    print("-" * 60 + "\n")

    # Create context and agent
    context = create_context()
    agent = Agent(context)

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Check for commands
            handled, response = parse_commands(user_input, context, agent)

            if handled:
                print(f"\nAssistant: {response}\n")
            else:
                # General question - use LLM
                response = get_response(user_input, context)
                print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
