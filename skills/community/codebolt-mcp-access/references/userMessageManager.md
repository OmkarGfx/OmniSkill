# User Message Manager

Access user message context and metadata.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `user_message_get_current` | Get current message object | (none) |
| `user_message_get_text` | Get message text | (none) |
| `user_message_get_config` | Get processing config | (none) |
| `user_message_get_mentioned_files` | Get mentioned files | (none) |

```javascript
const result = await codebolt.tools.executeTool("codebolt.userMessageManager", "user_message_get_current", {});
```
