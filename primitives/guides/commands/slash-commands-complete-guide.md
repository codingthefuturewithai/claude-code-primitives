# Slash Commands: Complete Guide

**Metadata for RAG Memory:**
- primitive_type: slash-command
- content_type: complete-guide
- version: 1.0

---

## What Are Slash Commands?

Slash commands are **custom Markdown files** that define frequently used prompts. They give users explicit control over when to invoke specific instructions.

When you create a file like `review-code.md` in `.claude/commands/`, it becomes available as `/review-code` that users can invoke by typing the command.

**Key characteristics:**
- Single Markdown file per command
- User explicitly invokes with `/command-name`
- Support arguments via `$ARGUMENTS`, `$1`, `$2`, etc.
- Can restrict available tools via YAML frontmatter
- Can execute bash commands and reference files

### Slash Commands vs Other Primitives

| Slash Commands | Skills | Subagents |
|---------------|--------|-----------|
| User explicitly invokes | Auto-activates based on context | Invoked by Claude or user |
| Single .md file | Directory with SKILL.md + resources | Single .md file |
| `/command-name` | Transparent activation | Via Task tool |
| Simple, focused prompts | Complex, multi-step capabilities | Isolated execution context |
| Want explicit control | Want automatic discovery | Need parallel execution or isolation |

---

## When to Use Slash Commands

Use slash commands when:
- **Explicit invocation needed** - User decides when to run
- **Repeated prompts** - Same instruction used frequently
- **Single file sufficient** - No need for supporting files
- **Quick templates** - Simple prompt snippets
- **User control preferred** - Not automatic activation

Do NOT use slash commands when:
- Complex workflows requiring multiple steps → Use **Skills**
- Capabilities requiring scripts/utilities → Use **Skills**
- Knowledge organized across multiple files → Use **Skills**
- Claude should decide when to activate → Use **Skills**
- Need parallel execution or isolation → Use **Subagents**

---

## Command Types & Organization

### Project Commands (`.claude/commands/`)

**Location:** `.claude/commands/` in your repository
**Scope:** Available only in this project
**Sharing:** Committed to git, shared with team
**Label:** Shows as "(project)" in `/help` output

**Use for:**
- Team-standardized workflows
- Project-specific operations
- Shared development tools

**Example:**
```
.claude/commands/deploy.md → /deploy (project)
```

### Personal Commands (`~/.claude/commands/`)

**Location:** `~/.claude/commands/` in your home directory
**Scope:** Available across ALL your projects
**Sharing:** Personal only
**Label:** Shows as "(user)" in `/help` output

**Use for:**
- Personal productivity tools
- Cross-project utilities
- Individual preferences

**Example:**
```
~/.claude/commands/security-review.md → /security-review (user)
```

### Namespacing with Subdirectories

**Pattern:** Subdirectories group related commands but don't affect command name

**Example structure:**
```
.claude/commands/
├── frontend/
│   ├── component.md     → /component (project:frontend)
│   └── optimize.md      → /optimize (project:frontend)
└── backend/
    ├── api.md           → /api (project:backend)
    └── database.md      → /database (project:backend)
```

**Namespace benefits:**
- Organize related commands
- Show context in `/help` output
- Allow multiple commands with same name in different namespaces

**Precedence rules:**
- Project commands override personal commands with same name
- Commands in subdirectories include namespace label

---

## File Format

### File Structure

```markdown
---
description: Brief description of what this command does
argument-hint: [expected-arguments]
allowed-tools: Read, Write, Bash
model: haiku
---

# Command Instructions

Your instructions here. Use $ARGUMENTS for all args, or $1, $2 for individual args.
```

**Filename = Command Name**
- `review-code.md` → `/review-code`
- `fix-tests.md` → `/fix-tests`
- Use kebab-case (lowercase with hyphens)

---

## YAML Frontmatter Format

### Required Fields

**None.** All frontmatter fields are optional, but `description` is highly recommended.

### Optional Fields

| Field | Type | Purpose | Default |
|-------|------|---------|---------|
| `description` | string | Brief command description | First line from prompt |
| `argument-hint` | string | Expected arguments (shown in autocomplete) | None |
| `allowed-tools` | string | Comma-separated tools this command can use | Inherits from conversation |
| `model` | string | Specific model for this command | Inherits from conversation |
| `disable-model-invocation` | boolean | Prevent SlashCommand tool from invoking | false |

### Field Specifications

#### description

