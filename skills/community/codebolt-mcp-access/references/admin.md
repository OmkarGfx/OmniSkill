# codebolt.admin - Administrative Tools

Administrative tools for managing orchestrators, codemaps, hooks, and event logs.

## Tools

### `orchestrator_list`
Lists all orchestrators with their IDs, names, descriptions, and metadata.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)* | - | - | No parameters required |

### `orchestrator_get`
Gets a specific orchestrator by its ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orchestrator_id | string | Yes | Unique identifier of the orchestrator |

### `orchestrator_create`
Creates a new orchestrator instance.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the orchestrator |
| description | string | Yes | Description of what the orchestrator does |
| agent_id | string | Yes | ID of the agent to associate |
| default_worker_agent_id | string | No | ID of the default worker agent |
| metadata | object | No | Additional metadata as key-value pairs |

### `orchestrator_update`
Updates an existing orchestrator's properties.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orchestrator_id | string | Yes | Unique identifier of the orchestrator |
| name | string | No | New name |
| description | string | No | New description |
| agent_id | string | No | New agent ID |
| metadata | object | No | Updated metadata |

### `codemap_list`
Lists all codemaps for a project.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_path | string | No | Project path (defaults to current project) |

### `codemap_get`
Gets a specific codemap by its ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| codemap_id | string | Yes | Unique identifier of the codemap |
| project_path | string | No | Project path (defaults to current project) |

### `codemap_create`
Creates a new codemap placeholder.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Title for the new codemap |
| query | string | No | Query describing the code structure |
| project_path | string | No | Project path (defaults to current project) |

### `hook_create`
Creates a new hook for triggering actions based on events.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the hook |
| trigger | string | Yes | Trigger event type (file.modified, git.commit, etc.) |
| action | string | Yes | Action to perform (notify, execute, log, webhook, agent) |
| trigger_config | object | No | Trigger configuration (pattern, path, etc.) |
| action_config | object | No | Action configuration (command, url, etc.) |
| enabled | boolean | No | Whether hook is enabled (default: true) |

### `hook_list`
Lists all hooks with their configurations.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)* | - | - | No parameters required |

### `hook_enable` / `hook_disable`
Enables or disables a hook.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| hook_id | string | Yes | Unique identifier of the hook |

### `eventlog_create_instance`
Creates a new event log instance.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name for the event log instance |
| description | string | No | Description of the event log |

### `eventlog_append_event`
Appends a new event to an event log instance.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | ID of the event log instance |
| event_type | string | No | Type of event being logged |
| payload | object | No | Event payload data |
| stream_id | string | No | Stream ID to categorize the event |
| metadata | object | No | Optional metadata |

### `eventlog_query_events`
Queries events using DSL-based filtering.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | ID of the event log instance |
| stream_id | string | No | Filter by stream ID |
| conditions | array | No | Filter conditions (field, operator, value) |
| order_by | object | No | Ordering (field, direction) |
| limit | number | No | Maximum events to return |

## Examples

```javascript
// Create an orchestrator
await codebolt.tools.executeTool("codebolt.admin", "orchestrator_create", {
  name: "Task Orchestrator",
  description: "Manages task distribution",
  agent_id: "agent-001"
});

// Create a hook for file changes
await codebolt.tools.executeTool("codebolt.admin", "hook_create", {
  name: "Test Runner",
  trigger: "file.modified",
  trigger_config: { pattern: "src/**/*.ts" },
  action: "execute",
  action_config: { command: "npm test" }
});

// Append an event
await codebolt.tools.executeTool("codebolt.admin", "eventlog_append_event", {
  instance_id: "log-123",
  event_type: "task_completed",
  payload: { task_id: "task-456", duration_ms: 5000 }
});
```
