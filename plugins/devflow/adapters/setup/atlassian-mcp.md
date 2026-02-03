# Atlassian MCP Server Setup

## Overview

The Atlassian MCP server is built into Claude Code. It provides access to Jira and Confluence via the Atlassian API.

**Note:** This is a first-party MCP server - no additional installation required.

---

## Prerequisites

- Atlassian Cloud account (Jira/Confluence)
- API token from Atlassian

---

## Step 1: Create API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Give it a name (e.g., `devflow-mcp`)
4. Copy the token immediately

### Store Token Securely

```bash
echo "your-api-token-here" > ~/.atlassian-token
chmod 600 ~/.atlassian-token
```

---

## Step 2: Add to Claude Code

```bash
claude mcp add atlassian \
  -e "ATLASSIAN_EMAIL=your-email@example.com" \
  -e "ATLASSIAN_API_TOKEN=$(cat ~/.atlassian-token)" \
  -- npx -y @anthropic/mcp-atlassian
```

---

## Step 3: Verify Connection

Restart Claude Code, then run:
```
/mcp
```

Should show:
```
atlassian: ... - ✓ Connected
```

---

## Test the Connection

Try getting accessible resources:
```
Call mcp__atlassian__getAccessibleAtlassianResources
```

This should return your Atlassian Cloud ID and available products.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Verify email and token are correct |
| No resources found | Ensure your account has access to Jira/Confluence |
| Permission denied | Check API token permissions |

---

## Quick Reference

| Setting | Value |
|---------|-------|
| MCP Server | `@anthropic/mcp-atlassian` |
| Transport | stdio (via npx) |
| Auth Method | Email + API Token |
| Token URL | https://id.atlassian.com/manage-profile/security/api-tokens |

---

## Available Products

The Atlassian MCP provides access to:

### Jira
- Get/create/update issues
- Transition issues through workflow
- Add comments and worklogs
- Search with JQL

### Confluence
- Get/create/update pages
- Search content
- Add comments
- Access spaces
