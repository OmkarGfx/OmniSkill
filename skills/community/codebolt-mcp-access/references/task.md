# Task

Task CRUD operations for managing work items.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `task_create` | Create a new task | title (req), description, thread_id |
| `task_list` | List all tasks | (none) |
| `task_update` | Update task properties | task_id (req), name, completed, status |

```javascript
await codebolt.tools.executeTool("codebolt.task", "task_create", {
  title: "New task", description: "Task description"
});
```
