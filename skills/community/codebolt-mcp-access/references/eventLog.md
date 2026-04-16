# Event Log

Event logging with DSL query support.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `eventlog_create_instance` | Create event log | name (req), description |
| `eventlog_get_instance` | Get instance by ID | instanceId (req) |
| `eventlog_list_instances` | List all instances | (none) |
| `eventlog_update_instance` | Update instance | instanceId (req), name, description |
| `eventlog_delete_instance` | Delete instance | instanceId (req) |
| `eventlog_append_event` | Append single event | instanceId (req), stream_id, event_type, payload, metadata |
| `eventlog_append_events` | Append multiple events | instanceId (req), events (req) |
| `eventlog_query_events` | Query with DSL | query (req): {from, where, select, orderBy, limit, reduce} |
| `eventlog_get_instance_stats` | Get statistics | instanceId (req) |

```javascript
await codebolt.tools.executeTool("codebolt.eventLog", "eventlog_append_event", {
  instanceId: "app_logs",
  stream_id: "user_actions",
  event_type: "user_login",
  payload: { userId: "user123" }
});
```
