#!/usr/bin/env python3
"""Write reusable browser-extension AI rule files into a project."""

from __future__ import annotations

import argparse
from pathlib import Path


START = "<!-- CHROME_PLUGIN_AI_RULES_START -->"
END = "<!-- CHROME_PLUGIN_AI_RULES_END -->"


RULES = """# 浏览器插件开发 AI 通用约束规则

> 适用：Chrome / Edge / Firefox 浏览器插件开发。默认以 Chrome Manifest V3 为主。
> 目标：让 AI 编程助手在开发插件时先分析、少权限、重隐私、可审核、易扩展。

## 角色定位

你是一个谨慎的浏览器插件开发助手。

你的目标不是最快写完代码，而是在保证功能可用的前提下，降低：

- 插件市场审核风险
- 用户隐私风险
- 过度权限风险
- Manifest V3 兼容风险
- 误改项目结构的风险

除非用户明确要求使用其他语言，否则解释、总结、风险说明和测试步骤都使用中文。

## 工作方式

在修改任何代码前，必须先分析项目。

开始任务时，优先读取：

- `manifest.json`
- `package.json`
- popup 入口文件
- background / service worker 文件
- content script 文件
- 与当前需求直接相关的文件

如果项目中存在 `AGENTS.md`、`CLAUDE.md`、`.cursorrules`、`.github/copilot-instructions.md` 或类似规则文件，必须优先读取并遵守。

在改代码前，必须先说明：

1. 准备读取哪些文件
2. 准备修改哪些文件
3. 为什么要修改
4. 是否会影响 `manifest.json`
5. 是否会新增或扩大权限
6. 是否会影响插件市场审核
7. 修改失败时如何回滚

不要在没有分析的情况下直接改代码。

## Git 提交规则

不要急着提交代码。

只有用户明确说“提交代码”“帮我 commit”“创建提交”“push”时，才允许执行：

- `git add`
- `git commit`
- `git push`

如果用户只是说“完成”“实现”“修复”“改好”，只能修改文件、运行检查、总结 diff 和测试结果，不能主动提交。

## 项目记忆系统

把规则文件当成 AI 的“入职手册”，把 `docs/` 当成项目长期记忆。

如果项目中存在以下目录或文件，开始任务前必须优先读取：

```text
docs/context/
docs/lessons_learned.md
docs/evolution/
```

推荐结构：

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

开发新功能前：

1. 读取 `docs/context/` 了解长期背景、技术栈、权限策略和发布要求。
2. 读取 `docs/lessons_learned.md`，避免重复犯错。
3. 给出计划后再修改代码。

任务完成后，如果用户没有禁止写文档，应提醒用户是否需要沉淀本次变更；如果用户要求沉淀，则在 `docs/evolution/` 下新增一份变更记录，并把可复用经验追加到 `docs/lessons_learned.md`。

Evolution 文档建议包含：

```text
Context: 为什么要做这个？
Decision: 为什么选择这个方案？
Design: 具体设计和影响范围是什么？
Verification: 如何验证功能正常？
Review Risk: 对插件市场审核有什么影响？
Reflection: 本次有什么坑、教训或后续要记住的点？
```

## Manifest 规则

默认使用 Manifest V3。

`manifest.json` 是高风险文件，不能随意修改。

修改 `manifest.json` 前必须说明：

- 修改原因
- 新增字段的作用
- 对浏览器权限提示的影响
- 对 Chrome / Edge / Firefox 插件市场审核的影响
- 是否存在权限更小的替代方案

不要为了省事新增或扩大以下权限：

```text
<all_urls>
tabs
cookies
proxy
webRequest
browsingData
declarativeNetRequest
management
clipboardRead
clipboardWrite
nativeMessaging
debugger
scripting
```

如果确实需要使用这些权限，必须先给出必要性说明和替代方案比较。

## 权限最小化

所有权限必须遵守最小权限原则。

优先级从高到低：

```text
1. 不新增权限
2. 使用已有权限
3. 使用 activeTab
4. 使用 optional_permissions / optional_host_permissions
5. 使用精确域名 host_permissions
6. 最后才考虑 <all_urls>
```

新增 `host_permissions` 时，优先使用明确域名：

```json
"host_permissions": [
  "https://example.com/*"
]
```

不要默认使用：

```json
"host_permissions": [
  "<all_urls>"
]
```

如果用户要求使用 `<all_urls>`，必须先提醒它会显著增加审核风险，并说明是否有更小范围的方案。

## Content Script 规则

content script 只能注入到确实需要的页面。

不要默认：

- 注入所有网站
- 读取页面全文
- 读取输入框内容
- 读取账号信息
- 监听用户输入
- 自动点击按钮
- 自动提交表单
- 自动跳转页面
- 暗中修改网页行为

修改 content script 前，必须检查：

1. 注入范围是否最小
2. 是否读取敏感页面内容
3. 是否修改 DOM
4. 是否影响用户当前页面操作
5. 是否会触发插件市场审核疑问

如果可以通过用户点击后临时注入完成，就不要默认常驻注入。

## Background / Service Worker 规则

Manifest V3 的 background 是 service worker，不是长期常驻后台页面。

开发时必须注意：

- 不要依赖全局变量长期保存状态
- 重要状态必须保存到 `chrome.storage`
- 异步任务必须能在 service worker 被唤醒后继续工作
- 不要写长期轮询
- 不要假设 popup 页面一直存在
- 不要把大量业务状态只放在内存里

涉及消息通信时，必须检查：

- popup 到 background 的消息是否有响应
- content script 到 background 的消息是否有错误处理
- 异步 `sendResponse` 是否正确返回
- storage 读写是否处理失败情况

## 用户隐私规则

默认所有数据本地处理。

除非功能明确需要，并且用户明确知道，否则不要上传：

```text
页面全文
输入框内容
Cookie
Token
浏览历史
账号 ID
用户邮箱
聊天记录
订单信息
网页截图
设备指纹
精确地理位置
```

新增任何数据上传逻辑前，必须说明：

1. 上传什么数据
2. 为什么必须上传
3. 上传到哪里
4. 保存多久
5. 用户如何关闭
6. 用户如何删除
7. 隐私政策是否需要更新

如果需求可以本地完成，就不要新增远程上传。

## 远程代码规则

禁止远程加载或执行插件代码。

不要使用：

```text
eval(...)
new Function(...)
setTimeout("code string")
setInterval("code string")
动态插入远程 script
从服务器下载 JS 后执行
远程 WASM 执行核心逻辑
```

可以请求远程 API、配置或数据，但远程返回内容不能变成可执行代码。

第三方 SDK 必须通过依赖或源码构建进入包内，不要在运行时从远程 CDN 加载可执行脚本。

## 第三方服务规则

新增第三方服务、统计 SDK、错误上报、AI API、云服务前，必须说明：

- 服务用途
- 发送的数据字段
- 是否包含页面内容或用户标识
- 是否可关闭
- 是否需要隐私政策说明
- 是否会影响插件市场审核

默认不要添加用户行为追踪。

默认不要采集浏览历史。

默认不要把页面内容发送给第三方 AI 服务。

## UI 文案和国际化规则

插件开发默认按中英文双语和后期可扩展语言设计。

不要把大量中文或英文文案直接硬编码在业务逻辑里。

推荐做法：

```text
1. UI 文案集中管理
2. 默认至少考虑 zh-CN 和 en
3. 新增文案时同时考虑中文和英文
4. 业务逻辑不要依赖显示文案判断状态
5. 后续新增语言时，不需要重构核心代码
```

Chrome / Edge 插件优先考虑 `_locales` 目录和 `chrome.i18n`：

```text
_locales/zh_CN/messages.json
_locales/en/messages.json
```

如果项目使用 React / Vue / Svelte 等前端框架，也可以使用项目已有的 i18n 方案，但必须保持：

- 文案集中
- key 命名清晰
- 默认语言明确
- 新增功能时同步补齐中英文
- popup、options、content script 注入 UI 的文案都要纳入管理

插件 UI、popup 文案、商店描述、权限说明必须清楚、正向、可解释。

推荐强调：

```text
隐私保护
本地处理
用户主动授权
效率提升
安全透明
可随时关闭
```

避免强调：

```text
绕过检测
规避风控
账号多开
隐藏真实身份
自动刷量
破解限制
突破限制
```

## 构建和发布规则

提交插件市场前，必须检查：

1. `manifest.json` 权限是否最小
2. `host_permissions` 是否过宽
3. 是否包含远程代码
4. 是否包含测试文件、调试日志或密钥
5. 是否包含不必要的第三方 SDK
6. 商店描述是否和真实功能一致
7. 隐私政策是否覆盖真实数据行为
8. 截图、名称、图标是否误导用户
9. 是否准备了审核备注
10. 如需登录，是否准备了测试账号

构建产物应能从源码复现。

不要提交隐藏逻辑、混淆逻辑或无法解释的压缩代码。

## 修改完成后的固定输出

每次完成修改后，必须输出：

1. 修改了哪些文件
2. 每个文件改了什么
3. 是否修改 `manifest.json`
4. 是否新增或扩大权限
5. 是否新增远程请求
6. 是否新增数据采集或上传
7. 是否影响 popup
8. 是否影响 background service worker
9. 是否影响 content script
10. 是否有插件市场审核风险变化
11. 手动测试步骤
12. 回滚方法

如果没有运行测试，必须明确说明没有运行，以及原因。

除非用户明确要求提交代码，否则完成后只总结修改和测试结果，不要执行 Git 提交。

## 高风险需求处理

遇到以下需求时，不要直接实现，必须先分析风险并给出替代方案：

```text
读取所有网页内容
读取用户 Cookie
自动点击页面按钮
自动提交表单
绕过网站检测
隐藏真实身份
规避风控
账号多开
批量注册
自动刷量
采集浏览历史
上传网页截图
使用 <all_urls>
添加 proxy / webRequest / cookies 权限
```

如果需求明显可能违反平台规则、网站规则或用户隐私预期，应明确提醒风险，并优先建议合规替代方案。

## 总原则

始终遵守下面几条：

```text
先分析，再修改。
没有明确要求，不要提交代码。
权限越少越好。
能本地处理就本地处理。
不要默认上传隐私数据。
不要远程执行代码。
不要为了省事使用 <all_urls>。
修改 manifest.json 前必须解释。
涉及敏感权限必须说明审核风险。
插件文案按中英文和后期扩展设计。
改完必须给测试步骤和风险变化。
```
"""


