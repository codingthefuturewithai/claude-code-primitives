---
name: devflow:guide
description: Discover all DevFlow plugin primitives - skills, sub-agents, hooks, and commands with descriptions and usage
argument-hint: "[build|pm|docs|rag-memory|devops|hooks|agents|all]"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
---

# DevFlow Plugin Guide

**Say exactly:** "SKILL INVOKED: devflow:guide"

**Request:** $ARGUMENTS

---

## Step 1: Find the Plugin

Search for the plugin directory:

1. Use Glob with pattern `~/.claude/plugins/cache/claude-code-primitives/devflow/*/skills/*/SKILL.md`
2. If no results, try `plugins/devflow/skills/*/SKILL.md` (source repo)

The plugin contains these primitive types:
- **Skills** - Workflows invoked with `/name`
- **Sub-agents** - Skills that run in isolated context (`context: fork`)
- **Hooks** - Approval scripts that run before tool calls
- **Commands** - Traditional slash commands (if any exist)

---

## Step 2: Discover Skills and Sub-agents

For each SKILL.md found:

1. Read the first 20 lines to extract YAML frontmatter
2. Parse these fields:
   - `name:` - The slash command
   - `description:` - What it does
   - `context:` - If "fork", this is a sub-agent
   - `agent:` - The agent type (Explore, Plan, etc.)
   - `disable-model-invocation:` - If true, user-only invocation

3. Categorize by directory name prefix:
   - `build-*` → Build (development workflow)
   - `pm-*` → PM (project management)
   - `docs-*` → Docs (documentation)
   - `rag-memory-*` → RAG Memory (knowledge base)
   - `devops-*` → DevOps
   - Others → Core (setup, utilities)

4. Flag skills with `context: fork` as **Sub-agents**

---

## Step 3: Discover Hooks

Use Glob to find hook scripts:
- Pattern: `~/.claude/plugins/cache/claude-code-primitives/devflow/*/hooks/*.py`
- Or: `plugins/devflow/hooks/*.py`

For each `.py` file found, note its purpose:
- `atlassian-approval.py` → Protects Jira and Confluence
- `gitlab-approval.py` → Protects GitLab issues and MRs
- `google-workspace-approval.py` → Protects Google Docs/Drive
- `rag-memory-approval.py` → Protects RAG Memory

---

## Step 4: Discover Commands (if any)

Check for a commands directory:
- Pattern: `~/.claude/plugins/cache/claude-code-primitives/devflow/*/commands/*.md`
- Or: `plugins/devflow/commands/*.md`

If found, read frontmatter from each. If none exist, note "No traditional commands - plugin uses skills."

---

## Step 5: Filter by Argument

| Argument | Show |
|----------|------|
| (empty) or "all" | Everything |
| "build" | Build category skills |
| "pm" | PM category skills |
| "docs" | Docs category skills |
| "rag-memory" | RAG Memory skills |
| "devops" | DevOps skills |
| "hooks" | Only hooks |
| "agents" | Only sub-agents (context: fork) |

---

## Step 6: Present Results

### Skills

For each category with skills:

**[Category] Skills ([count])**

| Skill | Description |
|-------|-------------|
| `/[name]` | [description] |

### Sub-agents

Skills that run in isolated context:

| Sub-agent | Agent Type | Description |
|-----------|------------|-------------|
| `/[name]` | [agent type] | [description] |

### Hooks

| Hook | Protects |
|------|----------|
| [filename] | [systems protected] |

### Commands

If any traditional commands exist, list them. Otherwise: "No traditional commands."

---

## Step 7: Summary

**Total:** [X] skills ([Y] sub-agents), [Z] hooks

**Primitives overview:**
- Skills: Workflows you invoke with `/name`
- Sub-agents: Skills that run in isolated context for exploration/planning
- Hooks: Approval prompts before modifying external systems

**Quick start:**
- `/devflow-setup` - Configure backends
- `/devflow:build:workflow-guide` - Development workflow overview
- `/devflow:build:fetch-issue [KEY]` - Start working on an issue
