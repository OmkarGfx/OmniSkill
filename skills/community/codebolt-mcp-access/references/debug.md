# Debug

Debugging utilities.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `debug_open_browser` | Open browser for debugging | url (req), port (req) |
| `debug_add_log` | Add debug log message | log (req), type (req): info/error/warning |

```javascript
await codebolt.tools.executeTool("codebolt.debug", "debug_add_log", {
  log: "Debug message", type: "info"
});
```
