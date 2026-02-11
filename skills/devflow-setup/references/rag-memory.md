# RAG Memory — Detection & Setup

## Step 1: Detection

Test RAG Memory MCP access:
```
Call mcp__rag-memory-primary__list_collections
```

---

## If Detection Succeeds

> "RAG Memory MCP connected."

If collections already exist, display them:
> "Existing collections: [list]"

> "After setup completes, you can run `/devflow:rag-memory:setup-collections` to create recommended collections."

Store:
- `RAG_ENABLED = true`

Return to SKILL.md for next step.

---

## If Detection Fails

Present options:
> "RAG Memory MCP not available. Would you like:"
> 1. I already set it up — Help me connect it
> 2. Help me set it up — First-time setup
> 3. Skip RAG Memory

### Option 1: Already Set Up — Troubleshooting

> "To connect your existing RAG Memory to Claude Code:
>
> **Step 1: Verify container is running**
> ```bash
> docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
> ```
> Look for the RAG Memory container on port 3333.
>
> If not running:
> ```bash
> cd ~/mcp-rag-memory
> docker compose up -d
> ```
>
> **Step 2: Add to Claude Code**
> ```bash
> claude mcp add --transport http rag-memory http://localhost:3333/mcp
> ```
>
> **Step 3: Restart Claude Code** (Cmd+Q and relaunch)
>
> **Step 4: Verify** — Run `/mcp` and confirm `rag-memory: ... - ✓ Connected`"

| Issue | Solution |
|-------|----------|
| Connection refused | Container not running or wrong port |
| Port conflict | Change `MCP_PORT` in .env and restart |
| Database errors | Check data directory permissions |

After troubleshooting:
> 1. I've fixed it — Try detection again
> 2. Skip RAG Memory for now

If "Try again" → retry from Step 1.

### Option 2: First-Time Setup

> **Step 1: Clone Repository**
> ```bash
> cd ~
> git clone https://github.com/codingthefuturewithai/mcp-rag-memory.git
> cd mcp-rag-memory
> ```
>
> **Step 2: Configure**
> ```bash
> cp .env.example .env
> ```
> Default settings work for most setups. Key settings:
> ```
> MCP_PORT=3333
> DATA_DIR=./data
> ```
>
> **Step 3: Start Server**
> ```bash
> docker compose up -d
> ```
>
> **Step 4: Add to Claude Code**
> ```bash
> claude mcp add --transport http rag-memory http://localhost:3333/mcp
> ```
>
> **Step 5: Restart Claude Code** (Cmd+Q and relaunch)
>
> **Step 6: Verify** — Run `/mcp` and confirm `rag-memory: ... - ✓ Connected`
>
> Then re-run `/devflow-setup` to continue configuration.

### Option 3: Skip

Set `RAG_ENABLED = false`. Return to SKILL.md.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `enabled` | `true` |
