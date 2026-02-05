---
name: devflow:guide
description: Discover all DevFlow plugin primitives - skills, sub-agents, hooks, and commands with descriptions and usage
argument-hint: "[build|pm|docs|rag-memory|devops|hooks|agents|all]"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# DevFlow Plugin Guide

**Say exactly:** "SKILL INVOKED: devflow:guide"

**Request:** $ARGUMENTS

---

## Step 1: Run Discovery Script

Execute the discovery script to find all plugin primitives:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/devflow-guide/scripts/discover.py"
```

The script outputs JSON containing:
- `skills` - All skills with name, description, category, and sub-agent status
- `hooks` - All hook scripts and what they protect
- `commands` - Traditional commands (if any)
- `by_category` - Skills grouped by category
- `summary` - Counts of each primitive type

---

## Step 2: Filter by Argument

Based on $ARGUMENTS, filter the results:

| Argument | Action |
|----------|--------|
| (empty) or "all" | Show everything |
| "build" | Show only `by_category.build` skills |
| "pm" | Show only `by_category.pm` skills |
| "docs" | Show only `by_category.docs` skills |
| "rag-memory" | Show only `by_category.rag-memory` skills |
| "devops" | Show only `by_category.devops` skills |
| "core" | Show only `by_category.core` skills |
| "hooks" | Show only hooks |
| "agents" | Show only skills where `is_subagent` is true |

---

## Step 3: Present Results

Format the JSON output as readable markdown tables:

### For Skills (by category):

**[Category] Skills ([count])**

| Skill | Description |
|-------|-------------|
| `/[name]` | [description] |

### For Sub-agents:

**Sub-agents ([count])**

Skills that run in isolated context:

| Sub-agent | Agent Type | Description |
|-----------|------------|-------------|
| `/[name]` | [agent_type] | [description] |

### For Hooks:

**Hooks ([count] active)**

| Hook | Protects |
|------|----------|
| [name] | [protects] |

---

## Step 4: Summary

End with:

**Total:** [summary.total_skills] skills ([summary.subagents] sub-agents), [summary.hooks] hooks

**Quick start:**
- `/devflow-setup` - Configure your backends
- `/devflow:build:workflow-guide` - Learn the development workflow
- `/devflow:build:fetch-issue [KEY]` - Start working on an issue
