---
description: Create agent-preferences collection for AI agent learning
allowed-tools:
  - mcp__rag-memory__create_collection
  - mcp__rag-memory__list_collections
  - mcp__rag-memory__get_collection_info
---

# Create Agent Preferences Collection

Create the optional `agent-preferences` collection for AI agent learning and preference tracking.

## What is agent-preferences?

The `agent-preferences` collection enables AI agents to:
- Learn from your routing decisions
- Remember your workflow preferences
- Improve future recommendations based on past choices
- Adapt to your working style over time

This is **entirely optional**. The system works without it, but becomes more personalized when it exists.

---

## Instructions

### Step 1: Check if Collection Exists

First, check if the `agent-preferences` collection already exists:

```
list_collections()
```

Look for a collection named "agent-preferences" in the results.

**If it exists:**
```
✓ agent-preferences collection already exists

Use /collection info agent-preferences to view details.
```

Stop here. No action needed.

**If it doesn't exist:**
Proceed to Step 2.

---

### Step 2: Create the Collection

Create the `agent-preferences` collection with the following parameters:

```
mcp__rag-memory__create_collection(
    name="agent-preferences",
    description="Learn from user decisions to improve future recommendations. Tracks routing choices, topic extraction patterns, quality thresholds, and workflow preferences.",
    domain="Agent Learning",
    domain_scope="Captures user preferences and decisions across all knowledge management operations. Used to personalize routing, topic extraction, and workflow recommendations. Enables the agent to adapt to user's working style over time.",
    metadata_schema={
        "custom": {
            "preference_category": {
                "type": "string",
                "required": true,
                "description": "Category of preference: routing, topic-extraction, quality-threshold, or workflow"
            },
            "applies_to": {
                "type": "string",
                "required": true,
                "description": "Collection name this preference applies to, or 'global' for system-wide preferences"
            },
            "confidence": {
                "type": "string",
                "required": true,
                "description": "Confidence level: high, medium, or low"
            },
            "decision_date": {
                "type": "string",
                "required": false,
                "description": "ISO 8601 timestamp of when preference was established"
            },
            "context": {
                "type": "string",
                "required": false,
                "description": "Additional context about the preference or decision"
            }
        }
    }
)
```

**Note:** This will trigger the kb-modification-approval.py hook with an "⚠️ AGENT LEARNING" warning, ensuring you're aware you're creating a learning collection.

---

### Step 3: Report Success

After creation:

```
✅ Agent Preferences Collection Created

Name: agent-preferences
Purpose: Learn from your decisions to improve recommendations

Metadata Fields:
- preference_category (required): routing, topic-extraction, quality-threshold, workflow
- applies_to (required): Collection name or "global"
- confidence (required): high, medium, low
- decision_date (optional): ISO 8601 timestamp
- context (optional): Additional notes

Next Steps:
- Use /capture-with-learning to capture content with preference tracking
- Or use /capture normally - it will automatically check for preferences

The agent will now:
1. Query this collection before making decisions
2. Offer to remember your choices after approval
3. Improve recommendations based on your patterns
```

---

## Metadata Schema Details

### Required Fields

**preference_category** (string, required)
- Valid values: "routing", "topic-extraction", "quality-threshold", "workflow"
- Purpose: Categorize the type of preference being captured
- Examples:
  - "routing": Which collection for which content type
  - "topic-extraction": When to ask vs infer topics
  - "quality-threshold": Minimum quality scores
  - "workflow": Process preferences (e.g., always preview websites)

**applies_to** (string, required)
- Valid values: Any collection name or "global"
- Purpose: Scope the preference to a specific collection or system-wide
- Examples:
  - "knowledge-and-reference": Preference applies to this collection
  - "global": Preference applies everywhere

**confidence** (string, required)
- Valid values: "high", "medium", "low"
- Purpose: Indicate how strongly this preference should be weighted
- Examples:
  - "high": User explicitly stated this preference multiple times
  - "medium": User approved this once, seems consistent
  - "low": User tried this once, may change

### Optional Fields

**decision_date** (string, optional)
- Format: ISO 8601 timestamp (e.g., "2026-01-17T14:30:00Z")
- Purpose: Track when preference was established
- Use: Helps identify outdated preferences

