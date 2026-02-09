# Git Workflow Rules Template

Generate `.claude/rules/git-workflow.md` using this structure. Only include sections with actual rules.

---

```markdown
# Git Workflow

## Branching

- Strategy: {e.g., "Trunk-based development — short-lived feature branches off main"}
- Branch naming: `{pattern}` (e.g., `feat/JIRA-123-short-description`, `fix/description`)
- {Any branch rules, e.g., "Never push directly to main"}

## Commits

- Format: {e.g., "Conventional Commits — `type(scope): description`"}
- Types: {e.g., "feat, fix, chore, docs, refactor, test"}
- {Rules, e.g., "Keep commits atomic — one logical change per commit"}

## Pull Requests / Merge Requests

- {Size rule, e.g., "Keep PRs under 300 lines when possible"}
- {Review rule, e.g., "Require 1 approval before merge"}
- {CI rule, e.g., "All checks must pass before merge"}
- Merge strategy: {e.g., "Squash and merge to main"}
- {Template, e.g., "Use PR template — include summary, test plan, and issue reference"}

## Releases

- {Process, e.g., "Tag main with semver — CI auto-publishes on tag"}
- {Versioning, e.g., "Follow semver strictly"}
```

---

## Guidelines

- Branch naming patterns help Claude create correctly named branches.
- Commit format rules help Claude write proper commit messages.
- PR size guidance affects how Claude breaks up work.
