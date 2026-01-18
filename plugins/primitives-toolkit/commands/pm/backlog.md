---
description: Manage JIRA backlog from Confluence roadmap - sync candidates, create issues, assign sprints
argument-hint: "[sync|create|sprint] [args...]"
allowed-tools: ["Read", "Glob", "Grep", "AskUserQuestion", "mcp__atlassian__getConfluencePage", "mcp__atlassian__searchJiraIssuesUsingJql", "mcp__atlassian__getJiraIssue", "mcp__atlassian__createJiraIssue", "mcp__atlassian__editJiraIssue", "mcp__atlassian__getVisibleJiraProjects", "mcp__atlassian__getJiraProjectIssueTypesMetadata", "mcp__atlassian__getTransitionsForJiraIssue"]
---

# JIRA Backlog Management

Manage JIRA backlog downstream of Confluence planning. This command operates on **implementation candidates** - items flagged for implementation in Confluence.

**Request:** $ARGUMENTS

---

## System Reference (KB Project)

| Item | Value |
|------|-------|
| Cloud ID | `codingthefuturewithai.atlassian.net` |
| Project Key | `KB` |
| Board ID | `70` |
| Sprint Field | `customfield_10020` |
| Product Roadmap Page | `147652616` |
| Feature Backlog Page | `148242435` |

---

## What is an "Implementation Candidate"?

Items ready for JIRA issue creation:
- Items in **"Ready for JIRA"** table on Product Roadmap (page 147652616)
- **📋 Defined** items in Feature Backlog (page 148242435)

**Ignored:** Items in "Exploring" table, "Future Vision" list, or 💡 Idea / 🔍 Exploring status (not ready for JIRA)

---

## Step 1: Parse Arguments & Route

**Parse $ARGUMENTS to determine mode:**

- No arguments OR empty → **Interactive Menu**
- `sync` → **Sync Mode**
- `create [item]` → **Create Mode**
- `sprint [issue]` → **Sprint Mode**

---

## Interactive Menu (No Arguments)

If no arguments provided, present menu:

Say: "What would you like to do?"

Options:
1. **Sync** - Find implementation candidates without JIRA issues
2. **Create** - Create a JIRA issue from a candidate or ad-hoc
3. **Sprint** - Add an issue to a sprint

Ask using AskUserQuestion. Then route to appropriate mode below.

---

## Sync Mode (`/backlog sync`)

**Purpose:** Find implementation candidates WITHOUT JIRA issues

### Step S1: Fetch Implementation Candidates from Confluence

**From Feature Backlog:**
```
[Call mcp__atlassian__getConfluencePage cloudId="codingthefuturewithai.atlassian.net" pageId="148242435"]
```

Parse the markdown content:
- Find items with "📋" prefix (Defined status)
- **Ignore:** Items with 💡 Idea or 🔍 Exploring status

---

**From Product Roadmap:**
```
[Call mcp__atlassian__getConfluencePage cloudId="codingthefuturewithai.atlassian.net" pageId="147652616"]
```

Parse the markdown content:
- Find items in **"Ready for JIRA"** table (these have decisions made, requirements clear)
- **Ignore:** "Exploring" table (not ready), "Future Vision" list (long-term only)

Store all candidates as `implementation_candidates` list.

---

### Step S2: Fetch KB Issues from JIRA

```
[Call mcp__atlassian__searchJiraIssuesUsingJql cloudId="codingthefuturewithai.atlassian.net" jql="project = KB ORDER BY created DESC"]
```

Get all KB issues with summary, status, sprint.

---

### Step S3: Match Candidates to Issues

For each candidate:
- Search JIRA issues for similar title (case-insensitive, fuzzy match on key words)
- Categorize:
  - ✅ **Has JIRA issue** - Candidate matched to existing issue
  - ❌ **No JIRA issue** - Candidate ready for JIRA issue creation

---

### Step S4: Present Results

```
## Implementation Candidates → JIRA Status

### ✅ Already in JIRA (X items)
- "Authentication" (Roadmap: Ready for JIRA) → KB-12 (In Progress)
- "Community Detection" (Backlog: Defined) → KB-18 (Backlog)

### ❌ Ready for JIRA Issue (Y items)
- "Collection Permissions" (Roadmap: Ready for JIRA)
- "Custom Quality Rubrics" (Backlog: Defined)
```

---

### Step S5: Handle Edge Cases

