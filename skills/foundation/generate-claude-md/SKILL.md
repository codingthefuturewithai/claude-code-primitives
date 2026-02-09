---
name: devflow:foundation:generate-claude-md
description: Analyze a repo, surface deltas against team conventions, and help the developer create or update their convention layer (CLAUDE.md + .claude/rules/). Developer is always in control.
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

Analyze the current repo, optionally retrieve team conventions as advisory context, surface deltas, and help the developer create or update their convention layer. The developer decides everything.

**All generated files are standalone** — they work for any Claude Code user, no plugin required.

## Critical Rules

- **Developer is the authority.** Team conventions are advisory context, not mandates. The developer decides what goes into their repo — including nothing at all.
- **Observe, don't prescribe.** Surface deltas as observations ("I notice this repo uses X, team conventions say Y"), never as directives ("You should change X to Y").
- **Generate only what's approved.** Never write files the developer didn't explicitly approve.
- **Trust Claude's intelligence.** Don't spell out what Claude already knows about languages, frameworks, or tools. Focus on team-specific decisions and project-specific patterns Claude can't infer.
- **Keep it compact.** CLAUDE.md ~60 lines max. Rules files should be concise directives, not tutorials.
- **Respect what exists.** If there's already a CLAUDE.md or rules files, they represent the developer's current intent. Don't assume they need replacing.
- **No separate modes.** The flow is always the same: understand what's here → retrieve conventions → show deltas → developer decides → write what they approved. The starting context differs (greenfield vs existing vs already has rules), but the conversation is the same.

---

## Step 1: Understand What's Here

### 1a: Detect Repo Shape

Determine where you are and what kind of repo this is.

```bash
git rev-parse --show-toplevel    # Find repo root
pwd                               # Current directory
```

**Check for monorepo indicators** (at repo root):
```
Glob: pnpm-workspace.yaml, lerna.json, nx.json, turbo.json,
      rush.json, package.json (check for "workspaces" field),
      Cargo.toml (check for [workspace]), go.work
```

**Classify the situation:**

| Where am I? | Monorepo? | Scope |
|---|---|---|
| Repo root | No | Single-project repo |
| Repo root | Yes | Monorepo root — team-general conventions belong here |
| Project directory in monorepo | Yes | Project-level — project-specific only, don't duplicate root |
| Arbitrary subdirectory | — | Ask: "You're in `{path}`. Should I scope to the repo root, a specific project, or this directory?" |

**If at monorepo root**, identify the projects:
- List workspace members / top-level project directories
- Note which have their own package files, CLAUDE.md, or `.claude/rules/`

**If at project level in monorepo**, check what exists at root:
- Root CLAUDE.md? Root `.claude/rules/`?
- Note what's already covered at root — don't duplicate it

Announce:
> "I'm in `{path}`. This looks like a **{single-project repo / monorepo root with N projects / project within a monorepo}**."

### 1b: Check Existing Convention Layer

```
Glob: CLAUDE.md, .claude/CLAUDE.md
Glob: .claude/rules/*.md
```

If files exist, read them — they represent the developer's current intent.

### 1c: Analyze the Repo/Project

Use parallel tool calls where possible.

**Package files** — detect stack and dependencies:
```
Glob: package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml,
      build.gradle, Gemfile, requirements.txt, setup.py, setup.cfg,
      composer.json, mix.exs, Project.toml
```
Read each found file for dependencies, scripts, and configuration.

**Config files** — detect existing tool conventions:
```
Glob: .eslintrc*, eslint.config.*, .prettierrc*, prettier.config.*,
      tsconfig*.json, .editorconfig, ruff.toml, .golangci.yml,
      rustfmt.toml, .stylelintrc*, biome.json, .clang-format
```

