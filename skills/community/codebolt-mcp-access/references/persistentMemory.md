# Persistent Memory

Long-term memory storage with retrieval pipelines.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `persistent_memory_create` | Create memory config | config (req): {label, retrieval, contribution} |
| `persistent_memory_get` | Get memory by ID | memoryId (req) |
| `persistent_memory_list` | List memories | filters: {inputScope, activeOnly} |
| `persistent_memory_update` | Update memory | memoryId (req), updates (req) |
| `persistent_memory_delete` | Delete memory | memoryId (req) |
| `persistent_memory_execute_retrieval` | Execute retrieval | memoryId (req), intent (req): {query, keywords} |
| `persistent_memory_validate` | Validate config | memory (req) |
| `persistent_memory_get_step_specs` | Get step specs | (none) |

```javascript
await codebolt.tools.executeTool("codebolt.persistentMemory", "persistent_memory_create", {
  config: {
    label: "Project Docs",
    retrieval: { source_type: "vectordb", source_id: "docs-db" },
    contribution: { format: "markdown" }
  }
});
```
