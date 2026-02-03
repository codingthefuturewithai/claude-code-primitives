---
description: Configure DevFlow backends for issue tracking, documentation, and VCS
argument-hint: ""
allowed-tools: ["Read", "Write", "Bash", "mcp__atlassian__getAccessibleAtlassianResources", "mcp__gitlab__list_projects", "mcp__google-workspace__list_drive_items", "mcp__rag-memory__list_collections", "AskUserQuestion"]
---

# DevFlow Setup Wizard

I'll help you configure DevFlow backends for your development workflow.

**Say exactly:** "COMMAND INVOKED: devflow:admin:setup"

---

## Philosophy: Everything is Optional

All integrations are optional. You choose what you want:
- Issue tracking: Jira, GitLab, or skip entirely
- Documentation: Confluence, Google Docs, RAG Memory, or skip
- VCS: Automatically detected from git remote

---

## Step 1: Check Existing Configuration

[Check for existing config file]

```bash
if [ -f ".claude/devflow-config.md" ]; then
  echo "Project config exists"
elif [ -f "$HOME/.claude/devflow-config.md" ]; then
  echo "Global config exists"
else
  echo "No config found - starting fresh"
fi
```

If config exists, show current settings and ask:
> "You have an existing DevFlow configuration. Would you like to:"
> 1. Reconfigure from scratch
> 2. Keep current settings
> 3. View current settings

---

## Step 2: Issue Tracking

**Ask user:**
> "Do you want to use an issue tracker with DevFlow?"
> 1. Yes - Jira (Atlassian MCP)
> 2. Yes - GitLab Issues (GitLab MCP)
> 3. Yes - GitHub Issues (gh CLI)
> 4. No - Skip issue tracking (code-only workflows)

### If Jira selected:

**Test Atlassian MCP:**
```
Call mcp__atlassian__getAccessibleAtlassianResources
```

- **Success:** Store cloudId, continue
- **Failure:**
  > "Atlassian MCP not available. Would you like:"
  > 1. Help setting it up (show instructions)
  > 2. Try a different option
  > 3. Skip issue tracking

If help requested, read and display: `adapters/setup/atlassian-mcp.md`

### If GitLab selected:

**Test GitLab MCP:**
```
Call mcp__gitlab__list_projects
```

- **Success:** Continue
- **Failure:**
  > "GitLab MCP not available. Would you like:"
  > 1. Help setting it up (show instructions)
  > 2. Try a different option
  > 3. Skip issue tracking

If help requested, read and display: `adapters/setup/gitlab-mcp.md`

### If GitHub Issues selected:

**Test gh CLI:**
```bash
# Check if gh is installed
which gh

# Check if authenticated
gh auth status
```

- **Success (both checks pass):** Continue
- **gh not installed:**
  > "GitHub CLI (gh) not installed. Would you like:"
  > 1. Help installing it (show instructions)
  > 2. Try a different option
  > 3. Skip issue tracking

  If help requested, show:
  > "Install the GitHub CLI:
  > - macOS: `brew install gh`
  > - Linux: See https://github.com/cli/cli#installation
  > - Windows: `winget install GitHub.cli`
  >
  > Then authenticate: `gh auth login`"

- **gh not authenticated:**
  > "GitHub CLI not authenticated. Please run: `gh auth login`
  > Then re-run this setup."

---

## Step 3: Documentation System

**Ask user:**
> "Do you want documentation integration?"
> 1. Yes - Confluence (Atlassian)
> 2. Yes - Google Docs
> 3. No - Skip documentation

### If Confluence selected:

**Test (reuse Atlassian check from Step 2 if available):**
```
Call mcp__atlassian__getAccessibleAtlassianResources
```

- **Success:** Continue
- **Failure:** Offer setup help or skip

### If Google Docs selected:

**Test Google Workspace MCP:**
```
Call mcp__google-workspace__list_drive_items
```

- **Success:** Continue
- **Failure:**
  > "Google Workspace MCP not available. Would you like:"
  > 1. Help setting it up (show instructions)
  > 2. Try a different option
  > 3. Skip documentation

