"""
File system tools for directory listing, file reading, searching, and file information.
"""

import glob
import time
import logging
from pathlib import Path
from typing import List, Dict, Any
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register_file_tools(mcp: FastMCP):
    """Register all file system tools with the MCP server."""

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
    def search_files(pattern: str, directory: str = ".", max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for files matching a pattern in the specified directory.

        Args:
            pattern: File pattern to search for (supports wildcards)
            directory: Directory to search in (default: current directory)
            max_results: Maximum number of results to return

        Returns:
            List of matching files with their paths and sizes
        """
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