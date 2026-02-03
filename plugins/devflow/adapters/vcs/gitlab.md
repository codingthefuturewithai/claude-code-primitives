# GitLab VCS Adapter

## Overview

Adapter patterns for GitLab merge request operations via GitLab MCP.

---

## Operations

### Create Merge Request

```
Call mcp__gitlab__create_merge_request with:
  - project_id: "my-group/my-project"
  - source_branch: "feature/issue-123-description"
  - target_branch: "main"
  - title: "[#123]: Summary"
  - description: "MR description"
```

**Optional parameters:**
- `assignee_id` - User ID to assign
- `reviewer_ids` - Array of reviewer user IDs
- `labels` - Comma-separated label names
- `milestone_id` - Milestone ID
- `remove_source_branch` - true/false (delete branch on merge)
- `squash` - true/false (squash commits)

---

### Get Merge Request

```
Call mcp__gitlab__get_merge_request with:
  - project_id: "my-group/my-project"
  - merge_request_iid: 42
```

**Response fields:**
- `iid` - MR number within project
- `title` - MR title
- `description` - MR description
- `state` - "opened", "merged", "closed"
- `source_branch` - Source branch name
- `target_branch` - Target branch name
- `web_url` - Browser link
- `merge_status` - "can_be_merged", "cannot_be_merged", etc.

---

### Update Merge Request

```
Call mcp__gitlab__update_merge_request with:
  - project_id: "my-group/my-project"
  - merge_request_iid: 42
  - title: "Updated title" (optional)
  - description: "Updated description" (optional)
  - state_event: "close" | "reopen" (optional)
```

---

### List Merge Requests

```
Call mcp__gitlab__list_merge_requests with:
  - project_id: "my-group/my-project"
  - state: "opened" | "merged" | "closed" | "all"
```

---

### Add Comment to MR

```
Call mcp__gitlab__create_note with:
  - project_id: "my-group/my-project"
  - merge_request_iid: 42
  - body: "Comment text"
```

---

### Merge (Accept) MR

```
Call mcp__gitlab__accept_merge_request with:
  - project_id: "my-group/my-project"
  - merge_request_iid: 42
  - squash: true (optional)
  - should_remove_source_branch: true (optional)
```

---

## MR Description Template

Standard format for DevFlow:

```markdown
Closes #123

## Summary
[1-3 sentences describing what was done]

## Changes
- [File/component]: [What changed]
- [File/component]: [What changed]

## Validation
[How the changes were tested]
- Tests: [X passed, Y failed]
- Pipeline: [status]

## Related
- Issue: #123
- Docs: [link if applicable]
```

**Note:** GitLab uses `Closes #123` to auto-close issues on merge.

---

## Branch Naming Convention

Recommended format:
```
[type]/[issue-id]-[short-description]
```

Examples:
- `feature/123-add-user-auth`
- `fix/456-login-redirect`
- `refactor/789-cleanup-utils`

GitLab can auto-create branches from issues with the "Create branch" button.

---

## Key Differences from GitHub PRs

| Aspect | GitHub PR | GitLab MR |
|--------|-----------|-----------|
| Name | Pull Request | Merge Request |
| ID | PR number | MR iid |
| Auto-close | "Fixes #123" | "Closes #123" |
| Creation | `gh pr create` | MCP tool call |
| Draft | `--draft` flag | `draft: true` parameter |
| Squash | Merge option | `squash` parameter |

---

## Branch Operations via Git

Push branch:
```bash
git checkout -b feature/123-description
git push -u origin feature/123-description
```

Delete after merge:
```bash
git checkout main
git pull
git branch -d feature/123-description
git push origin --delete feature/123-description
```

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | Token invalid | Check/regenerate PAT |
| 403 | Insufficient permissions | Check token scopes |
| 404 | Project/MR not found | Verify IDs |
| 409 | Cannot merge | Check merge status, resolve conflicts |

---

## Integration with DevFlow

### complete-issue Command (GitLab mode)

1. Run validation (tests)
2. Analyze changes with `git diff`
3. Create MR via `mcp__gitlab__create_merge_request`
4. Close issue via `mcp__gitlab__update_issue` (state_event: close)
5. Return MR URL

### post-merge Command

1. Switch to main: `git checkout main`
2. Pull changes: `git pull`
3. Delete local branch: `git branch -d feature-branch`
4. Delete remote (if not auto-deleted): `git push origin --delete feature-branch`
