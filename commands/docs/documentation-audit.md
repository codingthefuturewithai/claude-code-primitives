---
description: Audit and update project documentation against actual source code
argument-hint: "[scope: directory name, component name, or 'all'] (default: all)"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Edit", "Write", "Task"]
---

# Documentation Audit

## Critical Rules

1. **Explore the repository FIRST. Read documentation SECOND.** Do NOT let documentation guide your exploration. You must independently discover what exists, then compare with what is documented.

2. **Never assume documentation is complete.** Undocumented components are findings, not oversights to ignore. New code may exist that has never been documented.

3. **Progressive disclosure is mandatory.** Work in layers. Report findings at each layer and get user confirmation before going deeper. Never try to read all code and all docs in one pass.

4. **Bidirectional verification.** Check both directions:
   - Code → Docs: Does every significant component have documentation?
   - Docs → Code: Does every documented claim match reality?

5. **No edits without approval.** Present your findings and proposed changes. Wait for the user to approve what gets created, updated, or deleted.

---

## Layer 1: Structural Discovery

**Goal:** Understand the repo layout and locate documentation.

**Actions:**
- Scan the repo root and top-level directories
- Identify documentation locations by checking for:
  - Common doc directories: `docs/`, `doc/`, `docs/`, `documentation/`, `wiki/`, `.github/`, `guides/`
  - Doc tool configs: `mkdocs.yml`, `docusaurus.config.js`, `.readthedocs.yml`, `book.toml`, `vitepress`, `astro.config.*`
  - Root-level docs: `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `CHANGELOG.md`
  - Inline documentation patterns (docstrings, JSDoc, rustdoc, etc.)
- Identify the project type (monorepo, library, app, CLI tool, etc.)

**Report to user:**
- "Here is the repo structure I see."
- "I found documentation in these locations: [list]"
- "The project appears to be: [type]"
- "Should I proceed with auditing all documentation, or focus on a specific area?"

**Wait for confirmation before Layer 2.**

---

## Layer 2: Component Inventory

**Goal:** Build a complete manifest of what exists in this codebase, independent of documentation.

**Actions:**
- For each major directory/area, identify:
  - Services, applications, frontends, backends
  - Scripts, CLI tools, utilities
  - Configuration systems, environment handling
  - Infrastructure, deployment, CI/CD
  - Database schemas, migrations
  - API surfaces (REST, GraphQL, RPC, MCP, etc.)
  - Test suites and their coverage areas
- Note anything that looks new, experimental, or recently added (check git recency if helpful)

**Report to user:**
- "These are the components I discovered: [structured list]"
- Group by area/concern
- Flag anything that looks significant but might be undocumented

**Wait for confirmation before Layer 3.**

---

## Layer 3: Documentation Inventory

**Goal:** Catalog what is currently documented without deep-reading every file.

**Actions:**
- For each documentation location found in Layer 1:
  - Read file names, directory structure, and section headers
  - Note what each doc claims to cover (from title/headers only)
  - Identify any index files, tables of contents, or navigation configs
- Do NOT read full file contents yet — headers and structure only

**Report to user:**
- "Here is what your documentation currently covers: [list mapped to files]"
- "Each doc's apparent scope based on its headers: [summary]"

**Wait for confirmation before Layer 4.**

---

## Layer 4: Gap Analysis

**Goal:** Compare the component inventory (Layer 2) against the documentation inventory (Layer 3).

**Produce three buckets:**

### A. Undocumented Components (Code exists, no docs)
Components discovered in Layer 2 that have no corresponding documentation. These may need new documents created.

### B. Potentially Stale Docs (Docs exist, code may have changed)
Documentation that covers components which exist but may have drifted. These need accuracy verification in Layer 5.

### C. Orphaned Docs (Docs reference things that no longer exist)
Documentation covering components, features, or patterns that no longer exist in the codebase. Candidates for removal or rewrite.

**Report to user:**
- Present all three buckets clearly
- For Bucket A: "These components have no documentation. Want me to create docs for any/all?"
- For Bucket B: "These docs may be outdated. Want me to verify accuracy?"
- For Bucket C: "These docs reference things I can't find in the code. Remove or investigate?"
- Ask user which items to proceed with

**Wait for explicit approval on what to tackle before Layer 5.**

---

## Layer 5: Deep Audit & Remediation

**Goal:** For user-approved items only, do detailed verification and make changes.

**For each approved item, based on its bucket:**

### Bucket A (New docs needed):
- Read the relevant source code thoroughly
- Draft documentation following the repo's existing conventions (style, format, location)
- Present draft to user before writing

### Bucket B (Accuracy check):
- Read the full doc content AND the corresponding source code
- Identify specific claims that are wrong, outdated, or incomplete
- Present a diff of proposed changes to user before editing

### Bucket C (Orphaned docs):
- Confirm the referenced code/feature truly doesn't exist
- Recommend: delete, archive, or rewrite
- Wait for user decision

**Work in batches.** If there are many items, group them logically and process one group at a time. Report progress between groups.

---

## Scope Argument

The optional argument lets the user focus the audit:

- No argument / `all` → Full repo audit, all layers
- A directory name (e.g., `frontend`, `api`) → Focus component discovery and doc audit on that area
- A doc directory name (e.g., `docs`) → Only audit that documentation directory's accuracy

When scoped, still perform Layer 1 discovery to understand the full context, but limit Layers 2-5 to the specified scope.

---

## Conventions to Respect

- Match the repo's existing documentation style (markdown flavor, heading levels, voice)
- Match the repo's existing file organization (if docs are flat, don't nest; if nested, follow the pattern)
- Don't add documentation tooling or config that doesn't already exist
- Don't restructure documentation layout without explicit user approval
- Keep docs focused and maintainable — prefer updating existing files over creating new ones unless a genuinely new component needs coverage
