# DevFlow Test Environment - Setup Complete

## Overview

A local test environment replicating a client's infrastructure (GitLab CE + Google Workspace) has been successfully set up to prototype AI-native DevFlow adaptations. This replaces the original Jira/Confluence/GitHub stack with GitLab/Google Workspace equivalents.

**Setup Date:** 2026-02-03
**Location:** `/Users/timkitchens/projects/client-repos/gitlab-test`

---

## MCP Servers Configured

### 1. GitLab MCP (`@zereight/mcp-gitlab`)

**Purpose:** Replaces Jira + GitHub functionality

| Config | Value |
|--------|-------|
| API URL | `http://localhost:8929/api/v4` |
| Auth | Personal Access Token (`GITLAB_PERSONAL_ACCESS_TOKEN`) |
| Transport | stdio |
| Features Enabled | Wiki, Milestones, Pipelines |

**Key Tools Available:**
- `list_projects` / `get_project` - Project management
- `create_issue` / `update_issue` / `get_issue` - Issue tracking (replaces Jira)
- `create_note` / `create_issue_note` - Comments
- `get_file_contents` - Repository file access
- `create_merge_request` / `update_merge_request` - Code review (replaces GitHub PRs)
- `list_labels` / `create_label` - Label management (replaces Jira issue types)

### 2. Google Workspace MCP (`taylorwilsdon/google_workspace_mcp`)

**Purpose:** Replaces Confluence functionality

| Config | Value |
|--------|-------|
| Server URL | `http://localhost:8847` |
| Auth | OAuth 2.0 (Desktop app) |
| Authenticated User | `codingthefuturewithai@gmail.com` |
| Transport | streamable-http |

**Key Tools Available:**
- `list_drive_items` / `search_drive_files` - File discovery (replaces Confluence spaces)
- `create_doc` / `get_doc_content` - Document creation/reading
- `modify_doc_text` / `find_and_replace_doc` - Document editing
- `search_docs` - Document search (replaces Confluence CQL)
- `list_gmail_labels` / `search_gmail_messages` - Gmail integration
- `read_sheet_values` / `modify_sheet_values` - Google Sheets

---

## Infrastructure Details

### GitLab CE (Docker)

| Component | Value |
|-----------|-------|
| Container | `gitlab-ce` |
| Image | `gitlab/gitlab-ce:latest` |
| HTTP URL | `http://localhost:8929` |
| SSH Port | `2224` |
| Admin User | `root` |
| Test Project | `root/mcp-cookie-cutter` (ID: 1) |

**Docker Compose Location:** `/Users/timkitchens/projects/client-repos/gitlab-test/docker-compose.yml`

### Google Workspace MCP (Docker)

| Component | Value |
|-----------|-------|
| Container | `gws_mcp` |
| Port | `8847` |
| OAuth Client Type | Desktop application |
| Credentials Location | `/Users/timkitchens/google_workspace_mcp/.env` |

**Docker Compose Location:** `/Users/timkitchens/google_workspace_mcp/docker-compose.yml`

---

## Validation Tests Completed

### GitLab MCP Tests (All Passed)

| Test | Result | Details |
|------|--------|---------|
| List projects | PASS | Found `root/mcp-cookie-cutter` |
| Get project details | PASS | Full metadata retrieved |
| Create issue | PASS | Issue #3 created with labels |
| Add comment | PASS | Note added via `create_note` |
| Update issue | PASS | State changed (open/close) |
| Read file | PASS | README.md (6121 bytes) retrieved |

### Google Workspace MCP Tests (All Passed)

| Test | Result | Details |
|------|--------|---------|
| List Drive files | PASS | 5 items found |
| List Gmail labels | PASS | 17 labels found |
| Create document | PASS | Doc ID: `1v9CWth_AiUPhqO6Wj-uIJrD1fZU9SGi8-QRyHNScGro` |
| Read document | PASS | Content retrieved |
| Update document | PASS | Find/replace worked |
| Search documents | PASS | Query returned results |

### End-to-End Workflow Test (Passed)

Simulated DevFlow-style workflow:
1. PASS - Created GitLab issue
2. PASS - Created linked Google Doc
3. PASS - Verified both exist
4. PASS - Updated issue description with Google Doc link
5. PASS - Closed issue with completion comment

---

## DevFlow Adaptation Mapping

### Jira to GitLab Mapping

| DevFlow Operation | Jira Tool | GitLab Equivalent |
|-------------------|-----------|-------------------|
| Fetch issue | `getJiraIssue` | `get_issue` |
| Create issue | `createJiraIssue` | `create_issue` |
| Edit issue | `editJiraIssue` | `update_issue` |
| Add comment | `addCommentToJiraIssue` | `create_note` |
| Transition issue | `transitionJiraIssue` | `update_issue` (state_event) |
| Search issues | `searchJiraIssuesUsingJql` | `list_issues` (filters) |
| Create PR | `gh pr create` | `create_merge_request` |

### Confluence to Google Docs Mapping

| DevFlow Operation | Confluence Tool | Google Workspace Equivalent |
|-------------------|-----------------|----------------------------|
| Get page | `getConfluencePage` | `get_doc_content` |
| Update page | `updateConfluencePage` | `modify_doc_text` |
| Create page | `createConfluencePage` | `create_doc` |
| Search | `searchConfluenceUsingCql` | `search_docs` |
| List spaces | `getConfluenceSpaces` | `list_drive_items` (folders) |

### Conceptual Adaptations Required

1. **Issue Types to Labels**: Use label convention `type::feature`, `type::bug`, `type::task`
2. **Sprints to Milestones**: Assign issues to milestones instead of sprints
3. **Page Hierarchy to Drive Folders**: Use folder structure `DevFlow/[Project]/[Feature]/`
4. **Issue to Doc Linking**: Store Google Doc URLs in GitLab issue descriptions

---

## Environment Variables Required

```bash
# GitLab
export GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
export GITLAB_API_URL="http://localhost:8929/api/v4"

# Google Workspace
export GOOGLE_OAUTH_CLIENT_ID="424974618247-xxxxx.apps.googleusercontent.com"
export GOOGLE_OAUTH_CLIENT_SECRET="GOCSPX-xxxxx"
export WORKSPACE_MCP_PORT="8847"
export GOOGLE_OAUTH_REDIRECT_URI="http://localhost:8847/oauth2callback"
```

---

## Quick Start Commands

```bash
# Start GitLab
cd /Users/timkitchens/projects/client-repos/gitlab-test
docker compose up -d

# Start Google Workspace MCP
cd /Users/timkitchens/google_workspace_mcp
docker compose up -d

# Verify both running
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## Key URLs

- **GitLab UI:** http://localhost:8929
- **GitLab API:** http://localhost:8929/api/v4
- **Google Workspace MCP:** http://localhost:8847
- **Test Project:** http://localhost:8929/root/mcp-cookie-cutter
- **Test Google Doc:** https://docs.google.com/document/d/1v9CWth_AiUPhqO6Wj-uIJrD1fZU9SGi8-QRyHNScGro/edit

---

## Status: READY FOR DEVFLOW ADAPTATION

All infrastructure is operational. Both MCP servers are connected and validated. The environment supports the full DevFlow workflow pattern of issue management + documentation linking.
