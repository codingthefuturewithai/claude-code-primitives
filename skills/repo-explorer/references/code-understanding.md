# Code Understanding MCP Server - Tool Reference

This document provides detailed parameter documentation for the Code Understanding MCP server tools used by the repo-explorer skill.

---

## CRITICAL: max_tokens Guardrail

When calling `get_source_repo_map`:

| Threshold | Value | Behavior |
|-----------|-------|----------|
| Default | 15,000 | Use when no value specified |
| Warning | 20,000 | Warn user but allow |
| Hard Cap | 24,000 | **NEVER exceed** - refuse if requested |

**Rationale**: Results exceeding ~25K tokens get saved to file instead of returning inline, breaking the workflow. The skill requires inline results to function properly.

**Enforcement**:
- Always explicitly pass `max_tokens` parameter
- If user requests > 24000, refuse with explanation
- If user requests > 20000, warn but proceed

---

## Tools

### clone_repo

Clone a GitHub repository to the local cache for analysis.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | GitHub repository URL |
| `branch` | string | No | Specific branch to clone (defaults to default branch) |
| `cache_strategy` | string | No | Caching strategy to use |

**Example:**
```
clone_repo(
    url="https://github.com/tobymao/sqlglot",
    branch="main"
)
```

---

### list_cached_repository_branches

Check if a repository is already cached and list available branches.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | GitHub repository URL |

**Example:**
```
list_cached_repository_branches(
    url="https://github.com/tobymao/sqlglot"
)
```

**Returns**: List of cached branches or indication that repo is not cached.

---

### get_repo_structure

Get the directory and file structure of a repository.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repo_path` | string | Yes | Repository URL or local path |
| `directories` | list[string] | No | Specific directories to analyze |
| `include_files` | boolean | No | Whether to include files in output |

**Example:**
```
get_repo_structure(
    repo_path="https://github.com/tobymao/sqlglot",
    directories=["sqlglot/dialects"],
    include_files=true
)
```

---

### get_source_repo_map

Get function and class signatures from repository source code. This is the primary tool for understanding code structure.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repo_path` | string | Yes | Repository URL or local path |
| `files` | list[string] | No | Specific files to analyze |
| `directories` | list[string] | No | Specific directories to analyze |
| `max_tokens` | integer | **Always pass** | Maximum tokens in response |

**max_tokens Guidelines:**
- **Default**: 15,000 (use when not specified)
- **Warning**: > 20,000 (warn user but proceed)
- **Hard cap**: 24,000 (NEVER exceed)

**Example:**
```
get_source_repo_map(
    repo_path="https://github.com/tobymao/sqlglot",
    directories=["sqlglot/optimizer"],
    max_tokens=15000
)
```

**Returns**: Function signatures, class definitions, method signatures organized by file.

---

### get_repo_critical_files

Identify the most important files in a repository based on various metrics.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repo_path` | string | Yes | Repository URL or local path |
| `limit` | integer | No | Maximum number of files to return |
| `include_metrics` | boolean | No | Include importance metrics in output |

**Example:**
```
get_repo_critical_files(
    repo_path="https://github.com/tobymao/sqlglot",
    limit=20,
    include_metrics=true
)
```

**Returns**: List of critical files ranked by importance, with optional metrics.

---

### get_repo_documentation

Find and retrieve documentation files from a repository.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repo_path` | string | Yes | Repository URL or local path |

**Example:**
```
get_repo_documentation(
    repo_path="https://github.com/tobymao/sqlglot"
)
```

**Returns**: List of documentation files (README, docs/, etc.) with contents or summaries.

---

### get_repo_file_content

Read the contents of a specific file from the repository.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repo_path` | string | Yes | Repository URL or local path |
| `resource_path` | string | No | Path to specific file within repo |

**Example:**
```
get_repo_file_content(
    repo_path="https://github.com/tobymao/sqlglot",
    resource_path="sqlglot/optimizer/optimize.py"
)
```

**Returns**: Full file contents.

---

### list_repository_branches

List all branches for a repository.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | GitHub repository URL |

---

### list_remote_branches

List remote branches for a repository.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | GitHub repository URL |

---

### refresh_repo

Refresh/update a cached repository.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | GitHub repository URL |

---

## Typical Workflow

1. **Check cache**: `list_cached_repository_branches(url)`
2. **Clone if needed**: `clone_repo(url, branch)`
3. **Explore structure**: `get_repo_structure(repo_path)`
4. **Find key files**: `get_repo_critical_files(repo_path, include_metrics=true)`
5. **Get signatures**: `get_source_repo_map(repo_path, max_tokens=15000)`
6. **Read specific files**: `get_repo_file_content(repo_path, resource_path)`
