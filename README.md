# Claude Code Primitives

A comprehensive toolkit of reusable primitives for Claude Code that supercharges your AI-assisted development workflow. This plugin provides battle-tested skills and protective hooks that integrate seamlessly with Jira, GitLab, Confluence, Google Docs, and RAG Memory.

## What This Plugin Offers

### Development Workflow Automation (DevFlow)
Complete issue-integrated development cycle from issue creation through PR/MR completion. Claude guides you through fetching issues, planning work, implementing code, and closing out issues with proper documentation.

### Knowledge Management
Intelligent routing of content to RAG Memory or your docs backend (Confluence/Google Docs). Claude understands your content and helps you store it in the right place with proper organization.

### Project Management
Confluence-integrated roadmap and backlog management. Review ideas, refine thoughts, and keep your product planning organized.

### Protective Hooks
Automatic approval prompts before any modifications to external systems. Prevents accidental changes to Jira, GitLab, Confluence, Google Docs, and RAG Memory.

---

## Installation

### Step 1: Add the Marketplace
```
/plugin marketplace add codingthefuturewithai/claude-code-primitives
```

### Step 2: Install the Plugin
```
/plugin install devflow@claude-code-primitives
```

### Step 3: Configure Backends (Optional)
```
/devflow-setup
```
This wizard configures your issue tracking (Jira/GitLab/GitHub), documentation (Confluence/Google Docs), and VCS backends.

### Step 4: Verify Installation
```
/devflow:build:workflow-guide
```
You should see the workflow guide, confirming the plugin is active.

---

## What's Included

### Skills (AI-Driven Workflows)

Skills are intelligent workflows that Claude invokes based on context or explicit `/command` invocation.

| Skill | Description |
|-------|-------------|
| `/devflow-setup` | Configure backends for issue tracking, docs, and VCS |
| `/knowledge-management` | Routes content to RAG Memory or docs backend |
| `/repo-explorer` | Explores and analyzes GitHub repository structure |
| `/devflow:build:fetch-issue` | Fetch issue and analyze feasibility |
| `/devflow:build:plan-work` | Analyze issue and develop implementation plan |
| `/devflow:build:implement-plan` | Execute approved implementation plan |
| `/devflow:build:create-issue` | Create issue with codebase analysis |
| `/devflow:build:complete-issue` | Final validation, create PR/MR, mark issue done |
| `/devflow:build:post-merge` | Sync with remote after PR/MR merge |
| `/devflow:build:security-review` | Security analysis of changes |
| `/devflow:build:workflow-guide` | DevFlow workflow overview |
| `/devflow:pm:roadmap` | Manage Confluence product roadmap |
| `/devflow:pm:backlog` | Manage Jira backlog from Confluence roadmap |
| `/devflow:docs:documentation-audit` | Audit and sync documentation with codebase |
| `/devflow:docs:reference-audit` | Discover and synchronize project documentation |
| `/devflow:rag-memory:setup-collections` | Interactive wizard to scaffold RAG Memory collections |
| `/devflow:rag-memory:create-agent-preferences` | Create agent-preferences collection |
| `/devflow:devops:sync-claude-knowledge` | Sync Claude Code changelog to knowledge base |
| `/devflow:commands-guide` | Discover all available slash commands |

### Hooks (Automatic Protection)

Hooks run automatically before certain actions to protect your data. Each skill includes appropriate hooks for the tools it uses.

**Protected Operations:**
- RAG Memory: create/delete collections, ingest content, update/delete documents
- Confluence: create/update pages, add comments
- Jira: create/edit issues, add comments, transition status
- GitLab: create/update issues, create MRs, add notes
- Google Workspace: create/modify docs, create/update/share files

---

## Supported Backends

| Component | Options |
|-----------|---------|
| Issues | Jira (Atlassian MCP), GitLab (GitLab MCP), GitHub (gh CLI) |
| Documentation | Confluence (Atlassian MCP), Google Docs (Google Workspace MCP) |
| Knowledge Base | RAG Memory MCP |
| VCS | GitHub (gh CLI), GitLab (GitLab MCP) |

---

## Requirements

### MCP Servers
Some features require MCP servers to be configured:

| Feature | Required MCP Server |
|---------|---------------------|
| Jira integration | `atlassian` |
| Confluence integration | `atlassian` |
| GitLab integration | `gitlab` |
| Google Docs integration | `google-workspace` |
| Knowledge management | `rag-memory` |
| Repo Explorer | `code-understanding` |

### Permissions
The plugin will prompt for tool permissions on first use. Hooks provide approval prompts before external system modifications.

---

## Troubleshooting

### "MCP server not available" errors
Ensure the required MCP servers are configured. Check with:
```
/mcp
```

### Hook not triggering
Verify hooks are loaded:
```
/hooks
```
You should see `PreToolUse` hooks from the plugin.

---

## Contributing

Contributions welcome! This plugin is part of the [Coding the Future with AI](https://github.com/codingthefuturewithai) project.

## License

MIT License - see individual skill files for specific licensing.
