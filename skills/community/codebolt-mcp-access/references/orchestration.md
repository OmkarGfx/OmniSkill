# codebolt.orchestration - Orchestration Tools

Tools for managing tasks, agents, and threads in multi-agent workflows.

## Task Management

### `task_create`
Creates a new task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Title/name of the task |
| description | string | No | Task description |
| thread_id | string | No | Thread ID for the task |

### `task_update`
Updates an existing task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | string | Yes | Task ID to update |
| name | string | No | New name for the task |
| completed | boolean | No | Whether task is completed |
| status | string | No | Task status ('completed', 'pending') |

### `task_delete`
Deletes a task by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | string | Yes | Task ID to delete |

### `task_list`
Retrieves all tasks. No parameters required.

### `task_get`
Retrieves details of a specific task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | string | Yes | Task ID to retrieve |

### `task_assign`
Assigns an agent to a task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | string | Yes | Task ID |
| agent_id | string | Yes | Agent ID to assign |

### `task_execute`
Executes a task with a specific agent.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | string | Yes | Task ID to execute |
| agent_id | string | Yes | Agent ID to execute with |

## Agent Management

### `agent_find`
Finds agents suitable for a given task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task | string | Yes | Task description to find agents for |
| max_results | number | No | Maximum results (default: 3) |

### `agent_start`
Starts an agent with a specific task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_id | string | Yes | Agent ID to start |
| task | string | Yes | Task for the agent |

### `agent_list`
Lists all available agents. No parameters required.

### `agent_details`
Retrieves details of specific agents.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_list | array | No | List of agent IDs |

## Thread Management

### `thread_create`
Creates a new thread.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| options | object | Yes | Thread creation options (name, priority, etc.) |

### `thread_create_start`
Creates and immediately starts a new thread.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| options | object | Yes | Thread options (name, agent_id, etc.) |

### `thread_create_background`
Creates a thread in background.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| options | object | Yes | Thread creation options |
| groupId | string | No | Optional group ID |

### `thread_list`
Retrieves threads with optional filtering.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| options | object | No | Filtering options (status, etc.) |

### `thread_get`
Retrieves thread information.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| threadId | string | Yes | Thread ID |

### `thread_start` / `thread_update` / `thread_delete`
Thread lifecycle management by threadId.

### `thread_get_messages`
Retrieves messages for a thread.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| threadId | string | Yes | Thread ID |
| limit | number | No | Message limit |
| offset | number | No | Pagination offset |
| before | string | No | Messages before timestamp |
| after | string | No | Messages after timestamp |

### `thread_update_status`
Updates thread status.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| threadId | string | Yes | Thread ID |
| status | string | Yes | New status |

## Examples

```javascript
// Create and manage tasks
const task = await codebolt.tools.executeTool("codebolt.orchestration", "task_create",
  { title: "Implement auth", description: "Add JWT-based auth flow" });

await codebolt.tools.executeTool("codebolt.orchestration", "task_update",
  { task_id: "task-456", status: "completed" });

// Find and start agents
const agents = await codebolt.tools.executeTool("codebolt.orchestration", "agent_find",
  { task: "Write unit tests", max_results: 5 });

await codebolt.tools.executeTool("codebolt.orchestration", "agent_start",
  { agent_id: "agent-789", task: "Review login component" });

// Manage threads
const thread = await codebolt.tools.executeTool("codebolt.orchestration", "thread_create",
  { options: { name: "Feature Dev", priority: "high" } });

await codebolt.tools.executeTool("codebolt.orchestration", "thread_start",
  { threadId: "thread-123" });

const messages = await codebolt.tools.executeTool("codebolt.orchestration", "thread_get_messages",
  { threadId: "thread-123", limit: 50 });

// Assign and execute
await codebolt.tools.executeTool("codebolt.orchestration", "task_assign",
  { task_id: "task-456", agent_id: "agent-789" });

await codebolt.tools.executeTool("codebolt.orchestration", "task_execute",
  { task_id: "task-456", agent_id: "agent-789" });
```
