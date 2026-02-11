---
name: devflow:pm:define-prd
description: Create, import, or update a Product Requirements Document. Multi-source ingestion, template-based gap assessment, and iterative human-approved drafting.
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
  - mcp__rag-memory-primary__query_relationships
  - mcp__rag-memory-primary__query_temporal
  - mcp__rag-memory-primary__ingest_text
  - mcp__rag-memory-primary__ingest_file
  - mcp__rag-memory-primary__ingest_url
  - mcp__rag-memory-primary__update_document
  - mcp__atlassian__searchConfluenceUsingCql
  - mcp__atlassian__getConfluencePage
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__getConfluenceSpaces
  - mcp__atlassian__createConfluencePage
  - mcp__atlassian__updateConfluencePage
  - mcp__atlassian__searchJiraIssuesUsingJql
  - mcp__google-drive__search_files
  - mcp__google-drive__download_file
  - mcp__google-drive__create_file
  - mcp__google-drive__update_file
---

# Define PRD

**Say exactly:** "SKILL INVOKED: pm/define-prd"

## Your Role

You are helping the user create, import, or update a Product Requirements Document. This is the most complex upstream skill — it handles multi-source ingestion, template-based gap assessment, and iterative drafting with human approval at every step.

## Your Goal

Produce a baselined PRD that describes WHAT to build and WHY — never HOW. The primary workflow is: gather existing material, assess completeness against the template, fill gaps, and produce a structured document the team can build from.

## How to Work

1. **Load configuration**: Read `~/.claude/plugins/config/devflow/config.md` for available backends. Check `.devflow/project.md` for upstream artifacts (problem statement from pm/discover).

2. **Gather existing material**: Use the **`multi-source-fetcher`** agent to search all configured doc backends in parallel for related material. This is heavy read work that benefits from context isolation — the agent searches across RAG Memory, Confluence, Google Drive, and issue trackers, then returns an organized summary of what was found where. Follow the ingestion workflow in [references/ingestion-guide.md](references/ingestion-guide.md) for the full process (proactive scan → present → ask for more → reflect → confirm → assess → fill gaps → consolidate).

3. **Assess against the PRD template**: Use the **`gap-assessor`** agent to compare gathered material against [references/prd-template.md](references/prd-template.md). The agent produces a section-by-section coverage report (covered, partial, missing) with quality assessment. This heavy analysis benefits from context isolation — keeps the comparison work out of the main conversation.

4. **Fill gaps through conversation**: For each gap, ask the user or draft from context. Work through gaps conversationally — significant gaps one at a time, minor gaps in batches.

5. **Draft and iterate**: Produce the structured PRD. Present for review. Iterate until the user approves.

6. **Store and baseline**: Present storage options. Store with status "baselined" in the project manifest. Update `.devflow/project.md`.

## Entry Modes (Auto-Detected)

- **From existing material** (primary) — docs exist, ingest and assess against template
- **From scratch** (edge case) — no existing material, guided creation section by section
- **Update** — existing PRD found in project manifest, load it, compare against current state
- **Import** — user points to specific doc(s) to restructure into template format

## Critical Rules

- **Existing material first.** Always search before asking the user to write from scratch.
- **WHAT and WHY, never HOW.** If requirements describe implementation, flag and rewrite.
- **Human approves every section.** Never store a PRD the user hasn't reviewed.
- **Conflicts must be resolved.** When sources disagree, surface the conflict and let the user decide.
- **Open questions are better than hidden assumptions.** Mark unknowns explicitly.
- **PRD has a shelf life.** Tied to the initiative, not the product. Record initiative name and status.
- **Update the project manifest.** Record where the PRD is stored and its status.

---

## ⛔ STOP

Skill complete.
