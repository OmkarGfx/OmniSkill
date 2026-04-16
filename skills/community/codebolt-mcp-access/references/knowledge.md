# codebolt.knowledge - Knowledge Graph Tools

Tools for managing knowledge graph templates, instances, records (nodes), and edges (relationships).

## Tools

### `kg_template_create`
Creates a new knowledge graph template with record kinds and edge types.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Template name |
| description | string | No | Template description |
| record_kinds | array | Yes | Array of node types (name, label, attributes) |
| edge_types | array | Yes | Array of relationship types (name, label, from_kinds, to_kinds) |

### `kg_template_list`
Lists all knowledge graph templates.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)* | - | - | No parameters required |

### `kg_template_get`
Gets a template by its ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | Yes | ID of the template |

### `kg_template_delete`
Deletes a template permanently.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | Yes | ID of the template |

### `kg_instance_create`
Creates a new knowledge graph instance based on a template.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | Yes | ID of the template to use |
| name | string | Yes | Instance name |
| description | string | No | Instance description |

### `kg_instance_list`
Lists knowledge graph instances.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| template_id | string | No | Filter by template ID |

### `kg_instance_get` / `kg_instance_delete`
Gets or deletes an instance.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | ID of the instance |

### `kg_record_add`
Adds a record (node) to an instance.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | ID of the instance |
| kind | string | Yes | Record kind (must match template) |
| attributes | object | Yes | Record data as JSON object |
| valid_from | string | No | Start of validity (ISO date) |
| valid_to | string | No | End of validity (ISO date) |

### `kg_record_list`
Lists records in an instance.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | ID of the instance |
| kind | string | No | Filter by record kind |
| limit | number | No | Max records to return |
| offset | number | No | Records to skip |

### `kg_edge_add`
Adds an edge (relationship) between two records.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | ID of the instance |
| kind | string | Yes | Edge kind (must match template) |
| from_node_id | string | Yes | Source node ID |
| to_node_id | string | Yes | Target node ID |
| attributes | object | No | Edge attributes |

### `kg_edge_list`
Lists edges in an instance.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | Yes | ID of the instance |
| kind | string | No | Filter by edge kind |
| from_node_id | string | No | Filter by source node |
| to_node_id | string | No | Filter by target node |

## Examples

```javascript
// Create a template
await codebolt.tools.executeTool("codebolt.knowledge", "kg_template_create", {
  name: "Project Dependencies",
  record_kinds: [
    { name: "project", label: "Project", attributes: { name: { type: "string" } } },
    { name: "library", label: "Library", attributes: { name: { type: "string" } } }
  ],
  edge_types: [
    { name: "depends_on", label: "Depends On", from_kinds: ["project"], to_kinds: ["library"] }
  ]
});

// Create an instance
await codebolt.tools.executeTool("codebolt.knowledge", "kg_instance_create", {
  template_id: "template-123",
  name: "My Project Graph"
});

// Add records
await codebolt.tools.executeTool("codebolt.knowledge", "kg_record_add", {
  instance_id: "instance-456",
  kind: "project",
  attributes: { name: "my-app", version: "1.0.0" }
});

// Add an edge
await codebolt.tools.executeTool("codebolt.knowledge", "kg_edge_add", {
  instance_id: "instance-456",
  kind: "depends_on",
  from_node_id: "project-123",
  to_node_id: "library-456"
});
```

## Notes

- Templates define schema (what record/edge types are allowed)
- Instances store actual graph data
- Records can have validity periods for temporal data
