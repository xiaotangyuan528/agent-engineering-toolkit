# Installation

## Standard Agent Skills

Requires Node.js/npm and `npx`.

List available Skills:

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --list
```

Install all Skills globally:

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --all -g
```

Install one Skill:

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --skill technical-architecture-design -g
```

Omit `-g` for project-level installation. Use `-a <agent-id>` to target supported agents; repeat `-a` for multiple agents. Add `-y` for non-interactive use. Agent support depends on the installed CLI version.

Official references:
- https://github.com/vercel-labs/skills
- https://github.com/vercel-labs/skills/blob/main/docs/commands.md

## Codex Plugin

The plugin is under `plugins/codex/`. Its `skills/` entry is a symbolic link to the canonical root `skills/` directory, avoiding duplicate Skill source files.

```bash
codex plugin marketplace add xiaotangyuan528/agent-engineering-toolkit
codex plugin marketplace list
```

Codex also supports sparse Git-backed marketplace sources:

```bash
codex plugin marketplace add https://github.com/xiaotangyuan528/agent-engineering-toolkit.git --sparse .agents/plugins --sparse plugins/codex
```

Then open Plugins Directory in the ChatGPT desktop app, select **Agent Engineering Toolkit**, and install **Software Technical Docs Assistant**. Start a new session after installation.

The marketplace CLI command adds/tracks the source; the desktop Plugins Directory is the documented surface for browsing and installing a plugin. Repository marketplace publication is separate from the universal public plugin directory.

Official reference: https://developers.openai.com/plugins/build/plugins

## DOCX conversion

```bash
python -m pip install -r requirements-docx.txt
python scripts/render_docx.py input.md -o output.docx
```

Mermaid blocks remain fenced code text and are not rendered as Word diagrams.

## Validate

```bash
python scripts/validate_package.py
```
