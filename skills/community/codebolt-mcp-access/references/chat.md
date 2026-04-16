# codebolt.chat - Chat Interaction Tools

## Tools

### `chat_summarize_all`
Summarizes all chat history.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `chat_summarize`
Summarizes a specific set of messages.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| messages | array | Yes | Messages to summarize |
| depth | number | No | Summarization depth |

### `chat_get_history`
Retrieves chat history for a thread.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| threadId | string | Yes | Thread identifier |

### `chat_send`
Sends a message through WebSocket.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | Message to send |
| payload | object | No | Additional payload data |

### `chat_wait_reply`
Waits for user reply to a message.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | Message expecting reply |

### `chat_confirm`
Sends a confirmation request with customizable buttons.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | Confirmation message |
| buttons | array | No | Custom button labels |
| withFeedback | boolean | No | Include feedback option |

### `chat_ask`
Asks a question with customizable responses.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| question | string | Yes | Question to ask |
| buttons | array | No | Custom button labels |
| withFeedback | boolean | No | Include feedback option |

### `chat_notify`
Sends a notification event.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | Notification message |
| type | string | Yes | Type: debug, git, planner, browser, editor, terminal, preview |

### `chat_stop_process`
Stops the ongoing process.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

## Examples

```javascript
// Send message
const sendResult = await codebolt.tools.executeTool(
  "codebolt.chat",
  "chat_send",
  { message: "Processing complete", payload: { status: "success" } }
);

// Wait for reply
const reply = await codebolt.tools.executeTool(
  "codebolt.chat",
  "chat_wait_reply",
  { message: "Please confirm the changes" }
);

// Send notification
const notify = await codebolt.tools.executeTool(
  "codebolt.chat",
  "chat_notify",
  { message: "Debugging auth module", type: "debug" }
);

// Ask question
const answer = await codebolt.tools.executeTool(
  "codebolt.chat",
  "chat_ask",
  { question: "Continue?", buttons: ["Yes", "No", "Skip"] }
);

// Get history
const history = await codebolt.tools.executeTool(
  "codebolt.chat",
  "chat_get_history",
  { threadId: "thread-123" }
);
```
