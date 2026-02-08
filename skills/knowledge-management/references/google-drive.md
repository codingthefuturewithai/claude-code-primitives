# Google Drive Reference

## Google Drive Workflow

### Step 1: Search for Existing Content

**Search for related files:**
```
Call mcp__google-drive__search_files with:
  - query: "[topic keywords]"
```

Optionally filter by file type (e.g., `file_type: "document"`, `file_type: "spreadsheet"`).

Show results to user. If related content already exists on Drive, inform them before proceeding.

### Step 2: Determine How to Store

**Flag overrides (skip asking):**
- `--separate` → Go to Upload to Google Drive Workflow
- `--update` + related file found → Inform user: Google Drive MCP uploads files but does not edit existing Google Docs inline. Suggest downloading, editing locally, and re-uploading, or editing directly in Google Drive UI.

**No flags (default):**

If related file found in Step 1 → Ask the user:
> I found a related file: '[title]'
>
> How would you like to handle this?
> 1. Upload as a new file alongside it
> 2. Download the existing file for local editing
> 3. Cancel

STOP and wait for response. Then route accordingly.

If no related file found → Go to Upload to Google Drive Workflow (no need to ask)

---

## Upload to Google Drive Workflow

The user may provide:
- **A local file** (any format: PDF, PPTX, spreadsheet, markdown, image, etc.) → upload as-is
- **A URL** → Google Drive MCP doesn't ingest URLs. Suggest RAG Memory for URLs, or the user downloads the file first, then uploads.
- **Raw text/information** (no file) → write to a temp `.md` file, then upload

### Determine Destination Folder

Based on plugin config `docs.organization` setting:

**If "manual":**
- Upload file without specific folder
- Return file link to user

**If "default-folder":**
- Use `default_folder_id` from config

**If "ask-each-time":**
- Ask user: "Where should I upload this file?"
- Options: Default folder, specific folder ID, or no folder

### Upload

**If user provided a file path:**
```
Call mcp__google-drive__upload_file with:
  - local_path: [user's file path]
  - folder_id: [FROM: config default_folder_id or user input. NEVER construct.]
  - file_name: [original filename or user-specified name]
```

**If user provided raw text (no file):**
1. Write content to a temp `.md` file
2. Upload:
```
Call mcp__google-drive__upload_file with:
  - local_path: [temp file path]
  - folder_id: [FROM: config default_folder_id or user input. NEVER construct.]
  - file_name: "[Title].md"
```

Confirm success with file link.

---

## Retrieve from Google Drive

**Download a file:**
```
Call mcp__google-drive__download_file with:
  - file_id: [FROM: search results or user. NEVER fabricate.]
  - local_path: [destination path]
  - export_format: [optional - for Google Workspace files]
```

Export formats for Google Workspace files:
- Google Docs → `txt`, `pdf`, `docx`
- Google Sheets → `csv`, `xlsx`
- Google Slides → `pdf`, `pptx`

**Get file metadata (without downloading):**
```
Call mcp__google-drive__get_file_info with:
  - file_id: [FROM: search results or user. NEVER fabricate.]
```

---

## Browse Google Drive

**List folder contents:**
```
Call mcp__google-drive__list_folder with:
  - folder_id: [FROM: config, search results, or user. NEVER construct.]
```

**Create a folder:**
```
Call mcp__google-drive__create_folder with:
  - folder_name: "[name]"
  - parent_folder_id: [FROM: config or user. NEVER construct.]
```

---

## Tool Parameters

### mcp__google-drive__search_files

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| query | string | Yes | Search terms | User topic - OK to construct |
| file_type | string | No | Filter by type (document, spreadsheet, etc.) | User preference |
| max_results | integer | No | Limit results | Default or user preference |

### mcp__google-drive__upload_file

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| local_path | string | Yes | Local file to upload | User input or generated temp path |
| folder_id | string | No | Destination folder | Config `default_folder_id` or user input |
| file_name | string | No | Name for uploaded file | User input or original filename |

### mcp__google-drive__download_file

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| file_id | string | Yes | File to download | Search results or user |
| local_path | string | Yes | Local destination path | User input or generated |
| export_format | string | No | Export format for Workspace files | User preference |

### mcp__google-drive__get_file_info

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| file_id | string | Yes | File to get info for | Search results or user |

### mcp__google-drive__list_folder

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| folder_id | string | No | Folder to list | Config, search results, or user |

### mcp__google-drive__create_folder

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| folder_name | string | Yes | Name for new folder | User input |
| parent_folder_id | string | No | Parent folder | Config or user input |

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| file_id | Search results, list results, or user-provided | Fabricate or guess |
| folder_id | Config `default_folder_id`, search/list results, or user input | Construct or guess |
| query | User topic (content, not identifier) | N/A |
| local_path | User-provided file path or generated temp path | N/A |
