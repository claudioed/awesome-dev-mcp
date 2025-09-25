#!/usr/bin/env python3
"""
FastMCP 2.0 Server - Demo Implementation
A basic MCP server with common tools and resources for development tasks.
"""

from fastmcp import FastMCP
from typing import List, Dict, Any
import json
import os
import subprocess
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp-server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Development Tools Server 🛠️")

logger.info("Starting MCP server initialization")

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@mcp.tool
def list_directory(path: str = ".") -> List[Dict[str, Any]]:
    """List files and directories in the specified path.

    Args:
        path: Directory path to list (defaults to current directory)

    Returns:
        List of file/directory information including name, type, and size
    """
    logger.info(f"Listing directory: {path}")
    try:
        directory = Path(path)
        if not directory.exists():
            logger.warning(f"Directory does not exist: {path}")
            return [{"error": f"Path '{path}' does not exist"}]

        items = []
        for item in directory.iterdir():
            try:
                stat = item.stat()
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else None,
                    "modified": stat.st_mtime
                })
            except (OSError, IOError) as e:
                logger.warning(f"Could not access stats for {item.name}: {e}")
                items.append({
                    "name": item.name,
                    "type": "unknown",
                    "error": "Could not access file stats"
                })

        result = sorted(items, key=lambda x: (x.get("type", ""), x.get("name", "")))
        logger.info(f"Successfully listed {len(result)} items in {path}")
        return result

    except Exception as e:
        logger.error(f"Failed to list directory {path}: {e}")
        return [{"error": f"Failed to list directory: {str(e)}"}]

@mcp.tool
def read_file(file_path: str, max_lines: int = 100) -> Dict[str, Any]:
    """Read content from a text file.

    Args:
        file_path: Path to the file to read
        max_lines: Maximum number of lines to read (default: 100)

    Returns:
        Dictionary with file content and metadata
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File '{file_path}' does not exist"}

        if not path.is_file():
            return {"error": f"'{file_path}' is not a file"}

        with open(path, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.rstrip('\n\r'))

        return {
            "path": str(path.absolute()),
            "lines_read": len(lines),
            "content": lines,
            "truncated": i >= max_lines - 1
        }

    except UnicodeDecodeError:
        return {"error": f"File '{file_path}' is not a valid text file"}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

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

@mcp.tool
def search_files(pattern: str, directory: str = ".", max_results: int = 10) -> List[Dict[str, Any]]:
    """Search for files matching a pattern in the specified directory.

    Args:
        pattern: File pattern to search for (supports wildcards)
        directory: Directory to search in (default: current directory)
        max_results: Maximum number of results to return

    Returns:
        List of matching files with their paths and sizes
    """
    import glob

    try:
        search_path = Path(directory) / pattern
        matches = glob.glob(str(search_path), recursive=True)

        results = []
        for match in matches[:max_results]:
            path = Path(match)
            try:
                stat = path.stat()
                results.append({
                    "path": str(path.absolute()),
                    "name": path.name,
                    "size": stat.st_size if path.is_file() else None,
                    "type": "directory" if path.is_dir() else "file",
                    "modified": stat.st_mtime
                })
            except (OSError, IOError):
                results.append({
                    "path": str(path.absolute()),
                    "name": path.name,
                    "error": "Could not access file stats"
                })

        return results

    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]

@mcp.tool
def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get detailed information about a file or directory.

    Args:
        file_path: Path to the file or directory

    Returns:
        Dictionary with detailed file information
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": f"Path '{file_path}' does not exist"}

        stat = path.stat()
        import time

        info = {
            "path": str(path.absolute()),
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
            "size": stat.st_size,
            "modified": time.ctime(stat.st_mtime),
            "modified_timestamp": stat.st_mtime,
            "created": time.ctime(stat.st_ctime),
            "created_timestamp": stat.st_ctime,
            "permissions": oct(stat.st_mode)[-3:],
            "owner_uid": stat.st_uid,
            "group_gid": stat.st_gid
        }

        if path.is_file():
            info["extension"] = path.suffix
            info["stem"] = path.stem

        return info

    except Exception as e:
        return {"error": f"Failed to get file info: {str(e)}"}

# Prompts
@mcp.prompt
def code_review_prompt() -> str:
    """Generate a comprehensive code review checklist and guidelines."""
    return """
# Code Review Checklist

## Functionality
- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled properly?
- [ ] Are error conditions handled gracefully?
- [ ] Is the logic clear and correct?

## Code Quality
- [ ] Is the code readable and well-structured?
- [ ] Are variable and function names descriptive?
- [ ] Is the code properly commented where necessary?
- [ ] Are there any code smells or anti-patterns?

## Performance
- [ ] Are there any obvious performance bottlenecks?
- [ ] Is memory usage appropriate?
- [ ] Are expensive operations optimized or cached?

## Security
- [ ] Are there any security vulnerabilities?
- [ ] Is user input properly validated and sanitized?
- [ ] Are secrets and sensitive data handled securely?

