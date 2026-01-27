---
description: Interactive wizard to scaffold RAG Memory collections based on your use cases
argument-hint: ""
allowed-tools: ["Read", "AskUserQuestion"]
---

# Setup Collections - RAG Memory Collection Scaffold

You are helping a user set up their RAG Memory collections with a minimal, durable starter scaffold.

## Critical Instructions

- **Always check current state first** - Use `mcp__rag-memory__list_collections()` before doing anything
- **Don't create automatically** - If collections exist, ask the user what they want to do
- **Use MCP tools directly** - Create collections via `mcp__rag-memory__create_collection`
- **Keep it simple** - Propose a small set of durable collections, not many narrow ones
- **Add routing hints** - After creating each collection, add routing hints via `mcp__rag-memory__update_collection_metadata_schema`
- **Do NOT create agent-preferences** - The `agent-preferences` collection is auto-created by the MCP server on startup

---

## Step 1: Check Current State (REQUIRED FIRST STEP)

**Always start here:**

```
mcp__rag-memory__list_collections()
```

### If collections exist:

Display what they have (name, domain, description if available).

Then ask:

"You already have collections set up. What would you like to do?

A) **Add missing recommended collections** (I'll propose what's missing from the standard scaffold)
B) **Review what I have and map them to recommendations** (understand your current setup)
C) **Start fresh conceptually** (no deletions, just build a new mental model)

Please choose A, B, or C."

**[WAIT FOR RESPONSE - DO NOT CREATE ANYTHING UNTIL USER RESPONDS]**

### If no collections exist:

Say: "Your knowledge base is empty. I'll propose a minimal starter scaffold of 5-6 durable collections that stay useful as you grow."

Proceed to Step 2.

---

## Step 2: Explain the Approach (Empty KB Only)

Before proposing collections, provide this brief explanation:

"**Why start with a small number of collections?**

Collections are partitions for retrieval - when you search, you search one collection at a time. Having fewer, clearer buckets reduces confusion and makes it easier to know where to put things and where to search.

This is a starting scaffold designed around *semantic categories* (what something is about) rather than *source types* (where it came from). You can always add more later, but starting simple is better than over-organizing.

I'll propose 5 core collections, plus an optional business collection if you need it."

---

## Step 3: Propose Collections (Empty KB Only)

Present this exact scaffold:

"**Recommended starter scaffold:**

1. **Knowledge and Reference** (`knowledge-and-reference`)
   - Purpose: External documentation and reference material (library docs, frameworks, official docs, standards, manuals)
   - Domain: Engineering / Reference

2. **Projects** (`projects`)
   - Purpose: Work-in-progress contexts (project notes, plans, drafts, links related to things being built or explored)
   - Domain: Project

3. **Practices and Procedures** (`practices-and-procedures`)
   - Purpose: Stable ways of working (SOPs, checklists, playbooks, principles, workflows, rules)
   - Domain: Operations

4. **People and Relationships** (`people-and-relationships`)
   - Purpose: Person-centric notes (who someone is, context about people, preferences, history)
   - Domain: Personal

5. **Inbox Unsorted** (`inbox-unsorted`)
   - Purpose: Temporary holding for uncategorized items; meant to be reviewed and refiled later
   - Domain: Intake

---

**Optional:** Do you also want a collection for running a business (ops/finance/clients)?

If yes, I'll add:

6. **Business Operations** (`business-operations`)
   - Purpose: Accounting/finance exports, vendors, client operations, business strategy, internal business procedures
   - Domain: Business

---

Does this look good? I can create these as-is, or you can suggest modifications."

**[WAIT FOR CONFIRMATION]**

---

## Step 4: Create Collections

Once the user confirms, create each collection using the exact names and purposes above.

### Collection: knowledge-and-reference

```
mcp__rag-memory__create_collection(
    name="knowledge-and-reference",
    description="External documentation and reference material (library docs, frameworks, official docs, standards, manuals)",
    domain="Engineering",
    domain_scope="Official documentation, technical references, standards, and external learning resources. Does not include internal company docs or work-in-progress project notes.",
    metadata_schema={
        "custom": {},
        "routing": {
            "examples": [
                "What does the React docs say about X?",
                "Official guidelines for Y",
                "Framework documentation for Z",
                "API reference for this library"
            ],
            "exclusions": [
                "Our team's process for X",
                "Project notes about Y",
                "Internal company documentation"
            ]
        }
    }
)
```

### Collection: projects

```
mcp__rag-memory__create_collection(
    name="projects",
    description="Work-in-progress contexts (project notes, plans, drafts, links related to things being built or explored)",
    domain="Project",
    domain_scope="Active and recent project work including design docs, specs, exploration notes, and prototyping context. Does not include stable procedures or completed/archived work.",
    metadata_schema={
        "custom": {},
        "routing": {
            "examples": [
                "Notes about the redesign project",
                "What are we building for feature X?",
                "Project plan for Y",
                "Design decisions for the new system"
            ],
            "exclusions": [
                "External library documentation",
                "Standard operating procedures",
                "Stable team workflows"
            ]
        }
    }
)
```

### Collection: practices-and-procedures

```
mcp__rag-memory__create_collection(
    name="practices-and-procedures",
    description="Stable ways of working (SOPs, checklists, playbooks, principles, workflows, rules)",
    domain="Operations",
    domain_scope="Established processes, standard operating procedures, decision frameworks, and repeatable workflows. Does not include one-off project plans or temporary experiments.",
    metadata_schema={
        "custom": {},
        "routing": {
            "examples": [
                "What is our code review process?",
                "How do we deploy to production?",
                "Team workflow for X",
                "Our standard checklist for releases"
            ],
            "exclusions": [
                "External documentation",
                "One-off project plans",
                "Temporary experiments"
            ]
        }
    }
)
```