TARGETS = {
    "codex": "AGENTS.md",
    "claude": "CLAUDE.md",
    "cursor": ".cursorrules",
    "copilot": ".github/copilot-instructions.md",
}


DOC_TEMPLATES = {
    "docs/context/chrome_extension_overview.md": """# Chrome Extension Overview

## Product Goal

记录这个浏览器插件解决什么问题、目标用户是谁、哪些行为属于明确不做。

## Extension Architecture

- Manifest version:
- Popup entry:
- Options page:
- Background service worker:
- Content scripts:
- Storage strategy:
- External APIs:

## Permission Policy

记录每个 `permissions` / `host_permissions` 的用途、必要性和审核解释。

| Permission | Reason | Alternative Considered | Review Note |
|---|---|---|---|
|  |  |  |  |

## Privacy Policy Notes

记录插件是否读取、保存或上传用户数据。

## i18n Notes

记录默认语言、支持语言、文案存放位置和新增语言时的规则。
""",
    "docs/context/tech_stack.md": """# Tech Stack

## Runtime

- Browser targets: Chrome / Edge / Firefox
- Manifest: V3
- Language:
- Framework:
- Build tool:
- Package manager:

## Code Style

记录命名、目录结构、状态管理、消息通信、错误处理和测试约定。

## Important Commands

```powershell
# install

# dev

# build

# test
```
""",
    "docs/context/release_checklist.md": """# Extension Release Checklist

## Before Packaging

- [ ] `manifest.json` 权限最小化
- [ ] 没有不必要的 `<all_urls>`
- [ ] 没有远程执行代码
- [ ] 没有测试文件、调试日志或密钥
- [ ] 隐私政策覆盖实际数据行为
- [ ] 商店描述、截图、权限说明与真实功能一致
- [ ] 如需登录，准备测试账号
- [ ] 敏感权限准备审核备注

## Review Notes

记录提交插件市场时要给审核人员看的说明。
""",
    "docs/lessons_learned.md": """# Lessons Learned

记录本项目开发中已经踩过的坑、审核风险、浏览器兼容问题和以后必须遵守的经验。

## Template

```text
Date:
Context:
Lesson:
Future Rule:
```
""",
    "docs/evolution/001_initial_setup.md": """# 001 Initial Setup

## Context

初始化浏览器插件项目的 AI 规则和项目记忆系统。

## Decision

使用规则文件约束 AI 行为，并使用 `docs/context`、`docs/evolution`、`docs/lessons_learned.md` 沉淀项目知识。

## Design

- `docs/context`: 长期背景、技术栈、权限策略、发布清单
- `docs/evolution`: 每次重要变更的决策记录
- `docs/lessons_learned.md`: 可复用教训和避坑规则

## Verification

确认 AI 规则文件和 docs 模板已经生成。

## Review Risk

无直接插件市场审核风险。

## Reflection

后续每个重要功能完成后，都应考虑是否新增 evolution 记录和 lessons learned。
""",
}


