---
description: Final validation, create PR/MR, and mark issue done
argument-hint: "[ISSUE-KEY, GitLab issue number, or GitHub issue number]"
allowed-tools: [
  "Bash", "Read", "Grep", "Glob",
  "mcp__atlassian__getJiraIssue", "mcp__atlassian__getAccessibleAtlassianResources",
  "mcp__atlassian__transitionJiraIssue", "mcp__atlassian__getTransitionsForJiraIssue",
  "mcp__gitlab__get_issue", "mcp__gitlab__update_issue", "mcp__gitlab__create_merge_request"
]
---

# Complete Work

I'll run final validation, create a PR/MR, and update the issue to Done.

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
   - Extract `issues.backend` (jira, gitlab, github, none)
   - Extract `vcs.backend` (github, gitlab)
   - For Jira: Extract `cloudId` if saved
   - For GitLab: Extract `default_project` if saved
   - For GitHub Issues: Uses current repo context

3. **If no config exists:**
   - Default to Jira + GitHub (backwards compatible)
   - Suggest: "Tip: Run /devflow:admin:setup to configure backends"

4. Store:
   - ISSUES_BACKEND for issue updates
   - VCS_BACKEND for PR/MR creation

**Backend determines adapters:**
- Issues: `adapters/issues/jira.md`, `adapters/issues/gitlab.md`, or `adapters/issues/github.md`
- VCS: `adapters/vcs/github.md` or `adapters/vcs/gitlab.md`

---

## 🔒 Recommended Prerequisites

**Security review recommended before running complete:**

If you haven't already, consider running:
```bash
/devflow:build:security-review $ARGUMENTS
```

This is especially important if your changes involve authentication, input validation, database queries, or other security-sensitive code.

**Skip if:**
- You already ran security-review and addressed all findings
- Changes are documentation-only or other low-risk refactoring
- You want to proceed without security analysis

---

## Step 1: Final Validation

**Strategy adapts to work type:**

**For code with tests:**
- Discover test command from project files (package.json, Makefile, README, etc.)
- Check for coverage tools (pytest-cov, coverage.py, jest --coverage, go test -cover, simplecov)
- Run full test suite (with coverage if available)
- Verify all tests pass
- Report coverage summary if available

**For bug fixes:**
- Run affected test suite
- Verify regression test passes
- Confirm bug no longer reproduces

**For infrastructure/config:**
- Trigger validation (build, workflow, deployment dry-run)
- Verify expected behavior
- Check logs/output

**For documentation:**
- Verify accuracy of changes
- Test any code examples
- Check links work

[Run appropriate validation]

**Validation Results:**

[If tests exist]:
- **Tests:** [X] passed, [Y] failed
- **Coverage** (if available): [Z]% overall
  - New/modified files: [list with coverage %]
  - Coverage change: [+/-X]% vs previous

[Otherwise]:
[Report results - builds, checks, etc.]

⚠️ If validation fails, STOP - must fix before proceeding

✅ Validation passed

---

## Step 2: Fetch Issue Details

[If ISSUES_BACKEND = "jira"]:

[Call `mcp__atlassian__getAccessibleAtlassianResources`]
[Call `mcp__atlassian__getJiraIssue`]

Issue: [ISSUE-KEY] - [Summary]

---

[If ISSUES_BACKEND = "gitlab"]:

[Call `mcp__gitlab__get_issue` with project_id and issue_iid]

Issue: #[IID] - [Title]

---

[If ISSUES_BACKEND = "github"]:

**Verify gh CLI:**
```bash
which gh && gh auth status
```

If gh is not installed or not authenticated, STOP and inform user.

**Fetch issue:**
```bash
gh issue view $ARGUMENTS --json number,title,body,state,url
```

Issue: #[number] - [title]

---

[If ISSUES_BACKEND = "none"]:

Using issue identifier from argument: $ARGUMENTS

---

## Step 3: Analyze Changes for PR/MR

```bash
git diff --name-only [base-branch]...HEAD
git log --oneline [base-branch]...HEAD
```

[Read key changed files to understand implementation]

**Changes Summary:**
- [What was implemented/fixed]
- [Key files modified]
- [How it addresses issue requirements]

---

## Step 4: Create Pull Request / Merge Request

[If VCS_BACKEND = "github"]:

**Creating GitHub Pull Request using gh CLI**

**Title:** [ISSUE-KEY]: [Issue Summary]

**Body:**
```markdown
Fixes [ISSUE-KEY]

## Summary
[What was implemented and how it addresses requirements]

## Changes
- [Key changes with file paths]

## Validation
- [Validation approach used]
- [Results summary]
- [If tests exist: Tests: X passed, Coverage: Y%]

**Issue:** [link to issue]
```

```bash
gh pr create --title "[ISSUE-KEY]: [Summary]" --body "[generated description]"
```

✅ PR: [URL]

---

[If VCS_BACKEND = "gitlab"]:

**Creating GitLab Merge Request using GitLab MCP**

[Call `mcp__gitlab__create_merge_request` with:
  - project_id
  - source_branch: current branch
  - target_branch: main (or default branch)
  - title: "[#IID]: [Issue Title]"
  - description: MR body (see below)
]

**Title:** [#IID]: [Issue Title]

**Body:**
```markdown
Closes #[IID]

## Summary
[What was implemented and how it addresses requirements]

## Changes
- [Key changes with file paths]

## Validation
- [Validation approach used]
- [Results summary]
- [If tests exist: Tests: X passed]

**Issue:** #[IID]
```

✅ MR: [web_url from response]

---

## Step 5: Update Issue Status

[If ISSUES_BACKEND = "jira"]:

[Call `mcp__atlassian__getTransitionsForJiraIssue`]
[Find transition to "Done" by `to.name`]
[Call `mcp__atlassian__transitionJiraIssue` to "Done"]

✅ JIRA: [ISSUE-KEY] → Done

---

[If ISSUES_BACKEND = "gitlab"]:

[Call `mcp__gitlab__update_issue` with:
  - project_id
  - issue_iid
  - state_event: "close"
]

✅ GitLab Issue: #[IID] → Closed

**Note:** GitLab will also auto-close the issue when the MR is merged (due to "Closes #IID" in description).

---

[If ISSUES_BACKEND = "github"]:

**Note:** If VCS is also GitHub, the issue will auto-close when PR is merged (due to "Fixes #[number]" in PR body).

If you want to close the issue immediately:
```bash
gh issue close $ARGUMENTS --comment "Completed in PR #[PR_NUMBER]"
```

✅ GitHub Issue: #[number] → Closed

---

[If ISSUES_BACKEND = "none"]:

No external issue tracker to update. PR/MR created successfully.

---

## ✅ Complete

**Summary:**
- ✅ Validation passed
- ✅ [PR/MR] created: [URL]
- ✅ Issue: [Status updated]

**Next Steps:**
1. Review [PR/MR] or request reviews
2. Address feedback if any
3. Merge when approved
4. **After [PR/MR] is merged,** run post-merge cleanup:
   ```bash
   /devflow:build:post-merge
   ```

The post-merge command will:
- Switch back to main branch
- Pull the merged changes
- Delete the feature branch
- Update dependencies (optional)
- Run tests to verify (optional)

---

Work complete! Remember to run `/devflow:build:post-merge` after your PR/MR is merged.
