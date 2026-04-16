# Requirement Plan

Structured requirement documents with sections.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `requirement_plan_create` | Create requirement plan | fileName (req) |
| `requirement_plan_get` | Get plan by path | filePath (req) |
| `requirement_plan_update` | Update plan | filePath (req), content (req) |
| `requirement_plan_list` | List all plans | (none) |
| `requirement_plan_add_section` | Add section | filePath (req), section (req): {type, title, content/linkedFile} |
| `requirement_plan_update_section` | Update section | filePath (req), sectionId (req), updates (req) |
| `requirement_plan_remove_section` | Remove section | filePath (req), sectionId (req) |
| `requirement_plan_reorder_sections` | Reorder sections | filePath (req), sectionIds (req) |
| `requirement_plan_review` | Request review | filePath (req) |

```javascript
await codebolt.tools.executeTool("codebolt.requirementPlan", "requirement_plan_create", {
  fileName: "api-requirements"
});
```
