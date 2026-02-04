# Confluence Reference

## Confluence Workflow

### Step 1: Get Cloud ID and Available Spaces

Call `mcp__atlassian__getAccessibleAtlassianResources` (no parameters needed - discovery call).

Extract `cloudId` from response. [FROM: config `cloudId` OR this response. NEVER fabricate.]

Call `mcp__atlassian__getConfluenceSpaces` to list available spaces.

### Step 2: Search for Related Content

```
Call mcp__atlassian__search with:
  - query: "What documentation exists about [topic]?"
```

- query: [FROM: user topic. Content, not identifier - OK to construct.]

Show results to user.

### Step 3: Determine How to Store

**Flag overrides (skip asking):**
- `--separate` → Go to Create New Page Workflow
- `--update` + related page found → Go to Update Existing Page Workflow

**No flags (default):**

If related page found in Step 2 → Ask the user:
> I found a related page: '[title]'
>
> How would you like to handle this?
> 1. Update '[title]' with this information
> 2. Create a new page
> 3. Cancel

STOP and wait for response. Then route accordingly.

If no related page found → Go to Create New Page Workflow (no need to ask)

---

## Update Existing Page Workflow

Append new content to an existing page.

1. Extract `pageId` from search results. [FROM: search results. NEVER fabricate.]
2. Get current content if needed:
   ```
   Call mcp__atlassian__getConfluencePage with:
     - cloudId: [FROM: config "cloudId" OR getAccessibleAtlassianResources response. NEVER fabricate.]
     - pageId: [FROM: search results. NEVER fabricate.]
   ```
3. Append with timestamp:
   ```
   [existing content]

   ---

   **Added [YYYY-MM-DD HH:MM]:**
   [new content]
   ```
4. Update:
   ```
   Call mcp__atlassian__updateConfluencePage with:
     - cloudId: [FROM: config "cloudId" OR getAccessibleAtlassianResources response. NEVER fabricate.]
     - pageId: [FROM: search results. NEVER fabricate.]
     - title: [FROM: existing page title. NEVER change without user consent.]
     - content: [FROM: generated updated content. OK to construct.]
   ```
5. Confirm success

---

## Create New Page Workflow

### Select Space

Present available spaces from Step 1. Let user choose.

### Create Page

```
Call mcp__atlassian__createConfluencePage with:
  - cloudId: [FROM: config "cloudId" OR getAccessibleAtlassianResources response. NEVER fabricate.]
  - spaceId: [FROM: getConfluenceSpaces response + user selection. NEVER guess.]
  - title: [FROM: user input or suggested title. OK to suggest.]
  - content: [FROM: user's exact content - do not modify.]
```

Confirm success with link to new page.

---

## Tool Parameters

### mcp__atlassian__getAccessibleAtlassianResources

No parameters required. Returns cloud ID needed for other operations.

### mcp__atlassian__getConfluenceSpaces

No parameters required. Returns list of available spaces with:
- `id` - Space ID
- `key` - Space key
- `name` - Space name

### mcp__atlassian__search

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| query | string | Yes | Natural language question | User topic - OK to construct |

This is the semantic search tool. Use this for duplicate/related content checking.

### mcp__atlassian__getConfluencePage

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| cloudId | string | Yes | Atlassian cloud instance ID | Config `cloudId` OR `getAccessibleAtlassianResources` |
| pageId | string | Yes | Page ID | Search results. NEVER fabricate. |

Returns page content. Use when you need existing content before appending.

### mcp__atlassian__createConfluencePage

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| cloudId | string | Yes | Atlassian cloud instance ID | Config `cloudId` OR `getAccessibleAtlassianResources` |
| spaceId | string | Yes | Target space ID | `getConfluenceSpaces` + user selection |
| title | string | Yes | Page title | User input - OK to suggest |
| content | string | Yes | Page content (supports wiki markup) | User content |

### mcp__atlassian__updateConfluencePage

| Parameter | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| cloudId | string | Yes | Atlassian cloud instance ID | Config `cloudId` OR `getAccessibleAtlassianResources` |
| pageId | string | Yes | Existing page ID | Search results. NEVER fabricate. |
| title | string | Yes | Updated title | Existing page title |
| content | string | Yes | Updated content | Generated - OK to construct |

---

## Edge Cases

### CQL vs Semantic Search

Do NOT use `searchConfluenceUsingCql()` for duplicate checking. CQL searches titles/labels, not content meaning. Use the semantic `search()` tool.

### Listing Pages

Do NOT use `getPagesInConfluenceSpace()` as a search substitute. It lists pages, doesn't search content.

### Updating vs Creating

If search finds similar content, offer to update the existing page instead of creating a duplicate.

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| cloudId | Config `cloudId` OR `getAccessibleAtlassianResources` response | Guess, infer, construct |
| pageId | Search results | Fabricate or guess |
| spaceId | `getConfluenceSpaces` + user selection | Guess or hardcode |
| title | User input or existing page title | N/A (content) |
| content | User input or generated | N/A (content) |
| query | User topic (content, not identifier) | N/A |
