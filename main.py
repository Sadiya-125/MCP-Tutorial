"""
Lab 6: Context Design & Hierarchy
==================================
Building on Lab 5, we organize context into reusable, hierarchical layers.

Key Changes from Lab 5:
- Added context/ package with hierarchy
- Context levels: Global, Project, Task, Session
- Modular and scalable context management

Key Learning Points:
- Global vs local context
- Reusable context schemas
- Failure modes from poor context design
"""

from mcp import Orchestrator


def main():
    """
    Main interaction loop with context hierarchy.

    Context Layers:
    1. Global - System-wide settings
    2. Project - Project-specific context
    3. Task - Current task context
    4. Session - Current session state
    """
    print("=" * 60)
    print("Lab 6: Context Design & Hierarchy")
    print("=" * 60)
    print("\nContext is now MODULAR and SCALABLE.")
    print("\nContext Layers:")
    print("  - Global: System-wide settings")
    print("  - Project: Project-specific context")
    print("  - Task: Current task context")
    print("  - Session: Current session state")
    print("\nCommands:")
    print("  'hierarchy' - View context hierarchy")
    print("  'project <name>' - Set project name")
    print("  'project lang <language>' - Set project language")
    print("  'project framework <framework>' - Set framework")
    print("  'task: <description>' - Set current task")
    print("  'status' - View system status")
    print("  'memory' - View persistent memory")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

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

            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            if lower_input == 'hierarchy':
                print(f"\n{orchestrator.get_context_summary()}\n")
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

            # Project commands
            if lower_input.startswith('project '):
                parts = user_input[8:].split(' ', 1)
                if parts[0].lower() == 'lang' and len(parts) > 1:
                    orchestrator.context_hierarchy.project_ctx.language = parts[1]
                    print(f"\nProject language set to: {parts[1]}\n")
                elif parts[0].lower() == 'framework' and len(parts) > 1:
                    orchestrator.context_hierarchy.project_ctx.framework = parts[1]
                    print(f"\nProject framework set to: {parts[1]}\n")
                else:
                    result = orchestrator.set_project(parts[0])
                    print(f"\n{result}\n")
                continue

            # Task commands
            if lower_input.startswith('task:'):
                task_desc = user_input[5:].strip()
                result = orchestrator.set_task(task_desc, goal=task_desc)
                print(f"\n{result}\n")
                continue

            if lower_input in ['next', 'step']:
                result = orchestrator.execute_step()
                print(f"\nAssistant: {result}\n")
                continue

            # Remember/recall commands
            if lower_input.startswith('remember '):
                parts = user_input[9:].split(' ', 1)
                if len(parts) == 2:
                    result = orchestrator.tools.invoke('remember', key=parts[0], value=parts[1])
                    print(f"\n{result.output}\n")
                continue

            if lower_input.startswith('recall '):
                key = user_input[7:].strip()
                result = orchestrator.tools.invoke('recall', key=key)
                print(f"\n{result.output}\n")
                continue

            # Increment session message count
            orchestrator.context_hierarchy.session_ctx.increment_messages()

            # Process through the orchestrator
            response = orchestrator.process(user_input)
            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
