# PRD: BlogWatcher MCP Server

## Overview

An MCP (Model Context Protocol) server that wraps the existing `blogwatcher` CLI tool, exposing its RSS feed management and article tracking capabilities to AI agents and MCP-compatible clients.

## Problem Statement

BlogWatcher is a robust CLI tool for managing RSS feeds with proper read/unread article tracking—a feature missing from all existing RSS MCP servers. However, it's only accessible via command line, requiring workarounds like Clawdbot skills to integrate with AI workflows. A native MCP interface would enable direct, seamless integration with Claude Desktop, Claude Code, Cursor, and other MCP clients.

## Goals

1. Expose all core blogwatcher functionality via MCP tools
2. Zero modifications to blogwatcher itself—pure wrapper
3. Maintain blogwatcher's SQLite storage (`~/.blogwatcher/blogwatcher.db`)
4. Provide clean, well-typed tool interfaces suitable for LLM consumption

## Non-Goals

- Replacing or forking blogwatcher
- Adding features not present in blogwatcher CLI
- Managing multiple user databases
- Web UI or REST API

---

## MCP Tools Specification

### Tool 1: `add_blog`

**Description**: Add a new blog/RSS feed to track.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Unique identifier for the blog (e.g., "simonwillison") |
| `url` | string | Yes | Blog homepage URL or direct RSS feed URL |
| `feed_url` | string | No | Explicit RSS/Atom feed URL if different from main URL |
| `scrape_selector` | string | No | CSS selector for scraping if RSS unavailable |

**Underlying CLI**: 
```bash
blogwatcher add <name> <url> [--feed-url <feed_url>] [--scrape-selector <selector>]
```

**Returns**: Confirmation message with blog name and feed URL detected/used.

**Example**:
```json
{
  "name": "simonwillison",
  "url": "https://simonwillison.net",
  "feed_url": "https://simonwillison.net/atom/everything/"
}
```

---

### Tool 2: `remove_blog`

**Description**: Remove a blog and all its tracked articles from the database.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Name of the blog to remove |
| `confirm` | boolean | No | Skip confirmation prompt (default: true for MCP usage) |

**Underlying CLI**:
```bash
blogwatcher remove <name> -y
```

**Returns**: Confirmation of removal.

---

### Tool 3: `list_blogs`

**Description**: List all configured blogs/feeds.

**Parameters**: None

**Underlying CLI**:
```bash
blogwatcher blogs
```

**Returns**: Array of blog objects with name, URL, feed URL, and article counts.

**Example Response**:
```json
{
  "blogs": [
    {
      "name": "simonwillison",
      "url": "https://simonwillison.net",
      "feed_url": "https://simonwillison.net/atom/everything/",
      "total_articles": 30,
      "unread_articles": 5
    },
    {
      "name": "anthropic-engineering",
      "url": "https://www.anthropic.com/engineering",
      "feed_url": "https://raw.githubusercontent.com/...",
      "total_articles": 17,
      "unread_articles": 17
    }
  ],
  "total_blogs": 2,
  "total_unread": 22
}
```

---

### Tool 4: `scan_blogs`

**Description**: Fetch new articles from all blogs or a specific blog.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `blog_name` | string | No | Specific blog to scan (omit for all blogs) |
| `silent` | boolean | No | Suppress detailed output (default: false) |
| `workers` | integer | No | Number of parallel workers (default: 4) |

**Underlying CLI**:
```bash
blogwatcher scan [blog_name] [-s] [-w <workers>]
```

**Returns**: Summary of new articles found per blog.

**Example Response**:
```json
{
  "scanned": 9,
  "new_articles": 12,
  "blogs_updated": [
    {"name": "simonwillison", "new": 3},
    {"name": "latentspace", "new": 9}
  ]
}
```

---

### Tool 5: `list_articles`

**Description**: List articles, optionally filtered by blog and read status.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `blog_name` | string | No | Filter to specific blog |
| `include_read` | boolean | No | Include already-read articles (default: false, shows unread only) |
| `limit` | integer | No | Maximum articles to return (default: 50) |

**Underlying CLI**:
```bash
blogwatcher articles [-b <blog_name>] [-a]
```