### Collection: people-and-relationships

```
mcp__rag-memory__create_collection(
    name="people-and-relationships",
    description="Person-centric notes (who someone is, context about people, preferences, history)",
    domain="Personal",
    domain_scope="Information about individuals including teammates, clients, contacts, and their preferences, history, and context. Does not include general team documentation or processes.",
    metadata_schema={
        "custom": {},
        "routing": {
            "examples": [
                "What do I know about John?",
                "Client X's preferences",
                "Who is the contact for Y?",
                "Notes about my conversation with Z"
            ],
            "exclusions": [
                "Technical documentation",
                "Project execution details",
                "Team processes"
            ]
        }
    }
)
```

### Collection: inbox-unsorted

```
mcp__rag-memory__create_collection(
    name="inbox-unsorted",
    description="Temporary holding for uncategorized items; meant to be reviewed and refiled later",
    domain="Intake",
    domain_scope="Temporary staging area for new content that hasn't been categorized yet. Should be periodically reviewed and moved to appropriate collections.",
    metadata_schema={
        "custom": {},
        "routing": {
            "examples": [
                "Save this but not sure where it goes",
                "Quick capture for later sorting",
                "Miscellaneous note to categorize later"
            ],
            "exclusions": [
                "Content that clearly fits another collection"
            ]
        }
    }
)
```

### Collection: business-operations (if requested)

```
mcp__rag-memory__create_collection(
    name="business-operations",
    description="Accounting/finance exports, vendors, client operations, business strategy, internal business procedures",
    domain="Business",
    domain_scope="Business management including financial records, vendor relationships, client operations, strategic planning, and internal business processes. Does not include project execution details or external technical documentation.",
    metadata_schema={
        "custom": {},
        "routing": {
            "examples": [
                "Q4 financial records",
                "Vendor contract details",
                "Client invoice for X",
                "Business strategy notes"
            ],
            "exclusions": [
                "External technical docs",
                "Personal relationship notes",
                "Project execution details"
            ]
        }
    }
)
```

Report each success as you create them:
- "✓ Created 'knowledge-and-reference'"
- "✓ Created 'projects'"
- etc.

---

## Step 5: Verify and Provide "What Goes Where" Guide

After creation, verify:

```
mcp__rag-memory__list_collections()
```

Show the user their new setup in a simple table:

"**Your collections are ready:**

| Collection | Purpose |
|------------|---------|
| knowledge-and-reference | External docs, frameworks, standards, technical references |
| projects | Work-in-progress project notes, plans, designs, exploration |
| practices-and-procedures | SOPs, playbooks, checklists, stable workflows |
| people-and-relationships | Person-centric notes, context, preferences, history |
| inbox-unsorted | Temporary holding; review and refile periodically |
| business-operations | (if created) Finance, vendors, clients, business strategy |

---

**Quick "what goes where" guide:**

- Downloaded the React docs? → **knowledge-and-reference**
- Notes about the redesign project you're building? → **projects**
- Your team's code review checklist? → **practices-and-procedures**
- Notes about a client's preferences? → **people-and-relationships**
- Saved an article but not sure where it fits yet? → **inbox-unsorted**
- Exported your accounting records? → **business-operations**

These collections can evolve as your needs grow, but this scaffold gives you a durable starting point."

**[DONE - Do not suggest next steps or ask what they want to do next]**

---

## Handling Existing Collections (User chose A, B, or C)

### Option A: Add missing recommended collections

Compare their existing collections to the standard scaffold. Identify which of the 5-6 standard collections are missing.

"Based on the standard scaffold, you're missing:
- [Collection Name] - [Purpose]
- [Collection Name] - [Purpose]

Would you like me to create these?"

If yes, create only the missing ones using the definitions from Step 4.

### Option B: Review and map to recommendations

Present their existing collections alongside the standard scaffold:

"Here's how your current collections map to the recommended scaffold:

**Your Current Collections:**
- [their collection name] → might be similar to [standard collection]
- [their collection name] → might be similar to [standard collection]

**Standard Scaffold:**
- knowledge-and-reference (external docs/references)
- projects (work-in-progress contexts)
- practices-and-procedures (stable ways of working)
- people-and-relationships (person-centric notes)
- inbox-unsorted (temporary holding)

You can keep your existing setup, rename/reorganize, or add from the standard scaffold. What would you like to do?"

### Option C: Start fresh conceptually

"I'll explain the standard scaffold philosophy without touching your existing collections:

[Provide the explanation from Step 2]

[Present the standard scaffold from Step 3]

Your existing collections remain unchanged. This is just a conceptual framework you can use to think about organization going forward."

---

## Error Handling

**If collection creation fails (name already exists):**
"A collection named `{name}` already exists. Skipping this one since it's already set up."

**If MCP server not connected:**
"I can't connect to the RAG Memory server. Make sure:
1. The server is running
2. Your MCP configuration is set up correctly

Would you like help troubleshooting?"

---

## Important Reminders

- **Always call `list_collections()` first** - Never skip this step
- **Never create collections automatically if they exist** - Always ask first
- **Use exact names** - Follow kebab-case format: "knowledge-and-reference" (lowercase with hyphens only)
- **Naming constraint** - Collection names MUST contain only alphanumeric characters, hyphens, and underscores (no spaces, no special chars)
- **Include routing hints at creation** - Pass routing hints via `metadata_schema` parameter when calling `create_collection`
- **Do NOT create agent-preferences** - The `agent-preferences` collection is auto-created by the RAG Memory MCP server on startup with pre-populated routing hints. You will see it when you call `list_collections()`.
- **Keep it minimal** - 5-6 collections is the goal, not 10+
