# codebolt.testing - Test Management Tools

## Test Suite Tools

### `test_suite_create`
Creates a new test suite.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the test suite |
| description | string | No | Suite description |
| test_case_ids | array | No | Test case IDs to include |

### `test_suite_get`
Retrieves a test suite by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| suite_id | string | Yes | Suite ID to retrieve |

### `test_suite_list`
Lists all test suites.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filters | object | No | Optional filters (reserved) |

### `test_suite_update`
Updates an existing test suite.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| suite_id | string | Yes | Suite ID to update |
| name | string | No | New name |
| description | string | No | New description |
| test_case_ids | array | No | New test case IDs |

### `test_suite_delete`
Permanently deletes a test suite.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| suite_id | string | Yes | Suite ID to delete |

## Test Case Tools

### `test_case_create`
Creates a new test case.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | string | Yes | Unique key (e.g., "TC-001") |
| name | string | Yes | Test case name |
| description | string | No | What the test validates |
| steps | array | Yes | Array of steps with content and order |
| labels | array | No | Labels for categorization |
| priority | string | No | low, medium, high, automated |
| type | string | No | Test type (functional, regression) |

### `test_case_get`
Retrieves a test case by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| case_id | string | Yes | Case ID to retrieve |

### `test_case_list`
Lists all test cases.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| suite_id | string | No | Filter by suite ID |
| filters | object | No | Optional filters (reserved) |

### `test_case_update`
Updates an existing test case.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| case_id | string | Yes | Case ID to update |
| key | string | No | New key |
| name | string | No | New name |
| description | string | No | New description |
| steps | array | No | New steps |
| labels | array | No | New labels |
| priority | string | No | New priority |
| type | string | No | New type |

## Test Run Tools

### `test_run_create`
Creates a new test run for a suite.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| test_suite_id | string | Yes | Suite ID to run |
| name | string | No | Run name (e.g., "Sprint 1 Regression") |

### `test_run_get`
Retrieves a test run by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| run_id | string | Yes | Run ID to retrieve |

### `test_run_update_status`
Updates test run status.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| run_id | string | Yes | Run ID to update |
| status | string | Yes | pending, running, completed, cancelled |

## Examples

```javascript
// Create a test suite
const suite = await codebolt.tools.executeTool(
  "codebolt.testing", "test_suite_create",
  { name: "Authentication Tests", description: "Tests for auth flows" }
);

// Create a test case with steps
const testCase = await codebolt.tools.executeTool(
  "codebolt.testing", "test_case_create",
  {
    key: "TC-001",
    name: "User Login Test",
    steps: [
      { content: "Navigate to login page", order: 1 },
      { content: "Enter valid credentials", order: 2 },
      { content: "Click login button", order: 3 },
      { content: "Verify dashboard displayed", order: 4 }
    ],
    priority: "high",
    labels: ["authentication", "smoke"]
  }
);

// Create and run a test run
const run = await codebolt.tools.executeTool(
  "codebolt.testing", "test_run_create",
  { test_suite_id: "suite-123", name: "Sprint 1 Regression" }
);

// Update run status to completed
await codebolt.tools.executeTool(
  "codebolt.testing", "test_run_update_status",
  { run_id: "run-456", status: "completed" }
);

// List all test suites
const suites = await codebolt.tools.executeTool(
  "codebolt.testing", "test_suite_list", {}
);
```