**Returns**: Array of article objects.

**Example Response**:
```json
{
  "articles": [
    {
      "id": 241,
      "title": "One Human + One Agent = One Browser From Scratch",
      "url": "https://simonwillison.net/2026/Jan/27/one-human-one-agent/",
      "blog_name": "simonwillison",
      "published": "2026-01-27T16:58:00Z",
      "is_read": false
    },
    {
      "id": 240,
      "title": "Kimi K2.5: Visual Agentic Intelligence",
      "url": "https://simonwillison.net/2026/Jan/27/kimi-k25/",
      "blog_name": "simonwillison", 
      "published": "2026-01-27T15:07:00Z",
      "is_read": false
    }
  ],
  "total": 2,
  "showing": "unread"
}
```

---

### Tool 6: `mark_article_read`

**Description**: Mark a specific article as read.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `article_id` | integer | Yes | ID of the article to mark as read |

**Underlying CLI**:
```bash
blogwatcher read <article_id>
```

**Returns**: Confirmation with article title.

---

### Tool 7: `mark_all_read`

**Description**: Mark all articles as read, optionally filtered to a specific blog.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `blog_name` | string | No | Only mark articles from this blog as read |
| `confirm` | boolean | Yes | Must be true to execute (safety measure) |

**Underlying CLI**:
```bash
blogwatcher read-all [--blog <name>] --yes
```

**Returns**: Count of articles marked as read.

**Example Response**:
```json
{
  "marked_read": 47,
  "blog_filter": null,
  "message": "Marked 47 articles as read"
}
```

---

### Tool 8: `mark_article_unread`

**Description**: Mark a specific article as unread.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `article_id` | integer | Yes | ID of the article to mark as unread |

**Underlying CLI**:
```bash
blogwatcher unread <article_id>
```

**Returns**: Confirmation with article title.

---

## Implementation Notes

### CLI Execution Strategy

The MCP server should execute blogwatcher commands via subprocess and parse the output. Two approaches:

1. **Parse CLI output** (simpler): Run `blogwatcher <command>` and parse stdout
2. **Direct SQLite access** (faster): Read/write `~/.blogwatcher/blogwatcher.db` directly

**Recommendation**: Start with CLI wrapping for safety and compatibility. Blogwatcher's output is relatively structured. Direct SQLite access could be added later for performance if needed.

### Error Handling

- Blog not found → Return clear error with available blog names
- Network errors during scan → Return partial results with error details
- Invalid article ID → Return error with valid ID range hint

### Configuration

The MCP server should respect blogwatcher's default paths:
- Database: `~/.blogwatcher/blogwatcher.db`
- No additional configuration required

Optional environment variable:
- `BLOGWATCHER_PATH`: Custom path to blogwatcher executable (default: assumes it's in PATH)

---

## Example MCP Client Usage

### Claude Desktop / Claude Code

```
User: "What new articles do I have?"

Agent: [calls list_articles with include_read=false]

Agent: "You have 12 unread articles across your feeds:
- 3 from Simon Willison's blog
- 5 from Latent Space  
- 4 from Anthropic Engineering

Would you like me to show you the titles?"
```

```
User: "Show me the Simon Willison articles and mark them as read after"

Agent: [calls list_articles with blog_name="simonwillison"]
Agent: [displays articles]
Agent: [calls mark_article_read for each, or mark_all_read with blog_name="simonwillison"]
```

```
User: "Add the Anthropic research blog"

Agent: [calls add_blog with name="anthropic-research", url="https://www.anthropic.com/research"]

Agent: "Added 'anthropic-research'. Would you like me to scan for articles now?"
```

---

## Success Criteria

1. All 8 tools functional and returning structured JSON
2. Full compatibility with existing blogwatcher database
3. Works with Claude Desktop, Claude Code, and Cursor
4. No blogwatcher modifications required
5. Handles errors gracefully with actionable messages

---

## Future Enhancements (Out of Scope for v1)

- Article content fetching (full text, not just titles)
- Search across article titles/content
- Export/import OPML
- Scheduled background scanning
- Article tagging/categorization beyond read/unread
