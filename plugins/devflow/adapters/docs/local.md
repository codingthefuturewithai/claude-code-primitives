# Local Documentation Adapter (Stub)

## Overview

Local documentation using Markdown files. **Future implementation.**

---

## Planned Structure

```
.devflow/
└── docs/
    ├── plans/
    │   └── issue-123-implementation-plan.md
    ├── technical/
    │   └── architecture.md
    └── _index.md
```

---

## Planned File Format

```markdown
---
title: Implementation Plan for Issue 123
type: plan
created: 2024-01-15
issue: 123
tags: [feature, backend]
---

# Implementation Plan

## Overview
...

## Steps
1. ...
2. ...

## Notes
...
```

---

## Planned Operations

| Operation | Implementation |
|-----------|---------------|
| Create | Write new markdown file |
| Read | Read markdown file |
| Update | Edit markdown file |
| Search | Grep across doc files |
| List | Glob pattern match |

---

## Not Yet Implemented

This adapter is a placeholder for future local-only workflows.

Current DevFlow documentation options:
- Confluence (via Atlassian MCP)
- Google Docs (via Google Workspace MCP)
- RAG Memory (for AI-retrievable knowledge)

To use DevFlow without external documentation:
```
/devflow-setup
```
And skip the documentation option, or use RAG Memory only.
