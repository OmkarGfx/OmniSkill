# User Message Utilities

Access current message context information.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `user_utilities_get_current` | Get complete message object | (none) |
| `user_utilities_get_text` | Get message text | (none) |
| `user_utilities_get_mentioned_mcps` | Get mentioned MCPs | (none) |
| `user_utilities_get_mentioned_files` | Get mentioned files | (none) |
| `user_utilities_get_current_file` | Get current file | (none) |
| `user_utilities_get_selection` | Get text selection | (none) |

```javascript
await codebolt.tools.executeTool("codebolt.userMessageUtilities", "user_utilities_get_text", {});
```
