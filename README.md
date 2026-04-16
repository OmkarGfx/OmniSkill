# 🌀 OmniSkill

> **The Infinite Hub for Standardized AI Agent Capabilities.**

**OmniSkill** is a massive, curated repository designed to empower AI agents with an ever-expanding universe of skills across all major models (Gemini, Claude, GPT, etc.). By leveraging the **Model Context Protocol (MCP)** and automated discovery, we provide a unified logic layer for agents to interact with the world at infinite scale.

---

## 🛠️ Key Features

- **Infinite Skill Expansion**: A core engine designed to handle thousands—and eventually millions—of high-quality skills.
- **Unified Metadata**: Every skill follows a strict JSON schema for seamless agentic integration.
- **Instruction-Complete**: Full `SKILL.md` instructions for zero-shot capability adoption.
- **Automated Ingestion**: High-performance discovery engine built for large-scale ingestion.

---

## 📂 Repository Structure

```text
/
├── skills/               # The Capability Library (Categorized)
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
