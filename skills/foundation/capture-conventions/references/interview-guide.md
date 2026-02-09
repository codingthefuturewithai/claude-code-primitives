# Interview Guide — Question Bank by Project Type

Reference for the capture-conventions skill. Contains the full question bank organized by project type. Only ask sections relevant to the team's selected domains.

---

## Tech Stack Questions

### Frontend (Web Applications)

| Topic | Question | Common Options |
|-------|----------|---------------|
| Language | What language for frontend? | TypeScript, JavaScript |
| Framework | What frontend framework? | React, Vue, Angular, Svelte, Next.js, Nuxt, SvelteKit |
| Component library | UI component library? | Radix, shadcn/ui, Material UI, Ant Design, Chakra, custom, none |
| State management | State management approach? | React Context, Zustand, Redux, Jotai, Pinia, Vuex |
| CSS approach | How do you handle styling? | Tailwind, CSS Modules, styled-components, Sass, vanilla CSS |
| Build tool | Build tooling? | Vite, Webpack, Turbopack, esbuild |

### Backend / API Services

| Topic | Question | Common Options |
|-------|----------|---------------|
| Language | What language for backend? | TypeScript/Node, Python, Go, Rust, Java, Kotlin, C# |
| Framework | What backend framework? | Express, Fastify, Hono, FastAPI, Django, Flask, Spring, Gin, Axum |
| Database | Primary database? | PostgreSQL, MySQL, MongoDB, DynamoDB, SQLite, Redis |
| ORM/query | ORM or query layer? | Prisma, Drizzle, TypeORM, SQLAlchemy, GORM, Diesel, raw SQL |
| API style | API design style? | REST, GraphQL, gRPC, tRPC |
| Auth | Authentication approach? | JWT, session-based, OAuth2, API keys |

### Mobile Apps

| Topic | Question | Common Options |
|-------|----------|---------------|
| Approach | Mobile development approach? | React Native, Flutter, SwiftUI (iOS), Kotlin/Compose (Android), native |
| Shared code | Code sharing strategy? | Shared core library, fully cross-platform, fully native per platform |
| Navigation | Navigation library? | React Navigation, expo-router, GoRouter, UIKit |
| State | State management? | Redux, Zustand, Riverpod, Provider, SwiftUI @State |

### Data / ML

| Topic | Question | Common Options |
|-------|----------|---------------|
| Language | Primary language? | Python, R, Scala, Julia |
| ML framework | ML frameworks? | PyTorch, TensorFlow, scikit-learn, JAX, Hugging Face |
| Data processing | Data processing? | Pandas, Polars, Spark, Dask |
| Notebooks vs scripts | Development style? | Jupyter notebooks, Python scripts, mixed |
| Data storage | Where is data stored? | S3, GCS, BigQuery, Snowflake, Delta Lake, local |
| Experiment tracking | Experiment tracking? | MLflow, Weights & Biases, Neptune, none |

### DevOps / Infrastructure

| Topic | Question | Common Options |
|-------|----------|---------------|
| IaC tool | Infrastructure as Code? | Terraform, Pulumi, CloudFormation, CDK, Ansible |
| Cloud | Primary cloud provider? | AWS, GCP, Azure, multi-cloud |
| Container | Container orchestration? | Kubernetes, ECS, Docker Compose, Nomad, none |
| CI/CD | CI/CD platform? | GitHub Actions, GitLab CI, Jenkins, CircleCI, ArgoCD |
| Monitoring | Monitoring/observability? | Datadog, Grafana, Prometheus, CloudWatch, New Relic |

### CLI Tools / Developer Tooling

| Topic | Question | Common Options |
|-------|----------|---------------|
| Language | Primary language? | Rust, Go, Python, TypeScript/Node, Bash |
| CLI framework | CLI framework? | clap (Rust), cobra (Go), Click/Typer (Python), Commander (Node) |
| Distribution | How is it distributed? | Homebrew, npm, pip, cargo, binary releases, Docker |
| Config format | Config file format? | TOML, YAML, JSON, dotenv |

### Desktop Applications

