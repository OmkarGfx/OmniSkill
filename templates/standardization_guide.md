# OmniSkill Standardization Guide

To maintain a high-quality, infinite scale library of agent capabilities, all skills in **OmniSkill** must follow these standardization rules.

## 📁 Directory Structure
Each skill must reside in its own folder within `skills/[category]/[skill-name]/`:
```text
[skill-name]/
├── skill.json    # Standardized metadata
├── SKILL.md      # Natural language instructions for the agent
└── logic/        # (Optional) Binary/Script/Source files
```

## 📄 Metadata (`skill.json`)
Every skill **must** have a `skill.json` with at least these fields:
```json
{
  "name": "unique-skill-name",
  "category": "category-name",
  "description": "Short internal description for indexing",
  "source_url": "Original repository URL",
  "supported_models": ["All"],
  "capabilities": ["Basename of primary tools"],
  "install_runtime": "npx | uv | pip | etc."
}
```

## 🧠 Instructions (`SKILL.md`)
The `SKILL.md` is the most important file. It should include:
1. **Name and YAML Frontmatter**: Metadata for discovery.
2. **When to use**: Clear triggers for the LLM.
3. **Usage Examples**: Concrete CLI or code examples.
4. **Options/Arguments**: Detailed reference for parameters.

## 🚀 Contribution Process
1. Use the `ingester/ingester.py` to draft a new skill from a GitHub repo.
2. Manually verify the `SKILL.md` clarity.
3. Update the `capabilities` in `skill.json`.
4. Submit a Pull Request!
