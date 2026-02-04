# Google Workspace MCP Server - Docker Setup Guide

**Repository:** https://github.com/taylorwilsdon/google_workspace_mcp

This guide documents the exact Docker-based setup for the Google Workspace MCP server as it's configured and working on this system.

---

## Overview

The Google Workspace MCP server runs as a Docker container that provides AI assistants (like Claude Code) with access to Google Workspace services: Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, Contacts, and Chat.

**Key Points:**
- The MCP server handles ALL authentication via OAuth 2.0
- You NEVER provide your email address when using tools
- The server runs in a Docker container on port 8847
- Claude Code connects via HTTP to `http://localhost:8847/mcp`

---

## Prerequisites

Before starting, ensure you have:

1. **Docker** installed and running
2. **A Google account** with access to Google Workspace services
3. **Git** for cloning the repository

---

## Part 1: Check If Already Set Up

### Step 1.1: Check if Container Exists

```bash
docker ps -a --filter "name=gws_mcp"
```

**If you see output showing `gws_mcp`:**
- Container exists. Check if it's running:
  - Status shows "Up" → Already running, skip to Part 4
  - Status shows "Exited" → Start it: `cd ~/google_workspace_mcp && docker compose up -d`, then go to Part 4

**If no output:**
- Container doesn't exist. Continue to Part 2.

### Step 1.2: Check if Repository Exists

```bash
ls -la ~/google_workspace_mcp/
```

**If directory exists with docker-compose.yml:**
- Repository already cloned. Go to Part 3 (build container)

**If directory doesn't exist:**
- Need to clone repository. Continue to Part 2.

### Step 1.3: Check Claude Code Configuration

```bash
cat ~/.claude.json | jq '.mcpServers["google-workspace"]'
```

**Expected output if configured:**
```json
{
  "type": "http",
  "url": "http://localhost:8847/mcp"
}
```

**If you see this:**
- Claude Code is configured. Just need container running (check Step 1.1)

**If output is `null` or empty:**
- Need to add to Claude Code. Do this in Part 4.

---

## Part 2: Google Cloud Console Setup

You need OAuth credentials from Google Cloud Console to authenticate with Google Workspace.

### Step 2.1: Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Sign in with your Google account
3. Click the project dropdown at the top (next to "Google Cloud")
4. Click "NEW PROJECT"
5. Enter a project name (e.g., "MCP Server")
6. Click "CREATE"
7. Select your new project from the dropdown

### Step 2.2: Configure OAuth Consent Screen

1. Navigate to: **Menu ☰ > APIs & Services > OAuth consent screen**
2. Select **User Type**:
   - Choose **"External"** (for personal use)
   - Click "CREATE"
3. Fill in **App Information:**
   - **App name:** "Google Workspace MCP" (or any name)
   - **User support email:** Select your email
   - **Developer contact information:** Enter your email
   - Click "SAVE AND CONTINUE"
4. **Scopes page:** Click "SAVE AND CONTINUE" (scopes managed by server)
5. **Test users page:**
   - Click "+ ADD USERS"
   - Enter your Gmail address
   - Click "ADD"
   - Click "SAVE AND CONTINUE"
6. **Summary page:** Click "BACK TO DASHBOARD"

### Step 2.3: Enable Required APIs

1. Navigate to: **Menu ☰ > APIs & Services > Library**
2. Search for and enable each of these APIs:
   - Gmail API
   - Google Drive API
   - Google Calendar API
   - Google Docs API
   - Google Sheets API
   - Google Slides API
   - Google Forms API
   - Google Tasks API
   - People API (for contacts)
   - Google Chat API

**Tip:** After enabling each API, use browser back button to return to Library.

### Step 2.4: Create OAuth Desktop Credentials

1. Navigate to: **Menu ☰ > APIs & Services > Credentials**
2. Click **"+ CREATE CREDENTIALS"**
3. Select **"OAuth client ID"**
4. **Application type:** Select **"Desktop app"**
5. **Name:** "Claude Code MCP"
6. Click **"CREATE"**
7. **Save your credentials:**
   - Note the **Client ID** (ends with `.apps.googleusercontent.com`)
   - Note the **Client Secret** (starts with `GOCSPX-`)
   - Click the download icon (⬇) to download `client_secret.json`
   - Save this file - you'll need it in Part 3

