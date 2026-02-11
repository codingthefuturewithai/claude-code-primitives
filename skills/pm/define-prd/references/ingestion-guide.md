# Multi-Source Ingestion Guide

Shared reference for PM skills that need to gather existing material from multiple sources. This workflow applies whenever a skill needs to ingest, assess, and consolidate scattered inputs.

---

## The Primary Workflow

Existing material is the norm, not the exception. Most teams arrive with requirements, designs, or ideas scattered across multiple systems. The primary workflow is always:

**Ingest → Assess → Gap-fill → Consolidate**

---

## Step 1: Proactive Scan

Search ALL configured backends for material related to the topic:

| Backend | How to Search |
|---------|---------------|
| RAG Memory | `search_documents(query="[topic]")` across relevant collections |
| Confluence | `searchConfluenceUsingCql(cql="text ~ '[topic]' AND type = 'page'")` |
| Google Drive | `search_files(query="[topic]")` |
| Issue Tracker | Search for related issues (Jira JQL, GitLab, or GitHub) |
| Codebase | Grep for related terms, check README, docs/ directory |
| Local files | Check `.devflow/` for existing artifacts |

**Use subagents for parallel search** — searching multiple backends is heavy read work that benefits from context isolation.

Present findings: "Here's what I found across your configured systems..."

---

## Step 2: Ask for More

After presenting findings:

> "Here's what I found. Is there anything else to add? You can point me to:
> - URLs (specs, docs, articles)
> - Local files (markdown, PDFs, exports)
> - Paste text directly (from Slack, email, meeting notes)"

Accept whatever the user provides. Fetch and organize.

---

## Step 3: Reflect

Show the user everything gathered, organized clearly:

- What was found in each system
- What the user provided additionally
- Total input inventory

---

## Step 4: Confirm

> "This is the complete set of inputs I'll work from. Anything missing before I assess coverage?"

**Wait for confirmation.** Do not proceed until the user confirms the input set is complete.

---

## Step 5: Assess Coverage

Map gathered material against the target template (PRD template, architecture template, etc.). Produce a coverage report:

| Section | Status | Detail |
|---------|--------|--------|
| Section 1 | Covered | From Confluence page X |
| Section 2 | Partial | Has goals but missing metrics. Source: Google Doc Y |
| Section 3 | Missing | No content found |
| Section 4 | Covered | From meeting notes (pasted) + Jira issues |

**Adaptive depth:**
- Completely missing sections → flag at section level
- Partial sections → flag at sub-section level (e.g., "has goals but missing metrics")
- Covered sections → note source and any ambiguities

---

## Step 6: Fill Gaps

For each gap:
1. **Ask the user directly** — they may know the answer
2. **Draft from context** — if enough surrounding info exists, propose content
3. **Mark as open question** — if no one has the answer yet

Work through gaps conversationally. One at a time for significant gaps, batch for minor ones.

---

## Step 7: Consolidate

Produce the structured artifact from combined inputs + gap-fills:

- Organized per the target template
- Sources attributed ("from Confluence page X", "from user input")
- Open questions clearly marked
- Ready for user review

Present the draft. User reviews, edits, approves before storage.

---

## Completeness Scales with Input

| Existing Material | Workflow Emphasis |
|-------------------|-------------------|
| Thorough existing docs | Quick ingest → light gap assessment → minor fills → consolidate |
| Rough/partial docs | Ingest → moderate gap assessment → guided creation for missing sections |
| Scattered fragments | Ingest all → deduplicate → reconcile conflicts → extensive gap-filling |
| Nothing | Guided creation from scratch — walk through template section by section |

These aren't separate modes — the depth adapts automatically based on input completeness.
