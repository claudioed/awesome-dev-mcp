"""
System tools for executing commands and system operations.
"""

import subprocess
import logging
from typing import Dict, Any
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register_system_tools(mcp: FastMCP):
    """Register all system tools with the MCP server."""

    @mcp.tool
    def run_command(command: str, working_dir: str = ".") -> Dict[str, Any]:
        """Execute a shell command and return the result.

        Args:
            command: Shell command to execute
            working_dir: Working directory for command execution

        Returns:
            Dictionary with command output and metadata
        """
        logger.info(f"Executing command: {command} in {working_dir}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            response = {
                "command": command,
                "working_dir": working_dir,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }

            if result.returncode == 0:
                logger.info(f"Command executed successfully: {command}")
            else:
                logger.warning(f"Command failed with return code {result.returncode}: {command}")

            return response

        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command}")
            return {
                "command": command,
                "error": "Command timed out after 30 seconds"
            }
        except Exception as e:
            logger.error(f"Failed to execute command {command}: {e}")
            return {
                "command": command,
                "error": f"Failed to execute command: {str(e)}"
            }