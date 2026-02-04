# GitLab VCS Operations (Merge Requests)

## Operations

### Create Merge Request

Call `mcp__gitlab__create_merge_request` with:
  - project_id: [FROM: config `default_project` OR `list_projects` + user selection. NEVER guess.]
  - source_branch: [FROM: `git branch --show-current`. NEVER guess.]
  - target_branch: [FROM: git context (usually "main" or "master"). Verify with `git remote show origin | grep 'HEAD branch'`.]
  - title: [FROM: issue key + issue title from tracker response. NEVER fabricate.]
  - description: [FROM: generated from change analysis. OK to construct.]

**Optional parameters (only include if user provides):**
- assignee_id: [FROM: GitLab API user lookup. NEVER guess user IDs.]
- reviewer_ids: [FROM: GitLab API user lookup. NEVER guess.]
- labels: [FROM: user input. Comma-separated.]
- milestone_id: [FROM: GitLab API milestone lookup. NEVER guess.]
- remove_source_branch: true/false [FROM: user preference or default true]
- squash: true/false [FROM: user preference]

---

### Get Merge Request

Call `mcp__gitlab__get_merge_request` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - merge_request_iid: [FROM: `create_merge_request` response or user input. NEVER guess.]

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

Call `mcp__gitlab__update_merge_request` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - merge_request_iid: [FROM: `create_merge_request` response or user input. NEVER guess.]
  - title: [FROM: user input] (optional)
  - description: [FROM: user input or generated] (optional)
  - state_event: "close" | "reopen" [FROM: user request] (optional)

---

### List Merge Requests

Call `mcp__gitlab__list_merge_requests` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - state: "opened" | "merged" | "closed" | "all" [FROM: user request]

---

### Add Comment to MR

Call `mcp__gitlab__create_note` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - merge_request_iid: [FROM: `create_merge_request` response or user input. NEVER guess.]
  - body: [FROM: generated content. OK to construct.]

---

### Accept (Merge) MR

Call `mcp__gitlab__accept_merge_request` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - merge_request_iid: [FROM: `create_merge_request` response or user input. NEVER guess.]
  - squash: true [FROM: user preference] (optional)
  - should_remove_source_branch: true [FROM: user preference] (optional)

---

## MR Description Template

Standard format for DevFlow:

```markdown
Closes #[IID]

## Summary
[1-3 sentences describing what was done]

## Changes
- [File/component]: [What changed]

## Validation
[How the changes were tested]
- Tests: [X passed, Y failed]
- Pipeline: [status]

## Related
- Issue: #[IID]
- Docs: [link if applicable]
```

**Note:** GitLab uses `Closes #[IID]` to auto-close issues on merge.
- `[IID]`: [FROM: user input `$ARGUMENTS`. NEVER construct.]

---

## Branch Operations

**Create branch:**
```bash
git checkout -b [BRANCH_NAME]
git push -u origin [BRANCH_NAME]
```

- `[BRANCH_NAME]`: [FROM: constructed from issue ID + description slug. OK to construct from user input.]

Branch naming convention:
- Feature: `feature/[issue-id]-[slug]`
- Bug fix: `fix/[issue-id]-[slug]`
- Other: `refactor/[issue-id]-[slug]`

**Delete after merge:**
```bash
git checkout main
git pull
git branch -d [BRANCH_NAME]
git push origin --delete [BRANCH_NAME]
```

- `[BRANCH_NAME]`: [FROM: `git branch --show-current` before switching. NEVER guess.]

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | Token invalid | Check/regenerate PAT |
| 403 | Insufficient permissions | Check token scopes |
| 404 | Project/MR not found | Verify IDs |
| 409 | Cannot merge | Check merge status, resolve conflicts |

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| project_id | Config `default_project` OR `list_projects` + user selection | Guess from repo name |
| source_branch | `git branch --show-current` | Guess |
| target_branch | Git context (verify with remote) | Assume without checking |
| merge_request_iid | `create_merge_request` response or user input | Fabricate |
| assignee_id | GitLab API user lookup | Guess user IDs |
| reviewer_ids | GitLab API user lookup | Guess |
| MR title | Issue key (user input) + issue title (tracker response) | Fabricate |
