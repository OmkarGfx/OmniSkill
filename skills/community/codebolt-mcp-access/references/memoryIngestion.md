# Memory Ingestion

Memory ingestion pipelines for automated data processing.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `memoryIngestion_create` | Create ingestion pipeline | pipelineId (req), label (req), source (req), processors (req) |
| `memoryIngestion_execute` | Execute pipeline | pipelineId (req), inputData |

```javascript
await codebolt.tools.executeTool("codebolt.memoryIngestion", "memoryIngestion_create", {
  pipelineId: "customer-data-pipeline",
  label: "Customer Data Ingestion",
  source: { type: "file", path: "/data/customers.csv" },
  processors: [{ type: "cleaner", rules: ["removeNulls"] }]
});
```
