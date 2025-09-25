#!/usr/bin/env python3
"""
FastMCP 2.0 Server - Modular Implementation
A development tools MCP server with organized modular structure.
"""

from fastmcp import FastMCP
import logging
from shared.config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(config.server_name)

logger.info("Starting MCP server initialization")

# Register all modules
from tools.math_tools import register_math_tools
from tools.file_tools import register_file_tools
from tools.system_tools import register_system_tools
from prompts import (
    register_code_quality_prompts,
    register_workflow_prompts,
    register_backend_prompts,
    register_data_prompts,
    register_domain_prompts,
    register_debugging_prompts,
    register_documentation_prompts
)
from resources.system_resources import register_system_resources

# Register all tools
register_math_tools(mcp)
register_file_tools(mcp)
register_system_tools(mcp)

# Register all prompts by category
register_code_quality_prompts(mcp)
register_workflow_prompts(mcp)
register_backend_prompts(mcp)
register_data_prompts(mcp)
register_domain_prompts(mcp)
register_debugging_prompts(mcp)
register_documentation_prompts(mcp)

# Register all resources
register_system_resources(mcp)

logger.info("MCP server modules registered successfully")

if __name__ == "__main__":
    mcp.run()