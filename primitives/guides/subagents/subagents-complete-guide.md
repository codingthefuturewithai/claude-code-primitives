# Subagents: Complete Guide

**Metadata for RAG Memory:**
- primitive_type: subagent
- content_type: complete-guide
- version: 1.0

---

## What Are Subagents?

Subagents are **specialized Claude instances** spawned via the Task tool to handle specific work in isolated context or parallel execution.

**Key characteristics:**
- **Isolated context** - Fresh conversation, doesn't see main session history
- **Parallel execution** - Multiple subagents can run simultaneously
- **Specialized expertise** - Can have skills attached for domain knowledge
- **Tool access** - Inherits tools or can be restricted
- **Programmatic invocation** - Launched via Task tool, not user-invoked

### Subagents vs Other Primitives

| Feature | Subagents | Skills | Slash Commands |
|---------|-----------|--------|----------------|
| Invocation | Via Task tool | Auto (Claude decides) | Manual (user types) |
| Context | Isolated/fresh | Shared | Shared |
| Parallel | Yes | No | No |
| Expertise | Via skills field | Via SKILL.md | N/A |
| Tool Access | Inherits or restricted | Via allowed-tools | Via allowed-tools |

---

## When to Use Subagents

Use subagents when:
- **Parallel execution needed** - Run multiple analyses simultaneously
- **Isolated context required** - Don't want to pollute main conversation
- **Specialized expertise** - Need specific skills for this task
- **Large analysis tasks** - Keep main session clean while doing heavy work
- **Consistent role/perspective** - Want same agent behavior across invocations

Do NOT use subagents when:
- **Simple single-purpose task** - Use Slash Command instead
- **User should control invocation** - Use Slash Command
- **Need automatic activation** - Use Skill instead
- **External API integration** - Use MCP Server

---

## File Format

Subagents are defined in markdown files with YAML frontmatter:

```
.claude/agents/
  code-reviewer.md
  pattern-analyzer.md
  test-generator.md

~/.claude/agents/
  security-expert.md
  documentation-writer.md
```

---

## YAML Frontmatter Format

### Required Fields

```yaml
---
name: subagent-name
description: What this subagent specializes in and when to use it
---
```

### Optional Fields

```yaml
---
name: subagent-name
description: Specialized subagent for [purpose]
skills: [skill-1, skill-2]
model: sonnet
allowed-tools: [Tool1, Tool2]
---
```

### Field Specifications

**name:** (required, string)
- Kebab-case, lowercase
- No spaces, use hyphens
- Example: `code-reviewer`, `pattern-analyzer`, `security-expert`

**description:** (required, string)
- Explains subagent's specialization and when to use it
- Used in Task tool `subagent_type` parameter
- Be specific about expertise area
- Good: "Specialized agent for analyzing code patterns and identifying best practices to follow"
- Bad: "Code analysis agent" (too vague)

**skills:** (optional, array of strings)
- Skills to attach to this subagent
- Skills give the subagent domain expertise
- Example: `skills: [security-reviewer, code-quality]`
- Skills must exist in .claude/skills/ or ~/.claude/skills/

**model:** (optional, string)
- Override model for this subagent
- Values: "sonnet", "opus", "haiku"
- Default: Inherits from session
- Use haiku for simple/fast analysis, opus for complex reasoning
- Example: `model: haiku` for quick pattern scanning

**allowed-tools:** (optional, array)
- Restrict which tools subagent can use
- If omitted: subagent inherits all tools from parent
- If specified: subagent can ONLY use these tools
- Use to prevent subagent from making unwanted changes
- Example: `allowed-tools: [Read, Glob, Grep]` (read-only analysis)

### Example - Complete Frontmatter

```yaml
---
name: security-expert
description: Specialized agent for security analysis of code changes. Use when analyzing commits, PRs, or new code for security vulnerabilities, threat modeling, and OWASP compliance.
skills: [security-reviewer, threat-modeler]
model: sonnet
allowed-tools: [Read, Bash, Grep, Glob]
---
```

---

## Content Format: Instructions (Not Documentation)

Subagent content should be written as **instructions for the subagent**, not explanations of what it does.

### ❌ Documentation Style (Wrong)

```markdown
This subagent performs code reviews by checking code quality, style, and best practices. It can identify issues and suggest improvements.
```

**Why it's wrong:** Describes WHAT the subagent is, not HOW to do its work.

