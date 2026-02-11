# Claude Code Primitives Reference

This directory contains comprehensive reference documentation for every Claude Code primitive type. Use this to understand what each primitive does, how to write them, and how they connect.

## Quick Reference: Which Primitive Do I Need?

| I need to... | Use this primitive | Reference |
|--------------|-------------------|-----------|
| Create a user-invocable workflow | **Skill (action)** | [skills.md](skills.md) |
| Provide background knowledge Claude auto-applies | **Skill (reference)** | [skills.md](skills.md) |
| Isolate heavy work (search, analysis, comparison) | **Custom subagent** | [subagents.md](subagents.md) |
| Guarantee something happens (approval gate, validation) | **Hook** | [hooks.md](hooks.md) |
| Connect to an external service (Jira, Confluence, etc.) | **MCP Server** | (configured in `.mcp.json`) |
| Distribute skills + agents + hooks as a package | **Plugin** | [plugin-architecture.md](plugin-architecture.md) |
| Coordinate multiple Claude sessions working in parallel | **Agent Team** | [agent-teams.md](agent-teams.md) |
| Understand how primitives connect and interact | — | [how-they-relate.md](how-they-relate.md) |

## Documents in This Directory

### [skills.md](skills.md)
SKILL.md file format, every frontmatter field (`name`, `description`, `allowed-tools`, `context`, `agent`, `hooks`, etc.), string substitutions (`$ARGUMENTS`, `$N` shorthand), dynamic content injection, action vs reference skills, commands/skills merge, nested directory discovery, extended thinking (`ultrathink`), visual output patterns, skill permission control, execution model, and best practices.

### [subagents.md](subagents.md)
Custom agent file format, every frontmatter field (`name`, `description`, `tools`, `model`, `skills`, `mcpServers`, `hooks`, `memory`, etc.), built-in agents (Explore with thoroughness levels, Plan, general-purpose, claude-code-guide, statusline-setup), CLI-defined subagents (`--agents` flag), `/agents` management interface, how agents are invoked and auto-discovered, restricting/disabling subagents, transcript persistence, foreground vs background execution, priority order, key behavioral constraints, and best practices.

### [hooks.md](hooks.md)
All 14 hook events (`PreToolUse`, `PostToolUse`, `SubagentStart`, `Stop`, `SessionStart`, `TeammateIdle`, `TaskCompleted`, etc.), the 3 hook types (`command`, `prompt`, `agent`), configuration format, matcher patterns per event, PreToolUse decision control (`hookSpecificOutput`, `permissionDecision`, `updatedInput`), PermissionRequest decision control, exit code 2 blocking behavior table, `CLAUDE_ENV_FILE` for SessionStart, where hooks can be defined (settings, frontmatter, plugins), and common patterns.

### [plugin-architecture.md](plugin-architecture.md)
Plugin directory structure (with common mistake warning), auto-discovery of `commands/`, `skills/`, `agents/`, `hooks/`, the `plugin.json` manifest, commands/skills merge, namespacing rules, symlink rules, caching behavior, `${CLAUDE_PLUGIN_ROOT}`, LSP server configuration, `--plugin-dir` for local testing, marketplace distribution, installation scopes, and version pinning.

### [agent-teams.md](agent-teams.md)
Experimental multi-session collaboration. Architecture (team lead, teammates, shared task list, mailbox), when to use teams vs subagents, display modes (in-process, split panes), coordination primitives, quality gate hooks (`TeammateIdle`, `TaskCompleted`), delegate mode, permissions, limitations, and cleanup.

### [how-they-relate.md](how-they-relate.md)
The three patterns connecting skills and subagents (fork, preload, delegation), how skills and hooks relate, commands/skills merge, how plugins bundle everything, priority/precedence across all primitives, the task management system, context cost awareness, and a decision framework for choosing the right primitive.
