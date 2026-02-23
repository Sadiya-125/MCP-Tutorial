"""
Lab 9: Prompting vs MCP (Proof Week)
====================================
Empirically compare long prompts with MCP-driven context.
"""

from mcp import Orchestrator
from execution.pipeline import create_mcp_pipeline
from feedback import OutputReviewer, ErrorTracker
from experiments import PromptVsMCPComparison


def main():
    """Main loop with comparison experiment."""
    print("=" * 60)
    print("Lab 9: Prompting vs MCP Comparison")
    print("=" * 60)
    print("\nCompare prompt-only vs MCP approaches empirically.")
    print("\nCommands:")
    print("  'compare' - Run prompt vs MCP comparison")
    print("  'summary' - View comparison summary")
    print("  'status' - View system status")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    orchestrator = Orchestrator(use_persistent_memory=True)
    pipeline = create_mcp_pipeline(orchestrator)
    comparison = PromptVsMCPComparison()

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            lower_input = user_input.lower()

            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if lower_input == 'compare':
                print("\nRunning comparison experiment...")
                result = comparison.run_preset_comparison()
                print(f"\n=== Results ===")
                print(f"Long Prompt: {result.prompt_tokens} tokens, {result.prompt_time_ms:.0f}ms")
                print(f"MCP Approach: {result.mcp_tokens} tokens, {result.mcp_time_ms:.0f}ms")
                print(f"Token Savings: {result.token_savings:.1f}%")
                print(f"Time Savings: {result.time_savings:.1f}%\n")
                continue

            if lower_input == 'summary':
                print(f"\n{comparison.get_summary()}\n")
                continue

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            # Regular execution
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
