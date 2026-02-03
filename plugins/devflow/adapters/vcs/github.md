# GitHub VCS Adapter

## Overview

Adapter patterns for GitHub operations via `gh` CLI.

---

## Prerequisites

- GitHub CLI (`gh`) installed
- Authenticated: `gh auth login`

---

## Operations

### Create Pull Request

```bash
gh pr create --title "[ISSUE-KEY]: Summary" --body "$(cat <<'EOF'
Fixes [ISSUE-KEY]

## Summary
What was implemented and why

## Changes
- Key change 1
- Key change 2

## Validation
- Tests: X passed
- Coverage: Y%

**JIRA:** [link to issue]
EOF
)"
```

**Options:**
- `--base main` - Target branch
- `--head feature-branch` - Source branch
- `--draft` - Create as draft
- `--assignee @me` - Assign to self
- `--reviewer user1,user2` - Request reviews

---

### View Pull Request

```bash
gh pr view [PR_NUMBER]
gh pr view --web  # Open in browser
```

---

### List Pull Requests

```bash
gh pr list
gh pr list --state open
gh pr list --author @me
```

---

### Check PR Status

```bash
gh pr status
gh pr checks [PR_NUMBER]
```

---

### Merge Pull Request

```bash
gh pr merge [PR_NUMBER] --merge   # Merge commit
gh pr merge [PR_NUMBER] --squash  # Squash and merge
gh pr merge [PR_NUMBER] --rebase  # Rebase and merge
```

---

### Create Branch

```bash
git checkout -b feature/ISSUE-123-description
git push -u origin feature/ISSUE-123-description
```

---

### View Repository Info

```bash
gh repo view
gh repo view --web
```

---

## PR Body Template

Standard format for DevFlow:

```markdown
Fixes [ISSUE-KEY]

## Summary
[1-3 sentences describing what was done]

## Changes
- [File/component]: [What changed]
- [File/component]: [What changed]

## Validation
[How the changes were tested]
- Tests: [X passed, Y failed]
- Coverage: [Z%] (if applicable)

## Related
- JIRA: [link]
- Docs: [link if applicable]
```

---

## Branch Naming Convention

Recommended format:
```
[type]/[ISSUE-KEY]-[short-description]
```

Examples:
- `feature/PROJ-123-add-user-auth`
- `fix/PROJ-456-login-redirect`
- `refactor/PROJ-789-cleanup-utils`

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| "not a git repository" | Not in git repo | cd to repo root |
| "authentication required" | Not logged in | `gh auth login` |
| "no upstream branch" | Branch not pushed | `git push -u origin branch` |
| "merge conflicts" | Conflicts exist | Resolve conflicts first |

---

## Integration with DevFlow

### complete-issue Command

1. Run validation (tests)
2. Analyze changes with `git diff`
3. Create PR with `gh pr create`
4. Return PR URL

### post-merge Command

1. Switch to main: `git checkout main`
2. Pull changes: `git pull`
3. Delete local branch: `git branch -d feature-branch`
4. Delete remote branch: `git push origin --delete feature-branch`
