# AI-Native Software Development: Philosophy Framework

A philosophy, guiding principles, and strategic framework for taking software development teams from ad-hoc AI usage to consistent, reliable, AI-native workflows.

---

## The Shift

Most teams using AI coding assistants are still in the "autocomplete on steroids" mindset. The developer writes code, occasionally asking the AI for help. The AI is a tool they reach for, like a search engine or Stack Overflow.

AI-native development inverts this. **The developer becomes the decision-maker. The AI becomes the executor.** The developer's job is no longer to write code — it's to:

1. **Define intent** — What are we building and why?
2. **Make decisions at gates** — Is this plan right? Is this approach sound? Is this secure?
3. **Provide verification criteria** — How do we know this works?
4. **Curate institutional knowledge** — What has this team learned?

Everything between those decision points is AI execution.

### Why This Matters

The Claude Code team's own data point is stark: Boris Cherny (the creator) says AI writes 100% of his code. His team runs 3-5 parallel agents via worktrees. They paste Slack bug reports and say "fix." They haven't written SQL in months.

But here's the part most people miss: **they're not being lazy — they're being precise.** The reason Claude can "just fix" bugs is that they've invested deeply in:
- Verification infrastructure (test suites, CI, linting)
- Institutional knowledge (CLAUDE.md, skills, notes directories)
- Workflow discipline (Plan mode for anything non-trivial)
- Context hygiene (subagents, /clear, worktree isolation)

**The teams that get the best results from AI aren't the ones prompting the hardest. They're the ones who've built the best infrastructure for AI to work within.**

### The Core Insight: Three Assets

In AI-native development, three assets compound over time:

1. **The Codebase** (obviously) — but now it's also Claude's primary context source
2. **The Convention Layer** (CLAUDE.md, skills, hooks, agents) — the team's institutional knowledge made executable
3. **The Verification Layer** (tests, CI, linting, security scans) — the feedback loops that let Claude self-correct

Traditional development invests mainly in #1. AI-native development invests equally in all three. **The convention layer and verification layer are what turn Claude from a coding assistant into a reliable team member.**

---

## Guiding Principles

### Principle 1: Explore, Plan, Implement, Verify

This is the fundamental loop. Every non-trivial task follows this pattern:

- **Explore**: Read code, ask questions, understand the landscape (Plan Mode, read-only)
- **Plan**: Create a detailed implementation plan, have it reviewed (by human and/or second Claude)
- **Implement**: Execute the plan incrementally, pausing for review after each logical unit
- **Verify**: Run tests, check output, compare behavior, validate against acceptance criteria

**Why this order matters**: Jumping to code produces code that solves the wrong problem. "A mediocre plan produces mediocre code, regardless of how capable the model is." The plan is the most important artifact.

**The two-Claude review pattern**: Claude A writes the plan. Claude B reviews it as a "staff engineer" looking for edge cases, bad assumptions, simpler alternatives, and performance issues. This mirrors what a strong engineering team does with design reviews.

### Principle 2: Human Decisions at Gates, AI Execution Between

The developer's judgment is concentrated at decision points:

| Gate | Developer's Decision |
|------|---------------------|
| **Issue selection** | What to work on, priority |
| **Feasibility** | Is this the right approach? |
| **Plan approval** | Is this plan sound? Does it match intent? |
| **Incremental review** | Does this implementation unit look right? |
| **Security triage** | Fix, dismiss, or create ticket for findings? |
| **PR/MR readiness** | Is this ready for team review? |

Between gates, Claude operates autonomously. The key insight: **you don't need to understand every line of code Claude writes. You need to understand every decision Claude is making about architecture, approach, and tradeoffs.**

### Principle 3: Verification is the Highest-Leverage Investment

"Probably the most important thing to get great results out of Claude Code: give Claude a way to verify its work." — Boris Cherny

This means:
- Test suites that Claude can run (not just human-readable specs)
- CI pipelines that produce machine-readable output
- Linters and type checkers that catch obvious issues
- Screenshot comparison for UI work
- "Prove to me this works" as a team norm

**The multiplier effect**: Once verification infrastructure exists, Claude can iterate toward correctness autonomously. Without it, every mistake requires human attention.

### Principle 4: Context is the Fundamental Constraint

Claude's context window holds the entire conversation: messages, file contents, command output. It fills fast. Performance degrades as it fills.

**Every practice is either about providing the right context or protecting the context window:**
- CLAUDE.md provides persistent context without consuming conversation space
- Skills provide on-demand context (loaded only when relevant)
- Subagents protect the main context (research in separate windows, only summaries return)
- `/clear` resets context between unrelated tasks
- Worktrees provide filesystem-level isolation between parallel sessions
- Statusline shows context usage so you know when you're running low

