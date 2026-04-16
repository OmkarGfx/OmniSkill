# Crawler

Web crawler for browser automation.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `crawler_start` | Start crawler | (none) |
| `crawler_screenshot` | Take screenshot | (none) |
| `crawler_go_to_page` | Navigate to URL | url (req) |
| `crawler_scroll` | Scroll page | direction (req): up/down/left/right |
| `crawler_click` | Click element | id (req) |

```javascript
await codebolt.tools.executeTool("codebolt.crawler", "crawler_go_to_page", {
  url: "https://example.com"
});
```
