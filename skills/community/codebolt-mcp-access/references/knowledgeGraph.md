# Knowledge Graph

Knowledge graph management with instances, records, edges, and views.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `kg_create_instance_template` | Create instance template | config (req): {name, record_kinds, edge_types} |
| `kg_get_instance_template` | Get template by ID | templateId (req) |
| `kg_list_instance_templates` | List all templates | (none) |
| `kg_update_instance_template` | Update template | templateId (req), updates (req) |
| `kg_delete_instance_template` | Delete template | templateId (req) |
| `kg_create_instance` | Create instance from template | config (req): {templateId, name} |
| `kg_get_instance` | Get instance by ID | instanceId (req) |
| `kg_list_instances` | List instances | templateId |
| `kg_delete_instance` | Delete instance | instanceId (req) |
| `kg_add_memory_record` | Add memory record | instanceId (req), record (req): {kind, attributes} |
| `kg_add_memory_records` | Add multiple records | instanceId (req), records (req) |
| `kg_get_memory_record` | Get record by ID | instanceId (req), recordId (req) |
| `kg_list_memory_records` | List records | instanceId (req), filters |
| `kg_update_memory_record` | Update record | instanceId (req), recordId (req), updates (req) |
| `kg_delete_memory_record` | Delete record | instanceId (req), recordId (req) |
| `kg_add_edge` | Add edge | instanceId (req), edge (req): {kind, from_node_id, to_node_id} |
| `kg_add_edges` | Add multiple edges | instanceId (req), edges (req) |
| `kg_list_edges` | List edges | instanceId (req), filters |
| `kg_delete_edge` | Delete edge | instanceId (req), edgeId (req) |
| `kg_create_view_template` | Create view template | config (req): {name, applicable_template_ids, patterns} |
| `kg_get_view_template` | Get view template | templateId (req) |
| `kg_list_view_templates` | List view templates | applicableTemplateId |
| `kg_update_view_template` | Update view template | templateId (req), updates (req) |
| `kg_delete_view_template` | Delete view template | templateId (req) |
| `kg_create_view` | Create view | config (req): {name, instanceId, templateId} |
| `kg_list_views` | List views | instanceId (req) |
| `kg_execute_view` | Execute view query | viewId (req) |
| `kg_delete_view` | Delete view | viewId (req) |

```javascript
await codebolt.tools.executeTool("codebolt.knowledgeGraph", "kg_create_instance", {
  config: { templateId: "template-123", name: "My Graph" }
});
```