| Topic | Question | Common Options |
|-------|----------|---------------|
| Framework | Desktop framework? | Electron, Tauri, SwiftUI, WPF/.NET, Qt, GTK |
| Language | Primary language? | TypeScript, Rust, Swift, C#, C++, Python |
| Packaging | How is it packaged? | DMG, MSI, AppImage, Snap, Flatpak, auto-updater |
| Cross-platform | Cross-platform strategy? | Single codebase, platform-specific UI, web-based |

### Libraries / SDKs

| Topic | Question | Common Options |
|-------|----------|---------------|
| Language | Primary language? | TypeScript, Python, Rust, Go, Java, multi-language |
| Package registry | Where is it published? | npm, PyPI, crates.io, Maven Central, NuGet |
| API design | API design philosophy? | Minimal surface area, batteries-included, builder pattern |
| Docs | Documentation approach? | README + API docs, docsite (Docusaurus/MkDocs), examples-first |
| Versioning | Versioning strategy? | Strict semver, CalVer, 0.x until stable |
| Backwards compat | Backwards compatibility policy? | Strict (no breaking changes), deprecation cycle, LTS branches |

### Embedded / IoT

| Topic | Question | Common Options |
|-------|----------|---------------|
| Language | Primary language? | C, C++, Rust, MicroPython, Arduino |
| Platform | Target platform? | ESP32, STM32, Raspberry Pi, Arduino, custom RTOS |
| Build system | Build system? | CMake, PlatformIO, Make, Cargo (embedded Rust) |
| Communication | Communication protocol? | MQTT, HTTP, BLE, Zigbee, LoRa, custom serial |

---

## Code Quality & Refactoring Questions

Frame these as "triggers for thinking" — not every team tracks these formally, and that's fine.

| Topic | Question | Common Options |
|-------|----------|---------------|
| File size | Do you have file/module size guidance? | ~300 lines target, ~500 lines max, no formal limit, "use judgment" |
| Function length | Preferred function/method length? | ~30 lines, "fits on one screen", no limit, "use judgment" |
| DRY threshold | When do you extract shared code? | Rule of three, never duplicate, extract early, use judgment per case |
| Dead code | How do you handle dead code? | Delete immediately, comment out with ticket, keep behind feature flag, no formal policy |
| Refactoring triggers | What triggers a refactoring pass? | Before adding features to messy code, during PR review, scheduled sprints, opportunistic, tech debt tickets |
| Complexity metrics | Do you track code complexity? | SonarQube/SonarCloud, CodeClimate, ESLint complexity rule, informal awareness, not tracked |
| Code smells | Any specific code smells the team watches for? | Long parameter lists, deeply nested logic, god classes, feature envy, no formal list |
| Tech debt tracking | How do you track tech debt? | Dedicated tickets/issues, TODO comments, tech debt register, informal, not tracked |

---

## Coding Standards Questions

| Topic | Question | Notes |
|-------|----------|-------|
| Style guide | Do you follow a published style guide? | Airbnb, Google, Standard, language defaults |
| Formatter | What code formatter? | Match to languages: Prettier (JS/TS), Black (Python), gofmt (Go), rustfmt (Rust) |
| Formatter config | Any notable formatter config? | E.g., "Prettier with single quotes and trailing commas" |
| Linter | What linter? | ESLint, Ruff, golangci-lint, Clippy |
| Linter strictness | How strict? | Warnings allowed, zero warnings, custom rule set |
| Type strictness | Type checking strictness? | Strict mode, gradual typing, optional |
| Naming | Naming convention deviations? | Any team-specific rules beyond language defaults |
| Imports | Import organization? | Auto-sorted, grouped (stdlib/external/internal), manual |
| Error handling | Error handling philosophy? | Result/Either types, exceptions with specific patterns, error codes |
| Comments | Comment expectations? | Only non-obvious logic, JSDoc/docstrings for public API, minimal |

---

## Documentation Standards Questions

Frame as "what does your team expect?" — some teams document extensively, others keep it minimal.

