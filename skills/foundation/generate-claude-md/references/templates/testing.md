# Testing Rules Template

Generate `.claude/rules/testing.md` using this structure. Only include sections with actual rules.

---

```markdown
# Testing

## Framework

- {stack}: {framework} (e.g., "Frontend: Vitest", "Backend: pytest")
- E2E: {tool, if any} (e.g., "Playwright")

## Running Tests

```bash
# All tests
{command}

# Single file
{command}

# Watch mode
{command}

# Coverage
{command}
```

## Test Organization

- Location: {rule, e.g., "Colocated — `Foo.test.ts` next to `Foo.ts`"}
- Naming: {rule, e.g., "`*.test.ts` for unit, `*.spec.ts` for integration"}

## Coverage

- Target: {threshold or philosophy, e.g., "80% for new code" or "Cover critical paths"}
- {Enforcement, e.g., "CI fails below 80%"}

## Philosophy

- {Approach, e.g., "Test behavior, not implementation details"}
- {Balance, e.g., "Heavy unit tests, light integration, minimal E2E"}

## Mocking

- Approach: {rule, e.g., "Mock external services only — no mocking internal modules"}
- {Specific patterns, e.g., "Use MSW for API mocking in frontend tests"}

## Test Data

- {Strategy, e.g., "Use factories for test data, never hardcode IDs"}
```

---

## Guidelines

- Include the actual test commands — Claude needs the exact invocations.
- "Test behavior, not implementation" is worth stating if that's the team's philosophy.
- Mocking rules prevent common over-mocking problems.
