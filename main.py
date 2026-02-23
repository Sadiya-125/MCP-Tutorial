"""
Lab 5: State, Memory, and Guardrails
=====================================
Building on Lab 4, we add persistent memory and safety constraints.

Key Changes from Lab 4:
- Added memory/ package with persistent storage
- Added guardrails/ package with safety rules
- Memory survives across sessions
- Actions are checked against guardrails

Key Learning Points:
- Persistent vs ephemeral state
- Why AI needs rules
- Implementing capability boundaries
"""

from mcp import Orchestrator


def main():
    """
    Main interaction loop with persistent memory and guardrails.

    New features:
    - Memory persists to disk (memory/data/memory.json)
    - Safety guardrails check all actions
    - Warnings for potentially sensitive operations
    """
    print("=" * 60)
    print("Lab 5: State, Memory, and Guardrails")
    print("=" * 60)
    print("\nThe assistant is now SAFE and PERSISTENT.")
    print("\nNew Features:")
    print("  - Memory persists across sessions (to disk)")
    print("  - Safety guardrails check all actions")
    print("  - Warnings for sensitive operations")
    print("\nCommands:")
    print("  'status' - View system status")
    print("  'memory' - View persistent memory")
    print("  'guardrails' - View safety rules")
    print("  'remember <key> <value>' - Store persistently")
    print("  'recall <key>' - Retrieve from memory")
    print("  'search <query>' - Search memory")
    print("  'forget <key>' - Remove from memory")
    print("  'goal: <description>' - Set a goal")
    print("  'next' - Execute next step")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    # Create the MCP orchestrator with persistent memory
    orchestrator = Orchestrator(use_persistent_memory=True)

    # Show initial memory state
    if orchestrator.persistent_memory:
        stats = orchestrator.persistent_memory.get_stats()
        if stats['total_entries'] > 0:
            print(f"Loaded {stats['total_entries']} entries from persistent memory.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            lower_input = user_input.lower()

            # Handle special commands
            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye! Your memory has been saved.")
                break

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            if lower_input == 'memory':
                if orchestrator.persistent_memory:
                    print(f"\n{orchestrator.persistent_memory.to_context_string()}\n")
                else:
                    print("\nPersistent memory not enabled.\n")
                continue

            if lower_input == 'guardrails':
                print(f"\n{orchestrator.get_guardrail_status()}\n")
                continue

            if lower_input == 'tools':
                tools = orchestrator.tools.list_tools()
                print("\nAvailable tools:")
                for t in tools:
                    print(f"  - {t['name']}: {t['description']}")
                print()
                continue

            if lower_input in ['next', 'step']:
                result = orchestrator.execute_step()
                print(f"\nAssistant: {result}\n")
                continue

            # Handle remember command
            if lower_input.startswith('remember '):
                parts = user_input[9:].split(' ', 1)
                if len(parts) == 2:
                    result = orchestrator.tools.invoke('remember', key=parts[0], value=parts[1])
                    print(f"\n{result.output}\n")
                else:
                    print("\nUsage: remember <key> <value>\n")
                continue

            # Handle recall command
            if lower_input.startswith('recall '):
                key = user_input[7:].strip()
                result = orchestrator.tools.invoke('recall', key=key)
                print(f"\n{result.output}\n")
                continue

            # Handle search command
            if lower_input.startswith('search '):
                query = user_input[7:].strip()
                result = orchestrator.tools.invoke('search_memory', query=query)
                print(f"\n{result.output}\n")
                continue

            # Handle forget command
            if lower_input.startswith('forget '):
                key = user_input[7:].strip()
                result = orchestrator.tools.invoke('forget', key=key)
                print(f"\n{result.output}\n")
                continue

            # Process through the orchestrator
            response = orchestrator.process(user_input)
            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye! Your memory has been saved.")
            break


if __name__ == "__main__":
    main()