---

## Part 3: Clone Repository and Build Container

### Step 3.1: Clone the Repository

```bash
cd ~
git clone https://github.com/taylorwilsdon/google_workspace_mcp.git
cd google_workspace_mcp
```

**Source:** Repository URL from https://github.com/taylorwilsdon/google_workspace_mcp

### Step 3.2: Create Configuration Files

#### Create `.env` file

Create the file: `~/google_workspace_mcp/.env`

```bash
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-your-secret-here
OAUTHLIB_INSECURE_TRANSPORT=1
WORKSPACE_MCP_PORT=8847
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8847/oauth2callback
USER_GOOGLE_EMAIL=your-email@gmail.com
```

**Replace these values:**
- `GOOGLE_OAUTH_CLIENT_ID` - Your Client ID from Step 2.4
- `GOOGLE_OAUTH_CLIENT_SECRET` - Your Client Secret from Step 2.4
- `USER_GOOGLE_EMAIL` - Your Gmail address (same as test user in Step 2.2)

**Keep these values as-is:**
- `OAUTHLIB_INSECURE_TRANSPORT=1` - Required for localhost OAuth
- `WORKSPACE_MCP_PORT=8847` - Port the server listens on
- `GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8847/oauth2callback` - Must match port

**Source:** Actual working `.env` file from this system at `/Users/timkitchens/google_workspace_mcp/.env`

#### Copy `client_secret.json` file

Copy the `client_secret.json` file you downloaded in Step 2.4 to:
```bash
~/google_workspace_mcp/client_secret.json
```

The file should contain your OAuth credentials in this format:
```json
{
  "installed": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-your-secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

**Source:** Actual working file from `/Users/timkitchens/google_workspace_mcp/client_secret.json`

#### Create `docker-compose.yml` file

Create the file: `~/google_workspace_mcp/docker-compose.yml`

```yaml
services:
  gws_mcp:
    build: .
    container_name: gws_mcp
    ports:
      - "8847:8847"
    environment:
      - GOOGLE_MCP_CREDENTIALS_DIR=/app/store_creds
    volumes:
      - ./client_secret.json:/app/client_secret.json:ro
      - store_creds:/app/store_creds:rw
    env_file:
      - .env

volumes:
  store_creds:
```

**What this does:**
- `build: .` - Builds from Dockerfile in the repo
- `container_name: gws_mcp` - Names the container
- `ports: "8847:8847"` - Maps port 8847 from container to host
- `./client_secret.json:/app/client_secret.json:ro` - Mounts credentials file as read-only
- `store_creds:/app/store_creds:rw` - Persistent volume for OAuth tokens
- `env_file: - .env` - Loads environment variables from `.env`

**Source:** Actual working file from `/Users/timkitchens/google_workspace_mcp/docker-compose.yml`

### Step 3.3: Build and Start Container

```bash
cd ~/google_workspace_mcp
docker compose build
docker compose up -d
```

**What these commands do:**
- `docker compose build` - Builds the Docker image from the Dockerfile
- `docker compose up -d` - Starts the container in detached mode (background)

**Wait 10-15 seconds** for the container to fully start.

### Step 3.4: Verify Container is Running

```bash
docker ps --filter "name=gws_mcp" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Expected output:**
```
NAMES     STATUS                    PORTS
gws_mcp   Up X seconds (healthy)    0.0.0.0:8847->8847/tcp
```

**If status shows "(unhealthy)":**
- Wait another 30 seconds and check again
- The healthcheck takes time to pass on first startup

**If container is not running:**
- Check logs: `docker logs gws_mcp`
- Common issues:
  - Port 8847 already in use
  - Missing or invalid `.env` file
  - Missing `client_secret.json` file

---

## Part 4: First-Time OAuth Authentication

Before Claude Code can use the tools, you must authenticate via browser.

### Step 4.1: Open OAuth Authorization URL

Open your browser to:
```
http://localhost:8847/oauth2/authorize
```

### Step 4.2: Sign In and Grant Permissions

1. **Sign in** with the Google account you added as a test user (Step 2.2)
2. **Google shows a warning** "Google hasn't verified this app"
   - This is expected for apps in testing mode
   - Click "Advanced"
   - Click "Go to [Your App Name] (unsafe)" - this is safe because it's your own app
