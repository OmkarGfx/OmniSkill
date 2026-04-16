# codebolt.project - Project Management Tools

## Tools

### `project_get_path`
Retrieves the absolute file system path of the current project.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `project_get_settings`
Retrieves project configuration and settings information.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `project_get_repo_map`
Gets a structured representation of the project repository.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | any | No | Optional filter/configuration parameter |

### `project_run`
Executes the project run command configured for the project.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

### `project_get_editor_status`
Gets information about files currently open or modified in the editor.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

## Examples

```javascript
// Get project path
const pathResult = await codebolt.tools.executeTool(
  "codebolt.project",
  "project_get_path",
  {}
);

// Get project settings
const settingsResult = await codebolt.tools.executeTool(
  "codebolt.project",
  "project_get_settings",
  {}
);

// Get repository map
const repoMapResult = await codebolt.tools.executeTool(
  "codebolt.project",
  "project_get_repo_map",
  { message: "filter query" }
);

// Run project
const runResult = await codebolt.tools.executeTool(
  "codebolt.project",
  "project_run",
  {}
);

// Get editor status
const editorStatusResult = await codebolt.tools.executeTool(
  "codebolt.project",
  "project_get_editor_status",
  {}
);
```
