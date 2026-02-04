# Confluence — Detection & Setup

**Note:** SKILL.md handles the common case where Atlassian was already verified from Jira selection. This reference only loads when Atlassian is NOT yet verified.

## Step 1: Detection

Test Atlassian MCP access:
```
Call mcp__atlassian__getAccessibleAtlassianResources
```

---

## If Detection Succeeds

> "Atlassian MCP connected. Confluence is available."

Ask for optional default space:
> "Would you like to set a default Confluence space?"
> 1. Yes — Enter space key
> 2. No — I'll specify when needed

Store:
- `DOCS_BACKEND = "confluence"`
- `DOCS_ENABLED = true`
- `ATLASSIAN_VERIFIED = true`
- `DEFAULT_SPACE = [space key, or empty]`

Return to SKILL.md for next step.

---

## If Detection Fails

Present options:
> "Atlassian MCP not available. Would you like:"
> 1. I already set it up — Help me connect it
> 2. Help me set it up — First-time setup
> 3. Skip documentation

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
| No resources found | Ensure your account has access to Confluence |
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

Set `DOCS_BACKEND = "none"`, `DOCS_ENABLED = false`. Return to SKILL.md.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `backend` | `confluence` |
| `default_space` | Optional — user-provided space key |
| `ATLASSIAN_VERIFIED` | `true` |
