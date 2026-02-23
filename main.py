"""
Lab 11: MCP + Codebase: Multi-File Understanding
=================================================
Project-wide reasoning and codebase awareness.
"""

from mcp import Orchestrator
from execution.pipeline import create_mcp_pipeline
from tools import FileReader, EditorContext
from analysis import CodebaseAnalyzer


def main():
    """Main loop with codebase analysis."""
    print("=" * 60)
    print("Lab 11: Codebase-Aware Assistant")
    print("=" * 60)
    print("\nMCP now understands multi-file codebases.")
    print("\nCommands:")
    print("  'analyze [path]' - Analyze codebase")
    print("  'find <name>' - Find files by name")
    print("  'func <name>' - Find functions by name")
    print("  'class <name>' - Find classes by name")
    print("  'context' - View codebase context")
    print("  'read <file>' - Read a file")
    print("  'editor' - View editor context")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    orchestrator = Orchestrator(use_persistent_memory=True)
    pipeline = create_mcp_pipeline(orchestrator)
    file_reader = FileReader()
    editor = EditorContext()
    analyzer = CodebaseAnalyzer()

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            lower_input = user_input.lower()

            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if lower_input.startswith('analyze'):
                path = user_input[7:].strip() or "."
                analyzer = CodebaseAnalyzer(path)
                info = analyzer.analyze(force_refresh=True)
                print(f"\n=== Codebase Analysis ===")
                print(f"Root: {info.root_path}")
                print(f"Files: {info.total_files}")
                print(f"Lines: {info.total_lines}")
                print(f"Languages: {', '.join(f'{k}({v})' for k, v in info.languages.items())}")
                print()
                continue

            if lower_input.startswith('find '):
                name = user_input[5:].strip()
                results = analyzer.find_file(name)
                print(f"\nFiles matching '{name}':")
                for f in results[:10]:
                    print(f"  - {f.path} ({f.lines} lines)")
                print()
                continue

            if lower_input.startswith('func '):
                name = user_input[5:].strip()
                results = analyzer.find_function(name)
                print(f"\nFunctions matching '{name}':")
                for path, func in results[:10]:
                    print(f"  - {path}: {func}")
                print()
                continue

            if lower_input.startswith('class '):
                name = user_input[6:].strip()
                results = analyzer.find_class(name)
                print(f"\nClasses matching '{name}':")
                for path, cls in results[:10]:
                    print(f"  - {path}: {cls}")
                print()
                continue

            if lower_input == 'context':
                print(f"\n{analyzer.to_context_string()}\n")
                continue

            if lower_input.startswith('read '):
                filepath = user_input[5:].strip()
                content = file_reader.read(filepath)
                if content:
                    print(f"\n--- {content.path} ({content.lines} lines) ---")
                    print(content.content[:500])
                    if len(content.content) > 500:
                        print("... (truncated)")
                    print()
                else:
                    print("\nCould not read file.\n")
                continue

            if lower_input == 'editor':
                print(f"\n{editor.to_context_string()}\n")
                continue

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            # Regular execution with codebase context
            ctx = {
                "user_input": user_input,
                "editor": editor.to_context_string(),
                "codebase": analyzer.to_context_string()
            }
            result = pipeline.execute(ctx)
            if result.success:
                print(f"\nAssistant: {result.output}\n")
            else:
                print(f"\nError: {result.error}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