### ✅ Instructions Style (Correct)

```markdown
You are a code review expert. When invoked:

## Step 1: Understand Scope
Review the code provided in the invocation prompt.

## Step 2: Analyze Code Quality
Check for:
- Naming conventions
- Code duplication
- Function complexity (>50 lines = too complex)
- Missing error handling

## Step 3: Check Best Practices
Review against language-specific best practices:
- Python: PEP 8, type hints
- JavaScript: ESLint rules, modern syntax
- Go: Effective Go guidelines

## Step 4: Present Findings
Format as:
**Issues:**
- [file:line] [issue description]

**Suggestions:**
- [improvement with example]

**Approved:** [what's well done]
```

**Why it's correct:** Tells subagent exactly WHAT TO DO, step by step.

---

## Invoking Subagents

Subagents are invoked using the Task tool:

### Basic Invocation

```
Task(
    subagent_type="code-reviewer",
    description="Review authentication changes",
    prompt="Review the changes in auth.py for security issues and code quality"
)
```

### Parameters

- **subagent_type:** (required) Name of subagent (matches `name` field)
- **description:** (required) Short 3-5 word description of task
- **prompt:** (required) Detailed task for subagent
- **model:** (optional) Override model ("sonnet", "opus", "haiku")
- **run_in_background:** (optional) If true, runs async

### Who Can Invoke Subagents

**Slash Commands can invoke subagents:**
```markdown
---
description: Get help with primitives
allowed-tools: [Task]
---

Use Task tool with subagent_type="primitive-consultant" to guide the developer.
```

**Skills can invoke subagents:**
```yaml
---
name: architecture-reviewer
allowed-tools: [Read, Task, Bash]
---

When reviewing architecture:

## Step 1: Analyze Current State
Read relevant files.

## Step 2: Invoke Pattern Analyzer
Task(
    subagent_type="pattern-analyzer",
    description="Analyze design patterns",
    prompt="Analyze the design patterns in {files} and identify consistency issues"
)
```

**Main conversation can invoke subagents:**
User can't directly, but Claude can decide to use Task tool to invoke subagent.

**Subagents CANNOT invoke other subagents:**
This is an anti-pattern. Subagents should not spawn more subagents.

---

## Working Examples

### Example 1: Code Reviewer Subagent

**File: `.claude/agents/code-reviewer.md`**

```yaml
---
name: code-reviewer
description: Review code changes for quality, style, and best practices. Use when commits are made or code review is requested.
skills: [code-quality]
model: sonnet
allowed-tools: [Read, Bash, Grep, Glob]
---

You are a code review expert. When invoked:

## Your Role
Provide constructive code review feedback focused on quality, maintainability, and best practices.

## Step 1: Identify Files
If not specified in prompt, run:
`git diff --name-only HEAD~1`

## Step 2: Review Each File
For each file:
1. Read file content
2. Check naming conventions
3. Look for code duplication
4. Identify overly complex functions
5. Verify error handling

## Step 3: Apply Language-Specific Rules
**Python:**
- PEP 8 compliance
- Type hints present
- Docstrings for functions

**JavaScript:**
- Modern syntax (const/let, not var)
- Async/await over callbacks
- Proper error handling

**Go:**
- Error handling every error return
- Exported functions have comments
- Follows Effective Go

## Step 4: Present Findings

**Format:**
```
## Issues Found
- [file:line] [description]

## Suggestions
- [improvement with code example]

## Well Done
- [positive feedback]
```

## Step 5: Rate Severity
For each issue:
- 🔴 Critical: Must fix (breaks functionality, security risk)
- 🟡 Important: Should fix (quality/maintainability issue)
- 🟢 Optional: Nice to have (style preference)
```

**How to invoke:**
```
Task(
    subagent_type="code-reviewer",
    description="Review recent changes",
    prompt="Review the changes in the last commit for code quality issues"
)
```

### Example 2: Pattern Analyzer Subagent

**File: `.claude/agents/pattern-analyzer.md`**

