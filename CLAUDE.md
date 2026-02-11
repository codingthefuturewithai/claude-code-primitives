# Claude Code Primitives - Project Guide

## Project Structure

```
claude-code-primitives/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace metadata (VERSION HERE)
├── plugins/
│   └── devflow/
│       ├── .claude-plugin/
│       │   └── plugin.json   # Plugin metadata (VERSION HERE - must match marketplace.json)
│       ├── adapters/         # Backend adapter reference files
│       │   ├── issues/       # Jira, GitLab, Local issue adapters
│       │   ├── docs/         # Confluence, Google Drive, Local doc adapters
│       │   ├── vcs/          # GitHub, GitLab VCS adapters
│       │   └── setup/        # MCP server setup instructions
│       ├── commands/         # Slash commands for the plugin
│       │   ├── admin/        # Setup and configuration commands
│       │   ├── build/        # SDLC workflow commands (fetch, plan, implement, complete)
│       │   ├── pm/           # Project management commands
│       │   ├── rag-memory/   # RAG Memory setup commands
│       │   ├── docs/         # Documentation audit commands
│       │   └── devops/       # DevOps commands
│       ├── skills/           # Symlinks to standalone skills
│       ├── agents/           # Symlinks to standalone agents
│       └── hooks/            # Hooks for the plugin
├── commands/                 # Standalone commands (can be reused across plugins)
├── skills/                   # Standalone skills with SKILL.md and references/
├── agents/                   # Standalone custom subagents
├── hooks/                    # Standalone hooks
└── docs/                     # Reference documentation
    └── primitives/           # Claude Code primitives reference (skills, agents, hooks, plugins)
```

## Version Files - BOTH Must Be Updated

When releasing a new version, update BOTH files with the same version number:

1. **`.claude-plugin/marketplace.json`** - Line with `"version": "X.Y.Z"` inside the plugins array
2. **`plugins/devflow/.claude-plugin/plugin.json`** - Line with `"version": "X.Y.Z"`

These MUST match or the plugin will not work correctly.

## After Implementing a New Feature

1. Update version in both files listed above
2. Commit with message like: `chore: Bump plugin version to X.Y.Z for [feature name]`

## Testing Changes to Skills/Commands

After bumping versions and pushing changes:

1. **From command line, update the plugin:**
   ```bash
   claude plugin update devflow@claude-code-primitives
   ```

2. **Then start Claude Code and install:**
   ```bash
   claude
   # Then run:
   /plugin install devflow@claude-code-primitives
   ```

3. **First-time backend configuration:**
   ```
   /devflow-setup
   ```
   This wizard configures your issue tracking (Jira/GitLab), documentation (Confluence/Google Drive/RAG Memory), and VCS (GitHub/GitLab) backends.

4. **Verify installation:**
   - Run a slash command like `/devflow:build:workflow-guide`
   - Check that your changes are reflected

### If you need a clean reinstall:

```bash
# Remove all plugin traces
rm -rf ~/.claude/plugins/cache/claude-code-primitives
rm -rf ~/.claude/plugins/marketplaces/claude-code-primitives

# Remove entries from JSON files (edit these manually):
# ~/.claude/plugins/installed_plugins.json - remove "devflow@claude-code-primitives" entry
# ~/.claude/plugins/known_marketplaces.json - remove "claude-code-primitives" entry
```

Then start a new Claude Code session and:

```
/plugin marketplace add codingthefuturewithai/claude-code-primitives
/plugin install devflow@claude-code-primitives
/devflow-setup
```

## File Organization Rules

**DO NOT change the file structure.** If files exist as copies in multiple locations, keep them as copies. Do not convert to symlinks or change the architecture unless explicitly asked.

**Only modify the specific files mentioned in the ticket.** No structural changes, no "improvements" to organization.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `commands/` | Standalone slash commands |
| `skills/` | Standalone skills with SKILL.md and references/ |
| `agents/` | Standalone custom subagents (markdown files with YAML frontmatter) |
| `hooks/` | Standalone hooks |
| `docs/primitives/` | Claude Code primitives reference documentation |
| `plugins/devflow/adapters/` | Backend adapter patterns and setup instructions |
| `plugins/devflow/commands/build/` | SDLC workflow commands |
| `plugins/devflow/commands/admin/` | Setup and configuration |
| `plugins/devflow/skills/` | Symlinks to standalone skills |
| `plugins/devflow/agents/` | Symlinks to standalone agents |
| `plugins/devflow/hooks/` | Pre/post tool use hooks |
| `.devflow/plans/` | Implementation plans for issues |

## Symlinks

Symlinks in `plugins/devflow/skills/` and `plugins/devflow/agents/` exist **only to reuse standalone components across plugins within this repository**. Symlinks are NOT required for plugin distribution — Claude Code copies the entire plugin directory to cache during installation, resolving symlinks in the process.

## Claude Code Primitives

For comprehensive reference on skills, subagents, hooks, and plugin architecture, see `docs/primitives/`. Key files:

- `docs/primitives/skills.md` — SKILL.md format, frontmatter fields, execution model
- `docs/primitives/subagents.md` — Agent file format, frontmatter fields, invocation
- `docs/primitives/hooks.md` — Hook events, types, configuration
- `docs/primitives/plugin-architecture.md` — Plugin structure, distribution, namespacing
- `docs/primitives/how-they-relate.md` — How all primitives connect and when to use each

## Supported Backends

| Component | Options |
|-----------|---------|
| Issues | Jira (Atlassian MCP), GitLab (GitLab MCP) |
| Documentation | Confluence (Atlassian MCP), Google Drive (Google Drive MCP), RAG Memory |
| VCS | GitHub (gh CLI), GitLab (GitLab MCP) |

## Common Slash Commands

### Build Workflow (SDLC)
- `/devflow:build:fetch-issue` - Fetch issue and analyze feasibility
- `/devflow:build:plan-issue` - Create implementation plan
- `/devflow:build:implement-issue` - Execute approved plan
- `/devflow:build:security-review` - Security analysis
- `/devflow:build:complete-issue` - Create PR/MR and close issue
- `/devflow:build:post-merge` - Cleanup after merge
- `/devflow:build:create-issue` - Create new issue
- `/devflow:build:workflow-guide` - Workflow overview

### Admin
- `/devflow-setup` - Configure backends (Jira/GitLab, Confluence/Google Drive, GitHub/GitLab)

### RAG Memory
- `/devflow:rag-memory:setup-collections` - Scaffold RAG Memory collections
- `/devflow:rag-memory:create-agent-preferences` - Create agent preferences collection

### PM (Upstream SDLC)
- `/devflow:pm:discover` - Problem discovery and framing
- `/devflow:pm:define-prd` - Create, import, or update a PRD
- `/devflow:pm:define-architecture` - Architecture design and ADRs
- `/devflow:pm:plan-iterations` - Work decomposition and iteration planning
- `/devflow:pm:sync-artifacts` - Cross-artifact consistency check (read-only)

### Skills
- `/knowledge-management` - Route content to RAG Memory or docs backend
