# Root CLAUDE.md Template

Generate a lean CLAUDE.md (~60 lines max) using this structure. Replace placeholders with actual values from repo analysis. Remove sections that don't apply.

---

```markdown
# {Project Name}

{One-line description of what this project does.}

## Build & Run

{Include only commands that Claude can't guess from looking at package files.}

```bash
# Dev server
{command}

# Build
{command}

# Other common commands
{command}
```

## Test

```bash
# Run all tests
{command}

# Run specific test file
{command}

# Run with coverage
{command}
```

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `{path}/` | {brief description} |
| `{path}/` | {brief description} |
| `{path}/` | {brief description} |

## Important Notes

{Only include things Claude can't figure out from the code itself:}
{- Environment quirks}
{- Non-obvious setup steps}
{- Common gotchas}
{- Critical constraints}
```

---

## Guidelines

- **Target ~60 lines.** Every line is reprocessed with every message. Short = Claude follows it.
- **No coding standards, testing philosophy, git workflow, or architecture here.** Those go in `.claude/rules/`.
- **No file-by-file descriptions.** Claude can read the code.
- **No standard language conventions.** Claude already knows them.
- **No tutorials.** This is a reference, not a guide.
- **Include build/test commands** even if they're in package.json — Claude needs to know the exact invocation.
