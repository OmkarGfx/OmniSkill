# Tera Templates Reference

Complete Tera templating reference for Zola.

## Contents

- [Syntax](#syntax)
- [Variables](#variables)
- [Control Structures](#control-structures)
- [Filters](#filters)
- [Template Inheritance](#template-inheritance)
- [Macros](#macros)
- [Zola Variables](#zola-variables)
- [Zola Functions](#zola-functions)
- [Shortcodes](#shortcodes)
- [Common Patterns](#common-patterns)

---

## Syntax

```html
{{ variable }}        {# Output #}
{% statement %}       {# Control #}
{# comment #}         {# Comment #}
```

**Whitespace control:** `{%- trim -%}`, `{{- trim -}}`

---

## Variables

```html
{{ name }}
{{ user.name }}
{{ items[0] }}
{{ data[key] }}
```

**Operators:**
```html
{{ a + b }}  {{ a - b }}  {{ a * b }}  {{ a / b }}
{{ a == b }} {{ a != b }} {{ a < b }}  {{ a > b }}
{{ a and b }} {{ a or b }} {{ not a }}
{{ "Hello " ~ name }}    {# String concat #}
```

**Set variables:**
```html
{% set name = "value" %}
{% set_global counter = counter + 1 %}
```

---

## Control Structures

**Conditionals:**
```html
{% if condition %}
    ...
{% elif other %}
    ...
{% else %}
    ...
{% endif %}
```

**Tests:**
```html
{% if value is defined %}
{% if items is iterable %}
{% if text is containing("word") %}
{% if text is matching("^[a-z]+$") %}
```

**Loops:**
```html
{% for item in items %}
    {{ loop.index }}     {# 1-indexed #}
    {{ loop.first }}     {# true if first #}
    {{ loop.last }}      {# true if last #}
{% else %}
    No items.
{% endfor %}

{% for key, value in object %}
    {{ key }}: {{ value }}
{% endfor %}
```

---

## Filters

**String filters with examples:**

| Filter | Input | Output |
|--------|-------|--------|
| `lower` | `"Hello"` | `"hello"` |
| `upper` | `"Hello"` | `"HELLO"` |
| `title` | `"hello world"` | `"Hello World"` |
| `slugify` | `"Hello World!"` | `"hello-world"` |
| `truncate(length=10)` | `"Hello World"` | `"Hello W..."` |

```html
{{ text | lower }}
{{ text | upper }}
{{ text | title }}
{{ text | truncate(length=100) }}
{{ text | replace(from="old", to="new") }}
{{ text | split(pat=",") }}
{{ array | join(sep=", ") }}
{{ text | slugify }}
{{ html | striptags }}
{{ html | safe }}
```

**Number:**
```html
{{ num | round(precision=2) }}
{{ bytes | filesizeformat }}
```

**Array:**
```html
{{ items | length }}
{{ items | first }}
{{ items | last }}
{{ items | reverse }}
{{ items | sort(attribute="date") }}
{{ items | filter(attribute="draft", value=false) }}
{{ items | map(attribute="title") }}
{{ items | slice(start=0, end=5) }}
{{ items | json_encode() }}
```

**Date filters with examples:**

| Format | Input (2024-01-15) | Output |
|--------|-------------------|--------|
| `%Y-%m-%d` | date | `2024-01-15` |
| `%B %d, %Y` | date | `January 15, 2024` |
| `%A` | date | `Monday` |

```html
{{ date | date(format="%Y-%m-%d") }}
{{ date | date(format="%B %d, %Y") }}
```

Codes: `%Y` (2024), `%m` (01-12), `%d` (01-31), `%B` (January), `%A` (Monday)

**Default:**
```html
{{ value | default(value="fallback") }}
```

---

## Template Inheritance

**Base template:**
```html
<!DOCTYPE html>
<html>
<head>
    {% block head %}
    <title>{% block title %}{{ config.title }}{% endblock %}</title>
    {% endblock head %}
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

**Child template:**
```html
{% extends "base.html" %}

{% block title %}{{ page.title }}{% endblock %}

{% block head %}
    {{ super() }}    {# Include parent #}
    <link rel="stylesheet" href="/css/page.css">
{% endblock head %}

{% block content %}
<article>{{ page.content | safe }}</article>
{% endblock %}
```

---

## Macros

**Define:**
```html
{% macro post_card(post, show_date=true) %}
<article>
    <h2><a href="{{ post.permalink }}">{{ post.title }}</a></h2>
    {% if show_date %}<time>{{ post.date | date(format="%B %d, %Y") }}</time>{% endif %}
</article>
{% endmacro %}
```

**Use:**
```html
{% import "macros.html" as macros %}
{{ macros::post_card(post=post) }}
```

**Include:**
```html
{% include "header.html" %}
{% include "optional.html" ignore missing %}
```

---

## Zola Variables

**Global (all templates):**
```html
{{ config.base_url }}
{{ config.title }}
{{ config.extra.logo }}
{{ current_path }}
{{ current_url }}
{{ lang }}
```

**Page (page.html):**
```html
{{ page.title }}
{{ page.description }}
{{ page.content | safe }}
{{ page.summary | safe }}
{{ page.date }}
{{ page.updated }}
{{ page.permalink }}
{{ page.word_count }}
{{ page.reading_time }}
{{ page.toc }}
{{ page.taxonomies.tags }}
{{ page.extra.* }}
{{ page.lower }}           {# Previous page #}
{{ page.higher }}          {# Next page #}
{{ page.translations }}
```

**Section (section.html):**
```html
{{ section.title }}
{{ section.content | safe }}
{{ section.pages }}
{{ section.subsections }}
```

**Paginator:**
```html
{{ paginator.pages }}
{{ paginator.current_index }}
{{ paginator.number_pagers }}
{{ paginator.previous }}
{{ paginator.next }}
```

**Taxonomy list:**
```html
{{ taxonomy.name }}
{% for term in terms %}
    {{ term.name }}
    {{ term.permalink }}
    {{ term.pages | length }}
{% endfor %}
```

---

## Zola Functions

**URLs:**
```html
{{ get_url(path="blog/post") }}
{{ get_url(path="@/blog/_index.md") }}
{{ get_url(path="js/app.js", cachebust=true) }}
```

**Content:**
```html
{% set page = get_page(path="pages/about.md") %}
{% set section = get_section(path="blog/_index.md") %}
{% set section = get_section(path="blog/_index.md", metadata_only=true) %}
```

**Taxonomy:**
```html
{% set tags = get_taxonomy(kind="tags") %}
{{ get_taxonomy_url(kind="tags", name="rust") }}
```

**Data:**
```html
{% set data = load_data(path="data/config.json") %}
{% set data = load_data(url="https://api.example.com", format="json") %}
```

**Images:**
```html
{% set img = resize_image(path="photo.jpg", width=800, op="fit_width", format="webp") %}
<img src="{{ img.url }}" width="{{ img.width }}" height="{{ img.height }}">
```

Operations: `fill`, `fit_width`, `fit_height`, `fit`, `scale`
Formats: `auto`, `jpg`, `png`, `webp`, `avif`

**Hash:**
```html
integrity="sha384-{{ get_hash(path='static/js/app.js', sha_type=384, base64=true) }}"
```

---

## Shortcodes

**HTML shortcode** (`templates/shortcodes/youtube.html`):
```html
<iframe src="https://www.youtube-nocookie.com/embed/{{ id }}" allowfullscreen></iframe>
```

Usage: `{{ youtube(id="dQw4w9WgXcQ") }}`

**Body shortcode** (`templates/shortcodes/note.html`):
```html
<div class="note note-{{ type | default(value='info') }}">{{ body }}</div>
```

Usage:
```markdown
{% note(type="warning") %}
Important content.
{% end %}
```

---

## Common Patterns

**Navigation:**
```html
{% for item in config.extra.nav_items %}
<a href="{{ item.url }}" {% if current_path == item.url %}class="active"{% endif %}>
    {{ item.label }}
</a>
{% endfor %}
```

**Table of contents:**
```html
{% for h1 in page.toc %}
<li>
    <a href="{{ h1.permalink }}">{{ h1.title }}</a>
    {% if h1.children %}
    <ul>{% for h2 in h1.children %}
        <li><a href="{{ h2.permalink }}">{{ h2.title }}</a></li>
    {% endfor %}</ul>
    {% endif %}
</li>
{% endfor %}
```

**Pagination:**
```html
{% if paginator.previous %}<a href="{{ paginator.previous }}">← Newer</a>{% endif %}
<span>Page {{ paginator.current_index }} / {{ paginator.number_pagers }}</span>
{% if paginator.next %}<a href="{{ paginator.next }}">Older →</a>{% endif %}
```

**Debug:**
```html
{{ __tera_context }}
```
