---
name: devflow:pm:roadmap
description: Manage Confluence Product Planning & Roadmap - review, add ideas, refine thoughts. Use this to manage product roadmap in Confluence.
argument-hint: "[review|idea|refine] [args...]"
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - mcp__atlassian__getAccessibleAtlassianResources
  - mcp__atlassian__getConfluenceSpaces
  - mcp__atlassian__getConfluencePage
  - mcp__atlassian__getConfluencePageDescendants
  - mcp__atlassian__updateConfluencePage
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "mcp__atlassian__updateConfluencePage"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/hooks/atlassian-approval.py"
---

# Product Roadmap Management

Manage your Confluence Product Planning & Roadmap section directly from Claude Code.

**Request:** $ARGUMENTS

---

## Confluence Page IDs (Reference)

| Page | ID |
|------|-----|
| Product Planning & Roadmap | 147816449 |
| Product Roadmap | 147652616 |
| Feature Backlog & Ideas | 148242435 |
| Planning Notes & Decision Logs | 148275208 |

**CloudId:** `codingthefuturewithai.atlassian.net`

---

## Step 1: Parse Arguments & Route

**Parse $ARGUMENTS to determine mode:**

- No arguments OR empty → **Interactive Menu**
- `review [section]` → **Review Mode**
- `idea [description]` → **Idea Mode**
- `refine` → **Refine Mode**

---

## Interactive Menu (No Arguments)

If no arguments provided, present menu:

Say: "What would you like to do?"

Options:
1. **Review** - Browse current roadmap, backlog, or decisions
2. **Add Idea** - Capture a new feature idea
3. **Refine** - Structure a rough thought into something concrete

Ask using AskUserQuestion. Then route to appropriate mode below.

---

## Review Mode (`/roadmap review [section]`)

**Purpose:** Fetch and display current state from Confluence

### Step R1: Determine Section

If section provided in arguments, use it. Otherwise ask:

"Which section would you like to review?"
1. **Roadmap** - Pre-JIRA pipeline (Exploring → Ready for JIRA)
2. **Backlog** - Feature ideas by status
3. **Decisions** - Recent architectural decisions
4. **Drafts** - Local draft files in `.roadmap/drafts/`

**WAIT for response.**

---

### Step R2: Fetch Content

**For Roadmap (page 147652616):**
```
[Call mcp__atlassian__getConfluencePage with pageId="147652616"]
```

Parse and display:
- **Exploring:** Table of ideas under consideration (show: Idea, Goal, Status)
- **Ready for JIRA:** Table of defined items ready to become JIRA issues (show: Feature, Summary, Key Decisions)
- **Future Vision:** Brief bullet list of long-term opportunities

---

**For Backlog (page 148242435):**
```
[Call mcp__atlassian__getConfluencePage with pageId="148242435"]
```

Parse and display grouped by status:
- 💡 **Ideas:** [list]
- 🔍 **Exploring:** [list]
- 📋 **Defined:** [list]

---

**For Decisions (page 148275208):**
```
[Call mcp__atlassian__getConfluencePage with pageId="148275208"]
```

Parse and display recent decisions (newest first):
- Show: Title, Date, Status (🟢/🟡/🔴/⚪)
- Limit to 5 most recent unless user asks for more

---

**For Drafts (local):**
```
[Use Glob to find .roadmap/drafts/*.md]
[Read each file's frontmatter to show: title, type, category, created date]
```

If no drafts exist, say: "No local drafts found. Use `/roadmap idea` or `/roadmap refine` to create one."

---

### Step R3: Offer Follow-up

After displaying, ask: "Would you like to drill into any specific item, or are you done?"

If done, end. If drill-in requested, fetch and display full details.

---

## Idea Mode (`/roadmap idea [description]`)

**Purpose:** Add a new feature idea to the backlog

### Step I1: Accept Description

If description provided in arguments, use it. Otherwise ask:

"What's your idea? (Brief description is fine - I'll help structure it)"

**WAIT for response.** Store as `idea_description`.

---

### Step I2: Analyze Codebase

Say: "Let me check the codebase for related components..."

```
[Use Grep/Glob to search for keywords from idea_description]
[Look in: mcp-server/src/, web-ui/src/, scripts/]
[Identify: related files, existing patterns, integration points]
```

Present findings:
- "Related components: `src/ingestion/...`, `src/retrieval/...`"
- "Existing patterns: [describe if found]"
- "Integration points: [describe if found]"

If nothing found, say: "No directly related code found - this may be a new area."

---

### Step I3: Gather Details (Use AskUserQuestion with Menus)

**Question 1 - Category:**

Use AskUserQuestion tool:
- Question: "Which area does this idea belong to?"
- Options:
  1. Collections & Organization
  2. Graph & Relationships
  3. Search & Retrieval
  4. Quality & Evaluation
  5. Agent & Automation
  6. UI/UX Improvements
  7. Integrations
  8. Analytics & Observability
  9. Admin & Operations

**WAIT.** Store as `category`.

---

**Question 2 - Who Benefits:**

Use AskUserQuestion tool:
- Question: "Who benefits from this?"
- multiSelect: true (check all that apply)
- Options:
  1. Users (via web UI)
  2. Agents (via MCP tools)
  3. Admins (operations/management)
  4. Developers (API/integrations)

**WAIT.** Store as `beneficiary`.

---

**Question 3 - Primary Purpose:**

Use AskUserQuestion tool:
- Question: "What's the primary purpose?"
- Options:
  1. Find content faster
  2. Improve content quality
  3. Better organization
  4. Enable new workflows
  5. Other (let me describe)

If "Other", ask follow-up text question.

**WAIT.** Store as `purpose`.

---

