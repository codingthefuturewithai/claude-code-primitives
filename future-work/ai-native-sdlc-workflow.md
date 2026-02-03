# AI-Native SDLC Workflow Design

> **Purpose:** This document captures the design for a comprehensive AI-native Software Development Lifecycle (SDLC) workflow. It extends the existing DevFlow commands to cover the complete lifecycle from ideation to deployment.

> **Status:** Design phase - brainstorming and requirements capture

---

## Table of Contents

1. [Philosophy & Principles](#philosophy--principles)
2. [Current State: What DevFlow Already Covers](#current-state-what-devflow-already-covers)
3. [Universal SDLC Phases](#universal-sdlc-phases)
4. [QA/QC Philosophy: Built-In Quality](#qaqc-philosophy-built-in-quality)
5. [Knowledge Management Integration](#knowledge-management-integration)
6. [Bug Workflow](#bug-workflow)
7. [Detailed Phase Specifications](#detailed-phase-specifications)
8. [Preferences & Conventions System](#preferences--conventions-system)
9. [Implementation Priorities](#implementation-priorities)

---

## Philosophy & Principles

### Core Design Principles

1. **AI-First, Human-Readable Second**
   - Issue structures (executable specs, bugs, tasks) are optimized for AI consumption
   - Humans can read them, but the primary audience is the AI assistant
   - Structured, consistent formats that AI can parse reliably

2. **Human-in-the-Loop at Decision Boundaries**
   - AI does the work, humans approve at critical gates
   - No auto-proceed past approval points
   - User controls workflow progression

3. **Incremental Planning, Not Upfront Breakdown**
   - Don't create all issues/tasks upfront
   - Start with scaffolding iteration only
   - Create next batch of issues after completing each iteration
   - Review progress vs requirements, then plan next increment

4. **Built-In Quality, Not Checkpoint Quality**
   - QA/QC is continuous throughout the workflow
   - Code review and security review are part of development, not separate phases
   - Quality gates are integrated, not bolted on after

5. **Universal Abstraction**
   - Workflows apply to ANY software project (CLI, web app, API, library, etc.)
   - Technology-agnostic at the core
   - Project-specific extensions are delegated to individual repositories

6. **Not Scrum-Specific**
   - No epics, no stories in the traditional sense
   - Issue types: Executable Specs, Bugs, Tasks
   - Iterations instead of sprints (flexible, not time-boxed methodology)
   - JIRA is for human visibility (PMs, team), not the source of truth for AI

### Template-Based Scaffolding

Scaffolding is not always AI-generated from scratch. Common pattern:
- Select a cookiecutter template (React+FastAPI+PostgreSQL, MCP server, etc.)
- Run one terminal command, project scaffolded in seconds
- Then start adding features on top of the foundation

Workflows must accommodate both:
- **Template path:** User provides template → run it → done
- **AI-generated path:** No template → AI helps generate structure based on architecture

---

## Current State: What DevFlow Already Covers

The existing DevFlow commands handle feature development well:

| Command | Purpose | Status |
|---------|---------|--------|
| `/devflow:fetch-issue` | Fetch JIRA issue, analyze feasibility | ✅ Exists |
| `/devflow:plan-work` | Create implementation plan with approval loop | ✅ Exists |
| `/devflow:implement-plan` | Execute plan with incremental pauses | ✅ Exists |
| `/devflow:security-review` | OWASP-based security analysis | ✅ Exists |
| `/devflow:complete-issue` | Final validation, create PR, update JIRA | ✅ Exists |
| `/devflow:post-merge` | Cleanup after PR merge | ✅ Exists |
| `/devflow:create-issue` | Create structured JIRA issue | ✅ Exists |

### Current DevFlow Strengths

- Structured issue format (executable specs)
- TDD option in planning
- Mandatory pause points during implementation
- Security review integrated
- Pattern compliance enforcement
- Human-in-the-loop at every phase

### Current DevFlow Gaps

- No ideation/PRD phase
- No architecture phase
- No scaffolding workflow
- No code review step (quality check before security review)
- No iteration planning (reviewing progress vs requirements)
- No release management
- No bug-specific workflow
- No preferences/conventions enforcement

---

## Universal SDLC Phases

### Phase Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI-NATIVE SDLC WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────────────────┐ │
│  │  IDEATE  │───▶│ ARCHITECT │───▶│ SCAFFOLD │───▶│       DEVELOP        │ │
│  └──────────┘    └───────────┘    └──────────┘    │  (existing DevFlow)  │ │
│                                                    │  + code review       │ │
│                                                    └──────────┬───────────┘ │
│                                                               │             │
│                                                               ▼             │
│                                        ┌──────────┐    ┌──────────┐        │
│                                        │  ITERATE │◀───│ RELEASE  │        │
│                                        └────┬─────┘    └──────────┘        │
│                                             │                               │
│                                             └───────▶ (back to DEVELOP)    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  BUG WORKFLOW (variant):  TRIAGE ───▶ FIX (uses DEVELOP with bug focus)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Phase Definitions

| Phase | Input | Output | New or Existing |
|-------|-------|--------|-----------------|
| **Ideate** | Problem/idea | PRD + concept mockups | NEW |
| **Architect** | PRD | Architecture doc + stack decisions | NEW |
| **Scaffold** | Architecture | Working repo + initial task list | NEW |
| **Develop** | Task/Issue | Working code + PR | ENHANCE (add code review) |
| **Iterate** | Completed iteration | Next batch of tasks | NEW |
| **Release** | Completed code | Published release | NEW |

---

## QA/QC Philosophy: Built-In Quality

### Traditional vs Built-In Approach

| Traditional QA/QC | Built-In Approach |
|-------------------|-------------------|
| Separate QA team reviews after development | AI code review during development workflow |
| Security scan before release | Security review before every PR |
| Manual testing phase | TDD - tests written with implementation |
| Test coverage reports at end | Coverage gates as part of complete-issue |
| Code review by humans only | AI first pass, then human review |
| Quality as a gate | Quality as a continuous process |

### How to Explain This to Traditional QA Folks

> "Quality is built into every step of the development workflow, not bolted on after. AI assists with:
>
> - **Plan review:** Validates approach before coding starts
> - **Implementation:** TDD ensures tests exist alongside code
> - **Code review:** AI reviews for quality, patterns, maintainability before human review
> - **Security review:** AI scans for OWASP vulnerabilities before PR
> - **Regression check:** Ensures existing tests still pass
>
> This is continuous quality, not checkpoint quality. Every PR has already been reviewed for code quality, security, test coverage, and pattern compliance before a human ever sees it."

### DevFlow Enhancement: Add Code Review

Current flow:
```
fetch → plan → implement → security-review → complete
```

Enhanced flow:
```
fetch → plan → implement → CODE-REVIEW → security-review → complete
```

**`/devflow:code-review` responsibilities:**
- Check against stored preferences (file length, patterns, conventions)
- Validate modular design (flag files over threshold, e.g., 500 lines)
- Verify test coverage for new code paths
- Check documentation completeness
- Identify complexity growth / refactoring opportunities
- Ensure pattern adherence (imports, error handling, logging)

---

## Knowledge Management Integration

### The Routing Problem

During any workflow, AI encounters decisions, preferences, and research worth capturing. The question: where does it go?

### Knowledge Routing Rules

| Knowledge Type | Destination | Examples |
|----------------|-------------|----------|
| Code-specific decisions | **Repository** | Inline comments, docstrings, code-level ADRs |
| Reusable knowledge | **RAG Memory** | Tech research, preferences, patterns, conventions |
| Human-viewable / cross-project | **Confluence** | Product roadmaps, cross-app views, PM tracking |

### What Lives in RAG Memory

- **Preferred technologies/stack** - Languages, frameworks, libraries
- **Coding conventions** - Max file length, naming patterns, import style
- **Architectural decisions** - "We chose FastAPI over Flask because..."
- **Technology research** - Library evaluations, Context7 findings
- **Quality rules** - Modular design principles, refactoring triggers
- **Tool preferences** - Testing frameworks, linters, formatters

### What Lives in Confluence

- **Product roadmaps** - Multi-project view
- **Release plans** - Cross-team visibility
- **High-level architecture** - Company-wide system views
- **PM tracking** - For humans managing across multiple solutions

### What Lives in Repository

- **README, CONTRIBUTING** - Project-specific docs
- **API documentation** - OpenAPI specs, endpoint docs
- **Code comments** - Implementation-specific context
- **Project-level ADRs** - Decisions specific to this codebase

### Integration with Workflows

The existing `knowledge-management` skill helps route knowledge to the right place. Workflows should invoke this skill when capturing:
- Architectural decisions
- Technology choices
- Convention agreements
- Research findings

---

## Bug Workflow

Bugs have a different entry point than features. They need:
1. Capture (from user report, logs, monitoring)
2. Analysis (reproduce, identify root cause area)
3. Triage (severity, priority, assignment)
4. Fix (root cause fix + regression test)
5. Verification (confirm fix, run regression suite)
6. Quality control (code review, security review)
7. PR creation
8. Issue closure

### Bug Workflow Commands

**`/bugflow:triage`**
1. Capture bug report (paste or describe)
2. AI analyzes: reproduction steps, likely root cause areas, severity assessment
3. Human confirms/adjusts severity and priority
4. Creates JIRA issue using structured bug format
5. Outputs: Bug issue ready for fixing

**`/bugflow:fix`** (or DevFlow adapts when issue type is Bug)
1. Fetch bug issue
2. Deep analysis for root cause (more investigation than feature work)
3. Plan fix + regression test
4. Implement fix
5. Verify fix resolves issue
6. Run full regression suite
7. Code review → Security review → Complete

The fix workflow can potentially reuse DevFlow commands with bug-specific behavior detected from issue type.

---

## Detailed Phase Specifications

### Phase 1: Ideate

**Command:** `/ideate`

**Purpose:** Transform a problem or idea into a structured PRD with concept mockups

**Workflow:**
1. Capture problem statement
   - What problem are we solving?
   - Who has this problem?
   - Why does it matter?

2. Define user needs/goals
   - Jobs-to-be-done style
   - What outcomes do users want?

3. Identify core features
   - What's in scope?
   - What's explicitly out of scope?
   - MVP boundary

4. Establish constraints
   - Technical constraints
   - Business constraints
   - Timeline constraints

5. Generate concept mockups
   - Lightweight wireframes to visualize UX intent
   - Not pixel-perfect designs, just enough to communicate the concept
   - Applies to any UI (web, mobile, CLI, terminal)

6. Compile PRD document
   - Structured for AI consumption
   - Human-readable

**Outputs:**
- PRD document (markdown)
- Concept mockups/wireframes

**Notes:**
- Mockups are conceptual, not final design
- For actual UI implementation, use `frontend-design` skill
- PRD focuses on WHAT and WHY, not HOW

---

### Phase 2: Architect

**Command:** `/architect`

**Purpose:** Transform PRD into architecture document and technology decisions

**Workflow:**
1. Review PRD constraints
   - Technical requirements
   - Scale requirements
   - Integration requirements

2. Stack selection
   - Check for preferred technologies (from RAG Memory)
   - If preferences exist, validate fit for this project
   - If no preferences, recommend and capture decision

3. System design
   - High-level component architecture
   - Data flow
   - Integration points

4. Key architectural decisions
   - Document as ADRs
   - Capture rationale
   - Store in RAG Memory for future reference

5. Compile architecture document
   - Component diagrams
   - Technology choices with rationale
   - Integration approach

**Outputs:**
- Architecture document (markdown)
- ADRs captured in RAG Memory

**Notes:**
- Architecture is high-level, not implementation detail
- Should be technology-aware but not code-specific
- Feeds into scaffolding phase

---

### Phase 3: Scaffold

**Command:** `/scaffold`

**Purpose:** Create working project foundation and initial task list

**Workflow:**
1. Check for template
   - "Do you have a template to use?" (cookiecutter, etc.)

   **If yes (template path):**
   - Get template identifier
   - Run template command
   - Project scaffolded in seconds

   **If no (AI-generated path):**
   - Generate project structure based on architecture
   - Create basic files, dependencies, CI/CD

2. Initialize repository
   - Git setup
   - Basic CI/CD pipeline
   - Development environment config

3. Generate initial task list
   - Based on PRD and architecture
   - Just enough for first iteration (scaffolding iteration)
   - NOT full breakdown of all work
   - Focus: get to a functional foundation

4. Review with user
   - Present task list
   - User approves or adjusts

5. Create issues (optional)
   - User can run `/devflow:create-issue` for each task
   - Or defer issue creation

**Outputs:**
- Working repository with foundation
- Initial task list (markdown or directly to JIRA)

**Notes:**
- Template path is preferred when available
- AI-generated scaffolding is fallback
- Task list is for first iteration only, not complete breakdown

---

### Phase 4: Develop (Enhanced DevFlow)

**Commands:** Existing DevFlow suite with code review addition

**Enhanced Flow:**
```
/devflow:fetch-issue
    ↓
/devflow:plan-work [--tdd]
    ↓
/devflow:implement-plan [--auto]
    ↓
/devflow:code-review        ← NEW
    ↓
/devflow:security-review
    ↓
/devflow:complete-issue
    ↓
/devflow:post-merge
```

**New Command: `/devflow:code-review`**

**Purpose:** Quality review against preferences and conventions

**Workflow:**
1. Load preferences from RAG Memory
   - Max file length threshold
   - Modular design rules
   - Pattern conventions
   - Naming conventions

2. Analyze implemented code
   - Compare against preferences
   - Check for violations

3. Check categories:
   - **File length:** Flag files over threshold (e.g., 500 lines)
   - **Modular design:** Identify extraction opportunities
   - **Pattern adherence:** Verify coding conventions followed
   - **Test coverage:** Identify untested new code paths
   - **Documentation:** Flag missing docs for public APIs
   - **Complexity:** Identify high-complexity functions

4. Present findings
   - List issues with specific recommendations
   - Group by severity (must-fix, should-fix, consider)

5. User resolution for each finding:
   - `"fix"` → AI applies recommended refactoring
   - `"skip"` → Accept as-is (with optional rationale)
   - `"defer"` → Create tech debt issue for later

**Outputs:**
- Code review report
- Applied fixes (if any)
- Tech debt issues (if any)

---

### Phase 5: Iterate

**Command:** `/iterate`

**Purpose:** Review progress vs requirements, plan next batch of work

**Workflow:**
1. Review completed work
   - What issues/tasks are done?
   - What's the current state of the solution?

2. Compare against PRD/requirements
   - What capabilities exist now?
   - What's still missing?

3. Identify next priorities
   - What should come next?
   - Dependencies and sequencing

4. Generate next task batch
   - Just enough for next iteration
   - NOT remaining full breakdown

5. Review with user
   - Present proposed tasks
   - User approves or adjusts

6. Create issues
   - Use `/devflow:create-issue` for each approved task

**Outputs:**
- Next iteration task list
- JIRA issues (via create-issue)

**Notes:**
- This is the incremental planning philosophy in action
- Never plan too far ahead
- Each iteration informs the next

---

### Phase 6: Release

**Command:** `/release`

**Purpose:** Package and publish a release

**Workflow:**
1. Determine version bump
   - Analyze commits since last release
   - Suggest semantic version (major/minor/patch)
   - User confirms

2. Generate changelog
   - From commits and merged PRs
   - Group by type (features, fixes, etc.)

3. Create release notes
   - Human-readable summary
   - Highlight key changes

4. Tag and publish
   - Create git tag
   - Create GitHub release
   - Attach artifacts if applicable

**Outputs:**
- Updated CHANGELOG.md
- Git tag
- GitHub release

---

## Preferences & Conventions System

### What Gets Captured

| Category | Examples |
|----------|----------|
| **Languages** | Python 3.11+, TypeScript 5.x |
| **Frameworks** | FastAPI, React, Next.js |
| **Libraries** | pytest (not unittest), pydantic, axios |
| **Code style** | Max 500 lines per file, snake_case for Python |
| **Patterns** | Repository pattern for data access, dependency injection |
| **Testing** | pytest with fixtures, 80% coverage minimum |
| **Documentation** | Docstrings for public APIs, README for each module |
| **Tools** | uv for Python deps, pnpm for Node |

### How Preferences Are Used

1. **During architecture:** Check preferred stack, validate fit
2. **During scaffolding:** Use preferred tools and patterns
3. **During implementation:** Follow coding conventions
4. **During code review:** Enforce preferences, flag violations
5. **When making decisions:** Reference past ADRs

### Storage Location

Preferences are stored in **RAG Memory** because:
- They're reusable across projects
- They need to be queryable by AI
- They evolve over time (can be updated)
- They're not specific to one codebase

### Capture Mechanism

When preferences are established or changed:
1. AI recognizes a preference decision
2. Invokes knowledge-management skill
3. Skill routes to RAG Memory
4. Preference is stored with context

---

## Implementation Priorities

### Phase 1: Enhance DevFlow (High Priority)

1. **Add `/devflow:code-review`**
   - Quality check between implement and security-review
   - Preferences enforcement
   - Refactoring suggestions

2. **Create preferences schema**
   - Define what preferences look like in RAG Memory
   - Bootstrap with initial conventions

### Phase 2: New Workflows (Medium Priority)

3. **`/ideate`**
   - Problem → PRD → Mockups

4. **`/architect`**
   - PRD → Architecture → Stack decisions

5. **`/scaffold`**
   - Template or AI-generated foundation
   - Initial task list

6. **`/iterate`**
   - Progress review → Next batch of tasks

### Phase 3: Bug & Release (Lower Priority)

7. **`/bugflow:triage`**
   - Bug capture and analysis

8. **`/bugflow:fix`** (or DevFlow adaptation)
   - Bug-specific development flow

9. **`/release`**
   - Version → Changelog → Publish

---

## Open Questions

1. **Preferences bootstrap:** How do we initially populate preferences for a new user? Interactive wizard? Import from existing projects?

2. **Cross-project preferences:** Some preferences are personal (apply to all my projects), some are project-specific. How do we handle this?

3. **Template registry:** Should we maintain a list of known templates (cookiecutter, etc.) that the scaffold command can suggest?

4. **Iteration triggers:** What signals that an iteration is "complete" and it's time to run `/iterate`?

5. **Release automation:** How much of the release process should be automated vs prompted?

---

## Appendix: Existing DevFlow Command Reference

For complete details on existing commands, see:
- `/commands/devflow/fetch-issue.md`
- `/commands/devflow/plan-work.md`
- `/commands/devflow/implement-plan.md`
- `/commands/devflow/security-review.md`
- `/commands/devflow/complete-issue.md`
- `/commands/devflow/post-merge.md`
- `/commands/devflow/create-issue.md`

For knowledge management integration, see:
- `/skills/knowledge-management/SKILL.md`
