# Software Technical Docs Assistant

Write a source-grounded engineering handoff for maintainers, then request a separate review when needed. The Codex plugin and the standalone distribution each include two skills.

| Skill | Purpose |
| --- | --- |
| `technical-implementation-documentation` | Write one Markdown handoff from a fixed Git revision. Start with the architecture and a representative scenario, then link to detailed implementation. |
| `technical-document-review` | Check the draft against the source baseline, including diagrams, navigation, asynchronous results and failure behavior. |

See [Installation](INSTALL.md) for Codex and standalone installation.

```text
$software-technical-docs-assistant:technical-implementation-documentation
Write a handoff for <module> based on the current commit.
```

```text
$software-technical-docs-assistant:technical-document-review
Review this handoff against the same commit. Fix confirmed findings in the draft.
```

[中文说明](README.zh-CN.md) · [Compatibility](COMPATIBILITY.md)
