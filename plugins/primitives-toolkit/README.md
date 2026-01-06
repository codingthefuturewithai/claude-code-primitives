# Primitives Toolkit Plugin

Comprehensive toolkit for creating and managing Claude Code primitives.

## What's Included

This plugin provides:

- **`/create-primitive` command** - Guided primitive creation with progressive disclosure
- **Complete guides** - Reference documentation for all 6 primitive types
- **Working examples** - Demonstrated best practices for each primitive type

## Primitives Included

### Slash Commands
- `/primitives-toolkit:create-primitive` - Create new primitives with guidance

### Guides (via symlinks)
- **Skills** - Complete guide + advanced best practices
- **Slash Commands** - Format and usage patterns
- **Subagents** - Isolated contexts and skill access
- **Hooks** - Event-triggered automation
- **MCP Servers** - External service integration
- **Plugins** - Bundling and distribution

### Examples (via symlinks)
- Slash command: `format-code`
- Skill: `security-reviewer`
- Subagent: `code-reviewer`
- Hook: `python-formatter`
- MCP Server: `simple-time-server`
- Plugin: `dev-workflow`

## Installation

### Method 1: Symlink from Monorepo (Recommended for Development)

```bash
# Clone the monorepo
git clone <repo-url> ~/projects/claude-code-primitives

# Symlink plugin to Claude Code
cd ~/.claude/plugins
ln -s ~/projects/claude-code-primitives/plugins/primitives-toolkit primitives-toolkit

# Restart Claude Code
```

### Method 2: Copy Plugin

```bash
# Copy plugin directory
cp -r plugins/primitives-toolkit ~/.claude/plugins/

# Restart Claude Code
```

## Usage

### Creating Primitives

Use the `/create-primitive` command:

```
/primitives-toolkit:create-primitive
```

This will:
1. Ask what you want to accomplish
2. Determine the right primitive type
3. Query claude-code-guide for format details
4. Load relevant guides via progressive disclosure
5. Create the primitive with correct format

### Accessing Guides

Guides are available via the `/guides/` directory:

- **Navigation**: `guides/INDEX.md` - Central guide index
- **Skills**: `guides/skills/complete-guide.md`
- **Best Practices**: `guides/skills/best-practices.md`
- **All Types**: Complete guides for all 6 primitive types

The `/create-primitive` command automatically loads relevant guides as needed.

### Studying Examples

Examples demonstrate best practices:

- `examples/commands/format-code.md`
- `examples/skills/security-reviewer.md`
- `examples/subagents/code-reviewer.md`
- `examples/hooks/python-formatter-example.md`
- `examples/mcp-servers/simple-time-server-example.md`
- `examples/plugins/dev-workflow-plugin-example.md`

## Plugin Architecture

This plugin uses **symlinks** for efficient bundling:

```
primitives-toolkit/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # → ../../primitives/commands
├── agents/                   # → ../../primitives/subagents
├── skills/                   # → ../../primitives/skills
├── guides/                   # → ../../primitives/guides
└── examples/                 # → ../../examples
```

**Benefits**:
- Single source of truth in `primitives/` directory
- Updates propagate automatically via symlinks
- No file duplication
- Easy to maintain

## Progressive Disclosure Pattern

The `/create-primitive` command demonstrates progressive disclosure:

1. User invokes command
2. Command gathers requirements
3. Determines primitive type
4. Queries claude-code-guide for authoritative format
5. Loads only relevant guide via Read()
6. Creates primitive with complete guidance

**No RAG Memory dependency** - uses built-in Read() for progressive disclosure.

## Dependencies

**Required**:
- Claude Code (with claude-code-guide subagent)

**No external dependencies**:
- No RAG Memory MCP server required
- No additional tools needed
- Self-contained documentation

## How It Works

### Command Namespacing

Commands are prefixed with plugin name:
- File: `commands/create-primitive.md`
- Invocation: `/primitives-toolkit:create-primitive`

### Symlink Resolution

When Claude Code loads the plugin:
1. Reads `.claude-plugin/plugin.json`
2. Discovers `commands/`, `agents/`, `skills/` directories
3. Follows symlinks to actual primitive files
4. Loads primitives as if they were in the plugin directory

Git tracks symlinks natively - they work across systems.

## Updating

### If Installed via Symlink

```bash
cd ~/projects/claude-code-primitives
git pull origin main
# Changes automatically available via symlinks
```

### If Installed via Copy

```bash
cd ~/projects/claude-code-primitives
git pull origin main
cp -r plugins/primitives-toolkit ~/.claude/plugins/
```

## Contributing

To add new primitives to the monorepo:

1. Add to appropriate `primitives/` subdirectory
2. Update `primitives/guides/INDEX.md` if needed
3. Add example to `examples/`
4. Commit and push

Changes automatically available to plugin via symlinks.

## Distribution

This plugin can be:
- Shared via GitHub repository
- Distributed through Claude Code marketplace (future)
- Forked and customized for teams

## License

MIT

## Support

For issues or questions:
- GitHub Issues: [Repository URL]
- Documentation: See `guides/INDEX.md`
