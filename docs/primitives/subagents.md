# Custom Subagents Reference

> Source: Claude Code official documentation + RAG Memory (docs 19, 111)

## What Is a Custom Subagent?

A custom subagent is a markdown file with YAML frontmatter that defines a specialized agent. The frontmatter controls the agent's capabilities (tools, model, permissions). The markdown body IS the agent's system prompt — it tells the agent what it is, what to do, and how to return results.

Custom subagents extend Claude Code's built-in agents with domain-specific expertise.

## Built-in Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| `Explore` | haiku | Read-only (Glob, Grep, Read) | Fast codebase exploration. Claude specifies thoroughness: **quick** (targeted lookups), **medium** (balanced), or **very thorough** (comprehensive analysis). |
| `Plan` | inherit | Read-only | Planning and architectural analysis |
| `general-purpose` | inherit | All tools | Complex multi-step tasks |
| `Bash` | inherit | Bash only | Terminal command execution |
| `claude-code-guide` | haiku | Read, WebFetch, WebSearch | Questions about Claude Code features |
| `statusline-setup` | sonnet | — | Configuring the Claude Code status line (invoked by `/statusline`) |

## Agent File Format

Agent files are markdown with YAML frontmatter:

```yaml
---
name: my-agent
description: What this agent does and when Claude should delegate to it
tools:
  - Read
  - Glob
  - Grep
  - mcp__rag-memory-primary__search_documents
model: sonnet
---

You are a specialized agent that...

## Your Task
...

## What to Return
...

## Rules
...
```

## Frontmatter Fields (Complete Reference)

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `name` | Yes | string | — | Unique identifier. Plugin agents get namespaced: `plugin-name:agent-name` |
| `description` | Yes | string | — | When Claude should delegate to this agent. Critical for auto-selection. |
| `tools` | No | list | — | Allowlist of tools the agent can use. If omitted, inherits available tools. |
| `disallowedTools` | No | list | — | Denylist of tools the agent cannot use. |
| `model` | No | string | inherit | `sonnet`, `opus`, `haiku`, or inherits from parent session. |
| `permissionMode` | No | string | `default` | `default`, `acceptEdits`, `delegate`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | integer | — | Maximum agentic turns before stopping. |
| `skills` | No | list | — | Skills to preload at agent startup. Agent gets these as reference knowledge. |
| `mcpServers` | No | list | — | MCP servers available to this agent. |
| `hooks` | No | object | — | Lifecycle hooks scoped to the agent. Same format as skill/settings hooks. |
| `memory` | No | string | — | Persistent memory scope: `user`, `project`, or `local`. |

## Where Agent Files Live (Priority Order)

1. CLI `--agents` flag (highest — session only, JSON format, not saved to disk)
2. Project: `.claude/agents/`
3. User: `~/.claude/agents/`
4. Plugin: `plugins/<name>/agents/` (lowest)

Higher priority wins when agents share the same name.

### CLI-Defined Subagents

Subagents can be passed as JSON when launching Claude Code with `--agents`. They exist only for that session:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

The JSON accepts the same fields as file-based frontmatter. Use `prompt` for the system prompt (equivalent to the markdown body in file-based subagents).

### Managing Subagents with /agents

The `/agents` command provides an interactive interface to view, create, edit, and delete subagents. This is the recommended way to manage subagents. Subagents created via `/agents` are available immediately (no restart needed).

> Source: https://code.claude.com/docs/en/sub-agents

## How Custom Subagents Are Invoked

Custom agents are **auto-discovered** by Claude Code through directory scanning. Once discovered, they are available alongside built-in agents.

**Invocation mechanisms:**
1. **Claude delegates automatically** based on the agent's `description` field and task context
2. **A skill's instructions** tell Claude to use a specific agent (Claude invokes via Task tool)
3. **A skill with `context: fork` + `agent: agent-name`** runs the skill as that agent
4. **User invokes manually** through the `/agents` interface

When a skill's SKILL.md says "use the `prior-art-search` agent", Claude — executing that skill inline — recognizes `prior-art-search` as an available custom agent and invokes it as a subagent.

## Key Behaviors

- **Subagents CANNOT spawn other subagents** — they are leaf nodes in the execution tree
- **Subagents run in isolation** — own conversation history, own context window
- **Results are summarized** back to the parent conversation
- **Foreground subagents** block the main conversation; permission prompts pass through to the user
- **Background subagents** run concurrently; auto-deny unapproved permissions (cannot prompt user). MCP tools are not available in background subagents. Press **Ctrl+B** to background a running task.
- **Auto-compaction** at ~95% context capacity (configurable via `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`)
- **Resumable** — subagents can be resumed by agent ID with full context preserved
- **Transcript persistence** — subagent transcripts are stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` and persist independently of the main conversation

## Restricting Subagent Spawning

**Disable specific subagents** by adding them to the `deny` array in settings:

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(my-custom-agent)"]
  }
}
```

Also available via CLI: `claude --disallowedTools "Task(Explore)"`

**Restrict which subagents an agent can spawn** (only applies to agents running as main thread with `claude --agent`):

```yaml
tools: Task(worker, researcher), Read, Bash
```

This is an allowlist: only `worker` and `researcher` can be spawned. If `Task` is omitted entirely, no subagents can be spawned. `Task` without parentheses allows all.

> Note: `Task(agent_type)` has no effect in subagent definitions since subagents cannot spawn other subagents.

> Source: https://code.claude.com/docs/en/sub-agents

## Persistent Memory

If the `memory` field is set, the agent maintains persistent notes across sessions:

| Scope | Location |
|-------|----------|
| `user` | `~/.claude/agent-memory/<name>/` |
| `project` | `.claude/agent-memory/<name>/` |
| `local` | `.claude/agent-memory-local/<name>/` |

## Agent Body (System Prompt) Best Practices

The markdown body defines the agent's behavior. Structure it clearly:

```markdown
# Agent Name

You are a [role] that [purpose].

## Your Task
What the agent does when invoked.

## How to Work
Steps or approach (goal-driven, not overly procedural).

## What to Return
Exact output format expected by the parent skill/conversation.

## Rules
- Constraints and boundaries
- What NOT to do
```

1. **Be specific about output format** — the parent needs structured results it can use
2. **Include the right tools** — only what the agent needs for its specific task
3. **Choose the right model** — `haiku` for quick lookups, `sonnet` for analysis, `opus` for complex reasoning
4. **State constraints clearly** — what the agent should NOT do
5. **Design for the parent** — the agent's output is consumed by the skill/conversation that invoked it
