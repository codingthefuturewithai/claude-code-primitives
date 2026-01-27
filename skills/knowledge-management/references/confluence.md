# Confluence Reference

## Confluence Workflow

### Step 1: Get Available Spaces

Call `getConfluenceSpaces()` to list available spaces.

### Step 2: Search for Related Content

```
search(query="What documentation exists about [topic]?")
```

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

1. Extract `pageId` from search results
2. Get current content if needed: `getConfluencePage(cloudId, pageId)`
3. Append with timestamp:
   ```
   [existing content]

   ---

   **Added [YYYY-MM-DD HH:MM]:**
   [new content]
   ```
4. Update: `updateConfluencePage(cloudId, pageId, title, updatedContent)`
5. Confirm success

---

## Create New Page Workflow

### Select Space

Present available spaces from Step 1. Let user choose.

### Create Page

```
createConfluencePage(
    cloudId="[from getAccessibleAtlassianResources]",
    spaceId="[user's choice]",
    title="[suggested title]",
    content="[user's exact content - do not modify]"
)
```

Confirm success with link to new page.

---

## Tool Parameters

### getAccessibleAtlassianResources()

No parameters required. Returns cloud ID needed for other operations.

### getConfluenceSpaces()

No parameters required. Returns list of available spaces with:
- `id` - Space ID
- `key` - Space key
- `name` - Space name

### search(query)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language question |

This is the semantic search tool. Use this for duplicate/related content checking.

### getConfluencePage(cloudId, pageId)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| cloudId | string | Yes | From getAccessibleAtlassianResources |
| pageId | string | Yes | Page ID from search results |

Returns page content. Use when you need existing content before appending.

### createConfluencePage(cloudId, spaceId, title, content)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| cloudId | string | Yes | From getAccessibleAtlassianResources |
| spaceId | string | Yes | Target space ID |
| title | string | Yes | Page title |
| content | string | Yes | Page content (supports wiki markup) |

### updateConfluencePage(cloudId, pageId, title, content)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| cloudId | string | Yes | From getAccessibleAtlassianResources |
| pageId | string | Yes | Existing page ID |
| title | string | Yes | Updated title |
| content | string | Yes | Updated content |

---

## Edge Cases

### CQL vs Semantic Search

Do NOT use `searchConfluenceUsingCql()` for duplicate checking. CQL searches titles/labels, not content meaning. Use the semantic `search()` tool.

### Listing Pages

Do NOT use `getPagesInConfluenceSpace()` as a search substitute. It lists pages, doesn't search content.

### Updating vs Creating

If search finds similar content, offer to update the existing page instead of creating a duplicate.