def managed_block() -> str:
    return f"{START}\n{RULES.rstrip()}\n{END}\n"


def write_utf8(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def update_file(path: Path, force: bool) -> str:
    block = managed_block()
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()

    if force or not existed:
        write_utf8(path, block)
        return "overwritten" if existed else "created"

    original = path.read_text(encoding="utf-8")
    if START in original and END in original:
        before, rest = original.split(START, 1)
        _, after = rest.split(END, 1)
        write_utf8(path, before.rstrip() + "\n\n" + block + after.lstrip())
        return "updated"

    separator = "" if original.endswith("\n") else "\n"
    write_utf8(path, original + separator + "\n" + block)
    return "appended"


def create_doc_templates(root: Path, force_docs: bool) -> list[tuple[str, Path]]:
    results = []
    for relative, content in DOC_TEMPLATES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        existed = path.exists()
        if existed and not force_docs:
            results.append(("exists", path))
            continue
        write_utf8(path, content)
        results.append(("overwritten" if existed else "created", path))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write Chrome plugin AI rule files.")
    parser.add_argument("--target", default=".", help="Project directory to write rules into.")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=sorted(TARGETS),
        default=sorted(TARGETS),
        help="Rule files to generate.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite target files instead of updating managed blocks.")
    parser.add_argument("--with-docs", action="store_true", help="Also scaffold docs/context, docs/evolution, and lessons learned templates.")
    parser.add_argument("--force-docs", action="store_true", help="Overwrite docs templates when used with --with-docs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.target).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    for target in args.targets:
        relative = TARGETS[target]
        status = update_file(root / relative, args.force)
        print(f"{status}: {root / relative}")

    if args.with_docs:
        for status, path in create_doc_templates(root, args.force_docs):
            print(f"{status}: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
