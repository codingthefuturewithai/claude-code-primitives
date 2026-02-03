# Knowledge Management Skill - Architecture

```
        ┌────────────────────────────────────────────────┐
        │                 HOW IT TRIGGERS                │
        │                                                │
        │  Explicit:  /knowledge-management              │
        │             (optional: --rag --confluence      │
        │              --both, or no flag)               │
        │                                                │
        │  Implicit:  "store this...", "remember..."     │
        │             (Claude matches skill description) │
        └────────────────────┬───────────────────────────┘
                             │
                             ▼
                ┌───────────────────────────────┐
                │   KNOWLEDGE MANAGEMENT SKILL  │
                │                               │
                │   Teaches Claude how to       │
                │   route content to the        │
                │   right place                 │
                └───────────────┬───────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
    --confluence             (auto)                --rag
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐                       ┌─────────────────┐
│ ATLASSIAN MCP   │                       │ RAG MEMORY MCP  │
│ (MCP Server)    │                       │ (MCP Server)    │
│                 │                       │                 │
│ Gives Claude    │                       │ Gives Claude    │
│ tools to talk   │                       │ tools to talk   │
│ to Confluence   │                       │ to my vector    │
│                 │                       │ store + graph   │
└────────┬────────┘                       └────────┬────────┘
         │                                         │
         ▼                                         ▼
┌─────────────────┐                       ┌─────────────────┐
│   CONFLUENCE    │                       │   RAG MEMORY    │
│                 │                       │                 │
│ Shared docs     │                       │ Vector store    │
│ Team wikis      │                       │ Knowledge graph │
│ (like at PBS)   │                       │ Personal notes  │
└─────────────────┘                       └─────────────────┘
```

**Routing flags (optional):**
- `--confluence` → Confluence only
- `--rag` → RAG Memory only
- `--both` → store in both places
- no flag → skill recommends based on content type
