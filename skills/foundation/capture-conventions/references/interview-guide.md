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
