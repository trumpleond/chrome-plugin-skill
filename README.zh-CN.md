# chrome-plugin-skill

一个用于浏览器插件项目的 Codex / Claude Code 通用 Skill。

它可以在目标项目中生成 AI 约束规则文件，让 Codex、Claude Code、Cursor、Copilot 等 AI 编程助手在开发 Chrome / Edge / Firefox 插件时遵守更稳妥的默认规则：先分析、少权限、重隐私、不乱改 `manifest.json`、不主动提交代码，并考虑插件市场审核和后期国际化扩展。

## 这个 Skill 能做什么

运行脚本后，会在目标项目中创建或更新：

```text
AGENTS.md
CLAUDE.md
.cursorrules
.github/copilot-instructions.md
```

生成的规则会要求 AI：

- 修改代码前先分析项目结构。
- 不要在用户未明确要求时提交代码或 push。
- 把 `manifest.json` 当作高风险文件处理。
- 默认使用 Chrome Manifest V3。
- 不随意新增 `permissions` / `host_permissions`。
- 不为了省事使用 `<all_urls>`。
- 涉及 `cookies`、`proxy`、`webRequest`、`browsingData`、`declarativeNetRequest` 等敏感权限时，必须说明审核风险。
- 优先本地处理用户数据，减少隐私采集和远程上传。
- 不远程加载或执行插件代码。
- 插件文案默认按中文 / 英文和后期多语言扩展设计。
- 修改完成后输出测试步骤和插件市场审核风险变化。

## 项目记忆系统

如果使用 `--with-docs`，还会额外创建一套轻量级的 AI “入职手册”目录：

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

这套目录的作用是让项目知识持续沉淀，而不是只存在一次聊天里：

- `docs/context/`：记录长期背景、技术栈、权限策略、发布要求。
- `docs/evolution/`：记录每次重要变更的原因、决策、设计和验证方式。
- `docs/lessons_learned.md`：记录踩过的坑、审核风险和以后必须遵守的经验。

## 安装到 Codex

把整个目录复制到 Codex 的 skills 目录：

```powershell
Copy-Item -Recurse -Force . "$env:USERPROFILE\.codex\skills\chrome-plugin-skill"
```

重启 Codex 或新开会话后，搜索：

```text
chrome-plugin-skill
```

## 安装到 Claude Code

把整个目录复制到 Claude Code 的 skills 目录：

```powershell
Copy-Item -Recurse -Force . "$env:USERPROFILE\.claude\skills\chrome-plugin-skill"
```

重启 Claude Code 或新开会话后，使用：

```text
chrome-plugin-skill
```

## 基础用法

在这个 skill 目录中运行，给当前目录生成所有支持的规则文件：

```powershell
python scripts\write_chrome_plugin_rules.py
```

给指定插件项目生成规则文件：

```powershell
python scripts\write_chrome_plugin_rules.py --target D:\your-extension-project
```

只生成部分规则文件：

```powershell
python scripts\write_chrome_plugin_rules.py --targets codex claude cursor
```

同时创建 `docs` 项目记忆系统：

```powershell
python scripts\write_chrome_plugin_rules.py --with-docs
```

强制覆盖已有 docs 模板：

```powershell
python scripts\write_chrome_plugin_rules.py --with-docs --force-docs
```

强制覆盖整份规则文件：

```powershell
python scripts\write_chrome_plugin_rules.py --force
```

## 安全更新机制

默认情况下，脚本不会覆盖整份已有文件，而是只维护下面这个区块：

```text
<!-- CHROME_PLUGIN_AI_RULES_START -->
...
<!-- CHROME_PLUGIN_AI_RULES_END -->
```

这意味着你可以反复运行脚本。已有文件中位于 managed block 外面的内容会被保留。

## 在 AI 里怎么说

可以直接对 Codex 或 Claude Code 说：

```text
使用 chrome-plugin-skill，把浏览器插件开发约束规则写到当前项目。
```

如果还想创建项目记忆系统：

```text
使用 chrome-plugin-skill，把浏览器插件开发约束规则和 docs 项目记忆系统写到当前项目。
```

## 文件结构

```text
SKILL.md
README.md
README.zh-CN.md
agents/openai.yaml
scripts/write_chrome_plugin_rules.py
```

## 注意事项

- 生成的规则是项目开发约束，不是法律意见。
- Chrome / Edge / Firefox 插件市场政策会变化，正式发布前仍应核对最新官方要求。
- 脚本不会执行 `git add`、`git commit` 或 `git push`。
- docs 模板是轻量起点，后续应让 AI 随项目演进持续维护。
