# Skills Reference

> Source: Claude Code official documentation + RAG Memory (docs 17, 104)

## What Is a Skill?

A skill is a directory containing a `SKILL.md` file. The file has two parts: YAML frontmatter (metadata controlling behavior) and a markdown body (instructions Claude follows). Skills are the primary way to teach Claude Code new capabilities.

Skills follow the **Agent Skills open standard**, extended by Claude Code with additional fields.

> **Note:** Custom slash commands have been merged into skills. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work the same way. Existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter, and the ability for Claude to load them automatically when relevant. If a skill and a command share the same name, the skill takes precedence.

## Skill Types

| Type | Purpose | Key Traits |
|------|---------|------------|
| **Action skill** | Task-oriented workflow | Concrete goal, numbered steps, often `disable-model-invocation: true` |
| **Reference skill** | Background knowledge | Conventions, patterns; Claude auto-applies when relevant; often `user-invocable: false` |

## Directory Structure

```
my-skill/
├── SKILL.md              # Required — overview and navigation
├── references/            # Optional — detailed reference material
│   ├── template.md
│   └── guide.md
└── scripts/               # Optional — utility scripts
    └── validate.sh
```

Keep `SKILL.md` under 500 lines. Move detailed material to supporting files and reference them with markdown links:

```markdown
See [references/template.md](references/template.md) for the full template.
```

## Frontmatter Fields (Complete Reference)

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `name` | No | string | directory name | Display name. Lowercase, numbers, hyphens only (max 64 chars). Plugin skills get namespaced: `plugin-name:skill-name` |
| `description` | Recommended | string | first paragraph | What the skill does. Claude uses this for auto-invocation matching. Include keywords users naturally say. |
| `argument-hint` | No | string | — | Hint for expected arguments, shown during autocomplete. e.g., `[issue-number]` |
| `disable-model-invocation` | No | boolean | `false` | Prevents Claude from auto-triggering. Use for manual-only workflows. |
| `user-invocable` | No | boolean | `true` | Whether visible in `/` menu. Set `false` for Claude-only background knowledge. |
| `allowed-tools` | No | YAML list | — | Tools Claude can use without per-use permission while skill is active. |
| `model` | No | string | inherit | Override session model. Values: `opus`, `sonnet`, `haiku` |
| `context` | No | string | `conversation` | `conversation` = runs inline. `fork` = runs in a subagent (isolated context). |
| `agent` | No | string | `general-purpose` | Which agent type when `context: fork`. Built-in: `Explore`, `Plan`, `general-purpose`. Also accepts custom agent names from `agents/`. |
| `hooks` | No | object | — | Event handlers scoped to this skill's lifetime. Same format as settings hooks. |
| `once` | No | boolean | `false` | Run once and return result without further interaction. |

## String Substitutions

| Variable | Description | Example |
|----------|-------------|---------|
| `$ARGUMENTS` | All arguments passed when invoking | `/fix-issue 123` → `$ARGUMENTS` = `"123"` |
| `$ARGUMENTS[N]` | Specific argument by 0-based index | `$ARGUMENTS[0]` |
| `$N` | Shorthand for `$ARGUMENTS[N]` | `$0`, `$1`, `$2` |
| `${CLAUDE_SESSION_ID}` | Current session ID | For logging or session-specific files |

## Dynamic Content Injection (Preprocessing)

The `` !`command` `` syntax runs shell commands BEFORE the skill content reaches Claude. This is preprocessing — Claude only sees the final rendered output.

```yaml
---
name: pr-summary
context: fork
agent: Explore
---
PR diff: !`gh pr diff`
Changed files: !`gh pr diff --name-only`

Summarize this pull request...
```

## allowed-tools Details

YAML list format in frontmatter:

```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - mcp__rag-memory-primary__search_documents
```

