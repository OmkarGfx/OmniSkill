# codebolt.mcp - MCP Server Tools

Tools for managing and interacting with Model Context Protocol (MCP) servers.

## Tools

### `mcp_list_servers`
Lists all enabled MCP servers that are currently active.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)* | - | - | No parameters required |

### `mcp_get_tools`
Gets available MCP tools, optionally filtered by server.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| serverName | string | No | Server name to filter tools (returns all if not provided) |

### `mcp_execute_tool`
Executes an MCP tool on a specified server.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| serverName | string | Yes | Name of the MCP server |
| toolName | string | Yes | Name of the tool to execute |
| params | object | No | Parameters to pass to the tool |

### `mcp_configure_server`
Configures an MCP server with settings.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| serverName | string | Yes | Name of the MCP server |
| config | object | Yes | Configuration settings to apply |

## Examples

```javascript
// List all enabled MCP servers
await codebolt.tools.executeTool("codebolt.mcp", "mcp_list_servers", {});

// Get tools from all servers
await codebolt.tools.executeTool("codebolt.mcp", "mcp_get_tools", {});

// Get tools from a specific server
await codebolt.tools.executeTool("codebolt.mcp", "mcp_get_tools", {
  serverName: "github-server"
});

// Execute a tool on an MCP server
await codebolt.tools.executeTool("codebolt.mcp", "mcp_execute_tool", {
  serverName: "github-server",
  toolName: "create_issue",
  params: {
    repository: "owner/repo",
    title: "Bug Report",
    body: "Description of the issue",
    labels: ["bug"]
  }
});

// Configure an MCP server
await codebolt.tools.executeTool("codebolt.mcp", "mcp_configure_server", {
  serverName: "custom-server",
  config: {
    apiKey: "your-api-key",
    baseUrl: "https://api.example.com",
    timeout: 30000,
    retries: 3
  }
});
```

## Notes

- MCP servers extend agent capabilities with external tools and services
- Use `mcp_list_servers` to discover available servers
- Use `mcp_get_tools` to see what tools each server provides
- Use `mcp_execute_tool` to invoke tools with appropriate parameters