```yaml
---
name: pattern-analyzer
description: Analyze codebase to discover existing patterns and conventions. Use when implementing new features to ensure consistency.
model: haiku
allowed-tools: [Read, Glob, Grep, Bash]
---

You are a pattern discovery expert. When invoked:

## Your Role
Analyze existing code to identify patterns that new code should follow.

## Step 1: Understand Target
Based on prompt, identify what patterns to discover:
- File organization
- Naming conventions
- Error handling approaches
- Testing patterns
- Logging patterns

## Step 2: Search Codebase
Use Glob and Grep to find examples:
- Glob to find files of same type
- Grep to find pattern usage
- Read sample files

## Step 3: Identify Patterns
For each pattern category:
1. Find 3-5 examples
2. Identify common approach
3. Note variations
4. Document the pattern

## Step 4: Report Findings

**Format:**
```
## Patterns Discovered

### File Organization
- Controllers in /controllers/{domain}/{action}.py
- Tests in /tests/{domain}/test_{file}.py

### Naming Conventions
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE

### Error Handling
- Use custom exceptions from /lib/exceptions.py
- Log errors with logger.error()
- Return {"error": "message"} format

### Testing Patterns
- Fixtures in conftest.py
- Test class per module
- Use pytest.mark.parametrize for cases

## Recommendations
Follow these patterns in new implementation:
- [Specific guidance for current task]
```
```

**How to invoke:**
```
Task(
    subagent_type="pattern-analyzer",
    description="Discover existing patterns",
    prompt="Analyze the codebase to find patterns for API endpoint structure and error handling that I should follow"
)
```

### Example 3: Primitive Consultant Agent (Real Example)

**File: `~/.claude/agents/primitive-consultant-agent.md`**

```yaml
---
name: primitive-consultant-agent
description: Specialized agent for guiding developers through Claude Code primitive creation. Use when developer needs help creating slash commands, skills, subagents, MCP servers, hooks, or plugins.
skills: [primitive-consultant]
model: sonnet
---

You are a Claude Code primitives expert. Your job is to guide developers through creating the right primitive for their needs.

When invoked, the primitive-consultant skill is available to you. Use it to:

1. Understand what the developer is trying to build
2. Scan for existing primitives to prevent duplicates
3. Recommend the correct primitive type (slash command, skill, subagent, MCP server, hook, or plugin)
4. Gather complete requirements
5. Guide creation using RAG Memory best practices

The primitive-consultant skill has access to:
- Decision framework for choosing primitive types
- Requirements gathering templates for all 6 primitive types
- Composition rules for valid primitive combinations
- Anti-patterns to avoid

Follow the skill's 8-step consultation workflow to ensure the developer builds the right solution.
```

**How to invoke:**
```markdown
---
description: Get help designing Claude Code primitives
---

Use the Task tool with subagent_type="primitive-consultant-agent" to guide the developer through the primitive creation process.

Report what the primitive-consultant-agent recommends.
```

**This example shows:**
- Subagent with attached skill (primitive-consultant)
- Invoked by slash command (/create-primitive)
- Uses sonnet model for complex reasoning
- No allowed-tools restriction (inherits all tools)

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Subagent Invoking Subagent

**WRONG:**
```yaml
---
name: orchestrator
allowed-tools: [Task]
---

When invoked:
1. Invoke security-expert subagent
2. Invoke code-reviewer subagent
3. Invoke test-generator subagent
```

**Why it's wrong:** Subagents should not spawn other subagents. This creates deep nesting and loses context.

**RIGHT:** Have main conversation or slash command invoke multiple subagents in parallel:
```
# In slash command or main conversation
Task(subagent_type="security-expert", ...)
Task(subagent_type="code-reviewer", ...)
Task(subagent_type="test-generator", ...)
```

### ❌ Anti-Pattern 2: Using Subagent for User-Invoked Tasks

**WRONG:** Creating subagent that user should invoke directly

**Why it's wrong:** Users can't invoke subagents. Use Slash Command instead.

**RIGHT:** Slash Command → Subagent pattern:
```markdown
---
description: Review code quality
---

Use Task tool with subagent_type="code-reviewer" to review code.
```

### ❌ Anti-Pattern 3: Documentation Instead of Instructions

**WRONG:**
```markdown
This subagent reviews code and provides feedback.
```

**Why it's wrong:** Doesn't tell subagent HOW to do the work.

**RIGHT:**
```markdown
You are a code reviewer. When invoked:

## Step 1: Get code to review
[Instructions]

## Step 2: Analyze quality
[Instructions]
```

### ❌ Anti-Pattern 4: Missing Context in Invocation

