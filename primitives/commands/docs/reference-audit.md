---
description: Audit documentation directories to ensure all claims match actual source code
argument-hint: "[reference|docs] (default: both)"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Edit"]
---

# Reference Audit

## Goal

Ensure documentation accurately reflects the actual codebase. Find and fix discrepancies.

## Scope

- No argument → Audit both `.reference/` and `docs/`
- `reference` → Only `.reference/`
- `docs` → Only `docs/`

## Constraints

- You CAN edit files in `.reference/` and `docs/`
- You CANNOT edit code, `.claude/commands/`, `.claude/hooks/`, or settings

## How to Execute

1. Read root README.md to understand the project structure
2. Explore the entire repository - every directory, not just the ones you expect
3. Read the documentation directories
4. Compare both directions:
   - For each documented claim: does the code actually work that way?
   - For each discovered component: is it documented?
5. Fix gaps by editing existing files or creating new ones
6. Report what you found and fixed