**The team rule**: After two failed corrections in one session, `/clear` and start fresh with a better prompt. A clean session with a better prompt almost always outperforms a long session with accumulated corrections.

### Principle 5: The Convention Layer Compounds

The convention layer is the team's institutional knowledge made executable. It has **two complementary systems** in Claude Code:

**The CLAUDE.md hierarchy** — human-authored instructions TO Claude:

- **Root `CLAUDE.md`** = lean project overview, build/test commands, key directories (~60 lines max)
- **`.claude/rules/*.md`** = modular, topic-specific rules (coding standards, testing, git workflow, architecture)
- **`~/.claude/CLAUDE.md`** = personal preferences across all projects
- **`CLAUDE.local.md`** = personal per-project overrides (gitignored)

**The broader convention layer** — skills, hooks, and agents:

- **Skills** = on-demand knowledge and workflows (loaded when relevant, invoked with /)
- **Hooks** = deterministic enforcement (must happen every time, no exceptions)
- **Agents** = specialized assistants (own context, own tools, own focus)

**Why `.claude/rules/` matters**: Modular rules files reduce merge conflicts, are path-scopable (different rules for different parts of a monorepo via YAML frontmatter), and keep root CLAUDE.md short. Short CLAUDE.md = Claude actually reads and follows every instruction.

**Auto-memory — the self-authoring pattern**: Claude maintains its own persistent notes at `~/.claude/projects/<project>/memory/`. This is separate from CLAUDE.md. Humans write CLAUDE.md (instructions to Claude). Claude writes auto-memory (notes for itself — gotchas, patterns, lessons learned). Over time, auto-memory captures repo-specific learnings that would bloat CLAUDE.md.

**The maintenance discipline**: Review CLAUDE.md and `.claude/rules/` weekly as a team. Remove rules Claude already follows without prompting. Consolidate duplicates. Keep root CLAUDE.md under 60 lines, each rules file focused on one topic. Treat the convention layer like production code.

### Principle 6: Consistent Before Advanced

Teams must master the basic SDLC loop (issue, plan, implement, review, merge) with human-in-the-loop before attempting parallel agents, worktrees, or agent teams.

**Why**: Advanced patterns (worktrees, agent teams, headless mode) amplify whatever workflow you already have. If your workflow is inconsistent, you'll get inconsistent results faster. If your workflow is solid, you'll get solid results at scale.

**The crawl-walk-run progression**:
- **Crawl**: One developer, one Claude, one session, one issue at a time
- **Walk**: One developer, multiple Claude sessions (worktrees), skills and subagents
- **Run**: Team-wide coordination, agent teams, headless automation, CI integration

### Principle 7: Skills Encode What Teams Learn

"If you do something more than once a day, make it a skill." — Claude Code team

Skills aren't just fancy prompts. They're **executable institutional knowledge**:
- How this team does code review
- How this team queries the database
- How this team handles tech debt
- How this team creates issues (outcomes, not implementation)
- How this team syncs with external systems (Slack, Jira, analytics)

**The integration pattern**: Skills turn Claude Code into a hub. Instead of switching between tools (Jira, Slack, BigQuery, GitHub), you stay in the terminal and Claude handles the integration. Each skill encodes how your team uses that integration.

### Principle 8: Hooks Enforce, CLAUDE.md Advises

CLAUDE.md instructions are advisory — Claude might ignore them under context pressure. Hooks are deterministic.

| Use Case | CLAUDE.md | Hook |
|----------|-----------|------|
| "Run linting after edits" | Might forget | Will always happen |
| "Don't modify migration files" | Might override | Will block the action |
| "Ask before creating external resources" | Might skip | Will require approval |

**The rule of thumb**: If the consequence of skipping is a minor style issue, put it in CLAUDE.md. If the consequence is data loss, broken external systems, or security risk, make it a hook.

---

## The Convention Layer Architecture

The convention layer is one of three compounding assets. But how do teams create and maintain it — especially across multiple repos? This section describes the architecture.

### Claude Code's Official File Hierarchy

Claude Code loads instructions from a 6-level hierarchy, all additive (more specific wins on conflict):

| Level | Location | Scope | Priority |
|-------|----------|-------|----------|
| **Managed policy** | System-level CLAUDE.md | Org-wide, cannot be overridden | Highest |
| **Project** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared via git | Overrides user |
| **Project rules** | `./.claude/rules/*.md` | Modular, topic-specific, path-scopable | Same as project |
| **User** | `~/.claude/CLAUDE.md` | Personal across all projects | Lowest explicit |
| **Local** | `./CLAUDE.local.md` | Personal per-project (gitignored) | Overrides project & user |
| **Auto memory** | `~/.claude/projects/<project>/memory/` | Claude's own notes to itself | Separate system |

