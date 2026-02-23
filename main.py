"""
Lab 7: MCP Execution Flow
=========================
Building on Lab 6, we implement a deterministic execution pipeline.

Key Changes from Lab 6:
- Added execution/ package with pipeline
- Deterministic 5-step execution flow
- Traceable execution history

Key Learning Points:
- Deterministic execution pipelines
- Why execution flow matters more than prompts
- Context flows through the pipeline
"""

from mcp import Orchestrator
from execution.pipeline import create_mcp_pipeline


def main():
    """
    Main interaction loop with deterministic execution pipeline.

    Pipeline Steps:
    1. Initialize Context
    2. Interpret Instruction
    3. Decide Action
    4. Invoke Tool/Generate Response
    5. Update State
    """
    print("=" * 60)
    print("Lab 7: MCP Execution Flow")
    print("=" * 60)
    print("\nExecution is now DETERMINISTIC and TRACEABLE.")
    print("\nPipeline Steps:")
    print("  1. Initialize Context")
    print("  2. Interpret Instruction")
    print("  3. Decide Action")
    print("  4. Invoke Tool")
    print("  5. Update State")
    print("\nCommands:")
    print("  'pipeline' - View pipeline status")
    print("  'trace' - Run with visible trace")
    print("  'hierarchy' - View context hierarchy")
    print("  'status' - View system status")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    orchestrator = Orchestrator(use_persistent_memory=True)
    pipeline = create_mcp_pipeline(orchestrator)

    # Show initial state
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

            if lower_input == 'pipeline':
                print(f"\n{pipeline.get_status()}\n")
                history = pipeline.get_history()
                if history:
                    print(f"Executions: {len(history)}")
                    last = history[-1]
                    print(f"Last: {last['duration_ms']:.1f}ms, {last['steps_completed']} steps\n")
                continue

            if lower_input == 'hierarchy':
                print(f"\n{orchestrator.get_context_summary()}\n")
                continue

            if lower_input == 'memory':
                if orchestrator.persistent_memory:
                    print(f"\n{orchestrator.persistent_memory.to_context_string()}\n")
                continue

            # Trace mode - show pipeline execution
            if lower_input.startswith('trace '):
                query = user_input[6:].strip()
                print("\n--- Pipeline Execution Trace ---")

                # Execute through pipeline
                result = pipeline.execute({"user_input": query})

                print(f"\nSteps completed: {result.steps_completed}")
                print(f"Duration: {result.duration_ms:.1f}ms")
                print(f"Success: {result.success}")

                if result.success:
                    print(f"\nOutput:\n{result.output}\n")
                else:
                    print(f"\nError: {result.error}\n")
                continue

            # Project/task commands
            if lower_input.startswith('project '):
                parts = user_input[8:].split(' ', 1)
                if parts[0].lower() == 'lang' and len(parts) > 1:
                    orchestrator.context_hierarchy.project_ctx.language = parts[1]
                    print(f"\nProject language: {parts[1]}\n")
                elif parts[0].lower() == 'framework' and len(parts) > 1:
                    orchestrator.context_hierarchy.project_ctx.framework = parts[1]
                    print(f"\nProject framework: {parts[1]}\n")
                else:
                    orchestrator.set_project(parts[0])
                    print(f"\nProject set: {parts[0]}\n")
                continue

            if lower_input.startswith('task:'):
                task_desc = user_input[5:].strip()
                orchestrator.set_task(task_desc, goal=task_desc)
                print(f"\nTask started: {task_desc}\n")
                continue

            # Execute through pipeline
            result = pipeline.execute({"user_input": user_input})

            if result.success:
                print(f"\nAssistant: {result.output}\n")
            else:
                print(f"\nError: {result.error}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
