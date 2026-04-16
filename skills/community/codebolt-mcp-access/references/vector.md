# Vector

Vector database operations.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `add_item` | Add item to vector DB | item (req) |
| `query` | Query similar items | query (req), topK |
| `get_vector` | Retrieve vector by item | item (req) |

```javascript
await codebolt.tools.executeTool("codebolt.vector", "query", {
  query: "authentication flow", topK: 5
});
```
