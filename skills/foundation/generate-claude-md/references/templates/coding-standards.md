# Coding Standards Rules Template

Generate `.claude/rules/coding-standards.md` using this structure. Only include sections with actual rules — skip anything that's just "use language defaults."

For monorepos with different standards per package, use path-scoping frontmatter.

---

```markdown
# Coding Standards

## Formatting

- Formatter: {tool} ({key config notes, e.g., "single quotes, trailing commas"})
- Run: `{format command}`
- {Any formatter-specific rules, e.g., "Always format before committing"}

## Linting

- Linter: {tool} ({strictness, e.g., "strict preset, zero warnings"})
- Run: `{lint command}`
- {Key custom rules if any}

## Type Checking

- Strictness: {strict/gradual/optional}
- {Specific type rules, e.g., "No `any` types except in test files"}

## Naming Conventions

{Only include if the team deviates from language defaults.}
- {convention}: {rule}

## Error Handling

- Approach: {philosophy, e.g., "Use Result types for expected failures, exceptions for unexpected"}
- {Specific patterns, e.g., "All API errors must include error code and message"}

## Import Organization

- {Rule, e.g., "Auto-sorted by ESLint import plugin"}
- {Grouping, e.g., "Group: stdlib, external, internal, relative"}
```

---

## Path-Scoped Example (Monorepo)

```markdown
---
paths:
  - "packages/frontend/**"
---

# Frontend Coding Standards

- Formatter: Prettier (single quotes, trailing commas, 100 char width)
- Linter: ESLint with strict TypeScript preset
- Type strictness: strict (no `any`)
```

```markdown
---
paths:
  - "packages/backend/**"
---

# Backend Coding Standards

- Formatter: Black (default config)
- Linter: Ruff (all rules enabled)
- Type strictness: strict (mypy --strict)
```

---

## Guidelines

- Write rules as **directives**, not descriptions. "Use X" not "The team uses X."
- Only include rules that **differ from defaults**. Claude knows standard conventions.
- If the team just uses the formatter/linter defaults with no customization, a single line is enough.
