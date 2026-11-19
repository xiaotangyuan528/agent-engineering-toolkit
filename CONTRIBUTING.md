# Contributing

Contributions must directly improve one of these areas:
1. Software system technical architecture design.
2. Software module detailed design.
3. Software technical implementation documentation.

Do not add PRDs, product proposals, project plans, management reports, test plans, user manuals or unrelated writing workflows.

## Skill changes
- Keep each Skill independently usable.
- Keep `skills/` as the single source of truth.
- Do not copy Skill source files into platform adapters.
- Use valid YAML frontmatter with `name` and `description`.
- Make trigger conditions and scope boundaries explicit.
- Never instruct an agent to invent source paths, symbols, line numbers, test results, performance figures or runtime facts.
- Update examples and templates only when they improve one of the three supported document types.

## Validation

```bash
python scripts/validate_package.py
python -m pip install -r requirements-docx.txt
python scripts/render_docx.py examples/sample-document.md -o /tmp/sample-document.docx
```
