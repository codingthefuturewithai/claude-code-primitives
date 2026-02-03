# Local Issue Adapter (Stub)

## Overview

Local issue tracking using Markdown files. **Future implementation.**

---

## Planned Structure

```
.devflow/
└── issues/
    ├── 001-implement-feature.md
    ├── 002-fix-bug.md
    └── _index.md
```

---

## Planned File Format

```markdown
---
id: 001
title: Implement feature X
status: in_progress
priority: high
created: 2024-01-15
labels: [feature, frontend]
---

# Implement feature X

## Description
...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
...
```

---

## Planned Operations

| Operation | Implementation |
|-----------|---------------|
| Fetch | Read markdown file |
| Create | Write new markdown file |
| Update | Edit markdown file |
| Transition | Update `status` in frontmatter |
| Comment | Append to Notes section |
| Search | Grep across issue files |

---

## Status Values

- `todo`
- `in_progress`
- `review`
- `done`

---

## Not Yet Implemented

This adapter is a placeholder for future local-only workflows.

Current DevFlow requires either:
- Jira (via Atlassian MCP)
- GitLab (via GitLab MCP)

To use DevFlow without external issue tracking, run:
```
/devflow:admin:setup
```
And select "Skip issue tracking" option.
