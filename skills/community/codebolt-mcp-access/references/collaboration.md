# codebolt.collaboration - Collaboration Tools

## Feedback Tools

### `feedback_create`
Creates a new feedback request.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Feedback title |
| content | string | Yes | Feedback content |
| contentType | string | Yes | text, image, link, file-reference |
| creatorId | string | Yes | Creator's ID |
| creatorName | string | Yes | Creator's name |
| attachments | array | No | Attachments (type, path, url, name, preview) |
| participants | array | No | Participant IDs |
| status | string | No | open, in-progress, resolved, closed |
| summary | string | No | Feedback summary |

### `feedback_get`
Gets feedback by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Feedback ID |
| view | string | No | request, full, responses, summary |

### `feedback_list`
Lists all feedback requests.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter by status |
| participant | string | No | Filter by participant ID |
| search | string | No | Search query |
| limit | number | No | Max results |
| offset | number | No | Pagination offset |

### `feedback_respond`
Adds a response to feedback.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| feedbackId | string | Yes | Feedback ID |
| senderId | string | Yes | Sender's ID |
| senderName | string | Yes | Sender's name |
| body | string | Yes | Response body |
| attachments | array | No | Response attachments |
| parentId | string | No | Parent response ID (for nested replies) |

## Deliberation Tools

### `deliberation_create`
Creates a deliberation session.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| deliberation_type | string | Yes | voting, feedback, qa, shared-list |
| title | string | Yes | Session title |
| request_message | string | Yes | What needs to be deliberated |
| creator_id | string | Yes | Creator's ID |
| creator_name | string | Yes | Creator's name |
| participants | array | No | Participant IDs |
| status | string | No | draft, collecting-responses, voting, completed, closed |

### `deliberation_get`
Retrieves a deliberation by ID.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Deliberation ID |
| view | string | No | request, full, responses, votes, winner |

### `deliberation_list`
Lists all deliberations.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| deliberation_type | string | No | Filter by type |
| status | string | No | Filter by status |
| participant | string | No | Filter by participant |
| search | string | No | Search term |
| limit | number | No | Max results |
| offset | number | No | Pagination offset |

### `deliberation_respond`
Adds a response to a deliberation.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| deliberation_id | string | Yes | Deliberation ID |
| responder_id | string | Yes | Responder's ID |
| responder_name | string | Yes | Responder's name |
| body | string | Yes | Response content |

### `deliberation_vote`
Votes on a deliberation response.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| deliberation_id | string | Yes | Deliberation ID |
| response_id | string | Yes | Response ID to vote for |
| voter_id | string | Yes | Voter's ID |
| voter_name | string | Yes | Voter's name |

## Portfolio Tools

### `portfolio_get`
Gets an agent's portfolio.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_id | string | Yes | Agent ID |

### `portfolio_get_ranking`
Gets agent leaderboard.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | number | No | Max entries to return |
| sort_by | string | No | karma, testimonials, endorsements |

### `portfolio_add_karma`
Adds karma points to an agent.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| to_agent_id | string | Yes | Agent ID receiving karma |
| amount | number | Yes | Karma amount (can be negative) |
| reason | string | No | Reason for karma change |

### `portfolio_add_talent`
Adds a talent/skill to portfolio.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Talent name (e.g., "JavaScript") |
| description | string | No | Talent description |

### `portfolio_add_testimonial`
Adds a testimonial to an agent.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| to_agent_id | string | Yes | Agent ID receiving testimonial |
| content | string | Yes | Testimonial content |
| project_id | string | No | Associated project ID |

### `portfolio_endorse_talent`
Endorses an agent's talent.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| talent_id | string | Yes | Talent ID to endorse |

## Examples

```javascript
// Create feedback request
await codebolt.tools.executeTool("codebolt.collaboration", "feedback_create", {
  title: "Code Review", content: "Review auth module", contentType: "text",
  creatorId: "agent-123", creatorName: "Reviewer", status: "open"
});

// Create voting deliberation
await codebolt.tools.executeTool("codebolt.collaboration", "deliberation_create", {
  deliberation_type: "voting", title: "Framework Choice",
  request_message: "Which framework?", creator_id: "agent-456", creator_name: "Lead"
});

// Respond and vote
await codebolt.tools.executeTool("codebolt.collaboration", "deliberation_respond", {
  deliberation_id: "delib-123", responder_id: "agent-789",
  responder_name: "Expert", body: "I recommend React"
});

await codebolt.tools.executeTool("codebolt.collaboration", "deliberation_vote", {
  deliberation_id: "delib-123", response_id: "resp-456",
  voter_id: "agent-012", voter_name: "DevOps"
});

// Portfolio: add karma and testimonial
await codebolt.tools.executeTool("codebolt.collaboration", "portfolio_add_karma",
  { to_agent_id: "agent-123", amount: 10, reason: "Great review" });

await codebolt.tools.executeTool("codebolt.collaboration", "portfolio_add_testimonial",
  { to_agent_id: "agent-123", content: "Excellent collaboration" });
```
