"""
Mathematical tools for basic arithmetic operations.
"""

from fastmcp import FastMCP

def register_math_tools(mcp: FastMCP):
    """Register all mathematical tools with the MCP server."""

    @mcp.tool
    def add_numbers(a: int, b: int) -> int:
        """Add two numbers together."""
        return a + b

    @mcp.tool
    def multiply_numbers(a: float, b: float) -> float:
        """Multiply two numbers together."""
        return a * b