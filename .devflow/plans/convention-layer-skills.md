# Convention Layer Skills — Design Reference

Design specs for two skills that support the convention layer architecture described in the AI-Native Philosophy Framework (`ai-native-philosophy.md`).

---

## Skill A: Capture Team Conventions

**Command**: `/devflow:foundation:capture-conventions`

**Purpose**: Guided interview to capture team-wide conventions, then store the result in the team's configured documentation backend (Confluence, Google Drive, or RAG Memory).

**Pattern**: Same progressive disclosure + guided interview pattern as `/devflow-setup`. Same doc backend routing as `/knowledge-management`.

### Interview Flow

The interview uses progressive disclosure — ask only what's relevant based on prior answers. Each section ends with a human confirmation gate before proceeding.

#### 1. Team Identity

- Team/org name
- Primary domain(s): web app, mobile, data/ML, DevOps, platform/infra, other
- Number of active repos (rough sense of scale)

#### 2. Tech Stack by Project Type

Only ask about project types the team actually uses (based on domain answer above).

**Frontend:**
- Language (TypeScript, JavaScript, other)
- Framework (React, Vue, Angular, Svelte, Next.js, other)
- Component library (Radix, shadcn/ui, Material UI, custom, none)
- State management (React Context, Zustand, Redux, Jotai, other)
- CSS approach (Tailwind, CSS Modules, styled-components, Sass, other)

**Backend:**
- Language (TypeScript/Node, Python, Go, Rust, Java/Kotlin, other)
- Framework (Express, Fastify, FastAPI, Django, Spring, Gin, other)
- Database (PostgreSQL, MySQL, MongoDB, DynamoDB, other)
- ORM/query layer (Prisma, Drizzle, SQLAlchemy, GORM, other)
- API style (REST, GraphQL, gRPC, tRPC, other)

**Data/ML:**
- Language (Python, R, Scala, other)
- Frameworks (PyTorch, TensorFlow, scikit-learn, Spark, other)
- Notebook vs scripts preference
- Data storage (S3, GCS, BigQuery, Snowflake, other)

**Mobile:**
- Approach (React Native, Flutter, SwiftUI, Kotlin/Compose, native, other)
- Shared code strategy (shared core library, fully shared, fully native)

#### 3. Coding Standards

- Style guide (team custom, language default, Airbnb, Google, other)
- Formatter (Prettier, Black, gofmt, rustfmt, other + config highlights)
- Linter (ESLint, Ruff, golangci-lint, Clippy, other + strictness level)
- Type strictness (strict mode, gradual, optional)
- Naming conventions (any deviations from language defaults)
- Import organization (auto-sorted, manual grouping rules)
- Error handling philosophy (Result types, exceptions, error codes)

#### 4. Testing Conventions

- Framework per stack (Jest, Vitest, pytest, Go testing, other)
- Coverage requirements (percentage threshold, or "aim for critical paths")
- Testing philosophy (TDD, test-after, test-critical-paths-only)
- Unit vs integration vs E2E balance
- Test file location (colocated, separate `__tests__/` directory, `tests/` root)
- Mocking approach (minimal mocks, mock external only, mock liberally)

#### 5. Git & Workflow

- Branching strategy (trunk-based, GitFlow, GitHub Flow, other)
- Branch naming (e.g., `feature/JIRA-123-description`, `feat/description`)
- Commit message format (Conventional Commits, freeform, other)
- PR/MR requirements (reviewers, CI passing, squash vs merge, template)
- Release process (tags, release branches, automated, manual)

#### 6. Architecture Preferences

- Monorepo vs polyrepo
- Preferred patterns (clean architecture, hexagonal, MVC, microservices, serverless)
- Error handling (global handler, per-layer, error boundaries)
- Logging (structured JSON, levels, library preference)
- Environment management (dotenv, Vault, AWS SSM, other)
- Dependency management philosophy (pin exact, allow ranges, auto-update)

#### 7. Preferred Libraries

Common cross-cutting concerns per stack. Only ask if relevant:
- HTTP client (axios, fetch, httpx, reqwest)
- Validation (Zod, Joi, Pydantic, other)
- Authentication (NextAuth, Passport, custom JWT, OAuth library)
- Date/time (date-fns, Day.js, Luxon, native)
- Logging (Winston, Pino, structlog, slog)
- Observability (OpenTelemetry, Datadog, custom)