**Purpose:** Brief description shown in `/help` and used by SlashCommand tool

**Best practices:**
- Keep concise (one line)
- Describe what it does, not how
- Include when to use it

**Examples:**
```yaml
# Good
description: Review code for bugs and suggest improvements

# Good
description: Deploy application to staging environment

# Avoid (too vague)
description: Code review

# Avoid (too verbose)
description: This command helps Claude review your code by analyzing it for bugs, security issues, and suggesting improvements based on best practices
```

#### argument-hint

**Purpose:** Show expected arguments in autocomplete

**Format:** Square brackets for optional, plain text for required

**Examples:**
```yaml
argument-hint: [file-path]
argument-hint: <issue-number> [priority]
argument-hint: <branch-name>
```

#### allowed-tools

**Purpose:** Restrict which tools this command can use

**Format:** Comma-separated tool names

**Common patterns:**
```yaml
# Read-only operations
allowed-tools: Read, Grep, Glob

# File modifications
allowed-tools: Read, Write, Edit

# With bash execution
allowed-tools: Read, Bash, Write

# Specific bash commands only
allowed-tools: Bash(git status:*), Bash(git diff:*)

# Subagent invocation
allowed-tools: Task

# Everything (rarely needed)
allowed-tools: Read, Write, Edit, Bash, Task, Grep, Glob
```

**Why restrict tools?**
- Prevent unintended actions
- Make command behavior predictable
- Security/safety constraints

#### model

**Purpose:** Use specific model for cost/performance optimization

**Options:**
```yaml
model: haiku          # Fast, cheaper for simple tasks
model: sonnet         # Balanced
model: opus           # Deep reasoning, expensive
```

**When to specify:**
```yaml
# Simple formatting → use haiku
model: haiku

# Complex analysis → use opus
model: opus

# Default → omit field, inherits from conversation
```

#### disable-model-invocation

**Purpose:** Prevent SlashCommand tool from invoking this command

**When to use:**
- Command requires human context/judgment
- Command has side effects that need approval
- Don't want Claude auto-invoking

**Example:**
```yaml
disable-model-invocation: true
```

### Complete Example

```yaml
---
description: Create a git commit with conventional commit format
argument-hint: <type> <message>
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
model: haiku
---

# Git Commit

Create a conventional commit with type $1 and message: $2

## Context
- Current status: !`git status`
- Staged changes: !`git diff --cached`

## Instructions

1. Verify changes are staged
2. Create commit with format: "$1: $2"
3. Confirm commit was created
```

---

## Content Format: Instructions (Not Documentation)

### Write as Instructions (What to DO)

Slash commands should tell Claude **what actions to take**, not describe what the command is for.

#### ❌ Documentation Style (Wrong)

```markdown
# Code Review Command

This command helps Claude review code for potential issues.

Claude will analyze the code and look for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Best practice violations

The command is useful when you want comprehensive code review.
```

#### ✅ Instructions Style (Correct)

```markdown
# Review Code

Review the provided code for bugs, security issues, and best practices.

## Steps

1. Use Read tool to examine the code
2. Check for:
   - Logic errors and edge cases
   - Security vulnerabilities (SQL injection, XSS, etc.)
   - Performance bottlenecks
   - Best practice violations
3. Provide specific findings with line numbers
4. Suggest concrete improvements

## Output Format

Structure your findings as:
- **Critical Issues**: Must fix
- **High Priority**: Should fix
- **Suggestions**: Nice to have
```

**Key differences:**
- ✅ "Review the provided code" vs ❌ "This command reviews code"
- ✅ "Use Read tool to examine" vs ❌ "Claude will analyze"
- ✅ "Check for:" vs ❌ "The command looks for"
- ✅ "Provide specific findings" vs ❌ "The command is useful when"

---

## Argument Handling

### $ARGUMENTS (Capture All)

Captures all arguments as a single string.

**Example:**
```markdown
---
description: Fix an issue
argument-hint: <issue-number> [details]
---

Fix issue: $ARGUMENTS
```

**Usage:**
```
/fix-issue 123 high-priority security
# $ARGUMENTS becomes: "123 high-priority security"
```

**When to use:**
- Variable number of arguments
- Arguments form natural sentence
- Don't need to reference arguments separately

### Positional Parameters ($1, $2, $3)

Access arguments individually by position.

