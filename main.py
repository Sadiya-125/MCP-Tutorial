"""
Lab 10: MCP + Tooling: Code Editors & Files
===========================================
Docking file system and editor context into the MCP system.
"""

from mcp import Orchestrator
from execution.pipeline import create_mcp_pipeline
from tools import FileReader, EditorContext


def main():
    """Main loop with file and editor docking."""
    print("=" * 60)
    print("Lab 10: Editor & File Docking")
    print("=" * 60)
    print("\nMCP is now docked to files and editor context.")
    print("\nCommands:")
    print("  'read <file>' - Read a file")
    print("  'list [dir]' - List files")
    print("  'open <file>' - Set active file")
    print("  'select <text>' - Set selection")
    print("  'editor' - View editor context")
    print("  'quit' - Exit")
    print("\n" + "-" * 60 + "\n")

    orchestrator = Orchestrator(use_persistent_memory=True)
    pipeline = create_mcp_pipeline(orchestrator)
    file_reader = FileReader()
    editor = EditorContext()

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            lower_input = user_input.lower()

            if lower_input in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

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

            if lower_input.startswith('list'):
                dir_path = user_input[4:].strip() or "."
                files = file_reader.list_files(dir_path, "*.py")
                print(f"\nFiles in {dir_path}:")
                for f in files[:10]:
                    print(f"  - {f}")
                print()
                continue

            if lower_input.startswith('open '):
                filepath = user_input[5:].strip()
                editor.set_active_file(filepath)
                print(f"\nOpened: {filepath}\n")
                continue

            if lower_input.startswith('select '):
                text = user_input[7:].strip()
                editor.set_selection(text)
                print(f"\nSelected: {text[:50]}...\n")
                continue

            if lower_input == 'editor':
                print(f"\n{editor.to_context_string()}\n")
                continue

            if lower_input == 'status':
                print(f"\n{orchestrator.get_status()}\n")
                continue

            # Regular execution with editor context
            ctx = {"user_input": user_input, "editor": editor.to_context_string()}
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
