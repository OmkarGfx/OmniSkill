# codebolt.memory - Memory Tools

Memory operations for storing and retrieving data in various formats.

## Basic Memory

### `memory_set`
Store a value in memory.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | string | Yes | Key to store the value under |
| value | any | Yes | Value to store |

### `memory_get`
Retrieve a value from memory.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | string | Yes | Key to retrieve |

## JSON Memory

### `memory_json_save`
Saves a JSON object to memory. Returns memory ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| json | object | Yes | JSON object to save |

### `memory_json_update`
Updates an existing JSON object by memory ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| memoryId | string | Yes | Memory entry ID |
| json | object | Yes | New JSON object |

### `memory_json_delete`
Deletes a JSON object by memory ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| memoryId | string | Yes | Memory entry ID |

### `memory_json_list`
Lists JSON objects with optional filters.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filters | object | No | Optional filters |

## Todo Memory

### `memory_todo_save` / `memory_todo_update` / `memory_todo_delete` / `memory_todo_list`
CRUD operations for todo items. Same pattern as JSON memory with `todo` object and optional `metadata`.

## Markdown Memory

### `memory_markdown_save` / `memory_markdown_update` / `memory_markdown_delete` / `memory_markdown_list`
CRUD operations for markdown content. Uses `markdown` string and optional `metadata`.

## Episodic Memory

### `episodic_memory_create`
Creates a new episodic memory container.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Title for the episodic memory |

### `episodic_memory_append_event`
Appends an event to an episodic memory.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| memoryId | string | Yes | Episodic memory ID |
| event | object | Yes | Event object (event_type, emitting_agent_id, payload required) |

### `episodic_memory_query_events`
Queries events from an episodic memory.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| memoryId | string | No | Memory ID (or use swarmId) |
| swarmId | string | No | Swarm ID (alternative to memoryId) |
| lastMinutes | number | No | Filter events from last N minutes |
| lastCount | number | No | Limit number of events |
| event_type | string | No | Filter by event type |

### `episodic_memory_list` / `episodic_memory_get` / `episodic_memory_archive` / `episodic_memory_update_title`
Additional episodic memory management tools.

## Persistent Memory

### `persistent_memory_create`
Creates persistent memory with retrieval and contribution settings.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| label | string | Yes | Human-readable label |
| retrieval | object | Yes | Retrieval config (source_type, source_id) |
| contribution | object | Yes | Contribution config (format) |

### `persistent_memory_retrieve`
Executes a retrieval query on persistent memory.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| memory_id | string | Yes | Persistent memory ID |
| keywords | array | No | Keywords for retrieval |
| query | string | No | Direct query string |

### `persistent_memory_get` / `persistent_memory_list` / `persistent_memory_update`
Additional persistent memory management tools.

## Examples

```javascript
// Basic memory
await codebolt.tools.executeTool("codebolt.memory", "memory_set",
  { key: "user-pref", value: { theme: "dark" } });

const value = await codebolt.tools.executeTool("codebolt.memory", "memory_get",
  { key: "user-pref" });

// JSON memory
const saved = await codebolt.tools.executeTool("codebolt.memory", "memory_json_save",
  { json: { name: "Config", version: "1.0" } });

// Episodic memory
const memory = await codebolt.tools.executeTool("codebolt.memory", "episodic_memory_create",
  { title: "Session Log" });

await codebolt.tools.executeTool("codebolt.memory", "episodic_memory_append_event",
  {
    memoryId: "mem-id",
    event: { event_type: "action", emitting_agent_id: "agent-1", payload: { action: "click" } }
  });

// Persistent memory
await codebolt.tools.executeTool("codebolt.memory", "persistent_memory_create",
  {
    label: "User Preferences",
    retrieval: { source_type: "kv", source_id: "prefs-store" },
    contribution: { format: "json" }
  });
```
