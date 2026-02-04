# GitHub Issue Operations

## Prerequisites Check

Before any GitHub operation, verify the `gh` CLI is installed and authenticated:

```bash
which gh && gh auth status
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

STOP if either check fails. Do not proceed without working `gh` CLI.

---

## Repository Context

Get current repository:

```bash
gh repo view --json nameWithOwner -q '.nameWithOwner'
```

This returns the `owner/repo` format. [FROM: `gh repo view` response. NEVER guess the repo name.]

---

## Operations

### Fetch Issue

```bash
gh issue view [NUMBER] --json number,title,body,state,labels,assignees,author,milestone,url
```

- `[NUMBER]`: [FROM: user input `$ARGUMENTS`. NEVER construct.]

**Response fields:**
- `number` - Issue number
- `title` - Issue title
- `body` - Description (Markdown)
- `state` - "OPEN" or "CLOSED"
- `labels` - Array of label objects with `name` field
- `assignees` - Array of assigned users
- `author` - Creator
- `url` - Browser link

---

### Create Issue

```bash
gh issue create --title "[TITLE]" --body "[BODY]"
```

- `--title`: [FROM: user input. NEVER fabricate.]
- `--body`: [FROM: user input or generated content. OK to construct.]

Optional flags (only include if user provides):
- `--label "label1,label2"`: [FROM: user input]
- `--assignee "@me,username"`: [FROM: user input]
- `--milestone "v1.0"`: [FROM: user input]

**Returns:** Issue number and URL.

---

### Update Issue

```bash
gh issue edit [NUMBER] [flags]
```

- `[NUMBER]`: [FROM: user input `$ARGUMENTS`. NEVER construct.]

Available flags:
- `--title "New title"`: [FROM: user input]
- `--body "New body"`: [FROM: user input]
- `--add-label "label1,label2"`: [FROM: user input or workflow logic]
- `--remove-label "label"`: [FROM: user input or workflow logic]
- `--add-assignee "username"`: [FROM: user input]
- `--milestone "v1.0"`: [FROM: user input]

---

### Transition Issue (Close/Reopen)

**Close issue:**
```bash
gh issue close [NUMBER]
```
- `[NUMBER]`: [FROM: user input `$ARGUMENTS`. NEVER construct.]

**Close with comment:**
```bash
gh issue close [NUMBER] --comment "Fixed in PR #[PR_NUMBER]"
```
- `[NUMBER]`: [FROM: user input `$ARGUMENTS`. NEVER construct.]
- `[PR_NUMBER]`: [FROM: `gh pr create` response. NEVER guess.]

**Reopen issue:**
```bash
gh issue reopen [NUMBER]
```

**Workflow states via labels:**

GitHub doesn't have built-in workflow states. Use labels:
```bash
# Move to "In Progress"
gh issue edit [NUMBER] --add-label "in-progress" --remove-label "todo"

# Move to "Review"
gh issue edit [NUMBER] --add-label "in-review" --remove-label "in-progress"
```

---

### Add Comment

```bash
gh issue comment [NUMBER] --body "Comment text"
```

- `[NUMBER]`: [FROM: user input `$ARGUMENTS`. NEVER construct.]
- `--body`: [FROM: generated content. OK to construct.]

---

### Search Issues

```bash
gh issue list [flags]
```

Flags:
- `--state open|closed|all`: [FROM: user request]
- `--label "bug"`: [FROM: user request]
- `--assignee "@me"`: [FROM: user request]
- `--search "search term"`: [FROM: user request. OK to construct.]
- `--json number,title,state,labels`: Output format

---

### Link Issue to PR

When creating a PR, reference the issue in the body:
```bash
gh pr create --title "Fix #[NUMBER]" --body "Fixes #[NUMBER]"
```

Keywords that auto-close issues when PR is merged:
- `Fixes #[NUMBER]`
- `Closes #[NUMBER]`
- `Resolves #[NUMBER]`

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

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| "gh: command not found" | CLI not installed | Install gh CLI |
| "not logged in" | Not authenticated | Run `gh auth login` |
| "Could not resolve" | Repo not found | Check you're in a git repo with GitHub remote |
| "issue not found" | Invalid issue number | Verify issue exists |
| "HTTP 403" | Insufficient permissions | Check repo access |

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| issue number | User input `$ARGUMENTS` | Construct from other data |
| repo (owner/repo) | `gh repo view` response or git remote | Guess or assume |
| PR number | `gh pr create` response | Guess or fabricate |
| label names | User input or workflow logic | Infer from other backends |
