# Claude Code Primitives

A comprehensive toolkit of reusable primitives for Claude Code that supercharges your AI-assisted development workflow. This plugin provides battle-tested commands, intelligent skills, and protective hooks that integrate seamlessly with JIRA, Confluence, and RAG Memory.

## What This Plugin Offers

### Development Workflow Automation (DevFlow)
Complete JIRA-integrated development cycle from issue creation through PR completion. Claude guides you through fetching issues, planning work, implementing code, and closing out issues with proper documentation.

### Knowledge Management
Intelligent routing of content to RAG Memory or Confluence. Claude understands your content and helps you store it in the right place with proper organization.

### Project Management
Confluence-integrated roadmap and backlog management. Review ideas, refine thoughts, and keep your product planning organized.

### Protective Hooks
Automatic approval prompts before any modifications to your knowledge bases. Prevents accidental changes to RAG Memory or Confluence.

### Frontend Design
Production-grade UI creation with distinctive aesthetics. Claude generates creative, polished interfaces that avoid generic AI patterns.

---

## Installation

### Step 1: Add the Marketplace
```
/plugin marketplace add https://github.com/codingthefuturewithai/claude-code-primitives
```

### Step 2: Install the Plugin
```
/plugin install primitives-toolkit@claude-code-primitives
```

