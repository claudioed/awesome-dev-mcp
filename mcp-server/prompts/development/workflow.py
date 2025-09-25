"""
Development workflow and project management prompts.
"""

from fastmcp import FastMCP

def register_workflow_prompts(mcp: FastMCP):
    """Register all workflow prompts with the MCP server."""

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