# Content Organization Reference

Guide to organizing content in Zola: sections, pages, taxonomies, frontmatter.

## Contents

- [Sections vs Pages](#sections-vs-pages)
- [section Frontmatter](#section-frontmatter)
- [page Frontmatter](#page-frontmatter)
- [Asset Colocation](#asset-colocation)
- [URL Generation](#url-generation)
- [Internal Links](#internal-links)
- [Taxonomies](#taxonomies)
- [Multilingual](#multilingual)
- [Common Structures](#common-structures)

---

## Sections vs Pages

| Filename | Type | Template | Purpose |
|----------|------|----------|---------|
| `_index.md` | Section | `section.html` | Container/listing |
| `index.md` | Page | `page.html` | Page with colocated assets |
| `*.md` | Page | `page.html` | Single content |

```
content/
├── _index.md           # Section: /
├── about.md            # Page: /about/
├── blog/
│   ├── _index.md       # Section: /blog/
│   ├── post.md         # Page: /blog/post/
│   └── featured/
│       ├── index.md    # Page: /blog/featured/
│       └── hero.jpg    # Colocated asset
└── docs/
    ├── _index.md       # Section: /docs/
    └── getting-started/
        ├── _index.md   # Section: /docs/getting-started/
        └── install.md  # Page: /docs/getting-started/install/
```

---

## section Frontmatter

```toml
+++
title = "Blog"
description = "My articles"

# Sorting
sort_by = "date"              # "date", "title", "weight", "slug", "none"

# Pagination
paginate_by = 10
paginate_path = "page"        # /blog/page/2/

# Templates
template = "blog.html"        # Override section template
page_template = "post.html"   # Default for child pages

# Content
render = true                 # false = data-only
transparent = false           # Pass pages to parent
insert_anchor_links = "left"
in_search_index = true

# Feeds
generate_feeds = true

# Redirects
aliases = ["/articles/"]

[extra]
featured_image = "header.jpg"
+++
```

**Transparent sections:** `transparent = true` passes pages to parent section. Useful for year-based organization without yearly listings.

---

## page Frontmatter

```toml
+++
title = "My Post"
description = "SEO description"
date = 2024-01-15                    # NO QUOTES!
updated = 2024-02-01
authors = ["Alice"]

# URL Control
slug = "custom-url"                  # Override filename
path = "custom/full/path"            # Override entire path
aliases = ["/old-url/"]              # Redirects

# Visibility
draft = false
render = true

# Sorting
weight = 10                          # Lower = first

# Template
template = "custom.html"

# Search
in_search_index = true

[taxonomies]
tags = ["rust", "web"]
categories = ["programming"]

[extra]
featured = true
cover_image = "cover.jpg"
+++
```

**Date formats:**
```toml
date = 2024-01-15              # Correct
date = 2024-01-15T10:30:00Z    # With time
date = "2024-01-15"            # WRONG - string breaks sorting
```

**Date from filename:** `2024-01-15-hello.md` → `date = 2024-01-15`, `slug = "hello"`

---

## Asset Colocation

Use `index.md` (not `_index.md`) for pages with assets:

```
content/blog/my-post/
├── index.md              # The page
├── hero.jpg              # Image
├── diagram.svg           # SVG
└── data.json             # Data
```

**In Markdown:**
```markdown
![Hero](hero.jpg)
```

**In templates:**
```html
{% for asset in page.assets %}
    {% if asset is ending_with(".jpg") %}
        {% set img = resize_image(path=asset, width=800) %}
        <img src="{{ img.url }}">
    {% endif %}
{% endfor %}
```

---

## URL Generation

| Content Path | URL |
|--------------|-----|
| `content/about.md` | `/about/` |
| `content/blog/_index.md` | `/blog/` |
| `content/blog/post.md` | `/blog/post/` |
| `content/blog/my-post/index.md` | `/blog/my-post/` |
| `content/2024-01-15-hello.md` | `/hello/` |

**Slug vs Path:**
```toml
# Original: content/blog/my-file.md → /blog/my-file/

slug = "custom"
# Result: /blog/custom/

path = "tutorials/intro"
# Result: /tutorials/intro/ (ignores section)
```

---

## Internal Links

Use `@/` prefix for validated links:

```markdown
[About](@/about.md)
[Blog](@/blog/_index.md)
[Post](@/blog/post.md)
[Anchor](@/blog/post.md#section)
```

Build fails if target doesn't exist.

---

## Taxonomies

**Config:**
```toml
taxonomies = [
    {name = "tags", feed = true},
    {name = "categories", paginate_by = 10},
]
```

**Page frontmatter:**
```toml
[taxonomies]
tags = ["rust", "web"]
```

**Generated URLs:**
```
/tags/           # All tags
/tags/rust/      # Posts tagged "rust"
/tags/rust/atom.xml  # Feed (if enabled)
```

**Templates:**

List (`templates/tags/list.html` or `taxonomy_list.html`):
```html
{% for term in terms %}
<a href="{{ term.permalink }}">{{ term.name }} ({{ term.pages | length }})</a>
{% endfor %}
```

Single (`templates/tags/single.html` or `taxonomy_single.html`):
```html
<h1>{{ term.name }}</h1>
{% for page in term.pages %}
<a href="{{ page.permalink }}">{{ page.title }}</a>
{% endfor %}
```

**In page templates:**
```html
{% for tag in page.taxonomies.tags %}
<a href="{{ get_taxonomy_url(kind='tags', name=tag) }}">{{ tag }}</a>
{% endfor %}
```

---

## Multilingual

**Files:** `about.md` (default), `about.fr.md` (French)

**Config:**
```toml
default_language = "en"

[languages.fr]
title = "Mon Site"
taxonomies = [{name = "tags"}]

[languages.fr.translations]
read_more = "Lire la suite"
```

**Language switcher:**
```html
{% if page.translations %}
{% for trans in page.translations %}
<a href="{{ trans.permalink }}">{{ trans.lang | upper }}</a>
{% endfor %}
{% endif %}
```

---

## Common Structures

### Blog

```
content/
├── _index.md
└── blog/
    ├── _index.md               # sort_by = "date", paginate_by = 10
    ├── 2024-01-15-post.md
    └── featured/
        ├── index.md
        └── cover.jpg
```

**Verify:** `zola serve` → /blog/ shows posts sorted by date, /blog/featured/ shows page with image.

### Documentation

```
content/
├── _index.md
├── getting-started/
│   ├── _index.md               # weight = 1
│   ├── install.md              # weight = 1
│   └── quick-start.md          # weight = 2
├── guides/
│   ├── _index.md               # weight = 2
│   └── advanced/
│       └── _index.md
└── reference/
    ├── _index.md               # weight = 3
    └── api.md
```

Use `sort_by = "weight"` for manual ordering.

**Verify:** `zola serve` → sections appear in weight order, not alphabetical.

### Portfolio

```
content/
├── _index.md
├── projects/
│   ├── _index.md               # sort_by = "weight"
│   ├── project-a/
│   │   ├── index.md            # weight = 1
│   │   └── screenshot.png
│   └── project-b/
│       └── index.md            # weight = 2
└── about.md
```

**Verify:** `zola serve` → /projects/ shows project-a before project-b.
