# Upstream SDLC: Problem Space & Requirements

> **Purpose:** Define the upstream product activities that happen between "someone has an idea" and "team is ready for the first development iteration." Articulates WHAT these activities are, WHY they matter, WHO participates, and WHAT artifacts they produce.
>
> **Status:** Requirements phase. This document captures the problem space only. Design (how to support these activities) is a separate concern and a separate artifact.
>
> **Supersedes:** Phases 1-3 and 5 (Ideate, Architect, Scaffold, Iterate) from `ai-native-sdlc-workflow.md`. That document still covers code review, bug workflow, and release management as separate enhancements.

---

## Table of Contents

1. [The Problem](#the-problem)
2. [Who This Is For](#who-this-is-for)
3. [Why AI Assistance Matters for Upstream Activities](#why-ai-assistance-matters-for-upstream-activities)
4. [Guiding Principles](#guiding-principles)
5. [Part 1: Upstream Activities & Artifacts](#part-1-upstream-activities--artifacts)
6. [Part 2: Capabilities Required for the Artifact Lifecycle](#part-2-capabilities-required-for-the-artifact-lifecycle)
7. [Part 3: Decisions](#part-3-decisions)
8. [Part 4: Scope Boundaries](#part-4-scope-boundaries)

---

## The Problem

The DevFlow plugin handles feature development well: fetch an issue, plan the implementation, implement it, complete it. But that workflow assumes someone has already done the significant work of turning a rough idea into a well-formed, actionable issue.

**What happens between "someone has an idea" and "here's an issue ready to build"?**

Today, that upstream work is:

1. **Unsupported by the plugin.** The build workflow starts at "here's an issue." Everything before that — problem framing, requirements, architecture, work decomposition — happens outside the system with no AI assistance.

2. **Scattered and disconnected.** Product decisions live in Google Docs, Confluence pages, Slack threads, meeting notes, email chains. By the time a developer picks up an issue, the rationale behind it is buried or lost.

3. **Duplicated across efforts.** Without searchable prior art, teams explore the same problems repeatedly. Past attempts that were shelved aren't discoverable. Lessons learned from failed approaches aren't preserved.

4. **Quickly outdated.** Requirements start as documents but become lies within weeks. Architecture docs describe what was planned, not what was built. No one maintains them because maintenance is tedious manual work.

5. **Implicitly decided.** Architecture and technology decisions get made during implementation rather than deliberately during design. By the time someone realizes the choices don't compose, significant code has been written.

6. **Context-losing.** The gap between product vision and developer task is where the "why" gets lost. A developer sees "implement search endpoint" but doesn't know that the PM chose full-text search over exact match because of a specific client requirement. The decision happened, but the context didn't travel.

**The cost of this gap:**

- Teams build solutions to the wrong problems (no problem framing)
- Developers make assumptions about what "done" means (no clear requirements)
- Technical decisions that don't compose create architectural debt from day one (no deliberate architecture)
- Teams try to build everything at once instead of delivering incremental value (no iteration planning)
- New team members can't trust documentation because it's stale (no artifact maintenance)
- The same mistakes repeat because past decisions and their rationale aren't preserved

---

## Who This Is For

### The Cross-Functional Reality

AI is collapsing traditional role boundaries. In AI-assisted teams — especially small ones — the same person who frames the problem might also write the architecture, implement features, and test them. A technical PM becomes a code contributor, tester, and QC lead. A developer becomes an architect and documentation author. Teams are becoming small, cross-functional groups where everyone wears multiple hats.

The upstream activities described in this document require certain **perspectives**, not certain **people**:

| Perspective | What It Contributes | Where It Matters Most |
|-------------|---------------------|----------------------|
| **Product perspective** | Why are we building this? For whom? What does success look like? | Problem framing, requirements, prioritization |
| **Technical perspective** | Is this feasible? What are the trade-offs? How does it fit the existing system? | Architecture, technology selection, decomposition |
| **Implementation perspective** | How complex is this? What patterns exist? What will be hard? | Decomposition, effort estimation, scaffolding |
| **Stakeholder perspective** | Does this align with business goals? Is the investment justified? | PRD review, architecture approval |

In a 20-person team, these perspectives might belong to different people with different job titles. In a 3-person team, one person might hold all four. **The activities are the same regardless of team size or role structure.** The phases below describe WHAT needs to happen, not WHO does it.

### By Team Size

| Context | What Changes |
|---------|--------------|
| **Solo developer** | Wears all hats. Needs all activities but with minimal ceremony. A solo dev's PRD might be 1 page, not 10. The activities scale down, but the value of structured thinking still applies — a solo dev who skips problem framing still builds the wrong thing. |
| **Small team (2-5)** | Cross-functional. Everyone participates in most activities. Less formal gates. Artifacts serve as shared understanding more than formal handoffs. |
| **Larger team (5+)** | More specialization possible but not required. Multiple stakeholders reviewing artifacts. Artifacts serve as contracts between people who don't talk daily. The cost of ambiguity rises with team size. |

### By Project Context

| Context | What Changes |
|---------|--------------|
| **Greenfield** | No existing code. Architecture decisions are fully open. Team conventions (if captured) matter most here as starting guidance. Foundation/scaffolding is a distinct activity before feature work begins. |
| **Brownfield (extending existing product)** | Architecture is partially decided by what's already built. Analysis of the existing system is critical before making new decisions. New work must fit existing patterns or deliberately break from them with documented rationale. |
| **Major new capability in existing product** | Mix of both. Existing system constrains some decisions, but the new capability area may have greenfield architectural decisions within a brownfield context. |

---

## Why AI Assistance Matters for Upstream Activities

AI assistance isn't equally valuable everywhere. Here's where it specifically compounds in upstream product work:

1. **Synthesis from scattered sources.** Teams almost always have existing material spread across multiple systems. AI can ingest 15 scattered documents and produce a coherent coverage map against a template in minutes. A human doing this manually takes hours and misses things.

2. **Completeness assessment.** Humans often don't know what they don't know. AI can map existing requirements against a comprehensive template and systematically identify every gap — including gaps humans wouldn't think to check.

3. **Cross-system prior art discovery.** When checking whether a problem has been explored before, AI can search across all configured documentation systems, the codebase, and the issue tracker simultaneously. Humans search one system at a time and give up after two.

4. **Consistency maintenance.** When a PRD changes, does the architecture doc still hold? Do existing issues still make sense? AI can detect drift across artifacts by holding all of them in context. Humans forget to check, or check one thing and miss another.

5. **Structured drafting from messy inputs.** Given scattered, overlapping, sometimes contradictory inputs, AI produces structured first drafts that humans can review and refine. This eliminates blank-page paralysis and transforms the human role from "writer" to "editor."

6. **Rationale preservation.** AI can capture decision context (why this option, not that one; what trade-offs were considered) in real-time as decisions are made. Humans write down decisions but almost never write down rationale — it's the part that matters most and gets lost first.

7. **In-the-flow decision capture.** When a developer discovers mid-implementation that the planned approach won't work, AI can capture that decision and route it to the right artifact — without the developer leaving their current context. This is what makes artifact maintenance actually happen instead of being a chore everyone skips.

---

## Guiding Principles

1. **Backend-agnostic.** Teams choose their own documentation backend(s): Confluence, Google Drive, RAG Memory, or any combination. Upstream activities must work with whatever is configured. Some backends offer additional capabilities (temporal queries, relationship graphs) but none can be assumed.

2. **Lean artifacts.** No Scrum-specific terminology or mandatory ceremony artifacts. Use the plugin's own vocabulary: executable specs (not user stories), tasks (not stories), iterations (not sprints). Epics only if the team wants them — never required. The ceremony scales to the team.

3. **Conventions-aware, not conventions-dependent.** When making architecture or technology decisions, team conventions (if they've been captured) should be surfaced as context. But they must never be assumed to exist, and the user always has final say. Conventions are context, not constraints.

4. **Human-in-the-loop always.** AI assists, drafts, researches, and proposes. Humans decide. Every artifact must be reviewed and approved before it's considered baselined.

5. **Existing material is the norm, not the exception.** Most teams don't start from a blank page. The primary workflow is: ingest what exists, assess its completeness against a template, identify gaps, and help fill them. "Starting from scratch" is the edge case, not the default.

6. **Capture decisions in the flow, not after the fact.** Artifact updates must happen as part of the work itself — not as a separate ceremony that people skip. When a decision changes during development, the AI captures it where it belongs without requiring the developer to switch context. This is what keeps artifacts honest.

---

## Part 1: Upstream Activities & Artifacts

Everything that happens between "someone has an idea" and "team is ready to start the first iteration." Organized by natural phase boundaries.

### The Common Case: Existing Material

Before diving into phases, it's important to acknowledge how teams actually work. The phases below are presented linearly, but in practice a team typically arrives with some combination of:

- A Google Doc with a rough product brief or requirements
- Scattered Confluence pages from prior exploration
- Meeting notes or Slack threads capturing decisions
- A partial architecture sketch or tech stack decision
- An existing codebase they're extending
- Client emails or support tickets describing the problem
- A prior attempt that was shelved or partially completed
- Maybe even a thorough PRD that just needs to be imported and gap-checked

**The primary workflow is always: ingest existing material, assess what's there, map it against what a complete artifact looks like, show the gaps, and help fill them.** Determine which phase(s) the existing material covers, what's missing, and where to pick up.

This means the first question is always: "Do you have existing material? Point me to it." Only if the answer is "no, starting from scratch" does the guided creation flow activate.

#### Multi-Source Ingestion

Existing material is rarely in one place. A single product effort might have inputs scattered across:

- **Documentation systems** — Confluence pages, Google Drive files, RAG Memory documents
- **Local files** — markdown in the repo, PDFs, exported docs
- **URLs** — public specs, competitor analysis, API documentation
- **Raw text** — pasted from Slack, email, meeting notes

All of these input types must be accepted, pulled together, and synthesized. The user experience should be:

1. **Proactive scan** — Search configured backends for anything related to the topic. Present what's found.
2. **Ask for more** — "Here's what I found. Is there anything else to add?" User points to additional sources.
3. **Reflect** — Show the user everything that was gathered, organized clearly.
4. **Confirm** — User confirms this is the complete set of inputs before proceeding.
5. **Assess** — Content is mapped against the target artifact template. A coverage report is produced: what's covered, what's partial, what's missing entirely.
6. **Fill gaps** — For each gap, the user is asked directly, AI drafts from context, or the gap is marked as an open question.
7. **Consolidate** — The structured artifact is produced from the combined inputs + gap-fills. User reviews, edits, approves.

#### Completeness Scales with Input

| Existing Material | What Happens |
|-------------------|-------------|
| Thorough existing docs | Ingest, map to template, highlight minor gaps, consolidate quickly |
| Rough/partial docs | Ingest, map to template, show significant gaps, guided creation for missing sections |
| Scattered fragments | Ingest all, deduplicate, reconcile conflicts, synthesize into template, extensive gap-filling |
| Nothing | Guided creation from scratch (the edge case) |

These aren't four separate modes — they're a continuous spectrum where the amount of gap-filling adapts automatically based on input completeness.

---

### Phase A: Problem Discovery & Framing

**Why this phase matters:** Without explicit problem framing, teams build solutions to problems they haven't validated. They skip feasibility checks and rediscover what a past team already learned. They start requirements without agreeing on scope, leading to endless creep.

**What perspectives matter:** Product perspective (why this matters, for whom) and technical perspective (is it feasible, has it been tried before).

**What this phase produces:** A structured problem statement with scope boundaries.

#### A1. Problem/Opportunity Capture

Someone has a rough idea — a client request, an internal pain point, a market opportunity, a technical improvement. Could be a Slack message, a meeting note, a shower thought. Or they already have a document (or several) describing the problem space.

- **What AI can do:** Accept input in any form — unstructured text, existing docs, URLs, pasted fragments. Assess what's there: is this a well-formed problem statement or a vague direction? Ask clarifying questions for the gaps. Structure it. Store it so it's not lost.
- **What humans do:** Point to where existing material lives. Decide this is worth exploring further.

#### A2. Prior Art & Feasibility Check

Before investing in requirements: has this been tried? Is it feasible? Does something similar exist in our product, backlog, or codebase?

- **What AI can do:** Search all configured documentation systems for past related work. Search the codebase for existing capabilities. Search the issue tracker for similar past items. Surface connections to related past efforts. Check if a past initiative was abandoned and why.
- **What humans do:** Interpret findings. Decide whether past attempts are relevant. Make the go/no-go call.

**What goes wrong if skipped:** Team invests weeks in requirements for something that already exists in the codebase, or that was tried and abandoned for reasons that are still valid.

#### A3. Problem Scoping & Boundary Setting

What is IN scope? What is explicitly OUT? Is this a new product, a major feature for an existing product, or an extension?

- **What AI can do:** Draft scope based on problem statement. Ask targeted boundary questions. Reference existing product capabilities from the knowledge base.
- **What humans do:** Strategic decisions about investment level, scope boundaries, priority relative to other work.

#### Problem Statement Quality Criteria

A good problem statement:
- Clearly states the problem or opportunity (not the solution)
- Identifies who is affected and how
- Explains why it matters (business impact, user impact, technical impact)
- Has clear scope boundaries (what's in, what's explicitly out)
- References prior related work if any exists
- Has been reviewed by the people who will fund or prioritize the work

---

### Phase B: Requirements Gathering & PRD

**Why this phase matters:** Without structured requirements, developers make assumptions about what "done" means. Scope creeps because there's no agreed-upon boundary. Acceptance criteria are invented during code review instead of defined upfront. Multiple people have different mental models of the product, and the conflicts don't surface until implementation.

**What perspectives matter:** Product perspective (what to build, for whom, why), technical perspective (feasibility constraints), stakeholder perspective (alignment with business goals).

**What this phase produces:** A baselined PRD. WHAT and WHY, never HOW.

#### B1. Requirements Collection

This is where the "existing material" pattern matters most. Requirements almost never start from zero — they're scattered across documentation systems, meeting notes, client emails, support tickets. The team may already have a rough PRD, a formal spec, or just a pile of fragments.

- **What AI can do:** Accept pointers to multiple sources across different systems. Fetch content from each. Deduplicate overlapping requirements. Identify conflicts between sources (source A says "real-time", source B says "batch is fine"). Map all collected requirements against the PRD template to show coverage and gaps.
- **What humans do:** Point to where requirements live. Resolve conflicts between sources. Validate completeness. Fill gaps AI identifies.

#### B2. Requirements Organization & Prioritization

Structure raw inputs into coherent requirement sets. Define functional requirements with acceptance criteria. Prioritize.

- **What AI can do:** Organize by theme/feature area. Draft requirements with acceptance criteria from raw inputs. Present for prioritization.
- **What humans do:** All prioritization decisions. Validate that requirements capture intent. Fill gaps.

#### B3. PRD Drafting

Compile everything into a structured, repeatable document. When existing docs are available, this is primarily a **restructuring and gap-filling** exercise, not a blank-page writing exercise.

**Standard PRD sections:**

1. Executive Summary / Problem Statement
2. Goals & Success Metrics (measurable)
3. Target Users / Personas
4. Functional Requirements (organized by feature area, each with acceptance criteria)
5. Non-Functional Requirements (performance, security, accessibility, compliance)
6. Constraints (timeline, budget, team, technical)
7. Out of Scope (explicit)
8. Dependencies (external systems, other teams)
9. Open Questions / Risks
10. Appendix (research, data, references)

Sections are optional — teams can mark any section N/A with rationale. Not every project needs all 10.

- **What AI can do:** Map collected requirements to template sections. For sections with existing content: restructure, flag ambiguities. For sections with partial content: draft completions, mark assumptions for human review. For missing sections: flag gaps, ask targeted questions or draft from context. When the team has a thorough existing PRD: import it, map to template, identify what's missing or inconsistent — this should be fast.
- **What humans do:** Review every section. Iterate. Fill in what AI can't know (business context, political constraints, budget). Resolve flagged ambiguities.

**What goes wrong if skipped:** Developers build from vague descriptions. "Add search" becomes three different features in three developers' heads. Acceptance criteria are debated in code review. Scope creeps because no one documented what's out of scope.

#### B4. PRD Review & Iteration

Stakeholders review, comment, request changes. Multiple rounds.

- **What AI can do:** Incorporate feedback, redraft sections, track what changed between versions.
- **What humans do:** All review decisions. Approve or request changes.

#### B5. PRD Baseline

PRD is agreed upon as the starting point. Not frozen — will evolve during the initiative — but approved to proceed.

- **What AI can do:** Store the approved version with "baselined" status. Record where it's stored so downstream activities can find it.
- **What humans do:** The approval decision.

#### PRD Quality Criteria

A good PRD:
- Has all relevant template sections addressed (or explicitly marked N/A with rationale)
- Contains measurable, testable acceptance criteria
- Describes WHAT to build, not HOW to build it
- Has conflicts between sources resolved (not hidden)
- Flags open questions explicitly rather than hiding assumptions
- Has been reviewed and approved by relevant people
- Is stored somewhere findable, not buried in a chat thread

#### PRD Shelf Life

A PRD is tied to the **initiative** it was created for, not to the product's lifetime. It captures the vision, scope, and requirements for a specific effort. Once that effort is delivered, the PRD becomes a historical record — "this is what we planned and why." The product itself (codebase, tests, deployed behavior) becomes the source of truth for what the product IS.

Future features get their own scoping and their own specs. They don't retroactively update the original PRD. This avoids turning the PRD into an unwieldy running tally of every feature ever built, and it avoids a DRY violation where the same requirements are maintained in the PRD AND in individual executable specs.

During the active initiative, the PRD should be updated when significant scope or requirement changes happen (see [Phase E: Keeping Artifacts Honest](#phase-e-keeping-artifacts-honest)). After the initiative is delivered, it's historical context.

---

### Phase C: Architecture & Technical Design

**Why this phase matters:** Without deliberate architecture, technical decisions get made implicitly during implementation. Different developers make different assumptions. The decisions don't compose. By the time someone realizes the choices are inconsistent, significant code has been written. Architecture debt accumulates from day one.

Architecture is SEPARATE from the PRD. The PRD says WHAT. Architecture says HOW at a high level. Separating them means requirements can change without automatically invalidating architectural decisions, and vice versa.

**What perspectives matter:** Technical perspective (feasibility, trade-offs, existing system constraints), implementation perspective (complexity, patterns), product perspective (requirements context).

**What this phase produces:** Architecture document + ADRs (Architecture Decision Records).

#### C0. Check for Team Conventions (Optional Context)

Before making technology or architecture decisions, check whether team conventions exist. If the team has previously captured their preferred tech stack, architecture patterns, testing philosophy, etc., those should be surfaced as starting context.

- **If conventions exist:** Present relevant sections. "Your team conventions suggest X — want to use these as a starting point?"
- **If no conventions:** Proceed without them. Perfectly fine.
- **Either way:** User always has final say. Conventions are context, not constraints.

#### C1. Existing System Analysis (Brownfield)

For adding to an existing product: understand current architecture, dependencies, integration points, tech debt.

- **What AI can do:** Analyze existing codebase. Search documentation systems for existing architecture docs, ADRs, past technical decisions. Map dependencies.
- **What humans do:** Interpret findings. Decide whether existing architecture can accommodate the new work.

**What goes wrong if skipped:** New feature built with assumptions that contradict the existing system. Integration pain discovered late. Existing patterns violated, creating inconsistency across the codebase.

#### C2. Technology Selection

Choose languages, frameworks, databases, infrastructure. For existing products: validate existing stack or identify needed additions.

- **What AI can do:** Use team conventions (if they exist) as a starting recommendation. Research current documentation for technology options. Compare alternatives with rationale. For brownfield: analyze what the codebase already uses.
- **What humans do:** Final technology choices. Trade-off resolution.

#### C3. System Design

High-level architecture: components, services, data stores, external integrations, data model, API design.

- **What AI can do:** Draft architecture based on PRD requirements + stack decisions + patterns from existing codebase. Generate diagrams. If team conventions specify architecture patterns, propose those as a starting approach.
- **What humans do:** All design decisions. Validate completeness.

#### C4. Architecture Decision Records (ADRs)

Document key decisions with context, options considered, rationale, consequences.

- **What AI can do:** Structure ADR documents from discussion context. Link to relevant PRD sections.
- **What humans do:** The decisions themselves.

**Why ADRs matter:** Six months from now, someone will ask "why did we use PostgreSQL instead of DynamoDB?" The ADR answers that question. Without it, the rationale is gone and the team either accepts the mystery or re-litigates the decision.

**ADR shelf life:** ADRs outlive the PRD. An architecture decision persists as long as the system uses that decision. When a decision is superseded, a new ADR references the old one ("supersedes ADR-003") so the evolution is traceable. ADRs are the longest-lived upstream artifacts.

#### C5. Architecture Review & Baseline

Technical review, risk identification, approval.

- **What AI can do:** Automated risk assessment (scalability, security, missing considerations). Store baseline.
- **What humans do:** Accept risks. Approve architecture.

#### Architecture Quality Criteria

A good architecture document:
- Addresses all PRD functional requirements (traceable)
- Has architectural answers for non-functional requirements (performance, security, etc.)
- Documents key decisions as ADRs with context, alternatives considered, and rationale
- For brownfield: accounts for existing system constraints and integration points
- Acknowledges trade-offs honestly (not just the happy path)
- Defines components, data model, and integration points explicitly
- Has been reviewed by the people who will build it

---

### Phase D: Work Decomposition & Iteration Planning

**Why this phase matters:** Without decomposition, teams try to build everything at once. Without iteration planning, there's no incremental value delivery — the product is either "not done" or "done" with nothing usable in between. Without clear executable specs, developers interpret vague requirements differently.

**What perspectives matter:** Technical and implementation perspectives (complexity, dependencies, patterns), product perspective (prioritization, iteration goals).

**What this phase produces:** A set of well-formed issues in the configured tracker, grouped into the first 2-3 iterations.

#### D1. Task Decomposition

Break PRD capabilities into a logical set of tasks. Identify dependencies. No mandatory epics layer — go straight from PRD to tasks unless the team explicitly wants grouping.

- **What AI can do:** Analyze PRD sections, propose task breakdown, surface cross-cutting concerns (auth, logging, error handling, observability), identify dependency chains.
- **What humans do:** Validate decomposition. Adjust granularity. Confirm dependencies.

#### D2. Foundation/Scaffolding Identification

What must exist before feature work begins? Repository setup, CI/CD, base dependencies, project structure, convention layer.

The plan for scaffolding is identified here as part of upstream activities. The actual execution of scaffolding is a task in the first iteration. For example: "I have a cookiecutter template that will scaffold the React project the way I want" — that decision is captured here, but running the template is iteration 1 work.

- **What AI can do:** Determine foundation needs from architecture + stack selection. Reference team conventions for scaffolding decisions if they exist. Propose scaffolding tasks.
- **What humans do:** Decide template vs AI-generated scaffold. Confirm foundation scope.

#### D3. Initial Task Breakdown (First 2-3 Iterations Only)

Convert tasks into executable specs (features) or tasks (infrastructure). Rough size estimates (T-shirt sizing, not hours). **Only plan the first 2-3 iterations** — not the entire product. Later iterations will be planned as the team learns.

- **What AI can do:** Draft issues with acceptance criteria. Analyze codebase for complexity indicators. Group into iterations.
- **What humans do:** Effort estimation. Priority within iterations. Capacity assessment.

#### Technical Guidance in Early Executable Specs

For greenfield projects, the technical guidance in executable specs will necessarily be loose at first. Only high-level architecture exists at this point — there are no established codebase patterns to reference. This is expected and fine.

Early technical guidance might say: "Use the authentication pattern described in the architecture doc" rather than "Follow the auth middleware pattern in `src/middleware/auth.ts`." As the codebase develops through early iterations, later executable specs can reference actual established patterns. The technical guidance gets more specific as the product matures.

The key: developers and their AI assistants can always deviate from technical guidance when they discover it won't work. When they deviate, the deviation should be captured (see [Phase E: Keeping Artifacts Honest](#phase-e-keeping-artifacts-honest)) — this is how the architecture evolves honestly rather than silently drifting.

#### D4. Iteration Goal Definition

What does "done" look like for iteration 1? Iteration 2?

- **What AI can do:** Propose iteration goals based on task dependencies. Suggest a "walking skeleton" approach for iteration 1 — minimal end-to-end functionality that proves the architecture works.
- **What humans do:** Approve goals. Ensure alignment with business priorities.

#### D5. Issue Creation

Create actual issues in the configured tracker.

- **What AI can do:** Create issues with proper structure, acceptance criteria, and links back to PRD and architecture docs. Features become executable specs, infrastructure becomes tasks.
- **What humans do:** Approve before creation.

**What goes wrong if this phase is done poorly:** Tasks are too large to estimate or too vague to implement. Dependencies aren't identified, causing blocking chains mid-iteration. First iteration doesn't deliver anything usable end-to-end. Cross-cutting concerns (auth, logging) are forgotten and retrofitted painfully.

#### Iteration Plan Quality Criteria

A good iteration plan:
- Tasks are small enough to estimate and build within an iteration
- Dependencies between tasks are identified and ordered
- First iteration delivers end-to-end value (walking skeleton)
- Cross-cutting concerns (auth, logging, error handling, observability) are accounted for
- Each task traces back to a PRD requirement or architecture decision
- Only the first 2-3 iterations are planned in detail (incremental planning)

---

### Phase E: Keeping Artifacts Honest

**Why this phase matters:** Artifacts that aren't maintained become lies. Within weeks of baselining a PRD, development reveals new insights, scope shifts, and unforeseen constraints. If the artifacts aren't updated, they describe a product that no one is building. New team members who read them are actively misled.

But here's the reality: **nobody maintains artifacts as a separate activity.** If updating docs requires a deliberate ceremony — "let's get together and review our artifacts" — it won't happen. The only artifact maintenance that actually happens is maintenance that's built into the flow of development itself.

#### The Primary Mechanism: In-the-Flow Decision Capture

Artifact updates must happen as a natural part of the build workflow, not as a separate activity. The critical trigger point is **issue completion** — the moment when the delta between "what was planned" and "what actually happened" is freshest in context.

**What should happen at issue completion (in addition to existing validation):**

1. **Deviation review** — AI surfaces what changed from the original plan during planning or implementation. "The plan said use WebSocket for real-time updates, but during implementation you switched to Server-Sent Events. The tracker issue still says WebSocket."

2. **Developer assesses significance** — Some deviations are trivial implementation details. Some are significant: a requirement was clarified through a conversation with a stakeholder, an architecture decision changed due to a technical constraint, a feature works differently than originally specified.

3. **Significant deviations get captured where they belong** — The AI knows the project's artifact map and routes updates to the right place:
   - **Tracker issue update** — if the feature works differently than the issue described, update the issue to reflect what was actually built
   - **New or updated ADR** — if an architecture decision changed (e.g., switched databases, changed API approach), capture the new decision with context and rationale
   - **Architecture doc update** — if a pattern or component changed significantly
   - **PRD update** — if a requirement changed or scope shifted during the active initiative
   - The developer doesn't have to figure out WHERE each update goes — the AI knows the artifact map and proposes the routing

4. **Developer confirms or dismisses** — Quick decision for each flagged deviation. "Yes, update the issue." "Yes, create an ADR for the database change." "No, that's a minor implementation detail, skip it."

**Why issue completion is the right trigger:**
- The context is freshest — the developer just lived through the decisions
- It's already a natural pause point in the build workflow
- It adds the RIGHT friction — small cost per issue, massive value over time
- Trying to reconstruct these decisions later (in a separate ceremony) is far more expensive and less accurate

#### What This Replaces

This in-the-flow pattern replaces the traditional "periodic artifact review" model. Instead of:
- Scheduling time to review artifacts (which gets skipped)
- Trying to remember what changed (which fails)
- Updating everything at once (which is overwhelming)

You get:
- Small, incremental updates at every issue completion
- Decisions captured with full context while they're fresh
- Artifacts that stay honest because maintenance is a byproduct of development, not a separate chore

#### Artifact Shelf Life

Not all artifacts live forever. Understanding when artifacts become historical context (valuable for reference but no longer the source of truth) prevents the trap of maintaining stale documents indefinitely.

| Artifact | Active Life | Becomes Historical When | Source of Truth After |
|----------|-------------|------------------------|---------------------|
| **Problem Statement** | During problem framing and requirements | PRD is baselined | The PRD itself |
| **PRD** | During the initiative it was created for | Initiative is delivered | The product (codebase, tests, deployed behavior) + issue history |
| **Architecture Doc** | While the system follows this architecture | Architecture evolves significantly (major refactor, rewrite) | The codebase + ADR history |
| **ADRs** | As long as the decision is in effect | Decision is superseded (new ADR references old) | The superseding ADR |
| **Iteration Plan** | During the iteration | Iteration is completed | Completed issues in tracker |

**Key insight:** The PRD does NOT become a running tally of every feature over the product's lifetime. It's tied to its initiative. Future features get their own scoping. This avoids a DRY violation where the same requirements exist in the PRD AND in individual executable specs — when they diverge, the PRD lies.

#### Cross-Artifact Consistency (Between Iterations)

Between iterations — when planning the next batch of work — is a natural point for a broader consistency check:

- Does the PRD still reflect what we're building, or has scope shifted?
- Does the architecture doc still describe the system, or have in-the-flow ADRs changed the picture?
- Are there tracker issues that no longer make sense given what we've learned?

This is a lighter version of what the in-the-flow mechanism handles at the issue level. It catches anything that slipped through — decisions that were too small to flag at issue completion but collectively represent drift.

- **What AI can do:** Compare artifacts, flag inconsistencies, present as a delta report — read-only, shows facts. "PRD says real-time updates, but ADR-007 changed to batch processing." "Three issues reference a component that was renamed."
- **What humans do:** Decide what to do about each inconsistency.

---

### Non-Linear Entry: Phases Are Not Mandatory Steps

Teams don't always follow the linear path A → B → C → D. Common real-world entry points:

| Scenario | Where Team Enters |
|----------|------------------|
| "We have a rough idea, help us flesh it out" | Phase A |
| "We already know what to build, here's our spec" | Phase B (import and assess existing PRD) |
| "We have requirements, need architecture help" | Phase C |
| "We know everything, just need to break it into issues" | Phase D |
| "We've been building for a while but our docs are stale" | Phase E (consistency check) |
| "We have an existing PRD in Google Docs" | Phase B (import, assess against template, fill gaps) |
| "We tried this before and shelved it — here's what we had" | Phase A (prior art) then assess what's reusable |

Each phase should check for the existence of prior-phase artifacts and use what exists. If the PRD exists, the architecture phase should find it and build on it. If it doesn't exist, the architecture phase should ask for the information it needs directly. **No phase should refuse to work because a prior phase wasn't completed.**

---

## Part 2: Capabilities Required for the Artifact Lifecycle

The upstream activities produce artifacts (problem statements, PRDs, architecture docs, ADRs, iteration plans). These artifacts need to be stored, searched, updated, and compared over time. Different documentation backends provide different levels of support for these needs.

### Required Capabilities

| Capability | Why It's Needed | Supported By |
|------------|----------------|--------------|
| **Store and retrieve artifacts** | Basic requirement — artifacts need a persistent, findable home | All backends (Confluence, Google Drive, RAG Memory, local files) |
| **Search across stored artifacts** | Prior art discovery (A2), finding related requirements, locating past decisions | All backends — with varying quality (keyword vs semantic search) |
| **Update artifacts with change tracking** | Artifacts evolve during active initiatives. Need to know what changed and when. | Confluence (page versioning), RAG Memory (change history), Google Drive (version history), local files (git history) |
| **Track artifact evolution over time** | "How has the PRD changed since we baselined it?" "When did the architecture change?" | RAG Memory (temporal queries), Confluence (page version comparison), limited in others |
| **Discover connections between artifacts** | "What relates this architecture decision to that PRD section?" Cross-artifact traceability. | RAG Memory (automatic relationship discovery), all others (AI reads and compares manually) |
| **Cross-artifact consistency checking** | Detecting drift between PRD, architecture, and tasks (Phase E) | All backends (by reading and comparing), RAG Memory (automatic relationship + temporal drift detection) |
| **Accept scattered multi-source input** | Requirements are never in one place (Phase B1). Must pull from multiple systems in a single effort. | All backends can be searched. Multiple backends must be searchable simultaneously. |
| **In-the-flow artifact updates from the build workflow** | When issue completion triggers a deviation review, the AI must be able to update artifacts in whatever backend they're stored in. | All backends must support updates from within the build workflow context. |

### Backend-Agnostic with Graceful Enhancement

The upstream activities must work with ANY configured backend. A team using only Google Drive gets full functionality for all phases. A team using RAG Memory gets additional capabilities (temporal evolution tracking, automatic relationship discovery) as a bonus — but the core activities never depend on a specific backend.

When NO documentation backend is configured, artifacts should still be manageable locally (version-controlled files in the repository).

### Artifact Discoverability Across Phases

A critical capability: downstream activities must be able to find artifacts that upstream activities produced. When architecture work begins, it needs to find the PRD. When decomposition begins, it needs both. When the build workflow's deviation review runs at issue completion, it needs to know where the architecture doc and ADRs live.

This requires some mechanism for recording where artifacts are stored and making that information accessible across all activities — both upstream phases and the build workflow. The specific mechanism is a design concern — the requirement is that artifacts produced in any phase are findable by any subsequent activity regardless of which backend they're stored in.

---

## Part 3: Decisions

Requirements-level questions that have been answered.

### D1. Where should product artifacts live by default?

**Decision:** Local project directory is ALWAYS an option, even when documentation backends are available. When the user begins upstream activities, present ALL discovered options (any configured backends + local) and let them choose. If no backends are found, explicitly inform the user: "I don't find any backend systems configured. Would you like to store locally, or configure a backend first?"

### D2. How customizable should artifact templates be?

**Decision:** Templates with optional sections. The PRD template has 10 sections, but teams can mark any section N/A with rationale. Not every project needs all sections. This balances consistency (everyone starts from the same template) with flexibility (teams skip what doesn't apply).

### D3. Is scaffolding part of upstream activities or a separate concern?

**Decision:** Both. Upstream identifies WHAT scaffolding is needed — the plan, the decisions, the tools (e.g., "we'll use a cookiecutter template for the React project structure"). The actual execution of scaffolding is a task in the first iteration. The upstream activity captures the scaffolding plan; the build workflow executes it.

### D4. How should artifacts scope to repositories?

**Decision:** Must be flexible enough to handle ALL scenarios — no single answer:
- **No repository exists yet** — artifacts live in the configured doc backend or local directory, independent of any repo
- **Single project repository** — one set of artifacts scoped to the repo
- **Monorepo with multiple projects** — per-project artifact scoping within the monorepo

The system must support all three without forcing teams into one model.

### D5. How should multi-source ingestion feel in a CLI context?

**Decision:** Combination approach:
1. Proactive scan — search configured backends for anything related to the topic
2. Present findings to the user
3. Ask if there's more to add — user provides additional links, paths, or pasted text
4. Reflect everything found — show the complete set of gathered material
5. Confirm — user approves the input set before assessment begins

This reduces manual pointing when docs are already in configured systems, while still allowing the user to add material the AI can't find on its own.

### D6. How detailed should gap assessments be?

**Decision:** Adaptive. Section-level for completely missing sections ("Section 4: Functional Requirements is missing entirely"), sub-section level for partial sections ("Section 4 exists but is missing acceptance criteria for 3 of 7 features"). The depth of assessment matches the depth of what exists.

---

## Part 4: Scope Boundaries

### Explicitly In Scope

- Problem framing and validation (Phase A)
- Requirements gathering, organization, and PRD creation (Phase B)
- Architecture and technical design (Phase C)
- Work decomposition and iteration planning (Phase D)
- In-the-flow artifact maintenance during active initiatives (Phase E)
- Multi-source ingestion from any configured backend
- Connection to the existing build workflow — Phase D produces issues, Phase E's deviation review integrates with issue completion

### Explicitly Out of Scope

- **Market research** — excluded by decision
- **Code review** — separate enhancement
- **Bug workflow** — separate enhancement
- **Release management** — separate enhancement
- **UI mockups/wireframes** — existing capability handles this
- **Design/architecture of the solution** — this document is requirements only; how to support these activities is a separate artifact

---

## Verification: Is This Requirements Document Complete?

1. Every upstream activity is described: what it is, why it matters, what perspectives are needed, what artifact it produces
2. Artifact quality criteria are defined for each phase output
3. Failure modes are articulated: what goes wrong when each phase is skipped or done poorly
4. The "for whom" reflects cross-functional reality: perspectives, team sizes, project contexts — not siloed roles
5. Existing material workflows are primary, not afterthoughts
6. Non-linear entry is explicitly supported
7. In-the-flow artifact updates are a first-class requirement, with issue completion as the primary trigger
8. Artifact shelf life is defined — PRDs are tied to initiatives, ADRs outlive PRDs, nothing is maintained forever
9. Backend capability requirements are stated without mandating specific backends
10. Decisions are recorded with rationale
11. Scope boundaries are explicit
12. Zero implementation details — no skill names, no primitive selection, no file paths, no tool references
