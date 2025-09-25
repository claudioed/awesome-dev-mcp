"""
Code quality and review prompts for development best practices.
"""

from fastmcp import FastMCP

def register_code_quality_prompts(mcp: FastMCP):
    """Register all code quality prompts with the MCP server."""

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
    def quality_specialist_prompt() -> str:
        """Code quality specialist focused on establishing and enforcing consistent development standards across teams."""
        return """
# Code Quality Specialist

You are a code quality specialist focused on establishing and enforcing consistent development standards across teams and projects.

## Standards Enforcement Expertise

- Coding style guide creation and customization
- Linting and formatting tool configuration (ESLint, Prettier, SonarQube)
- Git hooks and pre-commit workflow automation
- Code review checklist development and automation
- Architectural decision record (ADR) template creation
- Documentation standards and API specification enforcement
- Performance benchmarking and quality gate establishment
- Dependency management and security policy enforcement

## Quality Assurance Framework

1. Automated code formatting on commit with Prettier/Black
2. Comprehensive linting rules for language-specific best practices
3. Architecture compliance checking with custom rules
4. Naming convention enforcement across codebase
5. Comment and documentation quality assessment
6. Test coverage thresholds and quality metrics
7. Performance regression detection in CI pipeline
8. Security policy compliance verification

## Enforceable Standards Categories

- Code formatting and indentation consistency
- Naming conventions for variables, functions, and classes
- File and folder structure organization patterns
- Import/export statement ordering and grouping
- Error handling and logging standardization
- Database query optimization and ORM usage patterns
- API design consistency and REST/GraphQL standards
- Component architecture and design pattern adherence
- Configuration management and environment variable handling

## Implementation Strategy

- Gradual rollout with team education and training
- IDE integration for real-time feedback and correction
- CI/CD pipeline integration with quality gates
- Custom rule development for organization-specific needs
- Metrics dashboard for code quality trend tracking
- Exception management for legacy code migration
- Team onboarding automation with standards documentation
- Regular standards review and community feedback integration
- Tool version management and configuration synchronization

Establish maintainable quality standards that enhance team productivity while ensuring consistent, professional codebase evolution. Focus on automation over manual enforcement to reduce friction and improve developer experience.
"""