# codebolt.capability - Capability Management Tools

Tools for managing and executing capabilities including skills, powers, and talents.

## Tools

### `capability_list`
Lists all available capabilities with optional filtering.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | No | Filter by type: 'skill', 'power', 'talent' |
| tags | array | No | Filter by tags |
| author | string | No | Filter by author name |

### `capability_list_skills`
Lists all available skills with optional filtering.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tags | array | No | Filter by tags |
| author | string | No | Filter by author name |

### `capability_list_powers`
Lists all available powers with optional filtering.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tags | array | No | Filter by tags |
| author | string | No | Filter by author name |

### `capability_get_detail`
Gets detailed information about a specific capability.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| capabilityId | string | Yes | Name/identifier of the capability |
| capabilityType | string | No | Type: 'skill', 'power', 'talent' |

### `capability_start`
Starts a capability execution.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| capabilityId | string | Yes | Name/identifier of the capability |
| capabilityType | string | Yes | Type: 'skill', 'power', 'talent' |
| params | object | No | Parameters to pass to the capability |
| timeout | number | No | Execution timeout in milliseconds |

### `capability_start_skill`
Starts a skill execution (convenience method).
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skillId | string | Yes | Name/identifier of the skill |
| params | object | No | Parameters to pass to the skill |
| timeout | number | No | Execution timeout in milliseconds |

### `capability_stop`
Stops a running capability execution.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| capabilityId | string | Yes | Execution ID to stop |

### `capability_get_status`
Gets the current status of a capability execution.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| executionId | string | Yes | Execution ID to check |

## Examples

```javascript
// List all capabilities
await codebolt.tools.executeTool("codebolt.capability", "capability_list", {});

// List skills filtered by tags
await codebolt.tools.executeTool("codebolt.capability", "capability_list_skills", {
  tags: ["code-generation", "testing"]
});

// Get capability details
await codebolt.tools.executeTool("codebolt.capability", "capability_get_detail", {
  capabilityId: "code-analyzer",
  capabilityType: "skill"
});

// Start a capability
const execution = await codebolt.tools.executeTool("codebolt.capability", "capability_start", {
  capabilityId: "code-analyzer",
  capabilityType: "skill",
  params: { filePath: "/src/index.ts", analysisType: "deep" },
  timeout: 30000
});

// Start a skill (convenience)
await codebolt.tools.executeTool("codebolt.capability", "capability_start_skill", {
  skillId: "test-runner",
  params: { testSuite: "unit" }
});

// Check execution status
await codebolt.tools.executeTool("codebolt.capability", "capability_get_status", {
  executionId: "exec-12345"
});

// Stop a running capability
await codebolt.tools.executeTool("codebolt.capability", "capability_stop", {
  capabilityId: "exec-12345"
});
```

## Notes

- **Skills**: Executable tasks
- **Powers**: Enhanced functionality
- **Talents**: Agent-specific abilities
- Starting a capability returns an execution ID for tracking or stopping
