# GitLab Issue Operations

## Connection Setup

No cloud ID needed. Operations use `project_id` directly.

- project_id: [FROM: config `default_project` OR `list_projects` response + user selection. NEVER guess from repo name.]

---

## Operations

### Fetch Issue

Call `mcp__gitlab__get_issue` with:
  - project_id: [FROM: config `default_project` OR `list_projects` + user selection. NEVER guess.]
  - issue_iid: [FROM: user input `$ARGUMENTS`. NEVER construct.]

**Note:** GitLab uses `iid` (internal ID per project), not `id` (global ID).
If `$ARGUMENTS` is just a number (e.g., "123"), use it as `iid`.
If `$ARGUMENTS` includes project (e.g., "my-project/123"), parse accordingly.

**Response fields:**
- `iid` - Issue number within project
- `title` - Issue title
- `description` - Description (Markdown)
- `state` - "opened" or "closed"
- `labels` - Array of label names
- `assignees` - Array of assigned users
- `author` - Creator
- `milestone` - Associated milestone
- `web_url` - Browser link

---

### Create Issue

Call `mcp__gitlab__create_issue` with:
  - project_id: [FROM: config `default_project` OR `list_projects` + user selection. NEVER guess.]
  - title: [FROM: user input. NEVER fabricate.]
  - description: [FROM: user input or generated content. OK to construct.]

Optional fields (only include if user provides):
- labels: [FROM: user input. Comma-separated label names.]
- assignee_ids: [FROM: GitLab API user lookup. NEVER guess user IDs.]
- milestone_id: [FROM: GitLab API milestone lookup. NEVER guess.]

---

### Update Issue

Call `mcp__gitlab__update_issue` with:
  - project_id: [FROM: config `default_project` OR `list_projects` + user selection. NEVER guess.]
  - issue_iid: [FROM: user input `$ARGUMENTS`. NEVER construct.]
  - title: [FROM: user input] (optional)
  - description: [FROM: user input or generated content] (optional)
  - state_event: "close" | "reopen" [FROM: workflow context] (optional)
  - labels: [FROM: user input or workflow logic] (optional)

---

### Transition Issue (Close/Reopen)

GitLab uses simple states. To "transition":

**Close issue:**

Call `mcp__gitlab__update_issue` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - issue_iid: [FROM: user input `$ARGUMENTS`. NEVER construct.]
  - state_event: "close"

**Reopen issue:**

Call `mcp__gitlab__update_issue` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - issue_iid: [FROM: user input `$ARGUMENTS`. NEVER construct.]
  - state_event: "reopen"

**Workflow states via labels:**

GitLab doesn't have built-in workflow states like Jira. Use labels instead:
- Add label: include all existing labels plus new one in `labels` field
- Remove label: include all existing labels minus the one to remove

---

### Add Comment (Note)

Call `mcp__gitlab__create_note` with:
  - project_id: [FROM: config `default_project`. NEVER guess.]
  - issue_iid: [FROM: user input `$ARGUMENTS`. NEVER construct.]
  - body: [FROM: generated content. OK to construct.]

---

### Search Issues

Call `mcp__gitlab__list_issues` with:
  - project_id: [FROM: config `default_project`. NEVER guess.] (optional - omit for all projects)
  - state: "opened" | "closed" | "all" [FROM: user request]
  - labels: [FROM: user request. Comma-separated.]
  - search: [FROM: user request. Search term - OK to construct.]

---

### Project Discovery

Call `mcp__gitlab__list_projects` (no parameters needed).

Returns list of accessible projects. Present to user for selection. Store selected `project_id`.

---

## Status Mapping

GitLab has simple states. Use labels for workflow:

| DevFlow Status | GitLab State | Suggested Label |
|----------------|--------------|-----------------|
| todo | opened | "To Do" |
| in_progress | opened | "In Progress" |
| review | opened | "In Review" |
| done | closed | (none needed) |

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | Token invalid/expired | Regenerate PAT |
| 403 | Insufficient permissions | Check token scopes |
| 404 | Project/issue not found | Verify project_id and iid |

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| project_id | Config `default_project` OR `list_projects` + user selection | Guess from repo name or URL |
| issue_iid | User input `$ARGUMENTS` | Construct from other data |
| assignee_ids | GitLab API user lookup | Guess user IDs |
| milestone_id | GitLab API milestone lookup | Guess or hardcode |
| labels | User input or workflow logic | Infer from other backends |