| Topic | Question | Common Options |
|-------|----------|---------------|
| README | What should every repo's README contain? | Setup instructions only, setup + architecture overview, comprehensive (setup + arch + API + contributing), minimal |
| API docs | Do you use a formal API spec format? | OpenAPI/Swagger, GraphQL schema + playground, AsyncAPI, auto-generated from code, no formal spec |
| API doc tooling | API documentation tooling? | Swagger UI, Redoc, Stoplight, Postman collections, none/manual |
| ADRs | Does the team write Architecture Decision Records? | Yes with template (MADR, etc.), informal design docs, only for major decisions, no |
| Changelog | How do you track changes for consumers? | CHANGELOG.md (Keep a Changelog), auto-generated from commits (conventional-changelog), release notes only, none |
| Code comments | What are your expectations for code comments? | Only non-obvious logic, JSDoc/docstrings for public API, minimal (code should be self-documenting), comprehensive |
| Inline docs | Do you use doc generation from code? | TypeDoc, Sphinx/autodoc, Godoc, Rustdoc, JSDoc site, no |
| Runbooks | Do you maintain operational runbooks? | Yes in wiki (Confluence, Notion), yes in repo (docs/), ad hoc incident notes, no |
| Onboarding | Is there a developer onboarding guide? | Yes comprehensive, yes basic setup guide, README covers it, no |
| Diagrams | Do you maintain architecture diagrams? | Yes (Mermaid, draw.io, Excalidraw), yes but often stale, no |

---

## Testing Questions

| Topic | Question | Notes |
|-------|----------|-------|
| Framework | Test framework per stack? | Jest, Vitest, pytest, Go testing, JUnit, etc. |
| Coverage target | Coverage requirements? | Percentage (e.g., 80%), or philosophy (e.g., "critical paths") |
| Philosophy | Testing philosophy? | TDD, test-after, test-critical-paths-only |
| Balance | Unit/integration/E2E balance? | E.g., "Heavy unit, light integration, minimal E2E" |
| File location | Where do test files go? | Colocated (`Foo.test.ts` next to `Foo.ts`), `__tests__/`, `tests/` root |
| Mocking | Mocking approach? | Minimal mocks, mock external services only, mock liberally |
| E2E tool | E2E testing tool? | Playwright, Cypress, Selenium, none |
| Test data | Test data strategy? | Factories, fixtures, builders, inline |

---

## Git & Workflow Questions

| Topic | Question | Notes |
|-------|----------|-------|
| Branching | Branching strategy? | Trunk-based, GitFlow, GitHub Flow, custom |
| Branch naming | Branch naming pattern? | `feat/JIRA-123-description`, `feature/description`, custom |
| Commits | Commit message format? | Conventional Commits, freeform, custom template |
| PR/MR size | Preferred PR/MR size? | Small (< 300 lines), medium, no preference |
| Reviews | Review requirements? | Number of approvals, specific reviewers, CODEOWNERS |
| Merge strategy | Merge strategy? | Squash, merge commit, rebase |
| CI requirements | What must pass before merge? | Tests, lint, type check, security scan, coverage threshold |
| Release | Release process? | Git tags, release branches, automated from main, manual |

---

## Architecture Questions

| Topic | Question | Notes |
|-------|----------|-------|
| Repo structure | Monorepo or polyrepo? | Monorepo (Nx, Turborepo, Rush), polyrepo, hybrid |
| Patterns | Preferred architecture patterns? | Clean architecture, hexagonal, MVC, CQRS, microservices |
| Error handling | Error handling strategy? | Global handler, per-layer, error boundaries, Result types |
| Logging | Logging approach? | Structured JSON, log levels, specific library |
| Env management | Environment/secrets management? | dotenv, Vault, AWS SSM, GCP Secret Manager |
| Dependencies | Dependency management? | Pin exact versions, allow ranges, automated updates (Dependabot/Renovate) |
| API versioning | API versioning strategy? | URL path (/v1/), headers, no versioning |

---

## Security Practices Questions

Frame as "what does your team do?" — every team has different security maturity, and that's okay.

