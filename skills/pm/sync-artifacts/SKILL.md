---
name: devflow:pm:sync-artifacts
description: Read-only cross-artifact consistency check. Compares PRD, architecture doc, ADRs, and tracker issues for drift. Shows deltas — no changes, no enforcement.
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__rag-memory-primary__list_collections
  - mcp__rag-memory-primary__search_documents
  - mcp__rag-memory-primary__query_relationships
  - mcp__rag-memory-primary__query_temporal
  - mcp__atlassian__searchConfluenceUsingCql
  - mcp__atlassian__getConfluencePage
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__searchJiraIssuesUsingJql
  - mcp__atlassian__getJiraIssue
  - mcp__google-drive__search_files
  - mcp__google-drive__download_file
  - mcp__gitlab__get_issue
  - mcp__gitlab__list_issues
---

# Sync Artifacts

**Say exactly:** "SKILL INVOKED: pm/sync-artifacts"

## Your Role

You are performing a read-only consistency check across all project artifacts. You compare the PRD, architecture doc, ADRs, iteration plans, and tracker issues for drift. You show deltas — you do NOT make changes.

## Your Goal

Produce a delta report showing inconsistencies between project artifacts. Each inconsistency shows what the artifacts say and where they disagree. The developer decides what to do about each one.

## How to Work

1. **Load the project manifest**: Read `.devflow/project.md`. If it doesn't exist, inform the user: "No project manifest found. This skill requires upstream artifacts to have been created with the PM skills (pm/discover, pm/define-prd, pm/define-architecture)." STOP.

2. **Fetch all artifacts**: Use the **`artifact-fetcher`** agent to read the project manifest and fetch current versions of ALL artifacts from their respective backends — PRD, architecture doc, ADRs, iteration plans, and related tracker issues. The agent handles backend-specific fetching (RAG Memory, Confluence, Google Drive, local files) and returns full artifact content with manifest metadata.

3. **Compare across artifact pairs**: Look for inconsistencies:
   - PRD requirements vs architecture coverage — are all requirements addressed?
   - Architecture doc vs ADRs — do ADRs contradict or supersede parts of the architecture doc?
   - PRD vs tracker issues — do issues still reflect current requirements?
   - Architecture vs codebase — has the code diverged from the architecture? (if codebase exists)
   - Iteration plan vs tracker issues — do issues match the plan?

4. **Present delta report**: Structured report with each inconsistency classified.

## Report Format

```
# Artifact Consistency Report
Date: [YYYY-MM-DD]
Project: [from manifest]

## Summary
- Consistent: [count]
- Inconsistencies: [count]
- Unable to check: [count]

## PRD <> Architecture
| Item | PRD Says | Architecture Says | Status |
|------|----------|-------------------|--------|
| [requirement] | [PRD text] | [arch text] | Consistent / Inconsistent |

## Architecture <> ADRs
| Item | Architecture Says | ADR Says | Status |
|------|-------------------|----------|--------|

## PRD <> Tracker Issues
| Item | PRD Says | Issue Says | Status |
|------|----------|------------|--------|

## Architecture <> Codebase
| Item | Architecture Says | Code Does | Status |
|------|-------------------|-----------|--------|
```

## Critical Rules

- **Read-only.** Do not create, modify, or delete any files or artifacts. Ever.
- **Report facts, not judgments.** "PRD says X, architecture says Y." Not "architecture should say X."
- **No suggestions.** Do not recommend fixes. Just report what is.
- **If manifest doesn't exist, stop.** This skill requires the project manifest.
- **Check everything.** Don't skip artifact pairs because they seem aligned.

---

## ⛔ STOP

Skill complete.
