---
name: devflow:foundation:capture-conventions
description: Guided interview to capture team-wide conventions and store them in your configured doc backend. Use this when setting up team conventions for the first time or updating existing ones.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__searchConfluenceUsingCql
  - mcp__atlassian__getConfluenceSpaces
  - mcp__atlassian__createConfluencePage
  - mcp__atlassian__updateConfluencePage
  - mcp__google-drive__search_files
  - mcp__google-drive__upload_file
  - mcp__google-drive__create_folder
  - mcp__google-drive__get_file_info
  - mcp__rag-memory-primary__list_collections
  - mcp__rag-memory-primary__search_documents
  - mcp__rag-memory-primary__ingest_text
  - mcp__rag-memory-primary__get_document_by_id
  - mcp__rag-memory-primary__update_document
  - mcp__rag-memory-primary__create_collection
hooks:
  PreToolUse:
    - matcher: "mcp__rag-memory-primary__ingest_text"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/rag-memory-approval.py"
    - matcher: "mcp__rag-memory-primary__update_document"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/rag-memory-approval.py"
    - matcher: "mcp__rag-memory-primary__create_collection"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/rag-memory-approval.py"
    - matcher: "mcp__atlassian__createConfluencePage"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/atlassian-approval.py"
    - matcher: "mcp__atlassian__updateConfluencePage"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/atlassian-approval.py"
    - matcher: "mcp__google-drive__upload_file"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/google-drive-approval.py"
    - matcher: "mcp__google-drive__create_folder"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/google-drive-approval.py"
---

# Capture Team Conventions

**Say exactly:** "SKILL INVOKED: capture-conventions"

Guided interview to capture your team's conventions and store them centrally. These conventions can later be used by `/devflow:foundation:generate-claude-md` to generate consistent CLAUDE.md + `.claude/rules/` files across all your repos.

## Critical Rules

- **Progressive disclosure** — only ask about project types the team actually uses
- **Human gates** — confirm each section before moving to the next
- **Never guess** — if something is ambiguous, ask
- **Re-runnable** — if conventions already exist, load them and let the user update specific sections
- **Triggers, not mandates** — present topics as "does your team do this?" not "you should do this"

---

## Step 0: Load Configuration & Check for Existing Conventions

**Load DevFlow config:**
1. Read `~/.claude/plugins/config/devflow/config.md`
2. If no config → tell user: "No DevFlow configuration found. Run `/devflow-setup` first to configure your backends." STOP.

**Determine doc backend:**
- If `docs.enabled=true` → use configured docs backend (Confluence or Google Drive)
- If `rag-memory.enabled=true` → RAG Memory is available
- If neither → tell user: "No documentation backend configured. Run `/devflow-setup` to enable one." STOP.

**Check for existing conventions (search broadly — never assume location):**

Search ALL configured backends for anything resembling team conventions. Do NOT assume a specific collection name, folder, or page title.

If **RAG Memory** enabled:
1. `list_collections()` — see what collections exist
2. `search_documents(query="team conventions tech stack coding standards workflow")` — search across ALL collections (no `collection_name` filter)
3. If relevant results found → show user what was found, ask if this is their existing conventions doc

If **Confluence** enabled:
1. Search broadly: `searchConfluenceUsingCql(cql="text ~ 'team conventions' AND type = 'page'")` — or similar broad search
2. If found → show results, ask user if any of these are their conventions

If **Google Drive** enabled:
1. `search_files(query="conventions")` and `search_files(query="coding standards")`
2. If found → show results, ask user if any of these are their conventions

If nothing found in any backend:
> "I didn't find existing team conventions in any of your configured backends. Would you like to:"
> 1. Start fresh with the interview
> 2. Point me to where your conventions are stored
> 3. Cancel

If user points to a location → load from there, go to **Update Flow**.

### Update Flow

Present current conventions:
> "Found existing team conventions. Here's a summary:"
> [Show section headings and key values]

Ask:
> "What would you like to do?"
> 1. Update specific sections
> 2. Start fresh (replace everything)
> 3. View full document
> 4. Cancel

If "Update specific sections" → ask which sections, then run only those interview sections. Merge updates into existing document.

---

## Step 1: Team Identity

Ask using AskUserQuestion:
> "Let's capture your team's conventions. First, some basics."

**Team/org name** — free text

**Primary domains** — ask in two rounds to stay within the 4-option limit of AskUserQuestion:

Round 1 (multiSelect):
> "What types of projects does your team work on?"
> - Web / Frontend (SPAs, SSR sites, static sites)
> - Backend / API services (REST, GraphQL, microservices, CLI tools)
> - Mobile apps (iOS, Android, cross-platform)
> - Data / ML / DevOps (pipelines, models, IaC, CI/CD)

Round 2 (multiSelect):
> "Any additional project types?"
> - Libraries / SDKs (reusable packages, open source)
> - Desktop applications (Electron, Tauri, native)
> - Embedded / IoT
> - None — that covers it

Store selections — these determine which tech stack sections to ask about in Step 2.

