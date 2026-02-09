# Repo Analysis Guide

Reference for the generate-claude-md skill. Defines what to look for when analyzing a repository.

---

## Package Files — Stack Detection

| File | Ecosystem | Extract |
|------|-----------|---------|
| `package.json` | Node.js/JS/TS | `dependencies`, `devDependencies`, `scripts`, `engines` |
| `pyproject.toml` | Python | `[project.dependencies]`, `[tool.*]` sections, scripts |
| `requirements.txt` | Python | Dependencies list |
| `Cargo.toml` | Rust | `[dependencies]`, `[dev-dependencies]`, edition |
| `go.mod` | Go | Module path, Go version, dependencies |
| `pom.xml` | Java/Maven | `<dependencies>`, `<build>` plugins |
| `build.gradle` | Java/Gradle | Dependencies, plugins, tasks |
| `Gemfile` | Ruby | Gems, groups |
| `composer.json` | PHP | Dependencies, scripts, autoload |

**Key framework detection from dependencies:**

| Dependency | Framework |
|-----------|-----------|
| `react`, `react-dom` | React |
| `next` | Next.js |
| `vue` | Vue.js |
| `@angular/core` | Angular |
| `svelte` | Svelte |
| `express` | Express.js |
| `fastify` | Fastify |
| `fastapi` | FastAPI |
| `django` | Django |
| `flask` | Flask |
| `gin-gonic/gin` | Gin (Go) |

---

## Config Files — Convention Detection

| File(s) | Convention | Extract |
|---------|-----------|---------|
| `.prettierrc*`, `prettier.config.*` | Formatter (Prettier) | Config options |
| `.eslintrc*`, `eslint.config.*` | Linter (ESLint) | Rules, extends, plugins |
| `biome.json` | Formatter + Linter (Biome) | Rules |
| `tsconfig.json` | TypeScript config | `strict`, `target`, `module`, paths |
| `.editorconfig` | Editor settings | Indent style/size, line endings |
| `ruff.toml`, `pyproject.toml [tool.ruff]` | Linter (Ruff/Python) | Rules, select/ignore |
| `pyproject.toml [tool.black]` | Formatter (Black) | Config options |
| `pyproject.toml [tool.mypy]` | Type checker (Python) | Strictness |
| `.golangci.yml` | Linter (Go) | Enabled linters, settings |
| `rustfmt.toml` | Formatter (Rust) | Config options |
| `.stylelintrc*` | CSS linter | Rules |

---

## CI/CD — Build/Test Command Extraction

| File(s) | Platform | Look For |
|---------|----------|----------|
| `.github/workflows/*.yml` | GitHub Actions | `run:` steps, especially test/build/lint |
| `.gitlab-ci.yml` | GitLab CI | `script:` sections per stage |
| `Jenkinsfile` | Jenkins | `sh` steps |
| `.circleci/config.yml` | CircleCI | `run:` commands |
| `Makefile` | Make | Target names and commands |
| `Taskfile.yml` | Task | Task definitions |
| `justfile` | Just | Recipe definitions |

**Extract:** The actual commands used for build, test, lint, and deploy.

---

## Directory Structure — Architecture Detection

| Pattern | Indicates |
|---------|-----------|
| `src/` single directory | Standard single-project layout |
| `packages/`, `apps/` | Monorepo |
| `src/features/` or `src/modules/` | Feature-based organization |
| `src/components/`, `src/pages/` | React/frontend app |
| `src/routes/`, `src/handlers/` | Backend API |
| `cmd/`, `internal/`, `pkg/` | Go project structure |
| `src/`, `tests/` at root | Rust/Python standard |
| `migrations/` | Database with migrations |
| `prisma/` | Prisma ORM |
| `docker/`, `deploy/`, `infra/` | Deployment infrastructure |

---

## Existing AI Config — Migration

| File | Tool | Action |
|------|------|--------|
| `.cursorrules` | Cursor | Read content, extract relevant rules into `.claude/rules/` |
| `.github/copilot-instructions.md` | GitHub Copilot | Read content, adapt rules for Claude |
| `.aider*` | Aider | Check for relevant conventions |
| Existing `CLAUDE.md` | Claude Code | Preserve and restructure into lean root + rules files |

When migrating from other AI config:
- Keep rules that are universal (coding standards, architecture decisions)
- Skip rules specific to the other tool's behavior
- Adapt terminology (e.g., Cursor-specific instructions → Claude-compatible)

---

## Git History — Pattern Detection

```bash
# Recent commit messages — detect format
git log --oneline -20

# Branch names — detect naming pattern
git branch -a | head -20

# Recent contributors
git shortlog -sn --since="3 months ago" | head -10
```

**Infer from commit messages:**
- Conventional Commits? (`feat:`, `fix:`, `chore:`)
- Issue references? (`JIRA-123`, `#456`, `gitlab.com/.../issues/789`)
- Freeform?

**Infer from branches:**
- Naming pattern (feature/, feat/, fix/, hotfix/)
- Long-lived branches (develop, staging, release/)
- Trunk-based (only main + short-lived branches)
