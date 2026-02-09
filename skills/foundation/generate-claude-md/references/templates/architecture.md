# Architecture Rules Template

Generate `.claude/rules/architecture.md` using this structure. Only include sections with actual rules and decisions.

---

```markdown
# Architecture

## Patterns

- {Primary pattern, e.g., "Clean architecture with hexagonal ports/adapters"}
- {Key rule, e.g., "Domain logic must not import from infrastructure layer"}
- {Dependency rule, e.g., "Dependencies point inward — outer layers depend on inner"}

## Project Structure

- {Structure type, e.g., "Monorepo using Turborepo"}
- {Organization, e.g., "Feature-based modules under src/features/"}
- {Key constraint, e.g., "Shared code goes in packages/shared — no cross-feature imports"}

## API Design

- Style: {e.g., "REST with OpenAPI specs"}
- {Conventions, e.g., "Use plural nouns for resources — /users, /orders"}
- {Versioning, e.g., "API versioned via URL path — /api/v1/"}

## Error Handling

- {Strategy, e.g., "Global error handler catches all unhandled errors"}
- {Pattern, e.g., "Use custom error classes extending BaseError"}
- {Logging, e.g., "All errors logged with structured context — no silent catches"}

## Data Layer

- {ORM/query, e.g., "Use Prisma for all database access"}
- {Migration, e.g., "Migrations via Prisma Migrate — never modify migration files manually"}
- {Patterns, e.g., "Repository pattern for data access — no direct DB calls in handlers"}

## Environment & Config

- {Management, e.g., "Use dotenv for local, AWS SSM for production"}
- {Validation, e.g., "Validate all env vars at startup with Zod schema"}
- {Secrets, e.g., "Never commit secrets — use .env.example as template"}

## Dependencies

- {Policy, e.g., "Pin exact versions — use Renovate for automated updates"}
- {Approval, e.g., "New dependencies require team discussion for anything >10KB"}

## Key Decisions

{Document significant architectural decisions that Claude should know about:}
- {Decision, e.g., "Chose SQLite over PostgreSQL for local-first architecture"}
- {Decision, e.g., "Using server components by default — client components only when needed"}
```

---

## Guidelines

- Architecture rules prevent Claude from making structural mistakes.
- "Key Decisions" captures the WHY behind choices — helps Claude make consistent decisions.
- Migration rules are critical — Claude modifying migration files can break databases.
- Only include decisions that affect how Claude should write code. Skip internal team process details.
