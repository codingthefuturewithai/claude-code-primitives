---
name: devflow:guide
description: Discover all DevFlow plugin components - skills, hooks, and commands with descriptions and usage instructions
argument-hint: "[category]"
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# DevFlow Plugin Guide

**Request:** $ARGUMENTS

---

## Step 1: Locate the Plugin

Find the installed DevFlow plugin location:

```bash
# Check for the plugin cache
PLUGIN_PATH=$(find ~/.claude/plugins/cache/claude-code-primitives -name "devflow" -type d 2>/dev/null | head -1)
echo "Plugin path: $PLUGIN_PATH"
```

If not found, check if we're in the source repo:
```bash
# Check if we're in the source repository
if [ -d "plugins/devflow" ]; then
  PLUGIN_PATH="plugins/devflow"
fi
```

---

## Step 2: Discover Skills

Scan the plugin's `skills/` directory to find all available skills:

```bash
# List all skill directories/symlinks
ls -la "$PLUGIN_PATH/skills/" 2>/dev/null
```

For each skill found, read its `SKILL.md` to extract:
- **name** - The slash command name (from frontmatter)
- **description** - What the skill does (from frontmatter)
- **argument-hint** - Arguments it accepts (from frontmatter)
- **user-invocable** - Whether user can invoke directly (from frontmatter)

**Reading skill info:**
```bash
# For each skill directory, read SKILL.md
head -20 "$PLUGIN_PATH/skills/<skill-name>/SKILL.md"
```

**Note:** Skills appear in the symlinked structure. Follow symlinks to read the actual SKILL.md files.

---

## Step 3: Discover Commands (if any)

Check if the plugin has a `commands/` directory:

```bash
# Check for commands directory
ls -la "$PLUGIN_PATH/commands/" 2>/dev/null
```

If commands exist, for each `.md` file, extract the same frontmatter fields.

**Note:** If no commands directory exists or it's empty, report "No traditional commands - this plugin uses skills."

---

## Step 4: Discover Hooks

Check the plugin's `hooks/` directory:

```bash
# List hook files
ls -la "$PLUGIN_PATH/hooks/" 2>/dev/null

# Read hooks.json for configured hooks
cat "$PLUGIN_PATH/hooks/hooks.json" 2>/dev/null
```

For each hook script (`.py` files), note its name and purpose.

**Note:** Hooks embedded in skill frontmatter are automatically active when that skill runs.

---

## Step 5: Handle Arguments

**If $ARGUMENTS is empty:**
Show ALL components organized by type (Skills, Commands, Hooks).

**If $ARGUMENTS matches a category (e.g., "build", "pm", "docs"):**
Show only skills/commands in that category.

**If $ARGUMENTS is "skills":**
Show only skills.

**If $ARGUMENTS is "hooks":**
Show only hooks.

**If $ARGUMENTS is "commands":**
Show only commands (or note if none exist).

---

## Step 6: Present Results

### Format for Skills:

```markdown
## Skills ([count] available)

### [Category] Skills

| Skill | Description |
|-------|-------------|
| `/devflow:category:name` | Description from frontmatter |

**Usage:** `/devflow:category:name [arguments]`
```

### Format for Commands (if any):

```markdown
## Commands ([count] available)

| Command | Description |
|---------|-------------|
| `/devflow:command` | Description from frontmatter |
```

### Format for Hooks:

```markdown
## Hooks ([count] active)

Hooks run automatically to protect external systems:

| Hook | Protects |
|------|----------|
| `atlassian-approval.py` | Jira and Confluence operations |
| `gitlab-approval.py` | GitLab issues and MRs |
| `google-workspace-approval.py` | Google Docs and Drive |
| `rag-memory-approval.py` | RAG Memory operations |

**Note:** Hooks prompt for approval before modifying external systems.
```

---

## Step 7: Provide Summary

At the end, provide:

1. Total counts: X skills, Y commands, Z hooks
2. Quick start tip based on what's available
3. Configuration reminder: "Run `/devflow-setup` to configure backends"

---

## Rules

**Always:**
- Scan the ACTUAL plugin directory structure
- Read frontmatter from each skill/command file
- Include any new components automatically discovered
- Follow symlinks to read actual file contents
- Report accurately what exists (don't invent components)

**Never:**
- Hardcode lists of skills/commands/hooks
- Assume what exists without checking
- Skip components because they're not in a predefined list
- Report components that don't exist in the plugin

---

## Example Output

```markdown
# DevFlow Plugin Guide

## Skills (18 available)

### Build Skills (9)
Development workflow - from issue fetch to PR completion

| Skill | Description |
|-------|-------------|
| `/devflow:build:fetch-issue` | Fetch issue and analyze feasibility |
| `/devflow:build:plan-work` | Analyze issue and develop implementation plan |
| `/devflow:build:implement-plan` | Execute approved implementation plan |
| `/devflow:build:create-issue` | Create issue with codebase analysis |
| `/devflow:build:complete-issue` | Final validation, create PR/MR, mark done |
| `/devflow:build:post-merge` | Sync with remote after merge and clean up |
| `/devflow:build:security-review` | Security analysis of changes |
| `/devflow:build:workflow-guide` | Workflow overview |
| `/devflow:build-ops` | Backend operations (internal) |

### PM Skills (2)
Product management - roadmap and backlog

| Skill | Description |
|-------|-------------|
| `/devflow:pm:roadmap` | Manage Confluence product roadmap |
| `/devflow:pm:backlog` | Manage Jira backlog from roadmap |

### Docs Skills (2)
Documentation management

| Skill | Description |
|-------|-------------|
| `/devflow:docs:documentation-audit` | Audit docs against source code |
| `/devflow:docs:reference-audit` | Discover and sync project docs |

### RAG Memory Skills (2)
Knowledge base setup

| Skill | Description |
|-------|-------------|
| `/devflow:rag-memory:setup-collections` | Scaffold RAG Memory collections |
| `/devflow:rag-memory:create-agent-preferences` | Create agent preferences |

### DevOps Skills (1)

| Skill | Description |
|-------|-------------|
| `/devflow:devops:sync-claude-knowledge` | Sync Claude Code changelog |

### Core Skills (3)

| Skill | Description |
|-------|-------------|
| `/devflow-setup` | Configure backends |
| `/devflow:guide` | This guide |
| `/devflow:knowledge-management` | Route content to KB |
| `/repo-explorer` | Analyze GitHub repositories |

## Commands

No traditional commands - this plugin uses skills.

## Hooks (4 active)

| Hook | Protects |
|------|----------|
| `atlassian-approval.py` | Jira/Confluence operations |
| `gitlab-approval.py` | GitLab issues/MRs |
| `google-workspace-approval.py` | Google Docs/Drive |
| `rag-memory-approval.py` | RAG Memory operations |

---

**Total: 18 skills, 0 commands, 4 hooks**

**Quick start:** Run `/devflow-setup` to configure your backends, then use `/devflow:build:workflow-guide` to learn the development workflow.
```