**CI/CD config** — extract build/test commands:
```
Glob: .github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile,
      .circleci/config.yml, Makefile, Taskfile.yml, justfile, Dockerfile
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

**Existing AI config** — note any existing conventions:
```
Glob: .cursorrules, .github/copilot-instructions.md, .aider*
```

**Git history** — infer patterns:
```bash
git log --oneline -20    # Recent commit message patterns
git branch -a 2>/dev/null | head -20   # Branching patterns
```

For **greenfield repos** (minimal or no code): most of this returns nothing — that's fine. Note what's absent.

---

## Step 2: Retrieve Team Conventions (Optional)

Attempt to load team conventions from the configured doc backend. These are **advisory context** — not requirements to apply.

**Load DevFlow config:**
1. Read `~/.claude/plugins/config/devflow/config.md`
2. If no config → skip conventions, proceed to Step 3

**Search broadly** — never assume a specific collection name, folder, or page title:

If **RAG Memory** enabled:
- `search_documents(query="team conventions tech stack coding standards workflow")` — no `collection_name` filter
- If multiple results → show developer, ask which is their team conventions doc

If **Confluence** enabled:
- `searchConfluenceUsingCql(cql="text ~ 'team conventions' AND type = 'page'")`
- If found → show results, ask developer to confirm, then `getConfluencePage(pageId=id)`

If **Google Drive** enabled:
- `search_files(query="conventions")` and `search_files(query="coding standards")`
- If found → show results, ask developer to confirm, then `download_file(fileId=id)`

**Result:**
- Found and confirmed → store as advisory reference for Step 3
- Not found → proceed without. Inform developer: "No team conventions found. I'll work from the repo analysis."

---

## Step 3: Present the Picture

Show the developer a clear, honest picture of their repo. If team conventions are available, show how the repo relates to them.

### Existing Repo (has code)

Present the repo analysis:
> "Here's what I found in your repo:"
> - **Stack:** {languages, frameworks, key dependencies}
> - **Build/test:** {detected commands}
> - **Structure:** {key directories and their purposes}
> - **Existing convention layer:** {what CLAUDE.md and rules files exist and cover}
> - **Detected tool config:** {formatter, linter, type config from config files}

If team conventions available, present deltas as neutral observations:

> "Your team conventions are available for reference. Here's how this repo compares:"
>
> **Aligned:**
> - {item} — matches convention
>
> **Differences:**
> - This repo uses {X}. Team conventions say {Y}.
>
> **In conventions but not in repo:**
> - Team conventions specify {X}. Not found in this repo.
>
> **In repo but not in conventions:**
> - This repo uses {X}. Not covered by team conventions.

**Important framing:** Every delta is an observation. No judgment, no recommendation. "This repo uses Mantine 8. Team conventions specify shadcn/ui." Full stop. The developer knows their repo better than the skill does.

### Greenfield Repo (minimal or no code)

> "This looks like a new repo."

If team conventions available:
> "Your team conventions cover these project types: {list from conventions}. What are you building?"

Ask project type. Then ask:
> "Do you have a PRD, project brief, or description I can use for context?"
> - Yes → ask for path or paste, analyze for architectural decisions and project context
> - No → proceed with project type + conventions

If no conventions:
> "No team conventions found. What type of project will this be? I can help scaffold a starting CLAUDE.md."

### Already Has Convention Layer

If CLAUDE.md and/or `.claude/rules/` exist:
> "You already have a convention layer. Here's what it covers:"
> [Summary of existing files]

If team conventions available, show drift:
> "Since your last sync, here's what changed:"
> - **Convention layer says {X}, repo now does {Y}** (repo drifted)
> - **Team conventions now say {X}, your rules say {Y}** (conventions updated)
> - **Rules mention {X} but it no longer exists in the repo** (stale content)

---

## Step 4: Developer Decides

Ask what the developer wants help with. Adapt options to context.

Use AskUserQuestion (multiSelect):
> "What would you like me to help with?"

**If no convention layer exists:**
- Create a CLAUDE.md (build commands, key directories, project notes)
- Add a team conventions reference file (`.claude/rules/team-conventions.md`)
- Document project architecture (`.claude/rules/architecture.md`)
- Nothing right now — I'll set things up myself

**If convention layer already exists:**
- Update CLAUDE.md with current repo state
- Update or add team conventions reference
- Update or add architecture notes
- Walk me through the deltas so I can decide what to change
- Leave everything as is

**If greenfield:**
- Scaffold a starting CLAUDE.md from project type (+ conventions if available)
- Just create a minimal CLAUDE.md — I'll fill it in as the project develops
- Nothing yet — too early

**If at monorepo root:**
- Create root CLAUDE.md (workspace overview, shared commands)
- Add team conventions reference at root level
- Help me set up per-project convention layers
- Nothing right now

The developer may select multiple items or none. **"Nothing" is a perfectly valid answer.** Respect it.

---

## Step 5: Draft and Review

For each item the developer selected, draft the content and present for review.

### CLAUDE.md

Focus on what Claude can't figure out on its own:
- Project name and one-line description
- Build, run, and test commands (exact commands from package files, CI, Makefile)
- Key directories with brief descriptions
- Important notes / gotchas / environment quirks
- Environment variables (if applicable)

Target ~60 lines. **Do NOT include:** coding standards, testing philosophy, git workflow, architectural explanations, or anything Claude already knows about the tech stack. Those are either covered by conventions, in separate rules files, or unnecessary.

**For greenfield:** include what's known, use TODO markers for what will emerge:
```markdown
<!-- TODO: Update build commands after initial setup -->
<!-- TODO: Add key directories once project structure is established -->
```

**For monorepo root:** workspace structure, shared commands, how projects relate, how to navigate.

**For project in monorepo:** this project's commands, directories, gotchas. Note: "Team conventions and shared rules are at the repo root."

### Team Conventions Reference (.claude/rules/team-conventions.md)

Only if the developer asked for it. Include relevant sections from team conventions — compact, in the team's own words, not rewritten or expanded.

```markdown
# Team Conventions Reference

