# Claude Code Primitives - Project Guide

## Project Structure

```
claude-code-primitives/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace metadata (VERSION HERE)
├── plugins/
│   └── primitives-toolkit/
│       ├── .claude-plugin/
│       │   └── plugin.json   # Plugin metadata (VERSION HERE - must match marketplace.json)
│       ├── commands/         # Slash commands for the plugin
│       ├── skills/           # Skills for the plugin
│       └── hooks/            # Hooks for the plugin
├── commands/                 # Standalone commands (can be reused across plugins)
├── skills/                   # Standalone skills (can be reused across plugins)
└── hooks/                    # Standalone hooks
```

## Version Files - BOTH Must Be Updated

When releasing a new version, update BOTH files with the same version number:

1. **`.claude-plugin/marketplace.json`** - Line with `"version": "X.Y.Z"` inside the plugins array
2. **`plugins/primitives-toolkit/.claude-plugin/plugin.json`** - Line with `"version": "X.Y.Z"`

These MUST match or the plugin will not work correctly.

## After Implementing a New Feature

1. Update version in both files listed above
2. Commit with message like: `chore: Bump plugin version to X.Y.Z for [feature name]`

## Testing Changes to Skills/Commands

After bumping versions and pushing changes:

1. **From command line, update the plugin:**
   ```bash
   claude plugin update primitives-toolkit@claude-code-primitives
   ```

2. **Then start Claude Code and install:**
   ```bash
   claude
   # Then run:
   /plugin install primitives-toolkit@claude-code-primitives
   ```

3. **Setup skills (required for skills to work):**
   ```
   /primitives-toolkit:admin:setup-skills
   ```
   This creates symlinks in `~/.claude/skills/` for the plugin's skills.

4. **Verify installation:**
   - Run a slash command like `/devflow:workflow-guide`
   - Check that your changes are reflected

### If you need a clean reinstall:

```bash
# Remove all plugin traces
rm -rf ~/.claude/plugins/cache/claude-code-primitives
rm -rf ~/.claude/plugins/marketplaces/claude-code-primitives

# Remove entries from JSON files (edit these manually):
# ~/.claude/plugins/installed_plugins.json - remove "primitives-toolkit@claude-code-primitives" entry
# ~/.claude/plugins/known_marketplaces.json - remove "claude-code-primitives" entry
```

Then start a new Claude Code session and:

```
/plugin marketplace add codingthefuturewithai/claude-code-primitives
/plugin install primitives-toolkit@claude-code-primitives
/primitives-toolkit:admin:setup-skills
```

## File Organization Rules

**DO NOT change the file structure.** If files exist as copies in multiple locations (e.g., `commands/` and `plugins/primitives-toolkit/commands/`), keep them as copies. Do not convert to symlinks or change the architecture unless explicitly asked.

**Only modify the specific files mentioned in the ticket.** No structural changes, no "improvements" to organization.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `commands/` | Standalone slash commands |
| `skills/` | Standalone skills with SKILL.md and references/ |
| `plugins/primitives-toolkit/commands/` | Plugin-specific commands |
| `plugins/primitives-toolkit/skills/` | Plugin-specific skills |
| `hooks/` | Pre/post tool use hooks |
| `.devflow/plans/` | Implementation plans for JIRA issues |

## Common Slash Commands in This Plugin

- `/devflow:fetch-issue` - Fetch JIRA issue and analyze feasibility
- `/devflow:plan-work` - Create implementation plan
- `/devflow:implement-plan` - Execute approved plan
- `/devflow:complete-issue` - Create PR and close issue
- `/rag-memory:setup-collections` - Scaffold RAG Memory collections
- `/knowledge-management` - Route content to RAG Memory or Confluence
