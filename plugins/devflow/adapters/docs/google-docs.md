# Google Docs Documentation Adapter

## Overview

Adapter patterns for Google Docs operations via Google Workspace MCP.

---

## Connection Setup

No initial setup call needed. Operations use document IDs directly.

Document ID can be extracted from URLs:
```
https://docs.google.com/document/d/[DOCUMENT_ID]/edit
```

### Google Email (CRITICAL)

**ALWAYS** pass `user_google_email` from the DevFlow config on every Google Workspace MCP call.

```
Read devflow-config.md → Extract google_email value → Pass as user_google_email
```

**NEVER** guess or infer the Google email from other context (Atlassian, GitLab, etc.). The user explicitly chose this email during `/devflow:admin:setup`.

---

## Operations

### List Documents in Drive

```
Call mcp__google-workspace__list_drive_items with:
  - folderId: "root" (or specific folder ID)
  - mimeType: "application/vnd.google-apps.document"
```

Returns array with:
- `id` - Document ID
- `name` - Document name
- `mimeType` - File type
- `webViewLink` - Browser URL

---

### Get Document Content

```
Call mcp__google-workspace__get_doc_content with:
  - documentId: "1ABC...xyz"
```

Returns document structure with:
- `title` - Document title
- `body.content` - Array of structural elements

---

### Create Document

```
Call mcp__google-workspace__create_doc with:
  - title: "Document Title"
```

Optional - create in specific folder:
```
Call mcp__google-workspace__create_drive_file with:
  - name: "Document Title"
  - mimeType: "application/vnd.google-apps.document"
  - parents: ["folder_id"]
```

---

### Update Document

**Modify text:**
```
Call mcp__google-workspace__modify_doc_text with:
  - documentId: "1ABC...xyz"
  - operations: [
      {
        "type": "insert",
        "text": "New text to insert",
        "index": 1
      }
    ]
```

**Find and replace:**
```
Call mcp__google-workspace__find_and_replace_doc with:
  - documentId: "1ABC...xyz"
  - find: "old text"
  - replace: "new text"
```

**Insert elements:**
```
Call mcp__google-workspace__insert_doc_elements with:
  - documentId: "1ABC...xyz"
  - elements: [...]
```

---

### Search Documents

```
Call mcp__google-workspace__search_docs with:
  - query: "search term"
```

Or search in Drive:
```
Call mcp__google-workspace__search_drive_files with:
  - query: "name contains 'plan' and mimeType = 'application/vnd.google-apps.document'"
```

---

### Add Comment

```
Call mcp__google-workspace__create_document_comment with:
  - documentId: "1ABC...xyz"
  - content: "Comment text"
```

To comment on specific text, include selection info.

---

### Share Document

```
Call mcp__google-workspace__share_drive_file with:
  - fileId: "1ABC...xyz"
  - email: "user@example.com"
  - role: "writer" | "reader" | "commenter"
```

---

## Content Format

Google Docs uses structural elements:

```json
{
  "body": {
    "content": [
      {
        "paragraph": {
          "elements": [
            {"textRun": {"content": "Text content"}}
          ]
        }
      }
    ]
  }
}
```

For creating/updating, use operations-based approach rather than raw structure.

---

## Organization Patterns

### No Enforced Structure

Unlike Confluence (which uses Spaces), Google Docs uses Drive folders. Organization is user-defined.

### Suggested DevFlow Convention

```
My Drive/
└── DevFlow/
    ├── Plans/
    │   └── [Issue-ID] Implementation Plan
    └── Documentation/
        └── Technical Docs
```

### Configuration Options

In `devflow-config.md`:
```markdown
## Documentation
backend: google-docs
organization: manual
# Options:
#   manual - User provides doc link when relevant
#   default-folder - Create in specified folder
#   ask-each-time - Prompt for location
default_folder_id: 1ABC...xyz (if organization = default-folder)
```

---

## Key Differences from Confluence

| Aspect | Confluence | Google Docs |
|--------|------------|-------------|
| Organization | Spaces (enforced) | Folders (flexible) |
| IDs | Page ID | Document ID (from URL) |
| Content format | Storage XML | Structural JSON |
| Updates | Version-based | Operation-based |
| Hierarchy | Parent pages | Folder structure |
| Search | CQL | Drive query syntax |

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | OAuth expired | Re-authenticate |
| 403 | Access denied | Check sharing permissions |
| 404 | Document not found | Verify document ID |
| 429 | Rate limited | Wait and retry |

---

## OAuth Scope Requirements

Required scopes for full functionality:
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`

If operations fail with permission errors, re-run OAuth authorization flow.
