# RAG Memory Reference

## Tool Parameters

### list_collections()

No parameters required. Returns array of collection names.

### get_collection_info(collection_name)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_name | string | Yes | Name of collection |

Returns:
- `name` - Collection name
- `domain` - High-level domain (e.g., "Operations", "Engineering")
- `domain_scope` - Description of what content belongs here
- `description` - Collection purpose

### search_documents(query, collection_name, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language question |
| collection_name | string | No | Limit to specific collection |
| limit | int | No | Max results (default 5) |
| metadata_filter | dict | No | Filter by metadata fields |

### ingest_url(url, collection_name, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | URL to ingest |
| collection_name | string | Yes | Target collection |
| topic | string | No | Topic for relevance |
| follow_links | bool | No | Crawl linked pages |
| max_pages | int | No | Max pages if following links (default 10, max 20) |
| mode | string | No | "ingest" (default) or "reingest" |

### ingest_text(content, collection_name, document_title, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| content | string | Yes | Text content |
| collection_name | string | Yes | Target collection |
| document_title | string | Yes | Document title |
| topic | string | No | Topic for relevance |
| mode | string | No | "ingest" (default) or "reingest" |

### ingest_file(file_path, collection_name, topic, ...)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | Yes | Local file path |
| collection_name | string | Yes | Target collection |
| topic | string | No | Topic for relevance |
| mode | string | No | "ingest" (default) or "reingest" |

## Edge Cases

### Duplicate Detection

If content already exists, you'll get a duplicate error. Options:
- Skip if content hasn't changed
- Use `mode="reingest"` to replace existing content

### Large Content

For URLs with many pages:
1. First call `analyze_website(url)` to see structure
2. Use `max_pages=20` limit per ingest
3. Do multiple ingests for large sites

### File Access

`ingest_file` requires the file to exist on the MCP server's filesystem. For cloud-hosted clients, use `ingest_text` with the file content instead.