**context** (string, optional)
- Format: Free text
- Purpose: Additional context about why this preference was chosen
- Examples:
  - "User explicitly chose this after seeing alternatives"
  - "Inferred from user's workflow pattern"
  - "User corrected initial routing decision"

---

## Examples of Preferences

### Routing Preference
```
Content: "User prefers routing official framework documentation to knowledge-and-reference collection.
Reason: Clear semantic match to external reference materials."

Metadata:
- preference_category: "routing"
- applies_to: "knowledge-and-reference"
- confidence: "high"
- decision_date: "2026-01-17T14:30:00Z"
- context: "User explicitly approved routing React docs here after seeing other options"
```

### Topic Extraction Preference
```
Content: "For project-related content, always ask user for project name rather than inferring.
User values explicit project identification over automatic extraction."

Metadata:
- preference_category: "topic-extraction"
- applies_to: "projects"
- confidence: "high"
- decision_date: "2026-01-15T09:15:00Z"
- context: "User corrected auto-extracted topic twice"
```

### Quality Threshold Preference
```
Content: "User accepts content with quality_score >= 0.6 for knowledge-and-reference collection.
Lower threshold for external docs is acceptable."

Metadata:
- preference_category: "quality-threshold"
- applies_to: "knowledge-and-reference"
- confidence: "medium"
- decision_date: "2026-01-16T11:45:00Z"
- context: "User approved several docs with scores 0.6-0.7"
```

### Workflow Preference
```
Content: "User prefers to always preview websites before multi-page crawls, even for known domains.
Values transparency over speed."

Metadata:
- preference_category: "workflow"
- applies_to: "global"
- confidence: "high"
- decision_date: "2026-01-17T08:00:00Z"
- context: "User requested preview multiple times despite high-confidence routing"
```

---

## Querying Preferences

Once created, query preferences using semantic search with metadata filters:

```
# Find routing preferences
search_documents(
    query="How has user routed documentation content?",
    collection_name="agent-preferences",
    metadata_filter={"preference_category": "routing"}
)

# Find preferences for specific collection
search_documents(
    query="What are user's preferences for projects collection?",
    collection_name="agent-preferences",
    metadata_filter={"applies_to": "projects"}
)

# Find high-confidence preferences only
search_documents(
    query="What are user's established preferences?",
    collection_name="agent-preferences",
    metadata_filter={"confidence": "high"}
)
```

---

## Privacy & Control

**What gets stored:**
- Your routing decisions (which collection you chose)
- Your topic extraction preferences (when you want to be asked)
- Your workflow preferences (preview websites, quality thresholds)

**What does NOT get stored:**
- Actual content of documents
- Sensitive data or credentials
- Personal information beyond preferences

**Control:**
- You approve EVERY preference before it's saved (via hook)
- You can delete the collection anytime: `/collection delete agent-preferences`
- You can view all preferences: `/collection info agent-preferences`
- Each preference save shows "⚠️ AGENT LEARNING" warning

**When preferences are used:**
- Before routing decisions (to recommend based on history)
- Before topic extraction (to know if you prefer asking vs inferring)
- Never automatically applied without your approval

---

## When to Use This Collection

**Create it if:**
- ✅ You want the agent to learn your preferences
- ✅ You frequently route similar content types
- ✅ You want personalized recommendations
- ✅ You value efficiency in repeated tasks

**Skip it if:**
- ❌ You prefer manual decisions every time
- ❌ Your routing patterns change frequently
- ❌ You don't want the agent to remember choices
- ❌ You rarely use the knowledge management system

---

## Error Handling

**Collection already exists:**
```
✓ agent-preferences collection already exists

No action needed. The collection is ready to use.
```

**Collection creation fails:**
```
❌ Failed to create agent-preferences collection

Error: [error message]

Possible causes:
- Database connection issue
- Invalid metadata schema
- Permissions problem

Try again or check logs for details.
```

**Hook denies creation:**
```
❌ User denied agent-preferences collection creation

No changes made. The agent will continue working without preference tracking.
You can create it later using /create-agent-preferences
```
