# MCP Servers: Complete Guide

**Metadata for RAG Memory:**
- primitive_type: mcp-server
- content_type: complete-guide
- version: 1.0

---

## What Are MCP Servers?

MCP (Model Context Protocol) Servers are **external service integrations** that provide tools and resources to Claude Code through a standardized protocol.

**Key characteristics:**
- **External processes** - Run as separate Python/Node.js processes
- **Tool providers** - Expose functions Claude can call via `mcp__server__tool` format
- **Resource providers** - Expose data Claude can read
- **Bidirectional communication** - Claude calls tools, server responds with results
- **Standard protocol** - Uses MCP specification for communication

### MCP Servers vs Other Primitives

| Feature | MCP Servers | Skills | Slash Commands |
|---------|-------------|--------|----------------|
| Purpose | External API integration | Complex workflows | Simple user commands |
| Runs as | Separate process | In Claude session | In Claude session |
| Provides | Tools + Resources | Expertise | Prompt template |
| Configuration | settings.json | SKILL.md file | .md file |
| Language | Python or Node.js | Markdown instructions | Markdown instructions |

---

## When to Use MCP Servers

Use MCP servers when:
- **External API integration needed** - GitHub, JIRA, Slack, databases, etc.
- **Stateful operations required** - Maintaining connections, sessions, caching
- **Complex data transformations** - Processing outside Claude's capabilities
- **Reusable tools across projects** - Same API used in multiple projects
- **Performance-critical operations** - Native code execution

Do NOT use MCP servers when:
- **Simple workflow** - Use Skill or Slash Command instead
- **No external service** - Use Skills for internal workflows
- **User invocation needed** - Use Slash Command (MCP tools are called by Claude)
- **Automatic enforcement** - Use Hook instead

---

## Architecture

```
┌─────────────────────┐
│   Claude Code       │
│                     │
│  Skills/Commands    │
│  call tools via:    │
│  mcp__server__tool  │
└──────────┬──────────┘
           │ MCP Protocol
           │ (stdio/SSE)
           │
┌──────────▼──────────┐
│   MCP Server        │
│   (Python/Node.js)  │
│                     │
│   @mcp.tool()       │
│   def my_tool():    │
│       ...           │
└──────────┬──────────┘
           │
           │ API Calls
           │
┌──────────▼──────────┐
│  External Service   │
│  (GitHub, JIRA,     │
│   Database, etc.)   │
└─────────────────────┘
```

---

## Creating MCP Servers: The Cookiecutter Workflow

**CRITICAL:** NEVER write MCP server code manually. ALWAYS use the cookiecutter template.

### Step 1: Check for Official Servers First

Before creating custom server, ALWAYS check for existing official servers:

```bash
# Check official MCP servers repository
curl -s "https://api.github.com/repos/modelcontextprotocol/servers/contents" | grep -i "[service-name]"
```

**If official server exists:**
- Tell developer to install the official server instead
- Provide installation instructions
- DO NOT proceed to create custom server

**If NO official server exists:**
- Proceed to scaffold custom server using cookiecutter

### Step 2: Scaffold Using Cookiecutter

Use the official MCP cookiecutter template:

```bash
# Navigate to target directory
cd [target-directory]

# Run cookiecutter
cookiecutter gh:codingthefuturewithai/mcp-cookie-cutter
```

**Cookiecutter will prompt for:**
- `project_name`: Human-readable name (e.g., "GitHub MCP Server")
- `project_slug`: Directory name (e.g., "mcp-github-server")
- `package_name`: Python package name (e.g., "mcp_github_server")
- `description`: Brief description of what server does
- `author_name`: Developer name
- `author_email`: Developer email

### Step 3: Configure in settings.json

After scaffolding, add server configuration to appropriate config file:

**Project-level** (`.claude/settings.json`):
```json
{
  "mcpServers": {
    "mcp-[service]-server": {
      "command": "python",
      "args": ["-m", "mcp_[service]_server"],
      "env": {
        "API_KEY": "configure-this",
        "API_URL": "https://api.example.com"
      }
    }
  }
}
```

**Global** (`~/.claude/settings.json`): Same format

### Step 4: Guide Developer to Add Tools

The scaffolded project includes built-in AI assistance. Tell developer:

