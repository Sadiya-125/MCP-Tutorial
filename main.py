"""
Lab 2: Structured Context
=========================
Building on Lab 1, we now separate context from prompts.

Key Changes from Lab 1:
- Context is now a structured object (context.py)
- Prompts are minimal - context is injected separately
- The assistant can now "remember" within a session

Key Learning Points:
- Prompt ≠ memory
- Repetition is not persistence
- Structured context objects enable stateful behavior
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from context import Context, create_context

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Minimal system prompt - context is now external!
SYSTEM_PROMPT = """You are a helpful coding assistant.
You have access to a context object that maintains state across the conversation.
Use the context to remember information and provide consistent help.

When the user provides information (name, project details, etc.), acknowledge it
and refer back to it in future responses.

Be concise and provide working code examples when appropriate."""


def get_response(user_message: str, context: Context) -> str:
    """
    Get a response from the AI using structured context.

    Key improvement: Context is now injected into the prompt,
    allowing the assistant to "remember" information.
    """
    # Build the context-aware prompt
    context_str = context.to_prompt_context()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": f"Current Context:\n{context_str}"
        },
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


def parse_context_commands(user_input: str, context: Context) -> tuple[bool, str]:
    """
    Parse special commands that update context.

    This demonstrates how structured context enables commands
    that modify state without prompt engineering.
    """
    lower_input = user_input.lower()

    # Name command
    if lower_input.startswith("my name is "):
        name = user_input[11:].strip()
        context.user_name = name
        context.add_note(f"User introduced themselves as {name}")
        return True, f"Nice to meet you, {name}! I'll remember that."

    # Task command
    if lower_input.startswith("task:"):
        task_desc = user_input[5:].strip()
        context.set_task(task_desc)
        context.add_note(f"Started task: {task_desc}")
        return True, f"Got it! I'm now tracking this task: {task_desc}"

    # File command
    if lower_input.startswith("working on "):
        filename = user_input[11:].strip()
        context.set_file_context(filename)
        context.add_note(f"Now working on {filename}")
        return True, f"Noted! You're working on {filename}."

    # Framework command
    if lower_input.startswith("using "):
        framework = user_input[6:].strip()
        context.file_info.framework = framework
        context.add_note(f"Using framework: {framework}")
        return True, f"Got it! You're using {framework}."

    # Show context command
    if lower_input in ["context", "show context", "status"]:
        return True, f"Current Context:\n{context.to_prompt_context()}"

    return False, ""


def main():
    """
    Main interaction loop with structured context.

    Improvements over Lab 1:
    1. Context persists within session
    2. Special commands update context directly
    3. AI responses are context-aware
    """
    print("=" * 60)
    print("Lab 2: Structured Context")
    print("=" * 60)
    print("\nThis assistant now has SESSION memory via structured context.")
    print("\nSpecial commands:")
    print("  'my name is <name>' - Set your name")
    print("  'task: <description>' - Set current task")
    print("  'working on <file>' - Set current file")
    print("  'using <framework>' - Set framework")
    print("  'context' - Show current context")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    # Create structured context - this persists for the session
    context = create_context()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # First, check for context commands
            handled, response = parse_context_commands(user_input, context)

            if handled:
                print(f"\nAssistant: {response}\n")
            else:
                # Get AI response with context
                response = get_response(user_input, context)
                print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
