# codebolt.todo - Task Management Tools

Task management operations for creating, updating, and managing todo items.

## Tools

### `todo_add`
Adds a new todo item.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Title of the todo item |
| priority | string | No | Priority: 'high', 'medium', 'low' |
| tags | string[] | No | Array of tags for organizing |

### `todo_list`
Retrieves the todo list with optional filters.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filters | object | No | Filters to apply (priority, status, etc.) |

### `todo_list_incomplete`
Retrieves all incomplete todo items.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)* | - | - | No parameters required |

### `todo_update`
Updates an existing todo item.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | ID of the todo to update |
| title | string | No | New title |
| status | string | No | Status: 'pending', 'processing', 'completed', 'cancelled' |
| priority | string | No | Priority: 'high', 'medium', 'low' |
| tags | string[] | No | New tags |

### `todo_export`
Exports todos in JSON or markdown format.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| format | string | No | Format: 'json' or 'markdown' |
| listId | string | No | Filter by list ID |
| status | string[] | No | Filter by status values |

### `todo_import`
Imports todos from JSON or markdown format.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| data | string | Yes | Import data (JSON or markdown string) |
| format | string | No | Format: 'json' or 'markdown' |
| mergeStrategy | string | No | Strategy: 'replace' or 'merge' |
| listId | string | No | Target list ID |

## Examples

```javascript
// Add a basic todo
await codebolt.tools.executeTool("codebolt.todo", "todo_add", {
  title: "Implement user authentication"
});

// Add a todo with priority and tags
await codebolt.tools.executeTool("codebolt.todo", "todo_add", {
  title: "Review pull request #42",
  priority: "high",
  tags: ["code-review", "urgent"]
});

// List all todos
await codebolt.tools.executeTool("codebolt.todo", "todo_list", {});

// List with filters
await codebolt.tools.executeTool("codebolt.todo", "todo_list", {
  filters: { priority: "high", status: "pending" }
});

// List incomplete todos
await codebolt.tools.executeTool("codebolt.todo", "todo_list_incomplete", {});

// Update todo status
await codebolt.tools.executeTool("codebolt.todo", "todo_update", {
  id: "todo-123",
  status: "completed"
});

// Export todos as JSON
await codebolt.tools.executeTool("codebolt.todo", "todo_export", {
  format: "json"
});

// Import todos
await codebolt.tools.executeTool("codebolt.todo", "todo_import", {
  data: JSON.stringify([
    { title: "Task 1", priority: "high" },
    { title: "Task 2", priority: "low" }
  ]),
  format: "json",
  mergeStrategy: "merge"
});
```

## Notes

- Statuses: pending, processing, completed, cancelled
- Priorities: high, medium, low
- Supports custom tags for flexible organization
- Import/export for data portability
