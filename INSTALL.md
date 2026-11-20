# Installation

## Codex Plugin

```bash
codex plugin marketplace add xiaotangyuan528/agent-engineering-toolkit
codex plugin marketplace list
codex plugin add software-technical-docs-assistant@agent-engineering-toolkit
codex plugin list
```

If your CLI lacks `plugin add`, install from the Agent Engineering Toolkit marketplace in the desktop Plugins Directory. Start a new session, then use `$software-technical-docs-assistant:engineering-docs-router` to select the plugin Router explicitly. Natural-language selection is model-driven. See the [compatibility matrix](COMPATIBILITY.md).

## Independent Agent Skills

With Node.js, npm and npx available:

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --list
npx skills add xiaotangyuan528/agent-engineering-toolkit --all -g
npx skills add xiaotangyuan528/agent-engineering-toolkit --skill technical-architecture-design -g
```

The second and third commands are installation alternatives. Omit `-g` for project-local installation. Each installed skill includes its templates, converter and DOCX requirements. Paths are relative to the installed skill directory. Use the actual installed paths when invoking Python.

```bash
python -m pip install -r /path/to/installed/skill/requirements-docx.txt
python /path/to/installed/skill/scripts/render_docx.py input.md -o output.docx
```

Mermaid fences remain text in Word.

## Build and verify

```bash
python -m pip install -r requirements-build.txt -r requirements-docx.txt
python scripts/build.py
python scripts/validate_package.py
git diff --exit-code
```

Edit the canonical SKILL.md files under skills/, shared resources at the repository root, and plugin-source.json. Rebuild after editing and commit the generated files so installs from GitHub work without a build step.

[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) · [Vercel Skills CLI](https://github.com/vercel-labs/skills)