Available tools: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Task`, `Skill`, `AskUserQuestion`, and any MCP tool by full name.

Fine-grained Bash control: `Bash(npm *)`, `Bash(git *)` — allows specific commands only.

MCP tool patterns: `mcp__memory__*`, `mcp__filesystem__read*`

Tools only apply while the skill is active. Global permission rules still apply.

## Hooks in Skill Frontmatter

Hooks defined in a skill's frontmatter are **scoped to the skill's lifetime**. They only fire while the skill is active and clean up automatically when it finishes.

```yaml
hooks:
  PreToolUse:
    - matcher: "mcp__rag-memory__ingest_text"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/rag-memory-approval.py"
```

Same configuration format as settings-based hooks. See [hooks.md](hooks.md) for full hook reference.

## How Claude Executes a Skill

1. **Discovery**: Claude Code loads skill descriptions into context (lightweight — descriptions only, not full content)
2. **Triggering**: User invokes manually (`/skill-name`) OR Claude auto-invokes based on description match
3. **Preprocessing**: Any `` !`command` `` placeholders execute; `$ARGUMENTS` substituted
4. **Execution**: Claude receives the fully-rendered skill content as its task instructions
5. **Constraints**: `allowed-tools` grants permissions; `model` overrides; `hooks` enforce
6. **Completion**: Skill-scoped hooks clean up; normal conversation resumes

## Running a Skill in a Subagent (`context: fork`)

Adding `context: fork` runs the skill in an isolated subagent:

```yaml
---
name: deep-research
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---
Research $ARGUMENTS thoroughly...
```

- The skill content becomes the subagent's task
- The `agent` field picks the executor: `Explore` (read-only), `Plan`, `general-purpose`, or **any custom agent name**
- Subagent has its own conversation history (isolated from main)
- Results are summarized and returned to main conversation

**Important**: Skills with `context: fork` need explicit, actionable instructions. Guidelines without a concrete task produce no meaningful output.

## Where Skills Live (Priority Order)

1. Enterprise managed (highest)
2. Personal: `~/.claude/skills/`
3. Project: `.claude/skills/`
4. Plugin: `plugins/<name>/skills/` (lowest)

### Automatic Nested Directory Discovery

When you work with files in subdirectories, Claude Code automatically discovers skills from nested `.claude/skills/` directories. For example, editing a file in `packages/frontend/` causes Claude Code to also look for skills in `packages/frontend/.claude/skills/`. This supports monorepo setups where packages have their own skills.

### Skills from Additional Directories

Skills in `.claude/skills/` within directories added via `--add-dir` are loaded automatically and picked up by live change detection — you can edit them during a session without restarting.

## Skill Character Budget

Skills consume ~2% of context window (fallback: 16,000 chars). Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.

## Extended Thinking

To enable extended thinking in a skill, include the word **"ultrathink"** anywhere in the skill content. This activates Claude's extended thinking mode for that skill invocation.

> Source: https://code.claude.com/docs/en/skills

## Visual Output Pattern

Skills can bundle and run scripts that generate interactive HTML files (e.g., codebase visualizers, dependency graphs, test coverage reports). The skill content tells Claude to run the bundled script; the script does the heavy lifting. Use `allowed-tools: Bash(python *)` to allow execution.

> Source: https://code.claude.com/docs/en/skills

## Restricting Claude's Skill Access

Three ways to control which skills Claude can invoke:

1. **Disable all skills** — deny the `Skill` tool in `/permissions`
2. **Allow/deny specific skills** — `Skill(commit)` for exact match, `Skill(review-pr *)` for prefix match
3. **Hide individual skills** — `disable-model-invocation: true` in frontmatter

> Source: https://code.claude.com/docs/en/skills

## Best Practices

1. **Clear description** — include natural-language keywords for auto-invocation matching
2. **Goal-driven over procedural** — state WHAT to achieve and constraints, let Claude navigate
3. **Keep SKILL.md under 500 lines** — use supporting files for detailed reference material
4. **Minimum necessary tools** — only grant what the skill needs in `allowed-tools`
5. **Use `disable-model-invocation: true`** for workflows that should only be triggered manually
6. **Use `context: fork`** when the task is isolated research or investigation
7. **Reference supporting files** with markdown links so Claude can load them on demand