### Output Format

The output is a structured, human-readable document with clear section headings. It should be easy to scan and easy to retrieve programmatically.

```markdown
# Team Conventions: {Team Name}

Last updated: {date}
Domain: {primary domains}

## Tech Stack

### Frontend
- Language: TypeScript (strict mode)
- Framework: React 18 + Next.js 14 (App Router)
- Components: Radix UI + Tailwind CSS
...

### Backend
- Language: TypeScript (Node.js)
- Framework: Fastify
...

## Coding Standards
- Formatter: Prettier (default config + trailing commas)
- Linter: ESLint (strict preset, no warnings allowed)
...

## Testing
- Framework: Vitest (frontend), Jest (backend)
- Coverage: 80% minimum for new code
...

## Git Workflow
- Branching: trunk-based development
- Branch naming: feat/JIRA-123-short-description
...

## Architecture
- Pattern: Clean architecture with hexagonal ports/adapters
...

## Preferred Libraries
- HTTP: axios (frontend), fetch (backend)
- Validation: Zod
...
```

### Storage

Route to configured doc backend using the same pattern as `/knowledge-management`:
- **Confluence** → create/update page in configured space
- **Google Drive** → create/update document in configured folder
- **RAG Memory** → ingest into team conventions collection

### Re-run Behavior

If conventions already exist in the doc backend:
1. Load the existing document
2. Present current values: "Here are your current team conventions."
3. Ask which sections to update (or all)
4. Run interview for selected sections only
5. Merge updates into existing document
6. Save back to doc backend

---

## Skill B: Generate / Maintain Repo Convention Layer

**Command**: `/devflow:foundation:generate-claude-md`

**Purpose**: Analyze a repo, optionally retrieve team conventions, reconcile deviations with developer input, and generate or update the repo's convention layer.

### Core Design Principles

- **Team conventions are optional.** The skill works without them — it's still valuable for repo analysis alone.
- **Developer has override authority.** Conventions are defaults, not mandates. Every deviation is a valid choice.
- **Deviation detection is core.** For existing repos, compare actual state against team conventions and surface every deviation.
- **Complete resolution.** Every deviation presented and resolved — nothing silently ignored.
- **Standalone output.** All generated files work for any Claude Code user, no plugin required.

### Output Structure

```
repo/
├── CLAUDE.md                        # Lean: project overview, build/test commands, key dirs (~60 lines)
└── .claude/
    └── rules/
        ├── coding-standards.md      # Resolved coding conventions
        ├── testing.md               # Testing framework, approach, coverage
        ├── git-workflow.md          # Branching, commits, PR/MR process
        └── architecture.md          # Patterns, key decisions, constraints
```

#### Root CLAUDE.md Template (~60 lines)

```markdown
# {Project Name}

{One-line description}

## Build & Run

{build commands, dev server, common scripts}

## Test

{test commands, how to run specific tests}

## Key Directories

{directory layout with brief descriptions}

## Important Notes

{critical gotchas, environment quirks, things Claude can't infer from code}
```

Keep it lean. Everything else goes in `.claude/rules/`.

#### Rules File Format

Each rules file follows this pattern:

```markdown
---
# Optional: path scoping for monorepo rules
paths:
  - "src/frontend/**"
---

# {Topic} Rules

{Clear, concise rules. Each rule is a directive Claude can follow.}

## {Subsection}

- Rule 1: Do X when Y
- Rule 2: Always use Z for this concern
- Rule 3: Never do W because of [reason]
```

Path-scoped rules are used when different parts of a monorepo have different conventions (e.g., frontend uses Prettier, backend uses Black).

### Mode Detection

The skill auto-detects which mode to use:

| Condition | Mode |
|-----------|------|
| CLAUDE.md exists AND `.claude/rules/` exists | **Maintenance** |
| CLAUDE.md exists but no `.claude/rules/` | **Existing repo** (migrate to modular rules) |
| No CLAUDE.md, substantial code present | **Existing repo** |
| No CLAUDE.md, minimal/no code | **Greenfield** |