### Step 3: Enable Skills (Required)
Due to a [known Claude Code limitation](https://github.com/anthropics/claude-code/issues/15178), plugin skills require a one-time setup:
```
/primitives-toolkit:admin:setup-skills
```

### Step 4: Start a New Session
Restart Claude Code to load the skills.

### Step 5: Verify Installation
```
/knowledge-management --rag test
```
You should see "📋 SKILL INVOKED: knowledge-management" confirming the skill is active.

---

## What's Included

### Skills (AI-Driven Workflows)

Skills are intelligent workflows that Claude invokes based on context. They provide step-by-step guidance for complex tasks.

| Skill | Trigger | Description |
|-------|---------|-------------|
| `knowledge-management` | When you want to save/store content | Routes content to RAG Memory or Confluence with intelligent organization |
| `frontend-design` | When building UI components | Creates distinctive, production-grade interfaces with bold aesthetics |
| `skill-creator` | When creating new skills | Guides you through building effective Claude Code skills |

**Usage:** Skills activate automatically when Claude detects relevant intent, or invoke directly:
```
/knowledge-management --rag "Store this API documentation"
/knowledge-management --confluence "Add to team wiki"
/frontend-design "Create a dashboard for analytics"
```

### Commands (Explicit Actions)

Commands are explicit actions you invoke directly. They're organized by domain.

#### DevFlow Commands (JIRA Integration)
Complete development workflow from issue to PR:

| Command | Description |
|---------|-------------|
| `/primitives-toolkit:devflow:fetch-issue` | Fetch JIRA issue and analyze feasibility |
| `/primitives-toolkit:devflow:create-issue` | Create JIRA issue with codebase analysis |
| `/primitives-toolkit:devflow:plan-work` | Analyze issue and develop implementation plan |
| `/primitives-toolkit:devflow:implement-plan` | Execute approved implementation plan |
| `/primitives-toolkit:devflow:complete-issue` | Final validation, create PR, mark JIRA done |
| `/primitives-toolkit:devflow:post-merge` | Sync with remote after PR merge |
| `/primitives-toolkit:devflow:security-review` | Security analysis of changes |
| `/primitives-toolkit:devflow:workflow-guide` | Overview of the DevFlow workflow |

#### PM Commands (Confluence Integration)
| Command | Description |
|---------|-------------|
| `/primitives-toolkit:pm:roadmap` | Manage product roadmap in Confluence |
| `/primitives-toolkit:pm:backlog` | Manage product backlog in Confluence |

#### RAG Memory Commands
| Command | Description |
|---------|-------------|
| `/primitives-toolkit:rag-memory:setup-collections` | Interactive wizard to scaffold RAG Memory collections |
| `/primitives-toolkit:rag-memory:create-agent-preferences` | Create agent-preferences collection for AI routing |

#### Documentation Commands
| Command | Description |
|---------|-------------|
| `/primitives-toolkit:docs:reference-audit` | Audit and sync documentation with codebase |

#### Admin Commands
| Command | Description |
|---------|-------------|
| `/primitives-toolkit:admin:setup-skills` | One-time setup to enable plugin skills |

### Hooks (Automatic Protection)

Hooks run automatically before certain actions to protect your data.

| Hook | Trigger | Action |
|------|---------|--------|
| `kb-modification-approval` | Before any RAG Memory or Confluence write operation | Prompts for confirmation before modifying knowledge bases |

**Protected Operations:**
- RAG Memory: create/delete collections, ingest content, update/delete documents
- Confluence: create/update pages, add comments
- JIRA: create/edit issues, add comments, transition status

---

## How It All Fits Together

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRIMITIVES TOOLKIT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SKILLS (Intelligent Workflows)                                 │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │ knowledge-      │ │ frontend-       │ │ skill-          │   │
│  │ management      │ │ design          │ │ creator         │   │
│  │                 │ │                 │ │                 │   │
│  │ Routes content  │ │ Creates bold,   │ │ Guides skill    │   │
│  │ to RAG Memory   │ │ distinctive UI  │ │ development     │   │
│  │ or Confluence   │ │ components      │ │                 │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
│  COMMANDS (Explicit Actions)                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │ devflow/*   │ │ pm/*        │ │ rag-memory/*│ │ docs/*    │ │
│  │             │ │             │ │             │ │           │ │
│  │ JIRA-driven │ │ Confluence  │ │ Collection  │ │ Doc audit │ │
│  │ dev cycle   │ │ roadmap &   │ │ setup &     │ │ & sync    │ │
│  │             │ │ backlog     │ │ preferences │ │           │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│                                                                 │
│  HOOKS (Automatic Protection)                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ kb-modification-approval                                 │   │
│  │ Confirms before any write to RAG Memory or Confluence    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Skills vs Commands

| Aspect | Skills | Commands |
|--------|--------|----------|
| **Invocation** | Automatic (context-aware) or explicit | Always explicit |
| **Purpose** | Complex, multi-step workflows | Specific, bounded actions |
| **Guidance** | Claude follows detailed instructions | Claude executes defined steps |
| **Example** | "Store this in my knowledge base" triggers `knowledge-management` | `/devflow:fetch-issue ABC-123` fetches specific issue |

---

## Requirements

### MCP Servers
Some features require MCP servers to be configured:

| Feature | Required MCP Server |
|---------|---------------------|
| DevFlow commands | `atlassian` (JIRA) |
| PM commands | `atlassian` (Confluence) |
| Knowledge management | `rag-memory` and/or `atlassian` |
| RAG Memory commands | `rag-memory` |

### Permissions
The plugin will prompt for tool permissions on first use. You can pre-approve them in your Claude Code settings.

---

## Repository Structure

```
claude-code-primitives/
├── .claude-plugin/
│   └── marketplace.json          # Plugin marketplace definition
├── plugins/
│   └── primitives-toolkit/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── commands/
│       │   ├── admin/            # Administrative commands
│       │   │   └── setup-skills.md
│       │   ├── devflow/          # JIRA workflow commands
│       │   │   ├── fetch-issue.md
│       │   │   ├── create-issue.md
│       │   │   ├── plan-work.md
│       │   │   ├── implement-plan.md
│       │   │   ├── complete-issue.md
│       │   │   ├── post-merge.md
│       │   │   ├── security-review.md
│       │   │   └── workflow-guide.md
│       │   ├── docs/             # Documentation commands
│       │   │   └── reference-audit.md
│       │   ├── pm/               # Project management commands
│       │   │   ├── roadmap.md
│       │   │   └── backlog.md
│       │   └── rag-memory/       # RAG Memory setup commands
│       │       ├── setup-collections.md
│       │       └── create-agent-preferences.md
│       ├── hooks/
│       │   ├── hooks.json        # Hook definitions
│       │   └── kb-modification-approval.py
│       ├── skills/
│       │   ├── frontend-design/
│       │   │   └── SKILL.md
│       │   ├── knowledge-management/
│       │   │   ├── SKILL.md
│       │   │   └── references/
│       │   └── skill-creator/
│       │       ├── SKILL.md
│       │       └── references/
│       └── scripts/
│           └── setup-skills.py   # Standalone setup script
└── README.md
```

---

## Troubleshooting

### Skills not appearing in autocomplete
Run the setup command:
```
/primitives-toolkit:admin:setup-skills
```
Then start a new Claude Code session.

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
