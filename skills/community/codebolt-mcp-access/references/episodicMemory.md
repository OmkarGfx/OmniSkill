# Episodic Memory

Episode-based memory management for chronological event tracking.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `episodic_create_memory` | Create episodic memory | title (req) |
| `episodic_list_memories` | List all memories | (none) |
| `episodic_get_memory` | Get memory by ID | memoryId or swarmId |
| `episodic_append_event` | Append event to memory | memoryId/swarmId, event_type (req), emitting_agent_id (req), payload (req) |
| `episodic_query_events` | Query events with filters | memoryId/swarmId, lastMinutes, lastCount, tags, event_type |
| `episodic_get_event_types` | Get unique event types | memoryId/swarmId |
| `episodic_get_tags` | Get unique tags | memoryId/swarmId |
| `episodic_get_agents` | Get unique agent IDs | memoryId/swarmId |
| `episodic_archive_memory` | Archive memory | memoryId/swarmId |
| `episodic_unarchive_memory` | Unarchive memory | memoryId/swarmId |
| `episodic_update_title` | Update memory title | memoryId/swarmId, title (req) |

```javascript
await codebolt.tools.executeTool("codebolt.episodicMemory", "episodic_create_memory", {
  title: "Project Planning Session"
});
```
