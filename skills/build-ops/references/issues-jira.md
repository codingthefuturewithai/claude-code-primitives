# Jira Issue Operations

## Connection Setup

### Get Cloud ID

Call `mcp__atlassian__getAccessibleAtlassianResources` (no parameters needed).

Returns available Atlassian instances. Extract:
- `id` → use as `cloudId` [FROM: this response OR config `cloudId`. NEVER fabricate.]

If config has `cloudId`, use that directly. If not, call this and store the result.

---

## Operations

### Fetch Issue

Call `mcp__atlassian__getJiraIssue` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - issueIdOrKey: [FROM: user input `$ARGUMENTS`. NEVER construct from other data.]

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

---

### Create Issue

Call `mcp__atlassian__createJiraIssue` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - projectKey: [FROM: `getVisibleJiraProjects` response + user selection. NEVER guess.]
  - issueType: [FROM: `getJiraProjectIssueTypesMetadata` response + user selection. NEVER guess.]
  - summary: [FROM: user input. NEVER fabricate.]
  - description: [FROM: user input or generated content. OK to construct.]

Optional fields (only include if user provides):
- priority: [FROM: user input]
- labels: [FROM: user input]
- assignee: [FROM: `lookupJiraAccountId` response. NEVER guess account IDs.]

---

### Update Issue

Call `mcp__atlassian__editJiraIssue` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - issueKey: [FROM: user input `$ARGUMENTS`. NEVER construct.]
  - summary: [FROM: user input] (optional)
  - description: [FROM: user input or generated content] (optional)

---

### Transition Issue

**Step 1: Get available transitions**

Call `mcp__atlassian__getTransitionsForJiraIssue` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - issueKey: [FROM: user input `$ARGUMENTS`. NEVER construct.]

Returns array of transitions with `id` and `name`.

**Step 2: Execute transition**

Call `mcp__atlassian__transitionJiraIssue` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - issueKey: [FROM: user input `$ARGUMENTS`. NEVER construct.]
  - transitionId: [FROM: `getTransitionsForJiraIssue` response. Find by `to.name` matching desired state. NEVER hardcode.]

**Pattern:** Find transition by destination name (e.g., "In Progress", "Done"), then use its `id`.

---

### Add Comment

Call `mcp__atlassian__addCommentToJiraIssue` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - issueKey: [FROM: user input `$ARGUMENTS`. NEVER construct.]
  - body: [FROM: generated content. OK to construct.]

---

### Search Issues (JQL)

Call `mcp__atlassian__searchJiraIssuesUsingJql` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - jql: [FROM: constructed query based on user request. OK to construct - this is a search query, not an identifier.]

Common JQL patterns:
- `project = PROJ` - All issues in project
- `assignee = currentUser()` - My issues
- `status = "To Do"` - By status
- `labels = "devflow"` - By label

---

### Project Discovery

Call `mcp__atlassian__getVisibleJiraProjects` (no parameters needed besides cloudId).

With:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]

Returns list of projects. Present to user for selection.

Call `mcp__atlassian__getJiraProjectIssueTypesMetadata` with:
  - cloudId: [FROM: config `cloudId` OR `getAccessibleAtlassianResources` response. NEVER fabricate.]
  - projectKey: [FROM: `getVisibleJiraProjects` response + user selection. NEVER guess.]

Returns available issue types for the project.

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

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| cloudId | Config `cloudId` OR `getAccessibleAtlassianResources` response | Guess, infer, construct |
| issueKey | User input `$ARGUMENTS` | Construct from other data |
| projectKey | `getVisibleJiraProjects` + user selection | Guess from issue key prefix |
| transitionId | `getTransitionsForJiraIssue` response | Hardcode or guess |
| assignee (accountId) | `lookupJiraAccountId` response | Guess, use email directly |
| issueType | `getJiraProjectIssueTypesMetadata` + user selection | Assume type names |
