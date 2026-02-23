"""
MCP Server
==========
Lab 12: Complete MCP Server with resources and tools.

Implements JSON-RPC 2.0 over stdio for MCP protocol.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Any


class MCPServer:
    """
    MCP Server implementing JSON-RPC 2.0 protocol.

    Resources:
    - git://status - Current git status
    - git://commits - Recent commits
    - todo://list - TODO.md contents

    Tools:
    - add_todo - Add item to TODO.md
    - read_file - Read a file
    - analyze_codebase - Analyze codebase structure
    """

    def __init__(self):
        self.root_path = Path(".")
        self.todo_file = self.root_path / "TODO.md"

    def handle_request(self, request: dict) -> dict:
        """Handle incoming JSON-RPC request."""
        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        try:
            if method == "initialize":
                result = self._initialize(params)
            elif method == "resources/list":
                result = self._list_resources()
            elif method == "resources/read":
                result = self._read_resource(params)
            elif method == "tools/list":
                result = self._list_tools()
            elif method == "tools/call":
                result = self._call_tool(params)
            else:
                return self._error_response(req_id, -32601, f"Method not found: {method}")

            return self._success_response(req_id, result)

        except Exception as e:
            return self._error_response(req_id, -32603, str(e))

    def _initialize(self, params: dict) -> dict:
        """Initialize the server."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "resources": {"subscribe": False, "listChanged": False},
                "tools": {}
            },
            "serverInfo": {
                "name": "mcp-teaching-server",
                "version": "1.0.0"
            }
        }

    def _list_resources(self) -> dict:
        """List available resources."""
        return {
            "resources": [
                {
                    "uri": "git://status",
                    "name": "Git Status",
                    "description": "Current git repository status",
                    "mimeType": "text/plain"
                },
                {
                    "uri": "git://commits",
                    "name": "Recent Commits",
                    "description": "Recent git commit history",
                    "mimeType": "text/plain"
                },
                {
                    "uri": "todo://list",
                    "name": "TODO List",
                    "description": "Contents of TODO.md",
                    "mimeType": "text/markdown"
                }
            ]
        }

    def _read_resource(self, params: dict) -> dict:
        """Read a resource by URI."""
        uri = params.get("uri", "")

        if uri == "git://status":
            content = self._get_git_status()
        elif uri == "git://commits":
            content = self._get_git_commits()
        elif uri == "todo://list":
            content = self._get_todo_list()
        else:
            raise ValueError(f"Unknown resource: {uri}")

        return {
            "contents": [
                {"uri": uri, "mimeType": "text/plain", "text": content}
            ]
        }

    def _list_tools(self) -> dict:
        """List available tools."""
        return {
            "tools": [
                {
                    "name": "add_todo",
                    "description": "Add an item to TODO.md",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "item": {"type": "string", "description": "Todo item text"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"]}
                        },
                        "required": ["item"]
                    }
                },
                {
                    "name": "read_file",
                    "description": "Read contents of a file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path"}
                        },
                        "required": ["path"]
                    }
                },
                {
                    "name": "analyze_codebase",
                    "description": "Analyze codebase structure",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Root path", "default": "."}
                        }
                    }
                }
            ]
        }

    def _call_tool(self, params: dict) -> dict:
        """Call a tool."""
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        if name == "add_todo":
            result = self._add_todo(arguments)
        elif name == "read_file":
            result = self._read_file(arguments)
        elif name == "analyze_codebase":
            result = self._analyze_codebase(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

        return {"content": [{"type": "text", "text": result}]}

    def _get_git_status(self) -> str:
        """Get git status."""
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout or "Working tree clean"
        except Exception as e:
            return f"Error: {e}"

    def _get_git_commits(self) -> str:
        """Get recent commits."""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout or "No commits"
        except Exception as e:
            return f"Error: {e}"

    def _get_todo_list(self) -> str:
        """Get TODO.md contents."""
        try:
            if self.todo_file.exists():
                return self.todo_file.read_text(encoding='utf-8')
            return "# TODO\n\nNo items yet."
        except Exception as e:
            return f"Error: {e}"

    def _add_todo(self, args: dict) -> str:
        """Add item to TODO.md."""
        item = args.get("item", "")
        priority = args.get("priority", "medium")

        if not item:
            return "Error: No item provided"

        priority_markers = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        marker = priority_markers.get(priority, "🟡")

        try:
            content = ""
            if self.todo_file.exists():
                content = self.todo_file.read_text(encoding='utf-8')

            if not content.strip():
                content = "# TODO\n\n"

            content += f"- [ ] {marker} {item}\n"
            self.todo_file.write_text(content, encoding='utf-8')

            return f"Added: {item} ({priority} priority)"
        except Exception as e:
            return f"Error: {e}"

    def _read_file(self, args: dict) -> str:
        """Read a file."""
        path = args.get("path", "")
        try:
            file_path = Path(path)
            if file_path.exists():
                return file_path.read_text(encoding='utf-8')[:2000]
            return f"File not found: {path}"
        except Exception as e:
            return f"Error: {e}"

    def _analyze_codebase(self, args: dict) -> str:
        """Analyze codebase."""
        from analysis import CodebaseAnalyzer

        path = args.get("path", ".")
        analyzer = CodebaseAnalyzer(path)
        return analyzer.to_context_string()

    def _success_response(self, req_id: Any, result: Any) -> dict:
        """Create success response."""
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    def _error_response(self, req_id: Any, code: int, message: str) -> dict:
        """Create error response."""
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    def run(self):
        """Run server reading from stdin."""
        print("MCP Server started", file=sys.stderr)

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                error = self._error_response(None, -32700, f"Parse error: {e}")
                print(json.dumps(error))
                sys.stdout.flush()


def main():
    """Entry point for MCP server."""
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()
