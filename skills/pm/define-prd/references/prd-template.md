# PRD Template

Reference template for the pm/define-prd skill. 10 standard sections — all optional (teams can mark any section N/A with rationale). Quality criteria embedded per section.

---

## 1. Executive Summary / Problem Statement

**What to capture:** The problem being solved, who it's for, and why it matters. Link to problem statement if one was created in pm/discover.

**Quality check:**
- Concise (1 paragraph)
- States the problem, not the solution
- Clear value proposition

---

## 2. Goals & Success Metrics

**What to capture:** Measurable outcomes that define success. How will we know this worked?

**Quality check:**
- Each goal is measurable (number, percentage, qualitative threshold)
- Metrics are observable (can actually be measured with available tools)
- Goals relate back to the problem statement
- Success criteria don't describe features — they describe outcomes

---

## 3. Target Users / Personas

**What to capture:** Who will use this? What are their key characteristics, needs, and context?

**Quality check:**
- Specific user types, not "everyone"
- Each persona has: role, goals, pain points, context of use
- Distinguishes primary from secondary users
- Optional section if the audience is obvious from context (mark N/A with rationale)

---

## 4. Functional Requirements

**What to capture:** What the system must DO, organized by feature area. Each requirement has acceptance criteria.

**Quality check:**
- Organized by feature area or theme
- Each requirement states WHAT, not HOW
- Each requirement has testable acceptance criteria
- Acceptance criteria describe outcomes, not implementation steps
- Priority indicated (must-have / should-have / nice-to-have)
- Conflicts between requirements identified and resolved

**Format per requirement:**

```
### FR-[number]: [Requirement Title]

**Priority:** Must-have | Should-have | Nice-to-have

**Description:** [What the system must do]

**Acceptance Criteria:**
- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]
```

---

## 5. Non-Functional Requirements

**What to capture:** Quality attributes — performance, security, accessibility, scalability, compliance.

**Quality check:**
- Specific and measurable where possible ("page loads in < 2s", not "fast")
- Covers: performance, security, accessibility, scalability, reliability
- Compliance requirements identified (GDPR, SOC2, etc.) or explicitly N/A
- Realistic given constraints

---

## 6. Constraints

**What to capture:** Fixed boundaries — timeline, budget, team size, technical constraints, regulatory requirements.

**Quality check:**
- Hard constraints clearly distinguished from soft preferences
- Technical constraints reference specific technologies or systems
- Timeline is realistic given scope and team
- Budget is at least order-of-magnitude estimated, or explicitly unconstrained

---

## 7. Out of Scope

**What to capture:** What this initiative explicitly does NOT include. Things people might assume are included.

**Quality check:**
- Lists specific things, not vague exclusions
- Each exclusion has brief rationale (why not now?)
- Covers likely assumptions people will make
- Any out-of-scope items that relate to in-scope features are called out

---

## 8. Dependencies

**What to capture:** External systems, other teams, third-party services, or prerequisites that this work depends on.

**Quality check:**
- Each dependency has: what, who owns it, status, risk if unavailable
- Internal dependencies (other team's work) have timeline alignment
- External dependencies (third-party APIs, services) have fallback plans
- Infrastructure dependencies identified

---

## 9. Open Questions / Risks

**What to capture:** What we don't know yet. What could go wrong. What decisions are deferred.

**Quality check:**
- Questions are specific and actionable
- Each question identifies who might answer it
- Risks have: description, likelihood, impact, mitigation
- Deferred decisions have a "decide by" trigger or date

---

## 10. Appendix

**What to capture:** Supporting material — research, data, references, related documents.

**Quality check:**
- Links to source material are working
- Research findings summarized (not just raw links)
- Related documents identified and accessible
- Optional section — mark N/A if no supporting material exists

---

## Overall PRD Quality Criteria

A complete PRD:
- Has all relevant sections addressed (or explicitly marked N/A with rationale)
- Contains measurable, testable acceptance criteria
- Describes WHAT to build, not HOW to build it
- Has conflicts between sources resolved (not hidden)
- Flags open questions explicitly rather than hiding assumptions
- Has been reviewed and approved by relevant people
- Is stored somewhere findable with status tracked in the project manifest

## PRD Shelf Life

The PRD is tied to the INITIATIVE, not the product's lifetime. Once the initiative is delivered, the PRD becomes historical — the product itself (codebase, tests, deployed behavior) becomes the source of truth. Future features get their own scoping. During the active initiative, update the PRD when significant scope or requirement changes happen.
