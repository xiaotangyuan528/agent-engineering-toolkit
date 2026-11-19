# Agent Engineering Toolkit

**Cross-agent technical documentation skills for software engineers.**

A focused, reusable documentation toolkit for three engineering disciplines:
1. **Software system architecture design**
2. **Software module detailed design**
3. **Software technical implementation documentation**

It provides five independent [Agent Skills](https://agentskills.io/) and a Codex-specific plugin package. The Skills are the canonical source; the Codex plugin references the same `skills/` directory rather than maintaining a second copy.

[中文说明](README.zh-CN.md) · [Installation](INSTALL.md) · [Contributing](CONTRIBUTING.md)

## Scope

| Document type | Main coverage | Typical readers |
|---|---|---|
| Technical architecture design | System boundaries, architecture views, module responsibilities, interactions, deployment, quality attributes, decisions and trade-offs | Architects, technical leads, cross-module engineers |
| Module detailed design | Responsibilities, interfaces, classes, data structures, state machines, concurrency, failure handling and resource lifecycle | Module developers, reviewers, integration engineers |
| Technical implementation documentation | Fixed code baseline, files, classes, functions, call chains, algorithms, state changes, concurrency, error paths and test evidence | Maintainers, engineers taking over a codebase, troubleshooters |

**Out of scope:** PRDs, product proposals, project plans, management reports, test plans, user manuals, marketing copy and general-purpose business writing.

## Five Skills

| Skill | Purpose |
|---|---|
| `engineering-docs-router` | Identifies the document type; checks audience, object, purpose, scope and evidence; routes to the relevant Skill |
| `technical-architecture-design` | System/subsystem architecture design |
| `module-detailed-design` | Implementable module interfaces, objects, states, concurrency and lifecycle design |
| `technical-implementation-documentation` | Actual code behavior against a fixed repository revision, with source/test traceability |
| `technical-document-review` | Reviews only the three supported technical document types |

Each Skill is independently installable. The router coordinates the other Skills when the host supports multi-Skill workflows; users can also invoke a specific Skill explicitly.

## Quick start: standard Agent Skills

Requires Node.js and `npx`.

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --all -g
```

Install one Skill only:

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --skill technical-architecture-design -g
```

List available Skills:

```bash
npx skills add xiaotangyuan528/agent-engineering-toolkit --list
```

The Vercel Skills CLI can prompt for compatible agents. To target a specific supported agent, use `-a <agent-id>`. The supported agent list depends on the CLI version; see the [CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

## Codex Plugin

The Codex plugin is specifically for Codex. Other agents should install the standard Skills above; they do not need this plugin.

```bash
codex plugin marketplace add xiaotangyuan528/agent-engineering-toolkit
codex plugin marketplace list
```

Then open the Plugins Directory in the ChatGPT desktop app, select **Agent Engineering Toolkit**, and install **Software Technical Docs Assistant**. Start a new session after installation.

For sparse Git-backed marketplace sources, Codex also supports:

```bash
codex plugin marketplace add https://github.com/xiaotangyuan528/agent-engineering-toolkit.git --sparse .agents/plugins --sparse plugins/codex
```

See [INSTALL.md](INSTALL.md). A repository marketplace is not the same as publication in the universal public plugin directory.

## Usage examples

### Architecture design

```text
Use the technical architecture design Skill to document this system.
Establish the system boundary, dependencies, key scenarios and quality attributes.
Then describe architecture views, module responsibilities, interactions, deployment,
decisions and risks. Do not invent performance or availability targets.
```

### Module detailed design

```text
Use the module detailed design Skill for <module>.
Cover responsibility boundaries, dependencies, interfaces, core classes and data
structures, state transitions, sequence, concurrency, error handling and lifecycle.
```

### Technical implementation documentation

```text
Analyze <module> from the current repository revision. Record the commit SHA,
trace the main call path, and explain files, classes, functions, data structures,
state changes, concurrency and failure paths. Cite source locations for key
conclusions; mark anything unverified as pending confirmation.
```

### Review

```text
Review this architecture, module design or implementation document.
Check correctness, boundaries, contracts, state completeness, concurrency,
failure paths, source evidence and diagram/text consistency. Classify findings
as P0/P1/P2/P3 and explain impact and remediation.
```

## Markdown and DOCX

```bash
python -m pip install -r requirements-docx.txt
python scripts/render_docx.py input.md -o output.docx
```

The converter supports headings, paragraphs, bold text, inline code, lists, tables and fenced code blocks. Mermaid blocks remain code text; they are not rendered as Word diagrams.

## Repository layout

```text
skills/                         # Canonical, single-source Skill definitions
plugins/codex/                  # Codex plugin manifest; skills/ links to ../../skills
.agents/plugins/marketplace.json
assets/templates/               # Architecture, module, implementation and ADR templates
scripts/                        # DOCX converter and package validator
examples/                       # Usage prompts and sample document
```

## Quality principles

- Architecture and detailed design describe the **target design**; implementation documentation describes **observed code behavior** for a fixed revision.
- Do not invent source paths, symbols, line numbers, test results, performance figures, SLAs or runtime behavior.
- Distinguish source-confirmed facts, test-confirmed facts, runtime evidence, code-derived inference and unknowns.
- Ask only for missing context that materially affects correctness.
- Use relevant sections and diagrams; do not fill templates mechanically.

See [CONTRIBUTING.md](CONTRIBUTING.md).
