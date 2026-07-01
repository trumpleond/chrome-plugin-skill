---
name: chrome-plugin-skill
description: Generate reusable AI constraint rule files and optional project memory docs for Chrome/Edge/Firefox browser extension projects. Use when the user wants to create, install, apply, refresh, or write common Codex/Claude/Cursor/Copilot rules, AI onboarding manuals, docs/context, docs/evolution, lessons_learned, browser plugin development constraints, extension store review rules, Manifest V3 permissions, privacy, i18n, or "Chrome 插件开发 AI 约束文件".
---

# Chrome Plugin Skill

Use this skill to write browser-extension development constraints into the current project. When the user wants an AI "onboarding manual" or reusable project memory, also scaffold docs templates.

## What It Generates

The bundled script writes the same managed rule block to common AI rule files:

- `AGENTS.md` for Codex-style project instructions
- `CLAUDE.md` for Claude Code project memory
- `.cursorrules` for Cursor
- `.github/copilot-instructions.md` for GitHub Copilot

With `--with-docs`, it also creates:

- `docs/context/chrome_extension_overview.md`
- `docs/context/tech_stack.md`
- `docs/context/release_checklist.md`
- `docs/lessons_learned.md`
- `docs/evolution/001_initial_setup.md`

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
- Read `docs/context` and `docs/lessons_learned.md` before coding when present
- Record important decisions in `docs/evolution` when the user wants project memory
- Report test steps and extension-store review risk after changes

## Workflow

1. Treat the user's current working directory as the target project unless they provide another path.
2. Run `scripts/write_chrome_plugin_rules.py` from this skill folder.
3. Add `--with-docs` when the user asks for an AI onboarding manual, project memory, evolution logs, reusable context, or lessons learned.
4. Do not run `git add`, `git commit`, or `git push` unless the user explicitly asks for a commit or push.
5. After generation, summarize which files were created, updated, or already existed.

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

Also scaffold project memory docs:

```bash
python scripts/write_chrome_plugin_rules.py --with-docs
```

Overwrite docs templates too:

```bash
python scripts/write_chrome_plugin_rules.py --with-docs --force-docs
```

Prefer the default managed-block behavior. It preserves any existing content outside:

```text
<!-- CHROME_PLUGIN_AI_RULES_START -->
...
<!-- CHROME_PLUGIN_AI_RULES_END -->
```
