"""
Prompts module - Contains all MCP prompts organized by category.
"""

# Import registration functions only
from .development.code_quality import register_code_quality_prompts
from .development.workflow import register_workflow_prompts
from .architecture.backend import register_backend_prompts
from .architecture.data import register_data_prompts
from .architecture.domain import register_domain_prompts
from .specialization.debugging import register_debugging_prompts
from .specialization.documentation import register_documentation_prompts

__all__ = [
    'register_code_quality_prompts',
    'register_workflow_prompts',
    'register_backend_prompts',
    'register_data_prompts',
    'register_domain_prompts',
    'register_debugging_prompts',
    'register_documentation_prompts',
]