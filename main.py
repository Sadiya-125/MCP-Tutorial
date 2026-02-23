"""
Lab 8: Feedback Loops & Iterative Refinement
=============================================
Building on Lab 7, we add self-reflection and error tracking.

Key Changes from Lab 7:
- Added feedback/ package with reviewer and error tracker
- Output review for quality assessment
- Error tracking for learning from mistakes
"""

from mcp import Orchestrator
from execution.pipeline import create_mcp_pipeline
from feedback import OutputReviewer, ErrorTracker


def main():
    """Main loop with feedback and self-correction."""
    print("=" * 60)
    print("Lab 8: Feedback Loops & Iterative Refinement")
    print("=" * 60)
    print("\nThe assistant now SELF-REFLECTS and IMPROVES.")
    print("\nCommands:")
    print("  'review' - Review last output quality")
    print("  'errors' - View tracked errors")
    print("  'quality' - View average quality score")
    print("  'pipeline' - View pipeline status")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    orchestrator = Orchestrator(use_persistent_memory=True)
    pipeline = create_mcp_pipeline(orchestrator)
    reviewer = OutputReviewer()
    error_tracker = ErrorTracker()

    last_output = ""
    last_query = ""

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            lower_input = user_input.lower()

            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if lower_input == 'review' and last_output:
                result = reviewer.review(last_output, last_query)
                print(f"\nQuality Score: {result.quality_score:.2f}")
                if result.issues:
                    print(f"Issues: {', '.join(result.issues)}")
                if result.suggestions:
                    print(f"Suggestions: {', '.join(result.suggestions)}")
                print()
                continue

            if lower_input == 'errors':
                print(f"\n{error_tracker.to_context_string()}")
                stats = error_tracker.get_stats()
                print(f"Total: {stats['total']}, Unresolved: {stats['unresolved']}\n")
                continue

            if lower_input == 'quality':
                avg = reviewer.get_average_quality()
                print(f"\nAverage Quality: {avg:.2f}")
                issues = reviewer.get_common_issues()
                if issues:
                    print(f"Common Issues: {', '.join(issues)}")
                print()
                continue

            if lower_input == 'pipeline':
                print(f"\n{pipeline.get_status()}\n")
                continue

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            # Execute through pipeline
            last_query = user_input
            result = pipeline.execute({"user_input": user_input})

            if result.success:
                last_output = str(result.output)
                print(f"\nAssistant: {result.output}\n")
            else:
                error_tracker.track("pipeline_error", result.error or "Unknown error")
                print(f"\nError: {result.error}\n")

        except Exception as e:
            error_tracker.track("exception", str(e))
            print(f"\nError: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