```
I've scaffolded the MCP server for [service]:

**Location**: [path]/mcp-[service]-server/
**Configuration**: Added to [config location]

**Next steps:**
1. Navigate to project: cd mcp-[service]-server
2. Install dependencies: pip install -e .
3. Use built-in /add-tool command to add features:

   Example:
   /add-tool

   Create a tool to fetch [service] data:
   - Tool name: get_[service]_data
   - Parameters: query (str), limit (int, default 10)
   - API endpoint: https://api.[service].com/v1/data

4. The generated project will guide you through implementation
5. Restart Claude Code after adding tools

The scaffolded project includes:
- /add-tool - Add new tools with AI assistance
- /test - Test your server
- Complete best practices structure
```

### Why Cookiecutter Instead of Manual Code

**Cookiecutter provides:**
- ✅ Correct project structure
- ✅ Best practices built in
- ✅ Built-in AI assistance for adding tools
- ✅ Testing infrastructure
- ✅ Documentation templates
- ✅ Proper type hints (NO Optional[T])
- ✅ Error handling patterns

**Manual code creation leads to:**
- ❌ Missing best practices
- ❌ Type hint mistakes (Optional[T])
- ❌ No testing infrastructure
- ❌ Inconsistent structure
- ❌ No built-in AI assistance

---

## Configuration Format

MCP servers are configured in `settings.json` or `config.json`:

### Basic Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["-m", "mcp_server_package"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Field Specifications

**server-name:** (required, string)
- Unique identifier for this server
- Used in tool names: `mcp__server-name__tool-name`
- Kebab-case recommended
- Example: `github`, `jira-connector`, `database-client`

**command:** (required, string)
- Command to launch the server process
- Python: `"python"` or `"python3"`
- Node.js: `"node"`
- Example: `"python"`, `"npx"`

**args:** (required, array)
- Arguments passed to command
- Python module: `["-m", "package_name"]`
- Node.js script: `["path/to/server.js"]`
- Example: `["-m", "mcp_github_server"]`

**env:** (optional, object)
- Environment variables for server process
- API keys, tokens, configuration
- Example: `{"GITHUB_TOKEN": "ghp_xxx", "API_URL": "https://api.example.com"}`

### Complete Example

```json
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["-m", "mcp_github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx",
        "GITHUB_API_URL": "https://api.github.com"
      }
    },
    "jira": {
      "command": "python",
      "args": ["-m", "mcp_jira_server"],
      "env": {
        "JIRA_URL": "https://company.atlassian.net",
        "JIRA_EMAIL": "user@company.com",
        "JIRA_API_TOKEN": "xxxxx"
      }
    }
  }
}
```

---

## Python MCP Server Structure

### Minimal Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Create server instance
mcp = Server("server-name")

# Define a tool
@mcp.tool()
def hello_world(name: str) -> dict:
    """Say hello to someone.

    Args:
        name: Name of person to greet

    Returns:
        Greeting message
    """
    return {"message": f"Hello, {name}!"}

