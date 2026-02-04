# Jira — Detection & Setup

## Step 1: Detection

Test Atlassian MCP access:
```
Call mcp__atlassian__getAccessibleAtlassianResources
```

---

## If Detection Succeeds

Extract the `cloudId` from the response. Display available resources and confirm with user:
> "Atlassian MCP connected. Found cloud ID: [cloudId]"
> "Is this the correct Atlassian instance?"

Store:
- `ISSUES_BACKEND = "jira"`
- `ISSUES_ENABLED = true`
- `ATLASSIAN_VERIFIED = true`
- `CLOUD_ID = [cloudId]`

Return to SKILL.md for next step.

---

## If Detection Fails

Present options:
> "Atlassian MCP not available. Would you like:"
> 1. I already set it up — Help me connect it
> 2. Help me set it up — First-time setup
> 3. Skip issue tracking

### Option 1: Already Set Up — Troubleshooting

> "To connect your existing Atlassian MCP to Claude Code:"
>
> **Verify it's running:**
> ```
> /mcp
> ```
> Look for `atlassian` in the server list.
>
> **If not listed, add it:**
> ```bash
> claude mcp add atlassian \
>   -e "ATLASSIAN_EMAIL=your-email@example.com" \
>   -e "ATLASSIAN_API_TOKEN=your-token" \
>   -- npx -y @anthropic/mcp-atlassian
> ```
>
> **Restart Claude Code** (Cmd+Q and relaunch), then re-run `/devflow-setup`.

| Issue | Solution |
|-------|----------|
| Authentication failed | Verify email and API token are correct |
| No resources found | Ensure your account has access to Jira |
| Permission denied | Check API token permissions |

### Option 2: First-Time Setup

> **Step 1: Create API Token**
> 1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
> 2. Click **Create API token**
> 3. Name it (e.g., `devflow-mcp`)
> 4. Copy the token immediately
>
> **Step 2: Store Token Securely**
> ```bash
> echo "your-api-token-here" > ~/.atlassian-token
> chmod 600 ~/.atlassian-token
> ```
>
> **Step 3: Add to Claude Code**
> ```bash
> claude mcp add atlassian \
>   -e "ATLASSIAN_EMAIL=your-email@example.com" \
>   -e "ATLASSIAN_API_TOKEN=$(cat ~/.atlassian-token)" \
>   -- npx -y @anthropic/mcp-atlassian
> ```
>
> **Step 4: Restart Claude Code** (Cmd+Q and relaunch)
>
> **Step 5: Verify** — Run `/mcp` and confirm `atlassian: ... - ✓ Connected`
>
> Then re-run `/devflow-setup` to continue configuration.

### Option 3: Skip

Set `ISSUES_BACKEND = "none"`, `ISSUES_ENABLED = false`. Return to SKILL.md.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `backend` | `jira` |
| `cloudId` | Extracted from `getAccessibleAtlassianResources` |
| `ATLASSIAN_VERIFIED` | `true` (used by Step 2 for Confluence shortcut) |
