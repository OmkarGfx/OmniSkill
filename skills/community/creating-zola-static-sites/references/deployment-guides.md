# Zola Deployment Guides

Platform-specific deployment configurations.

## Contents

- [Netlify](#netlify)
- [Cloudflare Pages](#cloudflare-pages)
- [GitHub Pages](#github-pages)
- [Vercel](#vercel)
- [Firebase](#firebase)
- [Docker](#docker)
- [Common Patterns](#common-patterns)

---

## Netlify

**netlify.toml:**
```toml
[build]
publish = "public"
command = "zola build"

[build.environment]
ZOLA_VERSION = "0.19.2"

[context.deploy-preview]
command = "zola build --base-url $DEPLOY_PRIME_URL"
```

```
Setup Checklist:
- [ ] Push to Git repository
- [ ] Connect repository in Netlify
- [ ] Build command: zola build
- [ ] Publish directory: public
- [ ] Environment: ZOLA_VERSION=0.19.2
- [ ] Deploy → check build logs for errors
- [ ] Visit deploy URL → site loads correctly
```

---

## Cloudflare Pages

**Settings:**
- Framework preset: Zola
- Build command: `zola build`
- Output directory: `public`
- Environment: `ZOLA_VERSION=0.19.2`

```
Setup Checklist:
- [ ] Connect Git repository
- [ ] Select Zola preset
- [ ] Add ZOLA_VERSION=0.19.2 variable
- [ ] Deploy → check build logs
- [ ] Visit *.pages.dev URL → site loads
```

---

## GitHub Pages

**.github/workflows/deploy.yml:**
```yaml
name: Deploy Zola

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Zola
        uses: taiki-e/install-action@v2
        with:
          tool: zola@0.19.2
      
      - name: Build
        run: zola build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
```

```
Setup Checklist:
- [ ] Create .github/workflows/deploy.yml
- [ ] Settings → Pages → Source: GitHub Actions
- [ ] Push to main branch
- [ ] Actions tab → workflow completes green
- [ ] Visit github.io URL → site loads
```

---

## Vercel

**vercel.json:**
```json
{
  "trailingSlash": true,
  "cleanUrls": true
}
```

**package.json:**
```json
{
  "scripts": {
    "install-zola": "curl -sL https://github.com/getzola/zola/releases/download/v0.19.2/zola-v0.19.2-x86_64-unknown-linux-gnu.tar.gz | tar xz",
    "build": "./zola build"
  }
}
```

```
Setup Checklist:
- [ ] Connect repository
- [ ] Framework: Other
- [ ] Build: npm run install-zola && npm run build
- [ ] Output: public
- [ ] Deploy → check build logs
- [ ] Visit *.vercel.app URL → site loads
```

---

## Firebase

**firebase.json:**
```json
{
  "hosting": {
    "public": "public",
    "ignore": ["firebase.json", "**/.*"],
    "rewrites": [{"source": "**", "destination": "/404.html"}],
    "headers": [
      {
        "source": "**/*.@(js|css)",
        "headers": [{"key": "Cache-Control", "value": "max-age=31536000"}]
      }
    ]
  }
}
```

```
Setup Checklist:
- [ ] npm install -g firebase-tools
- [ ] firebase login
- [ ] firebase init hosting
- [ ] zola build
- [ ] firebase deploy
- [ ] Visit firebase URL → site loads
```

---

## Docker

**Dockerfile:**
```dockerfile
FROM ghcr.io/getzola/zola:v0.19.1 as builder
COPY . /project
WORKDIR /project
RUN ["zola", "build"]

FROM nginx:alpine
COPY --from=builder /project/public /usr/share/nginx/html
EXPOSE 80
```

```bash
docker build -t my-site .
docker run -p 8080:80 my-site
```

---

## Common Patterns

**Base URL override:**
```bash
zola build --base-url $DEPLOY_URL
```

**Include drafts:**
```bash
zola build --drafts
```

**Link checking in CI:**
```yaml
- name: Check links
  run: zola check --skip-external-links
```

**Cache processed images:**
```yaml
cache:
  paths:
    - public/processed_images/
```
