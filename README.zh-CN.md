# 软件技术交接助手

基于固定 Git 提交，为接手维护的研发编写一份 Markdown。先讲用途与架构，再用一个典型场景串起流程，最后链接到关键文件、函数、异常分支和源码依据。

| Skill | 何时使用 |
| --- | --- |
| `technical-implementation-documentation` | 写技术交接稿，包含总体架构、核心场景和详细实现。 |
| `technical-document-review` | 按需专项审查，核对阅读层次、图文、源码和完成语义。 |

在 Codex 中写作时调用 `$software-technical-docs-assistant:technical-implementation-documentation`。需要审查时再调用 `$software-technical-docs-assistant:technical-document-review`。

[安装说明](INSTALL.md) · [兼容性](COMPATIBILITY.md)
