# Skills: Complete Guide

**Metadata for RAG Memory:**
- primitive_type: skill
- content_type: complete-guide
- version: 1.0

---

## What Are Skills?

Skills are **complex, multi-step workflows** that Claude Code activates automatically when it detects a matching situation. They are Claude's specialized expertise areas.

**Key characteristics:**
- **Auto-activate** - Claude decides when to use them based on context
- **Multi-step** - Handle complex workflows with multiple phases
- **Expert knowledge** - Encapsulate domain expertise (security, testing, architecture, etc.)
- **Tool access** - Can use allowed-tools to do real work
- **Supporting files** - Can reference additional documentation loaded on demand

### Skills vs Other Primitives

| Feature | Skills | Slash Commands | Subagents |
|---------|--------|----------------|-----------|
| Invocation | Auto (Claude decides) | Manual (user types /cmd) | Programmatic (via Task tool) |
| Complexity | Multi-step workflows | Simple single-purpose | Parallel execution |
| Tool Access | Via allowed-tools field | Via allowed-tools field | Inherits or restricted |
| Supporting Files | Yes (progressive disclosure) | No | No |
| Context | Shared with main session | Shared with main session | Isolated |

---

## When to Use Skills

Use skills when:
- **Complex multi-step workflow** - More than just "do X"
- **Claude should auto-activate** - Don't want to remember to invoke manually
- **Domain expertise needed** - Security reviews, code reviews, architecture analysis
- **Supporting documentation required** - Decision frameworks, patterns, templates
- **Repeated use across projects** - Want behavior available everywhere

