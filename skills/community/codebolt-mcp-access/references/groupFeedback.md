# Group Feedback

Collaborative feedback sessions with threaded discussions.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `feedback_create` | Create feedback session | title (req), description (req), participants |
| `feedback_get` | Get feedback by ID | feedbackId (req) |
| `feedback_list` | List feedback sessions | status, participantId |
| `feedback_respond` | Submit response | feedbackId (req), response (req) |
| `feedback_reply` | Reply to response | feedbackId (req), responseId (req), reply (req) |
| `feedback_update_status` | Update status | feedbackId (req), status (req) |
| `feedback_update_summary` | Update summary | feedbackId (req), summary (req) |

```javascript
await codebolt.tools.executeTool("codebolt.groupFeedback", "feedback_create", {
  title: "Q1 Roadmap Review",
  description: "Collecting feedback on Q1 roadmap"
});
```
