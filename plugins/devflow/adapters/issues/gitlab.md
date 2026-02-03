# GitLab Issue Adapter

## Overview

Adapter patterns for GitLab issue operations via GitLab MCP.

---

## Connection Setup

No cloud ID needed. Operations use `project_id` directly.

### Find Project ID

```
Call mcp__gitlab__list_projects
```

Or derive from project path:
- Project path: `my-group/my-project`
- URL-encoded: `my-group%2Fmy-project`

---

## Operations

### Fetch Issue

```
Call mcp__gitlab__get_issue with:
  - project_id: "my-group/my-project" (or numeric ID)
  - issue_iid: 123
```

**Note:** GitLab uses `iid` (internal ID per project), not `id` (global ID).

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

```
Call mcp__gitlab__create_issue with:
  - project_id: "my-group/my-project"
  - title: "Issue title"
  - description: "Description text"
```

Optional fields:
- `labels` - Comma-separated label names
- `assignee_ids` - Array of user IDs
- `milestone_id` - Milestone ID

---

### Update Issue

```
Call mcp__gitlab__update_issue with:
  - project_id: "my-group/my-project"
  - issue_iid: 123
  - title: "Updated title" (optional)
  - description: "Updated description" (optional)
  - state_event: "close" | "reopen" (optional)
  - labels: "label1,label2" (optional)
```

---

### Transition Issue (Close/Reopen)

GitLab uses simple states. To "transition":

**Close issue:**
```
Call mcp__gitlab__update_issue with:
  - project_id: "my-group/my-project"
  - issue_iid: 123
  - state_event: "close"
```

**Reopen issue:**
```
Call mcp__gitlab__update_issue with:
  - project_id: "my-group/my-project"
  - issue_iid: 123
  - state_event: "reopen"
```

**Workflow states via labels:**

GitLab doesn't have built-in workflow states like Jira. Use labels instead:
- Add label: `labels: "existing-label,In Progress"`
- Remove label: Update with labels excluding the one to remove

---

### Add Comment (Note)

```
Call mcp__gitlab__create_note with:
  - project_id: "my-group/my-project"
  - issue_iid: 123
  - body: "Comment text"
```

---

### Search Issues

```
Call mcp__gitlab__list_issues with:
  - project_id: "my-group/my-project" (optional, omit for all)
  - state: "opened" | "closed" | "all"
  - labels: "bug,urgent"
  - search: "search term"
```

Or use global search across all projects:
```
Call mcp__gitlab__search with:
  - search: "search term"
  - scope: "issues"
```

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

## Key Differences from Jira

| Aspect | Jira | GitLab |
|--------|------|--------|
| Issue ID | Key (PROJ-123) | IID (123 per project) |
| Workflow | Complex transitions | Simple open/closed |
| Custom states | Built-in | Use labels |
| Project ref | Cloud ID + key | Project path or ID |
| Epics | Issue type | Separate endpoint |

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | Token invalid/expired | Regenerate PAT |
| 403 | Insufficient permissions | Check token scopes |
| 404 | Project/issue not found | Verify project_id and iid |