**If no implementation candidates found:**
Say: "No implementation candidates found. Use `/roadmap` to refine ideas and promote them to 'Ready for JIRA' or 📋 Defined status."
**END**

**If all candidates have JIRA issues:**
Say: "All implementation candidates already have JIRA issues. Nothing to create."
Show the existing matches.
**END**

---

### Step S6: Offer Actions

If items missing JIRA issues:

Ask: "Create JIRA issue for one of these?"
- List each candidate without a JIRA issue (numbered)
- Add option: "Done reviewing"

**WAIT for selection.**

If user selects a candidate → Route to Create Mode with that candidate.
If "Done reviewing" → **END**

---

## Create Mode (`/backlog create [item]`)

**Purpose:** Create JIRA issue from implementation candidate OR ad-hoc

### Step C1: Determine Source

**If `[item]` provided in arguments:**
Use as starting point. Check if it matches a known candidate.

**If no argument:**
Ask: "Create from implementation candidate or new ad-hoc issue?"
1. **From candidate** - I'll show candidates without JIRA issues
2. **Ad-hoc** - Describe what you want to create

**WAIT for selection.**

---

### Step C1a: If From Candidate

Run Sync Steps S1-S3 to get candidates without JIRA issues.

Present numbered list:
```
Which candidate?
1. "Collection Permissions" (Roadmap: Ready for JIRA)
2. "Custom Quality Rubrics" (Backlog: Defined)
```

**WAIT for selection.** Store selected candidate.

---

### Step C1b: If Ad-hoc

Ask: "What's the issue about? (Brief description)"

**WAIT for response.** Store as `description`.

---

### Step C2: Pull Context from Confluence (if from candidate)

The candidate already has structured content in Confluence. Extract:
- Title
- Goal/Description
- Priority (if stated)
- Features list
- Dependencies
- Open Questions

Store this as `confluence_context` for use in JIRA description.

---

### Step C3: Analyze Codebase

Say: "Let me check the codebase for related components..."

```
[Use Grep/Glob to search for keywords from title/description]
[Look in: mcp-server/src/, web-ui/src/, scripts/]
[Identify: related files, existing patterns, integration points]
```

Present findings:
- "Related components: `src/ingestion/...`, `src/retrieval/...`"
- "Existing patterns: [describe if found]"
- "Integration points: [describe if found]"

If nothing found, say: "No directly related code found - this may be a new area."

---

### Step C4: Gather Issue Details (One Question at a Time)

**Question 1 - Issue Type:**

"What type of issue is this?"
1. **Executable Spec** - New feature with acceptance criteria (recommended for candidates)
2. **Bug** - Something broken
3. **Task** - General work item

**WAIT.** Store as `issue_type`.

---

**Question 2 - Priority:**

If priority found in Confluence context, confirm:
"Priority appears to be [X] based on Confluence. Use this? (Yes / Change)"

If not found, ask:
"Priority? (High / Medium / Low)"

**WAIT.** Store as `priority`. Default Medium if unclear.

---

**Question 3 - Summary:**

Suggest title based on candidate title or description:
"Use this summary: '[suggested]' or provide your own?"

**WAIT.** Store as `summary`.

---

### Step C5: Generate Description

**For Executable Spec:**

```markdown
## Background & Goal

[From Confluence context or user description]

## Acceptance Criteria

- [ ] [Capability 1 - from Confluence Features list]
- [ ] [Capability 2]
- [ ] [etc.]

## Technical Guidance

**Codebase Analysis:**
[Findings from Step C3]

**Dependencies:**
[From Confluence context]

**Open Questions:**
[From Confluence context]

## Testing Requirements

- [ ] Unit tests for [components]
- [ ] Integration tests for [flows]
```

---

**For Bug or Task:**

```markdown
## Description

[From user description or Confluence context]

## Technical Context

**Related Components:**
[Findings from Step C3]

## Acceptance Criteria

- [ ] [Expected outcome]
```

---

### Step C6: Preview and Confirm

Show complete preview:

```
## New JIRA Issue Preview

**Project:** KB
**Type:** [issue_type]
**Summary:** [summary]
**Priority:** [priority]

**Description:**
[Full generated description]

Create this issue? (Yes / Edit / Cancel)
```

**⏸️ WAIT for explicit "Yes"**

- **Edit:** Ask what to change, revise, show preview again
- **Cancel:** Stop, do not create
- **Yes:** Proceed to create

---

### Step C7: Create Issue