Key behaviors: parent directory CLAUDE.md files load recursively up to root. Child directory CLAUDE.md files load on-demand when Claude reads files in those dirs. `@import` syntax allows referencing other files.

### Three Layers of Convention

| Layer | Scope | Where It Lives | Who Maintains |
|-------|-------|----------------|---------------|
| **Team Conventions** | All repos, all projects | Configured doc backend (Confluence / Google Drive / RAG Memory) | Team lead / periodic review |
| **Repo Convention Layer** | Single repository | Lean `CLAUDE.md` + `.claude/rules/*.md` (checked into git) | Generated by skill + developer review + auto-memory over time |
| **Personal Preferences** | Individual developer | `~/.claude/CLAUDE.md` + `CLAUDE.local.md` | Individual developer |

### How They Compose

**Team conventions** are stored centrally in the doc backend (the same backend configured via `/devflow-setup`). Updated once, pulled into any repo on demand.

**Repo convention layer** is generated as multiple files:
- Root `CLAUDE.md` — lean (~60 lines): project overview, build/test commands, key directories
- `.claude/rules/coding-standards.md` — resolved coding conventions for this repo
- `.claude/rules/testing.md` — testing framework, approach, coverage expectations
- `.claude/rules/git-workflow.md` — branching, commits, PR/MR process
- `.claude/rules/architecture.md` — patterns, key decisions, constraints
- Additional rules files as needed

**Personal preferences** layer on top via `~/.claude/CLAUDE.md` (global) and `CLAUDE.local.md` (per-project, gitignored).

When team conventions change, developers re-run the generate skill → rules files update. Auto-memory accumulates repo-specific learnings separately.

### Why This Architecture

- **Aligns with official Claude Code patterns** — uses `.claude/rules/` exactly as Anthropic intended
- **Keeps root CLAUDE.md short** — under the recommended ~60 lines, so instructions aren't ignored
- **Modular rules reduce merge conflicts** — each topic is a separate file
- **Rules are path-scopable** — different conventions for different parts of a monorepo
- **No new storage mechanism** — team conventions use existing doc backends
- **Everything is standalone** — checked into git, works without the plugin
- **Centrally maintainable** — one source of truth for team conventions in doc backend

### Two Skills Support This Architecture

1. **Capture Team Conventions** — guided interview to capture team-wide conventions, stored in the configured doc backend. Re-runnable to update specific sections.

2. **Generate / Maintain Repo Convention Layer** — analyze a repo, optionally retrieve team conventions, reconcile deviations with developer input, and generate lean CLAUDE.md + `.claude/rules/` files. Three modes: existing repo (deviation detection), greenfield (bootstrap from conventions), and maintenance (drift detection).

See `.devflow/plans/convention-layer-skills.md` for detailed skill designs.

---

## The Maturity Model

### Phase 1: BASELINE — One Team, One Workflow

**Goal**: Every developer follows the same issue-to-merge workflow with Claude Code.

**Prerequisites (one-time setup before the daily rhythm):**
1. Run `/devflow:foundation:setup` → configure backends (issue tracking, docs, VCS)
2. Run **capture-conventions** → guided interview → team conventions stored in doc backend
3. Each developer runs **generate-claude-md** in their repo(s) → lean CLAUDE.md + `.claude/rules/` generated
4. Now the team is ready for the daily SDLC loop

**The essential practices:**
1. Repo convention layer checked into git: lean CLAUDE.md + `.claude/rules/*.md` (team conventions, not individual preferences)
2. One SDLC workflow: issue, explore, plan, implement, verify, merge
3. Plan mode as default for non-trivial work
4. Human approval at every gate (no autonomous merging)
5. Test suites that Claude can run
6. Approval hooks for external system modifications
7. `/clear` between unrelated tasks

**The developer's daily rhythm:**
1. Pick an issue (or have one assigned)
2. Enter Plan Mode, explore the codebase, understand the problem
3. Have Claude create a detailed plan (with clarifying questions)
4. Review and approve the plan
5. Claude implements incrementally, pausing after each unit
6. Run tests, verify behavior, review code
7. Claude creates PR/MR with issue references
8. Move to next issue

