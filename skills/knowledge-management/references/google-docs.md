# Google Docs Reference

## Google Docs Workflow

### Step 1: Check Available Content

**Search for related documents:**
```
Call mcp__google-workspace__search_docs with:
  - query: "[topic keywords]"
  - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
```

Or search in Drive:
```
Call mcp__google-workspace__search_drive_files with:
  - query: "name contains '[topic]' and mimeType = 'application/vnd.google-apps.document'"
  - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
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
2. Get current content:
   ```
   Call mcp__google-workspace__get_doc_content with:
     - documentId: [FROM: search results or user-provided URL. NEVER fabricate.]
     - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
   ```
3. Append with timestamp:
   ```
   Call mcp__google-workspace__modify_doc_text with:
     - documentId: [FROM: search results or user-provided URL. NEVER fabricate.]
     - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
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

Based on plugin config `docs.organization` setting:

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
  - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
```

**Creation in folder:**
```
Call mcp__google-workspace__create_drive_file with:
  - name: "[suggested title]"
  - mimeType: "application/vnd.google-apps.document"
  - parents: ["folder_id"]
  - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
```

- `parents`: [FROM: config `default_folder_id` or user input. NEVER construct.]

Then add content:
```
Call mcp__google-workspace__modify_doc_text with:
  - documentId: "[new doc id]"
  - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
  - operations: [
      {
        "type": "insert",
        "text": "[user's exact content - do not modify]",
        "index": 1
      }
    ]
```

- `documentId`: [FROM: `create_doc` or `create_drive_file` response. NEVER fabricate.]

Confirm success with link to new document.

---

## Tool Parameters

### mcp__google-workspace__search_docs

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| query | string | Yes | Search terms | User topic - OK to construct |
| user_google_email | string | Yes | Google account email | Config `google_email` ONLY |

Returns list of matching documents.

### mcp__google-workspace__search_drive_files

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| query | string | Yes | Drive query syntax | User topic - OK to construct |
| user_google_email | string | Yes | Google account email | Config `google_email` ONLY |

Use for more precise searches. Query syntax:
- `name contains 'term'` - Title search
- `fullText contains 'term'` - Content search
- `mimeType = 'application/vnd.google-apps.document'` - Docs only
- Combine with `and` / `or`

### mcp__google-workspace__get_doc_content

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| documentId | string | Yes | Document ID from URL or search | Search results or user URL |
| user_google_email | string | Yes | Google account email | Config `google_email` ONLY |

Returns document structure with content.

### mcp__google-workspace__create_doc

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| title | string | Yes | Document title | User input - OK to suggest |
| user_google_email | string | Yes | Google account email | Config `google_email` ONLY |

Creates empty document. Returns document ID.

### mcp__google-workspace__create_drive_file

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| name | string | Yes | File name | User input - OK to suggest |
| mimeType | string | Yes | `application/vnd.google-apps.document` for Docs | Constant |
| parents | array | No | Array of folder IDs | Config `default_folder_id` or user input |
| user_google_email | string | Yes | Google account email | Config `google_email` ONLY |

Creates file in Drive with specified type and location.

### mcp__google-workspace__modify_doc_text

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| documentId | string | Yes | Target document ID | Previous API response |
| operations | array | Yes | Array of text operations | Generated content |
| user_google_email | string | Yes | Google account email | Config `google_email` ONLY |

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

### mcp__google-workspace__share_drive_file

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| fileId | string | Yes | Document/file ID | Previous API response |
| email | string | Yes | Email to share with | User input |
| role | string | Yes | "writer", "reader", etc. | User input |
| user_google_email | string | Yes | Google account email | Config `google_email` ONLY |

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
  - fileId: [FROM: previous API response. NEVER fabricate.]
  - email: [FROM: user input. NEVER guess.]
  - role: [FROM: user input]
  - user_google_email: [FROM: config "google_email". NEVER infer from Atlassian or any other backend. If not in config, ASK the user.]
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

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| user_google_email | Config `google_email` ONLY | Infer from Atlassian, GitLab, domain names, or any other source |
| documentId | Search results or user-provided URL | Fabricate or guess |
| folderId | Config `default_folder_id` or user input | Construct |
| fileId | Search/list results or create response | Fabricate |
| query | User topic (content, not identifier) | N/A |
