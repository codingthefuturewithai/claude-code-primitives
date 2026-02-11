# How Claude Code Primitives Relate

> Source: Claude Code official documentation + RAG Memory (docs 74, 76, knowledge graph)

## The Primitive Toolkit

| Primitive | Purpose | Context Cost | When to Use |
|-----------|---------|-------------|-------------|
| **CLAUDE.md** | Persistent rules and context | Every request | Always-on project rules |
| **Skill (action)** | User-invocable workflow | Low (description only until invoked) | Repeatable tasks triggered by user |
| **Skill (reference)** | Background knowledge | Low (description only until invoked) | Conventions, patterns Claude auto-applies |
| **Custom subagent** | Isolated task execution | Zero (own context) | Heavy reads, parallel search, context preservation |
| **Hook** | Deterministic automation | Zero (external) | Guaranteed actions, approval gates |
| **MCP Server** | External service integration | Every request (tool definitions) | Connect to Jira, Confluence, databases, etc. |
| **Plugin** | Distribution package | Bundles all above | Sharing across projects/teams |
| **Task System** | Built-in task tracking | Low (tool definitions) | Multi-step work coordination |
| **Agent Team** | Multi-session collaboration | Experimental, high token cost | Parallel research, competing hypotheses, cross-layer work. See [agent-teams.md](agent-teams.md) |

## How Skills and Subagents Relate

There are **two official patterns** connecting skills and subagents (plus a third practical pattern):

### Pattern 1: Skill Runs IN a Subagent (`context: fork`)

The skill IS the task. The subagent IS the executor.

```yaml
# In SKILL.md frontmatter
---
name: codebase-audit
context: fork
agent: Explore       # Built-in or custom agent name
---
Audit the codebase for...
```

- The entire skill content becomes the subagent's task prompt
- The subagent runs in isolation with its own context
- Results are summarized back to the main conversation
- The `agent` field accepts built-in names OR custom agent names from `agents/`

### Pattern 2: Subagent Preloads Skills (`skills` field)

The subagent IS the task. The skills ARE the knowledge.

```yaml
# In agent frontmatter
---
name: my-agent
skills:
  - api-conventions
  - error-handling-patterns
---
Agent prompt here...
```

- When the subagent is invoked, the listed skills are loaded as reference knowledge
- The subagent can use those skills as context for its work

### Pattern 3: Skill Instructions Reference an Agent (Our Primary Pattern)

A regular conversation skill (no `context: fork`) instructs Claude to delegate specific work to a named custom agent.

```markdown
# In SKILL.md body
3. **Search for prior art**: Use the **`prior-art-search`** agent to search
   ALL configured backends in parallel. This is heavy read work that benefits
   from context isolation.
```

**How this works:**
1. User invokes the skill (e.g., `/devflow:pm:discover`)
2. Claude reads the SKILL.md and follows instructions inline (in the main conversation)
3. At the delegation point, Claude recognizes `prior-art-search` as an available custom agent
4. Claude invokes it as a subagent (auto-discovered from the plugin's `agents/` directory)
5. The subagent runs in isolation with its own tools and model
6. Results return to Claude in the main conversation
7. Claude continues the skill workflow with the agent's results

**This is the pattern used by DevFlow's PM skills.** The skill orchestrates the overall workflow (conversational, human-in-the-loop). The agents handle isolated heavy work (searching, analyzing, comparing).

## How Skills and Hooks Relate

- **Hooks in skill frontmatter** fire only while the skill is active
- Hooks enforce deterministic behavior (approval gates, validation)
- Skills provide guidance; hooks provide guarantees
- Example: A skill's instructions say "store the PRD in the user's chosen backend." A hook on the write tool ensures the user approves before it happens.

**Rule of thumb:** If it MUST happen → hook. If Claude should consider it → skill instruction.

## How Skills and Commands Relate

> **Commands have been merged into skills.** Both `.claude/commands/review.md` and `.claude/skills/review/SKILL.md` create `/review`. Existing commands keep working, but skills are recommended.

| Aspect | Commands (legacy) | Skills (recommended) |
|--------|----------|--------|
| Location | `commands/domain/name.md` | `skills/name/SKILL.md` |
| Plugin naming | `plugin:domain:name` | `plugin:name` |
| Symlinks | **NO** (bug #14929) | YES |
| Frontmatter | Same fields supported | Full feature set |
| Supporting files | No | Yes (references/, scripts/) |
| Auto-invocation | Same | Same |

If a skill and a command share the same name, the skill takes precedence.

> Source: https://code.claude.com/docs/en/skills

## How Plugins Bundle Everything

A plugin distributes all primitive types:

```
my-plugin/
├── .claude-plugin/plugin.json    # Manifest
├── commands/                     # Slash commands
├── skills/                       # Skills (SKILL.md directories)
├── agents/                       # Custom subagents
├── hooks/                        # hooks.json + scripts
├── .mcp.json                     # MCP server configs
└── .lsp.json                     # LSP server configs
```

Auto-discovery scans `commands/`, `skills/`, `agents/`, `hooks/` automatically. All components get namespaced under the plugin name.

## Priority/Precedence

When multiple definitions exist for the same component:

**Skills:** Enterprise > Personal (`~/.claude/skills/`) > Project (`.claude/skills/`) > Plugin

**Agents:** CLI flag > Project (`.claude/agents/`) > User (`~/.claude/agents/`) > Plugin (`agents/`)

**Hooks:** Managed policy > User settings > Project settings > Project local > Plugin > Skill/Agent frontmatter

Higher priority wins.

## Context Cost Awareness

When designing with primitives, consider context impact:

| Primitive | Context Cost | Strategy |
|-----------|-------------|----------|
| CLAUDE.md | Loaded every request | Keep under 500 lines |
| Skill descriptions | Always loaded (lightweight) | Keep descriptions concise |
| Skill content | Loaded on invocation | Keep SKILL.md under 500 lines; use supporting files |
| MCP tool definitions | Always loaded | Only configure needed servers |
| Subagent execution | Zero main context cost | Use for heavy reads and searches |
| Hooks | Zero context cost | External execution |

**Key insight:** Subagents preserve main context by keeping heavy work isolated. This is why PM skills delegate searching, analyzing, and comparing to subagents — it keeps the conversational workflow with the user clean and focused.

## Design Decision Framework

When implementing a new capability, ask:

1. **Does the user need to invoke it?** → Skill (action)
2. **Should Claude know it automatically?** → Skill (reference) or CLAUDE.md
3. **Is it heavy read/analysis work?** → Custom subagent
4. **Must it happen deterministically?** → Hook
5. **Does it connect to an external service?** → MCP Server
6. **Should it be shared across projects?** → Plugin

Multiple primitives often combine: a skill orchestrates the workflow, delegates heavy work to subagents, and hooks enforce approval gates on writes.
