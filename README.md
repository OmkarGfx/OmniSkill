# 🌀 OmniSkill-10K

> **The World's Largest Standardized Hub for AI Agent Capabilities.**

**OmniSkill** is a massive, curated repository designed to empower AI agents with a standardized set of 10,000+ skills across all major models (Gemini, Claude, GPT, etc.). By leveraging the **Model Context Protocol (MCP)** and advanced discovery techniques, we provide a unified logic layer for agents to interact with any system.

---

## 🛠️ Key Features

- **10,000+ Skills**: A comprehensive library covering coding, finance, social, system OS, and more.
- **Unified Metadata**: Every skill follows a strict JSON schema for seamless agentic integration.
- **Instruction-Complete**: Full `SKILL.md` instructions for zero-shot capability adoption.
- **Automated Ingestion**: Built-in discovery engine to keep the hub growing.

---

## 📂 Repository Structure

```text
/
├── skills/               # The Mega-Library (Categorized)
│   ├── mcp/              # Official Model Context Protocol servers
│   └── community/        # Discovered community skills (standardized)
├── ingester/             # The brain of the OmniSkill engine
├── templates/            # Standardization schemas and prompt adapters
└── README.md             # You are here
```

---

## 🚀 Getting Started

### 1. Ingest More Skills
To discover and add even more capabilities:
```bash
python ingester/ingester.py --query "your-topic"
```

### 2. Standardize New Skills
Drop your custom skills into `skills/community/` and use our templates to ensure compatibility.

---

## 📜 License
MIT License.
