---
name: primitives-toolkit:knowledge-management
description: Intelligent workflow for storing and organizing external knowledge. Use this skill when the user asks to store, remember, capture, or preserve any information externally or mentions saving to a knowledge base.
user-invocable: true
---

# Knowledge Management

Route content to the right destination.

**Say exactly:** "SKILL INVOKED: knowledge-management"

## Self-Identification (REQUIRED)

Before ANY ingestion operation, identify yourself:
- Reflect on which AI coding assistant you are (product name, not model name)
- Pass this as `actor_type` on ALL ingest calls
- If you get an invalid actor_type error, adjust based on the error message

## Critical Rules

STOP IMMEDIATELY and inform the user when:
- URL access fails (403, 401, 404, blocked, forbidden)
- File access fails (not found, unsupported type, too large)
- Any error where proceeding would definitely fail

DO NOT:
- Ask for inputs when the operation will fail anyway
- Claim you did something you didn't
- Offer actions you cannot perform

**Principle:** If a step fails, ask: will the same failure affect the next step? If yes, STOP.

## Flags

| Flag | Description |
|------|-------------|
| `--rag` | Route to RAG Memory only |
| `--confluence` | Route to Confluence only |
| `--both` | Search both, then decide |
| `--update` | Force update of related existing document |
| `--quick` | Force save as quick note (RAG only) |
| `--separate` | Force creation of full document |

---

## Step 1: Determine Destination

**`--rag` flag?** → Go to RAG MEMORY (skip Atlassian check)

**`--confluence` flag?** → Check Atlassian availability (Step 2)

**`--both` flag?** → Check Atlassian availability (Step 2)

**No flag?** → Check Atlassian availability (Step 2)

---

## Step 2: Check Atlassian Availability

Call `getAccessibleAtlassianResources()`.

**Available?** → Go to Step 3

**Not available?**
- If `--confluence` was requested: "Confluence unavailable (Atlassian MCP not configured). Store in RAG Memory instead?" Wait for response.
- If `--both` was requested: "Confluence unavailable. Proceeding with RAG Memory only." → Go to RAG MEMORY
- If no flag: "Note: Confluence unavailable. Storing to RAG Memory." → Go to RAG MEMORY

---

## Step 3: Route by Flag

**`--confluence`?** → Go to CONFLUENCE

**`--both`?** → Go to BOTH

**No flag?** → Ask user:
> Where would you like to store this?
> 1. RAG Memory
> 2. Confluence
> 3. Search both first, then decide
> 4. Cancel

STOP and wait. Then route based on answer.

---

## RAG MEMORY

Follow the workflow in [references/rag-memory.md](references/rag-memory.md).

Summary:
1. **User topic check** - If provided, use it exactly
2. **Quick note check** - Short, informal → route to `quick-notes`
3. **URL preview** - If URL without topic, preview first; STOP if blocked
4. **Agent-preferences FIRST** - Check for routing rules before collection discovery
5. **Collection discovery** - Only if no preference found
6. **Confirm with user** - Present recommendation, wait for approval
7. **Ingest** - Use appropriate tool with collection, topic, actor_type

---

## CONFLUENCE

Follow the workflow in [references/confluence.md](references/confluence.md).

Summary:
1. Get available spaces
2. Search for existing related content
3. Classify content (short update vs full page)
4. Route accordingly:
   - **Update existing** → Append to related page
   - **New page** → Select space, create page

---

## BOTH

Search both systems, then let user decide.

1. Discover RAG collections (see rag-memory.md)
2. Get Confluence spaces (see confluence.md)
3. Search both:
   - `search_documents(query="[topic]", limit=5)`
   - `search(query="[topic]")`
4. Show results from both
5. Ask: "Based on these results, where should I store this - RAG Memory or Confluence?"
6. Route to chosen destination's workflow

