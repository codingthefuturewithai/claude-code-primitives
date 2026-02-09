---
name: devflow:foundation:generate-claude-md
description: Analyze a repo and generate a lean CLAUDE.md + .claude/rules/ files. Optionally retrieves team conventions for reconciliation. Use this when setting up a new repo's convention layer or maintaining an existing one.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
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

# Generate / Maintain Repo Convention Layer

**Say exactly:** "SKILL INVOKED: generate-claude-md"

Analyze the current repo, optionally retrieve team conventions, reconcile deviations with you, and generate a lean CLAUDE.md + `.claude/rules/` files.

**All generated files are standalone** — they work for any Claude Code user, no plugin required.

## Critical Rules

- **Developer has override authority.** Conventions are defaults, not mandates.
- **Every deviation is surfaced.** Nothing silently ignored or changed.
- **Standalone output.** Generated files must not reference DevFlow, this plugin, or any external system.
- **Keep CLAUDE.md lean.** ~60 lines max. Everything else goes in `.claude/rules/`.

---

## Step 0: Detect Mode

Check the current repo state to determine which mode to run:

```
Check 1: Does CLAUDE.md exist? (root or .claude/CLAUDE.md)
Check 2: Does .claude/rules/ exist with .md files?
Check 3: Are there substantial source files? (package.json, src/, lib/, app/, etc.)
```

| CLAUDE.md exists | `.claude/rules/` exists | Substantial code | Mode |
|:---:|:---:|:---:|------|
| Yes | Yes | - | **Maintenance** (Step 4) |
| Yes | No | - | **Existing Repo** (Step 1) — will migrate to modular rules |
| No | No | Yes | **Existing Repo** (Step 1) |
| No | No | No | **Greenfield** (Step 3) |

Announce the detected mode:
> "Detected mode: **{mode}**. {brief explanation of what this means}."

---

## Step 1: Existing Repo — Gather Inputs

### 1a: Retrieve Team Conventions (Optional)

Attempt to load team conventions from configured doc backend. This is best-effort — the skill works without them.

**Load DevFlow config:**
1. Read `~/.claude/plugins/config/devflow/config.md`
2. If no config → skip conventions, proceed to 1b

**Search for conventions:**

Search broadly — never assume a specific collection name, folder, or page title.

If **RAG Memory** enabled:
- `search_documents(query="team conventions tech stack coding standards workflow")` — search ALL collections (no `collection_name` filter)
- If multiple results → show user, ask which is their team conventions doc

If **Confluence** enabled:
- `searchConfluenceUsingCql(cql="text ~ 'team conventions' AND type = 'page'")` — broad search
- If found → show results, ask user to confirm, then `getConfluencePage(pageId=id)` to load

If **Google Drive** enabled:
- `search_files(query="conventions")` and `search_files(query="coding standards")`
- If found → show results, ask user to confirm, then `download_file(fileId=id)` to load

**Result:**
- Conventions found and confirmed → store for reconciliation in Step 2
- Not found → inform developer: "No team conventions found in any configured backend. I'll generate from repo analysis alone. You can also point me to where conventions are stored."
- Developer points to a location → load from there. Proceed to 1b.

### 1b: Analyze Repo

Analyze the repository to understand its current state. Use parallel tool calls where possible.

**Package files** — detect stack, dependencies, scripts:
```
Glob: package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml, build.gradle,
      Gemfile, requirements.txt, setup.py, setup.cfg
```
Read each found file for dependencies, scripts, and configuration.

**Config files** — detect existing conventions:
```
Glob: .eslintrc*, eslint.config.*, .prettierrc*, prettier.config.*,
      tsconfig*.json, .editorconfig, ruff.toml, pyproject.toml [tool.ruff],
      .golangci.yml, rustfmt.toml, .stylelintrc*, biome.json
```

**CI/CD config** — extract build/test commands:
```
Glob: .github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile,
      .circleci/config.yml, Makefile, Taskfile.yml, justfile
```

**Directory structure:**
```bash
ls -la  # Root directory
# Then explore key directories: src/, lib/, app/, packages/, services/
```

**README** — extract project context:
```
Glob: README.md, README.rst, README.txt, README
```

**Existing AI config** — migrate relevant content:
```
Glob: .cursorrules, .github/copilot-instructions.md, .aider*
```

**Git history** — infer patterns:
```bash
git log --oneline -20  # Recent commit message patterns
git branch -a          # Branching patterns
```

**Compile analysis into structured findings:**
- Detected stack (languages, frameworks, key dependencies)
- Detected conventions (formatter, linter, type config)
- Build/test commands (from scripts, CI, Makefile)
- Project structure (key directories and their purposes)
- Project context (from README)
- Existing AI config content (if any)

Present summary to developer:
> "Here's what I found in the repo:"
> [Structured summary of findings]

---

## Step 2: Reconciliation (if team conventions exist)

Compare repo analysis against team conventions. For each topic, classify:

**Aligned** — repo matches convention (no action needed):
> "Repo uses {X} — matches team convention."

**Deviation** — repo differs from convention (developer decides):
> "Repo uses {X}, but team convention specifies {Y}."

Use AskUserQuestion:
- Keep repo's choice (rules reflect actual repo state)
- Align with convention (rules reflect the team convention)
- Customize (developer specifies something different)

**Not covered** — repo has something conventions don't address:
> "Repo uses {X} — team conventions don't specify this."
> Captured as-is in rules.

**Missing from repo** — convention specifies something not found in repo:
> "Team convention requires {X}, but not found in repo."

