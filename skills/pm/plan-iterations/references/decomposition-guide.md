# Decomposition Guide

Reference for the pm/plan-iterations skill. Guidance on breaking PRD requirements and architecture into buildable tasks.

---

## Decomposition Principles

### 1. PRD Requirements → Tasks

Each functional requirement in the PRD becomes one or more tasks:

| PRD Element | Becomes | DevFlow Type |
|-------------|---------|-------------|
| Functional requirement (user-facing) | Executable Spec (feature) | Feature |
| Non-functional requirement | Task (infrastructure) | Task |
| Cross-cutting concern | Task (infrastructure) | Task |
| Scaffolding/setup | Task (infrastructure) | Task |

### 2. Size Guide

Tasks should be completable in a reasonable timeframe:

| Size | Rough Scope | When to Break Down Further |
|------|-------------|---------------------------|
| S | Single component, clear scope | Don't — this is ideal |
| M | Multiple components or moderate complexity | Consider splitting if dependencies are unclear |
| L | Spans multiple systems or high uncertainty | Must split — L tasks are planning risks |
| XL | Multi-week effort | Always split — this is an epic in disguise |

### 3. Dependency Identification

Look for these dependency patterns:

| Pattern | Example | How to Handle |
|---------|---------|---------------|
| Data dependency | "Search requires indexed data" | Index task before search task |
| API dependency | "Frontend needs API endpoint" | API task before frontend task |
| Infrastructure dependency | "Deployment needs CI/CD" | CI/CD task in scaffolding |
| Cross-cutting dependency | "All features need auth" | Auth task in scaffolding or iteration 1 |

### 4. Cross-Cutting Concerns

Always check for these — they're the most commonly forgotten:

| Concern | Questions to Ask |
|---------|-----------------|
| **Authentication** | Who needs to authenticate? What method? Where is the boundary? |
| **Authorization** | What permissions exist? Who can do what? |
| **Error handling** | What's the error handling pattern? How are errors surfaced? |
| **Logging** | What gets logged? What format? Where do logs go? |
| **Observability** | What metrics matter? What alerts? What dashboards? |
| **Configuration** | What's configurable? How are configs managed? |
| **Testing infrastructure** | What test frameworks? CI integration? Coverage requirements? |

### 5. Walking Skeleton (Iteration 1)

Iteration 1 should deliver a walking skeleton — minimal end-to-end functionality that proves the architecture works:

**What a walking skeleton includes:**
- Basic project structure (scaffolding)
- One thin slice of end-to-end functionality
- CI/CD pipeline running
- Core infrastructure in place (auth, error handling, logging — at least stubbed)

**What it does NOT include:**
- Full feature implementations
- Performance optimization
- Comprehensive error handling
- All edge cases

**The test:** Can you demonstrate the system working end-to-end, even if the functionality is minimal? If yes, the skeleton walks.

### 6. Iteration Grouping Strategy

| Iteration | Focus | Typical Contents |
|-----------|-------|-----------------|
| 1 | Walking skeleton | Scaffolding + one thin slice + infrastructure |
| 2 | Core features | Must-have features, building on skeleton |
| 3 | Completion | Should-have features, polish, edge cases |

**Only plan 2-3 iterations.** Later iterations will be planned as the team learns from earlier ones.

### 7. Acceptance Criteria for Tasks

Each task needs clear acceptance criteria. Follow DevFlow conventions:

- State outcomes, not implementation steps
- "User can search by keyword and see results" (good)
- "Create search endpoint using Elasticsearch" (bad — that's implementation)

For executable specs (features):

```
**Acceptance Criteria:**
- [ ] [Observable outcome 1]
- [ ] [Observable outcome 2]
- [ ] [Edge case handled]
```

For tasks (infrastructure):

```
**Acceptance Criteria:**
- [ ] [Infrastructure works as expected]
- [ ] [Integration verified]
```

### 8. Linking Back to Upstream Artifacts

Every task should be traceable:

| Task Field | Links To |
|------------|----------|
| Description / Background | PRD requirement (section + number) |
| Technical guidance | Architecture doc (section) + relevant ADRs |
| Acceptance criteria | PRD acceptance criteria (restated for this specific task) |
