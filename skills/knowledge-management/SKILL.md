---
name: devflow:knowledge-management
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

---

## Step 0: Check Available Backends

Load DevFlow configuration to determine what's available.

**Check for config file:**
1. Check `~/.claude/plugins/config/devflow/config.md`
2. If no config → Default to checking both RAG Memory and Atlassian

**Parse configuration:**
- `rag-memory.enabled` - Is RAG Memory available?
- `docs.enabled` - Is a docs backend enabled?
- `docs.backend` - Which one? (confluence, google-drive)
- `rag-memory.routing` - How to route content (decide-each-time, quick-to-rag, all-to-rag)
Store:
- RAG_ENABLED: true/false
- DOCS_ENABLED: true/false
- DOCS_BACKEND: confluence/google-drive/none

**Availability check:**

| RAG Memory | Docs Backend | Skill Status |
|------------|--------------|--------------|
| Enabled | Enabled | Full routing available |
| Enabled | Disabled | RAG Memory only |
| Disabled | Enabled | Docs backend only |
| Disabled | Disabled | Inform user to run `/devflow-setup` and STOP |

---

## Parameter Validation Gate (MANDATORY)

**Before ANY MCP tool call in this skill, validate EVERY parameter.**

For EVERY parameter on EVERY call, verify where the value came from:

| Source | Allowed? | Action |
|--------|----------|--------|
| Value from plugin config read in Step 0 | **YES** | Use it |
| Value returned from a PREVIOUS call to the SAME backend's MCP server | **YES** | Use it |
| Value provided by the user in this conversation | **YES** | Use it |
| Value from a DIFFERENT backend's MCP server | **NO** | STOP. Backends are isolated. |
| Value that "looks right" or was inferred | **NO** | STOP. ASK the user. |

### Confluence

- `cloudId`: Read from config `cloudId` OR call `getAccessibleAtlassianResources`. NEVER fabricate.

### RAG Memory

- `actor_type`: Self-identify (already required in Self-Identification section above).
- `collection_name`: From `list_collections` + user selection. NEVER guess.

---

## Flags

| Flag | Description |
|------|-------------|
| `--rag` | Route to RAG Memory only |
| `--docs` | Route to configured docs backend (Confluence or Google Drive) |
| `--confluence` | Route to Confluence specifically (if available) |
| `--google` | Route to Google Drive specifically (if available) |
| `--both` | Search both, then decide |
| `--update` | Force update of related existing document |
| `--quick` | Force save as quick note (RAG only) |
| `--separate` | Force creation of full document |

---

## Step 1: Determine Destination

**`--rag` flag?**
- If RAG_ENABLED: Go to RAG MEMORY
- If not: "RAG Memory not configured. Run /devflow-setup to enable." STOP

**`--docs` flag?**
- If DOCS_ENABLED: Go to DOCS BACKEND (Confluence or Google Drive based on config)
- If not: "No docs backend configured. Run /devflow-setup to enable." STOP

**`--confluence` flag?**
- Check Atlassian MCP availability
- If available: Go to CONFLUENCE
- If not: "Confluence unavailable. Store in RAG Memory instead?" Wait for response.

**`--google` flag?**
- Check Google Drive MCP availability
- If available: Go to GOOGLE DRIVE
- If not: "Google Drive unavailable. Store in RAG Memory instead?" Wait for response.

**`--both` flag?** → Go to Step 2 (check what's available)

**No flag?**
- If only RAG_ENABLED: Go to RAG MEMORY (no need to ask)
- If only DOCS_ENABLED: Go to DOCS BACKEND (no need to ask)
- If both enabled: Go to Step 2

---

## Step 2: Check Backend Availability

**If RAG_ENABLED:**
Test: `mcp__rag-memory-primary__list_collections`
- Success → RAG available
- Failure → RAG unavailable

**If DOCS_BACKEND = "confluence":**
Test: `mcp__atlassian__getAccessibleAtlassianResources`
- Success → Confluence available
- Failure → Confluence unavailable

**If DOCS_BACKEND = "google-drive":**
Test: `mcp__google-drive__search_files` with:
  - query: "test"
  - max_results: 1
- Success → Google Drive available
- Failure → Google Drive unavailable

**Route based on availability:**

| RAG | Docs | Action |
|-----|------|--------|
| ✓ | ✓ | Ask user where to store (Step 3) |
| ✓ | ✗ | "Note: [Docs backend] unavailable. Storing to RAG Memory." → RAG MEMORY |
| ✗ | ✓ | "Note: RAG Memory unavailable. Storing to [Docs backend]." → DOCS BACKEND |
| ✗ | ✗ | "Neither backend available. Check your MCP server connections." STOP |

---

## Step 3: Route by User Choice

Ask user:
> Where would you like to store this?
> 1. RAG Memory
> 2. [Confluence/Google Drive] (based on config)
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

## GOOGLE DRIVE

Follow the workflow in [references/google-drive.md](references/google-drive.md).

Summary:
1. Search for existing related files on Google Drive
2. Route user-provided content (local file, raw text) to Google Drive via upload
3. For URLs, suggest RAG Memory (Google Drive MCP does not ingest URLs)
4. For raw text with no file, write to temp `.md` then upload

---

## BOTH

Search both systems, then let user decide.

1. Discover RAG collections (see rag-memory.md)
2. **If DOCS_BACKEND = "confluence":**
   - Get Confluence spaces
   - Search: `search(query="[topic]")`
3. **If DOCS_BACKEND = "google-drive":**
   - Search: `mcp__google-drive__search_files(query="[topic]")`
4. Search RAG Memory: `search_documents(query="[topic]", limit=5)`
5. Show results from both
6. Ask: "Based on these results, where should I store this - RAG Memory or [Confluence/Google Drive]?"
7. Route to chosen destination's workflow

