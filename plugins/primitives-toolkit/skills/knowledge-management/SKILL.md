---
name: primitives-toolkit:knowledge-management
description: Intelligent workflow for storing and organizing external knowledge. Use this skill when the user asks to store, remember, capture, or preserve any information externally.
user-invocable: true
---

# Knowledge Management

Route content to the right destination. Execute these steps in exact order.

**Important:** Step labels (R1, R2, C1, B1, etc.) are for YOUR navigation only. NEVER announce step labels to users. Just do the work.

## Optional Flags

| Flag | Description |
|------|-------------|
| `--rag` | Route to RAG Memory only |
| `--confluence` | Route to Confluence only |
| `--both` | Search both, then decide |
| `--update` | Force update of related existing document (skip confirmation) |
| `--aggregate` | Force quick notes aggregation (skip confirmation) - RAG only |
| `--separate` | Force creation of standalone document (skip confirmation) |

## Workflow

**0.** Say exactly: "📋 SKILL INVOKED: knowledge-management"

**1.** Check arguments for destination flag:

   **`--rag` flag present** → Go to RAG MEMORY PATH below (no Atlassian check needed)

   **`--confluence` flag present** → Go to step 2

   **`--both` flag present** → Go to step 2

   **No flag present** → Go to step 2

**2.** Check if Atlassian MCP server is available by calling `getAccessibleAtlassianResources()`.

   **Atlassian available** → Go to step 3

   **Atlassian NOT available (tool fails or not found)** →

   - If user requested `--confluence`: Say "Confluence is not available. The Atlassian MCP server is not configured. Would you like to store in RAG Memory instead?" Wait for response.
   - If user requested `--both`: Say "Confluence is not available. The Atlassian MCP server is not configured. Proceeding with RAG Memory only." Go to RAG MEMORY PATH.
   - If no flag: Say "Note: Confluence is not available (Atlassian MCP server not configured). Storing to RAG Memory." Go to RAG MEMORY PATH.

**3.** Atlassian is available. Now route based on original request:

   **`--confluence` flag was present** → Go to CONFLUENCE PATH below

   **`--both` flag was present** → Go to BOTH PATH below

   **No flag was present** → Ask the user:
   "Where would you like to store this?
   1. RAG Memory
   2. Confluence
   3. Search both first, then decide
   4. Cancel - I didn't mean to trigger this"

   STOP and wait for user response before proceeding.

   **User selects 1** → Go to RAG MEMORY PATH below
   **User selects 2** → Go to CONFLUENCE PATH below
   **User selects 3** → Go to BOTH PATH below
   **User selects 4** → Say "No problem, cancelled." and END.

---

## RAG MEMORY PATH

Only touch RAG Memory MCP server. Do NOT call any Confluence/Atlassian tools.

**R1.** Call `list_collections()` to get all RAG Memory collections.

**R2.** For EACH collection returned, call `get_collection_info(collection_name)`.
   Store the `domain` and `domain_scope` values.

**R3.** Search for existing content:
   ```
   search_documents(query="What content exists about [topic]?", limit=5)
   ```

**R4.** Show search results to user.

**R5.** Query agent-preferences for collection guidance:
   ```
   search_documents(
       query="What are the user's routing preferences for [domain] content?",
       collection_name="agent-preferences"
   )
   ```
   Use domain values like "Operations", "Engineering" from R2.

**R6.** Select collection: match content against `domain_scope`, present top 2-3 collections, let user choose.

**R7.** Suggest a topic. Ask user to accept or modify.

**R7.5** Quick Capture Detection:

   Check if content qualifies as quick capture (ALL must be true):
   - Length < 500 characters
   - No markdown headers (lines starting with `#`)
   - Single paragraph (no `\n\n`)

   **NOT quick capture** → Go to R8 (normal ingestion)

   **IS quick capture** → Check flags:
   - `--separate` present → Go to R8 (normal ingestion)
   - `--aggregate` present → Go to QUICK NOTES AGGREGATION below
   - `--update` present → Go to UPDATE EXISTING DOCUMENT below

   **No flag (most common)** → Use search results from R3:

   **Related document found in R3:**
   Ask user:
   "This looks like a quick note. I found a related document: '[title]'

   How would you like to handle this?
   1. Update '[title]' with this information
   2. Add to Quick Notes for [collection]
   3. Create a separate document
   4. Cancel"

   STOP and wait for response.
   - User selects 1 → Go to UPDATE EXISTING DOCUMENT
   - User selects 2 → Go to QUICK NOTES AGGREGATION
   - User selects 3 → Go to R8
   - User selects 4 → Say "No problem, cancelled." and END

   **No related document found:**
   Ask user:
   "This looks like a quick note. How would you like to store it?
   1. Add to Quick Notes for [collection]
   2. Create a separate document
   3. Cancel"

   STOP and wait for response.
   - User selects 1 → Go to QUICK NOTES AGGREGATION
   - User selects 2 → Go to R8
   - User selects 3 → Say "No problem, cancelled." and END

   ---

   **UPDATE EXISTING DOCUMENT:**
   1. Get document content via `get_document_by_id(document_id)`
   2. Append with timestamp: `**Added [YYYY-MM-DD HH:MM]:** [content]`
   3. Call `update_document(document_id, content=updated_content)`
   4. Confirm success and END

   ---

   **QUICK NOTES AGGREGATION:**
   1. Look for existing document titled `Quick Notes - [collection] - YYYY-MM` (current month)
      Use `list_documents(collection_name)` to find it
   2. **If exists:**
      - Get content via `get_document_by_id()`
      - Append entry: `## YYYY-MM-DD HH:MM\n[content]\n\n---\n`
      - Call `update_document(document_id, content=updated_content)`
   3. **If not exists:**
      - Create via R8 with:
        - title: `Quick Notes - [collection] - YYYY-MM`
        - content formatted as: `## YYYY-MM-DD HH:MM\n[content]\n\n---\n`
   4. Confirm success and END

