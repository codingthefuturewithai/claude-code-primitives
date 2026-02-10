# Best Practices for CLAUDE.md and .claude/rules/

Best practices for creating effective Claude Code convention layer files, based on Claude Code's official documentation and practical experience.

---

## Claude Code's File Hierarchy

Claude Code loads instruction files from multiple levels, all additively. More specific levels win on conflict.

| Level | Location | Scope |
|-------|----------|-------|
| **Managed policy** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Org-wide, cannot be overridden |
| **Project** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared via git |
| **Project rules** | `./.claude/rules/*.md` | Modular, topic-specific, path-scopable |
| **User** | `~/.claude/CLAUDE.md` | Personal across all projects |
| **Local** | `./CLAUDE.local.md` | Personal per-project (gitignored) |
| **Auto memory** | `~/.claude/projects/<project>/memory/` | Claude's own persistent notes |

**Key behaviors:**
- Parent directory CLAUDE.md files load recursively up to the repo root
- Child directory CLAUDE.md files load on-demand when Claude reads files in those directories
- `@import` syntax allows referencing other files (max depth 5, truncated at 2000 lines)
- All levels are additive — Claude sees everything

**Implication:** In a monorepo project directory, root-level CLAUDE.md and .claude/rules/ content is already visible to Claude. Don't duplicate it at the project level.

---

## Root CLAUDE.md — Keep It Short

**Target: ~60 lines max.** Every line is reprocessed with every message Claude processes. Bloated files cause Claude to skim or ignore instructions.

### What to Include

- **Project name and one-line description**
- **Build, run, and test commands** — the exact invocations, even if they're in package.json. Claude needs to know `npm run test:run` not just "run tests."
- **Key directories** — brief table of what lives where
- **Important gotchas** — environment quirks, non-obvious setup, critical constraints
- **Environment variables** — if applicable

### What to Exclude

- **Standard language conventions** — Claude already knows them
- **File-by-file descriptions** — Claude can read the code
- **Tutorials or explanations** — this is a reference, not a guide
- **Coding standards, testing philosophy, git workflow, architecture** — those go in `.claude/rules/`
- **Anything that changes frequently** — keep CLAUDE.md stable

### Greenfield Repos

For new repos with little or no code, include what's known and use TODO markers for what will emerge:

```markdown
<!-- TODO: Update build commands after initial setup -->
<!-- TODO: Add key directories once project structure is established -->
```

---

## .claude/rules/ — Modular Rules

Use `.claude/rules/*.md` files for topic-specific rules. Benefits:

- Smaller files reduce merge conflicts
- Can be shared across projects via symlinks
- Support path-scoped rules via YAML frontmatter

### Common Topics

Not every repo needs all of these. Only create files for topics that have rules worth stating.

- **critical-rules.md** — things Claude MUST or MUST NOT do (permission gates, migration rules, things that could break production)
- **coding-standards.md** — formatter, linter, type strictness, naming conventions (only what differs from language defaults)
- **testing.md** — framework, commands, philosophy, coverage expectations
- **architecture.md** — patterns, key decisions and their reasoning, how to add common things, constraints

Create additional topic files only when the repo has something meaningful to say about that topic.

### Writing Style

- **Directives, not descriptions.** "Use X" not "The team uses X."
- **Only what differs from defaults.** Claude knows standard conventions for every major language and framework.
- **Focus on what Claude would get wrong without this context.** If Claude would naturally do the right thing, you don't need a rule for it.
- **Concise.** Rules files should be compact directives, not documentation or tutorials.

### Path-Scoped Rules (Monorepos)

Use YAML frontmatter to scope rules to specific paths:

```yaml
---
paths:
  - "packages/frontend/**"
---

# Frontend Coding Standards

- Formatter: Prettier (single quotes, trailing commas)
- Linter: ESLint with strict TypeScript preset
```

This is especially useful when different projects in a monorepo use different stacks or conventions.

---

## Monorepo Patterns

### At the Repo Root

- **CLAUDE.md**: Workspace overview, how to navigate, shared commands, what projects exist and how they relate
- **.claude/rules/**: Rules that apply to ALL projects (shared coding standards, commit format, etc.)

### At the Project Level

- **CLAUDE.md**: This project's specific build/test/run commands, key directories, and gotchas
- **.claude/rules/**: Project-specific rules (framework conventions, testing specifics) — use path-scoping

### Avoid

- **Don't duplicate root content at project level** — Claude loads parents recursively, so root rules are already visible
- **Don't put project-specific content at root** — it confuses work in other projects
- **Don't assume monorepo from subdirectories alone** — look for workspace config files (pnpm-workspace.yaml, lerna.json, nx.json, turbo.json, Cargo.toml with [workspace], go.work), multiple package files, or projects with their own CLAUDE.md

---

## Working with Existing Files

### Existing CLAUDE.md or .claude/rules/

- Read and understand them first — they represent the developer's current intent
- Don't assume they need replacing — they may be exactly right
- Propose targeted updates rather than wholesale replacement when improvements are clear
- If recommending a rewrite, explain specifically what improves

### Other AI Config Files

If the repo has `.cursorrules`, `.github/copilot-instructions.md`, or `.aider*` files:

- Read them for relevant rules worth preserving
- Keep universal rules (coding standards, architecture decisions)
- Skip instructions specific to the other tool's behavior
- Adapt terminology where needed

---

## Common Mistakes

1. **Overloading CLAUDE.md** — putting everything in one giant file instead of using .claude/rules/
2. **Restating the obvious** — writing rules Claude already follows by default
3. **Prescribing instead of documenting** — suggesting technologies or patterns the repo doesn't actually use
4. **Ignoring existing files** — proposing a fresh convention layer when one already exists and works
5. **Duplicating across levels** — repeating the same rules in both root and project CLAUDE.md in a monorepo
6. **Writing essays** — rules should be terse directives, not multi-paragraph explanations
7. **Recommending incompatible technologies** — suggesting Tailwind for a Mantine project, or similar conflicts
