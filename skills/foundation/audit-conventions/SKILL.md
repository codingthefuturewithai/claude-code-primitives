---
name: devflow:foundation:audit-conventions
description: Read-only audit comparing a repository's actual state against team conventions. Shows deltas — no file changes, no enforcement, no suggestions.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__rag-memory-primary__list_collections
  - mcp__rag-memory-primary__search_documents
  - mcp__atlassian__searchConfluenceUsingCql
  - mcp__atlassian__getConfluencePage
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__google-drive__search_files
  - mcp__google-drive__download_file
---

# Audit Conventions

**Say exactly:** "SKILL INVOKED: audit-conventions"

Read-only comparison of a repository's actual state against the team's captured conventions. Shows deltas — what the team says vs what the repo does. Nothing more.

## Critical Rules

- **Read-only.** Do not create, modify, or delete any files in the repo. Ever.
- **Report deltas, not judgments.** "Team says X, repo does Y." Not "repo should do X."
- **No suggestions.** Do not recommend fixes, alignment, or changes. Just report what is.
- **Every section gets compared.** Don't skip convention sections because they seem irrelevant.
- **If conventions don't exist, stop.** This skill requires team conventions to audit against.

---

## Step 1: Load Configuration & Find Conventions

**Load DevFlow config:**
1. Read `~/.claude/plugins/config/devflow/config.md`
2. If no config → tell user: "No DevFlow configuration found. Run `/devflow-setup` first." STOP.

**Find team conventions — search all configured backends:**

If **RAG Memory** enabled:
1. `list_collections()` — see what collections exist
2. `search_documents(query="team conventions coding standards workflow")` — search broadly across all collections
3. If found → load the conventions document

If **Confluence** enabled:
1. `searchConfluenceUsingCql(cql="text ~ 'team conventions' AND type = 'page'")`
2. If found → load the page

If **Google Drive** enabled:
1. `search_files(query="conventions")` and `search_files(query="coding standards")`
2. If found → load the document

Also check the repo itself:
- `.claude/rules/team-conventions.md` — portable conventions file

**If nothing found in any location:**
> "No team conventions found. Run `/devflow:foundation:capture-conventions` to capture your team's conventions first."
> STOP.

**If found:** Show the user what was found and confirm it's the right conventions document before proceeding.

---

## Step 2: Analyze the Repository

Examine the repo's actual state across all convention areas:

- **Package files** (package.json, pyproject.toml, Cargo.toml, go.mod) → detect stack, dependencies, scripts
- **Config files** (.eslintrc, tsconfig, prettier, .editorconfig, biome.json) → detect formatter, linter, type settings
- **Test files** → detect test framework, file location, patterns, coverage config
- **CI/CD config** (.github/workflows, .gitlab-ci.yml, Jenkinsfile) → detect CI requirements, merge strategy
- **Directory structure** → detect architecture patterns, monorepo vs single repo
- **Documentation** → detect what docs exist (README, API docs, ADRs, changelog, runbooks)
- **Git history** → detect branching patterns, commit message format, branch naming
- **Security config** → detect dependency scanning, static analysis tools, secrets management

Be thorough. Look at every area the conventions document covers.

---

## Step 3: Generate Delta Report

Compare each section of the team conventions against the repo's actual state.

For each convention item, classify as one of:

- **Aligned** — convention matches repo reality
- **Deviation** — repo does something different from convention
- **Not observable** — can't determine from repo analysis alone
- **Not applicable** — convention doesn't apply to this repo's stack

### Report Format

Present a structured report:

```
# Convention Audit: {repo name}
Date: {YYYY-MM-DD}
Conventions source: {where conventions were loaded from}

## Summary
- Aligned: {count}
- Deviations: {count}
- Not observable: {count}
- Not applicable: {count}

## Tech Stack
| Convention | Team Says | Repo Has | Status |
|-----------|-----------|----------|--------|
| Language | TypeScript | TypeScript | Aligned |
| Framework | Next.js | Express | Deviation |

## Coding Standards
| Convention | Team Says | Repo Has | Status |
|-----------|-----------|----------|--------|
| Formatter | Prettier | Prettier (.prettierrc found) | Aligned |
| Linter | ESLint strict | No ESLint config found | Deviation |

## Testing
...

## Documentation Standards
...

## Git & Workflow
...

## Architecture
...

## Security Practices
...

## Definition of Done
...

## Preferred Libraries
...
```

---

## Step 4: Present Results

Present the full report to the developer.

> "Here's your convention audit. This is a read-only comparison — no changes have been made to your repo."

**Do NOT:**
- Suggest fixing deviations
- Offer to update files
- Recommend aligning with conventions
- Create any documents or files
- Editorialize about whether deviations are good or bad

The developer now has a clear picture of where their repo aligns with and deviates from team conventions. What they do with that information is entirely up to them.

---

## ⛔ STOP

Skill complete.
