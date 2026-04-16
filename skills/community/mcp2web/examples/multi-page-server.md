# Multi-Page mcp2web Server

A multi-page mcp2web server with navigation between pages and form submission. This example builds a simple contact book application.

## Project Structure

```
contact-book/
├── package.json
├── tsconfig.json
└── src/
    ├── pages.ts
    └── server.ts
```

## package.json

```json
{
  "name": "contact-book-mcp2web",
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

## tsconfig.json

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

## src/pages.ts

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

const styles = `
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #1a1a2e;
    color: #e0e0e0;
    line-height: 1.6;
    padding: 20px;
  }
  .container { max-width: 600px; margin: 0 auto; }
  h1 { color: #16c79a; margin-bottom: 16px; }
  a { color: #16c79a; text-decoration: none; }
  a:hover { text-decoration: underline; }
  nav {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    border-bottom: 1px solid #0f3460;
    padding-bottom: 12px;
  }
  nav a {
    padding: 6px 14px;
    background: #0f3460;
    border-radius: 6px;
  }
  nav a:hover { background: #16c79a; color: #1a1a2e; text-decoration: none; }
  .card {
    background: #16213e;
    border: 1px solid #0f3460;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
  }
  .card h2 { color: #16c79a; font-size: 1.1em; margin-bottom: 4px; }
  .card p { color: #a0a0b0; font-size: 0.95em; }
  label { display: block; color: #a0a0b0; font-size: 0.9em; margin-bottom: 4px; }
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 14px;
    background: #1a1a2e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    color: #e0e0e0;
    font-size: 1em;
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
  .empty { color: #666; font-style: italic; }
`;

function nav(): string {
  return `
    <nav>
      <a href="mcp2web://contact-book/home">Home</a>
      <a href="mcp2web://contact-book/contacts">Contacts</a>
      <a href="mcp2web://contact-book/add">Add Contact</a>
    </nav>
  `;
}

function page(title: string, body: string): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>${styles}</style>
</head>
<body>
  <div class="container">
    ${nav()}
    ${body}
  </div>
</body>
</html>`;
}

// --- Exported Page Functions ---

export function homePage(contactCount: number): string {
  return page("Contact Book", `
    <h1>Contact Book</h1>
    <div class="card">
      <p>You have <strong>${contactCount}</strong> contact${contactCount !== 1 ? "s" : ""}.</p>
      <p style="margin-top: 8px;">
        <a href="mcp2web://contact-book/contacts">View contacts</a> |
        <a href="mcp2web://contact-book/add">Add a contact</a>
      </p>
    </div>
  `);
}

interface Contact {
  name: string;
  email: string;
  phone: string;
}

export function contactsPage(contacts: Contact[]): string {
  const list = contacts.length === 0
    ? '<p class="empty">No contacts yet. <a href="mcp2web://contact-book/add">Add one!</a></p>'
    : contacts.map(c => `
        <div class="card">
          <h2>${escapeHtml(c.name)}</h2>
          <p>Email: ${escapeHtml(c.email)}</p>
          <p>Phone: ${escapeHtml(c.phone)}</p>
        </div>
      `).join("");

  return page("Contacts", `
    <h1>Contacts</h1>
    ${list}
  `);
}

export function addContactPage(): string {
  return page("Add Contact", `
    <h1>Add Contact</h1>
    <div class="card">
      <form action="mcp2web-tool://add-contact" method="POST">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" placeholder="Full name" required>

        <label for="email">Email</label>
        <input type="email" id="email" name="email" placeholder="email@example.com" required>

        <label for="phone">Phone</label>
        <input type="tel" id="phone" name="phone" placeholder="+1 234 567 8900">

        <button type="submit" class="btn">Save Contact</button>
      </form>
    </div>
  `);
}

export function contactSavedPage(name: string): string {
  return page("Contact Saved", `
    <h1>Contact Saved</h1>
    <div class="card">
      <p><strong>${escapeHtml(name)}</strong> has been added to your contacts.</p>
      <p style="margin-top: 12px;">
        <a href="mcp2web://contact-book/contacts">View all contacts</a> |
        <a href="mcp2web://contact-book/add">Add another</a>
      </p>
    </div>
  `);
}
```

## src/server.ts

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  homePage,
  contactsPage,
  addContactPage,
  contactSavedPage,
} from "./pages.js";

// In-memory contact store
interface Contact {
  name: string;
  email: string;
  phone: string;
}

const contacts: Contact[] = [];

const server = new McpServer({
  name: "contact-book",
  version: "1.0.0",
});

// --- Resources ---

server.resource("home", "mcp2web://contact-book/home", async (uri) => ({
  contents: [
    { uri: uri.href, mimeType: "text/html", text: homePage(contacts.length) },
  ],
}));

server.resource("contacts", "mcp2web://contact-book/contacts", async (uri) => ({
  contents: [
    { uri: uri.href, mimeType: "text/html", text: contactsPage(contacts) },
  ],
}));

server.resource("add", "mcp2web://contact-book/add", async (uri) => ({
  contents: [
    { uri: uri.href, mimeType: "text/html", text: addContactPage() },
  ],
}));

// --- Tools ---

server.tool(
  "add-contact",
  {
    name: z.string().max(100),
    email: z.string().email().max(254),
    phone: z.string().max(20),
  },
  async ({ name, email, phone }) => {
    contacts.push({ name, email, phone });
    return {
      content: [{ type: "text", text: contactSavedPage(name) }],
    };
  }
);

// --- Start ---

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Key Concepts Shown

### Navigation with `mcp2web://` links

The nav bar uses links that the Electron browser intercepts:

```html
<a href="mcp2web://contact-book/home">Home</a>
<a href="mcp2web://contact-book/contacts">Contacts</a>
```

When clicked, the browser calls `resources/read` with the target URI and renders the returned HTML.

### Form submission with `mcp2web-tool://` actions

The add contact form posts to a tool:

```html
<form action="mcp2web-tool://add-contact" method="POST">
  <input name="name" ...>
  <input name="email" ...>
  <input name="phone" ...>
</form>
```

The browser collects all form field values and calls `tools/call` with `{ name: "add-contact", arguments: { name, email, phone } }`.

### Dynamic resource content

Resources are functions, not static files. Each time a resource is read, the function runs and can return different content based on current state:

```typescript
server.resource("contacts", "mcp2web://contact-book/contacts", async (uri) => ({
  contents: [
    { uri: uri.href, mimeType: "text/html", text: contactsPage(contacts) },
  ],
}));
```

### Shared page templates

All pages share a common `page()` wrapper and `nav()` function from `pages.ts`, keeping styles and navigation consistent without duplication.

## How to Build and Run

```bash
npm install
npm run build
npm start
```
