# DevFlow Plugin — Complete Summary

Authoritative reference for what the DevFlow plugin does, what each skill enforces, how they chain together, and what is and isn't dictated by the plugin framework.

---

## The Workflow Chain

```
fetch-issue → plan-issue → implement-issue → security-review → complete-issue → post-merge
```

Every build workflow skill is designed to hand off to the next. The user controls progression at every decision point.

---

## Skills — What Each One Does and Enforces

### 1. fetch-issue

**Purpose:** Fetch an issue from Jira/GitLab/GitHub and analyze whether the work is already done.

**Enforces:**
- Nothing. It's read-only. Fetches the issue, searches the codebase, and reports feasibility (not implemented / partially done / fully done / conflicts).

**Outputs:** Issue summary, feasibility assessment.

**Hands off to:** `plan-issue` (with optional `--tdd` flag)

---

### 2. plan-issue

**Purpose:** Analyze the codebase and create a detailed implementation plan for user approval.

**Enforces:**
- **Context7 research** — must research libraries/frameworks mentioned in the issue using Context7 MCP (current docs, not stale training data)
- **Plan structure** — plan must include: issue summary, acceptance criteria, codebase analysis, implementation plan, testing strategy, Context7 research, **documentation updates**, commit strategy, incremental implementation schedule
- **Documentation updates section** — plan must identify "Files to update: README, docs/, .reference/, code comments"
- **Commit strategy** — each commit must reference the issue key
- **Pause points** — plan defines mandatory pause points (one per commit)
- **TDD workflow** — if `--tdd` flag: plan includes RED/GREEN/REFACTOR cycle with test cases from acceptance criteria
- **User approval gate** — plan cannot proceed to implementation without explicit user approval

**Outputs:** Approved plan saved to `.devflow/plans/[ISSUE-KEY].md`

**Hands off to:** `implement-issue` (with optional `--auto` flag)

---

### 3. implement-issue

**Purpose:** Execute the approved plan — create branch, write code, run tests, commit incrementally.

**Enforces:**
- **Branch naming** — `feature/[ISSUE-KEY]-[slug]`, `bugfix/[ISSUE-KEY]-[slug]`, or `task/[ISSUE-KEY]-[slug]` based on issue type
- **Issue status transition** — moves issue to "In Progress"
- **Test pattern compliance (MANDATORY):**
  - Discover existing test files in the repository
  - Study their structure, naming, organization, assertions
  - Follow those patterns EXACTLY
  - Do NOT create tests in a different style
- **Code pattern compliance (MANDATORY):**
  - Follow import patterns from existing code
  - Follow error handling conventions
  - Follow logging patterns
  - Follow module structure and organization
  - Maintain modular design
- **Documentation updates (MANDATORY — every commit):**
  - Search repository for all documentation files
  - Identify documentation affected by changes
  - Update ALL relevant documentation
  - Update code comments and docstrings
- **Commit format** — commits must reference issue key
- **Pause after every commit** — generate unit summary, stop, wait for user approval (unless `--auto`)
- **TDD cycle** — if TDD mode: RED (write failing tests) → GREEN (implement to pass) → REFACTOR → validate existing tests not broken

**Does NOT enforce:**
- What test framework to use (discovers from repo)
- What coverage target to hit (not specified)
- What documentation standard to follow (just says "update all relevant")
- Coding standards like formatter/linter (follows existing patterns)

**Outputs:** Committed code on feature branch, unit summaries.

**Hands off to:** `security-review` (recommended) or `complete-issue`

---

### 4. security-review

**Purpose:** OWASP Top 10 security analysis of branch changes, full repo, or specific files.

**Enforces:**
- **Security scanning** — comprehensive analysis following OWASP Top 10
- **Triage workflow** — every finding must be triaged: fix, dismiss (with reason), create ticket, manual, or skip
- **Dismissed issues tracked** — stored in `.devflow/security/[ISSUE-KEY]-dismissed.json`, filtered from future runs
- **Security fix commits** — if fixes applied, committed with issue reference
- **Warning gate** — warns if CRITICAL or HIGH severity issues remain unaddressed before proceeding

**Does NOT enforce:**
- WHEN to run security review (recommended, not mandatory — can be skipped for low-risk changes)
- What specific security practices the team follows (just scans for vulnerabilities)

**Outputs:** Security assessment, triage summary, optional security fix commit.

**Hands off to:** `complete-issue`

---

### 5. complete-issue

**Purpose:** Final validation, create PR/MR, and close the issue.

