# codebolt.review - Code Review Tools

## Tools

### `review_create`
Creates a new merge request review.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | Yes | review or review_merge |
| initial_task | string | Yes | Original task description |
| title | string | Yes | Review title |
| description | string | Yes | Change description |
| major_files_changed | array | Yes | Changed file paths |
| diff_patch | string | Yes | Unified diff content |
| agent_id | string | Yes | Creator agent ID |
| agent_name | string | Yes | Creator agent name |
| merge_strategy | string | No | patch or git_worktree |

### `review_get`
Gets a review by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| review_id | string | Yes | Review identifier |

### `review_list`
Lists reviews with filters.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | array | No | draft, pending_review, approved, merged, etc. |
| type | array | No | review, review_merge |
| agent_id | string | No | Filter by creator |
| sort_by | string | No | createdAt, updatedAt, status |

### `review_update`
Updates review properties.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| review_id | string | Yes | Review to update |
| title/description/status | various | No | Fields to update |

### `review_submit`
Submits a draft review for review.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| review_id | string | Yes | Review to submit |

### `review_approve`
Approves a review.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| review_id | string | Yes | Review to approve |
| agent_id | string | Yes | Approving agent ID |
| agent_name | string | Yes | Approving agent name |
| comment | string | No | Approval comment |

### `review_request_changes`
Requests changes on a review.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| review_id | string | Yes | Review ID |
| agent_id | string | Yes | Reviewer agent ID |
| agent_name | string | Yes | Reviewer agent name |
| comment | string | Yes | Required changes |

### `review_add_comment`
Adds a comment without approving/rejecting.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| review_id | string | Yes | Review ID |
| agent_id | string | Yes | Commenter agent ID |
| agent_name | string | Yes | Commenter agent name |
| comment | string | Yes | Comment text |

## Examples

```javascript
// Create review
const review = await codebolt.tools.executeTool(
  "codebolt.review", "review_create",
  {
    type: "review_merge",
    initial_task: "Implement auth",
    title: "Add JWT authentication",
    description: "Added JWT-based auth with refresh tokens",
    major_files_changed: ["src/auth/jwt.ts"],
    diff_patch: "--- a/src/auth/jwt.ts\n+++ b/src/auth/jwt.ts\n...",
    agent_id: "agent-001",
    agent_name: "CodeBot"
  }
);

// Approve review
await codebolt.tools.executeTool(
  "codebolt.review", "review_approve",
  { review_id: "rev-123", agent_id: "reviewer-001", agent_name: "ReviewBot", comment: "LGTM!" }
);

// Request changes
await codebolt.tools.executeTool(
  "codebolt.review", "review_request_changes",
  { review_id: "rev-123", agent_id: "reviewer-001", agent_name: "ReviewBot", comment: "Add error handling" }
);
```
