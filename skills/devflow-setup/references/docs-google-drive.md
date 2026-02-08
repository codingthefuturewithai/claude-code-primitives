# Google Drive — Detection & Setup

## Phase 1: Detection

Test MCP access:
```
Call mcp__google-drive__search_files with:
  - query: "test"
  - max_results: 1
```

No email parameter needed. Google Drive MCP uses OAuth-based authentication.

---

## Phase 2A: MCP Detected (search_files succeeds)

> "Google Drive MCP is connected."

Continue to Organization Settings below.

---

## Phase 2B: MCP Not Detected (search_files fails)

> "I don't have access to Google Drive MCP."
>
> "Google Drive MCP is required for Google Drive integration."
>
> "Options:"
> 1. I already set it up — Help me troubleshoot
> 2. Help me set it up from scratch
> 3. Skip Google Drive integration

### Option 1: Troubleshooting

> "To troubleshoot your Google Drive MCP connection:
>
> **Step 1: Verify MCP server is running**
> Check with `/mcp` — you should see `google-drive` listed and connected.
>
> **Step 2: Verify it was added correctly**
> The MCP server should have been added with `claude mcp add`.
>
> **Step 3: Restart Claude Code**
> Quit and relaunch Claude Code, then re-run `/devflow-setup`."
>
> **Common issues:**
>
> | Issue | Solution |
> |-------|----------|
> | Not in `/mcp` list | MCP server not added — run `claude mcp add` |
> | Shows disconnected | MCP server process not running |
> | Auth errors | Re-authenticate with the MCP server |

After troubleshooting:
> 1. I've completed these steps — Try detection again
> 2. Skip Google Drive for now

If "Try again" → retry from Phase 1.

### Option 2: First-Time Setup

> "To set up Google Drive MCP:
>
> 1. Follow the setup instructions in the Google Drive MCP server repository
> 2. Add the MCP server to Claude Code with `claude mcp add`
> 3. Restart Claude Code
> 4. Re-run `/devflow-setup`"

### Option 3: Skip

Set `DOCS_BACKEND = "none"`, `DOCS_ENABLED = false` → return to SKILL.md.

---

## Organization Settings (after detection confirmed)

> "How should files be organized in Google Drive?"
> 1. Manual — I'll manage file locations myself
> 2. Default folder — Upload to a specific folder
> 3. Ask each time — Prompt for location when uploading

**If "Default folder":**
> "What's the Google Drive folder ID?
>
> **To find a folder ID:**
> 1. Open folder in Google Drive
> 2. Look at URL: `https://drive.google.com/drive/folders/[FOLDER_ID]`
> 3. Copy the [FOLDER_ID] part
>
> Enter folder ID:"

Store:
- `DOCS_BACKEND = "google-drive"`
- `DOCS_ENABLED = true`
- `ORGANIZATION = [manual/default-folder/ask-each-time]`
- `DEFAULT_FOLDER_ID = [folder ID, if default-folder]`

Return to SKILL.md for next step.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `backend` | `google-drive` |
| `organization` | `manual`, `default-folder`, or `ask-each-time` |
| `default_folder_id` | Optional — Google Drive folder ID |
