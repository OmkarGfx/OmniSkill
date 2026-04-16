# Problem

Error and issue detection through pattern matching.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `problem_matcher_analyze` | Analyze content for problems | content (req), language (req), filePath (req), expectedSeverity |
| `problem_matcher_get_patterns` | Get patterns for a language | language (req) |
| `problem_matcher_add_pattern` | Add custom pattern | name (req), language (req), pattern (req) |
| `problem_matcher_remove_pattern` | Remove custom pattern | name (req), language (req) |
| `problem_matcher_list_problems` | List problems in files | filePath, severity, language, limit |

```javascript
await codebolt.tools.executeTool("codebolt.problem", "problem_matcher_analyze", {
  content: 'Error: Cannot find module',
  language: 'javascript', filePath: './src/app.js'
});
```