Use AskUserQuestion:
- Add to rules
- Skip for now
- Customize

**Batch resolution:** If there are many deviations, offer:
> "Accept all team conventions for uncontested items? You can override specific ones."

Track all resolutions — these feed into Step 2b.

### 2b: Compile Resolved Decisions

After all deviations are resolved, compile the final set of decisions:
- Per-topic rules (coding standards, testing, git workflow, architecture)
- Build/test commands (from repo analysis)
- Project overview (from README + analysis)
- Key directories (from structure analysis)

Proceed to Step 2c (Generate).

### 2c: Generate

Follow the generation process in **Step 5: Generate Files**.

---

## Step 3: Greenfield Repo

### 3a: Retrieve Team Conventions (Optional)

Same process as Step 1a.

### 3b: Gather Project Info

Ask:
> "What type of project is this?"

If team conventions exist, present applicable stacks:
> "Your team conventions define these project types: {list}. Which applies?"

Ask:
> "Do you have a PRD or project brief I can analyze for context?"
> If yes → ask for path or paste, analyze for architectural decisions.

### 3c: Interview or Apply Conventions

**If conventions exist:**
Present applicable conventions for this project type. For each section, ask:
> "Team convention for {topic}: {value}. Accept, override, or customize?"

**If no conventions:**
Run a lighter interview — just the essentials for this repo:
- Language and framework
- Testing framework and approach
- Git workflow basics
- Key architectural decisions

### 3d: Generate

Follow **Step 5: Generate Files**, but add TODO markers for details that will emerge:

```markdown
<!-- TODO: Update build commands after initial setup -->
<!-- TODO: Add key directories once project structure is established -->
```

---

## Step 4: Maintenance Mode

### 4a: Load Current Convention Layer

Read existing files:
```
Read: CLAUDE.md (or .claude/CLAUDE.md)
Glob: .claude/rules/*.md
```
Read each rules file.

### 4b: Retrieve Team Conventions (Optional)

Same process as Step 1a.

### 4c: Analyze Current Repo State

Same analysis as Step 1b.

### 4d: Drift Report

Compare three sources: existing rules, team conventions, and current repo state.

**Convention drift** (team conventions changed since last sync):
> "Team convention now specifies {X}. Your rules say {Y}."

**Repo drift** (repo changed but rules haven't):
> "New directory `{path}` detected — not covered by rules."
> "New dependency `{dep}` added — not mentioned in rules."
> "Build commands in CI differ from what CLAUDE.md says."

**Stale content** (rules reference things that don't exist):
> "Rules mention `{path}` but it no longer exists."
> "Rules reference `{dep}` but it's not in dependencies."

For each item, use AskUserQuestion to resolve:
- Update rules to match current state
- Keep current rules
- Customize

### 4e: Update Files

Apply resolved changes to affected files only. Present diffs to developer before writing.

Proceed to **Step 5: Generate Files** (update mode — only regenerate changed files).

---

## Step 5: Generate Files

### 5a: Generate Root CLAUDE.md

Use the template from [references/templates/claude-md.md](references/templates/claude-md.md).

Target: ~60 lines. Include only:
- Project name and one-line description
- Build & run commands
- Test commands
- Key directories with brief descriptions
- Important notes (gotchas, environment quirks)

**Do NOT include in CLAUDE.md:** Coding standards, testing philosophy, git workflow, architecture decisions — those go in `.claude/rules/`.

### 5b: Generate Rules Files

For each topic with resolved decisions, generate a rules file using the templates in [references/templates/](references/templates/).

Each rules file should:
- Be focused on ONE topic
- Contain clear, actionable directives (not descriptions)
- Use path-scoping frontmatter for monorepos where applicable
- Include provenance footer: `<!-- Generated by generate-claude-md | Last synced: {YYYY-MM-DD} -->`

**Standard rules files:**
- `.claude/rules/coding-standards.md` — from [references/templates/coding-standards.md](references/templates/coding-standards.md)
- `.claude/rules/testing.md` — from [references/templates/testing.md](references/templates/testing.md)
- `.claude/rules/git-workflow.md` — from [references/templates/git-workflow.md](references/templates/git-workflow.md)
- `.claude/rules/architecture.md` — from [references/templates/architecture.md](references/templates/architecture.md)

Only generate rules files that have substance. If a topic has no meaningful rules (e.g., "use language defaults for everything"), skip that file.

### 5c: Present for Review

Show all generated files with full content:

> "Here are the files I'll create:"
>
> **CLAUDE.md** (~{N} lines):
> ```
> [full content]
> ```
>
> **.claude/rules/coding-standards.md** (~{N} lines):
> ```
> [full content]
> ```
> [... for each file]

Ask:
> 1. Write all files
> 2. Edit a file before writing
> 3. Cancel

If "Edit" → ask which file and what to change, regenerate, re-present.

### 5d: Write Files

1. Create `.claude/rules/` directory if needed: `mkdir -p .claude/rules`
2. Write each file
3. Confirm what was written

### 5e: Suggest Commit

> "Convention layer generated. Suggested commit:"
> ```
> git add CLAUDE.md .claude/rules/
> git commit -m "feat: Add convention layer (CLAUDE.md + .claude/rules/)"
> ```
> Want me to commit these files?

---

## ⛔ STOP

Skill complete. Convention layer generated.

> **Maintenance:** Re-run this skill anytime to detect drift and update your convention layer.
> **Team conventions:** If your team updates their conventions, re-run to sync.
