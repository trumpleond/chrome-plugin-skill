# chrome-plugin-skill

A reusable Codex / Claude Code skill for generating browser-extension AI rule files and optional project memory docs.

[中文说明](README.zh-CN.md)

This skill writes a shared set of Chrome / Edge / Firefox extension development constraints into a target project so AI coding assistants follow safer defaults around Manifest V3, extension-store review, permissions, privacy, remote code, Git commits, i18n, and long-term project memory.

## What It Generates

Running the bundled script creates or updates these files in the target project:

```text
AGENTS.md
CLAUDE.md
.cursorrules
.github/copilot-instructions.md
```

The generated rules include:

- Analyze before editing code.
- Do not commit or push unless the user explicitly asks.
- Treat `manifest.json` as a high-risk file.
- Prefer Manifest V3.
- Avoid unnecessary `permissions` and `host_permissions`.
- Avoid `<all_urls>` unless clearly justified.
- Explain review risk for sensitive permissions such as `cookies`, `proxy`, `webRequest`, `browsingData`, and `declarativeNetRequest`.
- Prefer local processing and privacy minimization.
- Do not remotely load or execute extension code.
- Design plugin text for Chinese / English and future i18n expansion.
- Consider store-search keywords for extension names and descriptions without misleading users or keyword stuffing.
- Read `docs/context` and `docs/lessons_learned.md` before coding when present.
- Record important decisions in `docs/evolution` when project memory is requested.
- Report test steps and extension-store review risk after each change.

With `--with-docs`, the script also scaffolds an AI onboarding/manual style memory system:

```text
docs/
  context/
    chrome_extension_overview.md
    tech_stack.md
    release_checklist.md
  evolution/
    001_initial_setup.md
  lessons_learned.md
```

Use this when you want the project to accumulate decisions, review notes, and lessons instead of relying on chat history.

## Install

### Codex

Copy this folder to your Codex skills directory:

```powershell
Copy-Item -Recurse -Force . "$env:USERPROFILE\.codex\skills\chrome-plugin-skill"
```

Restart Codex or open a new session, then search for:

```text
chrome-plugin-skill
```

### Claude Code

Copy this folder to your Claude Code skills directory:

```powershell
Copy-Item -Recurse -Force . "$env:USERPROFILE\.claude\skills\chrome-plugin-skill"
```

Restart Claude Code or open a new session, then use:

```text
chrome-plugin-skill
```

## Usage

From this skill directory, write all supported rule files to the current directory:

```powershell
python scripts\write_chrome_plugin_rules.py
```

Write rules to a specific browser-extension project:

```powershell
python scripts\write_chrome_plugin_rules.py --target D:\your-extension-project
```

Write only selected rule files:

```powershell
python scripts\write_chrome_plugin_rules.py --targets codex claude cursor
```

Overwrite whole target files instead of updating only the managed block:

```powershell
python scripts\write_chrome_plugin_rules.py --force
```

Also create project memory docs:

```powershell
python scripts\write_chrome_plugin_rules.py --with-docs
```

Overwrite docs templates as well:

```powershell
python scripts\write_chrome_plugin_rules.py --with-docs --force-docs
```

## Managed Block

By default, the script preserves existing file content and only creates or updates this managed block:

```text
<!-- CHROME_PLUGIN_AI_RULES_START -->
...
<!-- CHROME_PLUGIN_AI_RULES_END -->
```

This makes the script safe to run repeatedly. Existing notes outside the managed block are kept.

## Skill Prompt Example

Use this in Codex or Claude Code:

```text
使用 chrome-plugin-skill，把浏览器插件开发约束规则写到当前项目。
```

Or:

```text
Use chrome-plugin-skill to generate Codex, Claude, Cursor, and Copilot rule files for this browser extension project.
```

To create the AI onboarding/manual docs too:

```text
使用 chrome-plugin-skill，把浏览器插件开发约束规则和 docs 项目记忆系统写到当前项目。
```

## Files

```text
SKILL.md
agents/openai.yaml
scripts/write_chrome_plugin_rules.py
```

## Notes

- The generated rules are project constraints, not legal advice.
- Extension-store policies change over time. For release-critical work, verify current Chrome / Edge / Firefox store requirements.
- The script does not run `git add`, `git commit`, or `git push`.
- The docs templates are intentionally lightweight; let the AI maintain them as the project evolves.
