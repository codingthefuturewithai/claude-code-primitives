# ADR Template

Reference template for Architecture Decision Records. Use this for every significant technical decision during architecture design or development.

---

## ADR-[NUMBER]: [Decision Title]

**Date:** [YYYY-MM-DD]

**Status:** Proposed | Accepted | Superseded by ADR-[X] | Deprecated

**Supersedes:** ADR-[Y] (if applicable)

---

### Context

What is the issue that we're seeing that is motivating this decision? What forces are at play?

**Quality check:**
- Describes the situation neutrally
- References specific requirements or constraints (link to PRD section if relevant)
- Explains why a decision is needed now

---

### Options Considered

| Option | Pros | Cons |
|--------|------|------|
| Option A: [name] | [advantages] | [disadvantages] |
| Option B: [name] | [advantages] | [disadvantages] |
| Option C: [name] | [advantages] | [disadvantages] |

**Quality check:**
- At least 2 options considered (even if the choice was obvious, document why)
- Pros and cons are specific, not vague
- If team conventions recommend an option, note that

---

### Decision

We will use [option] because [primary reason].

**Quality check:**
- States the decision clearly
- Links primary reason to the context
- Brief — detail is in the options table

---

### Rationale

Why this option was chosen over the alternatives. What trade-offs were accepted.

**Quality check:**
- Addresses the key differentiators between options
- Acknowledges what's being given up
- References any constraints that drove the decision

---

### Consequences

What becomes easier or more difficult because of this decision?

**Positive:**
- [What this enables]

**Negative:**
- [What this costs or constrains]

**Neutral:**
- [What changes but isn't clearly better or worse]

**Quality check:**
- Consequences are specific and actionable
- Negative consequences are honest
- Future work implied by this decision is identified

---

## ADR Shelf Life

ADRs outlive the PRD. An architecture decision persists as long as the system uses that decision. When a decision is superseded, a new ADR references the old one ("supersedes ADR-[X]") so the evolution is traceable. ADRs are the longest-lived upstream artifacts.
