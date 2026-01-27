# RAG Memory Reference

## Self-Identification

All ingest operations require `actor_type` to identify which AI assistant is performing the action.

**How to determine your actor_type:**
1. Reflect on which AI coding assistant environment you are operating within
2. Use your product name, NOT your model name
3. Valid values are maintained in the backend database (enumerated, not listed here)
4. If you receive an error for an invalid value, adjust based on the error message

**Why:** This creates an audit trail showing which AI assistant created or modified each document.

---

## Critical Rules

STOP IMMEDIATELY and inform the user when:
- URL access fails (403, 401, 404, blocked, forbidden)
- File access fails (not found, unsupported type, too large)
- Any error where proceeding would definitely fail

DO NOT:
- Ask for inputs when the operation will fail anyway
- Claim you did something you didn't
- Offer actions you cannot perform
- Fabricate topics or results

**Principle:** If a step fails, ask yourself: will the same failure affect the next step? If yes, STOP.

---

## RAG Memory Workflow

### Step 1: User Topic Check

If user provided a topic, use it exactly. Skip URL preview step.

### Step 2: Quick Note Check

**Flag override:** `--quick` → Go directly to Quick Note Workflow

Assess whether content is a quick note:
- Short, informal (a few sentences, a thought, a reminder)
- "Jot this down" energy vs "file this away" energy
- User wants to capture something without deciding where it belongs
- Unstructured - no clear organization or headers

If it's a quick note → Route to `quick-notes`, generate topic, ingest.

### Step 3: URL Preview (if URL input, no user topic)

For URLs when user hasn't provided a topic:
1. Use WebFetch to preview content
2. If blocked/forbidden/not found → STOP, tell user "I cannot access this URL"
3. If success → Generate topic (3-8 words) from title/content, proceed to routing

### Step 4: Check Agent-Preferences (MANDATORY FIRST)

**This step comes BEFORE collection discovery.**

Query for user's routing preferences:
```
search_documents(
    collection_name="agent-preferences",
    query="routing rules for [content type/domain]"
)
```

- If rules are found → Follow them exactly, skip to Step 6
- If no rules found → Proceed to Step 5

### Step 5: Collection Discovery (only if no preference found)

1. Call `list_collections()` to get all collections
2. For relevant collections, call `get_collection_metadata_schema(collection_name)`
3. Use `routing.examples` and `routing.exclusions` to score collections
4. Present top 2-3 collections with reasoning to user

### Step 6: Confirm with User

Present your recommendation:
> Based on [agent-preferences / routing hints], I recommend storing this in **[collection]** with topic: "[topic]"
>
> 1. Proceed
> 2. Choose different collection
> 3. Save as quick note instead
> 4. Cancel

STOP and wait for user response.

### Step 7: Ingest

Use the appropriate tool based on input type:
- URL → `ingest_url()`
- File path → `ingest_file()`
- Raw text → `ingest_text()`

Always include: `collection_name`, `topic`, `actor_type`

### Step 8: Offer to Save Preference (if applicable)

If user chose a collection different from what routing hints suggested, and no preference existed:
> Would you like me to remember that [content type] goes to [collection]?

If yes, save to agent-preferences collection.

---

## Quick Note Workflow

Quick notes go to the dedicated `quick-notes` system collection as individual documents.

1. Ingest to the `quick-notes` collection:
   ```
   ingest_text(
       content="[the note content]",
       collection_name="quick-notes",
       topic="[brief descriptive topic]",
       actor_type="[your product name]"
   )
   ```

2. Confirm: "Saved to Quick Notes. You can merge related notes later from the Quick Notes view."

**About quick-notes collection:**
- System collection, auto-created on server startup
- Cannot be deleted (protected)
- Has dedicated UI view for browsing and managing notes
- Users can select multiple notes and merge them into a single document

---

## Update Existing Workflow

When `--update` flag is set and related content was found:

1. Get document content: `get_document_by_id(document_id)`
2. Append with timestamp:
   ```
   [existing content]

   ---

   **Added [YYYY-MM-DD HH:MM]:**
   [new content]
   ```
3. Update: `update_document(document_id, content=updated_content)`
4. Confirm success

---

## Tool Parameters

### search_documents(query, collection_name, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language question |
| collection_name | string | No | Limit to specific collection |
| limit | int | No | Max results (default 5) |

### list_collections()

No parameters required. Returns array of collection names.

### get_collection_metadata_schema(collection_name)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_name | string | Yes | Name of collection |

Returns: `name`, `domain`, `domain_scope`, `description`, plus:
- `metadata_schema.routing.examples` - Content that SHOULD route here
- `metadata_schema.routing.exclusions` - Content that should NOT route here

### ingest_text(content, collection_name, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| content | string | Yes | Text content |
| collection_name | string | Yes | Target collection |
| topic | string | Yes | Topic for relevance |
| mode | string | No | "ingest" (default) or "reingest" |
| actor_type | string | **Yes** | Your AI assistant name |

### ingest_url(url, collection_name, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | URL to ingest |
| collection_name | string | Yes | Target collection |
| topic | string | Yes | Topic for relevance |
| follow_links | bool | No | Crawl linked pages |
| max_pages | int | No | Max pages (default 10, max 20) |
| mode | string | No | "ingest" (default) or "reingest" |
| actor_type | string | **Yes** | Your AI assistant name |

### ingest_file(file_path, collection_name, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | Yes | Local file path |
| collection_name | string | Yes | Target collection |
| topic | string | Yes | Topic for relevance |
| mode | string | No | "ingest" (default) or "reingest" |
| actor_type | string | **Yes** | Your AI assistant name |

### get_document_by_id(document_id)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| document_id | string | Yes | Document ID |

### update_document(document_id, content, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| document_id | string | Yes | Document to update |
| content | string | No | New content (triggers re-chunking) |
| metadata | dict | No | Updated metadata |

---

## Edge Cases

### Duplicate Detection

If content already exists, you'll get a duplicate error. Options:
- Skip if content hasn't changed
- Use `mode="reingest"` to replace existing content

### Large Websites

For URLs with many pages:
1. First call `analyze_website(url)` to see structure
2. Use `max_pages=20` limit per ingest
3. Do multiple ingests for large sites

### File Access

`ingest_file` requires the file to exist on the MCP server's filesystem. For cloud-hosted clients, use `ingest_text` with the file content instead.
