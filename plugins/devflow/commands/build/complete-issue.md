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

Use the **build-ops** skill to load backend configuration from `devflow-config.md`.

The build-ops skill handles config loading and parameter validation for both
issue tracking and VCS backends. See `skills/build-ops/SKILL.md`.

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

Use the **build-ops** skill to fetch issue $ARGUMENTS from the configured issue tracker.

The build-ops skill handles all backend-specific fetch operations and enforces
parameter validation. See `skills/build-ops/SKILL.md`.

Issue: [key/number] - [summary/title]

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

Use the **build-ops** skill to create a PR/MR in the configured VCS backend with:
- Issue reference: $ARGUMENTS
- Issue summary from Step 2
- Changes summary from Step 3
- Validation results from Step 1

The build-ops skill handles all backend-specific PR/MR creation (GitHub PRs via
`gh pr create`, GitLab MRs via MCP) and enforces parameter validation.
See `skills/build-ops/SKILL.md`.

✅ PR/MR: [URL]

---

## Step 5: Update Issue Status

Use the **build-ops** skill to transition issue $ARGUMENTS to "Done" / close it.

The build-ops skill handles all backend-specific close/transition logic (Jira
transitions to "Done", GitLab close, GitHub close with PR reference) and enforces
parameter validation. See `skills/build-ops/SKILL.md`.

**Note for GitHub:** If VCS is also GitHub, the issue may auto-close when PR is merged (due to "Fixes #[number]" in PR body).

✅ Issue status updated

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
