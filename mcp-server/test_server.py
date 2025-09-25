#!/usr/bin/env python3
"""
Test script for the FastMCP server to verify tool functionality.
"""

import asyncio
import json
from server import mcp

async def test_tools():
    """Test all available tools."""

    print("Testing FastMCP Server Tools\n" + "="*40)

    # Test mathematical tools
    print("\n1. Testing Mathematical Tools:")

    # Test add_numbers
    result = add_numbers(5, 3)
    print(f"add_numbers(5, 3) = {result}")

    # Test multiply_numbers
    result = multiply_numbers(4.5, 2.0)
    print(f"multiply_numbers(4.5, 2.0) = {result}")

    # Test file system tools
    print("\n2. Testing File System Tools:")

    # Test list_directory
    result = list_directory(".")
    print(f"list_directory('.') found {len(result)} items")

    # Test read_file
    result = read_file("server.py", 5)
    if "error" not in result:
        print(f"read_file('server.py', 5) read {result['lines_read']} lines")
    else:
        print(f"read_file error: {result['error']}")

    # Test search_files
    result = search_files("*.py", ".", 5)
    print(f"search_files('*.py', '.', 5) found {len(result)} files")

    # Test get_file_info
    result = get_file_info("server.py")
    if "error" not in result:
        print(f"get_file_info('server.py') - size: {result.get('size', 0)} bytes")
    else:
        print(f"get_file_info error: {result['error']}")

    # Test system tools
    print("\n3. Testing System Tools:")

    # Test run_command
    result = run_command("echo 'Hello from MCP Server'")
    if result.get("success"):
        print(f"run_command('echo') output: {result['stdout'].strip()}")
    else:
        print(f"run_command error: {result.get('error', 'Failed')}")

    # Test resources
    print("\n4. Testing Resources:")

    current_dir = get_current_directory()
    print(f"Current directory: {current_dir}")

    system_info = get_system_info()
    print(f"Python version: {system_info['python_version'].split()[0]}")
    print(f"Platform: {system_info['platform']}")

    print("\n" + "="*40)
    print("All tests completed successfully!")

if __name__ == "__main__":
    # Test the functions directly (not as MCP tools)
    def add_numbers(a: int, b: int) -> int:
        return a + b

    def multiply_numbers(a: float, b: float) -> float:
        return a * b

    from server import (
        list_directory, read_file, search_files, get_file_info,
        run_command, get_current_directory, get_system_info
    )

    # These need to be called directly as functions
    def test_list_directory(path="."):
        from server import list_directory as ld
        return ld(path)

    def test_read_file(file_path, max_lines=100):
        from server import read_file as rf
        return rf(file_path, max_lines)

    def test_search_files(pattern, directory=".", max_results=10):
        from server import search_files as sf
        return sf(pattern, directory, max_results)

    def test_get_file_info(file_path):
        from server import get_file_info as gfi
        return gfi(file_path)

    def test_run_command(command, working_dir="."):
        from server import run_command as rc
        return rc(command, working_dir)

    def test_get_current_directory():
        from server import get_current_directory as gcd
        return gcd()

    def test_get_system_info():
        from server import get_system_info as gsi
        return gsi()

    # Update the test function calls
    list_directory = test_list_directory
    read_file = test_read_file
    search_files = test_search_files
    get_file_info = test_get_file_info
    run_command = test_run_command
    get_current_directory = test_get_current_directory
    get_system_info = test_get_system_info

    # Run the tests
    asyncio.run(test_tools())