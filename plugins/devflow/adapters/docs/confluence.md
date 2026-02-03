# Confluence Documentation Adapter

## Overview

Adapter patterns for Confluence operations via Atlassian MCP.

---

## Connection Setup

Uses same Cloud ID as Jira:
```
Call mcp__atlassian__getAccessibleAtlassianResources
```

---

## Operations

### List Spaces

```
Call mcp__atlassian__getConfluenceSpaces with:
  - cloudId: [cloudId]
```

Returns array of spaces with:
- `key` - Space key (e.g., "DEV")
- `name` - Space name
- `type` - "global" or "personal"

---

### Get Page

```
Call mcp__atlassian__getConfluencePage with:
  - cloudId: [cloudId]
  - pageId: "123456789"
```

**Response fields:**
- `id` - Page ID
- `title` - Page title
- `body.storage.value` - Content (Confluence storage format)
- `space.key` - Space key
- `version.number` - Current version
- `_links.webui` - Browser URL

---

### Create Page

```
Call mcp__atlassian__createConfluencePage with:
  - cloudId: [cloudId]
  - spaceKey: "DEV"
  - title: "Page Title"
  - content: "<p>Page content in HTML</p>"
```

Optional:
- `parentPageId` - Create as child page

---

### Update Page

```
Call mcp__atlassian__updateConfluencePage with:
  - cloudId: [cloudId]
  - pageId: "123456789"
  - title: "Updated Title"
  - content: "<p>Updated content</p>"
  - version: [current version + 1]
```

**Important:** Must provide incremented version number.

---

### Search Content

```
Call mcp__atlassian__searchConfluenceUsingCql with:
  - cloudId: [cloudId]
  - cql: "text ~ 'search term' AND space = 'DEV'"
```

Common CQL patterns:
- `text ~ "term"` - Full-text search
- `title ~ "term"` - Title search
- `space = "KEY"` - Filter by space
- `type = "page"` - Only pages (not blogs)
- `ancestor = 123` - Under specific parent

---

### Add Comment

**Footer comment:**
```
Call mcp__atlassian__createConfluenceFooterComment with:
  - cloudId: [cloudId]
  - pageId: "123456789"
  - body: "Comment text"
```

**Inline comment:**
```
Call mcp__atlassian__createConfluenceInlineComment with:
  - cloudId: [cloudId]
  - pageId: "123456789"
  - body: "Comment text"
  - inlineCommentProperties: { ... selection info ... }
```

---

### Get Page Hierarchy

```
Call mcp__atlassian__getConfluencePageDescendants with:
  - cloudId: [cloudId]
  - pageId: "123456789"
```

---

## Content Format

Confluence uses storage format (XHTML-like):

```html
<p>Paragraph text</p>
<h1>Heading</h1>
<ul>
  <li>List item</li>
</ul>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">python</ac:parameter>
  <ac:plain-text-body><![CDATA[print("hello")]]></ac:plain-text-body>
</ac:structured-macro>
```

---

## Organization Patterns

### Recommended Structure

```
Space: DEV
├── Home
├── Technical Documentation
│   ├── Architecture
│   ├── Setup Guides
│   └── API Reference
├── Project Plans
│   └── [Issue-KEY] Implementation Plan
└── Knowledge Base
    └── Troubleshooting
```

### DevFlow Convention

For plan documents created via `/devflow:plan-work`:
- Space: Project-specific space
- Parent: "Project Plans" or "DevFlow Plans"
- Title: `[ISSUE-KEY] Implementation Plan`

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| 401 | Authentication failed | Check API token |
| 403 | Permission denied | Check space permissions |
| 404 | Page not found | Verify page ID |
| 409 | Version conflict | Fetch current version and retry |