### Mode 1: Existing Repo, No Convention Layer

#### Step 1 — Gather Inputs

**Retrieve team conventions (optional):**
1. Check for configured doc backend
2. If available → attempt to retrieve team conventions document
3. If not available (no backend configured, no document found, network issue) → proceed without. Inform developer: "No team conventions found. I'll generate from repo analysis alone."

**Analyze repo:**
- **Package files** (package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml) → detect stack, dependencies, scripts
- **Config files** (.eslintrc, tsconfig, prettier, .editorconfig, ruff.toml) → detect existing conventions
- **CI/CD config** (.github/workflows, .gitlab-ci.yml, Jenkinsfile) → extract build/test commands
- **Directory structure** → document architecture, identify monorepo boundaries
- **README** → extract project context, purpose, setup instructions
- **Existing AI config** (.cursorrules, .github/copilot-instructions.md) → migrate relevant content
- **Git history** → infer branching strategy, commit message patterns

#### Step 2 — Reconciliation (if team conventions exist)

Compare repo analysis against team conventions. Present a deviation report:

**Aligned** (no action needed):
> "Repo uses React + TypeScript — matches team convention"

**Deviation detected** (developer decides):
> "Repo uses Tailwind CSS, but team convention specifies styled-components"
> Options: [Keep repo choice] [Align with convention] [Customize]

**Not covered** (captured as-is):
> "Repo uses GraphQL — team conventions don't specify API style"
> → Captured in rules as the repo's convention

**Missing from repo** (developer decides):
> "Team convention requires 80% test coverage, but no coverage config found in repo"
> Options: [Add to rules] [Skip for now] [Customize threshold]

Developer resolves each deviation:
- **Keep deviation** → rules reflect the repo's actual choice with a note about the team convention
- **Align with convention** → rules reflect the team convention
- **Customize** → developer specifies the actual rule with context

#### Step 3 — Generate

1. Generate lean CLAUDE.md from repo analysis (project overview, build/test commands, key directories)
2. Generate `.claude/rules/` files from resolved decisions (one per topic)
3. Present all files to developer for review (show full content)
4. Developer approves → write files
5. Suggest committing: `git add CLAUDE.md .claude/rules/ && git commit -m "feat: Add convention layer (CLAUDE.md + rules)"`

**Without team conventions**: Skip Step 2 entirely. Generate from repo analysis + developer input on any ambiguous conventions.

### Mode 2: Greenfield Repo (No/Minimal Code)