| Topic | Question | Common Options |
|-------|----------|---------------|
| Dependency scanning | Do you scan dependencies for vulnerabilities? | Snyk, Dependabot alerts, npm audit / pip-audit, GitHub security advisories, Trivy, no formal process |
| Scan frequency | How often are dependency scans run? | Every PR (CI), nightly/weekly scheduled, manual/ad hoc, only when alerted |
| Input validation | Where does the team validate input? | At API boundaries only, every layer, schema-driven (Zod/Pydantic/JSON Schema), ad hoc |
| Secrets management | How are secrets handled in development? | dotenv with .gitignore, Vault/SSM/Secret Manager, CI/CD env vars, encrypted config (SOPS), 1Password/Doppler |
| Secrets in CI | How are secrets managed in CI/CD? | CI/CD secrets store (GitHub Secrets, GitLab CI vars), Vault integration, env vars, encrypted files |
| Auth patterns | Any team-wide authentication patterns? | JWT with refresh tokens, session-based, OAuth2 flows, delegated to auth service (Auth0, Clerk), API keys |
| Security review | When does a change get extra security scrutiny? | Any auth/permission changes, new API endpoints, dependency updates, all PRs, never formally |
| OWASP awareness | Does the team reference OWASP Top 10 or similar? | Active training/certification, awareness but informal, referenced during code review, not really |
| Static analysis | Do you use security-focused static analysis? | Semgrep, CodeQL, Bandit (Python), ESLint security plugin, SonarQube security rules, no |
| Container security | Do you scan container images? | Trivy, Snyk Container, AWS ECR scanning, no / not applicable |

---

## Definition of Done Questions

Frame as "what does 'done' mean on your team?" — this captures the cross-cutting checklist.

| Topic | Question | Common Options |
|-------|----------|---------------|
| Code complete | What must be true before code is "done"? | Tests pass, lint clean, types check, builds successfully, all of the above |
| Test requirements | What testing is required for a change to be done? | Unit tests for new logic, integration tests for new endpoints, E2E for user-facing changes, coverage threshold met, depends on change type |
| Doc updates | What documentation must be updated? | README if behavior changes, API docs if endpoints change, changelog entry, ADR for arch decisions, none required |
| Review | What review is required? | 1 approval, 2 approvals, specific reviewer for certain areas, CODEOWNERS-based, architect sign-off for major changes |
| Security scan | Is a security check part of "done"? | CI security scan passes, manual review for auth changes, Claude Code's security review, no formal requirement |
| Deploy readiness | Any deployment-related requirements? | Feature flag wrapped, backwards compatible, migration tested, monitoring/alerts configured, rollback plan documented |
| Accessibility | Are there accessibility requirements? | WCAG 2.1 AA compliance, basic a11y checks, screen reader testing, not applicable, no formal requirement |
| Performance | Any performance requirements? | No regressions (benchmarks), load testing for new endpoints, Lighthouse score maintained, no formal requirement |
| Cleanup | What cleanup is expected? | Remove debug code, clean up TODOs, remove unused imports, squash WIP commits, no formal checklist |

---

## Preferred Libraries Questions

Only ask about concerns relevant to the team's stack. Group by language ecosystem.

### JavaScript / TypeScript Ecosystem

| Concern | Question | Common Options |
|---------|----------|---------------|
| HTTP client | Preferred HTTP client? | axios, fetch (native), ky, got |
| Validation | Schema validation? | Zod, Joi, Yup, AJV |
| Date/time | Date/time library? | date-fns, Day.js, Luxon, Temporal (native) |
| Logging | Logging library? | Pino, Winston, console (structured) |
| Auth | Auth library? | NextAuth/Auth.js, Passport, Lucia, custom |

### Python Ecosystem

| Concern | Question | Common Options |
|---------|----------|---------------|
| HTTP client | Preferred HTTP client? | httpx, requests, aiohttp |
| Validation | Data validation? | Pydantic, marshmallow, attrs |
| Logging | Logging? | structlog, loguru, stdlib logging |
| Task queue | Background tasks? | Celery, RQ, Dramatiq, none |
| CLI | CLI framework? | Click, Typer, argparse |

### Go Ecosystem

| Concern | Question | Common Options |
|---------|----------|---------------|
| HTTP router | HTTP router? | chi, gorilla/mux, gin, standard library |
| Logging | Logging? | slog (stdlib), zap, zerolog |
| Config | Configuration? | viper, envconfig, koanf |

### Cross-Cutting

| Concern | Question | Common Options |
|---------|----------|---------------|
| Observability | Observability stack? | OpenTelemetry, Datadog, custom |
| Feature flags | Feature flag system? | LaunchDarkly, Unleash, custom, none |
| Email | Email sending? | SendGrid, AWS SES, Resend, Postmark |
