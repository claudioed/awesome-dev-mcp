"""
System resources for current directory and system information.
"""

import os
import sys
from typing import Dict, Any
from fastmcp import FastMCP

def register_system_resources(mcp: FastMCP):
    """Register all system resources with the MCP server."""

    @mcp.resource("file://current-directory")
    def get_current_directory() -> str:
        """Get the current working directory path."""
        return os.getcwd()

    @mcp.resource("file://system-info")
    def get_system_info() -> Dict[str, Any]:
        """Get system information including Python version and platform."""
        import platform

        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_executable": sys.executable
        }