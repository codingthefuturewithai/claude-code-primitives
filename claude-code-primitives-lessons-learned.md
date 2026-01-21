# Claude Code Primitives: Skills, Plugins, and Repository Organization

## Overview

This document captures lessons learned about creating and organizing Claude Code primitives, including skills, plugins, namespace prefixing conventions, repository structure, and the symlink architecture for sharing primitives across plugins.

---

## Skill Naming and Namespace Prefixes

### The `name` Field Determines Display Name

The `name` field in a skill's SKILL.md frontmatter determines the displayed name, including any namespace prefix.

**Correct format for plugin skills:**
```yaml
---
name: plugin-name:skill-name
description: Description of what the skill does
user-invocable: true
---
```

**Example:**
```yaml
---
name: primitives-toolkit:knowledge-management
description: Store or update content in RAG Memory or Confluence.
user-invocable: true
---
```

### Common Mistake: Missing Namespace Prefix

If a skill shows without its plugin prefix (e.g., `/knowledge-management` instead of `/primitives-toolkit:knowledge-management`), check the `name` field in SKILL.md. The issue is almost always that the `name` field lacks the `plugin-name:` prefix.

**Wrong:**
```yaml
name: knowledge-management
```

**Correct:**
```yaml
name: primitives-toolkit:knowledge-management
```

### Standalone Skills vs Plugin Skills

- **Standalone skills** (installed via ai-agent-skills): Use `repo-name:skill-name` format
- **Plugin skills**: Use `plugin-name:skill-name` format

Example for standalone skill in `ctf-claude-code-primitives` repo:
```yaml
name: ctf-claude-code-primitives:ctfai-brand
```

---

## Repository Structure for Primitives Marketplace

### Standard Plugin Structure

Claude Code plugins follow this standard structure with commands/, hooks/, skills/, and agents/ at the plugin root:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json         # Plugin manifest
├── commands/               # Slash commands
│   └── command-name/
│       └── COMMAND.md
├── hooks/                  # Automatic triggers
│   ├── hooks.json
│   └── hook-script.py
├── skills/                 # AI-driven workflows
│   └── skill-name/
│       └── SKILL.md
└── agents/                 # Subagent definitions
    └── agent-name/
        └── AGENT.md
```

### Primitives Marketplace Repository Structure

For repositories that serve as a "primitives marketplace" (containing multiple reusable primitives), use this structure:

```
marketplace-repo/
├── commands/                     # Shared commands (source of truth)
│   └── domain-name/
│       └── command-name/
│           └── COMMAND.md
├── hooks/                        # Shared hooks (source of truth)
│   └── hook-script.py
├── skills/                       # Shared skills (ai-agent-skills compatible)
│   └── skill-name/
│       └── SKILL.md
├── plugins/
│   └── plugin-name/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       │   ├── plugin-specific/  # Plugin-only commands
│       │   └── shared/ → ../../../commands/shared (symlinks)
│       ├── hooks/
│       │   └── hook.py → ../../../hooks/hook.py
│       └── skills/
│           ├── plugin-specific/  # Plugin-only skills
│           └── shared/ → ../../../skills/shared
└── README.md
```

### Key Insight: Root-Level `skills/` for ai-agent-skills

The `ai-agent-skills` NPX tool looks for a `skills/` folder at the repository root. Skills must be placed at `skills/skill-name/` for the installation command to work.

**Installation command format:**
```bash
npx ai-agent-skills install owner/repo/skill-name --agent claude
```

**Path resolution logic (from ai-agent-skills source):**
```javascript
const skillsDir = fs.existsSync(path.join(tempDir, 'skills'))
  ? path.join(tempDir, 'skills')
  : tempDir;
```

The tool:
1. Clones the repository
2. Checks if `skills/` directory exists at repo root
3. If yes, looks for `skills/skill-name/`
4. If no, looks for `skill-name/` at repo root

---

## Symlink Architecture for Sharing Primitives

### Why Symlinks?

When a repository contains both standalone skills (for ai-agent-skills installation) and a plugin (for marketplace installation), symlinks enable a single source of truth.

### Correct Symlink Paths

From `plugins/plugin-name/skills/`, the relative path to reach `skills/` at repo root is `../../../skills/`.

**Path calculation:**
```
plugins/plugin-name/skills/skill-name →
  ../                              (up to skills/)
  ../                              (up to plugin-name/)
  ../                              (up to plugins/)
  skills/skill-name                (down to target)
= ../../../skills/skill-name
```

### Creating Symlinks

```bash
# From the plugin's skills directory
cd plugins/plugin-name/skills

# Create symlink to shared skill
ln -s ../../../skills/knowledge-management knowledge-management

