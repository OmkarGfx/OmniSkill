# Notification

Event-based notifications for system events.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `notification_send` | Send notification with event type | message (req), eventType (req): debug/git/planner/browser/editor/terminal/console/preview |

```javascript
await codebolt.tools.executeTool("codebolt.notification", "notification_send", {
  message: "Build complete", eventType: "terminal"
});
```
