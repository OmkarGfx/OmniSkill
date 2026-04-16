# Project Structure

Manage project metadata, packages, routes, dependencies, and configurations.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `project_structure_get_metadata` | Get project metadata | workspacePath |
| `project_structure_update_metadata` | Update metadata | updates (req), workspacePath |
| `project_structure_get_packages` | Get all packages | workspacePath |
| `project_structure_get_package` | Get package by ID | packageId (req), workspacePath |
| `project_structure_create_package` | Create new package | name (req), path (req), type, description |
| `project_structure_update_package` | Update package | packageId (req), name, description, type |
| `project_structure_delete_package` | Delete package | packageId (req), workspacePath |
| `project_structure_add_route` | Add API route | packageId (req), path (req), method (req) |
| `project_structure_update_route` | Update route | packageId (req), routeId (req), path, method |
| `project_structure_delete_route` | Delete route | packageId (req), routeId (req), workspacePath |
| `project_structure_add_table` | Add database table | packageId (req), name (req), columns (req) |
| `project_structure_update_table` | Update table | packageId (req), tableId (req), name, columns |
| `project_structure_delete_table` | Delete table | packageId (req), tableId (req), workspacePath |
| `project_structure_add_dependency` | Add dependency | packageId (req), name (req), version (req), type (req) |
| `project_structure_update_dependency` | Update dependency | packageId (req), dependencyId (req), name, version |
| `project_structure_delete_dependency` | Delete dependency | packageId (req), dependencyId (req), workspacePath |
| `project_structure_add_command` | Add run command | packageId (req), name (req), command (req) |
| `project_structure_update_command` | Update command | packageId (req), commandId (req), name, command |
| `project_structure_delete_command` | Delete command | packageId (req), commandId (req), workspacePath |
| `project_structure_add_ui_route` | Add UI route | packageId (req), path (req), component |
| `project_structure_update_ui_route` | Update UI route | packageId (req), routeId (req), path, component |
| `project_structure_delete_ui_route` | Delete UI route | packageId (req), routeId (req), workspacePath |
| `project_structure_add_deployment` | Add deployment | packageId (req), name (req), type (req) |
| `project_structure_update_deployment` | Update deployment | packageId (req), configId (req), name, type |
| `project_structure_delete_deployment` | Delete deployment | packageId (req), configId (req), workspacePath |
| `project_structure_update_git` | Update git info | repository, branch, remote, mainBranch |
| `project_structure_update_design_guidelines` | Update design guidelines | packageId (req), colors, fonts, spacing |
| `project_structure_update_frontend_framework` | Update frontend framework | packageId (req), name (req), version |
| `project_structure_update_section` | Update package section | packageId (req), section (req), sectionData (req) |

```javascript
await codebolt.tools.executeTool("codebolt.projectStructure", "project_structure_create_package", {
  name: "api-service",
  path: "./packages/api",
  type: "backend"
});
```
