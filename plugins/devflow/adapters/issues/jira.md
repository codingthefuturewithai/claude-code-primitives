# Jira Issue Adapter

## Overview

Adapter patterns for Jira issue operations via Atlassian MCP.

---

## Connection Setup

### Get Cloud ID (Required for all operations)

```
Call mcp__atlassian__getAccessibleAtlassianResources
```

Returns:
```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "name": "Your Site Name",
  "url": "https://yoursite.atlassian.net"
}
```

Store the `id` as `cloudId` for subsequent calls.

---

## Operations

### Fetch Issue

```
Call mcp__atlassian__getJiraIssue with:
  - cloudId: [from getAccessibleAtlassianResources]
  - issueKey: "PROJ-123"
```

**Response fields:**
- `key` - Issue key (PROJ-123)
- `fields.summary` - Title
- `fields.description` - Description (ADF format)
- `fields.issuetype.name` - Bug, Task, Story, etc.
- `fields.status.name` - Current status
- `fields.priority.name` - Priority level
- `fields.assignee.displayName` - Assigned user
- `fields.reporter.displayName` - Reporter
- `fields.labels` - Array of labels
- `fields.customfield_*` - Custom fields

---

### Create Issue

```
Call mcp__atlassian__createJiraIssue with:
  - cloudId: [cloudId]
  - projectKey: "PROJ"
  - issueType: "Bug" | "Task" | "Story" | etc.
  - summary: "Issue title"
  - description: "Description text"
```

Optional fields:
- `priority` - Priority name
- `labels` - Array of labels
- `assignee` - Atlassian account ID

---

### Update Issue

```
Call mcp__atlassian__editJiraIssue with:
  - cloudId: [cloudId]
  - issueKey: "PROJ-123"
  - summary: "Updated title" (optional)
  - description: "Updated description" (optional)
```

---

### Transition Issue

**Step 1: Get available transitions**
```
Call mcp__atlassian__getTransitionsForJiraIssue with:
  - cloudId: [cloudId]
  - issueKey: "PROJ-123"
```

Returns array of transitions:
```json
{
  "transitions": [
    {"id": "21", "name": "In Progress"},
    {"id": "31", "name": "Done"}
  ]
}
```

**Step 2: Execute transition**
```
Call mcp__atlassian__transitionJiraIssue with:
  - cloudId: [cloudId]
  - issueKey: "PROJ-123"
  - transitionId: "31"
```

**Pattern:** Find transition by destination name, then use its ID.

---

### Add Comment

```
Call mcp__atlassian__addCommentToJiraIssue with:
  - cloudId: [cloudId]
  - issueKey: "PROJ-123"
  - body: "Comment text"
```

---

### Search Issues (JQL)

```
Call mcp__atlassian__searchJiraIssuesUsingJql with:
  - cloudId: [cloudId]
  - jql: "project = PROJ AND status = 'In Progress'"
```

Common JQL patterns:
- `project = PROJ` - All issues in project
- `assignee = currentUser()` - My issues
- `status = "To Do"` - By status
- `labels = "devflow"` - By label
- `created >= -7d` - Recent issues

---

## Status Mapping

Jira uses workflow-specific status names. Common mappings:

| DevFlow Status | Typical Jira Status |
|----------------|---------------------|
| todo | "To Do", "Open", "Backlog" |
| in_progress | "In Progress", "In Development" |
| review | "In Review", "Code Review" |
| done | "Done", "Closed", "Resolved" |

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | Authentication failed | Check API token |
| 403 | Permission denied | Check user permissions |
| 404 | Issue not found | Verify issue key |
| 400 | Invalid transition | Check available transitions first |
