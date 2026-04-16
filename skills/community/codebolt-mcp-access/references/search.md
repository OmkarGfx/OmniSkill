# codebolt.search - Search Tools

Tools for searching files, code patterns, and discovering available MCP tools across the codebase.

## Tools

### `glob`
Finds files matching a glob pattern.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pattern | string | Yes | Glob pattern to match files (e.g., '**/*.ts') |
| path | string | No | Directory to search in (defaults to project root) |

### `grep`
Searches for text patterns in files using grep-like functionality.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | Yes | Absolute path to search within (file or directory) |
| pattern | string | Yes | Text pattern or regex to search for |
| include | string | No | Glob pattern for files to include |
| exclude | string | No | Glob pattern for files/directories to exclude |
| case_sensitive | boolean | No | Case sensitive search (default: true) |

### `search_files`
Searches for content in files using regex patterns.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | Yes | Absolute path to directory to search |
| regex | string | Yes | Regex pattern to search for |
| file_pattern | string | No | Glob pattern to filter files |

### `codebase_search`
Performs semantic search across the codebase using natural language.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language description of what you're looking for |
| target_directories | array | No | Array of directory paths to limit search scope |

### `search_mcp_tool`
Searches for available MCP tools for a specific task.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Description of what you need a tool for |
| tags | array | No | Tags to filter results (e.g., ['database', 'api']) |

### `list_code_definition_names`
Lists code definitions (functions, classes, interfaces) in a file or directory.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | Yes | Absolute path to file or directory to analyze |

## Examples

```javascript
// Find TypeScript files
const files = await codebolt.tools.executeTool(
  "codebolt.search", "glob",
  { pattern: "**/*.ts", path: "/project/src" }
);

// Search for text patterns with grep
const grepResult = await codebolt.tools.executeTool(
  "codebolt.search", "grep",
  {
    path: "/project/src",
    pattern: "function\\s+handleAuth",
    include: "*.ts",
    case_sensitive: false
  }
);

// Regex search in files
const searchResult = await codebolt.tools.executeTool(
  "codebolt.search", "search_files",
  { path: "/project/src", regex: "TODO|FIXME", file_pattern: "*.ts" }
);

// Semantic codebase search
const semanticResult = await codebolt.tools.executeTool(
  "codebolt.search", "codebase_search",
  { query: "function that handles user authentication" }
);

// Find MCP tools
const mcpTools = await codebolt.tools.executeTool(
  "codebolt.search", "search_mcp_tool",
  { query: "database query", tags: ["database"] }
);

// List code definitions
const definitions = await codebolt.tools.executeTool(
  "codebolt.search", "list_code_definition_names",
  { path: "/project/src/utils/helpers.ts" }
);
```
