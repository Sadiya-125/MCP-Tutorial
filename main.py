"""
Lab 4: MCP Role Architecture
============================
Building on Lab 3, we refactor into clear MCP roles with separation of concerns.

Key Changes from Lab 3:
- Created mcp/ package with modular components
- Orchestrator: coordinates execution
- Reasoner: handles all LLM interactions
- ToolHandler: manages tool execution
- MemoryManager: handles state and persistence

Key Learning Points:
- Why monolithic AI systems fail
- MCP role separation and boundaries
- Designing modular AI system architecture
"""

from mcp import Orchestrator


def main():
    """
    Main interaction loop using MCP architecture.

    The system is now modular:
    - Orchestrator handles the flow
    - Reasoner does AI reasoning
    - Tools execute actions
    - Memory manages state

    This is the MCP "dock" structure!
    """
    print("=" * 60)
    print("Lab 4: MCP Role Architecture")
    print("=" * 60)
    print("\nThe system is now modular with clear role separation.")
    print("\nMCP Components:")
    print("  - Orchestrator: Coordinates the flow")
    print("  - Reasoner: LLM-based reasoning")
    print("  - ToolHandler: Executes actions")
    print("  - MemoryManager: Manages state")
    print("\nCommands:")
    print("  'status' - View MCP system status")
    print("  'memory' - View current memory")
    print("  'tools' - List available tools")
    print("  'goal: <description>' - Set a goal")
    print("  'next' - Execute next step")
    print("  'remember <key> <value>' - Store in memory")
    print("  'recall <key>' - Retrieve from memory")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    # Create the MCP orchestrator
    orchestrator = Orchestrator()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            lower_input = user_input.lower()

            # Handle special commands
            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            if lower_input == 'memory':
                print(f"\n{orchestrator.memory.to_context_string()}\n")
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

            # Process through the orchestrator
            response = orchestrator.process(user_input)
            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
