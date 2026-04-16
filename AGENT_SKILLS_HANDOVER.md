# Handover: Universal Agent Skills Hub

## 🚀 Project Overview
**Goal:** Build a public GitHub repository that serves as a categorized, standardized hub for AI Agent Skills.
**Core Features:**
- **Universal Support:** Support for Gemini, Claude, Codex, and other LLMs.
- **Categorization:** Skills organized by function (e.g., Coding, Search, Finance).
- **Automated Ingestion:** Scripts to download and "folderize" skills from existing public repos (MCP servers, GitHub tools, etc.).

---

## 🔍 Research & Sources Found
We identified the following high-value sources to pull from:
1. **MCP (Model Context Protocol) Servers:** The emerging standard. Sources include `modelcontextprotocol/servers` on GitHub and `mcp.so`.
2. **Framework Tools:** Skills from LangChain, CrewAI, and AutoGen tool libraries.
3. **Curated Lists:** `CommandCodeAI/agent-skills` and the `Awesome AI Agents` repository.

---

## 🏗️ Planned Architecture
```text
/
├── skills/
│   ├── <category>/ (e.g., coding, research, social)
│   │   ├── <skill_name>/
│   │   │   ├── skill.json (Standardized Metadata)
│   │   │   ├── logic/ (Python/JS/Prompts)
│   │   │   └── README.md (Usage instructions)
├── ingester/
│   ├── ingester.py (The script that clones, extracts, and folderizes)
│   └── sources.yaml (List of URLs to scrape from)
└── templates/
    └── prompt_adapters/ (Templates for Gemini vs Claude vs Codex)
```

---

## 🛠️ Metadata Standard (`skill.json`)
Every skill will be standardized with:
- `name`: String
- `category`: String
- `source_url`: String
- `supported_models`: ["Gemini", "Claude", "Codex", "All"]
- `capabilities`: List of tools/functions
- `install_runtime`: "npx", "uv", "pip", etc.

---

## ⏭️ Next Actions for the Next Chat
1. **Initialize Workspace:** Set up the directory structure in the new folder.
2. **Develop the Ingester:** Write a Python script that takes a GitHub URL from `sources.yaml`, clones it to a temp folder, and moves the relevant assets into the Hub structure.
3. **Draft the README:** Create a high-quality landing page for the repo to "WOW" potential users.
4. **First Ingestion:** Start with the "Filesystem" and "Google Maps" MCP servers as the initial skills.