**Example:**
```markdown
---
description: Review pull request
argument-hint: <pr-number> <priority> [reviewer]
---

Review PR #$1 with priority: $2
Assign to reviewer: $3

## Instructions

1. Fetch PR details for #$1
2. Set priority level to $2
3. If $3 is provided, assign reviewer
4. Perform review based on priority
```

**Usage:**
```
/review-pr 456 high alice
# $1 = "456"
# $2 = "high"
# $3 = "alice"
```

**When to use:**
- Access arguments individually in different sections
- Provide defaults for missing arguments
- Build structured commands with specific parameter roles
- Validate or transform individual arguments

### Combining Both Approaches

```markdown
---
description: Deploy application
argument-hint: <environment> [options]
---

Deploy to environment: $1
Additional options: $ARGUMENTS

## Pre-deployment Checks

1. Verify environment $1 exists
2. Check all arguments: $ARGUMENTS
3. Parse options from remaining arguments
```

---

## Advanced Features

### Bash Command Execution (! prefix)

Execute bash commands before the slash command runs, with output included in context.

**CRITICAL:** Must include `allowed-tools` with Bash

**Example:**
```yaml
---
description: Review changes before commit
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

# Pre-commit Review

## Current Status
!`git status`

## Staged Changes
!`git diff --cached`

## Instructions

Review the changes above and suggest improvements before committing.
```

**Output becomes part of context:**
```
## Current Status
On branch main
Changes to be committed:
  modified: src/auth.py

## Staged Changes
+ def login(username, password):
+     # New login logic
```

**Security pattern - Restrict bash commands:**
```yaml
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)
# NOT: allowed-tools: Bash
# Allows ONLY these specific git commands
```

### File References (@ prefix)

Include file contents using `@` prefix.

**Single file:**
```
/review @src/auth.py
```

**Multiple files:**
```
/compare @src/old-version.js with @src/new-version.js
```

**In command instructions:**
```markdown
---
description: Analyze test coverage
---

# Test Coverage Analysis

Analyze the test file @$1 and identify:
1. Untested functions
2. Missing edge cases
3. Coverage gaps
```

**Usage:**
```
/test-coverage tests/auth.test.js
# File contents included automatically
```

### Extended Thinking

Slash commands support extended thinking when prompt includes extended thinking keywords.

**Example:**
```markdown
---
description: Deep architectural analysis
model: opus
---

# Architecture Review

Perform deep analysis of the codebase architecture.

Use extended thinking to:
1. Understand system design patterns
2. Identify architectural trade-offs
3. Recommend improvements
```

---

## Working Examples

### Example 1: Simple Code Review

**File:** `.claude/commands/review.md`

```markdown
---
description: Review code for bugs and improvements
argument-hint: [file-path]
allowed-tools: Read, Grep
model: sonnet
---

# Code Review

Review the code at $ARGUMENTS for bugs and suggest improvements.

## Analysis Steps

1. Use Read to examine the code
2. Check for:
   - Logic errors
   - Edge cases
   - Security issues
   - Performance problems
3. Use Grep to find similar patterns in codebase
4. Suggest specific improvements with examples

## Output Format

**Issues Found:**
- [List issues with line numbers]

**Suggestions:**
- [Concrete improvements]

**Well Done:**
- [Positive observations]
```

**Usage:**
```
/review src/auth.py
/review
```

### Example 2: Git Commit with Conventional Format

**File:** `.claude/commands/commit.md`

```markdown
---
description: Create conventional commit
argument-hint: <type> <message>
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*)
model: haiku
---

# Conventional Commit

Create a commit with type: $1 and message: $2

## Pre-commit Context
- Status: !`git status`
- Staged: !`git diff --cached --stat`

## Instructions

1. Verify changes are appropriate for commit type $1
2. If no changes staged, use Bash to: `git add .`
3. Create commit: `git commit -m "$1: $2"`
4. Report commit hash and summary
```

**Usage:**
```
/commit feat "add user authentication"
/commit fix "resolve login timeout"
```

### Example 3: Deploy with Environment Validation

**File:** `.claude/commands/deploy.md`

```markdown
---
description: Deploy application to environment
argument-hint: <environment> [version]
allowed-tools: Bash(./deploy.sh:*), Read
---

# Deploy Application

Deploy to environment: $1
Version: $2 (latest if not specified)

## Pre-deployment Checks

1. Use Read to verify deploy.sh exists
2. Validate environment $1 is one of: dev, staging, prod
3. If $1 is "prod", require explicit confirmation
4. Check if version $2 is specified, default to "latest"

## Deployment

Execute: `./deploy.sh $1 $2`

## Post-deployment

Report deployment status and URL.
```

