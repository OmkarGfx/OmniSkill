# Output Parsers

Parse structured data from outputs.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `outputparsers_parse_json` | Parse JSON | jsonString (req) |
| `outputparsers_parse_xml` | Parse XML | xmlString (req) |
| `outputparsers_parse_csv` | Parse CSV | csvString (req) |
| `outputparsers_parse_text` | Parse text to lines | text (req) |
| `outputparsers_parse_errors` | Extract errors | output (req) |
| `outputparsers_parse_warnings` | Extract warnings | output (req) |

```javascript
await codebolt.tools.executeTool("codebolt.outputparsers", "outputparsers_parse_json", {
  jsonString: '{"name": "John", "age": 30}'
});
```
