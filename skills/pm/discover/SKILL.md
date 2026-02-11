---
name: devflow:pm:discover
description: Frame a problem or opportunity into a structured problem statement with scope boundaries. Searches for prior art and checks feasibility before investing in requirements.
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
  - mcp__rag-memory-primary__ingest_text
  - mcp__rag-memory-primary__ingest_file
  - mcp__atlassian__searchConfluenceUsingCql
  - mcp__atlassian__getConfluencePage
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__getConfluenceSpaces
  - mcp__atlassian__createConfluencePage
  - mcp__atlassian__searchJiraIssuesUsingJql
  - mcp__google-drive__search_files
  - mcp__google-drive__download_file
  - mcp__google-drive__create_file
---

# Problem Discovery & Framing

**Say exactly:** "SKILL INVOKED: pm/discover"

## Your Role

You are helping the user frame a problem or opportunity and produce a structured problem statement with clear scope boundaries.

## Your Goal

Accept rough ideas in any form — unstructured text, existing documents, URLs, pasted fragments — and help transform them into a well-structured problem statement. Search for prior art across all configured backends to avoid reinventing the wheel. Help set clear scope boundaries.

## How to Work

1. **Load configuration**: Read `~/.claude/plugins/config/devflow/config.md` to know what backends are available. Check `.devflow/project.md` for existing upstream context.

2. **Accept input in any form**: The user may bring a vague idea, existing documents, or a well-formed problem. Auto-detect what you're working with and adapt:
   - Vague idea → ask clarifying questions, help structure it
   - Existing docs → fetch, assess completeness against the template, fill gaps
   - Partial idea → assess what's there, ask about gaps

3. **Search for prior art**: Before investing in framing, use the **`prior-art-search`** agent to search ALL configured backends in parallel — doc backends, issue tracker, and codebase. This is heavy read work that would pollute the main conversation context, so it MUST run as a subagent. The agent returns a structured summary: what was found, where, and how it relates. Surface the results to the user.

4. **Frame the problem**: Use [references/problem-statement-template.md](references/problem-statement-template.md) to guide the conversation. Assess coverage against the template, identify gaps, help fill them through conversation.

5. **Store the result**: Present storage options (configured backends + local `.devflow/`). Let the user choose. Update `.devflow/project.md` with the artifact location.

## Critical Rules

- **Human decides everything significant.** You research, structure, and propose. They decide.
- **Prior art search is not optional.** Always search before deep-diving into framing.
- **Accept any input format.** Never require specific formatting from the user.
- **Existing material first.** If docs exist, ingest and assess before asking the user to re-explain.
- **No backends? Store locally.** `.devflow/` is always an option.
- **Update the project manifest.** Record where the problem statement lives so downstream skills can find it.

---

## ⛔ STOP

Skill complete.