**Usage:**
```
/deploy staging
/deploy prod v2.1.0
```

### Example 4: Test Runner with Coverage

**File:** `.claude/commands/test.md`

```markdown
---
description: Run tests with coverage report
argument-hint: [test-path]
allowed-tools: Bash(pytest:*), Bash(npm:*), Read
model: haiku
---

# Run Tests

Run tests at: $ARGUMENTS (or all tests if not specified)

## Instructions

1. Use Read to detect test framework:
   - Check for pytest.ini → pytest
   - Check for jest.config.js → jest
   - Check for go.mod → go test

2. Run appropriate command:
   - pytest: `pytest $ARGUMENTS --cov --cov-report=term`
   - jest: `npm test -- $ARGUMENTS --coverage`
   - go: `go test $ARGUMENTS -cover`

3. Parse results and report:
   - Total tests run
   - Passed/Failed counts
   - Coverage percentage
   - Failed test details
```

**Usage:**
```
/test tests/auth/
/test
```

### Example 5: Project-Specific API Documentation

**File:** `.claude/commands/api-docs.md`

```markdown
---
description: Generate API documentation
allowed-tools: Read, Write, Grep
---

# Generate API Docs

Generate API documentation for project endpoints.

## Discovery

1. Use Grep to find all API route definitions:
   - Pattern: `@app.route|@router.get|@router.post`
2. For each route found, use Read to get full function

## Documentation Generation

For each endpoint, document:
- HTTP method and path
- Parameters (query, path, body)
- Response format
- Example request/response
- Error codes

## Output

Use Write to create: `docs/API.md`
```

**Usage:**
```
/api-docs
```

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Complex Multi-Step Workflows

**Problem:** Slash commands for complex workflows are hard to maintain and debug.

**Wrong:**
```markdown
---
description: Complete CI/CD pipeline
---

# Run Full Pipeline

1. Run linting
2. Run tests
3. Build application
4. Run security scan
5. Generate coverage report
6. Create deployment package
7. Upload to staging
8. Run smoke tests
9. Promote to production
10. Send notifications
```

**Why it's wrong:**
- Too many steps in single file
- Hard to reuse individual steps
- Error handling becomes complex
- Can't activate automatically based on context

**Better approach:** Use a **Skill** instead
```markdown
# Skill: ci-cd-pipeline/SKILL.md
---
name: ci-cd-pipeline
description: Manages complete CI/CD pipeline...
---

# CI/CD Pipeline

## Step 1: Linting
Load linting-rules.md and run checks...

## Step 2: Testing
Load test-config.md and execute...

[Supporting files in same directory]
```

**Key difference:**
- Skill auto-activates when relevant
- Can have multiple supporting files
- Better for complex, multi-step workflows

### ❌ Anti-Pattern 2: Requiring Supporting Files/Scripts

**Problem:** Slash commands are single files - if you need utilities, use Skills.

**Wrong:**
```markdown
# .claude/commands/security-scan.md
---
description: Run security scan
---

# Security Scan

1. Load threat-model.md for context
2. Load owasp-checklist.md for rules
3. Run scan-script.sh
4. Use security-patterns.json for detection
```

**Why it's wrong:**
- Slash commands can't reference other files in organized way
- No structure for supporting materials
- Scripts should be in Skills, not commands

**Better approach:** Use a **Skill**
```
.claude/skills/security-scanner/
├── SKILL.md              # Main instructions
├── threat-model.md       # Supporting docs
├── owasp-checklist.md    # Reference
└── scripts/
    └── scan.sh           # Utilities
```

### ❌ Anti-Pattern 3: Expecting Automatic Activation

**Problem:** Slash commands require explicit invocation - they don't auto-activate.

**Wrong:**
```markdown
---
description: Reviews security when analyzing code
---

# Security Review

When Claude sees code being analyzed, automatically check for security issues...
```

**Why it's wrong:**
- Slash commands only run when user types `/command-name`
- They don't activate based on context
- User must remember to invoke

**Better approach:** Use a **Skill**
```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities. Use when analyzing code, reviewing PRs, or when user mentions security.
---

# Security Review

[Claude activates this automatically when appropriate]
```

### ❌ Anti-Pattern 4: Overly Broad Tool Permissions

**Problem:** Granting all tools when only a few are needed.

