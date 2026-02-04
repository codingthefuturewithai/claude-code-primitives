# Google Docs — Detection & Setup

## Phase 1: Detection

**IMPORTANT:** Do NOT ask for email yet. First check if MCP is accessible.

Test MCP access:
```
Call mcp__google-workspace__list_drive_items with:
  - page_size: 1
```

**DO NOT** pass `user_google_email` parameter. Let MCP use its default configured account.

**Technical Note:** The Google Workspace MCP server is pre-configured with a `USER_GOOGLE_EMAIL` in its `.env` file. When called without the parameter, it uses this default. We're testing if the MCP server is accessible and authenticated.

---

## Phase 2A: MCP Detected (list_drive_items succeeds)

### Extract Configured Email

The Google Workspace MCP is accessible.

**Extract email from tool parameter defaults:**
When you load Google Workspace tools via ToolSearch, check the `user_google_email` parameter schema for a default value. This default comes from the MCP server's configuration.

Example: `"user_google_email": {"default": "timkitch@gmail.com"}`

**Fallback if extraction fails:**
> "I have access to Google Workspace MCP, but couldn't automatically determine which Google account it's configured with.
>
> **Which Google account did you authenticate with when setting up Google Workspace MCP?**
> (This is the account you used at http://localhost:8847/oauth2/authorize when you granted permissions.)
>
> Enter the Google email address:"

Store the extracted or user-provided email as `DETECTED_EMAIL`.

### Confirm with User

> "I have access to Google Workspace MCP. It's configured with: **[DETECTED_EMAIL]**"
>
> "Is this the Google account you want to use for DevFlow documentation?"
> 1. Yes - Use [DETECTED_EMAIL]
> 2. No - I want to use a different account
> 3. Help - Explain what this means

**If "Yes":**
- Store `DETECTED_EMAIL` as `google_email` in config
- Continue to Organization Settings below

**If "No - Different account":**
> "You have Google Workspace MCP configured with [DETECTED_EMAIL], but want to use a different account.
>
> **Important:** Google Workspace MCP supports one Google account per server instance.
>
> To use a different account, you can:"
> 1. Re-configure the current instance with a different account
> 2. Set up a second Google Workspace MCP instance (advanced)
> 3. Use [DETECTED_EMAIL] for DevFlow anyway
> 4. Skip Google Docs integration

**If option 1 (re-configure):**
> "To re-configure your Google Workspace MCP with a different account:
>
> **Step 1: Reset OAuth authentication**
> ```bash
> cd ~/google_workspace_mcp  # or your actual MCP directory
> docker compose down
> docker volume rm google_workspace_mcp_store_creds
> docker compose up -d
> ```
>
> **Step 2: Re-authenticate in browser**
> Open: http://localhost:8847/oauth2/authorize
> Sign in with the Google account you want to use
>
> **Step 3: Re-run this setup**
> `/devflow-setup`
>
> **Warning:** This will disconnect [DETECTED_EMAIL]."

**If option 2 (second instance):**
> "Setting up a second Google Workspace MCP instance is an advanced configuration.
>
> This requires:
> - Separate OAuth credentials in Google Cloud Console
> - Different port (e.g., 8848 instead of 8847)
> - Separate docker-compose.yml and .env files
> - Adding second MCP server to Claude Code with different name
>
> For most users, option 1 (re-configure) is simpler.
>
> Would you like:"
> 1. See the second instance setup guide anyway
> 2. Go back and choose option 1 (re-configure)
> 3. Skip Google Docs integration

If "See guide": Read and display `GOOGLE_WORKSPACE_MCP_SETUP.md` from this repo's root, with a note about using different port and name.

**If option 3 (use detected email anyway):**
- Store `DETECTED_EMAIL` as `google_email` → continue to Organization Settings

**If option 4 (skip):**
- Set `DOCS_BACKEND = "none"`, `DOCS_ENABLED = false` → return to SKILL.md

**If "Help":**
> "**What is Google Workspace MCP?**
>
> Google Workspace MCP is a server running in Docker that gives Claude Code access to your Google Docs, Drive, Gmail, and other Google services.
>
> **How it works:**
> - You authenticated via browser when setting up the MCP server
> - You granted permissions to access your Google account
> - The MCP server stores these credentials securely
> - Claude Code talks to the MCP server, which talks to Google
>
> **Current setup:**
> - Your MCP is configured with: [DETECTED_EMAIL]
> - This is the account you authenticated in the OAuth flow
> - DevFlow will use this account for creating/reading Google Docs"
>
> Then re-present the Yes/No/Help options.

---

## Phase 2B: MCP Not Detected (list_drive_items fails)

> "I don't have access to Google Workspace MCP."
>
> "Google Workspace MCP is required for Google Docs integration. It runs as a Docker container and handles authentication with Google."
>
> "Do you already have Google Workspace MCP set up, or do you need help setting it up?"
> 1. I already set it up — Help me connect it
> 2. Help me set it up — First-time setup
> 3. Skip Google Docs integration

### Option 1: Already Set Up — Troubleshooting

> "To connect your existing Google Workspace MCP to Claude Code:
>
> **Step 1: Verify container is running**
> ```bash
> docker ps --filter "name=gws_mcp"
> ```
> You should see a container with status 'Up'.
>
> If not running:
> ```bash
> cd [YOUR_MCP_DIRECTORY]
> docker compose up -d
> ```
>
> **Step 2: Find your MCP port**
> Check your `docker-compose.yml` or `.env` file for `WORKSPACE_MCP_PORT`.
> Common ports: 8847 (default), 8848, 8849
>
> **Step 3: Add to Claude Code**
> ```bash
> claude mcp add --transport http -s user google-workspace http://localhost:[PORT]/mcp
> ```
> Replace [PORT] with your actual port.
>
> **Step 4: Restart Claude Code** (Cmd+Q and relaunch)
>
> **Step 5: Verify**
> Run `/mcp` — should see: `google-workspace: http://localhost:[PORT]/mcp (HTTP) - ✓ Connected`"
>
> **Common issues:**
>
> | Issue | Solution |
> |-------|----------|
> | Connection refused | Container not running or wrong port |
> | 404 Not Found | Wrong URL (should end in /mcp) |
> | Not in /mcp list | Didn't restart Claude Code |

After troubleshooting:
> 1. I've completed these steps — Try detection again
> 2. I'm stuck — Show me the detailed setup guide
> 3. Skip Google Docs for now

If "Try again" → retry from Phase 1.
If "Detailed guide" → Read and display `GOOGLE_WORKSPACE_MCP_SETUP.md` from this repo's root.

### Option 2: First-Time Setup

> "I can guide you through setting up Google Workspace MCP.
>
> **What you'll need:**
> - Docker installed and running
> - A Google account
>
> **Setup process:**
> 1. Set up Google Cloud Console (OAuth credentials)
> 2. Clone the MCP repository
> 3. Configure environment variables
> 4. Build and start Docker container
> 5. Authenticate via browser
> 6. Connect to Claude Code
>
> **Options:**
> 1. Show me the complete setup guide (I'll follow it myself)
> 2. Walk me through step-by-step (you guide me)
> 3. I'll do this later — Skip for now

**If "Complete setup guide":**
Read and display `GOOGLE_WORKSPACE_MCP_SETUP.md` from this repo's root. Then:
> "When you've completed setup, re-run `/devflow-setup` to configure DevFlow."

**If "Walk me through":**
Read `GOOGLE_WORKSPACE_MCP_SETUP.md` and guide user through each part:
1. Check if already set up
2. Google Cloud Console (OAuth setup)
3. Clone and configure (`.env`, `docker-compose.yml`)
4. Build and start container
5. OAuth authentication in browser
6. Add to Claude Code
7. Test: return to Phase 1

Wait for user confirmation at each step.

### Option 3: Skip

Set `DOCS_BACKEND = "none"`, `DOCS_ENABLED = false` → return to SKILL.md.

---

## Organization Settings (after email confirmed)

> "How should documents be organized in Google Drive?"
> 1. Manual — I'll provide doc links when relevant
> 2. Default folder — Create in a specific folder
> 3. Ask each time — Prompt for location when creating

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
- `DOCS_BACKEND = "google-docs"`
- `DOCS_ENABLED = true`
- `GOOGLE_EMAIL = [confirmed email]`
- `ORGANIZATION = [manual/default-folder/ask-each-time]`
- `DEFAULT_FOLDER_ID = [folder ID, if default-folder]`

Return to SKILL.md for next step.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `backend` | `google-docs` |
| `google_email` | User-confirmed email address |
| `organization` | `manual`, `default-folder`, or `ask-each-time` |
| `default_folder_id` | Optional — Google Drive folder ID |
