# DB Memory

Database memory for structured key-value storage.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `dbmemory_add` | Add knowledge entry | key (req), value (req) |
| `dbmemory_get` | Get knowledge entry | key (req) |

```javascript
await codebolt.tools.executeTool("codebolt.dbmemory", "dbmemory_add", {
  key: "project_config",
  value: { name: "My Project", version: "1.0.0" }
});
```
