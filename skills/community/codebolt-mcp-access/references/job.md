# codebolt.job - Job Management Tools

## Tools

### `job_create`
Creates a new job in a job group.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| group_id | string | Yes | Job group ID |
| name | string | Yes | Job title |
| type | string | Yes | bug, feature, task, epic, chore |
| priority | number | Yes | 1-4 (4 = urgent) |
| description | string | No | Job description |
| status | string | No | open, working, hold, closed |
| assignees | array | No | List of assignees |
| labels | array | No | List of labels |
| due_date | string | No | Due date |

### `job_get`
Retrieves a job by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | Job ID (e.g., "BE-5") |

### `job_update`
Updates an existing job.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | Job ID to update |
| name/type/priority/status/etc | various | No | Fields to update |

### `job_delete`
Permanently deletes a job.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | Job ID to delete |

### `job_list`
Lists jobs with optional filters.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | array | No | Filter by status |
| priority | array | No | Filter by priority |
| type | array | No | Filter by type |
| sort_by | string | No | priority, createdAt, updatedAt |

### `job_group_create`
Creates a new job group.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | No | Group display name |
| short_name | string | No | 3-4 letter prefix (e.g., "BE") |

### `job_add_dependency`
Adds dependency between jobs.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | Dependent job ID |
| depends_on_job_id | string | Yes | Blocking job ID |
| type | string | No | blocks, related, parent-child |

### `job_get_ready`
Gets jobs ready to work on (no blockers).
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status/priority/type | various | No | Optional filters |

### `job_get_blocked`
Gets jobs blocked by dependencies.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status/priority/type | various | No | Optional filters |

### `job_lock`
Acquires lock on a job for an agent.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | Job ID to lock |
| agent_id | string | Yes | Agent acquiring lock |

### `job_unlock`
Releases lock on a job.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | Job ID to unlock |
| agent_id | string | Yes | Agent releasing lock |

### `job_bid_add`
Adds a bid to work on a job.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | Job ID to bid on |
| agent_id | string | Yes | Bidding agent ID |
| reason | string | Yes | Bid justification |
| priority | number | Yes | Bid priority |

## Examples

```javascript
// Create job
const job = await codebolt.tools.executeTool(
  "codebolt.job", "job_create",
  { group_id: "grp-1", name: "Add auth", type: "feature", priority: 3 }
);

// List ready jobs
const ready = await codebolt.tools.executeTool(
  "codebolt.job", "job_get_ready",
  { status: ["open"], priority: [3, 4] }
);

// Lock and work
await codebolt.tools.executeTool(
  "codebolt.job", "job_lock",
  { job_id: "BE-1", agent_id: "agent-001" }
);
```