**WRONG:**
```
Task(
    subagent_type="code-reviewer",
    description="Review code",
    prompt="Review the code"
)
```

**Why it's wrong:** Subagent has isolated context - doesn't know what code to review.

**RIGHT:**
```
Task(
    subagent_type="code-reviewer",
    description="Review auth changes",
    prompt="Review the authentication changes in src/auth.py and src/middleware/auth.js for security issues. Pay special attention to JWT token validation and session management."
)
```

### ❌ Anti-Pattern 5: Unnecessary Isolation

**WRONG:** Creating subagent for simple task that doesn't need isolation

**Why it's wrong:** Subagents add overhead. Use Slash Command for simple tasks in shared context.

**RIGHT:** Only use subagents when you actually need isolation or parallelism.

---

## Skills Integration

### Attaching Skills to Subagents

Skills give subagents specialized expertise:

```yaml
---
name: security-expert
description: Security analysis specialist
skills: [security-reviewer, threat-modeler, owasp-checker]
---
```

**How it works:**
- Subagent has access to all attached skills
- Skills provide their tools via allowed-tools
- Skills can reference supporting documentation
- Skills define multi-step workflows

### When to Attach Skills

**Attach skills when:**
- Subagent needs domain expertise
- Expertise is reusable across subagents
- Workflow is complex and well-defined

**Don't attach skills when:**
- Simple analysis (just write instructions in subagent)
- One-time specialized task (instructions in subagent sufficient)

### Example: Subagent with Multiple Skills

```yaml
---
name: full-stack-reviewer
description: Comprehensive code review for full-stack changes
skills: [frontend-reviewer, backend-reviewer, database-reviewer, security-reviewer]
model: sonnet
---

You are a full-stack code review expert. When invoked:

## Step 1: Categorize Files
Group changed files by layer:
- Frontend (UI components, styles)
- Backend (APIs, business logic)
- Database (migrations, queries)

## Step 2: Activate Appropriate Skills
For each category, use the relevant skill:
- Frontend files → frontend-reviewer skill
- Backend files → backend-reviewer skill
- Database files → database-reviewer skill
- All files → security-reviewer skill

## Step 3: Synthesize Findings
Combine findings from all skills into cohesive review.
```

---

## Parallel Execution

Multiple subagents can run simultaneously:

### Example: Parallel Analysis

```markdown
---
description: Comprehensive code analysis
allowed-tools: [Task, Read]
---

Run parallel analyses using subagents:

1. Security analysis:
   Task(
       subagent_type="security-expert",
       description="Security analysis",
       prompt="Analyze {files} for security vulnerabilities",
       run_in_background=True
   )

2. Performance analysis:
   Task(
       subagent_type="performance-analyzer",
       description="Performance analysis",
       prompt="Analyze {files} for performance issues",
       run_in_background=True
   )

3. Quality analysis:
   Task(
       subagent_type="code-reviewer",
       description="Quality analysis",
       prompt="Review {files} for code quality",
       run_in_background=True
   )

Wait for all to complete, then synthesize findings.
```

**Benefits of parallel execution:**
- Faster results (analyses run concurrently)
- Independent analyses (each in own context)
- Specialized perspectives (each subagent focuses on one area)

---

## Location: Project vs Personal

### Project Subagents (`.claude/agents/`)

Use when:
- Subagent specific to this project's domain
- Contains project-specific expertise
- Team wants same agent behavior
- Example: `api-design-reviewer` for project with specific API standards

### Personal Subagents (`~/.claude/agents/`)

Use when:
- Subagent applies across all your projects
- General expertise (security, testing, patterns)
- Your personal workflow preferences
- Example: `commit-message-helper` for your commit style

---

## Tool Access Control

### Inheriting All Tools

If `allowed-tools` omitted, subagent inherits all tools from parent:

```yaml
---
name: full-access-agent
description: Agent with full tool access
---
```

**When to use:** Subagent needs to do actual work (edit files, run commands)

### Restricting Tools

If `allowed-tools` specified, subagent can ONLY use those tools:

```yaml
---
name: read-only-analyzer
description: Analysis-only agent
allowed-tools: [Read, Glob, Grep]
---
```

**When to use:**
- Subagent should only analyze, not modify
- Prevent accidental changes
- Security/safety (analysis only)

### Common Tool Combinations

**Read-only analysis:**
```yaml
allowed-tools: [Read, Glob, Grep]
```

