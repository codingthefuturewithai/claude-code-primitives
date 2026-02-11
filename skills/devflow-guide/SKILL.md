---
name: devflow:guide
description: Discover all DevFlow plugin primitives - skills, sub-agents, hooks, and commands with descriptions and usage
argument-hint: "[build|pm|foundation|docs|rag-memory|devops|setup-utilities|hooks|agents|all]"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# DevFlow Plugin Guide

**Say exactly:** "SKILL INVOKED: devflow:guide"

**Request:** $ARGUMENTS

---

## Goal

Discover all primitives installed in `${CLAUDE_PLUGIN_ROOT}` and present them to the user. If $ARGUMENTS specifies a filter, show only that section.

---

## Discovery

### Skills

Each subdirectory of `${CLAUDE_PLUGIN_ROOT}/skills/` that contains a `SKILL.md` is a skill. Read the YAML frontmatter of each `SKILL.md` to extract `name` and `description`.

Categorize each skill by its directory name prefix:

| Directory prefix | Category key | Display heading |
|-----------------|--------------|-----------------|
| build | build | Build Workflow (Issue → PR/MR) |
| pm | pm | Project Management (Upstream SDLC) |
| foundation | foundation | Foundation (Team Standards & Config) |
| docs | docs | Documentation |
| rag-memory | rag-memory | RAG Memory |
| devops | devops | DevOps |
| (no prefix match) | setup-utilities | Setup & Utilities |

### Agents

Every non-hidden file in `${CLAUDE_PLUGIN_ROOT}/agents/` is an agent definition (markdown with YAML frontmatter — may or may not have `.md` extension). Read the frontmatter to extract `name`, `description`, `model`, and `tools`.

### Hooks

`${CLAUDE_PLUGIN_ROOT}/hooks/` contains Python hook scripts (`.py` files) and a `hooks.json` configuration. Read `hooks.json` to find matchers grouped by event type. Group matchers by backend — infer from the matcher pattern (atlassian, gitlab, google-drive, rag-memory).

---

## Filtering

If $ARGUMENTS matches a category key, "hooks", or "agents", show only that section and end with:

> Run `/devflow:guide` with no arguments to see the full guide.

If $ARGUMENTS is empty or "all", show the full guide below.

---

## Full Guide Presentation

### 1. Opening

> **DevFlow** is an AI-native SDLC plugin for Claude Code. It connects your issue tracker, documentation, and VCS into a single workflow — from problem discovery through PR/MR creation.

### 2. Scenario Table

Present this verbatim as the first thing after the opening:

**Where do you want to start?**

| I want to... | Run |
|--------------|-----|
| Work on an existing issue | `/devflow:build:fetch-issue [KEY]` |
| Start a new project or feature | `/devflow:pm:discover` |
| Set up team standards | `/devflow:foundation:capture-conventions` |
| Audit a repo against team standards | `/devflow:foundation:audit-conventions` |
| Generate CLAUDE.md for a repo | `/devflow:foundation:generate-claude-md` |
| First-time setup | `/devflow-setup` |
| See the build workflow end-to-end | `/devflow:build:workflow-guide` |

### 3. Categorized Skill Inventory

For each category that has skills, render:

**[Display heading] ([count])**

| Skill | Description |
|-------|-------------|
| `/[name]` | [description] |

### 4. Agents

**Custom Agents ([count])**

| Agent | Model | Description |
|-------|-------|-------------|
| [name] | [model] | [description] |

### 5. Hooks

**Approval Hooks ([script count] scripts, [matcher count] protected operations)**

These hooks require user approval before writing to external backends.

For each backend group:

**[Backend Name]**

| Operation | Matcher |
|-----------|---------|
| [last segment of matcher] | [full matcher pattern] |

### 6. Summary Footer

**Total:** [skill count] skills, [agent count] agents, [hook script count] hook scripts ([matcher count] protected operations)

**Quick start:**
- `/devflow-setup` — Configure your backends (first time)
- `/devflow:build:workflow-guide` — Learn the build workflow
- `/devflow:build:fetch-issue [KEY]` — Start working on an issue
- `/devflow:pm:discover` — Start a new project or feature
