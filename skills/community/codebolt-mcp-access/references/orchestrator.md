# Orchestrator

Orchestrator lifecycle management.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `orchestrator_list` | List orchestrators | (none) |
| `orchestrator_get` | Get orchestrator by ID | orchestrator_id (req) |
| `orchestrator_get_settings` | Get settings | orchestrator_id (req) |
| `orchestrator_create` | Create orchestrator | name (req), description (req), agent_id (req) |
| `orchestrator_update` | Update orchestrator | orchestrator_id (req), name, description, agent_id |
| `orchestrator_update_settings` | Update settings | orchestrator_id (req), name, description |
| `orchestrator_delete` | Delete orchestrator | orchestrator_id (req) |
| `orchestrator_update_status` | Update status | orchestrator_id (req), status (req): idle/running/paused |

```javascript
await codebolt.tools.executeTool("codebolt.orchestrator", "orchestrator_create", {
  name: "Data Processor",
  description: "Handles data workflows",
  agent_id: "agent-123"
});
```
