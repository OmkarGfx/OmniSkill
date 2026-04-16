# Codebolt Event

Event management for background agent coordination.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `event_add_running_agent` | Add running agent to tracking | threadId (req), data (req), groupId |
| `event_get_running_agent_count` | Get running agent count | (none) |
| `event_check_background_agent_completion` | Check for completed agents (non-blocking) | (none) |
| `event_on_background_agent_completion` | Wait for agent completion (blocking) | (none) |
| `event_wait_for_external_event` | Wait for any external event | (none) |

```javascript
await codebolt.tools.executeTool("codebolt.event", "event_add_running_agent", {
  threadId: "thread-123",
  data: { task: "process-data" }
});
```
