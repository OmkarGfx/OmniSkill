# codebolt.git - Git Tools

## Tools

### `git_init`
Initialize repository.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | Yes | Path to initialize |

### `git_add`
Stage all changes. No parameters.

### `git_commit`
Commit staged changes.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | Commit message |

### `git_push`
Push to remote. No parameters.

### `git_pull`
Pull from remote. No parameters.

### `git_checkout`
Switch branches.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| branch | string | Yes | Branch name |

### `git_branch`
Create new branch.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| branch | string | Yes | New branch name |

### `git_logs`
View commit history.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | Yes | Repository path |

### `git_diff`
View commit diff.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| commit_hash | string | Yes | Commit hash |

### `git_status`
Check repository status. No parameters.

### `git_clone`
Clone repository.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | Repository URL |
| path | string | No | Clone destination |

## Examples

```javascript
// Clone and checkout
await codebolt.tools.executeTool("codebolt.git", "git_clone", {
  url: "https://github.com/user/repo.git"
});

// Commit workflow
await codebolt.tools.executeTool("codebolt.git", "git_add", {});
await codebolt.tools.executeTool("codebolt.git", "git_commit", {
  message: "feat: add new feature"
});
await codebolt.tools.executeTool("codebolt.git", "git_push", {});

// Branch workflow
await codebolt.tools.executeTool("codebolt.git", "git_branch", {
  branch: "feature/new-feature"
});
await codebolt.tools.executeTool("codebolt.git", "git_checkout", {
  branch: "feature/new-feature"
});
```
