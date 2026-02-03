# Google Docs Reference

## Google Docs Workflow

### Step 1: Check Available Content

**Search for related documents:**
```
Call mcp__google-workspace__search_docs with:
  - query: "[topic keywords]"
```

Or search in Drive:
```
Call mcp__google-workspace__search_drive_files with:
  - query: "name contains '[topic]' and mimeType = 'application/vnd.google-apps.document'"
```

Show results to user.

### Step 2: Determine How to Store

**Flag overrides (skip asking):**
- `--separate` → Go to Create New Document Workflow
- `--update` + related doc found → Go to Update Existing Document Workflow

**No flags (default):**

If related document found in Step 1 → Ask the user:
> I found a related document: '[title]'
>
> How would you like to handle this?
> 1. Update '[title]' with this information
> 2. Create a new document
> 3. Cancel

STOP and wait for response. Then route accordingly.

If no related document found → Go to Create New Document Workflow (no need to ask)

---

## Update Existing Document Workflow

Append new content to an existing document.

1. Extract `documentId` from search results (or from URL provided by user)
2. Get current content: `mcp__google-workspace__get_doc_content(documentId)`
3. Append with timestamp using `mcp__google-workspace__modify_doc_text`:
   ```
   Call mcp__google-workspace__modify_doc_text with:
     - documentId: "[doc id]"
     - operations: [
         {
           "type": "insert",
           "text": "\n\n---\n\n**Added [YYYY-MM-DD HH:MM]:**\n[new content]",
           "index": [end of document]
         }
       ]
   ```
4. Confirm success

---

## Create New Document Workflow

### Determine Location

Based on devflow-config.md `docs.organization` setting:

**If "manual":**
- Create document without specific folder
- Return document URL to user

**If "default-folder":**
- Use `default_folder_id` from config
- Create document in that folder

**If "ask-each-time":**
- Ask user: "Where should I create this document?"
- Options: Default folder, specific folder ID, or no folder

### Create Document

**Simple creation (no folder):**
```
Call mcp__google-workspace__create_doc with:
  - title: "[suggested title]"
```

**Creation in folder:**
```
Call mcp__google-workspace__create_drive_file with:
  - name: "[suggested title]"
  - mimeType: "application/vnd.google-apps.document"
  - parents: ["folder_id"]
```

Then add content:
```
Call mcp__google-workspace__modify_doc_text with:
  - documentId: "[new doc id]"
  - operations: [
      {
        "type": "insert",
        "text": "[user's exact content - do not modify]",
        "index": 1
      }
    ]
```

Confirm success with link to new document.

---

## Tool Parameters

### mcp__google-workspace__search_docs(query)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Search terms |

Returns list of matching documents.

### mcp__google-workspace__search_drive_files(query)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Drive query syntax |

Use for more precise searches. Query syntax:
- `name contains 'term'` - Title search
- `fullText contains 'term'` - Content search
- `mimeType = 'application/vnd.google-apps.document'` - Docs only
- Combine with `and` / `or`

### mcp__google-workspace__get_doc_content(documentId)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| documentId | string | Yes | Document ID from URL or search |

Returns document structure with content.

### mcp__google-workspace__create_doc(title)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Document title |

Creates empty document. Returns document ID.

### mcp__google-workspace__create_drive_file(name, mimeType, parents)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | File name |
| mimeType | string | Yes | `application/vnd.google-apps.document` for Docs |
| parents | array | No | Array of folder IDs |

Creates file in Drive with specified type and location.

### mcp__google-workspace__modify_doc_text(documentId, operations)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| documentId | string | Yes | Target document ID |
| operations | array | Yes | Array of text operations |

**Operation types:**
```json
{
  "type": "insert",
  "text": "text to insert",
  "index": 1
}
```

```json
{
  "type": "delete",
  "startIndex": 10,
  "endIndex": 20
}
```

---

## Edge Cases

### Document ID Extraction

Document ID can be extracted from URLs:
```
https://docs.google.com/document/d/[DOCUMENT_ID]/edit
```

### Content Formatting

Google Docs uses structural elements. For simple text:
- Insert plain text with operations
- Newlines work as expected
- For formatting (bold, headers), use batch_update_doc

### Folder Organization

Google Docs doesn't have "spaces" like Confluence. Organization is through Drive folders.

**Recommended structure:**
```
My Drive/
└── DevFlow/
    ├── Plans/
    │   └── [Issue-ID] Implementation Plan
    └── Documentation/
        └── Technical Docs
```

### Permissions

Documents inherit permissions from parent folder. To share:
```
Call mcp__google-workspace__share_drive_file with:
  - fileId: "[doc id]"
  - email: "user@example.com"
  - role: "writer"
```

---

## Comparison with Confluence

| Aspect | Confluence | Google Docs |
|--------|------------|-------------|
| Organization | Spaces (enforced hierarchy) | Folders (flexible) |
| Search | CQL + semantic | Drive query syntax |
| IDs | Page ID | Document ID (from URL) |
| Content format | Storage XML | Structural JSON |
| Updates | Version-based | Operation-based |
| Permissions | Space-level | File-level |
