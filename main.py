"""
Lab 12: Complete MCP System
===========================
Full MCP implementation with server, client, and all components.
"""

from mcp import Orchestrator
from execution.pipeline import create_mcp_pipeline
from tools import FileReader, EditorContext, GitTools, TodoTools
from analysis import CodebaseAnalyzer


def main():
    """Main loop with full MCP system."""
    print("=" * 60)
    print("Lab 12: Complete MCP System")
    print("=" * 60)
    print("\nFull MCP implementation with all components.")
    print("\nCommands:")
    print("  'analyze [path]' - Analyze codebase")
    print("  'git' - Show git status")
    print("  'commits' - Show recent commits")
    print("  'todo' - Show todo list")
    print("  'add <item>' - Add todo item")
    print("  'find <name>' - Find files")
    print("  'func <name>' - Find functions")
    print("  'read <file>' - Read a file")
    print("  'server' - Start MCP server mode")
    print("  'client' - Run MCP client demo")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    orchestrator = Orchestrator(use_persistent_memory=True)
    pipeline = create_mcp_pipeline(orchestrator)
    file_reader = FileReader()
    editor = EditorContext()
    analyzer = CodebaseAnalyzer()
    git = GitTools()
    todo = TodoTools()

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            lower_input = user_input.lower()

            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if lower_input == 'server':
                print("\nStarting MCP server mode...")
                print("Use 'python server.py' for JSON-RPC server.\n")
                continue

            if lower_input == 'client':
                print("\nRunning MCP client demo...")
                from client import demo
                demo()
                continue

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

            if lower_input == 'git':
                status = git.get_status()
                if status:
                    print(f"\n{status.to_context_string()}\n")
                else:
                    print("\nNot a git repository.\n")
                continue

            if lower_input == 'commits':
                commits = git.get_recent_commits(5)
                print("\n=== Recent Commits ===")
                for c in commits:
                    print(f"  {c.hash} {c.message} ({c.author}, {c.date})")
                print()
                continue

            if lower_input == 'todo':
                todo_list = todo.read()
                print(f"\n{todo_list.to_context_string()}\n")
                continue

            if lower_input.startswith('add '):
                item = user_input[4:].strip()
                if todo.add(item):
                    print(f"\nAdded: {item}\n")
                else:
                    print("\nFailed to add item.\n")
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

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            # Regular execution with full context
            git_status = git.get_status()
            todo_list = todo.read()

            ctx = {
                "user_input": user_input,
                "editor": editor.to_context_string(),
                "codebase": analyzer.to_context_string(),
                "git": git_status.to_context_string() if git_status else "",
                "todo": todo_list.to_context_string()
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
