# Hooks Reference

> Source: Claude Code official documentation + RAG Memory (docs 19, 89, 101)

## What Is a Hook?

A hook is a deterministic event handler that fires automatically during Claude's lifecycle. Hooks run shell commands, LLM evaluations, or multi-turn agent verifications in response to specific events.

Hooks are for **guaranteed automation** — things that MUST happen (approval gates, formatting, validation). Unlike skills (which Claude interprets), hooks execute deterministically.

## Hook Events (Complete List — 14 Events)

| Event | When It Fires | Can Block? | Common Use |
|-------|---------------|------------|------------|
| `SessionStart` | Session begins or resumes | No | Initialize environment, set env vars |
| `UserPromptSubmit` | User submits a prompt | Yes | Inject context, validate/block input |
| `PreToolUse` | Before a tool executes | Yes | **Block dangerous operations**, approval gates |
| `PermissionRequest` | Permission dialog appears | Yes | Auto-approve/deny patterns |
| `PostToolUse` | After a tool succeeds | No | Format output, notify |
| `PostToolUseFailure` | After a tool fails | No | Error handling |
| `Notification` | Claude sends a notification | No | Route to external systems |
| `SubagentStart` | A subagent spawns | No | Inject context, track execution |
| `SubagentStop` | A subagent finishes | Yes | Process results |
| `Stop` | Claude finishes responding | Yes | Prevent premature stopping |
| `TeammateIdle` | Agent team teammate going idle | Yes | Quality gates, coordination |
| `TaskCompleted` | A task is marked complete | Yes | Enforce completion criteria |
| `PreCompact` | Before context compaction | No | Preserve critical context |
| `SessionEnd` | Session terminates | No | Cleanup, logging |

> Source: https://code.claude.com/docs/en/hooks

## Hook Types

| Type | What It Does | Returns |
|------|-------------|---------|
| `command` | Runs a shell script | Exit code: 0=proceed, 2=block, other=non-blocking error |
| `prompt` | LLM evaluation of the situation | Decision + reasoning |
| `agent` | Multi-turn subagent verification | Thorough review |

## Hook Configuration Format

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"          # Optional — filter by tool name
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          timeout: 30
          statusMessage: "Validating..."
```

### Handler Fields

**Common fields (all types):**
- `type` — `command`, `prompt`, or `agent`
- `timeout` — max execution time (ms)
- `statusMessage` — shown to user while hook runs
- `once` — run only once per session

**Command-specific:**
- `command` — shell command to execute
- `async` — `true` to run in background without blocking

**Prompt/Agent-specific:**
- `prompt` — the evaluation prompt
- `model` — model to use for evaluation

## PreToolUse Decision Control

PreToolUse hooks use `hookSpecificOutput` for richer control than other events:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Database writes are not allowed",
    "updatedInput": { "command": "npm run lint" },
    "additionalContext": "Current environment: production."
  }
}
```

| Return Field | Values | Effect |
|-------------|--------|--------|
| `permissionDecision` | `allow`, `deny`, `ask` | `allow` bypasses permissions, `deny` blocks, `ask` prompts user |
| `permissionDecisionReason` | string | For allow/ask: shown to user. For deny: shown to Claude. |
| `updatedInput` | object | Modify tool input before execution |
| `additionalContext` | string | Inject context into Claude's conversation |

> **Deprecation note:** PreToolUse previously used top-level `decision` and `reason` fields — these are deprecated. Use `hookSpecificOutput.permissionDecision` and `hookSpecificOutput.permissionDecisionReason` instead. Other events (PostToolUse, Stop, etc.) continue to use top-level `decision` and `reason`.

## PermissionRequest Decision Control

PermissionRequest hooks use `hookSpecificOutput` with a `decision` object:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": { "command": "npm run lint" },
      "updatedPermissions": [{ "type": "toolAlwaysAllow", "tool": "Bash" }]
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `behavior` | `"allow"` grants the permission, `"deny"` denies it |
| `updatedInput` | For allow: modifies tool input before execution |
| `updatedPermissions` | For allow: applies permission rules (like "always allow" options) |
| `message` | For deny: tells Claude why |
| `interrupt` | For deny: if `true`, stops Claude |

> Source: https://code.claude.com/docs/en/hooks

## Exit Code Behavior

Exit codes for command hooks:
- `0` — proceed normally (stdout parsed for JSON output)
- `2` — blocking error (stderr fed back as error message)
- Other — non-blocking error (logged but execution continues)

