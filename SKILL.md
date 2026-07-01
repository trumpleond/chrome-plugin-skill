---
name: chrome-plugin-skill
description: Generate reusable AI constraint rule files for Chrome/Edge/Firefox browser extension projects. Use when the user wants to create, install, apply, refresh, or write common Codex/Claude/Cursor/Copilot rules for browser plugin development, extension store review, Manifest V3 permissions, privacy, i18n, or "Chrome 插件开发 AI 约束文件".
---

# Chrome Plugin Skill

Use this skill to write browser-extension development constraints into the current project.

## What It Generates

The bundled script writes the same managed rule block to common AI rule files:

- `AGENTS.md` for Codex-style project instructions
- `CLAUDE.md` for Claude Code project memory
- `.cursorrules` for Cursor
- `.github/copilot-instructions.md` for GitHub Copilot

The rules cover:

- Analyze before editing
- Do not commit unless the user explicitly asks
- Manifest V3 by default
- Avoid unnecessary `permissions` / `host_permissions`
- Avoid `<all_urls>` unless justified
- Explain review risk for sensitive permissions
- Prefer local processing and privacy minimization
- Do not remotely load or execute extension code
- Design plugin UI text for Chinese/English and future i18n expansion
- Report test steps and extension-store review risk after changes

## Workflow

1. Treat the user's current working directory as the target project unless they provide another path.
2. Run `scripts/write_chrome_plugin_rules.py` from this skill folder.
3. Do not run `git add`, `git commit`, or `git push` unless the user explicitly asks for a commit or push.
4. After generation, summarize which files were created or updated.

## Commands

Write all supported rule files to the current project:

```bash
python scripts/write_chrome_plugin_rules.py
```

Write to a specific project:

```bash
python scripts/write_chrome_plugin_rules.py --target /path/to/project
```

Write only selected files:

```bash
python scripts/write_chrome_plugin_rules.py --targets codex claude cursor
```

Overwrite whole target files instead of updating only the managed block:

```bash
python scripts/write_chrome_plugin_rules.py --force
```

Prefer the default managed-block behavior. It preserves any existing content outside:

```text
<!-- CHROME_PLUGIN_AI_RULES_START -->
...
<!-- CHROME_PLUGIN_AI_RULES_END -->
```

