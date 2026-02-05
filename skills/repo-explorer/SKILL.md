---
name: repo-explorer
description: Explore and analyze GitHub repositories. Use this skill when the user asks to understand, explore, or analyze a codebase, repository structure, or code architecture.
user-invocable: true
context: fork
agent: Explore
---

# Repo Explorer Skill

Explore and analyze GitHub repositories using the Code Understanding MCP server.

## Arguments

| Argument | Description |
|----------|-------------|
| `<url>` | Repository URL (required) |
| `--branch <name>` | Specific branch to analyze |
| `--dirs <list>` | Target specific directories (comma-separated) |
| `--files <list>` | Target specific files (comma-separated) |
| `--max-tokens <n>` | Override max_tokens for source map (capped at 24000, warns >20000) |

## Usage Examples

```
/repo-explorer https://github.com/tobymao/sqlglot
/repo-explorer https://github.com/some/repo --branch develop
/repo-explorer https://github.com/some/repo --dirs src/core,src/utils
/repo-explorer https://github.com/some/repo --files src/main.py,src/config.py
```

---

## CRITICAL: max_tokens Guardrail

When calling `get_source_repo_map`:
- **ALWAYS** pass the `max_tokens` parameter
- **Default**: 15,000
- **Warning threshold**: 20,000 (warn user but allow)
- **Hard cap**: 24,000 (NEVER exceed - refuse if requested)

**Rationale**: Results exceeding ~25K tokens get saved to file instead of returning inline, breaking the skill workflow.

---

## Workflow

### Phase 0: Skill Invocation

1. Announce: "Repo Explorer skill invoked"
2. Parse arguments:
   - Extract repo URL (required)
   - Extract optional `--branch`, `--dirs`, `--files`, `--max-tokens` flags
3. Validate URL is a GitHub URL (must start with `https://github.com/`)
4. If user provided additional instructions beyond the URL, note them for guided exploration

### Phase 1: Repository Setup

1. Load the Code Understanding MCP tools using MCPSearch:
   ```
   MCPSearch: select:mcp__code-understanding__list_cached_repository_branches
   MCPSearch: select:mcp__code-understanding__clone_repo
   ```

2. Check if repo is already cached:
   ```
   list_cached_repository_branches(url=<repo_url>)
   ```

3. If not cached, clone the repository:
   ```
   clone_repo(url=<repo_url>, branch=<branch_if_specified>)
   ```

4. Wait for clone to complete if needed

### Phase 2: Exploration (Route Based on Instructions)

#### IF User Provided Specific Instructions

Follow the user's exploration goals using available tools:

- `get_repo_structure(repo_path, directories?, include_files?)` - Understand organization
- `get_source_repo_map(repo_path, files?, directories?, max_tokens?)` - Get function signatures
- `get_repo_critical_files(repo_path, limit?, include_metrics?)` - Find important files
- `get_repo_documentation(repo_path)` - Find documentation
- `get_repo_file_content(repo_path, resource_path?)` - Read specific file contents

**ENFORCE**: Always pass `max_tokens` to `get_source_repo_map`:
- Use user-specified value if provided (capped at 24000)
- Default to 15000 if not specified
- Warn if value > 20000

Summarize findings according to user's specific goals.

#### IF No Instructions (Standard Analysis)

Execute the standard analysis workflow:

1. **Get repository structure**:
   ```
   get_repo_structure(repo_path=<url>)
   ```

2. **Identify critical files**:
   ```
   get_repo_critical_files(repo_path=<url>, include_metrics=true)
   ```

3. **Find documentation**:
   ```
   get_repo_documentation(repo_path=<url>)
   ```

4. **Get source map for critical files** (with guardrail):
   ```
   get_source_repo_map(repo_path=<url>, max_tokens=15000)
   ```

   If `--dirs` or `--files` specified, pass those parameters:
   ```
   get_source_repo_map(repo_path=<url>, directories=<dirs>, files=<files>, max_tokens=15000)
   ```

### Phase 3: Report

#### Standard Analysis Report Format

When no specific instructions provided, generate this structured report:

```markdown
## Repository Analysis: <repo_name>

### Overview
<1-2 sentences describing what this repository is about>

### Capabilities & Features
<Bulleted list of main capabilities/features>

### Technologies & Languages
<Languages, frameworks, key dependencies>

### Project Structure
<Brief description of organization>
<Key directories and their purposes>

### Critical Files
<List of most important files and why>

### Key Findings
<Any notable patterns, architecture decisions, or insights>
```

#### Guided Exploration Report Format

When user provided specific instructions:
- Answer the user's specific questions
- Organize findings around their goals
- Include relevant code snippets or signatures as needed

---

## Tool Reference

See `references/code-understanding.md` for detailed tool parameters.

### Quick Reference

| Tool | Purpose |
|------|---------|
| `clone_repo` | Clone a repository to cache |
| `list_cached_repository_branches` | Check if repo is cached |
| `get_repo_structure` | Get directory/file tree |
| `get_source_repo_map` | Get function/class signatures |
| `get_repo_critical_files` | Identify important files |
| `get_repo_documentation` | Find documentation files |
| `get_repo_file_content` | Read specific file contents |

---

## Error Handling

- **Invalid URL**: "This skill only supports GitHub URLs. Please provide a URL starting with `https://github.com/`"
- **Clone failed**: Report the error and suggest checking URL/permissions
- **max_tokens > 24000 requested**: "Refusing to use max_tokens > 24000. Results would be saved to file instead of returning inline. Maximum allowed: 24000"
- **max_tokens > 20000 requested**: Warn but proceed: "Warning: Using max_tokens > 20000 may produce large results. Proceeding with <value>."
