# Zola config.toml Reference

Only `base_url` is required. All other options have sensible defaults.

## Contents

- [Required](#required)
- [Site Metadata](#site-metadata)
- [Build Options](#build-options)
- [Markdown](#markdown)
- [Syntax Highlighting](#syntax-highlighting)
- [Search](#search)
- [Link Checker](#link-checker)
- [Feeds](#feeds)
- [Taxonomies](#taxonomies)
- [Slugification](#slugification)
- [Languages](#languages)
- [Extra Variables](#extra-variables)
- [Complete Example](#complete-example)

---

## Required

```toml
base_url = "https://example.com"
# For subpath: base_url = "https://example.com/blog"
```

---

## Site Metadata

```toml
title = "My Site"
description = "Site description"
default_language = "en"
author = "John Doe"
```

Access in templates: `{{ config.title }}`

---

## Build Options

```toml
output_dir = "public"
compile_sass = true
minify_html = true
hard_link_static = false
generate_sitemap = true
generate_robots_txt = true
ignored_content = ["*.draft.md", "temp/*"]
ignored_static = ["*.psd"]
```

---

## Markdown

```toml
[markdown]
render_emoji = true
smart_punctuation = true
external_links_target_blank = true
external_links_no_follow = false
external_links_class = "external"
lazy_async_image = true
bottom_footnotes = true
github_alerts = true
definition_list = true
insert_anchor_links = "heading"  # "none", "left", "right", "heading"
```

---

## Syntax Highlighting

```toml
[markdown.highlighting]
highlight_code = true
style = "class"                   # "class" or "inline"
light_theme = "github-light"
dark_theme = "github-dark"
error_on_missing_language = true
```

**Themes:** `base16-ocean-dark`, `dracula`, `github-dark`, `github-light`, `gruvbox-dark`, `monokai`, `nord`, `one-dark`, `solarized-dark`

---

## Search

```toml
build_search_index = true

[search]
include_title = true
include_description = true
include_content = true
truncate_content_length = 300
index_format = "elasticlunr_json"
```

**Formats:** `elasticlunr_json`, `elasticlunr_javascript`, `fuse_json`, `fuse_javascript`

---

## Link Checker

```toml
[link_checker]
skip_prefixes = ["http://localhost"]
skip_anchor_prefixes = ["https://caniuse.com/"]
internal_level = "error"
external_level = "warn"
```

Run: `zola check` or `zola check --skip-external-links`

---

## Feeds

```toml
generate_feeds = true
feed_filenames = ["atom.xml", "rss.xml"]
feed_limit = 20
```

---

## Taxonomies

```toml
taxonomies = [
    {name = "tags"},
    {name = "categories", feed = true},
    {name = "authors", paginate_by = 10},
]
```

**Options:** `name` (required), `feed`, `paginate_by`, `paginate_path`, `render`

**In page frontmatter:**
```toml
[taxonomies]
tags = ["rust", "web"]
```

---

## Slugification

```toml
[slugify]
paths = "on"              # "on", "safe", "off"
taxonomies = "on"
anchors = "on"
paths_keep_dates = false
```

---

## Languages

### Single Language

```toml
default_language = "en"

[translations]
read_more = "Read more"
```

Access: `{{ trans(key="read_more") }}`

### Multiple Languages

```toml
default_language = "en"

[languages.fr]
title = "Mon Site"
generate_feeds = true
taxonomies = [{name = "tags"}]

[languages.fr.translations]
read_more = "Lire la suite"
```

**Files:** `about.md` (default), `about.fr.md` (French)

---

## Extra Variables

```toml
[extra]
logo = "/images/logo.svg"
show_reading_time = true

nav_items = [
    {label = "Home", url = "/"},
    {label = "Blog", url = "/blog/"},
]

[extra.social]
github = "username"
twitter = "username"
```

Access: `{{ config.extra.logo }}`, `{{ config.extra.social.github }}`

---

## Complete Example

```toml
base_url = "https://myblog.com"
title = "My Blog"
description = "Tech articles"
default_language = "en"

compile_sass = true
minify_html = true
generate_sitemap = true
generate_feeds = true
feed_filenames = ["atom.xml"]
build_search_index = true

[search]
include_title = true
include_content = true
truncate_content_length = 300

[markdown]
render_emoji = true
smart_punctuation = true
external_links_target_blank = true
insert_anchor_links = "heading"

[markdown.highlighting]
highlight_code = true
style = "class"
light_theme = "github-light"
dark_theme = "github-dark"

[link_checker]
internal_level = "error"
external_level = "warn"

taxonomies = [
    {name = "tags", feed = true},
    {name = "categories", paginate_by = 10},
]

[translations]
read_more = "Read more →"

[extra]
logo = "/images/logo.svg"
show_reading_time = true

nav_items = [
    {label = "Home", url = "/"},
    {label = "Blog", url = "/blog/"},
]

[extra.social]
github = "username"
```
