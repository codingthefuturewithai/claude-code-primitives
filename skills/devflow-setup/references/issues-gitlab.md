# GitLab Issues — Detection & Setup

## Step 1: Detection

Test GitLab MCP access:
```
Call mcp__gitlab__list_projects
```

---

## If Detection Succeeds

Optionally ask for a default project:
> "GitLab MCP connected. Would you like to set a default project?"
> 1. Yes — Select from list
> 2. No — I'll specify per-issue

If yes, display the projects returned and let user pick.

Store:
- `ISSUES_BACKEND = "gitlab"`
- `ISSUES_ENABLED = true`
- `DEFAULT_PROJECT = [selected project, or empty]`

Return to SKILL.md for next step.

---

## If Detection Fails

Present options:
> "GitLab MCP not available. Would you like:"
> 1. I already set it up — Help me connect it
> 2. Help me set it up — First-time setup
> 3. Skip issue tracking

### Option 1: Already Set Up — Troubleshooting

> "To connect your existing GitLab MCP to Claude Code:"
>
> **Verify it's running:**
> ```
> /mcp
> ```
> Look for `gitlab` in the server list.
>
> **If not listed, add it:**
> ```bash
> claude mcp add gitlab npx \
>   -e "GITLAB_PERSONAL_ACCESS_TOKEN=your-token" \
>   -- -y @zereight/mcp-gitlab
> ```
>
> **Restart Claude Code** (Cmd+Q and relaunch), then re-run `/devflow-setup`.

| Issue | Solution |
|-------|----------|
| Connection failed | Check token has `api` scope |
| API URL error | Ensure URL ends with `/api/v4` (self-hosted only) |
| Permission denied | Verify token hasn't expired |

### Option 2: First-Time Setup

> **Step 1: Create Personal Access Token**
>
> **For gitlab.com:**
> 1. Go to https://gitlab.com/-/profile/personal_access_tokens
> 2. Create a new token with scopes: `api`, `read_api`, `read_repository`, `write_repository`
> 3. Copy the token immediately
>
> **For self-hosted GitLab:**
> 1. Navigate to: Avatar → **Edit profile** → **Access Tokens**
> 2. Click **Add new token**
> 3. Set scopes: `api`, `read_api`, `read_repository`, `write_repository`
> 4. Copy the token immediately
>
> **Step 2: Store Token Securely**
> ```bash
> echo "glpat-xxxxxxxxxxxxxxxxxxxx" > ~/.gitlab-token
> chmod 600 ~/.gitlab-token
> ```
>
> **Step 3: Add to Claude Code**
>
> For gitlab.com:
> ```bash
> claude mcp add gitlab npx \
>   -e "GITLAB_PERSONAL_ACCESS_TOKEN=$(cat ~/.gitlab-token)" \
>   -- -y @zereight/mcp-gitlab
> ```
>
> For self-hosted:
> ```bash
> claude mcp add gitlab npx \
>   -e "GITLAB_PERSONAL_ACCESS_TOKEN=$(cat ~/.gitlab-token)" \
>   -e "GITLAB_API_URL=http://your-gitlab.example.com/api/v4" \
>   -- -y @zereight/mcp-gitlab
> ```
>
> **Step 4: Restart Claude Code** (Cmd+Q and relaunch)
>
> **Step 5: Verify** — Run `/mcp` and confirm `gitlab: ... - ✓ Connected`
>
> Then re-run `/devflow-setup` to continue configuration.

### Option 3: Skip

Set `ISSUES_BACKEND = "none"`, `ISSUES_ENABLED = false`. Return to SKILL.md.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `backend` | `gitlab` |
| `default_project` | Optional — user-selected project ID |