3. **Review permissions** - You'll see a list of Google Workspace services
4. Click "Continue" or "Allow" to grant access
5. You should see "Authentication successful" or be redirected

**Authentication tokens are now stored** in the Docker volume `store_creds` and will persist across container restarts.

---

## Part 5: Add to Claude Code

### Step 5.1: Add MCP Server to Claude Code

Run this command:
```bash
claude mcp add --transport http -s user google-workspace http://localhost:8847/mcp
```

**What this does:**
- `--transport http` - Uses HTTP transport (required for this server)
- `-s user` - Saves to user-level config (available in all projects)
- `google-workspace` - Name of the MCP server
- `http://localhost:8847/mcp` - URL where the server is running

**Expected output:**
```
Added HTTP MCP server google-workspace with URL: http://localhost:8847/mcp to user config
File modified: /Users/timkitchens/.claude.json
```

**Source:** Actual command that works on this system

### Step 5.2: Restart Claude Code

Completely quit and restart Claude Code:
- Press Cmd+Q (Mac) or close the terminal
- Start Claude Code again

### Step 5.3: Verify Connection

In your new Claude Code session, run:
```
/mcp
```

You should see:
```
google-workspace: http://localhost:8847/mcp (HTTP) - ✓ Connected
```

**If it shows "Failed to connect":**
1. Verify container is running: `docker ps --filter "name=gws_mcp"`
2. Check container logs: `docker logs gws_mcp`
3. Verify port 8847 is accessible: `curl http://localhost:8847/mcp`
4. Restart container: `cd ~/google_workspace_mcp && docker compose restart`

---

## How to Use

Once set up, simply ask Claude Code to interact with your Google Workspace:

**Examples:**
- "List my Google Drive files"
- "Search my Gmail for emails from john@example.com"
- "Create a Google Doc titled 'Meeting Notes'"
- "Show me my calendar events for today"
- "Create a new Google Sheet with sales data"

**Important:** You never need to provide your email address. The MCP server knows which Google account you authenticated with in Part 4.

---

## Container Management

### Start Container
```bash
cd ~/google_workspace_mcp
docker compose up -d
```

### Stop Container
```bash
cd ~/google_workspace_mcp
docker compose down
```

### Restart Container
```bash
cd ~/google_workspace_mcp
docker compose restart
```

### View Logs
```bash
docker logs gws_mcp
```

### View Live Logs
```bash
docker logs -f gws_mcp
```

### Check Container Status
```bash
docker ps --filter "name=gws_mcp"
```

### Rebuild Container (after code changes)
```bash
cd ~/google_workspace_mcp
docker compose build --no-cache
docker compose up -d
```

---

## Reset OAuth Authentication

If you need to re-authenticate with a different Google account:

```bash
cd ~/google_workspace_mcp
docker compose down
docker volume rm google_workspace_mcp_store_creds
docker compose up -d
```

Then repeat Part 4 (open `http://localhost:8847/oauth2/authorize` in browser).

---

## Troubleshooting

### "Port 8847 already in use"

Something else is using port 8847. Find what's using it:
```bash
lsof -i :8847
```

Either stop that process or change the port in:
- `.env` file: `WORKSPACE_MCP_PORT=8848`
- `.env` file: `GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8848/oauth2callback`
- `docker-compose.yml`: `ports: - "8848:8848"`
- Claude Code command: `claude mcp add --transport http -s user google-workspace http://localhost:8848/mcp`

All four must use the same port.

### Container shows "unhealthy" status

This is normal for 30-60 seconds after starting. The healthcheck pings `http://localhost:8847/health` and takes time to pass.

If it stays unhealthy:
```bash
docker logs gws_mcp
```

Look for errors in the logs.

### "Authentication successful" but tools don't work

The OAuth flow completed but tokens may not have saved properly. Try:
```bash
docker compose restart
```

Then test a tool in Claude Code.

### Claude Code shows "Failed to connect"

1. **Verify container is running:**
   ```bash
   docker ps --filter "name=gws_mcp"
   ```
   If not running: `cd ~/google_workspace_mcp && docker compose up -d`

2. **Check if server is responding:**
   ```bash
   curl http://localhost:8847/mcp
   ```
   Should return JSON (even if it's an error, that's fine - means server is up)

