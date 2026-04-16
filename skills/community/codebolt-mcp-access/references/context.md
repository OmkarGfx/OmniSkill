# codebolt.context - Context Rule Engine Tools

Context rule engine operations for conditional rules that control memory inclusion/exclusion.

## Tools

### `context_rule_create`
Creates a new context rule engine with conditional rules.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the rule engine |
| description | string | No | Description of the rule engine |
| rules | array | Yes | Array of rule objects |
| enabled | boolean | No | Whether enabled (default: true) |

**Rule Object Structure:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Rule name |
| conditions | array | Yes | Array of condition objects |
| condition_logic | string | No | 'and' or 'or' |
| action | string | Yes | 'include', 'exclude', 'force_include', 'set_priority' |
| action_config | object | No | Config for action (e.g., priority value) |
| enabled | boolean | No | Whether rule is enabled |
| order | number | No | Execution order |

**Condition Object:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| variable | string | Yes | Variable name to evaluate |
| operator | string | Yes | 'equals', 'not_equals', 'less_than', 'greater_than', 'contains' |
| value | any | Yes | Value to compare against |

### `context_rule_list`
Lists all context rule engines.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *(none)* | - | - | No parameters required |

### `context_rule_get`
Gets a rule engine by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier of the rule engine |

### `context_rule_evaluate`
Evaluates context rules against provided variables.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| scope_variables | object | Yes | Variables to evaluate rules against |
| additional_variables | object | No | Additional variables |
| input | string | No | Optional input string for context |
| rule_engine_ids | string[] | No | Specific engine IDs to evaluate |

### `context_rule_delete`
Deletes a rule engine.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | ID of the rule engine to delete |

## Examples

```javascript
// Create a rule engine
await codebolt.tools.executeTool("codebolt.context", "context_rule_create", {
  name: "User Session Rules",
  enabled: true,
  rules: [
    {
      name: "Include Admin Memories",
      conditions: [
        { variable: "user_role", operator: "equals", value: "admin" }
      ],
      condition_logic: "and",
      action: "force_include",
      order: 1
    },
    {
      name: "Prioritize Recent Content",
      conditions: [
        { variable: "content_age_hours", operator: "less_than", value: 24 }
      ],
      action: "set_priority",
      action_config: { priority: 10 },
      order: 2
    }
  ]
});

// List all rule engines
await codebolt.tools.executeTool("codebolt.context", "context_rule_list", {});

// Evaluate rules
await codebolt.tools.executeTool("codebolt.context", "context_rule_evaluate", {
  scope_variables: {
    user_role: "admin",
    content_status: "active",
    content_age_hours: 12
  },
  input: "Searching for recent admin content"
});

// Delete a rule engine
await codebolt.tools.executeTool("codebolt.context", "context_rule_delete", {
  id: "rule-engine-123"
});
```

## Notes

- Rules evaluated in order, combined with AND/OR logic
- Actions: include, exclude, force_include, set_priority
- Evaluation returns matched_rules, included/excluded/forced memories
