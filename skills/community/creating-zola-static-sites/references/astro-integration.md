# Zola + Astro Hybrid Architecture

Patterns for combining Zola content with Astro interactive components.

## Contents

- [When to Use](#when-to-use)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [Build Scripts](#build-scripts)
- [Shared Navigation](#shared-navigation)
- [Firebase Export](#firebase-export)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)

---

## When to Use

- Zola for content-heavy sections (blogs, docs)
- Astro for interactive components (dashboards, forms)
- Gradual migration between frameworks
- Different team expertise

---

## Directory Structure

```
project/
├── astro/
│   ├── src/
│   ├── public/
│   │   └── docs/           # Zola output
│   └── astro.config.mjs
├── zola/
│   ├── content/
│   ├── templates/
│   └── config.toml
├── package.json
└── shared/
    └── navigation.json
```

---

## Configuration

**zola/config.toml:**
```toml
base_url = "https://example.com/docs"
output_dir = "../astro/public/docs"
```

**astro/astro.config.mjs:**
```javascript
export default defineConfig({
  site: 'https://example.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
```

---

## Build Scripts

**package.json:**
```json
{
  "scripts": {
    "build": "npm-run-all build:zola build:astro",
    "build:zola": "cd zola && zola build",
    "build:astro": "cd astro && npm run build",
    "dev": "npm-run-all --parallel dev:zola dev:astro",
    "dev:zola": "cd zola && zola serve --port 1111",
    "dev:astro": "cd astro && npm run dev"
  }
}
```

```
Build Checklist:
- [ ] Build Zola first: cd zola && zola build
- [ ] Verify: ls ../astro/public/docs/index.html exists
- [ ] Build Astro: cd ../astro && npm run build
- [ ] Verify: ls dist/index.html exists
- [ ] Verify: ls dist/docs/index.html exists
- [ ] Test locally: npx serve dist
```

---

## Shared Navigation

**shared/navigation.json:**
```json
{
  "main": [
    {"label": "Home", "href": "/"},
    {"label": "Docs", "href": "/docs/"},
    {"label": "Blog", "href": "/blog/"}
  ]
}
```

**In Zola:**
```html
{% set nav = load_data(path="../shared/navigation.json") %}
{% for item in nav.main %}
<a href="{{ item.href }}">{{ item.label }}</a>
{% endfor %}
```

**In Astro:**
```astro
---
import nav from '../../shared/navigation.json';
---
{nav.main.map(item => <a href={item.href}>{item.label}</a>)}
```

---

## Firebase Export

Export Firestore to Zola Markdown:

**scripts/export.ts:**
```typescript
import { initializeApp, cert } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';
import * as fs from 'fs';

initializeApp({ credential: cert('./service-account.json') });
const db = getFirestore();

interface Post {
  title: string;
  content: string;
  date: Date;
  tags?: string[];
}

function toFrontmatter(post: Post): string {
  const lines = [
    '+++',
    `title = "${post.title.replace(/"/g, '\\"')}"`,
    `date = ${post.date.toISOString().split('T')[0]}`,
  ];
  if (post.tags?.length) {
    lines.push('[taxonomies]');
    lines.push(`tags = [${post.tags.map(t => `"${t}"`).join(', ')}]`);
  }
  lines.push('+++');
  return lines.join('\n');
}

async function exportPosts(outputDir: string) {
  const snapshot = await db.collection('posts').orderBy('date', 'desc').get();
  fs.mkdirSync(outputDir, { recursive: true });
  
  for (const doc of snapshot.docs) {
    const post = doc.data() as Post;
    const slug = post.title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    const date = post.date.toISOString().split('T')[0];
    const content = `${toFrontmatter(post)}\n\n${post.content}`;
    fs.writeFileSync(`${outputDir}/${date}-${slug}.md`, content);
  }
}

exportPosts('./zola/content/blog');
```

---

## CI/CD Pipeline

**.github/workflows/deploy.yml:**
```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Zola
        uses: taiki-e/install-action@v2
        with:
          tool: zola@0.19.2
      
      - name: Build Zola
        run: cd zola && zola build
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Build Astro
        run: cd astro && npm ci && npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./astro/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| 404 on Zola content | Wrong output path | Verify Zola output in astro/public/docs |
| Broken cross-links | Relative paths | Use absolute paths (`/docs/`, not `docs/`) |
| Trailing slash mismatch | Different settings | Set `trailingSlash: 'always'` in both |
| Build order issue | Astro before Zola | Always build Zola first |

**URL consistency:**
- Both use trailing slashes
- Base URLs match deployment path
- Use absolute paths for cross-system links