# Run server
async def main():
    async with stdio_server() as streams:
        await mcp.run(
            streams[0],
            streams[1],
            mcp.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Tool Parameter Types

**CRITICAL: Never use `Optional[T]` for tool parameters**

```python
# ❌ WRONG - Will cause validation errors
@mcp.tool()
def my_tool(
    required_param: str,
    optional_param: Optional[str] = None  # DO NOT DO THIS
) -> dict:
    pass

# ✅ CORRECT - Use explicit None default
@mcp.tool()
def my_tool(
    required_param: str,
    optional_param: str = None  # This is correct
) -> dict:
    pass
```

**Why:** MCP/Pydantic frameworks reject `Optional[T]` type hints on tool definitions.

**Valid parameter types:**
- `str`, `int`, `float`, `bool`
- `list`, `dict`
- Custom types with `= None` for optional (NOT `Optional[T]`)

### File Structure

```
mcp_my_server/
  __init__.py
  __main__.py         # Entry point
  server.py           # Server implementation
  tools/
    __init__.py
    github_tools.py   # Tool definitions
    jira_tools.py
  utils/
    __init__.py
    api_client.py     # API wrapper
  config.py           # Configuration
  requirements.txt
  pyproject.toml      # Package metadata
```

### Entry Point (`__main__.py`)

```python
"""MCP Server entry point."""
from .server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
```

### Server Implementation (`server.py`)

```python
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from .tools import github_tools

# Create server
mcp = Server("github")

# Register tools
@mcp.tool()
def create_issue(
    repo: str,
    title: str,
    body: str = None,
    labels: list = None
) -> dict:
    """Create a GitHub issue.

    Args:
        repo: Repository in format "owner/repo"
        title: Issue title
        body: Issue description (optional)
        labels: List of label names (optional)

    Returns:
        Created issue details
    """
    token = os.getenv("GITHUB_TOKEN")
    api = GitHubAPI(token)
    return api.create_issue(repo, title, body, labels)

@mcp.tool()
def list_issues(
    repo: str,
    state: str = "open",
    limit: int = 10
) -> dict:
    """List GitHub issues.

    Args:
        repo: Repository in format "owner/repo"
        state: Issue state (open/closed/all)
        limit: Maximum number of issues

    Returns:
        List of issues
    """
    token = os.getenv("GITHUB_TOKEN")
    api = GitHubAPI(token)
    return api.list_issues(repo, state, limit)

# Main entry point
async def main():
    async with stdio_server() as streams:
        await mcp.run(
            streams[0],
            streams[1],
            mcp.create_initialization_options()
        )
```

---

## Using MCP Tools in Primitives

### In Skills

```yaml
---
name: github-issue-creator
description: Create GitHub issues when user reports bugs or requests features
allowed-tools: [mcp__github__create_issue, mcp__github__list_issues]
---

When user reports a bug or requests a feature:

## Step 1: Gather Information
Ask user for:
- Repository name
- Issue title
- Description
- Labels (optional)

## Step 2: Create Issue
Use mcp__github__create_issue tool:
- Pass repo, title, body, labels
- Handle API errors gracefully

## Step 3: Confirm
Show user the created issue URL and number.
```

### In Slash Commands

```markdown
---
description: Create GitHub issue from current context
allowed-tools: [mcp__github__create_issue, Bash, Read]
---

Create a GitHub issue from current context:

## Step 1: Gather Context
Run `git remote get-url origin` to find repo.
Run `git branch --show-current` for branch info.

## Step 2: Create Issue
Use mcp__github__create_issue with:
- repo: Extracted from remote URL
- title: Ask user or infer from context
- body: Include branch, file references
- labels: ["bug"] or ["feature-request"]

## Step 3: Report
Show issue URL and number.
```

### Tool Naming Convention

MCP tools use format: `mcp__[server-name]__[tool-name]`

Examples:
- `mcp__github__create_issue`
- `mcp__github__list_issues`
- `mcp__jira__create_ticket`
- `mcp__database__query`

---

## Working Examples

### Example 1: GitHub Integration Server

**Configuration (`.claude/settings.json`):**
```json
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["-m", "mcp_github_server"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

**Server Code (`mcp_github_server/server.py`):**
```python
import os
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server

mcp = Server("github")

class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_issue(self, repo, title, body, labels):
        url = f"{self.base_url}/repos/{repo}/issues"
        data = {"title": title, "body": body, "labels": labels or []}
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_issues(self, repo, state, limit):
        url = f"{self.base_url}/repos/{repo}/issues"
        params = {"state": state, "per_page": limit}
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
def create_issue(
    repo: str,
    title: str,
    body: str = None,
    labels: list = None
) -> dict:
    """Create a GitHub issue."""
    api = GitHubAPI(os.getenv("GITHUB_TOKEN"))
    return api.create_issue(repo, title, body, labels)

@mcp.tool()
def list_issues(
    repo: str,
    state: str = "open",
    limit: int = 10
) -> dict:
    """List GitHub issues."""
    api = GitHubAPI(os.getenv("GITHUB_TOKEN"))
    return api.list_issues(repo, state, limit)

async def main():
    async with stdio_server() as streams:
        await mcp.run(
            streams[0],
            streams[1],
            mcp.create_initialization_options()
        )
```

**Using in Slash Command:**
```markdown
---
description: Create GitHub issue for current bug
allowed-tools: [mcp__github__create_issue, Bash]
---

Create a GitHub issue for the current bug:

1. Get repo from: `git remote get-url origin`
2. Ask user for bug description
3. Call mcp__github__create_issue:
   - repo: Extracted repo name
   - title: "Bug: [user summary]"
   - body: Detailed description
   - labels: ["bug"]
4. Show created issue URL
```

### Example 2: Database Query Server

**Configuration:**
```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["-m", "mcp_database_server"],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "myapp",
        "DB_USER": "user",
        "DB_PASSWORD": "password"
      }
    }
  }
}
```

**Server Code:**
```python
import os
import psycopg2
from mcp.server import Server
from mcp.server.stdio import stdio_server

