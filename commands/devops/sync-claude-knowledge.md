---
description: Sync latest Claude Code changes into knowledge base - fetches releases, researches primitives impact, updates RAG Memory
argument-hint: "[scope: 'latest', version like 'v2.1.0', or date like 'since 2026-01-15'] (default: latest)"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "WebFetch", "WebSearch", "Task", "AskUserQuestion", "mcp__rag-memory__search_documents", "mcp__rag-memory__list_collections", "mcp__rag-memory__ingest_text", "mcp__rag-memory__update_document", "mcp__rag-memory__get_document_by_id", "mcp__rag-memory__list_documents", "mcp__rag-memory__get_collection_info"]
---

# Sync Claude Code Knowledge

Fetch Claude Code release notes, identify primitives-relevant changes, research implications, and update RAG Memory knowledge.

Scope: $ARGUMENTS (default: `latest`)

---

## Critical Rules

1. **Progressive disclosure is mandatory.** Work in layers. Report findings at each layer and get user confirmation before going deeper. Never skip ahead.

2. **No RAG Memory writes without approval.** Present proposed content changes and wait for explicit approval before ingesting or updating documents.

3. **Discovery-based, not hardcoded.** Do not assume collection names or document IDs. Always discover what exists in RAG Memory before deciding where to write.

4. **Stateless version tracking.** Determine "what's new" by searching RAG Memory for the most recently captured release version, then comparing against the current CHANGELOG. Do not rely on local state files.

---

## Layer 1: Fetch & Parse Release Notes

**Goal:** Get the Claude Code CHANGELOG and determine what's new based on the scope argument.

**Actions:**
- Fetch the CHANGELOG from GitHub:
  ```
  WebFetch: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
  ```
  If that fails, try: `gh api repos/anthropics/claude-code/contents/CHANGELOG.md --jq .content | base64 -d`
- Parse the scope argument:
  - `latest` or no argument → most recent release entry only
  - A version (e.g., `v2.1.0`) → that specific release entry
  - A date range (e.g., `since 2026-01-15`) → all releases after that date
- Extract structured data: version, date, feature list, bug fixes, breaking changes

**Stateless "what's new" detection:**
- Search RAG Memory for existing Claude Code release knowledge:
  ```
  search_documents(query="Claude Code release version changelog", collection_name=<discovered>)
  ```
- If prior versions are found, identify what's new since the last captured version
- If no prior knowledge exists, default to the most recent release entry only

**Report to user:**
- "Found release [version] dated [date] with [N] entries."
- High-level summary of change categories
- If multiple releases are in scope, list them with dates

**Ask:** "Should I analyze these for primitives-relevant changes?"

**Wait for confirmation before Layer 2.**

---

## Layer 2: Filter for Primitives-Relevant Changes

**Goal:** Identify which changelog entries affect primitives functionality.

**Relevance signals** (score each entry against these):
- Skills, commands, hooks, plugins, agents
- MCP, tool use, tool permissions, allowed-tools
- Frontmatter, YAML, metadata
- Slash commands, user-invocable
- Plugin marketplace, plugin install
- Sub-agents, Task tool, subagent_type
- Configuration (.claude/, CLAUDE.md, settings, project settings)
- CLI flags, arguments
- OAuth, authentication (for MCP servers)
- Context, memory, checkpoints, summarization
- Structural changes to how Claude Code discovers/loads components
- New tool types or tool behavior changes

**Categorize matches into impact areas:**

| Category | Description |
|----------|-------------|
| Breaking Changes | Things that might break existing primitives |
| New Capabilities | Features that enable new primitive patterns |
| Behavior Changes | Subtle differences in how existing things work |
| New Primitives/APIs | Entirely new component types or extension points |

**Report to user:**
- "Identified [N] primitives-relevant changes out of [M] total entries."
- Present categorized list with brief descriptions for each item

**Ask:** "Which of these should I research in depth? (all / specific items / none)"

**Wait for user selection before Layer 3.**

---

## Layer 3: Deep Research

**Goal:** For each user-selected change, research implications thoroughly.

**Research strategy per item:**
1. Re-read the full changelog entry for context
2. WebSearch for community discussions, blog posts, or official announcements about this change
3. Use the `claude-code-guide` sub-agent (Task tool with `subagent_type="claude-code-guide"`) to check official documentation
4. WebFetch relevant documentation pages if found
5. Check if the change affects any existing primitives in this repo:
   - Grep/Glob the local codebase for related patterns
   - Read affected files to understand current usage

**For each researched item, produce:**
- **What changed** — factual summary
- **Why it matters** — implications for primitives development
- **Impact on existing workflows** — what might need updating (if applicable)
- **Action items** — recommended next steps
- **Code examples** — if the change enables new patterns

**Report to user:**
- Present research findings grouped by impact category
- For each finding: summary, implications, recommendations

**Ask:** "Should I update the knowledge base with these findings?"

**Wait for approval on what to capture before Layer 4.**

---

## Layer 4: RAG Memory Discovery & Update Planning

**Goal:** Find where relevant knowledge lives in RAG Memory and plan updates.

**Discovery process:**
1. `list_collections()` — see all available collections
2. For each approved finding, `search_documents()` across relevant collections using semantic queries adapted to the specific change (e.g., "Claude Code skills architecture", "how to create commands", "MCP tool permissions")
3. For documents that seem relevant:
   - `get_document_by_id()` to read current content
   - Determine: UPDATE existing knowledge or CREATE new document?
4. If no existing documents cover the topic:
   - Review collection descriptions via `get_collection_info()`
   - Identify the best-fit collection

**Update strategy decisions:**
- **Existing doc covers the topic** → propose updated content (using `update_document()` or `ingest_text(mode='reingest')`)
- **No existing coverage** → propose new document with collection placement
- **Multiple docs partially cover it** → report to user, let them decide which to update

**Report to user:**
- "Found [N] existing documents relevant to these changes: [list with collection names]"
- For each proposed change: what will be updated/created and why
- Present the proposed content (full text of what will be written)

**Ask:** "Approve these RAG Memory updates? (all / specific items / modify first)"

**Wait for explicit approval before Layer 5.**

---

## Layer 5: Execute Updates & Summary

**Goal:** Write approved changes to RAG Memory and provide a session summary.

**Actions:**
- Execute each approved RAG Memory operation:
  - For updates: `update_document()` or `ingest_text(mode='reingest')`
  - For new documents: `ingest_text()` with appropriate collection and metadata
- Verify success of each operation (check for errors)
- If any operation fails, report the error and ask how to proceed

**Final summary:**
- **Discovered:** Release version(s) and date(s) processed
- **Analyzed:** Number of total entries vs. primitives-relevant entries
- **Researched:** Items that were deeply investigated
- **Captured:** Documents created or updated in RAG Memory (with collection names)
- **Recommended next steps:** Any actions suggested by the findings (e.g., "Consider updating your skill frontmatter to support the new X feature")

---

## Notes for AI Assistants

- The `$ARGUMENTS` variable contains the user's scope input. If empty, treat as `latest`.
- When fetching the CHANGELOG, it may be large. Focus parsing on the section(s) matching the requested scope — don't process the entire file if only one release is needed.
- The `claude-code-guide` sub-agent has access to official Claude Code documentation. Use it with a focused prompt like: "What does the official documentation say about [feature name]? Include any configuration details or examples."
- For RAG Memory operations, always check `list_collections()` first. Collection names and structures may vary between users. Never hardcode collection names.
- If the user says "all" at any confirmation point, proceed with all items. If they specify a subset, only process those items.
- Keep research findings factual and actionable. Avoid speculation about future changes.
