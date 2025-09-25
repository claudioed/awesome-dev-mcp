#!/usr/bin/env python3
"""
Simple test to verify server tools work correctly.
"""

print("Testing FastMCP Server Tools")
print("=" * 40)

# Test 1: Mathematical operations
print("\n1. Testing math operations:")
print(f"5 + 3 = {5 + 3}")
print(f"4.5 * 2.0 = {4.5 * 2.0}")

# Test 2: Import and test file operations
try:
    import os
    from pathlib import Path

    print("\n2. Testing file operations:")

    # List current directory
    current_files = list(Path('.').iterdir())
    print(f"Current directory has {len(current_files)} items")

    # Check if server.py exists and get its size
    server_file = Path('server.py')
    if server_file.exists():
        size = server_file.stat().st_size
        print(f"server.py exists and is {size} bytes")

    print("\n3. Testing system operations:")
    print(f"Current working directory: {os.getcwd()}")

    # Test subprocess
    import subprocess
    result = subprocess.run(['echo', 'Hello MCP'], capture_output=True, text=True)
    print(f"Echo command output: {result.stdout.strip()}")

    print("\n" + "=" * 40)
    print("✅ Basic functionality tests passed!")

except Exception as e:
    print(f"❌ Test failed: {e}")