# mcp2web Full Reference

This document provides a complete working mcp2web server implementation for reference. It demonstrates all protocol features: resources, tools, navigation, forms, and HTML page rendering.

## Complete Working Server: Task Manager

A full task manager application with multiple pages, form submission, and navigation.

### Project Structure

```
task-manager/
├── package.json
├── tsconfig.json
└── src/
    ├── pages.ts
    └── server.ts
```

### package.json

```json
{
  "name": "task-manager-mcp2web",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.1",
    "zod": "^3.24.4"
  },
  "devDependencies": {
    "typescript": "^5.8.3"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

### src/pages.ts

```typescript
// HTML-escape user input to prevent XSS
function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// Shared CSS styles used across all pages
const sharedStyles = `
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #1a1a2e;
    color: #e0e0e0;
    line-height: 1.6;
    padding: 20px;
  }
  .container { max-width: 700px; margin: 0 auto; }
  h1 { color: #16c79a; margin-bottom: 16px; font-size: 1.8em; }
  h2 { color: #16c79a; margin-bottom: 12px; font-size: 1.3em; }
  a { color: #16c79a; text-decoration: none; }
  a:hover { text-decoration: underline; }
  nav { margin-bottom: 24px; display: flex; gap: 16px; }
  nav a {
    padding: 8px 16px;
    background: #0f3460;
    border-radius: 6px;
    transition: background 0.2s;
  }
  nav a:hover { background: #16c79a; color: #1a1a2e; text-decoration: none; }
  .card {
    background: #16213e;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    border: 1px solid #0f3460;
  }
  .btn {
    background: #16c79a;
    color: #1a1a2e;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1em;
    font-weight: 600;
  }
  .btn:hover { background: #13b48a; }
  input, textarea, select {
    width: 100%;
    padding: 10px;
    margin-bottom: 12px;
    background: #1a1a2e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    color: #e0e0e0;
    font-size: 1em;
  }
  textarea { min-height: 80px; resize: vertical; }
  label { display: block; margin-bottom: 4px; color: #a0a0b0; font-size: 0.9em; }
  .status-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: 600;
  }
  .status-pending { background: #e2b93d; color: #1a1a2e; }
  .status-done { background: #16c79a; color: #1a1a2e; }
`;

// Navigation bar shared across pages
function nav(): string {
  return `
    <nav>
      <a href="mcp2web://task-manager/home">Home</a>
      <a href="mcp2web://task-manager/tasks">Tasks</a>
      <a href="mcp2web://task-manager/add-task">Add Task</a>
      <a href="mcp2web://task-manager/about">About</a>
    </nav>
  `;
}

// Wraps content in a full HTML document
function page(title: string, body: string): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>${sharedStyles}</style>
</head>
<body>
  <div class="container">
    ${nav()}
    ${body}
  </div>
</body>
</html>`;
}

// --- Page Functions ---

export function homePage(): string {
  return page("Task Manager", `
    <h1>Task Manager</h1>
    <div class="card">
      <p>Welcome to the Task Manager. Use the navigation above to view, add, and manage your tasks.</p>
    </div>
    <div class="card">
      <h2>Quick Actions</h2>
      <p><a href="mcp2web://task-manager/add-task">Create a new task</a></p>
      <p><a href="mcp2web://task-manager/tasks">View all tasks</a></p>
    </div>
  `);
}

interface Task {
  id: string;
  title: string;
  description: string;
  status: "pending" | "done";
}

export function tasksPage(tasks: Task[]): string {
  const taskCards = tasks.length === 0
    ? '<div class="card"><p>No tasks yet. <a href="mcp2web://task-manager/add-task">Add one!</a></p></div>'
    : tasks.map(t => `
        <div class="card">
          <h2>${escapeHtml(t.title)}</h2>
          <p>${escapeHtml(t.description)}</p>
          <p><span class="status-badge status-${t.status}">${t.status}</span></p>
          ${t.status === "pending" ? `
            <form action="mcp2web-tool://complete-task" method="POST" style="margin-top: 8px;">
              <input type="hidden" name="taskId" value="${t.id}">
              <button type="submit" class="btn">Mark Done</button>
            </form>
          ` : ""}
        </div>
      `).join("");

  return page("Tasks", `
    <h1>All Tasks</h1>
    ${taskCards}
  `);
}

export function addTaskPage(): string {
  return page("Add Task", `
    <h1>Add New Task</h1>
    <div class="card">
      <form action="mcp2web-tool://add-task" method="POST">
        <label for="title">Title</label>
        <input type="text" id="title" name="title" placeholder="Enter task title" required>

        <label for="description">Description</label>
        <textarea id="description" name="description" placeholder="Describe the task"></textarea>

        <button type="submit" class="btn">Add Task</button>
      </form>
    </div>
  `);
}

export function taskAddedPage(title: string): string {
  return page("Task Added", `
    <h1>Task Added</h1>
    <div class="card">
      <p>Task "<strong>${escapeHtml(title)}</strong>" has been added successfully.</p>
      <p style="margin-top: 12px;">
        <a href="mcp2web://task-manager/tasks">View all tasks</a> |
        <a href="mcp2web://task-manager/add-task">Add another</a>
      </p>
    </div>
  `);
}

export function taskCompletedPage(title: string): string {
  return page("Task Completed", `
    <h1>Task Completed</h1>
    <div class="card">
      <p>Task "<strong>${escapeHtml(title)}</strong>" has been marked as done.</p>
      <p style="margin-top: 12px;">
        <a href="mcp2web://task-manager/tasks">Back to tasks</a>
      </p>
    </div>
  `);
}

export function aboutPage(): string {
  return page("About", `
    <h1>About</h1>
    <div class="card">
      <p>Task Manager is a demo mcp2web server showing how to build web UIs
         that run inside the mcp2web Electron browser.</p>
      <p style="margin-top: 8px;">Built with the MCP SDK and the mcp2web protocol.</p>
    </div>
  `);
}
```

