# codebolt.agent - Agent Management Tools

## Tools

### `agent_start`
Starts an agent with a specific task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_id | string | Yes | ID of the agent to start |
| task | string | Yes | Task for the agent to execute |

### `agent_find`
Finds agents suitable for a given task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task | string | Yes | Task description to match |
| max_results | number | No | Maximum results (default: 3) |

### `agent_list`
Lists all available agents.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `agent_details`
Retrieves details of specific agents.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_list | string[] | No | List of agent IDs |

## Examples

```javascript
// Start an agent
const startResult = await codebolt.tools.executeTool(
  "codebolt.agent",
  "agent_start",
  { agent_id: "code-assistant", task: "Review the authentication module" }
);

// Find agents for a task
const findResult = await codebolt.tools.executeTool(
  "codebolt.agent",
  "agent_find",
  { task: "create node js application", max_results: 5 }
);

// List all agents
const listResult = await codebolt.tools.executeTool(
  "codebolt.agent",
  "agent_list",
  {}
);

// Get agent details
const detailResult = await codebolt.tools.executeTool(
  "codebolt.agent",
  "agent_details",
  { agent_list: ["ask", "act", "code-reviewer"] }
);
```
