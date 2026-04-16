# codebolt.terminal - Terminal Tools

## Tools

### `execute_command`
Execute CLI command.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| command | string | Yes | CLI command to execute |
| explanation | string | No | Why this command is being used |

## Examples

```javascript
// Run command
await codebolt.tools.executeTool("codebolt.terminal", "execute_command", {
  command: "npm install",
  explanation: "Installing project dependencies"
});

// Run build
await codebolt.tools.executeTool("codebolt.terminal", "execute_command", {
  command: "npm run build"
});

// Run tests
await codebolt.tools.executeTool("codebolt.terminal", "execute_command", {
  command: "npm test -- --coverage"
});
```

## Notes
- Use `--yes` flag for interactive commands
- Prefer CLI commands over scripts for flexibility
- Ensure commands are safe and non-destructive
