# Claude Code Primitives

A monorepo for creating, sharing, and maintaining Claude Code primitives and plugins.

## Overview

This repository provides a complete toolkit for working with Claude Code primitives:
- **Slash Commands** - User-invoked commands (e.g., `/create-primitive`)
- **Skills** - Auto-activated capabilities for specialized tasks
- **Subagents** - Isolated execution contexts with parallel capabilities
- **Hooks** - Event-triggered automation (e.g., pre-commit checks)
- **MCP Servers** - External service integrations
- **Plugins** - Bundled collections of primitives

## Repository Structure

```
claude-code-primitives/
├── primitives/              # Individual primitives (evolve independently)
│   ├── commands/           # Slash commands
│   ├── skills/             # Auto-activated skills
│   ├── subagents/          # Isolated execution contexts
│   ├── hooks/              # Event-triggered automation
│   ├── mcp-servers/        # External service integrations
│   └── guides/             # Reference documentation
│       └── INDEX.md        # Central navigation
│
├── plugins/                # Bundled collections (use symlinks)
│   └── primitives-toolkit/ # Comprehensive toolkit plugin
│
└── examples/               # Working examples with explanations
```

## Key Features

### 1. Independent Evolution
Primitives live in `primitives/` and evolve independently. Each primitive has its own directory with supporting files.

### 2. Plugin Bundling via Symlinks
Plugins bundle primitives using symlinks (not duplication):
- Reuse primitives across multiple plugins
- Single source of truth
- Git tracks symlinks natively
- Easy updates propagate to all plugins

### 3. Progressive Disclosure Pattern
The `/create-primitive` command uses progressive disclosure to load only needed documentation:
```
User runs /create-primitive
↓
Gather requirements
↓
Determine primitive type
↓
Load type-specific guide via Read()
↓
Load examples if needed
↓
Create primitive with complete context
```

### 4. No External Dependencies
- No RAG Memory MCP server required
- No additional setup needed
- Works immediately after installation
- Self-contained documentation

## Installation

### Install Plugin Locally

```bash
# Clone the repository
git clone <repo-url> ~/projects/claude-code-primitives

# Symlink the plugin to Claude Code
cd ~/.claude/plugins
ln -s ~/projects/claude-code-primitives/plugins/primitives-toolkit primitives-toolkit
```

### Install Specific Primitives

Copy individual primitives from `primitives/` to your Claude Code directory:

```bash
# Install a slash command
cp -r primitives/commands/create-primitive ~/.claude/commands/

# Install a skill
cp -r primitives/skills/security-reviewer ~/.claude/skills/

# Install a subagent
cp -r primitives/subagents/code-reviewer ~/.claude/agents/
```

## Usage

### Creating New Primitives

Use the `/create-primitive` command (included in primitives-toolkit plugin):

```
/create-primitive
```

This will guide you through:
1. Understanding your requirements
2. Determining the right primitive type
3. Loading relevant best practices
4. Creating the primitive with proper format

### Exploring Documentation

All guides are organized in `primitives/guides/`:
- `INDEX.md` - Central navigation
- `skills/` - Skills documentation and best practices
- `slash-commands/` - Slash command guides
- `subagents/` - Subagent documentation
- `hooks/` - Hook configuration guides
- `mcp-servers/` - MCP server integration
- `plugins/` - Plugin packaging and distribution

### Using Examples

Browse `examples/` for working examples of all 6 primitive types. Each example includes:
- Complete, working code
- Explanation of best practices applied
- Common pitfalls to avoid

## Composition Rules

**Valid compositions (platform supported):**
- ✅ Slash Command → Subagent (via Task tool)
- ✅ Subagent → Skills (via skills field)
- ✅ Subagent → Slash Commands (via SlashCommand tool)
- ✅ Hook → External Script (via shell command)

**Invalid compositions (platform prevents):**
- ❌ Subagent → Subagent (infinite nesting prevention)
- ❌ Slash Command → Slash Command (no mechanism)
- ❌ Skill → Skill (no mechanism)
- ❌ Skill → Subagent (no mechanism)

## Contributing

### Adding New Primitives

1. Create primitive in appropriate `primitives/` subdirectory
2. Follow naming conventions (e.g., gerund form for skills)
3. Include supporting files in the same directory
4. Update relevant plugin if applicable

### Updating Documentation

When Claude Code releases updates:
1. Review official docs at platform.claude.com/docs
2. Update affected guide(s) in `primitives/guides/`
3. Add new examples if patterns change
4. Update `INDEX.md` if structure changes

### Creating New Plugins

1. Create plugin directory in `plugins/`
2. Create symlinks to primitives from `primitives/`
3. Add `PLUGIN.md` with metadata
4. Include installation instructions

## Symlink Management

### Creating Symlinks

```bash
cd plugins/your-plugin/
ln -s ../../primitives/commands/your-command commands/your-command
```

### Verifying Symlinks

```bash
find plugins/ -type l -ls
```

### Updating Symlinked Content

Updates to files in `primitives/` automatically appear in all plugins via symlinks. No manual propagation needed.

## Architecture Philosophy

**Why Monorepo?**
- All primitives in one place
- Easy cross-referencing
- Consistent versioning
- Simplified distribution

**Why Symlinks?**
- No duplication
- Single source of truth
- Easy updates
- Reuse across plugins

**Why No RAG Memory?**
- Simpler architecture
- No external dependencies
- Progressive disclosure via Read() sufficient
- claude-code-guide provides authoritative format

**Why Progressive Disclosure?**
- Only load what's needed
- Reduces token usage
- Faster responses
- Better user experience

## Repository Maintenance

### Keeping Docs Current

1. Monitor Claude Code releases
2. Review changelog for primitive changes
3. Update relevant guides
4. Update examples if needed
5. Test primitives with new Claude Code version

### Version Management

This repository follows semantic versioning for plugins:
- MAJOR: Breaking changes to primitive interfaces
- MINOR: New primitives or features
- PATCH: Bug fixes and documentation updates

## License

[To be determined]

## Support

For issues, questions, or contributions:
- GitHub Issues: [To be added]
- Documentation: See `primitives/guides/INDEX.md`
- Examples: See `examples/`
