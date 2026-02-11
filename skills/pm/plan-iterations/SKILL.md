---
name: devflow:pm:plan-iterations
description: Break PRD requirements and architecture into buildable tasks grouped into iterations. Creates issues in the configured tracker. Bridges upstream activities to the build workflow.
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__rag-memory-primary__list_collections
  - mcp__rag-memory-primary__search_documents
  - mcp__rag-memory-primary__ingest_text
  - mcp__rag-memory-primary__update_document
  - mcp__atlassian__searchConfluenceUsingCql
  - mcp__atlassian__getConfluencePage
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__createJiraIssue
  - mcp__atlassian__searchJiraIssuesUsingJql
  - mcp__gitlab__create_issue
  - mcp__gitlab__list_issues
  - mcp__google-drive__search_files
  - mcp__google-drive__download_file
  - mcp__google-drive__create_file
---

# Plan Iterations

**Say exactly:** "SKILL INVOKED: pm/plan-iterations"

## Your Role

You are helping the user break their PRD and architecture into buildable tasks, group them into iterations, and create issues in the configured tracker. This skill bridges upstream activities to the existing build workflow (fetch-issue → plan-issue → implement-issue → complete-issue).

## Your Goal

Produce a set of well-formed issues grouped into the first 2-3 iterations. Iteration 1 should deliver a walking skeleton — minimal end-to-end functionality. Each issue must have clear acceptance criteria and trace back to PRD requirements.

## How to Work

1. **Load configuration**: Read `~/.claude/plugins/config/devflow/config.md` for available backends. Use the **build-ops** skill pattern for issue tracker configuration.

2. **Find upstream artifacts**: Check `.devflow/project.md` for PRD and architecture doc locations. Load both — the PRD provides requirements to decompose, the architecture provides technical context. If either is missing, ask the user for the information directly.

3. **Decompose**: Use the **`decomposition-analyzer`** agent to read the PRD + architecture doc and propose a structured task breakdown with dependency chains. This is a heavy read operation that benefits from context isolation. The agent uses [references/decomposition-guide.md](references/decomposition-guide.md) for guidance on breaking requirements into tasks, handling cross-cutting concerns, and dependency ordering. It returns a structured decomposition with iteration grouping.

4. **Plan iterations**: Group tasks into iterations using [references/iteration-template.md](references/iteration-template.md). Iteration 1 = walking skeleton + scaffolding. Iterations 2-3 = core features. Only plan 2-3 iterations.

5. **Review with user**: Present the full iteration plan for review. Tasks, sizes, dependencies, iteration assignments. Iterate until approved.

6. **Create issues**: After approval, create issues in the configured tracker. Features → Executable Specs, infrastructure → Tasks. Each issue includes acceptance criteria and links back to PRD requirements and architecture decisions. Use the **build-ops** skill for issue creation.

7. **Store iteration plan**: Store the iteration plan and update `.devflow/project.md`.

## Critical Rules

- **Only plan 2-3 iterations.** Not the entire product. Later iterations planned as the team learns.
- **Iteration 1 is a walking skeleton.** Minimal end-to-end functionality that proves the architecture.
- **Cross-cutting concerns must be accounted for.** Auth, logging, error handling, observability.
- **Acceptance criteria describe outcomes, not implementation.** "User can search" not "Create Elasticsearch index."
- **Each task traces back.** Every task links to a PRD requirement or architecture decision.
- **Human approves before issue creation.** Preview the full plan first.
- **Follow DevFlow conventions.** Features = Executable Specs, infrastructure = Tasks.
- **Update the project manifest.** Record the iteration plan location.

---

## ⛔ STOP

Skill complete.
