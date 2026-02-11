# Iteration Plan Template

Reference template for the pm/plan-iterations skill. Quality criteria embedded.

---

## Iteration [Number]: [Goal Title]

**Duration:** [estimated duration or "flexible"]

**Goal:** [One-sentence summary of what "done" looks like for this iteration]

**Status:** Planning | Active | Completed

---

### Iteration Goal

What is the end-to-end outcome of this iteration? What can you demonstrate or deliver when it's complete?

**Quality check:**
- Describes a deliverable outcome, not just "finish tasks X, Y, Z"
- For iteration 1: should be a walking skeleton — minimal end-to-end functionality
- Realistic given the team's capacity and the task dependencies

---

### Tasks

| # | Task | Type | Priority | Depends On | Size | Issue Key |
|---|------|------|----------|------------|------|-----------|
| 1 | [Task title] | Feature / Task | Must / Should / Nice | — | S/M/L | [created after approval] |
| 2 | [Task title] | Feature / Task | Must / Should / Nice | Task 1 | S/M/L | |
| 3 | [Task title] | Task | Must | — | S/M/L | |

**Quality check:**
- Tasks are small enough to estimate (S/M/L or T-shirt sizing)
- Dependencies between tasks identified and ordered
- Cross-cutting concerns included (auth, logging, error handling, observability)
- Each task traces back to a PRD requirement or architecture decision
- Features → Executable Specs, Infrastructure → Tasks (following DevFlow conventions)

---

### Cross-Cutting Concerns

Concerns that span multiple tasks and must be addressed:

| Concern | How Addressed | Which Tasks |
|---------|---------------|-------------|
| Authentication | [approach] | Tasks 1, 3 |
| Error handling | [approach] | All tasks |
| Logging/observability | [approach] | Tasks 2, 4 |

**Quality check:**
- Auth, logging, error handling, observability accounted for
- Each concern maps to specific tasks
- Not deferred indefinitely ("we'll add it later" is a smell)

---

### Scaffolding (Iteration 1 Only)

Foundation work that must complete before feature tasks:

| Item | Tool/Approach | Depends On |
|------|--------------|------------|
| Repository setup | [cookiecutter, manual, etc.] | — |
| CI/CD pipeline | [GitHub Actions, GitLab CI, etc.] | Repo setup |
| Base dependencies | [package.json, requirements.txt, etc.] | Repo setup |
| Convention layer | generate-claude-md | Repo setup |

**Quality check:**
- Scaffolding tasks precede feature tasks in dependency order
- Convention layer setup included for new repos
- CI/CD is functional before feature work begins

---

### Acceptance Criteria (Iteration-Level)

What must be true for this iteration to be "done"?

- [ ] [End-to-end outcome works as described in iteration goal]
- [ ] [All must-have tasks completed]
- [ ] [Tests pass]
- [ ] [PRD requirements covered by this iteration are verifiable]

---

## Overall Iteration Plan Quality Criteria

A good iteration plan:
- Tasks are small enough to estimate and build within an iteration
- Dependencies between tasks are identified and ordered
- First iteration delivers end-to-end value (walking skeleton)
- Cross-cutting concerns are accounted for
- Each task traces back to a PRD requirement or architecture decision
- Only the first 2-3 iterations are planned in detail
