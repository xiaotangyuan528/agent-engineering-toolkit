# Agent Engineering Toolkit

面向软件研发人员的跨 Code Agent 专业技术文档 Skills 工具集。

本项目只覆盖三个领域：软件系统技术架构设计、软件模块详细设计、软件技术实现文档。不覆盖 PRD、产品方案、项目计划、领导汇报、测试方案、用户手册等其他文档。

## 五个 Skills

- `engineering-docs-router`：识别文档类型，确认读者、对象、目的、范围和依据，并路由到对应 Skill。
- `technical-architecture-design`：系统/子系统技术架构设计。
- `module-detailed-design`：模块接口、对象、状态、并发和生命周期详细设计。
- `technical-implementation-documentation`：基于固定代码版本的源码级实现说明。
- `technical-document-review`：对以上三类技术文档进行专业审查。

## 安装标准 Agent Skills

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --all -g
```

只安装架构设计 Skill：

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --skill technical-architecture-design -g
```

Vercel Skills CLI 支持交互选择兼容 Agent，也可用 `-a <agent-id>` 指定。支持列表以 CLI 当前版本为准。

## 安装 Codex Plugin

```bash
codex plugin marketplace add xiaotangyuan528/agent-engineering-toolkit
codex plugin marketplace list
```

随后在 ChatGPT 桌面端 Plugins Directory 中选择 **Agent Engineering Toolkit** Marketplace，安装 **Software Technical Docs Assistant**。

## DOCX 输出

```bash
python -m pip install -r requirements-docx.txt
python scripts/render_docx.py input.md -o output.docx
```

Mermaid 图保留为代码文本，不会自动渲染为 Word 图片。更多细节见 [INSTALL.md](INSTALL.md)。


[Installation](INSTALL.md) · [Compatibility](COMPATIBILITY.md) · [Changelog](CHANGELOG.md)
