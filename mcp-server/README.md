# Awesome Dev MCP

An awesome Model Context Protocol (MCP) server built with FastMCP 2.0 that provides development tools and utilities for enhanced developer productivity.

## Features

### Tools
- **Mathematical Operations**: Add and multiply numbers
- **File System Operations**: List directories, read files, get file information, search files
- **System Commands**: Execute shell commands with output capture
- **System Information**: Get current directory and system details

### Resources
- **Current Directory**: Get the current working directory path
- **System Info**: Retrieve system and Python environment information

## Installation

1. Install `uv` package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
uv add fastmcp
```

## Configuration

The server can be configured using environment variables or the `.env` file:

- `MCP_SERVER_NAME`: Server display name
- `MCP_SERVER_VERSION`: Server version
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Log file path
- `MAX_FILE_SIZE_MB`: Maximum file size for operations (MB)
- `COMMAND_TIMEOUT_SECONDS`: Command execution timeout
- `MAX_SEARCH_RESULTS`: Maximum search results returned
- `DEBUG`: Enable debug mode (true/false)
- `ENABLE_METRICS`: Enable metrics collection (true/false)

## Running the Server

### Local Development
```bash
export PATH="$HOME/.local/bin:$PATH"
uv run server.py
```

### Using FastMCP CLI
```bash
fastmcp run server.py
```

## Available Tools

### Mathematical Tools
- `add_numbers(a: int, b: int) -> int`: Add two integers
- `multiply_numbers(a: float, b: float) -> float`: Multiply two numbers

### File System Tools
- `list_directory(path: str = ".") -> List[Dict]`: List directory contents
- `read_file(file_path: str, max_lines: int = 100) -> Dict`: Read file contents
- `search_files(pattern: str, directory: str = ".", max_results: int = 10) -> List[Dict]`: Search for files
- `get_file_info(file_path: str) -> Dict`: Get detailed file information

### System Tools
- `run_command(command: str, working_dir: str = ".") -> Dict`: Execute shell commands

## Available Resources
- `file://current-directory`: Current working directory
- `file://system-info`: System and Python environment information

## Security Features

- Command execution timeout (30 seconds default)
- File size limits for read operations
- Comprehensive error handling and logging
- Input validation and sanitization

## Logging

The server logs all operations to both console and file (`mcp-server.log`). Log levels and file paths are configurable through environment variables.

## Error Handling

All tools include comprehensive error handling with informative error messages returned in the response format. Errors are also logged for debugging purposes.

## Development

To extend this server:

1. Add new tools using the `@mcp.tool` decorator
2. Add new resources using the `@mcp.resource("uri")` decorator
3. Update configuration in `config.py` for new settings
4. Add logging for new operations

Example tool:
```python
@mcp.tool
def my_tool(param: str) -> Dict[str, Any]:
    """Description of what the tool does."""
    logger.info(f"Executing my_tool with param: {param}")
    try:
        # Tool implementation
        return {"result": "success"}
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return {"error": str(e)}
```