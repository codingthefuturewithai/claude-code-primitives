---
description: Fetch issue and analyze feasibility
argument-hint: "[ISSUE-KEY or GitLab issue number]"
allowed-tools: [
  "Grep", "Glob", "Read", "Bash",
  "mcp__atlassian__getJiraIssue", "mcp__atlassian__getAccessibleAtlassianResources",
  "mcp__gitlab__get_issue", "mcp__gitlab__list_projects"
]
---

# Fetch Issue & Analyze Feasibility

I'll fetch the issue and analyze if the work is already done or conflicts exist.

Issue: $ARGUMENTS

---

## Step 0: Load Backend Configuration

## Note for AI Assistants - CONFIG LOADING

1. Check for config file:
   ```bash
   if [ -f ".claude/devflow-config.md" ]; then
     CONFIG_PATH=".claude/devflow-config.md"
   elif [ -f "$HOME/.claude/devflow-config.md" ]; then
     CONFIG_PATH="$HOME/.claude/devflow-config.md"
   else
     CONFIG_PATH=""
   fi
   ```

2. **If config exists:** Read and parse:
   - Extract `issues.backend` (jira, gitlab, or none)
   - Extract `issues.enabled` (true/false)
   - For Jira: Extract `cloudId` if saved
   - For GitLab: Extract `default_project` if saved

3. **If no config exists:**
   - Default to Atlassian/Jira (backwards compatible)
   - Suggest: "Tip: Run /devflow:admin:setup to configure backends"

4. Store ISSUES_BACKEND for use in Step 1

**Backend determines adapter to use:**
- `jira` → Follow patterns in `adapters/issues/jira.md`
- `gitlab` → Follow patterns in `adapters/issues/gitlab.md`
- `none` → Skip issue fetch, proceed with local analysis only

---

## Step 1: Fetch Issue from Issue Tracker

[If ISSUES_BACKEND = "jira"]:

**Using Jira via Atlassian MCP**

[Call `mcp__atlassian__getAccessibleAtlassianResources`]
[Call `mcp__atlassian__getJiraIssue` with cloudId and issue key]

---

[If ISSUES_BACKEND = "gitlab"]:

**Using GitLab Issues via GitLab MCP**

[Call `mcp__gitlab__get_issue` with project_id and issue_iid]

**Note:** GitLab uses `iid` (project-specific issue number).
If $ARGUMENTS is just a number (e.g., "123"), use it as iid.
If $ARGUMENTS includes project (e.g., "my-project/123"), parse accordingly.

---

[If ISSUES_BACKEND = "none"]:

**Issue tracking disabled**

No external issue tracker configured. Proceeding with local codebase analysis.

---

**Issue Summary:**
- **Type**: [Bug/Feature/Task/etc.]
- **Summary**: [Title]
- **Priority**: [Priority]
- **Status**: [Current status]

**Requirements:**
[Key acceptance criteria and objectives]

---

## Step 2: Analyze Feasibility

Searching codebase to determine if work is already done...

**Search Strategy:**
- Grep for keywords from issue title and description
- Grep for function/class/component names mentioned
- Glob for related file structures
- Read relevant files to understand existing implementation
- Check recent git history for related changes

**Feasibility Assessment:**

[Provide one of these outcomes]:

✅ **Not Implemented**
- No existing implementation found
- Related patterns discovered: [list file paths if any]
- Ready to proceed

🔄 **Partially Implemented**
- Found: [what exists with file paths]
- Missing: [what still needs to be done]
- Recommend: [approach to complete]

❌ **Fully Implemented**
- Evidence: [file paths and functionality description]
- Recommend: Close or repurpose issue

⚠️ **Conflicts Detected**
- Issue: [architectural concerns or blocking problems]
- Recommend: Discuss with team before proceeding

---

## ⛔ STOP - Decision Point

Based on the feasibility analysis above, decide next steps:

**If ready to proceed:**

Standard workflow:
```
/devflow:build:plan-work $ARGUMENTS
```

**OR** with Test-Driven Development:
```
/devflow:build:plan-work --tdd $ARGUMENTS
```

TDD mode will:
- Detect test framework and existing test patterns
- Map tests to components being modified
- Generate test cases from acceptance criteria
- Guide RED/GREEN/REFACTOR implementation workflow

**If partially done or conflicts exist:**
Discuss approach with team first

**If fully implemented:**
Close or update issue

---

⏸️ **Stopped** - Choose your next step above and run the appropriate command