**Enforces:**
- **Final full test suite run** — adapts to work type:
  - Code with tests: full test suite with coverage if available
  - Bug fixes: affected test suite + regression test
  - Infrastructure: build/workflow validation
  - Documentation: accuracy, code examples, links
- **Coverage reporting** — reports coverage summary if coverage tools available
- **Validation gate** — must pass before proceeding (STOP if fails)
- **PR/MR creation** — via build-ops, includes issue reference, changes summary, validation results
- **Issue status transition** — moves issue to "Done" / closes it

**Does NOT enforce:**
- Coverage threshold (reports coverage but doesn't fail on a target)
- PR review count or reviewers (creates PR, review process is external)
- Merge strategy (PR is created, merge is manual)

**Outputs:** PR/MR URL, issue status updated.

**Hands off to:** `post-merge` (after PR/MR is merged)

---

### 6. post-merge

**Purpose:** Clean up after PR/MR merge — sync main, delete feature branch.

**Enforces:**
- Switch to main branch
- Pull latest changes
- Delete local feature branch
- Ask about remote branch cleanup

**Optional:** Update dependencies, run tests.

**Outputs:** Clean workspace ready for next issue.

---

### 7. create-issue

**Purpose:** Create detailed issues with codebase analysis and Context7 research.

**Enforces:**
- **Issue structure per type:**
  - Feature: Background, Acceptance Criteria (outcomes not implementation), Technical Guidance, Testing Requirements
  - Bug: Problem Statement, Steps to Reproduce, Root Cause, Investigation Areas
  - Documentation: What needs documenting, Current state, Desired outcome
  - Chore: Maintenance need, Current problem, Impact, Scope
  - Research: Questions, Deliverables, Success criteria, Time box
  - Technical Debt: Problem, Impact, Desired outcome, Benefit
- **Jira type mapping** — Feature → "Executable Spec", Bug → "Bug", Others → "Task"
- **User approval gate** — must approve before creation

---

### 8. workflow-guide

**Purpose:** Overview of the entire DevFlow workflow. No enforcement — just documentation.

**Key statements in the guide:**
- "Documentation updates are mandatory, not optional"
- "Test pattern compliance is enforced, not suggested"
- "Git branch naming adapts to issue type (feature/bugfix/task)"

---

### 9. build-ops (internal, not user-invocable)

**Purpose:** Backend operations dispatcher. Handles config loading, parameter validation, and routing to correct backend adapters.

**Enforces:**
- Config must exist (run `/devflow-setup` first)
- Parameter validation gate — every MCP parameter must have a verified source
- Backend isolation — identifiers never cross backend boundaries (Jira IDs stay in Jira, GitLab IDs stay in GitLab)

---

## What the Plugin Framework Dictates (Non-Negotiable)

These are the opinionated decisions the plugin makes. A team adopting DevFlow accepts these:

| Decision | Where Enforced | What It Says |
|----------|---------------|--------------|
| **Branch naming** | implement-issue Step 1 | `feature/`, `bugfix/`, `task/` + issue key + slug |
| **Commit format** | implement-issue, plan-issue | Must reference issue key |
| **PR/MR creation workflow** | complete-issue Step 4 | Created via build-ops with issue reference |
| **Test pattern compliance** | implement-issue Critical Requirements | Discover and follow existing test patterns EXACTLY |
| **Code pattern compliance** | implement-issue Critical Requirements | Follow existing import, error handling, logging, module patterns |
| **Documentation updates** | implement-issue Critical Requirements | MANDATORY — search for and update ALL affected docs, comments, docstrings |
| **Incremental commits with pause points** | implement-issue | Each commit = one pause for user review |
| **Final validation before PR/MR** | complete-issue Step 1 | Full test suite must pass |
| **Issue status transitions** | implement-issue Step 2, complete-issue Step 5 | In Progress → Done |
| **SDLC flow** | All build skills | fetch → plan → implement → (security review) → complete → post-merge |
| **OWASP-based security scanning** | security-review | Scans against OWASP Top 10 |
| **Issue structure standards** | create-issue | Outcomes not implementation, type-specific templates |

---

## What the Plugin Does NOT Dictate (Team Decisions)

The plugin enforces ACTIVITIES (you must update docs, you must follow test patterns, you must run tests) but does NOT define STANDARDS for those activities. These are team decisions:

| Decision Area | Plugin Says | Team Decides |
|---------------|-------------|--------------|
| **Testing framework** | "Discover and follow existing patterns" | Which framework, what philosophy (TDD, test-after, test-critical-paths) |
| **Coverage target** | "Report coverage if available" | What percentage is required, what's the coverage philosophy |
| **Documentation standard** | "Update ALL relevant documentation" | What docs are expected (README, API docs, ADRs, changelog, etc.), what level of detail |
| **Coding standards** | "Follow existing code patterns" | Formatter, linter, type strictness, naming conventions, error handling philosophy |
| **Code quality** | Nothing explicit | File size guidance, function length, DRY threshold, refactoring triggers, complexity metrics |
| **Security practices** | "Scan against OWASP Top 10" | Dependency scanning tools, input validation approach, secrets management, auth patterns |
| **Definition of done** | "Tests pass, docs updated, PR created" | Coverage threshold, review count, accessibility, performance, deployment readiness |
| **Architecture** | Nothing explicit | Patterns, error handling strategy, logging approach, env management, dependency policy |
| **Preferred tech stack** | Nothing explicit | Languages, frameworks, libraries for new projects |
| **CI requirements** | Nothing explicit | What checks must pass, merge strategy, release process |
| **Security review timing** | "Recommended before PR" | Whether it's mandatory or optional for the team |

**The key insight:** The plugin says "DO the activity." The team conventions say "HERE'S OUR BAR for that activity." They complement each other — conventions fill in the standards that the plugin's enforcement points reference.

---

## Non-Build Skills

| Skill | Purpose | User-Invocable |
|-------|---------|----------------|
| **devflow-setup** | Configure backends (Jira/GitLab/GitHub, Confluence/Google Drive/RAG Memory, GitHub/GitLab) | Yes |
| **plugin-overview** | DevFlow plugin overview — discover all skills, agents, hooks, and commands with entry points | Yes |
| **knowledge-management** | Route content to RAG Memory or docs backend for storage | Yes |
| **repo-explorer** | Explore and analyze GitHub repositories | Yes |
| **capture-conventions** | Guided interview to capture team conventions | Yes |
| **audit-conventions** | Read-only audit comparing repo state against team conventions — shows deltas, no enforcement | Yes |
| **generate-claude-md** | Help create/update CLAUDE.md + .claude/rules/ based on what's actually in the repo | Yes |
| **build-ops** | Backend operations dispatcher (used internally by build skills) | No |
| **skill-creator** | Create new skills | Yes |
| **frontend-design** | Frontend design assistance | Yes |
| **pm/roadmap** | Product roadmap management | Yes |
| **pm/backlog** | Backlog management | Yes |
| **docs/documentation-audit** | Audit documentation quality | Yes |
| **docs/reference-audit** | Audit reference documentation | Yes |
| **devops/sync-claude-knowledge** | Sync Claude knowledge | Yes |
| **rag-memory/setup-collections** | Scaffold RAG Memory collections | Yes |
| **rag-memory/create-agent-preferences** | Create agent preferences collection | Yes |

---

## How Conventions Fit

Three skills handle the convention layer, each with a distinct responsibility:

1. **capture-conventions** — Captures team standards via guided interview. Stores them in the doc backend. That's all it does. The result is a reference document — not enforceable, not a gold standard, just what the team would like.

2. **audit-conventions** — Read-only comparison of any repo against team conventions. Shows deltas as a report: "team says X, repo does Y." No file changes, no enforcement, no suggestions. Just facts.

3. **generate-claude-md** — Helps write CLAUDE.md + `.claude/rules/` based on what's actually in the repo and Claude Code best practices. Documents what IS, not what should be. Has nothing to do with team conventions — purely repo analysis.

### How conventions reach the repo

Team conventions captured by `capture-conventions` fill the "Team Decides" column above. If a developer chooses to place relevant conventions in their repo's `.claude/rules/` files, Claude reads them during every workflow step. The plugin's enforcement points ("update all docs", "follow test patterns", "run tests") then execute against the team's standards ("docs means README + API docs + changelog", "coverage must hit 80%", "use factories for test data").

**Without conventions in `.claude/rules/`:** The plugin still enforces its activities, but Claude uses its own judgment for the standards — no team-specific bar.

**With conventions in `.claude/rules/`:** Claude applies the team's specific standards during every enforced activity — documentation updates follow the team's expectations, tests follow the team's philosophy and coverage targets, code follows the team's coding standards.

**Audit as the bridge:** `audit-conventions` shows a developer exactly where their repo aligns with or deviates from team conventions. What the developer does with that information is their decision.
