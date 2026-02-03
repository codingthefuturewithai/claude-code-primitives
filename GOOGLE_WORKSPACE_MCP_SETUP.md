# Google Workspace MCP Server Setup Guide

This documents the exact setup used in this environment.

---

## Part 1: Google Cloud Console Setup

### Create Project and Enable APIs

1. Go to https://console.cloud.google.com
2. Create new project (e.g., `DevFlow-MCP-Test`)
3. Go to **APIs & Services** → **Library**
4. Enable these APIs:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Gmail API (optional)

### Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** → **Create**
3. Fill in:
   - App name: Any name
   - User support email: Your email
   - Developer contact: Your email
4. Click **Save and Continue**
5. On Scopes page, click **Add or Remove Scopes**, add:
   - `https://www.googleapis.com/auth/drive`
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/spreadsheets`
   - `https://www.googleapis.com/auth/gmail.readonly`
6. Click **Update** → **Save and Continue**
7. On Test Users page, add your Google email address
8. Click **Save and Continue**

### Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: Any name
5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

**Important**: Desktop app credentials automatically allow localhost redirects. No redirect URI configuration needed in Google Console.

---

## Part 2: Clone and Configure the Server

### Clone Repository

```bash
cd ~
git clone https://github.com/taylorwilsdon/google_workspace_mcp.git
cd google_workspace_mcp
```

### Create .env File

Location: `/Users/timkitchens/google_workspace_mcp/.env`

```
GOOGLE_OAUTH_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
OAUTHLIB_INSECURE_TRANSPORT=1
WORKSPACE_MCP_PORT=8847
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8847/oauth2callback
USER_GOOGLE_EMAIL=your_email@gmail.com
```

**Critical**: All three port values must match:
- `WORKSPACE_MCP_PORT=8847`
- `GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8847/oauth2callback`
- Docker port mapping `8847:8847`

### Create docker-compose.yml

Location: `/Users/timkitchens/google_workspace_mcp/docker-compose.yml`

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

## Part 3: Build and Start

```bash
cd ~/google_workspace_mcp
docker compose build
docker compose up -d
```

### Verify Container

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Should show:
```
gws_mcp   Up X minutes   0.0.0.0:8847->8847/tcp
```

---

## Part 4: OAuth Authentication

1. Open browser to: `http://localhost:8847/oauth2/authorize`
2. Sign in with the Google account you added as a test user
3. If you see "unverified app" warning:
   - Click **Advanced**
   - Click **Go to [App Name] (unsafe)**
4. Click **Allow** for each permission
5. You should see "Authentication successful"

---

## Part 5: Add to Claude Code

### The Exact Command Used

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

## Quick Reference

| Item | Value |
|------|-------|
| Repository | https://github.com/taylorwilsdon/google_workspace_mcp |
| Container Name | gws_mcp |
| Port | 8847 |
| MCP Endpoint | http://localhost:8847/mcp |
| OAuth Type | Desktop application |
| Transport | HTTP |

### Container Commands

```bash
# Start
cd ~/google_workspace_mcp
docker compose up -d

# Stop
docker compose down

# Logs
docker logs gws_mcp

# Rebuild
docker compose build --no-cache
```

### Reset OAuth (if needed)

```bash
docker compose down
docker volume rm google_workspace_mcp_store_creds
docker compose up -d
# Re-authenticate in browser
```

---

## Port Configuration (Critical)

These three values MUST all use the same port number:

| Location | Setting |
|----------|---------|
| `.env` | `WORKSPACE_MCP_PORT=8847` |
| `.env` | `GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8847/oauth2callback` |
| `docker-compose.yml` | `ports: "8847:8847"` |

If any of these mismatch, OAuth will fail with redirect URI errors.