**Which events can block (exit code 2):**

| Event | Exit 2 Effect |
|-------|---------------|
| `PreToolUse` | Blocks the tool call |
| `PermissionRequest` | Denies the permission |
| `UserPromptSubmit` | Blocks prompt processing, erases the prompt |
| `Stop` | Prevents Claude from stopping, continues conversation |
| `SubagentStop` | Prevents subagent from stopping |
| `TeammateIdle` | Prevents teammate from going idle |
| `TaskCompleted` | Prevents task from being marked completed |
| `PostToolUse` | Cannot block (tool already ran) — stderr shown to Claude |
| `PostToolUseFailure` | Cannot block — stderr shown to Claude |
| Others | Cannot block — stderr shown to user only |

## SessionStart Details

SessionStart matchers filter by how the session started: `startup`, `resume`, `clear`, `compact`.

**Additional input fields:**
- `source` — how the session started
- `model` — the model identifier
- `agent_type` — present when started with `claude --agent <name>`

**CLAUDE_ENV_FILE:** SessionStart hooks have access to the `CLAUDE_ENV_FILE` environment variable — a file path where you can persist environment variables for subsequent Bash commands:

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

Any variables written to this file are available in all subsequent Bash commands for the session. Only SessionStart hooks have access to `CLAUDE_ENV_FILE`.

> Source: https://code.claude.com/docs/en/hooks

## Matcher Patterns

| Event | What matcher filters | Example values |
|-------|---------------------|----------------|
| PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest | Tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| SessionStart | How session started | `startup`, `resume`, `clear`, `compact` |
| SessionEnd | Why session ended | `clear`, `logout`, `prompt_input_exit`, `other` |
| Notification | Notification type | `permission_prompt`, `idle_prompt`, `auth_success` |
| SubagentStart, SubagentStop | Agent type | `Bash`, `Explore`, `Plan`, custom names |
| PreCompact | Compaction trigger | `manual`, `auto` |
| UserPromptSubmit, Stop, TeammateIdle, TaskCompleted | No matcher | Always fires |

MCP tools follow the pattern `mcp__<server>__<tool>` — use `mcp__memory__.*` to match all tools from a server.

> Source: https://code.claude.com/docs/en/hooks

## Where Hooks Are Defined

| Location | Scope | Priority |
|----------|-------|----------|
| Managed policy | Organization-wide | Highest |
| `~/.claude/settings.json` | User-wide | High |
| `.claude/settings.json` | Project (committed) | Medium |
| `.claude/settings.local.json` | Project (gitignored) | Medium |
| Plugin `hooks/hooks.json` | Plugin scope | Lower |
| Skill/Agent frontmatter | Skill/Agent lifetime | Lowest (scoped) |

## Hooks in Skill/Agent Frontmatter

Hooks defined in frontmatter are **scoped to the skill/agent's lifetime**:
- Only fire while the skill/agent is active
- Clean up automatically when it finishes
- Same configuration format as settings-based hooks

```yaml
---
name: database-admin
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/block-destructive.sh"
---
```

## Plugin Hook Distribution

Hooks in plugins go in `hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__rag-memory__ingest_text",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/rag-memory-approval.py"
          }
        ]
      }
    ]
  }
}
```

`${CLAUDE_PLUGIN_ROOT}` resolves to the plugin's directory at runtime.

## Common Patterns

**Approval gate for external writes:**
```yaml
PreToolUse:
  - matcher: "mcp__atlassian__createConfluencePage"
    hooks:
      - type: command
        command: "${CLAUDE_PLUGIN_ROOT}/hooks/atlassian-approval.py"
```

**Auto-format after file edit:**
```yaml
PostToolUse:
  - matcher: "Write"
    hooks:
      - type: command
        command: "prettier --write $FILE_PATH"
```

**Re-inject context after compaction:**
```yaml
PreCompact:
  - hooks:
      - type: command
        command: "./scripts/save-critical-context.sh"
```

## Best Practices

1. **Hooks are for determinism** — things that MUST happen. Use skills for things Claude should consider.
2. **Keep hooks fast** — they run on every matching event
3. **Use `matcher`** to narrow scope — don't run hooks on every tool call
4. **Exit code 2 blocks** — use this for approval gates
5. **Use `${CLAUDE_PLUGIN_ROOT}`** for portable paths in plugin hooks
6. **Scope hooks to skills** when they only apply during a specific workflow
