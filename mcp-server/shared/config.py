"""
Configuration module for the MCP server.
Handles environment variables and server settings.
"""

import os
from typing import Optional
from pathlib import Path

class Config:
    """Configuration class for MCP server settings."""

    def __init__(self):
        self.load_env()

    def load_env(self):
        """Load environment variables from .env file if it exists."""
        env_file = Path(".env")
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, _, value = line.partition('=')
                        if key and value:
                            os.environ[key] = value

    @property
    def server_name(self) -> str:
        """Get the server name."""
        return os.getenv("MCP_SERVER_NAME", "Awesome Dev MCP Server")

    @property
    def server_version(self) -> str:
        """Get the server version."""
        return os.getenv("MCP_SERVER_VERSION", "1.0.0")

    @property
    def log_level(self) -> str:
        """Get the logging level."""
        return os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def log_file(self) -> str:
        """Get the log file path."""
        return os.getenv("LOG_FILE", "mcp-server.log")

    @property
    def max_file_size_mb(self) -> int:
        """Get the maximum file size in MB."""
        return int(os.getenv("MAX_FILE_SIZE_MB", "10"))

    @property
    def command_timeout_seconds(self) -> int:
        """Get the command execution timeout in seconds."""
        return int(os.getenv("COMMAND_TIMEOUT_SECONDS", "30"))

    @property
    def max_search_results(self) -> int:
        """Get the maximum number of search results."""
        return int(os.getenv("MAX_SEARCH_RESULTS", "50"))

    @property
    def debug(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv("DEBUG", "false").lower() == "true"

    @property
    def enable_metrics(self) -> bool:
        """Check if metrics are enabled."""
        return os.getenv("ENABLE_METRICS", "true").lower() == "true"

# Global configuration instance
config = Config()