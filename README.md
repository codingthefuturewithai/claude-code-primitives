# Claude Code Primitives

A monorepo for collecting, organizing, and sharing Claude Code primitives across projects.

## Repository Structure

```
claude-code-primitives/
├── primitives/              # Shared primitives (single source of truth)
│   ├── commands/           # Slash commands
│   ├── skills/             # Auto-activated skills
│   ├── agents/             # Subagents
│   └── hooks/              # Event-triggered automation
│
├── plugins/                # Bundled collections (use symlinks to primitives/)
│   └── [plugin-name]/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── commands/       # Symlinks to ../../primitives/commands/
│
└── external/               # External projects and references
    ├── anthropic-skills/   # Anthropic's official skills (cloned)
    └── rag-memory/         # RAG Memory MCP server
```

## How It Works

### Primitives Directory
All primitives live in `primitives/` as the single source of truth. Organize by type:
- `commands/` - Slash commands (user-invoked)
- `skills/` - Skills (auto-activated)
- `agents/` - Subagents (isolated execution)
- `hooks/` - Hooks (event-triggered)

### Plugin Bundling via Symlinks
Plugins bundle primitives using symlinks (not duplication):

```bash
# Create a plugin that includes shared primitives
cd plugins/my-plugin
mkdir commands
ln -s ../../primitives/commands/devflow commands/devflow
```

Benefits:
- Single source of truth in `primitives/`
- Update once, changes propagate everywhere
- Git tracks symlinks natively
- No file duplication

## Current Primitives

### Commands

| Category | Commands | Description |
|----------|----------|-------------|
| `devflow/` | 8 commands | JIRA-integrated development workflow |
| `pm/` | 2 commands | Product management (roadmap, backlog) |
| `docs/` | 1 command | Documentation tools |
| `features/` | 2 commands | Feature setup utilities |

### Skills

| Skill | Description |
|-------|-------------|
| `knowledge-management/` | RAG Memory and Confluence integration |

## Installation

### Use Primitives Directly

Copy primitives to your Claude Code directory:

```bash
# Install a command category
cp -r primitives/commands/devflow ~/.claude/commands/

# Install a skill
cp -r primitives/skills/knowledge-management ~/.claude/skills/
```

### Use as Plugin Source

Symlink this repo as a plugin marketplace:

```bash
claude plugin marketplace add ~/projects/claude-code-primitives/plugins
```

## Creating Plugins

1. Create plugin directory:
```bash
mkdir -p plugins/my-plugin/.claude-plugin
```

2. Add plugin manifest:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My plugin description"
}
```

3. Symlink primitives:
```bash
cd plugins/my-plugin
ln -s ../../primitives/commands/devflow commands/devflow
ln -s ../../primitives/skills/knowledge-management skills/knowledge-management
```

## Windows Setup

Windows requires Git configuration for symlinks:

```bash
# One-time setup
git config --global core.symlinks true

# Enable Developer Mode in Windows Settings
# Then clone normally
git clone <repo-url>
```

## Contributing

### Adding Primitives
1. Add to appropriate `primitives/` subdirectory
2. Follow Claude Code naming conventions
3. Update this README if adding new categories

### Creating Plugins
1. Create plugin in `plugins/`
2. Use symlinks to reference `primitives/`
3. Add `.claude-plugin/plugin.json` manifest

## License

MIT