**Confirm:** Show summary, ask if correct before proceeding.

---

## Step 2: Tech Stack

Only ask about project types selected in Step 1. For each relevant type, follow the interview guide.

See [references/interview-guide.md](references/interview-guide.md) for the full question bank organized by project type.

For each project type:
1. Ask the questions from the interview guide
2. Use AskUserQuestion with sensible defaults based on domain
3. Allow "Other" for every question (free text input)
4. Confirm the section before moving on

---

## Step 3: Coding Standards

Ask about:
- **Formatter** — with common options based on detected languages from Step 2
- **Linter** — same approach
- **Type strictness** — strict, gradual, or optional
- **Naming conventions** — any deviations from language defaults
- **Error handling philosophy** — Result types, exceptions, error codes

Confirm section.

---

## Step 4: Code Quality & Refactoring

Frame as: "Let's talk about code quality expectations — these are triggers for thinking, not hard rules."

Ask about:
- **File/module size guidance** — do you have a target max? (e.g., ~300 lines, no limit, "use judgment")
- **Function/method length** — preferred max? (e.g., ~30 lines, no limit, "fits on one screen")
- **DRY threshold** — when to extract vs duplicate? (e.g., "rule of three", "never duplicate", "use judgment")
- **Dead code policy** — delete immediately, comment out, keep behind feature flags?
- **Refactoring triggers** — what prompts a refactoring pass? (e.g., before adding features to messy code, during PR review, scheduled refactoring sprints, opportunistic)
- **Complexity awareness** — does the team track or discuss cyclomatic complexity, cognitive complexity, or similar metrics? (e.g., "we use SonarQube", "informal awareness", "not something we track")

See [references/interview-guide.md](references/interview-guide.md) for the full question bank.

Confirm section.

---

## Step 5: Testing Conventions

Ask about:
- **Test framework** per stack (based on languages from Step 2)
- **Coverage requirements** — percentage or philosophy
- **Testing philosophy** — TDD, test-after, test-critical-paths
- **Unit vs integration vs E2E balance**
- **Test file location** — colocated or separate directory
- **Mocking approach** — minimal, mock-external-only, liberal

Confirm section.

---

## Step 6: Documentation Standards

Frame as: "What does your team expect when it comes to documentation?"

Ask about:
- **README expectations** — what should every repo's README contain? (e.g., setup instructions, architecture overview, minimal, comprehensive)
- **API documentation** — do you use a spec format? (e.g., OpenAPI/Swagger, GraphQL schema, AsyncAPI, no formal spec, auto-generated)
- **Architecture Decision Records (ADRs)** — does the team write ADRs? (e.g., yes with a template, informal design docs, no)
- **Changelog** — how do you track changes? (e.g., CHANGELOG.md, auto-generated from commits, release notes only, none)
- **Code comments** — expectations? (e.g., only non-obvious logic, JSDoc/docstrings for public APIs, minimal, comprehensive)
- **Runbook/operational docs** — do you maintain them? (e.g., yes in wiki, yes in repo, ad hoc, no)

See [references/interview-guide.md](references/interview-guide.md) for the full question bank.

Confirm section.

---

## Step 7: Git & Workflow

Ask about:
- **Branching strategy** — Git Flow, GitHub Flow, trunk-based, custom
- **Branch naming** — conventions for feature, bugfix, hotfix branches
- **Commit message format** — Conventional Commits, issue key prefix, freeform
- **PR/MR size and reviews** — preferred PR/MR size, number of approvals, CODEOWNERS
- **CI requirements** — what must pass before merge? (e.g., tests, lint, type check, security scan, coverage threshold)
- **Merge strategy** — squash, merge commit, rebase
- **Release process** — tags, release branches, automated from main, manual
- **Environment promotion** — how code moves from dev → staging → production

See [references/interview-guide.md](references/interview-guide.md) for the full question bank.

Confirm section.

---

## Step 8: Architecture Preferences

Ask about:
- **Monorepo vs polyrepo**
- **Preferred patterns** — clean architecture, hexagonal, MVC, etc.
- **Error handling** — global handler, per-layer, error boundaries
- **Logging** — structured JSON, levels, library
- **Environment management** — dotenv, Vault, SSM
- **Dependency management** — pin exact, allow ranges, auto-update

Confirm section.

---

## Step 9: Security Practices

Frame as: "Let's capture what your team does around security — every team is different, so I'll ask rather than assume."

Ask about:
- **Dependency scanning** — do you scan dependencies for vulnerabilities? (e.g., Snyk, Dependabot alerts, npm audit, pip-audit, GitHub security advisories, no formal process)
- **Input validation** — where does the team validate? (e.g., at API boundaries only, every layer, schema-driven with Zod/Pydantic, ad hoc)
- **Secrets management** — how are secrets handled? (e.g., dotenv with .gitignore, Vault/SSM/Secret Manager, CI/CD env vars, encrypted config)
- **Authentication patterns** — any team-wide auth patterns? (e.g., JWT with refresh tokens, session-based, OAuth2 flows, delegated to auth service)
- **Security review triggers** — when does a change get extra security scrutiny? (e.g., any auth changes, new API endpoints, dependency updates, never formally, all PRs)
- **OWASP/security awareness** — does the team reference OWASP Top 10 or similar? (e.g., active training, awareness but informal, not really)

