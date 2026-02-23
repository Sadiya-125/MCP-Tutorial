"""
Lab 1: Prompt-Only Baseline
===========================
A simple prompt-based coding assistant demonstrating the limitations
of AI without structure, memory, or context.

Key Learning Points:
- No memory between interactions
- No structured context
- No predictability
- This is the baseline failure case that MCP will fix
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simple system prompt - everything hardcoded
SYSTEM_PROMPT = """You are a helpful coding assistant.
Help users with their programming questions and tasks.
Be concise and provide working code examples when appropriate."""


def get_response(user_message: str) -> str:
    """
    Get a response from the AI using only prompts.

    Notice: No memory, no context, no state - just raw prompting.
    Each call is completely independent.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """
    Main interaction loop.

    Problems you'll observe:
    1. No memory - it forgets everything between messages
    2. No context - doesn't know about your project
    3. No structure - can't maintain consistent behavior
    """
    print("=" * 60)
    print("Lab 1: Prompt-Only Baseline")
    print("=" * 60)
    print("\nThis assistant has NO memory and NO context.")
    print("Try asking it to remember something, then ask about it.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Each response is independent - no memory!
            response = get_response(user_input)
            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
