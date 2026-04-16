# codebolt.fs - File System Tools

## Tools

### `read_file`
Read file contents.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| absolute_path | string | Yes | Absolute path to file |
| offset | number | No | Line number to start from (0-based) |
| limit | number | No | Max lines to read |

### `write_file`
Create or overwrite a file.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| absolute_path | string | Yes | Absolute path to file |
| content | string | Yes | Content to write |

### `edit`
Replace text in a file.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| absolute_path | string | Yes | Absolute path to file |
| old_string | string | Yes | Text to find (must be unique) |
| new_string | string | Yes | Replacement text |
| expected_occurrences | number | No | Expected match count (fails if different) |

### `ls`
List directory contents.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | Yes | Absolute path to directory |
| ignore | string[] | No | Glob patterns to ignore |
| show_hidden | boolean | No | Show hidden files (default: false) |
| detailed | boolean | No | Include file sizes |
| limit | number | No | Max entries to return |

### `read_many_files`
Read multiple files at once.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | string[] | Yes | File paths, directories, or glob patterns |
| include | string[] | No | Include patterns (e.g., ['*.ts']) |
| exclude | string[] | No | Exclude patterns |
| recursive | boolean | No | Search subdirectories (default: true) |
| max_files | number | No | Max files to read |

## Examples

```javascript
// Read file
await codebolt.tools.executeTool("codebolt.fs", "read_file", {
  absolute_path: "/path/to/file.js"
});

// Edit file
await codebolt.tools.executeTool("codebolt.fs", "edit", {
  absolute_path: "/path/to/file.js",
  old_string: "const x = 1",
  new_string: "const x = 2"
});

// List directory
await codebolt.tools.executeTool("codebolt.fs", "ls", {
  path: "/path/to/dir",
  detailed: true
});
```
