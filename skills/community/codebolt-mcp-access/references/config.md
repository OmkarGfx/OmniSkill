# Config

MCP server configuration management.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `mcp_configure_server` | Configure MCP server settings | serverName (req), config (req): {command, args[]} |

```javascript
await codebolt.tools.executeTool("codebolt.config", "mcp_configure_server", {
  serverName: "filesystem",
  config: { command: "npx", args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"] }
});
```
