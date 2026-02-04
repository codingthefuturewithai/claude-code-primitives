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
> **Verify it's configured:**
> ```bash
> claude mcp get gitlab 2>&1
> ```
> If you see "No MCP server found with name: gitlab" — it's not configured yet.
>
> **If not listed, add it (choose your instance type):**
>
> **GitLab.com:**
> ```bash
> claude mcp add gitlab -s user \
>   -e GITLAB_PERSONAL_ACCESS_TOKEN="your-token" \
>   -- npx -y @zereight/mcp-gitlab
> ```
>
> **Self-hosted GitLab:**
> ```bash
> claude mcp add gitlab -s user \
>   -e GITLAB_PERSONAL_ACCESS_TOKEN="your-token" \
>   -e GITLAB_API_URL="https://gitlab.yourcompany.com/api/v4" \
>   -- npx -y @zereight/mcp-gitlab
> ```
>
> **Local Docker GitLab:**
> ```bash
> claude mcp add gitlab -s local \
>   -e GITLAB_PERSONAL_ACCESS_TOKEN="your-token" \
>   -e GITLAB_API_URL="http://localhost:PORT/api/v4" \
>   -- npx -y @zereight/mcp-gitlab
> ```
>
> **Restart Claude Code** (Cmd+Q and relaunch), then re-run `/devflow-setup`.

**Troubleshooting by error message:**

| Error | Cause | Solution |
|-------|-------|----------|
| "No MCP server found" | Not configured | Run the `claude mcp add` command above for your instance type |
| "Failed to connect" | Invalid token, wrong API URL, instance not running, or port mismatch | See checks below |
| "Authentication failed" / 401 | Token invalid or expired | Create a new PAT in GitLab → Settings → Access Tokens, then reconfigure |
| npm / "Cannot find module" errors | `npx` can't download the package | Check internet, verify `npx --version`, try `npm install -g @zereight/mcp-gitlab` |
| Permission denied on tools | Missing token scopes | Ensure PAT has scopes: `api`, `read_api`, `read_repository`, `write_repository` |

**"Failed to connect" checks:**
1. **Token:** Verify token is correct and hasn't expired
2. **API URL:** Must end with `/api/v4` (self-hosted/local only; omit for GitLab.com)
3. **Instance running (local Docker):** `docker ps --filter "name=gitlab"`
4. **Port match (local Docker):** Check port in `docker ps` output matches GITLAB_API_URL

After troubleshooting:
> 1. I've completed these steps — Try detection again
> 2. Show me the detailed setup guide
> 3. Skip issue tracking for now

If "Try again" → retry from Step 1.
If "Detailed guide" → Read and display `GITLAB_MCP_SETUP.md` from this repo's root.

### Option 2: First-Time Setup

> "Which type of GitLab instance do you use?"
> 1. GitLab.com (cloud)
> 2. Self-hosted GitLab
> 3. Local GitLab (Docker)

**Step 1: Create Personal Access Token**

> 1. Log in to your GitLab instance
> 2. Navigate to: Avatar → **Edit profile** → **Access Tokens**
> 3. Click **Add new token**
> 4. Token name: `claude-code-mcp`
> 5. Select scopes:
>    - `api` — Full API access
>    - `read_api` — Read-only API access
>    - `read_repository` — Read repositories
>    - `write_repository` — Write to repositories
>    - `read_registry` — Read container registry
>    - `write_registry` — Write to container registry
> 6. Click **Create personal access token**
> 7. **Copy the token immediately** (shown only once)

**Step 2: Store Token Securely**
> ```bash
> echo "glpat-xxxxxxxxxxxxxxxxxxxx" > ~/.gitlab-mcp-token
> chmod 600 ~/.gitlab-mcp-token
> ```

**Step 3: Add to Claude Code**

> **Scope selection:**
> - `-s user` — Available in all projects (recommended for GitLab.com / self-hosted)
> - `-s local` — Only available in current project directory (recommended for local Docker)

Show the correct command based on instance type selected above:

> **GitLab.com:**
> ```bash
> claude mcp add gitlab -s user \
>   -e GITLAB_PERSONAL_ACCESS_TOKEN="$(cat ~/.gitlab-mcp-token)" \
>   -- npx -y @zereight/mcp-gitlab
> ```
>
> **Self-hosted:**
> ```bash
> claude mcp add gitlab -s user \
>   -e GITLAB_PERSONAL_ACCESS_TOKEN="$(cat ~/.gitlab-mcp-token)" \
>   -e GITLAB_API_URL="https://gitlab.yourcompany.com/api/v4" \
>   -- npx -y @zereight/mcp-gitlab
> ```
>
> **Local Docker:**
> ```bash
> claude mcp add gitlab -s local \
>   -e GITLAB_PERSONAL_ACCESS_TOKEN="$(cat ~/.gitlab-mcp-token)" \
>   -e GITLAB_API_URL="http://localhost:PORT/api/v4" \
>   -- npx -y @zereight/mcp-gitlab
> ```

**Step 4: Restart Claude Code** (Cmd+Q and relaunch)

**Step 5: Verify** — Run `/mcp` and confirm `gitlab: ... - ✓ Connected`

> **Options:**
> 1. Show me the complete setup guide — Read and display `GITLAB_MCP_SETUP.md` from this repo's root
> 2. Walk me through step-by-step — Guide through each part of `GITLAB_MCP_SETUP.md`
> 3. Skip for now

If "Complete guide" → Read and display `GITLAB_MCP_SETUP.md` from this repo's root. Then: "When you've completed setup, re-run `/devflow-setup` to continue."
If "Walk me through" → Read `GITLAB_MCP_SETUP.md` and guide user through each part. Wait for user confirmation at each step.

### Option 3: Skip

Set `ISSUES_BACKEND = "none"`, `ISSUES_ENABLED = false`. Return to SKILL.md.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `backend` | `gitlab` |
| `default_project` | Optional — user-selected project ID |
