---
name: devflow:build:fetch-issue
description: Fetch issue and analyze feasibility. Use this when the user wants to start working on a Jira issue, GitLab issue, or GitHub issue.
argument-hint: "[ISSUE-KEY, GitLab issue number, or GitHub issue number]"
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Grep
  - Glob
  - Read
  - Bash
  - mcp__atlassian__getJiraIssue
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__gitlab__get_issue
  - mcp__gitlab__list_projects
---

# Fetch Issue & Analyze Feasibility

I'll fetch the issue and analyze if the work is already done or conflicts exist.

Issue: $ARGUMENTS

---

## Step 1: Load Configuration and Fetch Issue

Use the **build-ops** skill to:
1. Load backend configuration from `devflow-config.md`
2. Fetch issue $ARGUMENTS from the configured issue tracker

The build-ops skill handles all backend-specific operations (Jira, GitLab, GitHub)
and enforces parameter validation. See `skills/build-ops/SKILL.md`.

Store the returned issue details for use in subsequent steps.

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
/devflow:build:plan-issue $ARGUMENTS
```

**OR** with Test-Driven Development:
```
/devflow:build:plan-issue --tdd $ARGUMENTS
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
