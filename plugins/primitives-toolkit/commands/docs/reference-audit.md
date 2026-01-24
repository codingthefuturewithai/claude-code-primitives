---
description: Discover all documentation in the project and synchronize it with the current state of the code
argument-hint: "[focus area] (optional)"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Edit", "Task"]
---

# Documentation Audit

## Goal

Discover all documentation across the project, compare it against the actual codebase, and create a plan to synchronize documentation with the current state of the code.

## Discovery Phase

First, discover where documentation lives in this project:

1. **Find all markdown files**: Search for `*.md` files throughout the entire project
2. **Identify documentation directories**: Look for common patterns like `docs/`, `documentation/`, `.reference/`, `wiki/`, `guides/`, or any other directories containing documentation
3. **Check the `.claude` directory**: Examine commands, settings, hooks, and any other Claude Code configuration for documented behavior
4. **Read README files**: Find all README.md files at any level of the project
5. **Look for inline documentation**: Identify code comments, docstrings, or JSDoc that make claims about behavior

## Analysis Phase

For each piece of documentation discovered:

1. **Verify code references**: Does the code/file/function mentioned actually exist?
2. **Validate behavior claims**: Do the documented behaviors match what the code actually does?
3. **Check for completeness**: Are there significant code features that aren't documented anywhere?
4. **Identify stale content**: Are there references to removed or renamed components?
5. **Cross-reference**: Do different documentation sources contradict each other?

## Output

After discovery and analysis, produce:

1. **Documentation Map**: Where all documentation lives in this project
2. **Discrepancy List**: Specific mismatches between docs and code (with file paths and line references)
3. **Synchronization Plan**: Prioritized list of documentation updates needed

## Constraints

- You CAN edit documentation files (markdown, text, comments)
- You CANNOT edit application code, tests, or configuration files
- You CANNOT edit `.claude/commands/` or `.claude/hooks/` (document issues only)
- ASK before creating new documentation files

## Argument

If an argument is provided, focus the audit on that area (e.g., "API", "configuration", "hooks") but still discover documentation project-wide first.