**Wrong:**
```yaml
---
description: Review code
allowed-tools: Read, Write, Edit, Bash, Task, Grep, Glob
---
```

**Why it's wrong:**
- Command only needs Read, maybe Grep
- Granting Write/Edit/Bash is unnecessary risk
- User loses confidence in command safety

**Better approach:** Minimal necessary tools
```yaml
---
description: Review code
allowed-tools: Read, Grep
---
```

**Or for bash, specific commands only:**
```yaml
allowed-tools: Bash(git status:*), Bash(git diff:*)
# NOT: allowed-tools: Bash
```

### ❌ Anti-Pattern 5: Character Budget Bloat

**Problem:** Too many commands exceed 15K character budget for SlashCommand tool metadata.

**Symptom:** Warning in `/context`: "M of N commands visible to Claude"

**Wrong approach:** Create hundreds of project-specific commands
```
.claude/commands/
├── deploy-dev.md
├── deploy-staging.md
├── deploy-prod.md
├── test-unit.md
├── test-integration.md
├── test-e2e.md
[... 100+ more commands]
```

**Why it's wrong:**
- Exceeds character budget
- Claude can't see all commands
- SlashCommand tool becomes unreliable

**Better approach:** Consolidate with arguments
```
.claude/commands/
├── deploy.md          # Takes environment as $1
├── test.md            # Takes test type as $1
```

**Or use Skills for auto-activation:**
- Commands for explicit control (few, frequently used)
- Skills for automatic activation (many, context-based)

---

## Plugin & MCP Commands

### Plugin Commands

**Format:** `/plugin-name:command-name`

**Location:** `commands/` directory in plugin root

**Example plugin structure:**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── commands/
    ├── test.md     → /my-plugin:test
    └── deploy.md   → /my-plugin:deploy
```

**Features:**
- Support all custom command features
- Automatically discovered when plugin installed
- Namespaced to avoid conflicts

### MCP Slash Commands

**Format:** `/mcp__<server-name>__<prompt-name>`

**Example:**
```
/mcp__github__create_issue
/mcp__database__query
```

**Features:**
- Dynamically discovered from connected MCP servers
- Automatically available when server is active
- Permission wildcards: `mcp__github__*` approves all tools from github server

---

## SlashCommand Tool (Programmatic Invocation)

The SlashCommand tool allows Claude to invoke custom slash commands programmatically during conversation.

### How It Works

**When enabled:** Claude sees metadata for all custom commands and can invoke them when appropriate.

**Example conversation:**
```
User: Can you review the auth.py file?

Claude: I'll use the /review command.
[Invokes: SlashCommand tool with arguments: "/review src/auth.py"]
```

### Requirements

**For command to be invokable:**
- Must have `description` frontmatter field
- Must NOT have `disable-model-invocation: true`
- Must fit within character budget (15K default)

### Character Budget

**Default:** 15,000 characters for all SlashCommand metadata

**Customization:**
```bash
export SLASH_COMMAND_TOOL_CHAR_BUDGET=20000
```

**When exceeded:**
- Claude sees only subset of commands
- Warning in `/context`: "M of N commands visible"
- SlashCommand tool becomes unreliable

**Solution:**
- Reduce number of commands
- Use Skills for automatic activation
- Increase budget via environment variable

### Disabling SlashCommand Tool

**Disable all invocations:**
```
/permissions
# Add to deny rules: SlashCommand
```

**Disable specific command:**
```yaml
---
description: Dangerous operation
disable-model-invocation: true
---
```

**Permission patterns:**
```
SlashCommand:/commit           # Allow only /commit with no args
SlashCommand:/review-pr:*      # Allow /review-pr with any args
SlashCommand:*                 # Allow all commands
```

### Limitations

**Only supports CUSTOM commands:**
- ✅ Custom commands in `.claude/commands/`
- ✅ Personal commands in `~/.claude/commands/`
- ✅ Plugin commands
- ✅ MCP commands
- ❌ Built-in commands like `/compact`, `/init`, `/help`

---

## Common Mistakes When Creating Slash Commands

### Mistake 1: Using Slash Command When Skill Is Better

**Problem:** Creating slash command for capability that should auto-activate.

**Wrong:**
```markdown
# Command: /security-review

User must remember to type /security-review every time they want security analysis.
```

**Right:**
```markdown
# Skill: security-reviewer

