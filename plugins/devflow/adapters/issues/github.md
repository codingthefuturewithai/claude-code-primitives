# GitHub Issues Adapter

## Overview

Adapter patterns for GitHub Issues operations via `gh` CLI.

---

## Prerequisites Check

Before using GitHub Issues, verify the `gh` CLI is installed and authenticated:

```bash
# Check if gh is installed
which gh || echo "gh CLI not installed"

# Check if authenticated
gh auth status
```

**If not installed:**
> "The GitHub CLI (`gh`) is not installed. Please install it:
> - macOS: `brew install gh`
> - Linux: See https://github.com/cli/cli#installation
> - Windows: `winget install GitHub.cli`
>
> Then authenticate: `gh auth login`"

**If not authenticated:**
> "The GitHub CLI is not authenticated. Please run: `gh auth login`"

---

## Connection Setup

No special setup needed beyond `gh auth`. Operations use the current repository context.

### Determine Repository

```bash
# Get current repo in owner/repo format
gh repo view --json nameWithOwner -q '.nameWithOwner'
```

Or derive from git remote:
```bash
git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/'
```

---

## Operations

### Fetch Issue

```bash
gh issue view [NUMBER] --json number,title,body,state,labels,assignees,author,milestone,url
```

**Response fields:**
- `number` - Issue number
- `title` - Issue title
- `body` - Description (Markdown)
- `state` - "OPEN" or "CLOSED"
- `labels` - Array of label objects with `name` field
- `assignees` - Array of assigned users
- `author` - Creator
- `milestone` - Associated milestone
- `url` - Browser link

**Example:**
```bash
gh issue view 123 --json number,title,body,state,labels,url
```

---

### Create Issue

```bash
gh issue create --title "Issue title" --body "Description text"
```

Optional flags:
- `--label "bug,urgent"` - Comma-separated labels
- `--assignee "@me,username"` - Assignees
- `--milestone "v1.0"` - Milestone name
- `--project "Project Name"` - Add to project

**Example:**
```bash
gh issue create \
  --title "Add user authentication" \
  --body "## Background
User authentication is needed for...

## Acceptance Criteria
- Users can log in with email/password
- Session persists across browser refresh" \
  --label "feature,priority:high"
```

**Returns:** Issue number and URL

---

### Update Issue

```bash
gh issue edit [NUMBER] [flags]
```

Available flags:
- `--title "New title"` - Update title
- `--body "New body"` - Replace entire body
- `--add-label "label1,label2"` - Add labels
- `--remove-label "label"` - Remove labels
- `--add-assignee "username"` - Add assignee
- `--milestone "v1.0"` - Set milestone

**Example:**
```bash
gh issue edit 123 --add-label "in-progress" --remove-label "todo"
```

---

### Transition Issue (Close/Reopen)

**Close issue:**
```bash
gh issue close [NUMBER]
```

**Close with comment:**
```bash
gh issue close [NUMBER] --comment "Fixed in PR #456"
```

**Reopen issue:**
```bash
gh issue reopen [NUMBER]
```

**Workflow states via labels:**

GitHub doesn't have built-in workflow states. Use labels instead:
```bash
# Move to "In Progress"
gh issue edit 123 --add-label "in-progress" --remove-label "todo"

# Move to "Review"
gh issue edit 123 --add-label "in-review" --remove-label "in-progress"
```

---

### Add Comment

```bash
gh issue comment [NUMBER] --body "Comment text"
```

**Example:**
```bash
gh issue comment 123 --body "Started working on this. Initial analysis shows..."
```

---

### Search Issues

```bash
gh issue list [flags]
```

Flags:
- `--state open|closed|all` - Filter by state
- `--label "bug"` - Filter by label
- `--assignee "@me"` - Filter by assignee
- `--search "search term"` - Search in title/body
- `--json number,title,state,labels` - Output as JSON

**Examples:**
```bash
# List open issues
gh issue list --state open

# Search for issues
gh issue list --search "authentication" --json number,title,url

# Filter by label
gh issue list --label "bug" --state open
```

---

### Link Issue to PR

When creating a PR, reference the issue:
```bash
gh pr create --title "Fix authentication bug" --body "Fixes #123"
```

Keywords that auto-close issues when PR is merged:
- `Fixes #123`
- `Closes #123`
- `Resolves #123`

---

## Status Mapping

GitHub has simple states. Use labels for workflow:

| DevFlow Status | GitHub State | Suggested Label |
|----------------|--------------|-----------------|
| todo | OPEN | "todo" |
| in_progress | OPEN | "in-progress" |
| review | OPEN | "in-review" |
| done | CLOSED | (none needed) |

---

## Key Differences from Jira/GitLab

| Aspect | Jira | GitLab | GitHub |
|--------|------|--------|--------|
| Issue ID | Key (PROJ-123) | IID (123 per project) | Number (123 per repo) |
| Workflow | Complex transitions | Simple open/closed | Simple open/closed |
| Custom states | Built-in | Use labels | Use labels |
| API | REST via MCP | REST via MCP | CLI (`gh`) |
| Project ref | Cloud ID + key | Project path | owner/repo |
| Epics | Issue type | Separate endpoint | Issues with label |

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| "gh: command not found" | CLI not installed | Install gh CLI |
| "not logged in" | Not authenticated | Run `gh auth login` |
| "Could not resolve" | Repo not found | Check you're in a git repo with GitHub remote |
| "issue not found" | Invalid issue number | Verify issue exists |
| "HTTP 403" | Insufficient permissions | Check repo access |

---

## Complete Example: Full Workflow

```bash
# 1. Create issue
gh issue create \
  --title "Add dark mode support" \
  --body "## Background
Users have requested dark mode...

## Acceptance Criteria
- Toggle in settings
- Persists preference
- Follows system preference by default" \
  --label "feature,ui"

# 2. Start work - add label
gh issue edit 123 --add-label "in-progress" --remove-label "todo"

# 3. Add progress comment
gh issue comment 123 --body "Implementing theme provider..."

# 4. Create PR that closes issue
gh pr create --title "Add dark mode support" --body "Closes #123

## Summary
Implemented dark mode toggle..."

# 5. After PR merged, issue auto-closes due to 'Closes #123'
```
