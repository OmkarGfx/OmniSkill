# codebolt.planning - Planning & Roadmap Tools

## Plan Tools

### `plan_create`
Creates a new action plan.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name/title of the plan |
| description | string | No | Plan description |
| agentId | string | No | Associated agent ID |
| agentName | string | No | Associated agent name |
| status | string | No | Initial status (active, pending) |
| planId | string | No | Custom plan ID |

### `plan_get_detail`
Retrieves plan details by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | string | Yes | Plan ID to retrieve |

### `plan_get_all`
Retrieves all action plans with optional filters.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter by status |
| agentId | string | No | Filter by agent ID |

### `plan_update`
Updates an existing action plan.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | string | Yes | Plan ID to update |
| updates | object | Yes | Fields to update (name, description, status, agentId, agentName) |

### `plan_add_task`
Adds a task to a plan.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | string | Yes | Plan ID |
| task | object | Yes | Task object with name (required), description, priority, taskType |

### `plan_start_task`
Starts a task within a plan.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| planId | string | Yes | Plan ID |
| taskId | string | Yes | Task ID to start |

## Roadmap Tools

### `roadmap_get`
Retrieves complete project roadmap.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_path | string | No | Project path (uses active project if omitted) |

### `roadmap_get_phases`
Retrieves all roadmap phases.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_path | string | No | Project path |

### `roadmap_create_phase`
Creates a new roadmap phase.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Phase name |
| description | string | No | Phase description |
| order | number | No | Position in sequence |
| project_path | string | No | Project path |

### `roadmap_update_phase`
Updates an existing phase.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| phase_id | string | Yes | Phase ID |
| name | string | No | New name |
| description | string | No | New description |
| order | number | No | New order |
| project_path | string | No | Project path |

### `roadmap_delete_phase`
Deletes a phase (removes associated features).
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| phase_id | string | Yes | Phase ID to delete |
| project_path | string | No | Project path |

### `roadmap_get_features`
Retrieves features in a phase.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| phase_id | string | Yes | Phase ID |
| project_path | string | No | Project path |

### `roadmap_create_feature`
Creates a feature in a phase.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| phase_id | string | Yes | Phase ID |
| title | string | Yes | Feature title |
| description | string | No | Feature description |
| impact | string | No | low, medium, high, critical |
| difficulty | string | No | easy, medium, hard, very-hard |
| priority | number | No | Priority number |
| tags | array | No | Tags for categorization |
| category | string | No | Feature category |
| status | string | No | pending, in-progress, completed, cancelled |
| project_path | string | No | Project path |

### `roadmap_update_feature`
Updates an existing feature.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| feature_id | string | Yes | Feature ID |
| title | string | No | New title |
| description | string | No | New description |
| impact | string | No | New impact level |
| difficulty | string | No | New difficulty level |
| priority | number | No | New priority |
| tags | array | No | New tags |
| category | string | No | New category |
| status | string | No | New status |
| project_path | string | No | Project path |

### `roadmap_get_ideas`
Retrieves all pre-roadmap ideas.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_path | string | No | Project path |

### `roadmap_create_idea`
Creates a new idea suggestion.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Idea title |
| description | string | No | Idea description |
| category | string | No | Idea category |
| suggested_impact | string | No | Suggested impact level |
| suggested_difficulty | string | No | Suggested difficulty level |
| tags | array | No | Tags for categorization |
| project_path | string | No | Project path |

## Examples

```javascript
// Create an action plan
const plan = await codebolt.tools.executeTool(
  "codebolt.planning", "plan_create",
  { name: "Sprint 1", description: "First sprint tasks", status: "active" }
);

// Add a task to the plan
await codebolt.tools.executeTool(
  "codebolt.planning", "plan_add_task",
  { planId: "plan-123", task: { name: "Implement auth", priority: "high" } }
);

// Create a roadmap phase
await codebolt.tools.executeTool(
  "codebolt.planning", "roadmap_create_phase",
  { name: "Phase 1: MVP", description: "Core features", order: 1 }
);

// Create a feature
await codebolt.tools.executeTool(
  "codebolt.planning", "roadmap_create_feature",
  { phase_id: "phase-123", title: "User Dashboard", impact: "high", difficulty: "medium" }
);
```
