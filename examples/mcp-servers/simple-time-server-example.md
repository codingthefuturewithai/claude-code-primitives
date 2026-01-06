# MCP Server Example: Simple Time Server

This is a working example of a basic MCP server that provides time-related tools.

## What is an MCP Server?

MCP (Model Context Protocol) servers extend Claude Code with custom tools that connect to external services, APIs, or provide specialized functionality.

## Configuration File

**Location**: `.mcp.json` at project root

```json
{
  "mcpServers": {
    "time-server": {
      "command": "node",
      "args": ["${CLAUDE_PROJECT_DIR}/mcp-servers/time-server/index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

### Key Fields

- **Server name**: `"time-server"` - Unique identifier
- **command**: `"node"` - How to run the server
- **args**: Path to server implementation
- **env**: Environment variables (optional)

## Server Implementation

**File**: `mcp-servers/time-server/index.js`

```javascript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "time-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_current_time",
        description: "Get the current time in a specific timezone",
        inputSchema: {
          type: "object",
          properties: {
            timezone: {
              type: "string",
              description: "IANA timezone (e.g., 'America/New_York', 'Europe/London')",
              default: "UTC",
            },
            format: {
              type: "string",
              description: "Time format: '12h', '24h', or 'iso'",
              enum: ["12h", "24h", "iso"],
              default: "24h",
            },
          },
        },
      },
      {
        name: "calculate_time_difference",
        description: "Calculate time difference between two timezones",
        inputSchema: {
          type: "object",
          properties: {
            timezone1: {
              type: "string",
              description: "First timezone",
            },
            timezone2: {
              type: "string",
              description: "Second timezone",
            },
          },
          required: ["timezone1", "timezone2"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "get_current_time") {
    const { timezone = "UTC", format = "24h" } = args;
    const now = new Date();

    const options = {
      timeZone: timezone,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: format === "12h",
    };

    if (format === "iso") {
      return {
        content: [
          {
            type: "text",
            text: now.toISOString(),
          },
        ],
      };
    }

    const timeString = now.toLocaleTimeString("en-US", options);
    return {
      content: [
        {
          type: "text",
          text: `Current time in ${timezone}: ${timeString}`,
        },
      ],
    };
  }

  if (name === "calculate_time_difference") {
    const { timezone1, timezone2 } = args;
    const now = new Date();

    const formatter1 = new Intl.DateTimeFormat("en-US", {
      timeZone: timezone1,
      hour: "numeric",
      hour12: false,
    });
    const formatter2 = new Intl.DateTimeFormat("en-US", {
      timeZone: timezone2,
      hour: "numeric",
      hour12: false,
    });

    const hour1 = parseInt(formatter1.format(now));
    const hour2 = parseInt(formatter2.format(now));
    const difference = hour2 - hour1;

    return {
      content: [
        {
          type: "text",
          text: `Time difference between ${timezone1} and ${timezone2}: ${difference} hours`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Time MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```

## Package Configuration

**File**: `mcp-servers/time-server/package.json`

```json
{
  "name": "time-server",
  "version": "1.0.0",
  "description": "MCP server for time-related tools",
  "type": "module",
  "main": "index.js",
  "bin": {
    "time-server": "./index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Installation

1. **Install dependencies**:
   ```bash
   cd mcp-servers/time-server
   npm install
   ```

2. **Add to project** (`.mcp.json`):
   ```json
   {
     "mcpServers": {
       "time-server": {
         "command": "node",
         "args": ["${CLAUDE_PROJECT_DIR}/mcp-servers/time-server/index.js"]
       }
     }
   }
   ```

3. **Or use CLI**:
   ```bash
   claude mcp add --transport stdio time-server -- node mcp-servers/time-server/index.js
   ```

## Usage in Claude Code

Once configured, the tools are available:

```
What time is it in Tokyo?

# Claude uses mcp__time-server__get_current_time tool
# Returns: "Current time in Asia/Tokyo: 15:30:45"

What's the time difference between New York and London?

# Claude uses mcp__time-server__calculate_time_difference tool
# Returns: "Time difference between America/New_York and Europe/London: 5 hours"
```

## Key Concepts

### 1. Server Metadata

```javascript
const server = new Server(
  {
    name: "time-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);
```

Identifies the server and declares it provides tools.

### 2. Tool Definition

```javascript
{
  name: "get_current_time",
  description: "Get the current time in a specific timezone",
  inputSchema: {
    type: "object",
    properties: {
      timezone: {
        type: "string",
        description: "IANA timezone...",
      }
    }
  }
}
```

- **name**: Tool identifier (used as `mcp__time-server__get_current_time`)
- **description**: Helps Claude know when to use this tool
- **inputSchema**: JSON Schema for parameters

### 3. Tool Handler

```javascript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "get_current_time") {
    // Implementation
    return {
      content: [{ type: "text", text: result }]
    };
  }
});
```

Handles tool execution and returns results.

### 4. Transport

```javascript
const transport = new StdioServerTransport();
await server.connect(transport);
```

Uses stdio for communication with Claude Code.

## Best Practices Demonstrated

### ✅ Clear Tool Descriptions

```javascript
description: "Get the current time in a specific timezone"
```

Helps Claude understand when to use the tool.

### ✅ JSON Schema Validation

```javascript
inputSchema: {
  type: "object",
  properties: {
    timezone: { type: "string", description: "..." }
  }
}
```

Ensures parameters are validated before execution.

### ✅ Default Values

```javascript
timezone: {
  type: "string",
  default: "UTC",
}
```

Provides sensible defaults for optional parameters.

### ✅ Error Handling

```javascript
throw new Error(`Unknown tool: ${name}`);
```

Handles unexpected tool names gracefully.

## Common Mistakes to Avoid

### ❌ Missing Error Handling

```javascript
// WRONG - no error handling
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const result = someOperation();
  return { content: [{ type: "text", text: result }] };
});
```

### ✅ Proper Error Handling

```javascript
// CORRECT
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const result = someOperation();
    return { content: [{ type: "text", text: result }] };
  } catch (error) {
    throw new Error(`Operation failed: ${error.message}`);
  }
});
```

### ❌ Missing inputSchema

```javascript
// WRONG - Claude doesn't know what parameters to provide
{
  name: "get_time",
  description: "Get time"
}
```

### ✅ Complete Schema

```javascript
// CORRECT
{
  name: "get_time",
  description: "Get current time",
  inputSchema: {
    type: "object",
    properties: { /* ... */ }
  }
}
```

## Directory Structure

```
mcp-servers/
└── time-server/
    ├── package.json
    ├── index.js
    └── README.md
```

## Testing

1. **Start server manually**:
   ```bash
   node mcp-servers/time-server/index.js
   ```

2. **Check logs**:
   Should see: "Time MCP server running on stdio"

3. **Test in Claude Code**:
   ```
   /mcp
   # Should list time-server with its tools
   ```

4. **Use the tools**:
   ```
   What time is it in Tokyo?
   ```

## Extension Points

To enhance this server:

1. **Add more tools**:
   - `convert_timezone` - Convert time between zones
   - `schedule_reminder` - Set time-based reminders
   - `parse_date` - Parse natural language dates

2. **Add authentication**:
   ```javascript
   const API_KEY = process.env.TIME_API_KEY;
   if (!API_KEY) {
     throw new Error("TIME_API_KEY required");
   }
   ```

3. **Add external API calls**:
   ```javascript
   const response = await fetch("https://worldtimeapi.org/api/timezone/" + timezone);
   ```

## References

- **MCP SDK**: https://github.com/modelcontextprotocol/sdk
- **Transport Types**: stdio, SSE, HTTP
- **Tool Schema**: JSON Schema specification
