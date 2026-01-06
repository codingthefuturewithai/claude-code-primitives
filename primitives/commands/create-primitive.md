---
description: Create a Claude Code primitive with proper requirements gathering
allowed-tools: Task, Read
---

# Create Claude Code Primitive

Guide the user through creating the right primitive type with correct format.

## Step 1: Understand What They Want to Build

Ask: "What do you want to accomplish with this primitive?"

Gather:
- What problem does this solve?
- When should this run? (manually, automatically, on events)
- Who will use it? (just you, team, project-specific)
- What work will it do?

## Step 2: Determine Primitive Type

Use this decision tree:

**Q1: Does this connect to an external service or API?**
→ YES: Recommend **MCP Server** (requires separate implementation)
→ NO: Continue to Q2

**Q2: Must this run automatically on EVERY action (enforcement)?**
→ YES: Recommend **Hook**
→ NO: Continue to Q3

**Q3: How will this be invoked?**
→ "I'll type a command": Continue to Q4 (likely Slash Command)
→ "Claude should decide when": Continue to Q5 (likely Skill)

**Q4: Is this a simple, focused operation?**
→ YES: Recommend **Slash Command**
→ NO: Continue to Q5

**Q5: Need parallel execution or isolated context?**
→ YES: Recommend **Subagent** (ONLY option for parallel)
→ NO: Continue to Q6

**Q6: Has supporting files (templates, examples, scripts)?**
→ YES: Recommend **Skill**
→ NO: Recommend **Slash Command**

**Q7: Sharing with team via marketplace?**
→ YES: Recommend **Plugin** (AFTER building primitives)
→ NO: Use .claude/ or ~/.claude/ directly

State your recommendation and explain WHY based on their requirements.

## Step 3: Get Format Details from claude-code-guide

Use the claude-code-guide subagent to get authoritative format and syntax information:

```
Use the claude-code-guide subagent to answer: "What is the exact YAML frontmatter format for [primitive-type]? What fields are required versus optional?"
```

Ask additional questions as needed:
- "When should I use [primitive-type] versus [alternative]?"
- "What are the configuration requirements for [primitive-type]?"
- "How do I invoke [primitive-type] from other primitives?"

## Step 4: Assess Information Completeness

Check what you have from claude-code-guide:

**From claude-code-guide (Built-in subagent):**
- Format/syntax? YES/NO
- Required fields? YES/NO
- When to use? YES/NO

**Confidence Level:**
- High: All items YES
- Medium: Missing 1 item
- Low: Missing 2+ items

If confidence is Low, STOP and report:
"I cannot find complete documentation for creating [primitive-type]. Specifically missing: [list gaps]. I will NOT rely on my internal knowledge to fill these gaps."

## Step 5: Load Primitive-Specific Guidance (Progressive Disclosure)

**IMPORTANT**: Only load guides that exist. The plugin may not include all guides yet.

**First: Load central navigation**
```
Try to Read("primitives/guides/INDEX.md")
If file doesn't exist, skip this step and proceed with claude-code-guide info only
```

**Second: Load type-specific guide based on primitive type**

For each primitive type, attempt to load its complete guide:

- **Skills**: Read("primitives/guides/skills/complete-guide.md")
  - Also read: Read("primitives/guides/skills/best-practices.md") if available
  - **CRITICAL for skills**: Apply the skills checklist (third-person description, gerund naming, etc.)

- **Slash Commands**: Read("primitives/guides/commands/complete-guide.md")

- **Subagents**: Read("primitives/guides/subagents/complete-guide.md")

- **Hooks**: Read("primitives/guides/hooks/complete-guide.md")

- **MCP Servers**: Read("primitives/guides/mcp-servers/complete-guide.md")

- **Plugins**: Read("primitives/guides/plugins/complete-guide.md")

**Third: Load examples if helpful (optional)**

If user would benefit from seeing working examples:
```
Read("examples/[primitive-type]/[example-name].md")
```

**Note**: If any file doesn't exist, continue without it. The claude-code-guide information is sufficient to create basic primitives.

## Step 6: Gather Complete Requirements

Based on the primitive type, gather specific requirements:

**For Slash Commands:**
- Description (what it does)
- Argument format (if any)
- Tools needed
- Model preference (if any)

**For Skills:**
- Description for auto-activation
- Tools needed
- Supporting files required
- Progressive disclosure strategy

**For Subagents:**
- Description
- Skills it needs access to
- Tool restrictions (if any)
- Model preference

**For Hooks:**
- Event type (PostToolUse, PreToolUse, etc.)
- Tool matcher (which tools trigger it)
- Shell command to execute
- Scope (global ~/.claude/settings.json or project .claude/settings.json)

**For MCP Servers:**
- External service details
- Authentication requirements
- Tool definitions needed
- Note: Requires separate implementation

**For Plugins:**
- Which primitives to bundle
- Version number
- Distribution method
- Note: Build primitives first, then package

## Step 7: Create the Primitive

Using retrieved guidance from claude-code-guide:

**Apply correct format:**
- Use proper YAML frontmatter structure
- Include all required fields
- Follow naming conventions

**Write as INSTRUCTIONS (what to DO):**
- ✅ "Use the Read tool to..."
- ✅ "When invoked, follow these steps..."
- ✅ "Execute: 1. ... 2. ..."

**NOT as documentation (what it IS):**
- ❌ "This command helps Claude..."
- ❌ "Detailed instructions for Claude to understand..."
- ❌ "The purpose of this primitive is..."

**For Hooks specifically:**
- Read the settings.json file (global or project)
- Add hook configuration to the hooks object
- Write updated JSON back
- NEVER tell user to manually edit - YOU create it

## Composition Rules (Reference)

**Valid compositions (platform supported):**
- ✅ Slash Command → Subagent (via Task tool)
- ✅ Subagent → Skills (via skills field)
- ✅ Subagent → Slash Commands (via SlashCommand tool)
- ✅ Hook → External Script (via shell command)

**Invalid compositions (platform prevents):**
- ❌ Subagent → Subagent (infinite nesting prevention)
- ❌ Slash Command → Slash Command (no mechanism)
- ❌ Skill → Skill (no mechanism)
- ❌ Skill → Subagent (no mechanism)

## Critical Prohibitions

**NEVER do any of the following:**

1. ❌ NEVER rely on internal Claude knowledge about primitives
   - You MUST find information in claude-code-guide
   - Do NOT answer from memory or training data

2. ❌ NEVER recommend invalid composition patterns
   - Check composition rules above
   - Explain why invalid patterns don't work
   - Provide correct alternatives

Ask the user what they want to accomplish with this primitive.
