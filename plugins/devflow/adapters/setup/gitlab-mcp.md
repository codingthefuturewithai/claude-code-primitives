# GitLab MCP Server Setup

## Overview

The GitLab MCP server (`@zereight/mcp-gitlab`) provides access to GitLab issues, merge requests, and repositories.

**Repository:** https://github.com/zereight/mcp-gitlab

---

## Prerequisites

- GitLab instance (gitlab.com or self-hosted)
- Personal Access Token with appropriate scopes
- Node.js/npx available

---

## Step 1: Create Personal Access Token

### For gitlab.com

1. Go to https://gitlab.com/-/profile/personal_access_tokens
2. Create a new token with scopes:
   - `api`
   - `read_api`
   - `read_repository`
   - `write_repository`
3. Copy the token immediately

### For Self-Hosted GitLab

1. Log in to your GitLab instance
2. Navigate to: Avatar → **Edit profile** → **Access Tokens**
3. Click **Add new token**
4. Configure:
   - **Token name**: `devflow-mcp`
   - **Expiration**: Set as needed
   - **Scopes**: `api`, `read_api`, `read_repository`, `write_repository`
5. Click **Create personal access token**
6. Copy the token immediately

### Store Token Securely

```bash
echo "glpat-xxxxxxxxxxxxxxxxxxxx" > ~/.gitlab-token
chmod 600 ~/.gitlab-token
```

---

## Step 2: Add to Claude Code

### For gitlab.com

```bash
claude mcp add gitlab npx \
  -e "GITLAB_PERSONAL_ACCESS_TOKEN=$(cat ~/.gitlab-token)" \
  -- -y @zereight/mcp-gitlab
```

### For Self-Hosted GitLab

```bash
claude mcp add gitlab npx \
  -e "GITLAB_PERSONAL_ACCESS_TOKEN=$(cat ~/.gitlab-token)" \
  -e "GITLAB_API_URL=http://your-gitlab.example.com/api/v4" \
  -- -y @zereight/mcp-gitlab
```

---

## Step 3: Verify Connection

Restart Claude Code, then run:
```
/mcp
```

Should show:
```
gitlab: npx -y @zereight/mcp-gitlab - ✓ Connected
```

---

## Test the Connection

Try listing projects:
```
Call mcp__gitlab__list_projects
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection failed | Check token has `api` scope |
| API URL error | Ensure URL ends with `/api/v4` |
| Permission denied | Verify token hasn't expired |

---

## Quick Reference

| Setting | Value |
|---------|-------|
| MCP Server | `@zereight/mcp-gitlab` |
| Transport | stdio (via npx) |
| Required Scopes | `api`, `read_api`, `read_repository`, `write_repository` |