**Ongoing convention maintenance:**
- Team conventions change → update central doc (re-run capture skill or edit directly)
- Developer re-runs generate-claude-md in maintenance mode → convention layer syncs
- Auto-memory accumulates repo-specific learnings (Claude's notes — separate from CLAUDE.md)
- Periodic team review of both conventions doc and repo convention layers

**What success looks like**: A new team member can follow the same workflow on day one. Every PR/MR follows the same structure. The repo's convention layer (CLAUDE.md + rules files) captures 80%+ of "how we do things here."

### Phase 2: ACCELERATE — Multiply Throughput

**Goal**: Individual developers multiply their output with parallel sessions and advanced primitives.

**The essential practices:**
1. Git worktrees for parallel Claude sessions (2-3 per developer)
   - Development worktree (feature implementation)
   - Analysis worktree (read-only investigation, never commits)
   - Experimental worktree (throwaway experiments)
2. Custom skills for repeated team workflows
3. Subagents as habit ("use subagents" as suffix for research, verification, generation)
4. Two-Claude review pattern for plans
5. Voice dictation for long prompts (4x faster input)
6. Advanced prompting patterns:
   - "Before you plan, ask me clarifying questions about anything ambiguous"
   - "Knowing everything you know now, scrap this and implement the elegant solution"
   - "Grill me on these changes and don't make a PR until I pass your test"
7. Context-aware status line (usage %, branch, worktree, time since commit)

**What success looks like**: Developers routinely run 2-3 parallel sessions. Skills encode most team-specific workflows. Context hygiene is automatic (subagents for research, /clear between tasks).

### Phase 3: ORCHESTRATE — Team-Scale AI Coordination

**Goal**: The team leverages multi-agent coordination, automation, and advanced orchestration.

**The essential practices:**
1. Agent teams for complex tasks:
   - Parallel code review (security, performance, tests as separate reviewers)
   - Competing hypothesis debugging (adversarial investigation)
   - Cross-layer implementation (frontend, backend, tests as teammates)
2. Headless mode (`claude -p`) for CI and automation:
   - Automated bug fixing from CI failures
   - Fan-out migrations across many files
   - Automated PR descriptions and changelog generation
3. Auto-approval hooks for team-approved safe operations
4. Writer/Reviewer session patterns as standard quality gates
5. Knowledge feedback loops (skills evolve from patterns, CLAUDE.md self-maintains)

**What success looks like**: Complex features are planned and implemented by agent teams. CI failures are automatically investigated and fixed. The convention layer evolves faster than the codebase.

---

## Rethinking DevFlow

### Current Structure
The existing DevFlow plugin is strong at Phase 1 (SDLC loop with human-in-the-loop) but is organized around backend operations rather than developer journey:

```
Current: organized by backend/function
commands/build/     (SDLC workflow)
commands/admin/     (setup)
commands/pm/        (project management)
commands/docs/      (documentation)
commands/rag-memory/ (knowledge base)
commands/devops/    (DevOps)
skills/             (build-ops, knowledge-mgmt, repo-explorer)
hooks/              (approval hooks)
```

### Proposed: Organized by Developer Journey

The convention layer should mirror the maturity model. A developer (or team) should be able to see where they are and what's available at their level:

```
Proposed: organized by maturity phase and developer journey

foundation/
  setup/          (backend configuration, MCP setup)
  onboard/        (team onboarding, first-time walkthrough)
  claude-md/      (CLAUDE.md generation, maintenance, team review)
  knowledge/      (RAG memory, documentation management)

baseline/           (Phase 1: the daily SDLC loop)
  fetch/          (fetch issue, analyze feasibility)
  plan/           (explore, plan with clarifying questions)
  implement/      (incremental implementation with gates)
  verify/         (test, security review, validation)
  complete/       (PR/MR creation, issue closure)
  maintain/       (post-merge cleanup, CLAUDE.md updates)

accelerate/         (Phase 2: multiply throughput)
  worktrees/      (setup, management, best practices)
  patterns/       (two-Claude review, advanced prompting)
  parallel/       (subagent strategies, context hygiene)

orchestrate/        (Phase 3: team-scale coordination)
  teams/          (agent team templates and patterns)
  automate/       (headless mode, CI integration)
  evolve/         (self-maintaining conventions, feedback loops)

hooks/              (cross-cutting enforcement)
  approval/       (external system protection)
  quality/        (post-edit linting, test running)
  safety/         (migration protection, production guards)
```

### Key Structural Changes

1. **Foundation is separate from workflow.** Setup, onboarding, and knowledge management aren't part of the daily SDLC loop — they're infrastructure that supports it.

2. **The SDLC loop is "baseline," not "build."** The naming makes it clear this is the starting point, not an advanced feature. Teams start here.

3. **Accelerate and Orchestrate are explicit layers.** Teams can see what's available at their maturity level. This also guides the "what to build next" roadmap.

4. **Hooks are organized by purpose, not backend.** "Approval" vs "quality" vs "safety" is more intuitive than "Atlassian" vs "GitLab."

5. **The philosophy is embedded in the structure.** The directory tree itself teaches the maturity model: Foundation, Baseline, Accelerate, Orchestrate.

### Naming Philosophy: Specific Objects, Not Generic Verbs

**Problem with generic names**: If `/devflow:baseline:fetch` means "fetch an issue," what happens when we need to fetch a GitLab merge request, a Confluence page, or a roadmap item?

**The current names are better than they look.** `fetch-issue`, `plan-work`, `implement-plan`, `complete-issue` — these carry semantic meaning about WHAT is being fetched/planned/implemented. The object matters.

**Proposed naming principle**: `{phase}:{verb}-{object}` — keep the object in the name so commands remain unambiguous as the plugin grows.

**Immediate consistency fix**: All issue-centric commands should follow `{verb}-issue`:

| Current | Consistent Name | Change? |
|---------|----------------|---------|
| `fetch-issue` | `fetch-issue` | No change needed |
| `plan-work` | **`plan-issue`** | Rename — it's planning work ON an issue |
| `implement-plan` | **`implement-issue`** | Rename — it's implementing the plan FOR an issue |
| `security-review` | `security-review` | No change — reviews code, not issue-centric |
| `complete-issue` | `complete-issue` | No change needed |
| `create-issue` | `create-issue` | No change needed |
| `post-merge` | `post-merge` | No change — cleanup process, not issue-centric |

**Full proposed command mapping (phase restructure + naming fix)**:

| Current | Proposed | Notes |
|---------|----------|-------|
| `/devflow:build:fetch-issue` | `/devflow:baseline:fetch-issue` | Phase change only |
| `/devflow:build:plan-work` | `/devflow:baseline:plan-issue` | Renamed for consistency |
| `/devflow:build:implement-plan` | `/devflow:baseline:implement-issue` | Renamed for consistency |
| `/devflow:build:security-review` | `/devflow:baseline:security-review` | Phase change only |
| `/devflow:build:complete-issue` | `/devflow:baseline:complete-issue` | Phase change only |
| `/devflow:build:post-merge` | `/devflow:baseline:post-merge` | Phase change only |
| `/devflow:build:create-issue` | `/devflow:baseline:create-issue` | Phase change only |
| `/devflow-setup` | `/devflow:foundation:setup` | Moved to foundation |
| `/knowledge-management` | `/devflow:foundation:knowledge` | Moved to foundation |
| (new) | `/devflow:foundation:capture-conventions` | Guided interview → team conventions stored in doc backend |
| (new) | `/devflow:foundation:generate-claude-md` | Analyze repo + conventions → lean CLAUDE.md + `.claude/rules/` |
| (new) | `/devflow:accelerate:setup-worktrees` | Worktree setup and management |
| (new) | `/devflow:accelerate:review-plan` | Two-Claude review pattern |
| (new) | `/devflow:orchestrate:spawn-team` | Agent team templates |

---

## The Narrative

### For Teams

> Your team is already using AI to write code. But each developer is doing it differently — different prompts, different approaches, different levels of trust. Some paste entire files into ChatGPT. Some use Copilot autocomplete. Some have tried Claude Code but don't use it consistently.
>
> Here's what we've learned from the Claude Code team itself, from Anthropic's published best practices, and from teams shipping production software with AI every day:
>
> **The developers getting the best results aren't the ones prompting the hardest. They're the ones who've built the best infrastructure for AI to work within.**
>
> That infrastructure has three parts:
> 1. **A consistent workflow** — the same issue-to-merge path every time
> 2. **A convention layer** — team knowledge encoded in files AI reads automatically
> 3. **A verification layer** — test suites, CI, linting that let AI self-correct
>
> We start by getting everyone on the same workflow. One way to plan. One way to implement. One way to verify. Human approval at every decision point. This isn't about autonomy — it's about consistency.
>
> Once that's muscle memory, we accelerate. Parallel sessions. Custom skills. Subagents for research. Each developer multiplying their throughput, but within the same consistent framework.
>
> Then we orchestrate. Agent teams for complex features. Automated CI fixing. The convention layer evolving faster than the codebase itself.
>
> The goal isn't to replace developers with AI. It's to reposition developers as decision-makers and let AI handle execution. The teams that adopt this consistently will ship 3-5x more while maintaining or improving quality. The teams that stay ad-hoc will wonder why their AI tools feel unreliable.

### The One-Liner

**"Define intent. Decide at gates. Let AI execute between them."**
