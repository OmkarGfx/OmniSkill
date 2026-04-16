# Context Rule Engine

Conditional memory inclusion rules.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `rule_create` | Create rule engine | name (req), rules (req) |
| `rule_get` | Get rule by ID | id (req) |
| `rule_list` | List all rules | (none) |
| `rule_update` | Update rule engine | id (req), updates (req) |
| `rule_delete` | Delete rule engine | id (req) |
| `rule_evaluate` | Evaluate rules against variables | rule_engine_id (req), variables (req) |
| `rule_get_possible_variables` | Get possible variables | (none) |

```javascript
await codebolt.tools.executeTool("codebolt.contextRuleEngine", "rule_create", {
  name: "User Filter",
  rules: [{ conditions: [{ variable: "user.role", operator: "eq", value: "admin" }], action: "include" }]
});
```
