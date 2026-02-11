# Plugin Architecture Reference

> Source: Claude Code official documentation + RAG Memory (docs 18, 100, 103)

## What Is a Plugin?

A plugin is a distribution package that bundles skills, agents, hooks, commands, MCP server configs, and LSP server configs into a single installable unit. Plugins are how teams share Claude Code extensions.

> **Note:** Custom slash commands have been merged into skills. Both `commands/` and `skills/` directories work, but skills are recommended since they support additional features like supporting files, frontmatter control, and auto-invocation.

## Plugin Directory Structure

> **Common mistake:** Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root level.

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json         # Plugin manifest (required)
├── commands/               # Slash commands (real files only — NO symlinks)
├── skills/                 # Skills with SKILL.md directories (recommended over commands/)
├── agents/                 # Custom subagent definitions
├── hooks/                  # hooks.json + hook scripts
├── .mcp.json               # MCP server configurations
├── .lsp.json               # LSP server configurations
└── scripts/                # Utility scripts for hooks
```

## Auto-Discovery

Claude Code automatically scans these directories at the plugin root:
- `commands/` — discovers slash command markdown files
- `skills/` — discovers SKILL.md skill directories
- `agents/` — discovers agent markdown files
- `hooks/` — discovers hooks.json

No explicit registration needed — just put files in the right directories.

## Plugin Manifest (`plugin.json`)

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief description",
  "author": {
    "name": "Author Name",
    "email": "email@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://...",
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

**Path fields** (`commands`, `agents`, `skills`, `hooks`, etc.) **supplement** the default directories — they don't replace them. If `agents/` exists at the plugin root AND `plugin.json` specifies a custom path, BOTH are loaded.

## Namespacing

All plugin components get the plugin name as a prefix:
- Skills: `/plugin-name:skill-name`
- Agents: `plugin-name:agent-name`
- Commands: `/plugin-name:domain:command-name`

This prevents conflicts when multiple plugins define components with the same name.

## Symlink Rules

| Component | Symlinks OK? | Notes |
|-----------|-------------|-------|
| Commands | **NO** | Cache scanner bug (#14929) — must be real files |
| Skills | YES | Works fine |
| Agents | YES | Works fine |
| Hooks | YES | Works fine |

**Important clarification for this repo:** Symlinks in `plugins/devflow/skills/` and `plugins/devflow/agents/` exist only to **reuse components across plugins within this repository**. Symlinks are NOT required for plugin distribution — Claude Code copies the entire plugin directory to cache during installation, resolving symlinks in the process.

## Plugin Caching

When installed, plugins are copied to `~/.claude/plugins/cache/<marketplace>/<plugin>/`. The environment variable `${CLAUDE_PLUGIN_ROOT}` resolves to this cached directory at runtime.

**Important:** Path traversal outside the plugin root doesn't work in the cache. All paths must be relative to the plugin directory.

## Marketplace Distribution

A marketplace is a Git repository with a `marketplace.json`:

```json
{
  "name": "marketplace-name",
  "description": "Marketplace description",
  "owner": { "name": "Owner", "url": "https://..." },
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "source": "./plugins/plugin-name"
    }
  ]
}
```

Users install with:
```bash
# Add marketplace (once)
/plugin marketplace add owner/repo-name

# Install plugin
/plugin install plugin-name@marketplace-name
```

## Installation Scopes

| Scope | Location | Access |
|-------|----------|--------|
| `user` | `~/.claude/settings.json` | All projects |
| `project` | `.claude/settings.json` | This project (committed) |
| `local` | `.claude/settings.local.json` | This project (gitignored) |
| `managed` | Organization policy | Organization-wide |

## CLI Commands

```bash
claude plugin install <name>@<marketplace> [--scope user|project|local]
claude plugin uninstall <name>@<marketplace>
claude plugin enable <name>@<marketplace>
claude plugin disable <name>@<marketplace>
claude plugin update <name>@<marketplace>
```

## LSP Server Configuration

Plugins can include `.lsp.json` to provide code intelligence for specific languages:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Users installing the plugin must have the language server binary installed on their machine.

> Source: https://code.claude.com/docs/en/plugins

## Local Development Testing

Use the `--plugin-dir` flag to test plugins during development without installation:

```bash
claude --plugin-dir ./my-plugin
```

Load multiple plugins: `claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two`

> Source: https://code.claude.com/docs/en/plugins

## Version Pinning

Plugins can be pinned to specific Git SHAs for reproducibility (since v2.1.14).
