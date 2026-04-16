# Review Merge Request

Review merge request workflow.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `reviewMergeRequest_create` | Create merge request | title (req), description (req), sourceBranch (req), targetBranch (req), authorId (req) |
| `reviewMergeRequest_list` | List requests | status, authorId, swarmId, limit |
| `reviewMergeRequest_merge` | Merge request | id (req), mergedBy (req) |

```javascript
await codebolt.tools.executeTool("codebolt.reviewMergeRequest", "reviewMergeRequest_create", {
  title: "Add authentication",
  sourceBranch: "feature/auth",
  targetBranch: "main",
  authorId: "user-123"
});
```