mcp = Server("database")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@mcp.tool()
def query(sql: str, params: list = None) -> dict:
    """Execute SQL query.

    Args:
        sql: SQL query to execute
        params: Query parameters (optional)

    Returns:
        Query results
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, params or [])

        if sql.strip().upper().startswith("SELECT"):
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return {
                "columns": columns,
                "rows": [dict(zip(columns, row)) for row in rows],
                "count": len(rows)
            }
        else:
            conn.commit()
            return {"affected_rows": cursor.rowcount}
    finally:
        cursor.close()
        conn.close()

async def main():
    async with stdio_server() as streams:
        await mcp.run(
            streams[0],
            streams[1],
            mcp.create_initialization_options()
        )
```

### Example 3: System Monitor Server (Real Example)

**Configuration:**
```json
{
  "mcpServers": {
    "system_monitor": {
      "command": "python",
      "args": ["-m", "system_monitor_mcp"],
      "env": {
        "JIRA_URL": "https://company.atlassian.net",
        "JIRA_EMAIL": "user@company.com",
        "JIRA_API_TOKEN": "xxxxx"
      }
    }
  }
}
```

**Tools Provided:**
- `mcp__system_monitor__create_jira_issue`
- `mcp__system_monitor__fetch_jira_issue`
- `mcp__system_monitor__update_jira_issue`
- `mcp__system_monitor__get_system_metrics`

**Used by DevFlow workflow slash commands:**
```markdown
---
description: Fetch JIRA issue for development
allowed-tools: [mcp__system_monitor__fetch_jira_issue, Write]
---

Fetch issue details:
1. Call mcp__system_monitor__fetch_jira_issue(issue_key)
2. Write to .devflow/current-issue.json
3. Display issue summary
```

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Using Optional[T] for Tool Parameters

**WRONG:**
```python
from typing import Optional

@mcp.tool()
def my_tool(
    required: str,
    optional: Optional[str] = None  # ❌ BREAKS VALIDATION
) -> dict:
    pass
```

**Why it's wrong:** MCP/Pydantic rejects `Optional[T]` type hints.

**RIGHT:**
```python
@mcp.tool()
def my_tool(
    required: str,
    optional: str = None  # ✅ CORRECT
) -> dict:
    pass
```

### ❌ Anti-Pattern 2: MCP Server for Internal Workflows

**WRONG:** Creating MCP server to run code reviews (no external service)

**Why it's wrong:** MCP servers are for EXTERNAL integrations. Use Skill instead.

**RIGHT:** Create Skill with code review logic using Read, Grep, Bash tools.

### ❌ Anti-Pattern 3: Hardcoding Credentials

**WRONG:**
```python
@mcp.tool()
def create_issue():
    token = "ghp_hardcoded_token"  # ❌ NEVER DO THIS
```

**Why it's wrong:** Security risk, can't be changed per environment.

**RIGHT:**
```python
@mcp.tool()
def create_issue():
    token = os.getenv("GITHUB_TOKEN")  # ✅ From env config
```

### ❌ Anti-Pattern 4: Missing Error Handling

**WRONG:**
```python
@mcp.tool()
def create_issue(repo: str, title: str) -> dict:
    response = requests.post(url, json=data)
    return response.json()  # ❌ No error handling
```

**Why it's wrong:** API failures cause cryptic errors for Claude.

**RIGHT:**
```python
@mcp.tool()
def create_issue(repo: str, title: str) -> dict:
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {
            "error": f"GitHub API error: {e.response.status_code}",
            "message": e.response.text
        }
```

### ❌ Anti-Pattern 5: Overly Complex Tools

**WRONG:** Single tool that does 10 different things with mode parameter

**Why it's wrong:** Hard to use, unclear purpose, complex parameter combinations.

**RIGHT:** Create separate tools for each operation:
- `create_issue`
- `update_issue`
- `list_issues`
- `close_issue`

---

## Error Handling Best Practices

### Return Errors as Data

```python
@mcp.tool()
def create_issue(repo: str, title: str) -> dict:
    try:
        # API call
        return {"status": "success", "issue": issue_data}
    except requests.HTTPError as e:
        return {
            "status": "error",
            "error_type": "http_error",
            "status_code": e.response.status_code,
            "message": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": "unknown",
            "message": str(e)
        }
```

### Validate Inputs

```python
@mcp.tool()
def create_issue(repo: str, title: str, body: str = None) -> dict:
    # Validate format
    if "/" not in repo:
        return {
            "status": "error",
            "error_type": "validation",
            "message": "repo must be in format 'owner/repo'"
        }

    if not title or len(title) < 3:
        return {
            "status": "error",
            "error_type": "validation",
            "message": "title must be at least 3 characters"
        }

    # Proceed with API call
```

### Provide Helpful Messages

```python
@mcp.tool()
def create_issue(repo: str, title: str) -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {
            "status": "error",
            "error_type": "configuration",
            "message": "GITHUB_TOKEN environment variable not set. Please configure in settings.json mcpServers.github.env"
        }
```

---

## Testing MCP Servers

### Manual Testing

**Test tool directly:**
```python
# In server code, add test harness
if __name__ == "__main__":
    # Test mode - call tool directly
    result = create_issue(
        repo="owner/repo",
        title="Test issue",
        body="Testing MCP server"
    )
    print(result)
```

**Test via Claude Code:**
1. Configure server in settings.json
2. Restart Claude Code (to load server)
3. Create test slash command that calls tool
4. Invoke slash command
5. Verify tool response

### Debugging

**Add logging:**
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="/tmp/mcp-server.log"
)

@mcp.tool()
def create_issue(repo: str, title: str) -> dict:
    logging.info(f"Creating issue in {repo}: {title}")
    try:
        result = api.create_issue(repo, title)
        logging.info(f"Issue created: {result['number']}")
        return result
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
```

**Check server startup:**
```bash
# Manually start server to see errors
python -m mcp_my_server
```

**Common issues:**
- Server not configured in settings.json
- Wrong command/args in configuration
- Missing environment variables
- Import errors in server code
- Invalid tool parameter types (Optional[T])

---

## Location: Project vs Global

### Project MCP Server (`.claude/settings.json`)

Use when:
- Server specific to this project
- Custom tools for project's domain
- Project-specific API credentials
- Example: Custom internal API integration

### Global MCP Server (`~/.claude/config.json`)

Use when:
- Server used across all projects
- General API integrations (GitHub, JIRA, etc.)
- Shared credentials/configuration
- Example: GitHub, Slack, database clients

---

## Summary Checklist

When creating an MCP server, verify:

- [ ] Server configured in settings.json with unique name
- [ ] Command and args correctly specify how to launch server
- [ ] Environment variables configured for API keys/secrets
- [ ] Tools defined with `@mcp.tool()` decorator
- [ ] Tool parameters use correct types (NO `Optional[T]`)
- [ ] Tool docstrings explain purpose and parameters
- [ ] Error handling returns structured error data
- [ ] Input validation with helpful error messages
- [ ] Server runs as async main with stdio_server
- [ ] Package structure includes __main__.py entry point
- [ ] Dependencies listed in requirements.txt
- [ ] Server tested manually and via Claude Code
- [ ] Skills/commands have server tools in allowed-tools
- [ ] Tool names follow mcp__server__tool convention

---

## Reference

**Official MCP Documentation:**
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Code MCP Guide](https://docs.anthropic.com/claude/docs/mcp-servers)

**Configuration Location:**
- Project: `.claude/settings.json`
- Global: `~/.claude/config.json`

**Tool Naming:** `mcp__[server-name]__[tool-name]`

**Parameter Types:** str, int, float, bool, list, dict (NO `Optional[T]`)

**Communication:** stdio (stdin/stdout) or SSE

**Languages:** Python (recommended) or Node.js

**Entry Point:** `python -m package_name` or `node script.js`