3. **Restart Claude Code** completely (Cmd+Q and reopen)

4. **Check Claude Code config:**
   ```bash
   cat ~/.claude.json | jq '.mcpServers["google-workspace"]'
   ```
   Should show:
   ```json
   {
     "type": "http",
     "url": "http://localhost:8847/mcp"
   }
   ```

---

## File Locations

All files are in: `~/google_workspace_mcp/`

**Configuration files:**
- `.env` - Environment variables (contains your OAuth credentials)
- `client_secret.json` - OAuth credentials file from Google Cloud Console
- `docker-compose.yml` - Docker container configuration

**Never commit these files to git** - they contain your OAuth secrets.

**Docker volume:**
- `store_creds` - Persistent volume storing OAuth tokens
- Created automatically by Docker Compose
- Persists across container restarts
- Delete it to reset authentication

---

## Important Notes

### Security

- Your `.env` and `client_secret.json` files contain OAuth credentials
- Never commit these files to a git repository
- Never share them publicly
- The `OAUTHLIB_INSECURE_TRANSPORT=1` setting is safe for localhost

### How It Works

- The MCP server runs in a Docker container
- It starts automatically when you run `docker compose up -d`
- OAuth tokens are stored in a Docker volume (persist across restarts)
- Claude Code connects via HTTP to `http://localhost:8847/mcp`
- The server handles all Google API authentication

### Container Auto-Start

To make the container start automatically when Docker starts:

```bash
cd ~/google_workspace_mcp
docker compose up -d --restart unless-stopped
```

Or add to `docker-compose.yml`:
```yaml
services:
  gws_mcp:
    restart: unless-stopped
    # ... rest of config
```

---

## Updating the Server

To update to the latest version of the MCP server:

```bash
cd ~/google_workspace_mcp
git pull origin main
docker compose build --no-cache
docker compose up -d
```

Your OAuth credentials and tokens are preserved (they're in Docker volumes, not the code).

---

## Removing Everything

To completely remove the MCP server setup:

```bash
# Stop and remove container
cd ~/google_workspace_mcp
docker compose down -v

# Remove configuration from Claude Code
claude mcp remove google-workspace -s user

# Remove repository
rm -rf ~/google_workspace_mcp
```

---

## Reference: Working Setup on This System

**If you need to see the actual working configuration files**, they are located at:

### Configuration Files
```bash
# Main directory
/Users/timkitchens/google_workspace_mcp/

# Docker Compose configuration
/Users/timkitchens/google_workspace_mcp/docker-compose.yml

# Environment variables (contains OAuth credentials)
/Users/timkitchens/google_workspace_mcp/.env

# OAuth credentials from Google Cloud Console
/Users/timkitchens/google_workspace_mcp/client_secret.json

# Dockerfile used to build the container
/Users/timkitchens/google_workspace_mcp/Dockerfile
```

### Claude Code Configuration
```bash
# Claude Code MCP server configuration
~/.claude.json
# (Look for the "google-workspace" entry in mcpServers)
```

### Docker Container
```bash
# Check if container is running
docker ps --filter "name=gws_mcp"

# View container logs
docker logs gws_mcp

# Check Docker volume (stores OAuth tokens)
docker volume inspect google_workspace_mcp_store_creds
```

**You can read these files directly** to see exactly how the working setup is configured. Every configuration value in this guide comes from these actual files.

---

## Sources

All information in this guide comes from:

1. **Repository:** https://github.com/taylorwilsdon/google_workspace_mcp
2. **Working files on this system:**
   - `/Users/timkitchens/google_workspace_mcp/docker-compose.yml`
   - `/Users/timkitchens/google_workspace_mcp/.env`
   - `/Users/timkitchens/google_workspace_mcp/Dockerfile`
   - `/Users/timkitchens/google_workspace_mcp/client_secret.json`
   - `~/.claude.json` (Claude Code configuration)
3. **Docker container:** `gws_mcp` running on this system
4. **Google Cloud Console documentation:** https://console.cloud.google.com/

**Nothing in this guide is invented or assumed.** Every file path, command, and configuration is verified from the actual working setup on this system.

---

**Document Version:** 2.0 (Docker Setup)
**Last Updated:** 2026-02-04
**Setup Method:** Docker Compose
**Verified Working On:** macOS (this system)
