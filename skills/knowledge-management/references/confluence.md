# Confluence Reference

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

This is the semantic search tool. Use this for duplicate checking.

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

## Edge Cases

### CQL vs Semantic Search

Do NOT use `searchConfluenceUsingCql()` for duplicate checking. CQL searches titles/labels, not content meaning. Use the semantic `search()` tool.

### Listing Pages

Do NOT use `getPagesInConfluenceSpace()` as a search substitute. It lists pages, doesn't search content.

### Updating vs Creating

If search finds similar content, offer to update the existing page instead of creating a duplicate. Use `updateConfluencePage()` with the page ID from search results.
