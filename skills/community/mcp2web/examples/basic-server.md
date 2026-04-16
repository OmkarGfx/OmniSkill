# Basic mcp2web Server

A minimal single-page mcp2web server. This is the simplest possible server that serves one HTML page.

## Project Structure

```
hello-world/
├── package.json
├── tsconfig.json
└── src/
    └── server.ts
```

## package.json

```json
{
  "name": "hello-world-mcp2web",
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

## src/server.ts

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "hello-world",
  version: "1.0.0",
});

function homePage(): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hello World</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #1a1a2e;
      color: #e0e0e0;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }
    .card {
      background: #16213e;
      border-radius: 12px;
      padding: 40px;
      text-align: center;
      border: 1px solid #0f3460;
    }
    h1 { color: #16c79a; margin-bottom: 12px; }
    p { color: #a0a0b0; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Hello, mcp2web!</h1>
    <p>This is a minimal mcp2web server.</p>
  </div>
</body>
</html>`;
}

// Register a single page as a resource
server.resource("home", "mcp2web://hello-world/home", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "text/html", text: homePage() }],
}));

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## How to Build and Run

```bash
npm install
npm run build
npm start
```

The server communicates over stdio. The mcp2web Electron browser connects to it, calls `resources/list`, and renders the home page.

## What This Demonstrates

- Minimal project setup with TypeScript and the MCP SDK
- Single resource registration with `mcp2web://` URI scheme
- Complete HTML document with inline styles
- Dark theme following mcp2web conventions
- Stdio transport for communication with the Electron browser