# Verify symlink
ls -la
# Should show: knowledge-management -> ../../../skills/knowledge-management
```

### Common Mistake: Wrong Relative Paths

Using `../../skills/` instead of `../../../skills/` will create broken symlinks.

**Wrong:** `../../skills/skill-name`
**Correct:** `../../../skills/skill-name`

---

## Plugin Installation and Setup Flow

### Marketplace Installation Flow

1. **Add marketplace:**
   ```
   /plugin marketplace add https://github.com/owner/repo
   ```

2. **Install plugin:**
   ```
   /plugin install plugin-name@repo-name
   ```

3. **Setup skills (required due to Claude Code limitation):**
   ```
   /plugin-name:admin:setup-skills
   ```

4. **Restart Claude Code** to load the skills

5. **Verify:**
   ```
   /plugin-name:skill-name --test
   ```

### Standalone Skill Installation Flow

1. **Install skill:**
   ```bash
   npx ai-agent-skills install owner/repo/skill-name --agent claude
   ```

2. **Restart Claude Code**

3. **Use skill:**
   ```
   /repo-name:skill-name
   ```

---

## Environment Cleanup Procedures

### Full Plugin/Skill Cleanup

To completely remove a plugin and its skills for fresh testing:

```bash
# 1. Remove skill symlinks from user directory
rm ~/.claude/skills/skill-name

# 2. Remove plugin cache
rm -rf ~/.claude/plugins/cache/repo-name/

# 3. Remove marketplace cache
rm -rf ~/.claude/plugins/marketplaces/repo-name/

# 4. Edit installed_plugins.json - remove plugin entry
# File: ~/.claude/plugins/installed_plugins.json

# 5. Edit known_marketplaces.json - remove marketplace entry
# File: ~/.claude/plugins/known_marketplaces.json

# 6. Restart Claude Code
```

### Selective Skill Removal

To remove only a specific skill without removing the plugin:

```bash
rm ~/.claude/skills/skill-name
# Then restart Claude Code
```

---

## Troubleshooting Guide

### Skill Shows Without Plugin Prefix

**Symptom:** `/skill-name` instead of `/plugin-name:skill-name`

**Cause:** The `name` field in SKILL.md lacks the plugin prefix

**Fix:** Update SKILL.md frontmatter:
```yaml
name: plugin-name:skill-name
```

### Skill Not Found After Installation

**Symptom:** Skill doesn't appear in autocomplete or fails to invoke

**Causes and fixes:**
1. **Didn't run setup-skills:** Run `/plugin-name:admin:setup-skills`
2. **Didn't restart Claude Code:** Start a new session
3. **Wrong skills/ location:** Ensure skills are at `skills/skill-name/` at repo root for ai-agent-skills, or properly symlinked in plugin for marketplace installation

### Symlinks Not Working

**Symptom:** Plugin can't find skill files

**Cause:** Incorrect relative paths in symlinks

**Fix:**
```bash
# Check current symlink
ls -la plugins/plugin-name/skills/

# Remove broken symlink
rm plugins/plugin-name/skills/skill-name

# Create correct symlink
ln -s ../../../skills/skill-name plugins/plugin-name/skills/skill-name
```

### ai-agent-skills Installation Fails

**Symptom:** `npx ai-agent-skills install owner/repo/skill-name` doesn't find skill

**Causes:**
1. No `skills/` directory at repo root
2. Skill not at `skills/skill-name/` path
3. Missing SKILL.md in skill directory

**Fix:** Ensure repository structure follows:
```
repo/
└── skills/
    └── skill-name/
        └── SKILL.md
```

### Hooks Not Triggering

**Symptom:** PreToolUse hooks don't fire before protected operations

**Causes:**
1. **Session not restarted:** Hooks load at session start. Restart Claude Code after plugin installation.
2. **Hook file not found:** Check symlink resolves correctly
3. **hooks.json misconfigured:** Verify matcher patterns include the tool names

**Fix:** Restart Claude Code session after any plugin changes.

---

## Quick Reference

### Naming Conventions

| Context | Format | Example |
|---------|--------|---------|
| Plugin skill name field | `plugin-name:skill-name` | `primitives-toolkit:knowledge-management` |
| Standalone skill name field | `repo-name:skill-name` | `ctf-claude-code-primitives:ctfai-brand` |
| Skill invocation | `/name-from-skill.md` | `/primitives-toolkit:knowledge-management` |

### Path Reference

| From | To | Relative Path |
|------|-----|---------------|
| `plugins/plugin-name/skills/` | `skills/` | `../../../skills/` |
| `plugins/plugin-name/commands/` | `commands/` | `../../../commands/` |
| `plugins/plugin-name/hooks/` | `hooks/` | `../../../hooks/` |

### Key Files

| File | Purpose |
|------|---------|
| `skills/skill-name/SKILL.md` | Skill definition and instructions |
| `plugins/plugin-name/.claude-plugin/plugin.json` | Plugin manifest |
| `~/.claude/plugins/installed_plugins.json` | Installed plugins registry |
| `~/.claude/plugins/known_marketplaces.json` | Known marketplaces registry |
| `~/.claude/skills/` | User-level skill symlinks |

---

## Critical Lessons

1. **Never assume which copy is the source of truth.** Before restructuring, verify which file has the most recent changes.

2. **The `name` field in SKILL.md is everything.** It determines how the skill appears, including namespace prefixes.

3. **Hooks require session restart.** They load at session start, not dynamically.

4. **Symlink paths from plugins to root require `../../../`** - three levels up from `plugins/plugin-name/component/`.

5. **ai-agent-skills requires `skills/` at repo root.** The tool won't find skills in nested directories.

6. **Don't tell Claude which ingest tool to use.** Let Claude discover available tools and choose based on input type (file path, URL, or raw text).
