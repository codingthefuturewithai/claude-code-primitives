---
name: devflow:build-ops
description: Backend operations for issue tracking (Jira, GitLab, GitHub) and VCS (GitHub PRs, GitLab MRs). Handles config loading, parameter validation, and MCP tool calls for build workflow commands.
user-invocable: false
---

# Build Operations

Backend operations dispatcher for issue tracking and VCS.

**Say exactly:** "SKILL INVOKED: build-ops"

---

## Section 1: Config Loading (MANDATORY)

Load DevFlow configuration to determine backends and extract parameters.

**Step 1: Find config file**

1. Check `.claude/devflow-config.md` (project-level)
2. Check `~/.claude/devflow-config.md` (global-level)
3. If neither exists → STOP. Say: "No DevFlow config found. Run `/devflow:admin:setup` to configure backends."

**Step 2: Parse config and extract values**

Read the config file and extract ALL of the following:

| Variable | Config Key | Required For |
|----------|-----------|--------------|
| ISSUES_BACKEND | `issues.backend` | Issue operations (jira, gitlab, github, none) |
| ISSUES_ENABLED | `issues.enabled` | Whether issues are active |
| VCS_BACKEND | `vcs.backend` | PR/MR operations (github, gitlab) |
| CLOUD_ID | `cloudId` | Jira/Confluence calls |
| DEFAULT_PROJECT | `default_project` | GitLab calls |
| GOOGLE_EMAIL | `google_email` | Google Workspace calls |

Store ALL extracted values for downstream use. Do NOT discard any.

---

## Section 2: Parameter Validation Gate (MANDATORY)

**Before ANY MCP tool call or CLI command in this skill, validate EVERY parameter.**

For EVERY parameter on EVERY call, verify where the value came from:

| Source | Allowed? | Action |
|--------|----------|--------|
| Value read from `devflow-config.md` in this session | **YES** | Use it |
| Value returned from a PREVIOUS call to the SAME backend's MCP server | **YES** | Use it |
| Value provided by the user in this conversation | **YES** | Use it |
| Value from a DIFFERENT backend's MCP server or CLI | **NO** | STOP. Backends are isolated. Say: "I cannot use [value] from [source backend] for [target backend]. These backends are completely independent." |
| Value that "looks right" or was inferred | **NO** | STOP. Say: "I need the actual [parameter name]. Where should I get this value?" |
| Anything else | **UNKNOWN** | ASK the user. Do not proceed without a verified value. |

### Backend Isolation Rules

Identifiers NEVER cross backend boundaries:

- Atlassian IDs/emails → Atlassian calls ONLY
- GitLab project IDs/user IDs → GitLab calls ONLY
- GitHub repo/issue refs → GitHub calls ONLY
- Google email/doc IDs → Google Workspace calls ONLY
- RAG Memory collection names → RAG Memory calls ONLY

Content (titles, descriptions, text) CAN flow between backends. Identifiers CANNOT.

### Critical Parameters

| Parameter | ONLY Source | NEVER |
|-----------|-----------|-------|
| cloudId | Config `cloudId` OR `getAccessibleAtlassianResources` response | Guess, infer, construct |
| issueKey | User input `$ARGUMENTS` | Construct from other data |
| project_id | Config `default_project` OR `list_projects` + user selection | Guess from repo name |
| user_google_email | Config `google_email`. If missing, ASK user | Infer from Atlassian, GitLab, domain names |
| transitionId | `getTransitionsForJiraIssue` response | Hardcode or guess |

---

## Section 3: Operation Routing

Route to the correct reference file based on config and requested operation.

### Issue Operations

| Requested Operation | Config Match | Reference |
|---------------------|-------------|-----------|
| Fetch, search, or view issue | `ISSUES_BACKEND = "jira"` | [references/issues-jira.md](references/issues-jira.md) |
| Fetch, search, or view issue | `ISSUES_BACKEND = "gitlab"` | [references/issues-gitlab.md](references/issues-gitlab.md) |
| Fetch, search, or view issue | `ISSUES_BACKEND = "github"` | [references/issues-github.md](references/issues-github.md) |
| Create issue | `ISSUES_BACKEND = "jira"` | [references/issues-jira.md](references/issues-jira.md) |
| Create issue | `ISSUES_BACKEND = "gitlab"` | [references/issues-gitlab.md](references/issues-gitlab.md) |
| Create issue | `ISSUES_BACKEND = "github"` | [references/issues-github.md](references/issues-github.md) |
| Update or transition issue | `ISSUES_BACKEND = "jira"` | [references/issues-jira.md](references/issues-jira.md) |
| Update or transition issue | `ISSUES_BACKEND = "gitlab"` | [references/issues-gitlab.md](references/issues-gitlab.md) |
| Close issue | `ISSUES_BACKEND = "github"` | [references/issues-github.md](references/issues-github.md) |
| Any issue operation | `ISSUES_BACKEND = "none"` | Skip. Say: "Issue tracking disabled. No external tracker configured." |

### VCS Operations

| Requested Operation | Config Match | Reference |
|---------------------|-------------|-----------|
| Create PR, view PR, link issue | `VCS_BACKEND = "github"` | [references/vcs-github.md](references/vcs-github.md) |
| Create MR, view MR, link issue | `VCS_BACKEND = "gitlab"` | [references/vcs-gitlab.md](references/vcs-gitlab.md) |

### Project Discovery

| Requested Operation | Config Match | Reference |
|---------------------|-------------|-----------|
| List/select Jira projects | `ISSUES_BACKEND = "jira"` | [references/issues-jira.md](references/issues-jira.md) § Project Discovery |
| List/select GitLab projects | `ISSUES_BACKEND = "gitlab"` | [references/issues-gitlab.md](references/issues-gitlab.md) § Project Discovery |
| Get current GitHub repo | `ISSUES_BACKEND = "github"` | [references/issues-github.md](references/issues-github.md) § Repository Context |
