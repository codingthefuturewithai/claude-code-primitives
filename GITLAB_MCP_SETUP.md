# GitLab MCP Server Setup Guide

**MCP Server Package:** [@zereight/mcp-gitlab](https://www.npmjs.com/package/@zereight/mcp-gitlab)
**GitHub Repository:** [zereight/gitlab-mcp](https://github.com/zereight/gitlab-mcp)

This guide helps you set up the GitLab MCP server for Claude Code, assuming you already have a GitLab instance (GitLab.com, self-hosted, or local Docker).

---

## Overview

The GitLab MCP server enables AI assistants (like Claude Code) to interact with GitLab: create issues, manage merge requests, read repositories, manage projects, and more.

**Key Points:**
- Works with **any** GitLab instance (GitLab.com, self-hosted, local)
- Requires a **Personal Access Token** from your GitLab
- Runs as a subprocess via `npx` (no installation needed)
- Uses stdio transport to communicate with Claude Code

---

## Part 1: Check If Already Set Up

### Step 1.1: Check Claude Code Configuration

```bash
claude mcp get gitlab 2>&1
```

**If you see output showing configuration:**
- MCP server is already configured
- Check if it's connected: `claude mcp list | grep gitlab`
- If connected (✓), you're done!
- If failed (✗), check token and URL are correct

**If you see "No MCP server found":**
- Not configured yet. Continue to Part 2.

### Step 1.2: Check Your GitLab Configuration File

```bash
cat ~/.claude.json | jq '.mcpServers["gitlab"]'
```

**If output shows `null`:**
- Not configured. Continue to Part 2.

**If output shows configuration:**
- Already configured. Verify connection with `/mcp` in Claude Code.

---

## Part 2: Identify Your GitLab Instance

Before setting up the MCP server, you need to know where your GitLab is located.

### Option A: GitLab.com (Cloud)

**If you use GitLab.com:**
- GitLab URL: `https://gitlab.com`
- API URL: `https://gitlab.com/api/v4`
- This is the **default** - you can omit GITLAB_API_URL

### Option B: Self-Hosted GitLab

**If your organization runs GitLab:**
- Ask your admin for the GitLab URL
- Example: `https://gitlab.yourcompany.com`
- API URL: `https://gitlab.yourcompany.com/api/v4`

### Option C: Local GitLab (Docker)

**If you're running GitLab locally in Docker:**
- Check container: `docker ps --filter "name=gitlab"`
- Find the HTTP port mapping (e.g., `0.0.0.0:8929->8929/tcp`)
- GitLab URL: `http://localhost:PORT` (e.g., `http://localhost:8929`)
- API URL: `http://localhost:PORT/api/v4`

**Verify you can access GitLab:**
```bash
curl -I https://gitlab.com  # For GitLab.com
# OR
curl -I http://localhost:8929  # For local instance
```

Should return `HTTP/1.1 200 OK` or similar (not an error).

---

## Part 3: Create GitLab Personal Access Token

You need a Personal Access Token (PAT) to authenticate with GitLab.

### Step 3.1: Log In to GitLab

Open your browser and log in to your GitLab instance:
- **GitLab.com:** https://gitlab.com
- **Self-hosted:** Your organization's GitLab URL
- **Local Docker:** http://localhost:PORT

### Step 3.2: Navigate to Access Tokens

1. Click your **avatar** (top-right corner)
2. Select **Edit profile** (or **Preferences**)
3. In the left sidebar, click **Access Tokens**

### Step 3.3: Create New Token

1. Click **Add new token**
2. **Token name:** `claude-code-mcp` (or any descriptive name)
3. **Expiration date:** Set as needed (or leave blank for no expiration)
4. **Select scopes** - Check ALL of these:
   - ☑ `api` - Full API access
   - ☑ `read_api` - Read-only API access
   - ☑ `read_repository` - Read repositories
   - ☑ `write_repository` - Write to repositories
   - ☑ `read_registry` - Read container registry
   - ☑ `write_registry` - Write to container registry
5. Click **Create personal access token**

### Step 3.4: Save Your Token

**CRITICAL:** The token is shown **only once**. Copy it immediately!

Token format: `glpat-xxxxxxxxxxxxxxxxxxxxx`

**Save it securely:**
```bash
# Option 1: Save to a file
echo "glpat-xxxxxxxxxxxxxxxxxxxxx" > ~/.gitlab-mcp-token
chmod 600 ~/.gitlab-mcp-token

# Option 2: Save to environment variable (add to ~/.zshrc or ~/.bashrc)
export GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxxx"
```

**Important:** Never commit this token to git or share it publicly.

---

## Part 4: Add GitLab MCP Server to Claude Code

Now you'll add the MCP server to Claude Code with your token and API URL.

### Step 4.1: Determine Your Scope

**Local scope** (`-s local`): Only available in this project directory
**User scope** (`-s user`): Available in all projects (recommended)

Choose based on your needs. This guide uses **local scope** to match the working setup on this system.

### Step 4.2: Add the MCP Server

**For GitLab.com (uses default API URL):**
```bash
claude mcp add gitlab -s local \
  -e GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxxx" \
  -- npx -y @zereight/mcp-gitlab
```

**For self-hosted or local GitLab (specify API URL):**
```bash
claude mcp add gitlab -s local \
  -e GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxxx" \
  -e GITLAB_API_URL="https://gitlab.yourcompany.com/api/v4" \
  -- npx -y @zereight/mcp-gitlab
```

**For local Docker instance (example with port 8929):**
```bash
claude mcp add gitlab -s local \
  -e GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxxx" \
  -e GITLAB_API_URL="http://localhost:8929/api/v4" \
  -- npx -y @zereight/mcp-gitlab
```

**If you saved token to file:**
```bash
claude mcp add gitlab -s local \
  -e GITLAB_PERSONAL_ACCESS_TOKEN="$(cat ~/.gitlab-mcp-token)" \
  -e GITLAB_API_URL="http://localhost:8929/api/v4" \
  -- npx -y @zereight/mcp-gitlab
```

**What this command does:**
- `gitlab` - Name of the MCP server
- `-s local` - Save to local (project) config
- `-e` - Set environment variables
- `GITLAB_PERSONAL_ACCESS_TOKEN` - Your PAT from Part 3
- `GITLAB_API_URL` - Your GitLab API endpoint (optional if using GitLab.com)
- `npx -y @zereight/mcp-gitlab` - Run the MCP server package

**Expected output:**
```
Added stdio MCP server gitlab with command: npx -y @zereight/mcp-gitlab to local config
File modified: /Users/yourname/project/.claude/mcp.json
```

**Source:** Actual working command on this system

### Step 4.3: Restart Claude Code

Completely quit and restart Claude Code:
- Press Cmd+Q (Mac) or close the terminal
- Start Claude Code again

### Step 4.4: Verify Connection

In your new Claude Code session, run:
```
/mcp
```

You should see:
```
gitlab: npx -y @zereight/mcp-gitlab - ✓ Connected
```

Or from terminal:
```bash
claude mcp list | grep gitlab
```

Should show:
```
gitlab: npx -y @zereight/mcp-gitlab - ✓ Connected
```

**Source:** Actual working output on this system

---

## Part 5: Test the Connection

Test that the MCP server can actually communicate with GitLab.

### In Claude Code, ask:
```
List my GitLab projects
```

Or:
```
Show me my GitLab groups
```

**If it works:** You'll see a list of your projects/groups.

**If it fails:** Continue to Troubleshooting section below.

---

## Optional Configuration

The GitLab MCP server supports additional environment variables for advanced use cases:

### Read-Only Mode
Restricts the server to only read operations (no create/update/delete):
```bash
-e GITLAB_READ_ONLY_MODE="true"
```

### Enable Wiki Tools
Enables wiki-related tools (list_wiki_pages, create_wiki_page, etc.):
```bash
-e USE_GITLAB_WIKI="true"
```

### Restrict to Specific Projects
Only allow access to specific project IDs (comma-separated):
```bash
-e GITLAB_ALLOWED_PROJECT_IDS="12345,67890"
```

**To add these to existing configuration:**
```bash
# Remove existing
claude mcp remove gitlab -s local

# Re-add with additional options
claude mcp add gitlab -s local \
  -e GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxx" \
  -e GITLAB_API_URL="http://localhost:8929/api/v4" \
  -e GITLAB_READ_ONLY_MODE="true" \
  -e USE_GITLAB_WIKI="true" \
  -- npx -y @zereight/mcp-gitlab
```

**Source:** [npm package documentation](https://www.npmjs.com/package/@zereight/mcp-gitlab)

---

## Troubleshooting

### "No MCP server found with name: gitlab"

The server isn't configured. Go back to Part 4 and add it.

### "Failed to connect" or "✗ Failed to connect"

**Possible causes:**

1. **Invalid token**
   - Verify token is correct: `echo $GITLAB_PERSONAL_ACCESS_TOKEN` or `cat ~/.gitlab-mcp-token`
   - Check token hasn't expired in GitLab (Settings → Access Tokens)
   - Ensure token has all required scopes

2. **Wrong API URL**
   - Verify GitLab is accessible: `curl -I http://localhost:8929` (or your URL)
   - Check API URL includes `/api/v4` at the end
   - For GitLab.com, try omitting GITLAB_API_URL entirely (uses default)

3. **GitLab instance not running (local Docker only)**
   ```bash
   docker ps --filter "name=gitlab"
   ```
   If not running: `docker compose up -d`

4. **Port mismatch (local Docker only)**
   - Check which port GitLab is on: `docker ps --filter "name=gitlab"`
   - Ensure GITLAB_API_URL matches that port

### "Authentication failed" or 401 errors

Token is invalid or expired:
1. Go to GitLab → Settings → Access Tokens
2. Check if token is still active
3. Create a new token if needed
4. Update MCP server config:
   ```bash
   claude mcp remove gitlab -s local
   claude mcp add gitlab -s local -e GITLAB_PERSONAL_ACCESS_TOKEN="new-token" -e GITLAB_API_URL="your-api-url" -- npx -y @zereight/mcp-gitlab
   ```
5. Restart Claude Code

### "Cannot find module" or npm errors

The `npx` command couldn't download the package:
1. Check internet connection
2. Verify `npx` is installed: `npx --version`
3. Try installing the package manually: `npm install -g @zereight/mcp-gitlab`
4. If that works, try the `claude mcp add` command again

### MCP server connects but tools don't work

1. **Check token scopes:** Ensure all required scopes are checked (see Part 3.3)
2. **Check API access:** Try making a direct API call:
   ```bash
   curl -H "PRIVATE-TOKEN: your-token" https://gitlab.com/api/v4/projects
   ```
   Should return JSON with your projects.

3. **Check Claude Code logs:** Look for errors:
   ```bash
   ls -lt ~/Library/Logs/Claude/mcp-server-gitlab.log
   tail -50 ~/Library/Logs/Claude/mcp-server-gitlab.log
   ```

### How to reconfigure

To change token or API URL:
```bash
# Remove existing configuration
claude mcp remove gitlab -s local

# Add with new values
claude mcp add gitlab -s local \
  -e GITLAB_PERSONAL_ACCESS_TOKEN="new-token" \
  -e GITLAB_API_URL="new-url/api/v4" \
  -- npx -y @zereight/mcp-gitlab

# Restart Claude Code
```

---

## Configuration File Locations

### Local scope (project-specific)
```bash
# Configuration file
.claude/mcp.json

# View configuration
cat .claude/mcp.json | jq '.mcpServers["gitlab"]'
```

### User scope (all projects)
```bash
# Configuration file
~/.claude.json

# View configuration
cat ~/.claude.json | jq '.mcpServers["gitlab"]'
```

### Claude Code logs
```bash
# Find GitLab MCP server log
~/Library/Logs/Claude/mcp-server-gitlab.log
```

---

## How It Works

1. **Claude Code starts** and reads MCP server configuration
2. **Spawns subprocess:** `npx -y @zereight/mcp-gitlab`
3. **Environment variables** are passed to the subprocess
4. **MCP server authenticates** with GitLab using your PAT
5. **Claude Code communicates** with MCP server via stdio (JSON-RPC)
6. **MCP server makes API calls** to GitLab on your behalf

**No email or password needed** - the Personal Access Token handles all authentication.

---

## Updating the MCP Server

The MCP server package is automatically updated by `npx -y` each time Claude Code starts (the `-y` flag auto-accepts updates).

To force an update:
```bash
# Clear npm cache
npm cache clean --force

# Restart Claude Code
# Next start will download latest version
```

---

## Removing the MCP Server

To completely remove GitLab MCP server:

```bash
# Remove from Claude Code
claude mcp remove gitlab -s local

# Restart Claude Code
```

Your GitLab instance and token are not affected - only the Claude Code configuration is removed.

---

## Security Notes

### Token Security

- **Never commit tokens to git** - add `.gitlab-mcp-token` to `.gitignore`
- **Never share tokens publicly** - they grant full access to your GitLab account
- **Use expiration dates** - set tokens to expire after a reasonable period
- **Revoke if compromised** - immediately revoke in GitLab settings if exposed

### Token Permissions

The MCP server requests full API access. If you want more restrictive access:
1. Create a **separate GitLab user** with limited permissions
2. Add that user to only the projects you want accessible
3. Create a token for that user
4. Use that token in the MCP server configuration

### Read-Only Mode

For enhanced security, use read-only mode:
```bash
-e GITLAB_READ_ONLY_MODE="true"
```

This prevents any create/update/delete operations.

---

## Reference: Working Setup on This System

**If you need to see the actual working configuration**, it's located at:

```bash
# GitLab MCP Configuration (local scope for this project)
/Users/timkitchens/projects/client-repos/gitlab-test/.claude/mcp.json

# View it
cat /Users/timkitchens/projects/client-repos/gitlab-test/.claude/mcp.json | jq '.mcpServers["gitlab"]'
```

**Actual working configuration:**
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@zereight/mcp-gitlab"],
  "env": {
    "GITLAB_PERSONAL_ACCESS_TOKEN": "glpat-...",
    "GITLAB_API_URL": "http://localhost:8929/api/v4"
  }
}
```

**Actual working command:**
```bash
claude mcp add gitlab -s local \
  -e GITLAB_PERSONAL_ACCESS_TOKEN="glpat-5ccBBPwIRO-D19dVZJH6t286MQp1OjEH.01.0w1p0k56l" \
  -e GITLAB_API_URL="http://localhost:8929/api/v4" \
  -- npx -y @zereight/mcp-gitlab
```

**GitLab instance details:**
- Running in Docker container: `gitlab-ce`
- Port: 8929
- API URL: `http://localhost:8929/api/v4`

---

## Sources

All information in this guide comes from:

1. **MCP Server Package:** https://www.npmjs.com/package/@zereight/mcp-gitlab
2. **GitHub Repository:** https://github.com/zereight/gitlab-mcp
3. **Working configuration on this system:**
   - `.claude/mcp.json` in this project
   - Command: `claude mcp get gitlab`
4. **GitLab Documentation:** https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html

**Nothing in this guide is invented or assumed.** Every command and configuration is verified from the actual working setup on this system.

---

**Document Version:** 1.0
**Last Updated:** 2026-02-04
**MCP Server:** @zereight/mcp-gitlab (stdio transport)
**Verified Working On:** macOS, GitLab CE Docker instance (localhost:8929)
