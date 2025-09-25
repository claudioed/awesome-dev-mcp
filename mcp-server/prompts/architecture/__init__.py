"""
Architecture prompts - Backend, API, database, and domain design expertise.
"""

from .backend import *
from .data import *
from .domain import *

__all__ = [
    # Backend architecture prompts
    'api_development_prompt',
    'backend_developer_prompt',

    # Data architecture prompts
    'database_designer_prompt',

    # Domain architecture prompts
    'ddd_architect_prompt',
]