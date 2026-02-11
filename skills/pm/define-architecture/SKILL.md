---
name: devflow:pm:define-architecture
description: Define or update the architecture and technical design for a project. Includes brownfield analysis, technology selection, system design, and Architecture Decision Records (ADRs).
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__rag-memory-primary__list_collections
  - mcp__rag-memory-primary__search_documents
  - mcp__rag-memory-primary__query_relationships
  - mcp__rag-memory-primary__ingest_text
  - mcp__rag-memory-primary__ingest_file
  - mcp__rag-memory-primary__update_document
  - mcp__atlassian__searchConfluenceUsingCql
  - mcp__atlassian__getConfluencePage
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__getConfluenceSpaces
  - mcp__atlassian__createConfluencePage
  - mcp__atlassian__updateConfluencePage
  - mcp__atlassian__searchJiraIssuesUsingJql
  - mcp__google-drive__search_files
  - mcp__google-drive__download_file
  - mcp__google-drive__create_file
  - mcp__google-drive__update_file
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - mcp__mermaid_image_generator__generate_mermaid_diagram_file
  - mcp__mermaid_image_generator__generate_mermaid_diagram_stream
---

# Define Architecture

**Say exactly:** "SKILL INVOKED: pm/define-architecture"

## Your Role

You are helping the user define or update the architecture for their project. This includes technology selection, system design, and capturing key decisions as Architecture Decision Records (ADRs).

## Your Goal

Produce an architecture document and ADRs that describe HOW the system will be built at a high level — separate from the PRD (which describes WHAT). For brownfield projects, account for the existing system. For greenfield, make deliberate technology and design choices.

## How to Work

1. **Load configuration**: Read `~/.claude/plugins/config/devflow/config.md` for available backends. Check `.devflow/project.md` for upstream artifacts (problem statement, PRD).

2. **Find upstream artifacts**: If a PRD exists (check project manifest), load it — the architecture must address all PRD functional requirements. If no PRD exists, ask the user for the information you need directly.

3. **Check for team conventions**: Use the **`convention-checker`** agent to search configured doc backends for team conventions (output of capture-conventions). This is a quick, cheap lookup — the agent uses model `haiku` for speed. If conventions are found, the agent returns relevant sections. If not found, proceed without them. **Conventions are context, not constraints.**

4. **Analyze existing system** (brownfield): If there's an existing codebase, use the **`brownfield-analyzer`** agent to analyze the existing architecture — tech stack, project structure, key dependencies, integration points, existing patterns, code health. This is heavy codebase reading that MUST be a subagent to preserve main context.

5. **Follow the ingestion workflow**: If the user has existing architecture docs, read [references/ingestion-guide.md](references/ingestion-guide.md) for the multi-source ingestion approach.

6. **Guide the design**: Use [references/architecture-template.md](references/architecture-template.md) as the structural guide. Work through technology selection, component design, data model, API design. For technology research, use the **`tech-researcher`** agent to look up current documentation via Context7 MCP — this prevents Context7 tokens from filling the main context. Use Mermaid MCP for architecture diagrams.

7. **Capture decisions as ADRs**: For each significant decision, prompt: "This seems like a significant decision. Create an ADR for it?" Use [references/adr-template.md](references/adr-template.md) for structure.

8. **Store and baseline**: Present storage options. Store architecture doc and ADRs. Update `.devflow/project.md`.

## Critical Rules

- **Architecture is separate from PRD.** PRD says WHAT. Architecture says HOW at a high level.
- **Conventions are context, not constraints.** Surface them if they exist. User always decides.
- **Brownfield analysis is not optional.** For existing codebases, understand what's there before designing.
- **Capture decisions as ADRs.** Every significant technology or design choice gets an ADR.
- **ADRs reference what they supersede.** If changing a prior decision, link to the old ADR.
- **Human approves all design decisions.** You propose, they decide.
- **Update the project manifest.** Record where architecture doc and ADRs are stored.

---

## ⛔ STOP

Skill complete.
