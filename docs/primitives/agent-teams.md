# Agent Teams Reference

> Source: https://code.claude.com/docs/en/agent-teams

> **Experimental.** Agent teams are disabled by default. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in settings.json or environment.

## What Is an Agent Team?

Agent teams coordinate multiple Claude Code instances working together. One session acts as the **team lead**, coordinating work and assigning tasks. **Teammates** work independently, each in its own context window, and can communicate directly with each other.

Unlike subagents (which run within a single session and can only report back), teammates are fully independent sessions that can message each other.

## When to Use Agent Teams vs Subagents

|                   | Subagents                                        | Agent Teams                                       |
|-------------------|--------------------------------------------------|---------------------------------------------------|
| **Context**       | Own context; results return to caller            | Own context; fully independent                    |
| **Communication** | Report results back to main agent only           | Teammates message each other directly             |
| **Coordination**  | Main agent manages all work                      | Shared task list with self-coordination           |
| **Best for**      | Focused tasks where only the result matters      | Complex work requiring discussion and collaboration |
| **Token cost**    | Lower: results summarized back                   | Higher: each teammate is a separate Claude instance |

**Use agent teams for:**
- Research and review (multiple perspectives simultaneously)
- New modules/features (each teammate owns a separate piece)
- Debugging with competing hypotheses
- Cross-layer coordination (frontend, backend, tests)

**Use subagents instead for:**
- Sequential tasks
- Same-file edits
- Work with many dependencies
- Focused tasks where only the result matters

## Architecture

| Component | Role |
|-----------|------|
| **Team lead** | Main session that creates the team, spawns teammates, coordinates |
| **Teammates** | Separate Claude Code instances that each work on assigned tasks |
| **Task list** | Shared list of work items teammates claim and complete |
| **Mailbox** | Messaging system for inter-agent communication |

Storage locations:
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

## Display Modes

| Mode | Description | Requirement |
|------|-------------|-------------|
| `in-process` | All teammates in main terminal. Use Shift+Up/Down to select, type to message. | Any terminal |
| `tmux` / split panes | Each teammate gets its own pane. Click to interact. | tmux or iTerm2 |
| `auto` (default) | Uses split panes if inside tmux, in-process otherwise | — |

Configure via settings: `"teammateMode": "in-process"` or CLI: `claude --teammate-mode in-process`

## Coordination

- **Message**: Send to one specific teammate
- **Broadcast**: Send to all (use sparingly — costs scale with team size)
- **Task assignment**: Lead assigns, or teammates self-claim pending/unblocked tasks
- **Task claiming**: Uses file locking to prevent race conditions
- **Dependency management**: Tasks can depend on other tasks; blocked tasks auto-unblock when dependencies complete

## Quality Gates with Hooks

Two hook events for agent team quality enforcement:

| Hook Event | When It Fires | Exit Code 2 Effect |
|------------|---------------|-------------------|
| `TeammateIdle` | Teammate about to go idle | Teammate receives stderr feedback, continues working |
| `TaskCompleted` | Task being marked complete | Task stays open, model receives stderr feedback |

## Delegate Mode

Press **Shift+Tab** to enable delegate mode for the lead. Restricts the lead to coordination-only tools (spawning, messaging, shutting down teammates, managing tasks). Prevents the lead from implementing tasks itself.

## Permissions

Teammates start with the lead's permission settings. If the lead uses `--dangerously-skip-permissions`, all teammates do too. Individual modes can be changed after spawning but not at spawn time.

## Limitations

- **No session resumption** with in-process teammates (`/resume` and `/rewind` don't restore them)
- **One team per session** — clean up before starting a new team
- **No nested teams** — teammates cannot spawn their own teams
- **Lead is fixed** — cannot promote a teammate or transfer leadership
- **Permissions set at spawn** — all teammates inherit lead's mode
- **Split panes** not supported in VS Code terminal, Windows Terminal, or Ghostty
- **Shutdown can be slow** — teammates finish current request before stopping
- **Task status can lag** — teammates may fail to mark tasks completed

## Cleanup

Always use the lead to clean up: "Clean up the team." The lead checks for active teammates and fails if any are still running — shut them down first. Teammates should NOT run cleanup (their team context may not resolve correctly).
