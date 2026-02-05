---
name: devflow:guide
description: Discover all DevFlow plugin components - skills, hooks, and commands with descriptions and usage instructions
argument-hint: "[build|pm|docs|rag-memory|devops|hooks]"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Read
  - Glob
---

# DevFlow Plugin Guide

**Request:** $ARGUMENTS

Say: "SKILL INVOKED: devflow:guide"

---

## Step 1: Locate Plugin Skills

Use Glob to find all SKILL.md files in the plugin:

1. First check the plugin cache:
   - Pattern: `~/.claude/plugins/cache/claude-code-primitives/devflow/*/skills/*/SKILL.md`

2. If that fails, check if in source repo:
   - Pattern: `plugins/devflow/skills/*/SKILL.md`

---

## Step 2: Read Each Skill

For each SKILL.md found, read the first 15 lines to extract from YAML frontmatter:
- **name** - The slash command (e.g., `devflow:build:fetch-issue`)
- **description** - What it does

Parse the category from the skill directory name:
- `build-*` → Build category
- `pm-*` → PM category
- `docs-*` → Docs category
- `rag-memory-*` → RAG Memory category
- `devops-*` → DevOps category
- Others → Core category

---

## Step 3: Discover Hooks

Use Glob to find hook scripts:
- Pattern: `~/.claude/plugins/cache/claude-code-primitives/devflow/*/hooks/*.py`
- Or: `plugins/devflow/hooks/*.py`

List each hook file found. Known hooks and what they protect:
- `atlassian-approval.py` → Jira and Confluence
- `gitlab-approval.py` → GitLab issues and MRs
- `google-workspace-approval.py` → Google Docs and Drive
- `rag-memory-approval.py` → RAG Memory operations

---

## Step 4: Handle Arguments

**If $ARGUMENTS is empty or "all":**
Show ALL skills organized by category, then hooks.

**If $ARGUMENTS matches a category (build, pm, docs, rag-memory, devops):**
Show only skills in that category.

**If $ARGUMENTS is "hooks":**
Show only hooks.

---

## Step 5: Present Results

Format output as:

```
## DevFlow Plugin Guide

### Build Skills ([count])
| Skill | Description |
|-------|-------------|
| `/devflow:build:fetch-issue` | Fetch issue and analyze feasibility |
...

### PM Skills ([count])
...

### Hooks ([count] active)
| Hook | Protects |
|------|----------|
| atlassian-approval.py | Jira/Confluence operations |
...

---
**Total:** X skills, Y hooks

**Quick start:** `/devflow-setup` to configure backends
**Full workflow:** `/devflow:build:workflow-guide`
```

---

## Rules

**Always:**
- Use Glob to find actual files (don't assume)
- Read frontmatter from each SKILL.md
- Report only what exists
- Group by category based on directory name prefix

**Never:**
- Hardcode skill lists
- Use complex bash commands
- Assume structure without checking
- Report non-existent components
