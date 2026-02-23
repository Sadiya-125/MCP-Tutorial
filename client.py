"""
MCP Client
==========
Lab 12: Complete MCP Client connecting to server via JSON-RPC.
"""

import json
import subprocess
import sys
from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class MCPResponse:
    """Response from MCP server."""
    success: bool
    data: Any
    error: Optional[str] = None


class MCPClient:
    """
    MCP Client that connects to server via JSON-RPC over stdio.

    Usage:
        client = MCPClient()
        client.connect()
        resources = client.list_resources()
        client.disconnect()
    """

    def __init__(self, server_command: list[str] = None):
        self.server_command = server_command or [sys.executable, "server.py"]
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0

    def connect(self) -> MCPResponse:
        """Connect to MCP server."""
        try:
            self.process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Initialize connection
            response = self._send_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp-teaching-client", "version": "1.0.0"}
            })

            return response

        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))

    def disconnect(self):
        """Disconnect from server."""
        if self.process:
            self.process.terminate()
            self.process = None

    def list_resources(self) -> MCPResponse:
        """List available resources."""
        return self._send_request("resources/list", {})

    def read_resource(self, uri: str) -> MCPResponse:
        """Read a resource by URI."""
        return self._send_request("resources/read", {"uri": uri})

    def list_tools(self) -> MCPResponse:
        """List available tools."""
        return self._send_request("tools/list", {})

    def call_tool(self, name: str, arguments: dict = None) -> MCPResponse:
        """Call a tool."""
        return self._send_request("tools/call", {
            "name": name,
            "arguments": arguments or {}
        })

    def _send_request(self, method: str, params: dict) -> MCPResponse:
        """Send JSON-RPC request to server."""
        if not self.process:
            return MCPResponse(success=False, data=None, error="Not connected")

        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }

        try:
            # Send request
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()

            # Read response
            response_line = self.process.stdout.readline()
            if not response_line:
                return MCPResponse(success=False, data=None, error="No response")

            response = json.loads(response_line)

            if "error" in response:
                return MCPResponse(
                    success=False,
                    data=None,
                    error=response["error"].get("message", "Unknown error")
                )

            return MCPResponse(success=True, data=response.get("result"))

        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))


def demo():
    """Demonstrate MCP client usage."""
    print("=" * 60)
    print("MCP Client Demo")
    print("=" * 60)

    client = MCPClient()

    print("\n1. Connecting to MCP server...")
    result = client.connect()
    if result.success:
        print(f"   Connected! Server: {result.data.get('serverInfo', {}).get('name')}")
    else:
        print(f"   Error: {result.error}")
        return

    print("\n2. Listing resources...")
    result = client.list_resources()
    if result.success:
        for r in result.data.get("resources", []):
            print(f"   - {r['uri']}: {r['name']}")

    print("\n3. Reading git status...")
    result = client.read_resource("git://status")
    if result.success:
        contents = result.data.get("contents", [])
        if contents:
            print(f"   {contents[0].get('text', '')[:200]}")

    print("\n4. Listing tools...")
    result = client.list_tools()
    if result.success:
        for t in result.data.get("tools", []):
            print(f"   - {t['name']}: {t['description']}")

    print("\n5. Calling analyze_codebase tool...")
    result = client.call_tool("analyze_codebase", {"path": "."})
    if result.success:
        content = result.data.get("content", [])
        if content:
            text = content[0].get("text", "")
            print(f"   {text[:300]}...")

    print("\n6. Disconnecting...")
    client.disconnect()
    print("   Done!")


if __name__ == "__main__":
    demo()