1. **Retrieve team conventions** (optional, same as Mode 1)
2. **Ask project type**: "What type of project is this?" — if conventions exist, map to known team stacks
3. **Ask for project brief**: "Do you have a PRD or project brief?" — if yes, analyze for architectural context
4. **If conventions exist** → present applicable conventions for this project type, developer accepts/overrides/customizes each
5. **If no conventions** → guided interview covering stack, standards, testing, git workflow (lighter than capture-conventions — just what's needed for this repo)
6. **Generate** lean CLAUDE.md + `.claude/rules/` files from resolved decisions
7. Add `<!-- TODO: update after initial implementation -->` markers in rules files for details that will emerge as the project develops
8. Developer reviews → approves → commits

### Mode 3: Maintenance (Convention Layer Already Exists)

1. **Retrieve team conventions** (optional, same as Mode 1)
2. **Read existing** CLAUDE.md + `.claude/rules/` files
3. **Analyze current repo state** (same analysis as Mode 1)
4. **Present drift report**:

**Convention drift** (team conventions changed since last sync):
> "Team convention now requires Vitest instead of Jest. Your rules specify Jest."
> Options: [Update to Vitest] [Keep Jest] [Customize]

**Repo drift** (new deps, dirs, architectural changes not reflected in rules):
> "New `packages/mobile/` directory detected — no rules file covers it."
> "New dependency `@tanstack/query` added — not mentioned in architecture rules."

**Stale content** (rules reference things that no longer exist):
> "Rules reference `src/legacy/` directory which no longer exists."
> "Rules mention Express.js but the project migrated to Fastify."

5. Developer resolves each item
6. Update affected files → developer approves → commit

### Reconciliation Principles

1. **Every deviation is surfaced.** The developer sees every difference between team conventions, current rules, and repo state.
2. **Nothing is silently changed.** The skill proposes, the developer disposes.
3. **Context is preserved.** When a developer keeps a deviation, the rules file can include a comment explaining why (e.g., `# Deviates from team convention (styled-components) — migrating incrementally`).
4. **Batch resolution is available.** For large deviation lists: "Accept all team conventions for uncontested items?" with opt-out for specific ones.
5. **Provenance is tracked.** Rules files include a footer comment: `<!-- Generated by devflow:foundation:generate-claude-md | Last synced: {date} -->` to support maintenance mode drift detection.

### Interaction with Existing Tools

- **Builds on `/init`**: Claude Code's built-in `/init` analyzes a repo and generates a starter CLAUDE.md. This skill goes further: convention-awareness, reconciliation, modular rules generation.
- **Uses doc backend**: Same backend configured via `/devflow-setup` for retrieving team conventions.
- **Standalone output**: Generated files don't reference the plugin, DevFlow, or any external dependency. They work for anyone using Claude Code.

---

## How Both Skills Work Together

### Initial Setup (One-Time)

```
Team Lead                           Each Developer
─────────                           ──────────────
1. /devflow:foundation:setup        3. /devflow:foundation:generate-claude-md
   → configure backends                → analyzes their repo
                                        → retrieves team conventions
2. /devflow:foundation:              → reconciles deviations
   capture-conventions                  → generates CLAUDE.md + rules
   → guided interview                  → commits convention layer
   → conventions stored in
     doc backend
```

### Ongoing Maintenance

```
Team conventions change              Developer runs generate-claude-md
(re-run capture-conventions           in maintenance mode
 or edit doc directly)                → detects convention drift
         │                            → detects repo drift
         │                            → developer resolves
         └────────────────────────────→ rules files update
                                      → commits changes

Auto-memory accumulates              Periodic team review
repo-specific learnings              of conventions doc and
(Claude's own notes,                 repo convention layers
 separate from CLAUDE.md)            (weekly or monthly)
```

### Without Team Conventions

Both skills work independently:

- **capture-conventions** is only relevant for teams wanting centralized conventions
- **generate-claude-md** works standalone — analyzes repo, asks developer about ambiguous conventions, generates convention layer. No team conventions required.

This means a solo developer or a team without centralized conventions can still benefit from structured CLAUDE.md + `.claude/rules/` generation.

---

## Implementation Notes

### Dependencies

- Doc backend configuration (from `/devflow-setup`) — optional, only needed for team conventions
- Repo analysis capabilities — file reading, package file parsing, config detection
- No new MCP tools required — uses existing file system access and doc backend tools

### Skill File Structure

```
skills/
└── foundation/
    ├── capture-conventions/
    │   ├── SKILL.md              # Skill definition + interview flow
    │   └── references/
    │       └── interview-guide.md  # Section templates, question bank
    └── generate-claude-md/
        ├── SKILL.md              # Skill definition + mode logic
        └── references/
            ├── analysis-guide.md   # What to analyze in a repo
            ├── reconciliation.md   # How to present and resolve deviations
            └── templates/
                ├── claude-md.md    # Root CLAUDE.md template
                ├── coding-standards.md  # Rules file template
                ├── testing.md           # Rules file template
                ├── git-workflow.md      # Rules file template
                └── architecture.md      # Rules file template
```

### Key Design Decisions

1. **Rules files, not monolithic CLAUDE.md.** Official Claude Code guidance says CLAUDE.md should be short (~60 lines). `.claude/rules/` is the official modular system.

2. **Team conventions in doc backend, not a repo.** Conventions span all repos. Storing in the doc backend (Confluence/Google Drive/RAG Memory) keeps them accessible from any repo via the same configured backend.

3. **Deviation detection, not enforcement.** The skill surfaces differences. The developer decides. This respects that repos may have legitimate reasons to differ from team conventions.

4. **Standalone output.** Generated files reference no plugin, no skill, no external system. Any Claude Code user can benefit from the convention layer.

5. **Three modes auto-detected.** The developer doesn't need to know which mode applies — the skill figures it out from repo state.
