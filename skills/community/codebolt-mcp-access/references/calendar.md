# codebolt.calendar - Calendar Event Tools

## Tools

### `calendar_create_event`
Creates a new calendar event.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Event title |
| startTime | string | Yes | ISO 8601 start time |
| eventType | string | No | generic, meeting, reminder, deadline, check, milestone |
| endTime | string | No | ISO 8601 end time |
| description | string | No | Event description |
| participants | array | No | List of participants |
| isRecurring | boolean | No | Whether event recurs |
| cronExpression | string | No | Cron for recurring events |
| reminder | object | No | { enabled, minutesBefore } |
| checkType | string | No | email, website, api, file |

### `calendar_update_event`
Updates an existing event.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| eventId | string | Yes | Event to update |
| title/startTime/etc | various | No | Fields to update |

### `calendar_delete_event`
Permanently deletes an event.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| eventId | string | Yes | Event to delete |

### `calendar_get_event`
Gets event details by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| eventId | string | Yes | Event to retrieve |

### `calendar_list_events`
Lists events with filters.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| startDate | string | No | Filter start (ISO 8601) |
| endDate | string | No | Filter end (ISO 8601) |
| eventTypes | array | No | Filter by types |
| tags | array | No | Filter by tags |
| completed | boolean | No | Filter by completion |

### `calendar_get_upcoming`
Gets upcoming events within time window.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| withinMinutes | number | No | Minutes ahead (default: 60) |

### `calendar_mark_complete`
Marks an event as complete.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| eventId | string | Yes | Event to complete |

### `calendar_get_status`
Gets calendar scheduler status.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| *None* | - | - | No parameters required |

## Examples

```javascript
// Create meeting
const meeting = await codebolt.tools.executeTool(
  "codebolt.calendar", "calendar_create_event",
  {
    title: "Sprint Planning",
    startTime: "2024-12-15T10:00:00Z",
    endTime: "2024-12-15T11:00:00Z",
    eventType: "meeting",
    participants: [{ id: "user-1", name: "John", type: "user", status: "pending" }],
    reminder: { enabled: true, minutesBefore: 15 }
  }
);

// Create recurring reminder
const reminder = await codebolt.tools.executeTool(
  "codebolt.calendar", "calendar_create_event",
  {
    title: "Daily Standup",
    startTime: "2024-12-01T09:00:00Z",
    eventType: "reminder",
    isRecurring: true,
    cronExpression: "0 9 * * 1-5"
  }
);

// Get upcoming events
const upcoming = await codebolt.tools.executeTool(
  "codebolt.calendar", "calendar_get_upcoming",
  { withinMinutes: 120 }
);

// List events
const events = await codebolt.tools.executeTool(
  "codebolt.calendar", "calendar_list_events",
  { eventTypes: ["meeting", "deadline"], includeCompleted: false }
);
```
