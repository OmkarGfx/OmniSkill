# codebolt.state - State Management Tools

## Tools

### `state_get_app`
Retrieves the current application state with configuration and runtime info.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `state_add_agent`
Adds a key-value pair to the agent's persistent state.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | string | Yes | The key to add to agent state |
| value | string | Yes | The value for the key |

### `state_get_agent`
Retrieves all key-value pairs stored in the agent's state.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `state_get_project`
Retrieves project-specific configuration and data.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `state_update_project`
Updates a key-value pair in the project state.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | string | Yes | The key to update |
| value | any | Yes | The value (JSON-serializable) |

## Examples

```javascript
// Get application state
const appState = await codebolt.tools.executeTool(
  "codebolt.state",
  "state_get_app",
  {}
);

// Add to agent state
const addResult = await codebolt.tools.executeTool(
  "codebolt.state",
  "state_add_agent",
  { key: "userPreference", value: "dark-mode" }
);

// Get agent state
const agentState = await codebolt.tools.executeTool(
  "codebolt.state",
  "state_get_agent",
  {}
);

// Get project state
const projectState = await codebolt.tools.executeTool(
  "codebolt.state",
  "state_get_project",
  {}
);

// Update project state
const updateResult = await codebolt.tools.executeTool(
  "codebolt.state",
  "state_update_project",
  { key: "buildConfig", value: { target: "production" } }
);
```
