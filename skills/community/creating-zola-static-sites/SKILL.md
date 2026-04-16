---
name: creating-zola-static-sites
description: Build static sites with the Zola generator (Rust-based SSG). Handles project initialization, config.toml configuration, Tera templates, Markdown content (sections via _index.md, pages via *.md), taxonomies, image processing, and deployment. Use for Zola project setup, Tera templating, _index.md structure, RSS/Atom feeds, syntax highlighting, or deployment to Netlify/Cloudflare/GitHub Pages/Vercel/Firebase. Also covers Zola+Astro hybrid architectures.
---

# Creating Zola Static Sites

Single-binary static site generator. Built-in Sass, image processing, Tera templating.

## Quick Start

```
New Project:
- [ ] zola init my-site && cd my-site
- [ ] Edit config.toml: set base_url
- [ ] IF using theme: skip next step (theme provides templates)
- [ ] IF no theme: copy templates from skill assets/
- [ ] zola serve → http://127.0.0.1:1111 loads
- [ ] zola check → exit code 0
```

## Commands

| Command | Purpose | Verify Success |
|---------|---------|----------------|
| `zola init` | Create project | `ls config.toml` exists |
| `zola serve` | Dev server :1111 | Browser loads site |
| `zola build` | Output to public/ | `ls public/index.html` exists |
| `zola check` | Validate links | Exit 0, no errors printed |

## Core: Sections vs Pages

**`_` prefix = section (listing); no prefix = page (content):**

| Filename | Type | Template | Example URL |
|----------|------|----------|-------------|
| `_index.md` | section | section.html | `/blog/` (listing) |
| `index.md` | page | page.html | `/about/` (with assets) |
| `post.md` | page | page.html | `/blog/post/` |

```
content/
├── _index.md        # section: /
├── about.md         # page: /about/
└── blog/
    ├── _index.md    # section: /blog/
    └── post.md      # page: /blog/post/
```

## Frontmatter

**section** (`_index.md`):
```toml
+++
title = "Blog"
sort_by = "date"        # date|title|weight|none
paginate_by = 10
+++
```

**page** (`*.md`):
```toml
+++
title = "My Post"
date = 2024-01-15       # NO QUOTES or sorting breaks
[taxonomies]
tags = ["rust"]
+++
```

## Internal Links

Build-validated with `@/` prefix:
```markdown
[About](@/about.md)
[Blog](@/blog/_index.md)
```

## Workflows

### Create Blog

```
Blog Setup:
- [ ] Create content/blog/_index.md with sort_by="date"
- [ ] Create post: content/blog/2024-01-15-hello.md
- [ ] IF multilingual: add blog/_index.fr.md per language
- [ ] zola serve → /blog/ shows listing (empty if no posts yet)
- [ ] zola serve → /blog/hello/ shows post
- [ ] IF pagination: add more posts than paginate_by to test
- [ ] zola check → passes
```

### Add Taxonomies

```
Taxonomy Setup:
- [ ] config.toml: taxonomies = [{name = "tags", feed = true}]
- [ ] Page frontmatter: [taxonomies] tags = ["value"]
- [ ] IF need categories: add {name = "categories"} to array
- [ ] IF term has spaces: use slugified URL (/tags/my-tag/)
- [ ] zola serve → /tags/ lists tags
- [ ] zola serve → /tags/rust/ shows posts
```

### Deploy

```
Production Deploy:
- [ ] zola check → passes (use --skip-external-links if slow)
- [ ] zola build → no errors
- [ ] ls public/index.html → exists
- [ ] IF feeds enabled: ls public/atom.xml → exists
```

## Reference Files

| Task | Reference | Load When User Asks About |
|------|-----------|---------------------------|
| Config | [config-reference.md](references/config-reference.md) | Feeds, taxonomies, highlighting, search, link checker |
| Templates | [tera-templates.md](references/tera-templates.md) | Filters, loops, variables, macros, shortcodes |
| Content | [content-organization.md](references/content-organization.md) | _index.md vs index.md, frontmatter, multilingual |
| Deploy | [deployment-guides.md](references/deployment-guides.md) | Netlify, Cloudflare, GitHub Actions, Vercel, Firebase |
| Hybrid | [astro-integration.md](references/astro-integration.md) | Zola+Astro, Firebase export, shared navigation |

## Assets

Copy from skill `assets/` directory:

| Asset | Use For |
|-------|---------|
| `templates/base.html` | Base layout |
| `templates/section.html` | Listings with pagination |
| `templates/page.html` | Articles with TOC |
| `templates/404.html` | Error page |
| `templates/shortcodes/` | youtube.html, figure.html |
| `config-templates/blog.toml` | Blog preset |
| `config-templates/docs.toml` | Docs preset |

## Common Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `date = "2024-01-15"` | `date = 2024-01-15` | Quoted dates are strings, break sorting |
| `[About](about.md)` | `[About](@/about.md)` | Missing @/ means no build validation |
| `index.md` in blog/ | `_index.md` in blog/ | Without `_` it's a page, not a section |
| `templates/blog.html` | `templates/section.html` | Zola looks for section.html by default |

## Troubleshooting

| Error | Fix | Verify |
|-------|-----|--------|
| Template not found | Check spelling; ensure templates/ exists | `ls templates/*.html` shows files |
| Dates not sorting | Use `date = 2024-01-15` (no quotes) | Posts appear in date order |
| Broken @/ links | Path from content/, include .md extension | `zola check` passes |
| Slow check | Skip external: `zola check --skip-external-links` | Completes in <10s |

**Debug:** `{{ __tera_context }}` in template shows all variables.

**Verbose:** `RUST_LOG=zola=info zola build`

## When Not to Use

- **Other SSGs:** Hugo, Jekyll, Eleventy use different syntax
- **General Markdown:** Questions without Zola context
- **Pure Astro:** Projects without Zola integration