If help requested, read and display: `adapters/setup/google-workspace-mcp.md`

**If Google Docs enabled, ask about organization:**
> "How should documents be organized?"
> 1. I'll provide doc links when relevant (manual)
> 2. Create in a default folder (specify folder ID)
> 3. Ask me each time

---

## Step 4: RAG Memory (Knowledge Base)

**Ask user:**
> "Do you want RAG Memory for AI-retrievable knowledge?"
>
> RAG Memory stores knowledge that AI can search and retrieve - useful for:
> - Technical documentation
> - Project notes
> - Quick references
>
> 1. Yes - Enable RAG Memory
> 2. No - Skip RAG Memory

### If Yes:

**Test RAG Memory MCP:**
```
Call mcp__rag-memory__list_collections
```

- **Success:** Continue
- **Failure:**
  > "RAG Memory MCP not available. Would you like:"
  > 1. Help setting it up (show instructions)
  > 2. Skip RAG Memory

If help requested, read and display: `adapters/setup/rag-memory-mcp.md`

### If both docs AND RAG Memory enabled:

> "You have both a docs backend and RAG Memory enabled. How should content be routed?"
> 1. Let me decide each time (default)
> 2. Quick notes go to RAG, formal docs go to [Confluence/Google Docs]
> 3. Everything to RAG Memory

---

## Step 5: VCS Auto-Detection

**Detect from git remote:**
```bash
git remote get-url origin 2>/dev/null
```

- Contains `github.com` → GitHub (use gh CLI)
- Contains `gitlab` → GitLab (use GitLab MCP for MRs)
- Other → Default to git-only

**Show detection:**
> "Detected VCS: [GitHub/GitLab] from git remote"
>
> This will be used for PR/MR creation in `/devflow:build:complete-issue`

---

## Step 6: Summary & Write Configuration

**Show summary:**

```
DevFlow Configuration Summary
=============================

Issue Tracking:
  Backend: [jira/gitlab/none]
  Status: [enabled/disabled]

Documentation:
  Backend: [confluence/google-docs/none]
  Status: [enabled/disabled]
  Organization: [manual/default-folder/ask-each-time]

Knowledge Base (RAG Memory):
  Status: [enabled/disabled]
  Routing: [decide-each-time/quick-to-rag/all-to-rag]

Version Control:
  Backend: [github/gitlab]
  Auto-detected: [yes/no]

Configuration will be saved to: ~/.claude/devflow-config.md
```

**Ask for confirmation:**
> "Save this configuration?"
> 1. Yes - Save to global config (~/.claude/)
> 2. Yes - Save to project config (.claude/)
> 3. No - Cancel setup

---

## Step 7: Write Configuration File

Write to chosen location:

```markdown
# DevFlow Backend Configuration
# Generated by /devflow:admin:setup
# Regenerate anytime with: /devflow:admin:setup

## Issue Tracking
backend: [jira/gitlab/github/none]
enabled: [true/false]
# For Jira:
cloudId: [if jira]
# For GitLab:
default_project: [if gitlab, optional]
# For GitHub:
# Uses current repo context via gh CLI

## Documentation
backend: [confluence/google-docs/none]
enabled: [true/false]
organization: [manual/default-folder/ask-each-time]
# For Google Docs with default-folder:
default_folder_id: [folder id]
# For Confluence:
default_space: [space key, optional]

## Knowledge Base (RAG Memory)
enabled: [true/false]
routing: [decide-each-time/quick-to-rag/all-to-rag]

## Version Control
backend: [github/gitlab]
# Auto-detected from git remote
```

---

## Complete

> "DevFlow configured! Your backends are ready."
>
> **Available commands:**
> - `/devflow:build:fetch-issue` - Fetch and analyze issues
> - `/devflow:build:plan-work` - Create implementation plans
> - `/devflow:build:implement-plan` - Execute plans
> - `/devflow:build:complete-issue` - Create PR/MR and close issue
>
> **Reconfigure anytime:**
> - `/devflow:admin:setup`
>
> **If you enabled RAG Memory:**
> - Run `/devflow:rag-memory:setup-collections` to create recommended collections
