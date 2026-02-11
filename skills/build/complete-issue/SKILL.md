---
name: devflow:build:complete-issue
description: Final validation, create PR/MR, and mark issue done. Use this after implementing changes to create a pull request and close the issue.
argument-hint: "[ISSUE-KEY, GitLab issue number, or GitHub issue number]"
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
  - mcp__atlassian__getJiraIssue
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__transitionJiraIssue
  - mcp__atlassian__getTransitionsForJiraIssue
  - mcp__atlassian__editJiraIssue
  - mcp__atlassian__updateConfluencePage
  - mcp__atlassian__getConfluencePage
  - mcp__gitlab__get_issue
  - mcp__gitlab__update_issue
  - mcp__gitlab__create_merge_request
  - mcp__rag-memory-primary__search_documents
  - mcp__rag-memory-primary__update_document
  - mcp__google-drive__download_file
  - mcp__google-drive__update_file
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

## Step 3b: Deviation Review (If Project Manifest Exists)

**Check for project manifest:** Read `.devflow/project.md`.

- **If no project manifest exists** → skip to Step 4. Not all projects use upstream PM skills.
- **If project manifest exists** → proceed with deviation review.

**Compare plan vs implementation using the `deviation-reviewer` agent:**

Use the **`deviation-reviewer`** agent to compare the implementation plan against actual changes. Pass it:
- **Plan file path:** `.devflow/plans/[ISSUE-KEY].md`
- **Issue key:** The issue being completed
- **Base branch:** For computing the diff

The agent reads the plan, analyzes the git diff, and returns a structured deviation report classifying each deviation by type (Technology, Architecture, Scope, Approach) with potential artifact routing.

**If no plan file exists:** The agent still reviews the changes for significant architectural or requirement deviations worth capturing.

Present the agent's deviation report to the developer:

> "I noticed these differences between what was planned and what was built:"
> 1. [Deviation description] — Is this significant?
> 2. [Deviation description] — Is this significant?

**Developer responds for each:** Significant / Not significant / Dismiss all

If "Dismiss all" or no significant deviations → skip to Step 4.

---

## Step 3c: Capture Decisions (If Significant Deviations Found)

For each deviation the developer marked as significant, propose where to route the update:

| Deviation Type | Proposed Routing |
|----------------|-----------------|
| Feature works differently than issue described | Update tracker issue |
| Architecture decision changed | New ADR (stored alongside architecture doc) |
| Pattern or component changed significantly | Architecture doc update |
| Requirement changed or scope shifted | PRD update (only during active initiative) |

For each item:

> "[Description]. I recommend updating [artifact]. Confirm? (Yes / Skip)"

**Route confirmed updates** to the correct artifact using the project manifest to find locations. Use the appropriate backend tools.

**If no project manifest artifacts are found** for a proposed routing (e.g., no architecture doc stored), note it and move on: "No architecture doc found in project manifest. Consider recording this decision elsewhere."

After processing all items, proceed to Step 4.

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