Source: {where conventions are stored}
Last synced: {YYYY-MM-DD}

## Applicable Conventions
{Relevant sections from team conventions document, compactly}

## This Repo's Differences
- {What}: {repo value} (convention: {convention value})
```

Keep it factual. The "Differences" section captures what IS, not what SHOULD BE.

**For monorepo:** this file belongs at the repo root, not in each project directory. Claude Code loads parent rules recursively, so project-level work inherits root rules automatically.

**For project in monorepo where root already has this file:** don't create a duplicate. If the project has project-specific differences, create a separate file (e.g., `.claude/rules/project-notes.md`).

### Architecture Notes (.claude/rules/architecture.md)

Only if the developer asked for it AND the project has patterns worth documenting. Focus on:
- Architectural decisions and the reasoning behind them (the "why")
- How to add common things (new view, new endpoint, new module, new service)
- Key constraints or non-obvious patterns
- Things Claude would get wrong without this context

**Don't document:** things Claude can figure out by reading code, general framework knowledge, standard patterns.

### Other Rules Files

If the developer wants additional rules files for specific topics, draft them. Keep them concise — directives, not explanations.

For monorepo path-scoping:
```yaml
---
paths:
  - "packages/frontend/**"
---
```

### Present for Review

Show all drafted files with full content:

> "Here's what I'll create:"
>
> **CLAUDE.md** (~{N} lines):
> ```
> [full content]
> ```
>
> **.claude/rules/{filename}.md** (~{N} lines):
> ```
> [full content]
> ```
> [repeat for each file]

Ask:
> 1. Write all files
> 2. Edit a file before writing
> 3. Drop a file (don't create it)
> 4. Cancel everything

If "Edit" → ask what to change, redraft, re-present.

---

## Step 6: Write Approved Files

1. Create `.claude/rules/` directory if needed: `mkdir -p .claude/rules`
2. Write each approved file
3. Confirm what was written
4. Suggest commit:

> "Convention layer {created / updated}. Suggested commit:"
> ```
> git add CLAUDE.md .claude/rules/
> git commit -m "{feat/chore}: {Add/Update} convention layer (CLAUDE.md + .claude/rules/)"
> ```
> Want me to commit these files?

---

## ⛔ STOP

Skill complete.

> **Next:** Re-run this skill anytime to check for drift between your repo, your convention layer, and team conventions.
