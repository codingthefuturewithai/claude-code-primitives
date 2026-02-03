# RAG Memory MCP Server Setup

## Overview

RAG Memory is an AI-retrievable knowledge base that stores documents with semantic search and knowledge graph capabilities.

**Repository:** https://github.com/codingthefuturewithai/mcp-rag-memory

---

## Prerequisites

- Docker and Docker Compose
- Available port (default: 3333)

---

## Step 1: Clone Repository

```bash
cd ~
git clone https://github.com/codingthefuturewithai/mcp-rag-memory.git
cd mcp-rag-memory
```

---

## Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` as needed. Default settings work for most setups.

Key settings:
```
MCP_PORT=3333
DATA_DIR=./data
```

---

## Step 3: Start Server

```bash
docker compose up -d
```

### Verify Container

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Should show the RAG Memory container running on port 3333.

---

## Step 4: Add to Claude Code

```bash
claude mcp add --transport http rag-memory http://localhost:3333/mcp
```

### Verify Connection

Restart Claude Code, then run:
```
/mcp
```

Should show:
```
rag-memory: http://localhost:3333/mcp (HTTP) - ✓ Connected
```

---

## Test the Connection

Try listing collections:
```
Call mcp__rag-memory__list_collections
```

---

## Initial Setup

After connecting, run the DevFlow setup command to create recommended collections:
```
/devflow:rag-memory:setup-collections
```

This creates collections for:
- Technical knowledge
- Project documentation
- Quick notes
- Agent preferences

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Ensure container is running: `docker ps` |
| Port conflict | Change MCP_PORT in .env and restart |
| Database errors | Check data directory permissions |

### Restart Server

```bash
cd ~/mcp-rag-memory
docker compose down
docker compose up -d
```

### View Logs

```bash
docker compose logs -f
```

---

## Quick Reference

| Setting | Value |
|---------|-------|
| Repository | codingthefuturewithai/mcp-rag-memory |
| Default Port | 3333 |
| MCP Endpoint | http://localhost:3333/mcp |
| Transport | HTTP |
| Data Storage | Local (./data directory) |

---

## Usage Tips

### Collections

Organize content by domain:
- `technical-knowledge` - How-to guides, best practices
- `project-docs` - Project-specific documentation
- `quick-notes` - Short snippets, reminders
- `agent-preferences` - AI agent routing rules

### Ingestion

RAG Memory supports:
- Text content (`ingest_text`)
- URLs/websites (`ingest_url`)
- Local files (`ingest_file`)
- Directories (`ingest_directory`)

### Search

Use natural language questions for best results:
- Good: "How do I configure OAuth for GitLab?"
- Less effective: "gitlab oauth config"
