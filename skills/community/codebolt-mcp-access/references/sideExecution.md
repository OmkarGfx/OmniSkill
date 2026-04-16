# Side Execution

Isolated code execution in child processes.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `side_execution_start_action_block` | Start ActionBlock execution | action_block_path (req), params, timeout |
| `side_execution_start_code` | Start inline code execution | inline_code (req), params, timeout |
| `side_execution_stop` | Stop execution | side_execution_id (req) |
| `side_execution_list_action_blocks` | List ActionBlocks | project_path |
| `side_execution_get_status` | Get execution status | side_execution_id (req) |

```javascript
await codebolt.tools.executeTool("codebolt.sideExecution", "side_execution_start_code", {
  inline_code: "console.log('Hello');"
});
```
