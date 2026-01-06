# Claude Code Primitives - Guide Index

Central navigation for all Claude Code primitive documentation.

## Overview

This index provides quick access to complete guides for all 6 primitive types. Each guide includes format specifications, best practices, anti-patterns, and working examples.

## Quick Reference

| Primitive Type | Use Case | Guide Location |
|----------------|----------|----------------|
| **Skills** | Auto-activated capabilities | [skills/](#skills) |
| **Slash Commands** | User-invoked commands | [commands/](#slash-commands) |
| **Subagents** | Isolated execution contexts | [subagents/](#subagents) |
| **Hooks** | Event-triggered automation | [hooks/](#hooks) |
| **MCP Servers** | External service integrations | [mcp-servers/](#mcp-servers) |
| **Plugins** | Bundled primitive collections | [plugins/](#plugins) |

## Skills

**Location**: `primitives/guides/skills/`

Skills are auto-activated capabilities that Claude uses when appropriate. They support progressive disclosure for complex tasks.

### Available Guides:
- **[skills-complete-guide.md](skills/skills-complete-guide.md)** - Complete reference for creating skills
  - YAML frontmatter format
  - File structure and organization
  - Anti-patterns to avoid
  - Testing and validation
  - Progressive disclosure patterns

- **[skills-best-practices-advanced.md](skills/skills-best-practices-advanced.md)** - Advanced best practices
  - **CRITICAL**: 11 essential requirements (third-person descriptions, gerund naming, etc.)
  - Core principles (conciseness, degrees of freedom, context window as public good)
  - Evaluation-driven development
  - Claude A/B iterative pattern
  - Advanced executable code patterns
  - Workflow and feedback loop patterns

### Critical Requirements Checklist:
- [ ] Description in THIRD PERSON (not "I" or "you")
- [ ] Name uses gerund form (processing-pdfs, not helper)
- [ ] SKILL.md under 500 lines (split to supporting files if needed)
- [ ] Progressive disclosure strategy defined
- [ ] Appropriate degrees of freedom
- [ ] Checklist pattern for complex workflows
- [ ] Feedback loops for quality-critical tasks

## Slash Commands

**Location**: `primitives/guides/commands/`

Slash commands are user-invoked commands (e.g., `/create-primitive`). They provide explicit control over Claude's actions.

### Available Guides:
- **[slash-commands-complete-guide.md](commands/slash-commands-complete-guide.md)** - Complete reference
  - When to use vs Skills/Subagents
  - YAML frontmatter format (all fields)
  - Argument handling ($ARGUMENTS, $1, $2)
  - Tool restriction patterns
  - Advanced features (bash execution, file references)
  - Namespacing strategies
  - Project vs personal scope decisions
  - SlashCommand tool (programmatic invocation)
  - 5 anti-patterns with explanations
  - 5 common mistakes
  - Character budget management
  - Plugin & MCP command patterns
  - Testing guidance

### When to Use:
- User wants explicit control
- Simple, focused operations
- Single-step or linear workflows
- No need for auto-activation
- Repeated prompts used frequently

## Subagents

**Location**: `primitives/guides/subagents/`

Subagents are isolated execution contexts that can run in parallel and have access to specific skills.

### Available Guides:
- **[subagents-complete-guide.md](subagents/subagents-complete-guide.md)** - Complete reference
  - YAML frontmatter format
  - Skill access configuration
  - Tool restrictions
  - Parallel execution patterns
  - Model preferences

### When to Use:
- Need parallel execution
- Isolated context required
- Complex multi-step workflows
- Access to specific skills

## Hooks

**Location**: `primitives/guides/hooks/`

Hooks are event-triggered automation that runs before or after specific tool calls.

### Available Guides:
- **[hooks-complete-guide.md](hooks/hooks-complete-guide.md)** - Complete reference
  - Configuration in settings.json
  - Event types (PreToolUse, PostToolUse)
  - Tool matchers
  - Shell command execution
  - Global vs project scope

### When to Use:
- Automatic enforcement (e.g., formatting)
- Pre-commit checks
- Post-action cleanup
- Audit logging

## MCP Servers

**Location**: `primitives/guides/mcp-servers/`

MCP (Model Context Protocol) servers provide integrations with external services and APIs.

### Available Guides:
- **[mcp-servers-complete-guide.md](mcp-servers/mcp-servers-complete-guide.md)** - Complete reference
  - Server implementation
  - Tool definitions
  - Authentication
  - Resource providers
  - Configuration

### When to Use:
- External service integration
- Custom APIs
- Database access
- File system access

## Plugins

**Location**: `primitives/guides/plugins/`

Plugins are bundled collections of primitives that can be shared and distributed.

### Available Guides:
- **[plugins-complete-guide.md](plugins/plugins-complete-guide.md)** - Complete reference
  - Plugin structure
  - PLUGIN.md metadata
  - Bundling strategies
  - Versioning
  - Distribution
  - Private vs public plugins

### When to Use:
- Sharing multiple related primitives
- Team workflows
- Marketplace distribution
- Reusable collections

## Composition Rules

Understanding how primitives can be composed is critical for building effective workflows.

### Valid Compositions (Platform Supported):
- ✅ **Slash Command → Subagent** (via Task tool)
  - Example: `/analyze-codebase` → launches code-analyzer subagent
- ✅ **Subagent → Skills** (via skills field)
  - Example: code-reviewer subagent → uses security-reviewer skill
- ✅ **Subagent → Slash Commands** (via SlashCommand tool)
  - Example: deployment subagent → calls `/format-code` command
- ✅ **Hook → External Script** (via shell command)
  - Example: PostToolUse hook → runs formatter script

### Invalid Compositions (Platform Prevents):
- ❌ **Subagent → Subagent** (infinite nesting prevention)
- ❌ **Slash Command → Slash Command** (no mechanism)
- ❌ **Skill → Skill** (no mechanism)
- ❌ **Skill → Subagent** (no mechanism)

## Progressive Disclosure Pattern

Progressive disclosure is a pattern for loading only the content needed for the current task. It's used by the `/create-primitive` command and can be applied to any primitive.

### How It Works:
1. User invokes primitive
2. Primitive determines what information is needed
3. Uses Read() to load specific guides/examples
4. Presents only relevant content to user
5. Optionally loads additional details if needed

### Example from `/create-primitive`:
```
User runs /create-primitive
↓
Determine primitive type (e.g., "skill")
↓
Read("primitives/guides/INDEX.md")
↓
Read("primitives/guides/skills/complete-guide.md")
↓
Read("primitives/guides/skills/best-practices.md")
↓
If needed: Read("examples/skills/security-reviewer.md")
↓
Create primitive with complete guidance
```

### Benefits:
- Reduces token usage
- Faster responses
- Only loads relevant information
- User sees focused guidance

## Finding Information

### By Primitive Type:
Navigate directly to the type-specific directory above.

### By Topic:
- **Format/Syntax**: Check complete-guide.md for primitive type
- **Best Practices**: Check best-practices.md (if available) or complete-guide.md
- **Examples**: Check `examples/[type]/` directory (to be created)
- **Composition**: See "Composition Rules" section above
- **When to Use**: See "When to Use" sections for each type

### By Use Case:
- **Auto-activation**: Use Skills
- **User control**: Use Slash Commands
- **Parallel execution**: Use Subagents
- **Automatic enforcement**: Use Hooks
- **External integration**: Use MCP Servers
- **Sharing/bundling**: Use Plugins

## Examples

**Location**: `examples/` (at repository root)

Working examples for all 6 primitive types with explanations.

### Available Examples:
- **skills/** - *(To be created)*
  - security-reviewer - Security analysis skill
  - test-generator - Test generation skill

- **commands/** - *(To be created)*
  - create-primitive - Primitive creation command
  - format-code - Code formatting command

- **subagents/** - *(To be created)*
  - code-reviewer - Code review subagent
  - test-runner - Test execution subagent

- **hooks/** - *(To be created)*
  - python-formatter - Python formatting hook
  - pre-commit-check - Pre-commit validation hook

- **mcp-servers/** - *(To be created)*
  - github-integration - GitHub API integration

- **plugins/** - *(To be created)*
  - workflow-bundle - Example plugin bundle

## Keeping Guides Updated

When Claude Code releases updates:

1. Review official docs at platform.claude.com/docs
2. Update affected guide(s) in this directory
3. Add new examples if patterns change
4. Update this INDEX.md if structure changes
5. Test primitives with new Claude Code version

## Getting Help

If you can't find what you need:

1. Check the complete guide for your primitive type
2. Search for relevant examples
3. Review the Composition Rules section
4. Consult the official Claude Code documentation
5. Use `/create-primitive` for guided creation

## Contributing

To add or update guides:

1. Place guide in appropriate subdirectory
2. Update this INDEX.md with new content
3. Follow existing naming conventions
4. Include examples and anti-patterns
5. Test with actual primitive creation
