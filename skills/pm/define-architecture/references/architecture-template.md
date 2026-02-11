# Architecture Document Template

Reference template for the pm/define-architecture skill. Quality criteria embedded per section.

---

## 1. Overview

**What to capture:** High-level summary of the architectural approach. What system is being built (or extended) and what architectural style/pattern is being followed.

**Quality check:**
- Links to or references the PRD
- Identifies whether this is greenfield or brownfield
- States the primary architectural pattern (monolith, microservices, serverless, etc.)

---

## 2. System Context

**What to capture:** How this system fits in the broader ecosystem. External systems, users, integrations.

**Quality check:**
- External systems and their interfaces identified
- Data flows between systems described
- Authentication/authorization boundaries clear
- Diagrams encouraged (Mermaid format)

---

## 3. Technology Stack

**What to capture:** Languages, frameworks, databases, infrastructure choices. For brownfield: what exists vs what's being added.

**Quality check:**
- Each choice has rationale (even if brief)
- For brownfield: existing stack documented, changes justified
- If team conventions exist, alignment or deviation noted
- Version requirements specified where they matter

---

## 4. Component Architecture

**What to capture:** Major components/services, their responsibilities, and how they interact.

**Quality check:**
- Each component has: name, responsibility, interfaces, dependencies
- Component boundaries are clean (no overlapping responsibilities)
- Communication patterns between components defined (sync/async, protocols)
- Diagrams encouraged (Mermaid format)

---

## 5. Data Model

**What to capture:** Primary data entities, relationships, storage decisions.

**Quality check:**
- Core entities identified with key attributes
- Relationships defined (1:1, 1:N, M:N)
- Storage technology per entity group justified
- Data migration strategy if brownfield
- Diagrams encouraged (Mermaid ER format)

---

## 6. API Design

**What to capture:** External and internal APIs — style, key endpoints/operations, contracts.

**Quality check:**
- API style chosen and justified (REST, GraphQL, gRPC, etc.)
- Key endpoints/operations listed with purpose
- Authentication and authorization approach defined
- Error handling patterns established
- Versioning strategy defined (or explicitly not needed)

---

## 7. Non-Functional Architecture

**What to capture:** How the architecture addresses non-functional requirements from the PRD.

**Quality check:**
- Performance: expected load, scaling strategy, caching approach
- Security: threat model, authentication, authorization, data protection
- Reliability: failure modes, recovery, redundancy
- Observability: logging, monitoring, alerting, tracing
- Each non-functional requirement from PRD has an architectural answer

---

## 8. Infrastructure & Deployment

**What to capture:** Where and how the system runs. CI/CD, environments, deployment strategy.

**Quality check:**
- Deployment target defined (cloud provider, regions, services)
- CI/CD pipeline described
- Environment strategy (dev, staging, prod)
- Infrastructure as code approach identified

---

## 9. Cross-Cutting Concerns

**What to capture:** Patterns that span multiple components — error handling, logging, configuration, feature flags.

**Quality check:**
- Error handling pattern defined (consistent across components)
- Logging strategy defined (format, levels, aggregation)
- Configuration management approach
- Feature flag strategy (if applicable)

---

## 10. Constraints & Trade-offs

**What to capture:** What was sacrificed and why. What won't scale. What was deferred.

**Quality check:**
- Trade-offs are honest (not just happy-path)
- Constraints from PRD acknowledged
- Technical debt taken on deliberately is documented
- Scalability limits identified with thresholds

---

## 11. ADR Index

**What to capture:** Links to Architecture Decision Records created during this design.

**Quality check:**
- Each significant decision has an ADR
- ADRs are numbered and linked
- Supersession chains are clear

---

## Overall Architecture Quality Criteria

A complete architecture document:
- Addresses all PRD functional requirements (traceable)
- Has architectural answers for non-functional requirements
- Documents key decisions as ADRs with context, alternatives, and rationale
- For brownfield: accounts for existing system constraints and integration points
- Acknowledges trade-offs honestly
- Defines components, data model, and integration points explicitly
- Has been reviewed by the people who will build it