See [references/interview-guide.md](references/interview-guide.md) for the full question bank.

Confirm section.

---

## Step 10: Definition of Done

Frame as: "What does 'done' mean on your team? This helps Claude understand when work is truly complete."

Ask about:
- **Code complete criteria** — what must be true before code is considered done? (e.g., tests pass, linting clean, types check, builds successfully)
- **Testing requirements** — what testing is required? (e.g., unit tests for new logic, integration tests for new endpoints, E2E for user-facing changes, coverage threshold met)
- **Documentation updates** — what docs must be updated? (e.g., README if behavior changes, API docs if endpoints change, changelog entry, ADR for architectural decisions, none required)
- **Review requirements** — what review is needed? (e.g., 1 approval, 2 approvals, specific reviewer for certain areas, CODEOWNERS)
- **Security check** — is a security scan part of done? (e.g., CI security scan passes, manual review for auth changes, Claude Code's built-in scanner, no formal requirement)
- **Deployment readiness** — any deployment-related requirements? (e.g., feature flag wrapped, backwards compatible, migration tested, monitoring/alerts configured)

See [references/interview-guide.md](references/interview-guide.md) for the full question bank.

Confirm section.

---

## Step 11: Preferred Libraries

Only ask about cross-cutting concerns relevant to the team's stack. See [references/interview-guide.md](references/interview-guide.md) for the full question bank.

Confirm section.

---

## Step 12: Review & Store

### Generate the Document

Compile all answers into a structured markdown document:

```markdown
# Team Conventions: {Team Name}

Last updated: {YYYY-MM-DD}
Domain: {primary domains, comma-separated}

## Tech Stack

### {Project Type}
- Language: {answer}
- Framework: {answer}
...

## Coding Standards
- Formatter: {answer}
- Linter: {answer}
...

## Code Quality & Refactoring
- File size guidance: {answer}
- Function length: {answer}
- DRY threshold: {answer}
- Dead code policy: {answer}
- Refactoring triggers: {answer}
- Complexity awareness: {answer}

## Testing
- Framework: {answer per stack}
- Coverage: {answer}
...

## Documentation Standards
- README expectations: {answer}
- API documentation: {answer}
- ADRs: {answer}
- Changelog: {answer}
- Code comments: {answer}
- Runbooks: {answer}

## Git & Workflow
- Branching: {answer}
- Branch naming: {answer}
...

## Architecture
- Pattern: {answer}
...

## Security Practices
- Dependency scanning: {answer}
- Input validation: {answer}
- Secrets management: {answer}
- Auth patterns: {answer}
- Security review triggers: {answer}
- Security awareness: {answer}

## Definition of Done
- Code complete: {answer}
- Testing: {answer}
- Documentation: {answer}
- Review: {answer}
- Security: {answer}
- Deployment readiness: {answer}

## Preferred Libraries
- {concern}: {library}
...
```

### Present for Review

Show the full document to the user:
> "Here are your compiled team conventions. Please review:"
> [Full document]
>
> 1. Looks good — save it
> 2. Edit a section
> 3. Cancel

If "Edit" → ask which section, re-run that interview section, regenerate.

### Store

Route to the configured doc backend:

**RAG Memory:**
1. `list_collections()` — show available collections
2. Ask user which collection to store in, or suggest creating a new one:
   > "Where should I store your team conventions? Here are your existing collections:"
   > [list collections]
   > "Or I can create a new collection. What should it be called?"
3. If creating new → `create_collection(name=user_chosen_name, domain="team conventions", description="Team-wide coding conventions, tech stack decisions, and workflow standards")` — let user confirm name and description
4. Ingest: `ingest_text(content=document, collection_name=chosen_collection, document_title="Team Conventions: {Team Name}", actor_type="Claude Code")`

**Confluence:**
1. Ask which space to store in (or use `default_space` from config)
2. Ask for page title (suggest "Team Conventions: {Team Name}" but let user override)
3. Create page: `createConfluencePage(spaceKey=space, title=chosen_title, body=document)`

**Google Drive:**
1. Ask where to store (suggest `default_folder_id` from config if available, or let user specify)
2. Write document to temp file: `/tmp/team-conventions.md`
3. Upload: `upload_file(file_path="/tmp/team-conventions.md", name="Team Conventions - {Team Name}.md", folder_id=chosen_folder)`

### Confirm

> "Team conventions saved to {backend}. Any developer can now use `/devflow:foundation:generate-claude-md` in their repos to generate a convention layer based on these team standards."

---

## ⛔ STOP

Skill complete. Suggest next steps:

> **Next steps:**
> - Run `/devflow:foundation:generate-claude-md` in any repo to generate CLAUDE.md + `.claude/rules/` files from these conventions
> - Re-run this skill anytime to update conventions
