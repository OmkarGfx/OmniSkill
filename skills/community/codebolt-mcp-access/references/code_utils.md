# Code Utils

Code analysis and AST utilities.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_files_markdown` | Get files as markdown | (none) |
| `get_js_tree` | Get JS/TS AST tree | filePath (req) |
| `perform_match` | Pattern matching | matcherDefinition (req), pattern (req), problems (req) |
| `get_matcher_list` | Get available matchers | (none) |
| `get_match_detail` | Get matcher details | matcherId (req) |

```javascript
await codebolt.tools.executeTool("codebolt.code_utils", "get_js_tree", {
  filePath: "./src/app.ts"
});
```
