# codebolt.browser - Browser Automation Tools

## Tools

### `browser_navigate`
Navigate to URL.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | URL to navigate to |
| instance_id | string | No | Browser instance ID |

### `browser_click`
Click element.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| element_id | string | Yes | Element ID to click |
| instance_id | string | No | Browser instance ID |

### `browser_type`
Type text into element.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| element_id | string | Yes | Element ID |
| text | string | Yes | Text to type |
| instance_id | string | No | Browser instance ID |

### `browser_screenshot`
Capture screenshot.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| instance_id | string | No | Browser instance ID |
| full_page | boolean | No | Full page screenshot |
| quality | number | No | JPEG quality (0-100) |
| format | string | No | 'png' or 'jpeg' |

### `browser_get_content`
Get page text content. Optional: instance_id

### `browser_scroll`
Scroll page.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| direction | string | Yes | 'up', 'down', 'left', 'right' |
| pixels | string | Yes | Pixels to scroll |
| instance_id | string | No | Browser instance ID |

### `browser_get_url`
Get current URL. Optional: instance_id

### `browser_get_html`
Get page HTML. Optional: instance_id

### `browser_get_markdown`
Get page as Markdown. Optional: instance_id

### `browser_search`
Search in element.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| element_id | string | Yes | Element ID |
| query | string | Yes | Search query |
| instance_id | string | No | Browser instance ID |

### `browser_enter`
Press Enter key. Optional: instance_id

### `browser_close`
Close browser. Optional: instance_id

## Examples

```javascript
// Navigate and interact
await codebolt.tools.executeTool("codebolt.browser", "browser_navigate", {
  url: "https://example.com"
});

await codebolt.tools.executeTool("codebolt.browser", "browser_type", {
  element_id: "search-input",
  text: "search query"
});

await codebolt.tools.executeTool("codebolt.browser", "browser_click", {
  element_id: "submit-btn"
});

// Get content
const content = await codebolt.tools.executeTool("codebolt.browser", "browser_get_markdown", {});
```
