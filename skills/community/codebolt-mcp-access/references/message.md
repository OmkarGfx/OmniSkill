# Message

Message handling and process management.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `message_send` | Send a message | message (req) |
| `message_process_start` | Start message processing | process (req), message (req) |
| `message_process_stop` | Stop message processing | process (req), message (req) |

```javascript
await codebolt.tools.executeTool("codebolt.message", "message_send", {
  message: "Hello MCP"
});
```