**R8.** Ingest content as-is (do not expand or modify):
   ```
   ingest_text(content="[user's exact content]", collection_name="[chosen]", topic="[chosen]", ...)
   ```

**R9.** If no preference existed in R5, offer to save one:
   "Would you like me to remember that [domain] content goes to [collection]?"

END.

---

## CONFLUENCE PATH

Only touch Confluence/Atlassian MCP server. Do NOT call any RAG Memory tools.
Atlassian availability was already verified in step 2.

**C1.** Use the cloud ID from step 2. Call `getConfluenceSpaces()` to list available spaces.

**C2.** Search for existing content:
   ```
   search(query="What documentation exists about [topic]?")
   ```

**C3.** Show search results to user.

**C4.** Select space: present available spaces, let user choose.

**C4.5** Quick Capture Detection:

   Check if content qualifies as quick capture (ALL must be true):
   - Length < 500 characters
   - No markdown headers (lines starting with `#`)
   - Single paragraph (no `\n\n`)

   **NOT quick capture** → Go to C5 (normal page creation)

   **IS quick capture** → Check flags:
   - `--separate` present → Go to C5 (normal page creation)
   - `--update` present → Go to UPDATE EXISTING PAGE below

   **No flag (most common)** → Use search results from C2:

   **Related page found in C2:**
   Ask user:
   "This looks like a quick note. I found a related page: '[title]'

   How would you like to handle this?
   1. Update '[title]' with this information
   2. Create a new page
   3. Cancel"

   STOP and wait for response.
   - User selects 1 → Go to UPDATE EXISTING PAGE
   - User selects 2 → Go to C5
   - User selects 3 → Say "No problem, cancelled." and END

   **No related page found** → Go to C5 (normal page creation)

   ---

   **UPDATE EXISTING PAGE:**
   1. Extract `pageId` from search results
   2. Get current page content via `getConfluencePage(cloudId, pageId)` if needed
   3. Append with timestamp:
      ```
      [existing content]

      ---

      **Added [YYYY-MM-DD HH:MM]:**
      [new content]
      ```
   4. Call `updateConfluencePage(cloudId, pageId, title, updated_content)`
   5. Confirm success and END

**C5.** Create page:
   ```
   createConfluencePage(cloudId="...", spaceId="...", title="...", content="[user's exact content]")
   ```

END.

---

## BOTH PATH

Touch both MCP servers. Search both, then ask user where to store.
Atlassian availability was already verified in step 2.

**B1.** Call `list_collections()` to get all RAG Memory collections.

**B2.** For EACH collection returned, call `get_collection_info(collection_name)`.
   Store the `domain` and `domain_scope` values.

**B3.** Use the cloud ID from step 2. Call `getConfluenceSpaces()` to list available spaces.

**B4.** Search BOTH systems:
   ```
   search_documents(query="What content exists about [topic]?", limit=5)
   search(query="What documentation exists about [topic]?")
   ```

**B5.** Show results from both systems to user.

**B6.** Query agent-preferences for routing guidance:
   ```
   search_documents(
       query="What are the user's routing preferences for [domain] content?",
       collection_name="agent-preferences"
   )
   ```

**B7.** Ask user: "Based on these results, where should I store this - RAG Memory or Confluence?"

**B8.** Based on user answer:
   - RAG Memory → Go to R6 (skip R1-R5, already done)
   - Confluence → Go to C4 (skip C1-C3, already done)

END.

---

## Reference Documents

For detailed tool parameters and edge cases:
- [rag-memory.md](references/rag-memory.md) - RAG Memory tool details
- [confluence.md](references/confluence.md) - Confluence tool details
- [preferences.md](references/preferences.md) - Preference storage format