Do NOT use skills when:
- **User wants explicit control** - Use Slash Command instead (user types /command when they want it)
- **Simple single-purpose task** - Use Slash Command (skills are for complex workflows)
- **Needs parallel execution** - Use Subagent (skills run in main conversation)
- **External API integration** - Use MCP Server (skills don't directly integrate APIs)

---

## File Structure

Skills use **progressive disclosure** - main file (SKILL.md) + supporting files loaded on demand:

```
~/.claude/skills/
  security-reviewer/
    SKILL.md              # Main instructions (REQUIRED)
    threat-model.md       # Supporting doc (loaded when needed)
    owasp-checklist.md    # Supporting doc (loaded when needed)
    common-vulns.md       # Supporting doc (loaded when needed)
```

### Why Progressive Disclosure?

**Problem:** Loading all documentation at once wastes tokens

**Solution:**
- SKILL.md contains workflow + when to load supporting files
- Supporting files loaded only when needed via Read tool
- Example: "For OWASP checklist, use Read('~/.claude/skills/security-reviewer/owasp-checklist.md')"

---

## YAML Frontmatter Format

### Required Fields

```yaml
---
name: skill-name-here
description: When Claude should activate this skill (critical - this is the detection trigger)
allowed-tools: [Tool1, Tool2, Tool3]
---
```

### Field Specifications

**name:** (required, string)
- Kebab-case, lowercase
- No spaces, use hyphens
- Example: `security-reviewer`, `test-generator`, `architecture-analyzer`

**description:** (required, string)
- **CRITICAL:** This is how Claude decides when to activate the skill
- Be specific about WHEN to use, not WHAT it does
- Good: "Review code changes for security vulnerabilities when user commits or requests security analysis"
- Bad: "A security review skill" (too vague)
- Include trigger conditions: keywords, actions, contexts

**allowed-tools:** (required, array)
- List of tools this skill can use
- Common: Read, Write, Edit, Bash, Glob, Grep, Task
- MCP tools: Must use full name (e.g., `mcp__rag-memory__search_documents`)
- Empty array NOT allowed - skills must be able to DO something

### Optional Fields

**model:** (optional, string)
- Override model for this skill
- Values: "sonnet", "opus", "haiku"
- Default: Inherits from session
- Use haiku for simple/fast skills, opus for complex reasoning

**Example - Complete Frontmatter:**
```yaml
---
name: security-reviewer
description: Automatically review code changes for security vulnerabilities when user commits, pushes, or explicitly requests security analysis. Activates on keywords like security, vulnerability, OWASP, threat model.
allowed-tools: [Read, Bash, Grep, Glob, mcp__rag-memory__search_documents]
model: sonnet
---
```

---

## Content Format: Instructions (Not Documentation)

Skills should be written as **step-by-step instructions**, not explanations of what the skill does.

### ❌ Documentation Style (Wrong)

```markdown
This skill performs security reviews by checking for common vulnerabilities.
It looks for SQL injection, XSS, and authentication issues.
The skill can also check OWASP Top 10.
```

**Why it's wrong:** This describes WHAT the skill is, not HOW to do the work.

### ✅ Instructions Style (Correct)

```markdown
When activated, perform security review:

## Step 1: Identify Changed Files
Use Bash to run `git diff --name-only` to see modified files.

## Step 2: Scan for Common Vulnerabilities
For each file:
1. Read file content
2. Check for:
   - SQL concatenation (SQL injection risk)
   - innerHTML usage (XSS risk)
   - Missing authentication checks

## Step 3: Load OWASP Checklist
Use Read('~/.claude/skills/security-reviewer/owasp-checklist.md')

## Step 4: Report Findings
Present findings in format:
- 🔴 Critical: [issue]
- 🟡 Warning: [issue]
- 🟢 Pass: [check]
```

**Why it's correct:** This tells Claude exactly WHAT TO DO, step by step.

---

## Working Examples

### Example 1: Security Reviewer Skill

**File: `~/.claude/skills/security-reviewer/SKILL.md`**

```yaml
---
name: security-reviewer
description: Review code changes for security vulnerabilities when user commits, pushes, or requests security analysis
allowed-tools: [Read, Bash, Grep, Glob]
---

When activated, perform security review of code changes:

## Step 1: Identify Scope
If user just committed:
- Run `git diff --name-only HEAD~1` to see changed files
If user specified files:
- Use those files

## Step 2: Language-Specific Checks

For Python files:
1. Check for SQL concatenation: `grep -r "execute.*%.*format" {files}`
2. Check for eval() usage: `grep -r "eval(" {files}`
3. Check for pickle usage: `grep -r "pickle.loads" {files}`

For JavaScript files:
1. Check for innerHTML: `grep -r "innerHTML" {files}`
2. Check for eval: `grep -r "eval(" {files}`
3. Check for dangerouslySetInnerHTML: `grep -r "dangerouslySetInnerHTML" {files}`

## Step 3: Load Threat Model If Needed
If complex authentication/authorization logic found:
- Use Read('~/.claude/skills/security-reviewer/threat-model.md')

## Step 4: Report Findings

Format:
🔴 **Critical** (must fix before merge):
- [Finding with file:line reference]

🟡 **Warning** (should review):
- [Finding with file:line reference]

🟢 **Pass**: No critical security issues found

## Step 5: Explain Findings
For each finding:
- What the vulnerability is
- Why it's dangerous
- How to fix it
- Reference: [OWASP category or CWE number]
```

**Supporting File: `~/.claude/skills/security-reviewer/threat-model.md`**

```markdown
# Threat Modeling Framework

When reviewing authentication/authorization:

## Questions to Ask:
1. Who can access this resource?
2. What authorization checks exist?
3. Can users escalate privileges?
4. Are sessions properly managed?
5. Is sensitive data properly protected?

## Common Auth Vulnerabilities:
- Missing authorization checks
- Insecure direct object references
- Session fixation
- JWT algorithm confusion
- Privilege escalation paths
```

### Example 2: Test Generator Skill

**File: `~/.claude/skills/test-generator/SKILL.md`**

```yaml
---
name: test-generator
description: Generate tests when user creates new functions, classes, or explicitly requests test creation
allowed-tools: [Read, Write, Glob, Grep, Bash]
model: sonnet
---

When activated, generate appropriate tests:

## Step 1: Discover Test Framework
Check project for test framework:
- Python: Look for pytest.ini, look for `import unittest`
- JavaScript: Check package.json for jest/mocha/vitest
- Go: Standard library testing

Use Glob to find existing test files, determine naming convention.

## Step 2: Analyze Code to Test
Read the file containing code to test.
Identify:
- Function signatures
- Edge cases (nulls, empty arrays, boundary conditions)
- Error paths
- Dependencies to mock

## Step 3: Load Test Patterns
Based on framework discovered:
- Read('~/.claude/skills/test-generator/pytest-patterns.md')
- Read('~/.claude/skills/test-generator/jest-patterns.md')
- Read('~/.claude/skills/test-generator/go-patterns.md')

## Step 4: Generate Tests
Create test file following project conventions:
- Use discovered naming pattern
- Follow framework patterns from supporting files
- Include:
  - Happy path tests
  - Edge case tests
  - Error handling tests
  - Mock setup if needed

## Step 5: Verify Tests Run
Run test command for framework:
- pytest: `pytest {test_file} -v`
- jest: `npm test {test_file}`
- go: `go test {package}`

Report results and fix any issues.
```

### Example 3: Primitive Consultant Skill (Real Example)

**File: `~/.claude/skills/primitive-consultant/SKILL.md`**

```yaml
---
name: primitive-consultant
description: Help developers design Claude Code solutions using primitives. Analyzes problems, recommends architecture, gathers requirements. Use when developer wants to automate workflows, solve problems with Claude Code, create primitives, or mentions slash commands, skills, subagents, MCP servers, hooks, or plugins.
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit, mcp__rag-memory__search_documents, mcp__rag-memory__list_collections, mcp__rag-memory__get_collection_info]
---

When a developer wants to create a Claude Code primitive or automate a workflow, guide them through the consultation process:

## Step 1: Understand the Problem
Ask 2-3 questions maximum:
1. "What task are you trying to accomplish or automate?"
2. "How will you use this - invoke it yourself, or have Claude activate it automatically?"
3. "Is this just for you, or for your whole team?"

## Step 2: Analyze Existing Primitives (REQUIRED - NEVER SKIP)
Use Bash to scan both project-level (.claude/) and personal (~/.claude/) directories:

```bash
echo "=== Project-level primitives (.claude/) ===" && \
ls -la .claude/commands/*.md 2>/dev/null || echo "No commands found" && \
ls -la .claude/skills/*/SKILL.md 2>/dev/null || echo "No skills found" && \
ls -la .claude/agents/*.md 2>/dev/null || echo "No agents found"
```

If similar primitive exists: STOP and recommend using/modifying existing.

## Step 3: Apply Decision Framework
Use Read to load decision framework:
Read("~/.claude/skills/primitive-consultant/decision-framework.md")

Determine primary primitive type based on logic.

## Step 4: Check Composition Needs
If multiple primitives needed, use Read:
Read("~/.claude/skills/primitive-consultant/composition-patterns.md")

## Step 5: Present Recommendation
Format:
```
PRIMARY: [Type]
WHY: [Reason based on requirements]
LOCATION: [.claude/ or ~/.claude/]
EXISTING PRIMITIVES FOUND: [List or "None"]
```

## Step 6: Get Confirmation
Ask: "Does this approach work for you?"

## Step 7: Gather Detailed Requirements
Load appropriate guide:
- Read("~/.claude/skills/primitive-consultant/slash-commands-guide.md")
- Read("~/.claude/skills/primitive-consultant/skills-guide.md")
- etc.

Gather complete requirements.

## Step 8: Search RAG Memory and Create
Search for best practices:
```
mcp__rag-memory__search_documents(
    query="How do I create a [type] with the correct format and content structure?",
    collection_name="claude-code-primitives",
    metadata_filter={"primitive_type": "[type]", "content_type": "complete-guide"},
    limit=5
)
```

Verify retrieved: format specs, content crafting guidance, examples, anti-patterns.

Create the primitive file(s) using Write/Edit tools.
```

**This example shows:**
- Multi-step workflow (8 steps)
- Tool usage (Bash, Read, Write, MCP tools)
- Progressive disclosure (loads supporting files as needed)
- RAG Memory integration
- Clear instructions at each step

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Vague Description

**WRONG:**
```yaml
description: A code review skill
```

**Why it's wrong:** Claude won't know WHEN to activate this.

**RIGHT:**
```yaml
description: Review code changes when user commits, pushes, or explicitly requests code quality review. Activates on keywords like review, quality, refactor, clean up.
```

### ❌ Anti-Pattern 2: Documentation Instead of Instructions

**WRONG:**
```markdown
This skill analyzes code and provides feedback.
It checks for style issues and suggests improvements.
```

**Why it's wrong:** Doesn't tell Claude WHAT TO DO.

**RIGHT:**
```markdown
When activated:

## Step 1: Get Code to Review
Run `git diff --name-only` to see changed files.

## Step 2: Check Each File
For each file:
1. Read file content
2. Check for style issues
3. Note improvement opportunities

## Step 3: Present Feedback
Format findings as actionable items.
```

### ❌ Anti-Pattern 3: Missing allowed-tools

**WRONG:**
```yaml
---
name: test-runner
description: Run tests when user requests
allowed-tools: []
---
```

**Why it's wrong:** Skill can't do anything without tools. It needs at least Bash to run tests.

**RIGHT:**
```yaml
allowed-tools: [Bash, Read, Glob]
```

### ❌ Anti-Pattern 4: Loading All Supporting Files Upfront

**WRONG:**
```markdown
First, load all documentation:
- Read('doc1.md')
- Read('doc2.md')
- Read('doc3.md')
- Read('doc4.md')
```

**Why it's wrong:** Wastes tokens loading docs you might not need.

**RIGHT:**
```markdown
## Step 3: Load Specific Documentation If Needed
If Python code: Read('python-patterns.md')
If JavaScript code: Read('js-patterns.md')
```

### ❌ Anti-Pattern 5: Using Skill for Simple Tasks

**WRONG:** Creating a skill to format code (just call formatter directly)

**Why it's wrong:** Skills are for COMPLEX workflows. Simple tasks should be Slash Commands or Hooks.

**RIGHT:** Use Hook for auto-formatting:
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "black {file_path}"
    }
  }
}
```

---

## Location: Project vs Personal

### Project Skills (`.claude/skills/`)

Use when:
- Skill specific to this project's domain
- Contains project-specific patterns/conventions
- Team wants same expertise across their work
- Example: `api-design-reviewer` for project with specific API standards

### Personal Skills (`~/.claude/skills/`)

Use when:
- Skill applies across all your projects
- General expertise (security, testing, architecture)
- Your personal workflow preferences
- Example: `commit-message-helper` for your commit style

---

## allowed-tools Best Practices

### Common Tool Combinations

**Code Analysis Skills:**
```yaml
allowed-tools: [Read, Grep, Glob, Bash]
```

**File Creation Skills:**
```yaml
allowed-tools: [Read, Write, Glob, Grep]
```

**Code Modification Skills:**
```yaml
allowed-tools: [Read, Edit, Bash, Grep]
```

**Research/Documentation Skills:**
```yaml
allowed-tools: [Read, Glob, Grep, WebSearch, mcp__rag-memory__search_documents]
```

**Orchestration Skills (invoke subagents):**
```yaml
allowed-tools: [Read, Task, Bash]
```

### MCP Tool Access

To use MCP tools, include full tool name:

```yaml
allowed-tools: [Read, mcp__rag-memory__search_documents, mcp__context7__query-docs]
```

**Format:** `mcp__[server-name]__[tool-name]`

---

## Testing Skills

### How to Test a Skill

1. **Create skill** in appropriate directory
2. **Trigger activation** by creating the context described in description
3. **Verify behavior** - does it follow the instructions?
4. **Check tool usage** - does it use allowed-tools correctly?
5. **Validate output** - does it produce expected results?

### Example Test

**Skill:** `security-reviewer` that activates on git commits

**Test:**
1. Make code change with obvious vulnerability (e.g., SQL injection)
2. Commit: `git add . && git commit -m "Add user query"`
3. Watch for skill activation
4. Verify it:
   - Detected the commit
   - Scanned files
   - Found vulnerability
   - Reported with severity and fix

### Debugging Skills

**Skill not activating?**
- Check description - is it specific enough?
- Are you creating the right context/keywords?
- Try explicitly asking: "Can you review security?"

**Skill activating at wrong times?**
- Description too broad
- Make description more specific about WHEN to activate

**Skill can't do its work?**
- Check allowed-tools - does it have what it needs?
- Add missing tools to allowed-tools array

---

## Common Mistakes When Creating Skills

### Mistake 1: Creating Skill for Simple Task

**What developers think:** "I need a skill to run tests"

**Reality:** Simple tasks should be Slash Commands

**Fix:** Create `/test` slash command instead

### Mistake 2: Expecting Manual Invocation

**What developers think:** "I'll run this skill when I want it"

**Reality:** Skills auto-activate, use Slash Command for manual invocation

**Fix:** Create Slash Command that invokes Subagent with skill

### Mistake 3: Forgetting allowed-tools

**What developers think:** "Skill can use any tools"

**Reality:** Skills ONLY use tools in allowed-tools array

**Fix:** Add all needed tools to allowed-tools

### Mistake 4: Writing Documentation Instead of Instructions

**What developers think:** "Explain what the skill does"

**Reality:** Tell Claude what steps to execute

**Fix:** Use "Step 1:", "Step 2:" format with explicit actions

---

## Summary Checklist

When creating a skill, verify:

- [ ] YAML frontmatter has all required fields (name, description, allowed-tools)
- [ ] name is kebab-case lowercase
- [ ] description explains WHEN to activate (not what skill does)
- [ ] allowed-tools includes ALL tools skill needs
- [ ] MCP tools use full name format (mcp__server__tool)
- [ ] Content written as INSTRUCTIONS (steps to follow)
- [ ] NOT written as documentation (explanation of what skill is)
- [ ] Complex workflows broken into clear steps
- [ ] Supporting files use progressive disclosure (loaded when needed)
- [ ] Located in correct directory (.claude/skills/ or ~/.claude/skills/)
- [ ] Skill is appropriate choice (complex workflow, auto-activation needed)

---

## Reference

**Official Claude Code Skills Documentation:**
- [Skills Guide](https://docs.anthropic.com/claude/docs/skills)
- [Progressive Disclosure](https://docs.anthropic.com/claude/docs/skills#progressive-disclosure)

**Required Frontmatter Fields:** name, description, allowed-tools

**Optional Frontmatter Fields:** model

**Valid Model Values:** sonnet, opus, haiku

**Tool Access:** Must explicitly list in allowed-tools (MCP tools need full mcp__server__tool format)

**Directory Locations:**
- Project: `.claude/skills/[skill-name]/SKILL.md`
- Personal: `~/.claude/skills/[skill-name]/SKILL.md`