### src/server.ts

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  homePage,
  tasksPage,
  addTaskPage,
  taskAddedPage,
  taskCompletedPage,
  aboutPage,
} from "./pages.js";

// In-memory task store
interface Task {
  id: string;
  title: string;
  description: string;
  status: "pending" | "done";
}

const tasks: Task[] = [];

// Create MCP server
const server = new McpServer({
  name: "task-manager",
  version: "1.0.0",
});

// --- Resources (HTML pages) ---

server.resource("home", "mcp2web://task-manager/home", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "text/html", text: homePage() }],
}));

server.resource("tasks", "mcp2web://task-manager/tasks", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "text/html", text: tasksPage(tasks) }],
}));

server.resource("add-task", "mcp2web://task-manager/add-task", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "text/html", text: addTaskPage() }],
}));

server.resource("about", "mcp2web://task-manager/about", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "text/html", text: aboutPage() }],
}));

// --- Tools (form handlers) ---

server.tool(
  "add-task",
  { title: z.string().max(200), description: z.string().max(1000) },
  async ({ title, description }) => {
    const task: Task = {
      id: crypto.randomUUID(),
      title,
      description,
      status: "pending",
    };
    tasks.push(task);
    return {
      content: [{ type: "text", text: taskAddedPage(title) }],
    };
  }
);

server.tool(
  "complete-task",
  { taskId: z.string().uuid() },
  async ({ taskId }) => {
    const task = tasks.find((t) => t.id === taskId);
    if (!task) {
      return {
        content: [{ type: "text", text: "Task not found" }],
        isError: true,
      };
    }
    task.status = "done";
    return {
      content: [{ type: "text", text: taskCompletedPage(task.title) }],
    };
  }
);

// --- Start server ---

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Key Patterns Demonstrated

### 1. Resource Registration

Each page is a separate MCP resource with a `mcp2web://` URI. The Electron browser discovers these by calling `resources/list` and renders the first one as the home page.

```typescript
server.resource("name", "mcp2web://server/path", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "text/html", text: htmlString }]
}));
```

### 2. Tool Registration for Forms

Tools handle form submissions. Input `name` attributes must match tool parameter names exactly.

```typescript
server.tool("tool-name", { param: z.string() }, async ({ param }) => ({
  content: [{ type: "text", text: responseHtml }]
}));
```

### 3. Navigation Between Pages

Use anchor tags with `mcp2web://` URIs. The Electron browser intercepts these clicks and calls `resources/read` on the target URI.

```html
<a href="mcp2web://server-name/page-name">Go to page</a>
```

### 4. Form Submission to Tools

Use forms with `mcp2web-tool://` action URIs. The browser collects form data and sends it as tool call arguments.

```html
<form action="mcp2web-tool://tool-name" method="POST">
  <input name="paramName" type="text">
  <button type="submit">Submit</button>
</form>
```

### 5. Hidden Inputs for Context

Pass identifiers or state through hidden form fields:

```html
<input type="hidden" name="taskId" value="123">
```

### 6. Tool Error Responses

Return `isError: true` for error cases:

```typescript
return {
  content: [{ type: "text", text: "Error message" }],
  isError: true,
};
```

### 7. Page Template Organization

Keep HTML generation in a separate `pages.ts` file. Use shared style strings and a wrapper function to avoid duplication:

```typescript
function page(title: string, body: string): string {
  return `<!DOCTYPE html>
<html><head><title>${title}</title><style>${sharedStyles}</style></head>
<body><div class="container">${nav()}${body}</div></body></html>`;
}
```

## URI Scheme Summary

| Scheme | Used In | Triggers |
|--------|---------|----------|
| `mcp2web://<server>/<path>` | `<a href="...">` and resource registration | `resources/read` call |
| `mcp2web-tool://<tool-name>` | `<form action="...">` | `tools/call` with form data |

## Supported HTML Features

- Full HTML5 documents
- Inline `<style>` CSS (no external stylesheets)
- Forms with text inputs, textareas, selects, hidden fields, checkboxes
- Inline SVG graphics
- Basic `<script>` for client-side interactivity (within sandbox limits)

## Not Supported

- External resource loading (stylesheets, scripts, images, fonts)
- `allow-same-origin` in the sandbox (no localStorage, no cookies)
- Communication with the parent Electron window
- Node.js API access from page scripts