**Analysis with command execution:**
```yaml
allowed-tools: [Read, Glob, Grep, Bash]
```

**Full code modification:**
```yaml
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
```

**Orchestration (invoke other subagents):**
```yaml
allowed-tools: [Task, Read, Bash]
```

---

## Testing Subagents

### How to Test a Subagent

1. **Create subagent** in appropriate directory
2. **Invoke via Task tool** with clear prompt
3. **Verify behavior** - does it follow instructions?
4. **Check output** - is it useful and complete?
5. **Test edge cases** - how does it handle unclear situations?

### Example Test

**Subagent:** `pattern-analyzer` for discovering code patterns

**Test:**
```
Task(
    subagent_type="pattern-analyzer",
    description="Discover error patterns",
    prompt="Analyze the codebase to discover how error handling is implemented. Look at existing error handlers and identify the standard pattern I should follow."
)
```

**Expected output:**
- List of error handling patterns found
- Examples from codebase
- Recommendation for what pattern to follow
- Specific guidance for current task

### Debugging Subagents

**Subagent gives incomplete response?**
- Check prompt - is it detailed enough?
- Subagent has isolated context - include all needed info in prompt
- Example: Don't say "the files" - specify exact file paths

**Subagent can't do its work?**
- Check allowed-tools - does it have what it needs?
- If restricted, add necessary tools
- If using skills, check skill's allowed-tools

**Subagent behavior inconsistent?**
- Instructions too vague - be more specific
- Add step-by-step format
- Include examples in instructions

---

## Common Mistakes When Creating Subagents

### Mistake 1: Creating Subagent for Simple Task

**What developers think:** "I need a subagent to format code"

**Reality:** Simple tasks don't need isolation - use Slash Command or Hook

**Fix:** Only use subagents for complex analysis or parallel execution

### Mistake 2: Expecting User to Invoke

**What developers think:** "Users will type /use-subagent"

**Reality:** Users can't invoke subagents directly - only via Task tool

**Fix:** Create Slash Command that invokes subagent:
```markdown
---
description: Analyze patterns
allowed-tools: [Task]
---

Use Task tool with subagent_type="pattern-analyzer" to discover patterns.
```

### Mistake 3: Subagent Invoking Subagent

**What developers think:** "Subagent will orchestrate other subagents"

**Reality:** Subagent → Subagent is anti-pattern

**Fix:** Have main conversation or slash command invoke multiple subagents in parallel

### Mistake 4: Vague Invocation Prompt

**What developers think:** "Subagent will figure out what I want"

**Reality:** Subagent has isolated context - needs explicit information

**Fix:** Include all necessary context in prompt:
```
Task(
    subagent_type="code-reviewer",
    prompt="Review src/auth.py (attached) for security issues. Focus on JWT validation and session management. Check against OWASP Top 10."
)
```

---

## Summary Checklist

When creating a subagent, verify:

- [ ] YAML frontmatter has required fields (name, description)
- [ ] name is kebab-case lowercase
- [ ] description explains specialization and when to use
- [ ] skills field lists existing skills (if using expertise)
- [ ] allowed-tools restricts tools if read-only (or omitted for full access)
- [ ] model specified if different from default (haiku for fast, opus for complex)
- [ ] Content written as INSTRUCTIONS (what subagent should do)
- [ ] NOT written as documentation (what subagent is)
- [ ] Steps are clear and actionable
- [ ] Located in correct directory (.claude/agents/ or ~/.claude/agents/)
- [ ] Subagent is appropriate choice (needs isolation or parallelism)
- [ ] Invocation pattern planned (who/how will invoke this)

---

## Reference

**Official Claude Code Subagents Documentation:**
- [Subagents Guide](https://docs.anthropic.com/claude/docs/subagents)
- [Task Tool](https://docs.anthropic.com/claude/docs/task-tool)

**Required Frontmatter Fields:** name, description

**Optional Frontmatter Fields:** skills, model, allowed-tools

**Valid Model Values:** sonnet, opus, haiku

**Invocation:** Via Task tool with subagent_type parameter

**Tool Access:** Inherits all if allowed-tools omitted, restricted if specified

**Directory Locations:**
- Project: `.claude/agents/[name].md`
- Personal: `~/.claude/agents/[name].md`

**Anti-Pattern:** Subagent → Subagent (use parallel invocation from main/slash command instead)