```
[Call mcp__atlassian__createJiraIssue
  cloudId="codingthefuturewithai.atlassian.net"
  projectKey="KB"
  issueTypeName=[issue_type]
  summary=[summary]
  description=[description]
  priority=[priority]
]
```

Say: "Created KB-XX: [summary]"
Provide URL: `https://codingthefuturewithai.atlassian.net/browse/KB-XX`

---

### Step C8: Sprint or Backlog Decision

Ask: "What's next for KB-XX?"
1. **Add to sprint** - Assign to a sprint now
2. **Leave in backlog** - Done for now

**WAIT for selection.**

- **Add to sprint:** → Route to Sprint Mode with KB-XX
- **Leave in backlog:** Say "KB-XX is in the backlog." **END**

---

## Sprint Mode (`/backlog sprint [issue]`)

**Purpose:** Add issue to sprint

### Step P1: Get Issue

**If `[issue]` provided (e.g., "KB-6"):**
```
[Call mcp__atlassian__getJiraIssue cloudId="codingthefuturewithai.atlassian.net" issueIdOrKey="[issue]"]
```

Validate it exists and belongs to KB project.
Store issue key and summary.

---

**If no argument:**
```
[Call mcp__atlassian__searchJiraIssuesUsingJql
  cloudId="codingthefuturewithai.atlassian.net"
  jql="project = KB AND sprint is EMPTY AND status != Done ORDER BY created DESC"
]
```

Show unassigned issues:
```
Which issue to add to a sprint?
1. KB-12: "Implement Authentication"
2. KB-15: "Graph Visualization"
3. KB-18: "Community Detection"
```

**WAIT for selection.** Store selected issue.

---

### Step P2: Discover Available Sprints

```
[Call mcp__atlassian__searchJiraIssuesUsingJql
  cloudId="codingthefuturewithai.atlassian.net"
  jql="project = KB AND sprint is not EMPTY"
  fields=["summary", "status", "customfield_10020"]
]
```

For each issue in results:
- Extract sprint info from `customfield_10020` field
- Returns: `{id: 239, name: "KB Sprint 1", state: "future", boardId: 70}`
- Deduplicate by sprint ID
- Count issues per sprint

---

**If no sprints found (all issues have empty sprint):**

Say: "No sprints found. Please create a sprint in JIRA and add at least one issue to it, then try again."

**END**

---

### Step P3: Present Sprint Options

```
Which sprint?
1. KB Sprint 1 (future) - 3 issues
2. KB Sprint 2 (active) - 5 issues
```

Show sprint **NAME** (never ID), with state and issue count.

**WAIT for selection.** Store selected sprint (name AND id internally).

---

### Step P4: Confirm Assignment

```
Add KB-XX "[Issue Title]" to "KB Sprint 1"? (Yes / Cancel)
```

**⏸️ WAIT for explicit "Yes"**

---

### Step P5: Assign to Sprint

```
[Call mcp__atlassian__editJiraIssue
  cloudId="codingthefuturewithai.atlassian.net"
  issueIdOrKey="KB-XX"
  fields={"customfield_10020": <sprint_id>}
]
```

Say: "KB-XX added to KB Sprint 1"

**END**

---

## Error Handling

| Scenario | Response |
|----------|----------|
| No implementation candidates | "No implementation candidates found. Use `/roadmap` to refine ideas and promote them to 'Ready for JIRA' or 📋 Defined status." |
| All candidates have JIRA issues | "All implementation candidates already have JIRA issues. Nothing to create." Show existing matches. |
| No KB issues in sprints | "No sprints found. Add an issue to a sprint in JIRA first." |
| Issue not found | "KB-XX not found. Check the issue key." |
| Issue already in sprint | Show current sprint, ask "Move to different sprint?" |
| JIRA auth failed | "Authentication failed. Run /mcp to reconnect." |

---

## Rules

**Always:**
- Only look at "Ready for JIRA" table items + 📋 Defined backlog items (implementation candidates)
- Ignore "Exploring" table, "Future Vision" list, 💡 Idea, 🔍 Exploring items
- Show sprint NAMES, never IDs (IDs are internal)
- One question at a time, wait for response
- Preview before any JIRA write
- Get explicit "Yes" before creating/updating
- Pull Confluence content into JIRA description (don't ask user to re-type)

**Never:**
- Expose sprint IDs to user
- Create issues without approval
- Assume sprint exists without checking
- Skip codebase analysis for create mode
- Create JIRA issues for items not in "Ready for JIRA" or 📋 Defined status
