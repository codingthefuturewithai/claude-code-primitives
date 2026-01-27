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

## RAG Memory Workflow

### Step 1: Discover Collections

1. Call `list_collections()` to get all collections
2. For EACH collection, call `get_collection_metadata_schema(collection_name)`
3. Store the `domain`, `domain_scope`, and `routing` values (routing.examples and routing.exclusions)

### Step 2: Search for Related Content

```
search_documents(query="What content exists about [topic]?", limit=5)
```

Show results to user.

### Step 3: Check Agent Preferences

Query for user's routing preferences:
```
search_documents(
    query="What are the user's routing preferences for [domain] content?",
    collection_name="agent-preferences"
)
```

Use domain values like "Operations", "Engineering" from Step 1.

### Step 4: Determine How to Store

**Flag overrides (skip asking):**
- `--quick` → Go to Quick Note Workflow
- `--separate` → Go to Full Document Workflow
- `--update` + related content found → Go to Update Existing Workflow

**No flags → Use judgment, then ask:**

First, assess whether this feels like a quick note:
- Short, informal content (a few sentences, a thought, a reminder)
- "Jot this down" energy vs "file this away" energy
- User wants to capture something without deciding where it belongs
- Unstructured - no clear organization or headers

**If it feels like a quick note**, present quick note as the recommended option:

If related content found:
> I found a related document: '[title]'
>
> How would you like to handle this?
> 1. Save as quick note (recommended - can merge later)
> 2. Update '[title]' with this information
> 3. Create a full document
> 4. Cancel

If no related content:
> This seems like a quick note. How would you like to store it?
> 1. Save as quick note (recommended - can merge later)
> 2. Create a full document
> 3. Cancel

**If it feels like a full document** (structured, reference material, meant to be permanent):

If related content found:
> I found a related document: '[title]'
>
> How would you like to handle this?
> 1. Update '[title]' with this information
> 2. Create a full document
> 3. Save as quick note
> 4. Cancel

If no related content → Go to Full Document Workflow (collection selection)

STOP and wait for response. Then route accordingly.

---

## Quick Note Workflow

Quick notes go to the dedicated `quick-notes` system collection as individual documents.

1. Ingest to the `quick-notes` collection:
   ```
   ingest_text(
       content="[the note content]",
       collection_name="quick-notes",
       document_title="[brief title or first ~50 chars]",
       actor_type="[your product name]"
   )
   ```

2. Confirm: "Saved to Quick Notes. You can merge related notes later from the Quick Notes view."

**About quick-notes collection:**
- System collection, auto-created on server startup
- Cannot be deleted (protected)
- Has dedicated UI view for browsing and managing notes
- Users can select multiple notes and merge them into a single document
- Merge operation tracks full provenance in audit logs

---

## Update Existing Workflow

Append new content to an existing document.

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

## Full Document Workflow

### Select Collection

1. **Check agent-preferences first** (from Step 3):
   - If user has an explicit routing preference for this content type, use that collection
   - User decisions always override collection routing hints

2. **Score remaining collections** using routing hints from Step 1:
   - Use `routing.examples` to understand what TYPE of content fits each collection
   - Use `routing.exclusions` as negative signals (not hard filters)
   - These are illustrative examples - match the character of content, not literal text

3. **Present top 2-3 collections** with reasoning:
   > Based on the content, I recommend:
   > 1. [collection] - similar to: '[matched example type]'
   > 2. [collection] - similar to: '[matched example type]'

4. Let user confirm or correct.

### Suggest Topic

Suggest a topic. Ask user to accept or modify.

### Ingest

Ingest the content as-is (do not expand or modify). Use the appropriate tool based on input type:
- File path → `ingest_file()`
- URL → `ingest_url()`
- Raw text → `ingest_text()`

### Offer to Save Preference

If no preference existed in Step 3:
> Would you like me to remember that [domain] content goes to [collection]?

If yes, save to agent-preferences collection.

---

## Tool Parameters

### list_collections()

No parameters required. Returns array of collection names.

### get_collection_info(collection_name)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_name | string | Yes | Name of collection |

Returns: `name`, `domain`, `domain_scope`, `description`

### get_collection_metadata_schema(collection_name)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_name | string | Yes | Name of collection |

Returns everything from `get_collection_info()` plus:
- `metadata_schema.routing.examples` - Content that SHOULD route here
- `metadata_schema.routing.exclusions` - Content that should NOT route here

**Use this** instead of `get_collection_info()` when you need routing hints.

### search_documents(query, collection_name, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language question |
| collection_name | string | No | Limit to specific collection |
| limit | int | No | Max results (default 5) |

### ingest_text(content, collection_name, document_title, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| content | string | Yes | Text content |
| collection_name | string | Yes | Target collection |
| document_title | string | Yes | Document title |
| topic | string | No | Topic for relevance |
| mode | string | No | "ingest" (default) or "reingest" |
| actor_type | string | **Yes** | Your AI assistant name |

### ingest_url(url, collection_name, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | URL to ingest |
| collection_name | string | Yes | Target collection |
| topic | string | No | Topic for relevance |
| follow_links | bool | No | Crawl linked pages |
| max_pages | int | No | Max pages (default 10, max 20) |
| mode | string | No | "ingest" (default) or "reingest" |
| actor_type | string | **Yes** | Your AI assistant name |

### ingest_file(file_path, collection_name, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | Yes | Local file path |
| collection_name | string | Yes | Target collection |
| topic | string | No | Topic for relevance |
| mode | string | No | "ingest" (default) or "reingest" |
| actor_type | string | **Yes** | Your AI assistant name |

### list_documents(collection_name)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_name | string | Yes | Collection to list |

Returns documents with `document_id` and `title`.

### get_document_by_id(document_id)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| document_id | string | Yes | Document ID |

Returns full document including `content` field.

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

### Large Content

For URLs with many pages:
1. First call `analyze_website(url)` to see structure
2. Use `max_pages=20` limit per ingest
3. Do multiple ingests for large sites

### File Access

`ingest_file` requires the file to exist on the MCP server's filesystem. For cloud-hosted clients, use `ingest_text` with the file content instead.
