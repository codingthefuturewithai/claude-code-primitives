# Google Workspace MCP Server Setup

## Overview

The Google Workspace MCP server provides access to Google Docs, Drive, Sheets, Gmail, and more.

**Repository:** https://github.com/taylorwilsdon/google_workspace_mcp

---

## Prerequisites

- Google Cloud Console access
- Docker installed
- Ability to run OAuth flow in browser

---

## Step 1: Google Cloud Console Setup

### Create Project

1. Go to https://console.cloud.google.com
2. Create new project (e.g., `DevFlow-MCP`)
3. Note the project ID

### Enable APIs

Go to **APIs & Services** → **Library** and enable:
- Google Drive API
- Google Docs API
- Google Sheets API
- Gmail API (optional)

### Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** → **Create**
3. Fill in required fields:
   - App name: Any name
   - User support email: Your email
   - Developer contact: Your email
4. On Scopes page, add:
   - `https://www.googleapis.com/auth/drive`
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/spreadsheets`
5. On Test Users page, add your Google email address

### Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Click **Create**
5. Copy the **Client ID** and **Client Secret**

---

## Step 2: Clone and Configure

### Clone Repository

```bash
cd ~
git clone https://github.com/taylorwilsdon/google_workspace_mcp.git
cd google_workspace_mcp
```

### Create .env File

```bash
cat > .env << 'EOF'
GOOGLE_OAUTH_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
OAUTHLIB_INSECURE_TRANSPORT=1
WORKSPACE_MCP_PORT=8847
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8847/oauth2callback
USER_GOOGLE_EMAIL=your_email@gmail.com
EOF
```

**Critical:** All port values (8847) must match in `.env` and Docker config.

### Create docker-compose.yml

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

---

## Step 3: Build and Start

```bash
docker compose build
docker compose up -d
```

---

## Step 4: OAuth Authentication

1. Open browser: `http://localhost:8847/oauth2/authorize`
2. Sign in with the Google account you added as a test user
3. If "unverified app" warning appears:
   - Click **Advanced** → **Go to [App Name] (unsafe)**
4. Click **Allow** for each permission
5. Should see "Authentication successful"

---

## Step 5: Add to Claude Code

```bash
claude mcp add --transport http google-workspace http://localhost:8847/mcp
```

### Verify Connection

Restart Claude Code, then run:
```
/mcp
```

Should show:
```
google-workspace: http://localhost:8847/mcp (HTTP) - ✓ Connected
```

---

## Test the Connection

Try listing Drive files:
```
Call mcp__google-workspace__list_drive_items
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| OAuth redirect error | Check all port values match (8847) |
| Connection refused | Ensure container is running: `docker ps` |
| Permission denied | Re-run OAuth flow, ensure scopes are granted |

### Reset OAuth (if needed)

```bash
docker compose down
docker volume rm google_workspace_mcp_store_creds
docker compose up -d
# Re-authenticate in browser
```

---

## Quick Reference

| Setting | Value |
|---------|-------|
| Repository | taylorwilsdon/google_workspace_mcp |
| Container | gws_mcp |
| Port | 8847 |
| MCP Endpoint | http://localhost:8847/mcp |
| Transport | HTTP |