## Testing
- [ ] Is the code testable?
- [ ] Are there adequate tests covering the functionality?
- [ ] Do tests cover edge cases and error conditions?

## Documentation
- [ ] Is the code properly documented?
- [ ] Are API changes documented?
- [ ] Is the README updated if necessary?
"""

@mcp.prompt
def debugging_prompt() -> str:
    """Provide a systematic debugging approach and common troubleshooting steps."""
    return """
# Debugging Methodology

## 1. Understand the Problem
- What is the expected behavior?
- What is the actual behavior?
- When did the issue start occurring?
- Can you reproduce the issue consistently?

## 2. Gather Information
- Check error messages and logs
- Identify the scope of the issue
- Document the steps to reproduce
- Note any recent changes to the codebase

## 3. Form Hypotheses
- What could be causing this issue?
- List potential root causes
- Prioritize hypotheses by likelihood

## 4. Test Hypotheses
- Use debugging tools (debugger, print statements, logging)
- Test one hypothesis at a time
- Isolate variables and test components separately
- Use binary search to narrow down the problem area

## 5. Common Debugging Techniques
- Rubber duck debugging - explain the problem out loud
- Add logging and print statements strategically
- Use a debugger to step through code
- Check assumptions and validate inputs
- Review recent changes and git history
- Test with different inputs and edge cases

## 6. Verify the Fix
- Confirm the issue is resolved
- Test related functionality
- Add tests to prevent regression
- Document the solution
"""

@mcp.prompt
def git_workflow_prompt() -> str:
    """Provide git workflow best practices and common commands."""
    return """
# Git Workflow Best Practices

## Basic Workflow
1. Pull latest changes: `git pull origin main`
2. Create feature branch: `git checkout -b feature/your-feature-name`
3. Make changes and commit frequently
4. Push to remote: `git push -u origin feature/your-feature-name`
5. Create pull request for review
6. Merge after approval and delete feature branch

## Commit Best Practices
- Write clear, descriptive commit messages
- Use imperative mood: "Add feature" not "Added feature"
- Keep commits atomic (one logical change per commit)
- Commit frequently but push when ready

## Common Git Commands
```bash
# Status and information
git status                  # Show working tree status
git log --oneline          # Show commit history
git diff                   # Show unstaged changes
git diff --staged          # Show staged changes

# Staging and committing
git add .                  # Stage all changes
git add <file>             # Stage specific file
git commit -m "message"    # Commit with message
git commit --amend         # Modify last commit

# Branching
git branch                 # List branches
git checkout -b <branch>   # Create and switch to branch
git checkout <branch>      # Switch to existing branch
git branch -d <branch>     # Delete merged branch

# Remote operations
git push origin <branch>   # Push branch to remote
git pull                   # Fetch and merge from remote
git fetch                  # Fetch from remote without merging
```

## Merge Conflicts
1. Pull latest changes
2. Git will mark conflicted files
3. Edit files to resolve conflicts
4. Remove conflict markers (<<<<<<<, =======, >>>>>>>)
5. Stage resolved files: `git add <file>`
6. Complete merge: `git commit`
"""

@mcp.prompt
def project_structure_prompt() -> str:
    """Provide guidelines for organizing project structure and architecture."""
    return """
# Project Structure Guidelines

## Python Project Structure
```
project/
├── README.md
├── requirements.txt / pyproject.toml
├── .env / .env.example
├── .gitignore
├── setup.py / setup.cfg (if packaging)
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── services/
│       ├── utils/
│       └── config/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── fixtures/
├── docs/
├── scripts/
└── data/ (if needed)
```

## MCP Server Organization Strategies

### Option 1: Monolithic Structure
- Single server.py file with all tools/prompts/resources
- Good for: Small servers, rapid prototyping
- Pros: Simple, easy to understand
- Cons: Hard to maintain as it grows

### Option 2: Modular Structure
```
mcp-server/
├── server.py (main entry point)
├── tools/
│   ├── __init__.py
│   ├── file_tools.py
│   ├── system_tools.py
│   └── math_tools.py
├── prompts/
│   ├── __init__.py
│   ├── development.py
│   └── documentation.py
├── resources/
│   ├── __init__.py
│   └── system_resources.py
├── config/
│   ├── __init__.py
│   └── settings.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

### Option 3: Feature-Based Structure
```
mcp-server/
├── server.py
├── features/
│   ├── development/
│   │   ├── tools.py
│   │   ├── prompts.py
│   │   └── resources.py
│   ├── system/
│   │   ├── tools.py
│   │   └── resources.py
│   └── documentation/
│       └── prompts.py
└── shared/
    ├── config.py
    └── utils.py
```

## Choosing the Right Structure
- **Size**: Larger projects benefit from more modular approaches
- **Team**: Multiple developers need clear separation
- **Features**: Related functionality should be grouped together
- **Maintenance**: Consider long-term maintainability
- **Testing**: Structure should support easy testing
"""

if __name__ == "__main__":
    mcp.run()