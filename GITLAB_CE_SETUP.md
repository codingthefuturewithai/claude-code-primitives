# GitLab CE Docker + MCP Server Setup Guide

This documents the exact setup used in this environment.

---

## Part 1: GitLab CE Docker Container

### Docker Compose File

Location: `/Users/timkitchens/projects/client-repos/gitlab-test/docker-compose.yml`

```yaml
version: '3.8'
services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    container_name: gitlab-ce
    hostname: gitlab.local
    restart: unless-stopped
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://localhost:8929'
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
        # Reduce memory usage for local testing
        puma['worker_processes'] = 2
        sidekiq['concurrency'] = 5
        prometheus_monitoring['enable'] = false
    ports:
      - '8929:8929'    # HTTP
      - '2224:22'      # SSH
    volumes:
      - gitlab_config:/etc/gitlab
      - gitlab_logs:/var/log/gitlab
      - gitlab_data:/var/opt/gitlab
    shm_size: '256m'

volumes:
  gitlab_config:
  gitlab_logs:
  gitlab_data:
```

### Start the Container

```bash
cd /Users/timkitchens/projects/client-repos/gitlab-test
docker compose up -d
```

### Wait for Initialization (3-5 minutes)

```bash
docker logs -f gitlab-ce
# Wait until you see "gitlab Reconfigured!"
```

### Get Initial Root Password

```bash
docker exec -it gitlab-ce grep 'Password:' /etc/gitlab/initial_root_password
```

Save this password - it expires after 24 hours.

### First Login

- URL: http://localhost:8929
- Username: `root`
- Password: (from above)

---

## Part 2: Create Personal Access Token

1. Log in to GitLab at http://localhost:8929
2. Click avatar (top-right) → **Edit profile**
3. Left sidebar → **Access Tokens**
4. Click **Add new token**
5. Configure:
   - **Token name**: `devflow-mcp`
   - **Expiration**: Set as needed
   - **Scopes**: Check all:
     - `api`
     - `read_api`
     - `read_repository`
     - `write_repository`
     - `read_registry`
     - `write_registry`
6. Click **Create personal access token**
7. **Copy the token immediately** - it won't be shown again

### Store the Token

```bash
echo "glpat-xxxxxxxxxxxxxxxxxxxx" > ~/.gitlab-test-token
chmod 600 ~/.gitlab-test-token
```

---

## Part 3: Add GitLab MCP to Claude Code

### The Exact Command Used

```bash
claude mcp add gitlab npx \
  -e "GITLAB_PERSONAL_ACCESS_TOKEN=$(cat ~/.gitlab-test-token)" \
  -e "GITLAB_API_URL=http://localhost:8929/api/v4" \
  -- -y @zereight/mcp-gitlab
```

Or with the token directly:

```bash
claude mcp add gitlab npx \
  -e "GITLAB_PERSONAL_ACCESS_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx" \
  -e "GITLAB_API_URL=http://localhost:8929/api/v4" \
  -- -y @zereight/mcp-gitlab
```

### Verify Connection

Restart Claude Code, then run:
```
/mcp
```

Should show:
```
gitlab: npx -y @zereight/mcp-gitlab - ✓ Connected
```

---

## Quick Reference

| Item | Value |
|------|-------|
| GitLab URL | http://localhost:8929 |
| GitLab API | http://localhost:8929/api/v4 |
| SSH Port | 2224 |
| Container Name | gitlab-ce |
| Admin User | root |

### Container Commands

```bash
# Start
docker compose up -d

# Stop
docker compose down

# Logs
docker logs -f gitlab-ce

# Status
docker ps --format "table {{.Names}}\t{{.Status}}"
```