**Question 4 - Open Questions:**

Use AskUserQuestion tool:
- Question: "Any open questions or challenges?"
- Options:
  1. Implementation approach unclear
  2. Performance concerns
  3. UI/UX design needed
  4. Dependencies on other features
  5. None - straightforward

**WAIT.** Store as `open_questions`.

---

### Step I4: Generate Structured Idea

**A. Table row for Exploring section:**

| Idea | Goal | Open Questions | Status |
|------|------|----------------|--------|
| [Title] | [Short summary from purpose] | [open_questions] | Concept |

**B. Full Spec section (add below the tables, like Authentication has):**

```markdown
---

### [Title] - Full Spec

**Purpose:** [purpose]

**Who Benefits:** [beneficiary]

**Success Criteria:** [success]

**Open Questions:** [open_questions]

**Related Code:** [codebase findings from Step I2]
```

**IMPORTANT:** Both the table row AND the Full Spec section must be added to the page.

---

### Step I5: Choose Destination

Show preview, then ask:

"Where should this go?"
1. **Push to Confluence** - Add to Product Roadmap (Exploring section)
2. **Save as local draft** - Store in `.roadmap/drafts/` for later

**WAIT for response.**

---

### Step I6a: If Confluence

Show full preview of what will be added to the Exploring table.

Ask: "Add this to the Exploring section of Product Roadmap? (Yes / Edit / Cancel)"

**⏸️ WAIT for explicit "Yes"**

If Yes:
```
[Fetch current page content: mcp__atlassian__getConfluencePage pageId="147652616"]
[Find the "Exploring" table]
[Add new row to table with format: | [Title] | [Goal/Value] | [Open Questions/Challenges] | Concept |]
[Update page: mcp__atlassian__updateConfluencePage with versionMessage="Added to Exploring: [title]"]
```

Return: "Added to Confluence: [link to page]"

---

### Step I6b: If Local Draft

Generate draft file:

```markdown
---
type: idea
category: [category]
status: draft
created: [today's date YYYY-MM-DD]
confluence_section: [category section name]
---

# [Title]

[Full structured idea content]
```

```
[Create directory if needed: .roadmap/drafts/]
[Write file: .roadmap/drafts/[slugified-title].md]
```

Return: "Saved draft: `.roadmap/drafts/[filename].md`"

---

## Refine Mode (`/roadmap refine`)

**Purpose:** Take a rough/vague thought and structure it properly

### Step F1: Capture Raw Thought

Say: "Share your rough thought - it can be vague, half-formed, or just a direction you're thinking about. I'll help structure it."

**WAIT for response.** Store as `raw_thought`.

---

### Step F2: Analyze Codebase

Say: "Let me check what's already in the codebase related to this..."

```
[Use Grep/Glob to search for keywords from raw_thought]
[Identify: what exists, what's missing, related components]
```

Present findings:
- "Already exists: [describe if found]"
- "Related to: [list files/components]"
- "Gap identified: [what seems new]"

---

### Step F3: Clarifying Questions (One at a Time)

**Question 1:**
"What problem does this solve? (or what opportunity does it address?)"

**WAIT.** Store as `problem`.

---

**Question 2:**
"Who benefits from this? (agents, users, admins, developers?)"

**WAIT.** Store as `beneficiary`.

---

**Question 3:**
"What would success look like? How would you know it's working?"

**WAIT.** Store as `success_criteria`.

---

**Question 4:**
"Any known challenges, constraints, or dependencies?"

**WAIT.** Store as `challenges`.

---

### Step F4: Determine Output Type

Based on the conversation, determine what this is:

**If it's a feature idea** (early concept, needs validation):
→ Generate backlog entry (use Idea Mode template)

**If it's a roadmap item** (being explored OR ready for JIRA):
→ Generate roadmap entry with:
- For **Exploring** table: Idea, Goal, Open Questions, Status
- For **Ready for JIRA** table: Feature, Summary, Key Decisions, Dependencies
- Include Full Spec section if sufficiently defined

**If it's a decision** (architectural/product choice):
→ Generate decision log entry with:
- Context, Alternatives, Decision, Rationale, Consequences

Say: "This looks like a [type]. Let me structure it accordingly..."

---

### Step F5: Generate Content

Generate appropriate markdown based on type determined above.

Show full preview.

---

### Step F6: Choose Destination

Ask: "Where should this go?"
1. **Push to Confluence** - Add to appropriate page
2. **Save as local draft** - Store in `.roadmap/drafts/` for later

**WAIT for response.**

---

### Step F7a: If Confluence

Determine target page based on type:
- Feature idea (early concept) → Feature Backlog & Ideas (148242435)
- Roadmap item (exploring or ready for JIRA) → Product Roadmap (147652616)
- Decision → Planning Notes & Decision Logs (148275208)

Show preview with target page.

Ask: "Add this to [page name]? (Yes / Edit / Cancel)"

**⏸️ WAIT for explicit "Yes"**

If Yes:
```
[Fetch current page content]
[Find appropriate section]
[Append new entry]
[Update page with versionMessage]
```

Return: "Added to Confluence: [link]"

---

### Step F7b: If Local Draft

Generate draft file with appropriate type in frontmatter:

```
[Create directory if needed: .roadmap/drafts/]
[Write file: .roadmap/drafts/[slugified-title].md]
```

Return: "Saved draft: `.roadmap/drafts/[filename].md`"

---

## Rules

**Always:**
- Ask ONE question at a time, wait for response
- Preview before any Confluence write
- Get explicit approval before updating Confluence
- Include codebase analysis findings in generated content

**Never:**
- Update Confluence without approval
- Skip codebase analysis step
- Ask multiple questions at once
- Assume category or status without asking
