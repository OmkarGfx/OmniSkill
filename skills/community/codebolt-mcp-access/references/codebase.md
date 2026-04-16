# codebolt.codebase - Code Search Tools

Code search tools for exploring and understanding codebases.

## Tools

### `codebase_search`
Performs semantic search across the codebase using natural language.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language description of what you're looking for |
| target_directories | array | No | Directory paths to limit the search scope |

### `search_mcp_tool`
Searches for available MCP tools that can help with a task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Description of what you need a tool for |
| tags | array | No | Tags to filter results |

## Examples

```javascript
// Search codebase for authentication code
await codebolt.tools.executeTool("codebolt.codebase", "codebase_search", {
  query: "function that handles user authentication"
});

// Search with directory scope
await codebolt.tools.executeTool("codebolt.codebase", "codebase_search", {
  query: "error handling for API requests",
  target_directories: ["/src/api", "/src/utils"]
});

// Search for MCP tools
await codebolt.tools.executeTool("codebolt.codebase", "search_mcp_tool", {
  query: "send email"
});

// Search MCP tools with tags
await codebolt.tools.executeTool("codebolt.codebase", "search_mcp_tool", {
  query: "database query",
  tags: ["database", "api"]
});
```

## Notes

- `codebase_search` uses semantic search (understands code concepts, not just literal text)
- Good for finding implementations, understanding patterns, locating relevant code
- `search_mcp_tool` discovers available tools and their capabilities