Automatically activates when reviewing code or PRs. User doesn't need to remember.
```

**Decision rule:** If Claude should decide when to activate → Use Skill

### Mistake 2: Missing description Field

**Problem:** Command not visible to SlashCommand tool.

**Wrong:**
```yaml
---
argument-hint: <file-path>
---
```

**Right:**
```yaml
---
description: Review code for bugs and improvements
argument-hint: <file-path>
---
```

### Mistake 3: Vague Descriptions

**Problem:** Claude doesn't know when to invoke command.

**Wrong:**
```yaml
description: Code review
```

**Right:**
```yaml
description: Review code for bugs, security issues, and best practices
```

### Mistake 4: Granting Unnecessary Tool Access

**Problem:** Security risk and unclear command scope.

**Wrong:**
```yaml
allowed-tools: Read, Write, Edit, Bash, Task
# Command only reads files
```

**Right:**
```yaml
allowed-tools: Read, Grep
```

### Mistake 5: Not Using Namespacing

**Problem:** Unorganized commands in flat structure.

**Wrong:**
```
.claude/commands/
├── frontend-component.md
├── frontend-optimize.md
├── frontend-test.md
├── backend-api.md
├── backend-database.md
└── backend-deploy.md
```

**Right:**
```
.claude/commands/
├── frontend/
│   ├── component.md
│   ├── optimize.md
│   └── test.md
└── backend/
    ├── api.md
    ├── database.md
    └── deploy.md
```

---

## Testing Slash Commands

### Test Command Directly

1. **Create command file:**
   ```bash
   echo "---
   description: Test command
   ---
   Echo the argument: \$ARGUMENTS" > .claude/commands/test.md
   ```

2. **Restart Claude Code or reload commands**

3. **Test invocation:**
   ```
   /test hello world
   ```

4. **Verify:**
   - Command appears in `/help`
   - Executes with correct arguments
   - Produces expected output

### Test with Arguments

**Positional arguments:**
```
# Create command using $1, $2
/test-args first second third
```

**Verify:**
- $1 = "first"
- $2 = "second"
- $3 = "third"

### Test Tool Restrictions

**Command with Read only:**
```yaml
---
allowed-tools: Read
---
```

**Test:**
```
/test-command
# Try to use Write → Should fail
# Try to use Read → Should succeed
```

### Test Bash Execution

**Command with bash:**
```yaml
---
allowed-tools: Bash(git status:*)
---
## Status
!`git status`
```

**Test:**
- Verify git status output appears
- Verify other bash commands fail

### Test SlashCommand Tool

**Enable command for tool:**
```yaml
---
description: Review code for bugs
---
```

**Test:**
1. Check `/context` - Command should be listed
2. Ask Claude: "Can you review this file?"
3. Verify Claude invokes command automatically

**Disable and test:**
```yaml
disable-model-invocation: true
```

Verify command NOT in `/context` metadata.

---

## Summary Checklist

When creating a slash command, verify:

**File & Format:**
- [ ] File in `.claude/commands/` (project) or `~/.claude/commands/` (personal)
- [ ] Filename is kebab-case matching desired command name
- [ ] YAML frontmatter at top with `---` markers
- [ ] Content after frontmatter is instructions (not documentation)

**Frontmatter:**
- [ ] `description` field present (required for SlashCommand tool)
- [ ] `argument-hint` if command takes arguments
- [ ] `allowed-tools` restricts to necessary tools only
- [ ] `model` specified if cost/performance optimization needed
- [ ] `disable-model-invocation: true` if shouldn't auto-invoke

**Content:**
- [ ] Written as instructions ("Do this") not documentation ("This command...")
- [ ] Uses $ARGUMENTS or $1, $2, $3 for argument handling
- [ ] Clear steps or workflow
- [ ] Output format specified if relevant

**Decision:**
- [ ] Verified slash command is right primitive (not Skill or Subagent)
- [ ] Simple, focused, single-file operation
- [ ] User should explicitly invoke (not auto-activate)

**Testing:**
- [ ] Command appears in `/help`
- [ ] Arguments work correctly
- [ ] Tool restrictions enforced
- [ ] Bash execution works (if used)
- [ ] SlashCommand tool can invoke (if enabled)

---

## Reference

**Official Documentation:**
- https://code.claude.com/docs/en/slash-commands

**Related Primitives:**
- Skills: Auto-activating capabilities
- Subagents: Isolated execution contexts
- Hooks: Event-triggered automation

**Tools:**
- `/help` - List all available commands
- `/context` - View SlashCommand tool metadata
- `/permissions` - Manage tool permissions
